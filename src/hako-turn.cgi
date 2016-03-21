#----------------------------------------------------------------------
# Ȣ����� ver2.30
# ������ʹԥ⥸�塼��(ver1.02)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# LitsȢ���Ѳ�¤
# ��¤�ԡ�MT
# ������ץȤκ����ۤ϶ػߤ��ޤ���
#----------------------------------------------------------------------

#����2�إå����κ�ɸ
my(@ax) = (0,-1, 1, 0, 0,-2,-1, 0, 1, 2, 1, 0,-1, 0, 1, 2, 3, 2, 1, 0,-1,-2,-3, -2,-1);
my(@ay) = (0, 0, 0, 1,-1, 0, 1, 2, 1, 0,-1,-2,-1, 3, 2, 1, 0,-1,-2,-3,-2,-1, 0,  1, 2);

#----------------------------------------------------------------------
# ��ο��������⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub newIslandMain {
    # �礬���äѤ��Ǥʤ��������å�
    if($HislandNumber >= $HmaxIsland) {
	unlock();
	tempNewIslandFull();
	return;
    }

    # ̾�������뤫�����å�
    if($HcurrentName eq '') {
	unlock();
	tempNewIslandNoName();
	return;
    }

    # ̾���������������å�
    if($HcurrentName =~ /[,\?\(\)\<\>\$]|^̵��$/) {
	# �Ȥ��ʤ�̾��
	unlock();
	tempNewIslandBadName();
	return;
    }

    # ̾���ν�ʣ�����å�
    if(nameToNumber($HcurrentName) != -1) {
	# ���Ǥ�ȯ������
	unlock();
	tempNewIslandAlready();
	return;
    }

    # password��¸��Ƚ��
    if($HinputPassword eq '') {
	# password̵��
	unlock();
	tempNewIslandNoPassword();
	return;
    }

    # ��ǧ�ѥѥ����
    if($HinputPassword2 ne $HinputPassword) {
	# password�ְ㤤
	unlock();
	tempWrongPassword();
	return;
    }

    # ����������ֹ�����
    $HcurrentNumber = $HislandNumber;
    $HislandNumber++;
    $Hislands[$HcurrentNumber] = makeNewIsland();
    my($island) = $Hislands[$HcurrentNumber];

    # �Ƽ���ͤ�����
    $island->{'name'} = $HcurrentName;
    $island->{'id'} = $HislandNextID;
    $HislandNextID ++;
    $island->{'absent'} = $HgiveupTurn - 3;
    $island->{'comment'} = '(̤��Ͽ)';
    $island->{'password'} = encode($HinputPassword);
$island->{'score'} = 0;
$island->{'monsnumber'} = 0;
$island->{'kouei'} = 0;
$island->{'kanei'} = 0;
$island->{'sen'} = 0;
$island->{'hei'} = 0;
$island->{'ino'} = 0;
my($monsnumber) = '';
my($i);
for($i = 0; $i < $HmonsterNumber; $i++) { $monsnumber .= '0,';}

    # �͸�����¾����
    estimate($HcurrentNumber);

    # �ǡ����񤭽Ф�
    writeIslandsFile($island->{'id'});
    logDiscover($HcurrentName); # ��

    # ����
    unlock();

    # ȯ������
    tempNewIslandHead($HcurrentName); # ȯ�����ޤ���!!
    islandInfo(); # ��ξ���
    islandMap(1); # ����Ͽޡ�owner�⡼��
}

# ����������������
sub makeNewIsland {
    # �Ϸ�����
    my($land, $landValue) = makeNewLand();

    # ������ޥ�ɤ�����
    my(@command, $i);
    for($i = 0; $i < $HcommandMax; $i++) {
	 $command[$i] = {
	     'kind' => $HcomDoNothing,
	     'target' => 0,
	     'x' => 0,
	     'y' => 0,
	     'arg' => 0
	 };
    }

    # ����Ǽ��Ĥ����
    my(@lbbs);
    for($i = 0; $i < $HlbbsMax; $i++) {
	 $lbbs[$i] = "0>>";
    }

    # ��ˤ����֤�
    return {
	'birth' => $HislandTurn,
	'land' => $land,
	'landValue' => $landValue,
	'command' => \@command,
	'lbbs' => \@lbbs,
	'money' => $HinitialMoney,
	'food' => $HinitialFood,
	'prize' => '0,0,',
    };
}

# ����������Ϸ����������
sub makeNewLand {
    # ���ܷ������
    my(@land, @landValue, $x, $y, $i);

    # ���˽����
    for($y = 0; $y < $HislandSize; $y++) {
	 for($x = 0; $x < $HislandSize; $x++) {
	     $land[$x][$y] = $HlandSea;
	     $landValue[$x][$y] = 0;
	 }
    }

    # �����4*4�˹��Ϥ�����
    my($center) = $HislandSize / 2 - 1;
    for($y = $center - 1; $y < $center + 3; $y++) {
	 for($x = $center - 1; $x < $center + 3; $x++) {
	     $land[$x][$y] = $HlandWaste;
	 }
    }

    # 8*8�ϰ����Φ�Ϥ�����
    for($i = 0; $i < 120; $i++) {
	 # �������ɸ
	 $x = random(6) + $center - 3;
	 $y = random(6) + $center - 3;

	 my($tmp) = countAround(\@land, $x, $y, $HlandSea, 5);
	 if(countAround(\@land, $x, $y, $HlandSea, 5) != 5){
	     # �����Φ�Ϥ������硢�����ˤ���
	     # �����Ϲ��Ϥˤ���
	     # ���Ϥ�ʿ�Ϥˤ���
	     if($land[$x][$y] == $HlandWaste) {
		 $land[$x][$y] = $HlandPlains;
		 $landValue[$x][$y] = 0;
	     } else {
		 if($landValue[$x][$y] == 1) {
                     $land[$x][$y] = $HlandWaste;
                     $landValue[$x][$y] = 0;
		 } else {
		     $landValue[$x][$y] = 1;
		 }
	     }
	 }
    }

    # ������
    my($count) = 0;
    while($count < 4) {
	 # �������ɸ
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # ���������Ǥ˿��Ǥʤ���С�������
	 if($land[$x][$y] != $HlandForest) {
	     $land[$x][$y] = $HlandForest;
	     $landValue[$x][$y] = 5; # �ǽ��500��
	     $count++;
	 }
    }

    # Į����
    $count = 0;
    while($count < 2) {
	 # �������ɸ
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # ����������Į�Ǥʤ���С�Į����
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest)) {
	     $land[$x][$y] = $HlandTown;
	     $landValue[$x][$y] = 5; # �ǽ��500��
	     $count++;
	 }
    }

    # ������
    $count = 0;
    while($count < 1) {
	 # �������ɸ
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # ����������Į�Ǥʤ���С�Į����
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest)) {
	     $land[$x][$y] = $HlandMountain;
	     $landValue[$x][$y] = 0; # �ǽ�Ϻη���ʤ�
	     $count++;
	 }
    }

    # ���Ϥ���
    $count = 0;
    while($count < 1) {
	 # �������ɸ
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # ����������Į�����Ǥʤ���С�����
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest) &&
	    ($land[$x][$y] != $HlandMountain)) {
	     $land[$x][$y] = $HlandBase;
	     $landValue[$x][$y] = 0;
	     $count++;
	 }
    }

    return (\@land, \@landValue);
}

#----------------------------------------------------------------------
# �����ѹ��⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub changeMain {
    # id����������
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    my($flag) = 0;

    # �ѥ���ɥ����å�
    if($HoldPassword eq $HspecialPassword) {
	# �ü�ѥ����
	$island->{'money'} = 9999;
	$island->{'food'} = 9999;
    } elsif(!checkPassword($island->{'password'},$HoldPassword)) {
	# password�ְ㤤
	unlock();
	tempWrongPassword();
	return;
    }

    # ��ǧ�ѥѥ����
    if($HinputPassword2 ne $HinputPassword) {
	# password�ְ㤤
	unlock();
	tempWrongPassword();
	return;
    }

    if($HcurrentName ne '') {
	# ̾���ѹ��ξ��	
	# ̾���������������å�
	if($HcurrentName =~ /[,\?\(\)\<\>]|^̵��$/) {
	    # �Ȥ��ʤ�̾��
	    unlock();
	    tempNewIslandBadName();
	    return;
	}

	# ̾���ν�ʣ�����å�
	if(nameToNumber($HcurrentName) != -1) {
	    # ���Ǥ�ȯ������
	    unlock();
	    tempNewIslandAlready();
	    return;
	}

	if($island->{'money'} < $HcostChangeName) {
	    # �⤬­��ʤ�
	    unlock();
	    tempChangeNoMoney();
	    return;
	}

	# ���
	if($HoldPassword ne $HspecialPassword) {
	    $island->{'money'} -= $HcostChangeName;
$island->{'shuu'}-= $HcostChangeName;
	}

	# ̾�����ѹ�
	logChangeName($island->{'name'}, $HcurrentName);
	$island->{'name'} = $HcurrentName;
	$flag = 1;
    }

    # password�ѹ��ξ��
    if($HinputPassword ne '') {
	# �ѥ���ɤ��ѹ�
	$island->{'password'} = encode($HinputPassword);
	$flag = 1;
    }

    if(($flag == 0) && ($HoldPassword ne $HspecialPassword)) {
	# �ɤ�����ѹ�����Ƥ��ʤ�
	unlock();
	tempChangeNothing();
	return;
    }

    # �ǡ����񤭽Ф�
    writeIslandsFile($HcurrentID);
    unlock();

    # �ѹ�����
    tempChange();
}
sub changeOwner {
  # id����������
  $HcurrentNumber = $HidToNumber{$HcurrentID};
  my($island) = $Hislands[$HcurrentNumber];
  my($flag) = 0;

  if(!checkPassword($island->{'password'},$HoldPassword)) {
    # password�ְ㤤
    unlock();
    tempWrongPassword();
    return;
  }
  # �����ʡ�̾���ѹ�
  $HcurrentOwnerName =~ s/</&lt;/g;;
  $HcurrentOwnerName =~ s/>/&gt;/g;;
  $island->{'ownername'} = $HcurrentOwnerName;
  $flag = 1;

  # �ǡ����񤭽Ф�
  writeIslandsOwner($HcurrentID);
  unlock();

  # �ѹ�����
  tempChange();
}
sub changeFlag {
  # id����������
  $HcurrentNumber = $HidToNumber{$HcurrentID};
  my($island) = $Hislands[$HcurrentNumber];
  my($flag) = 0;

  if(!checkPassword($island->{'password'},$HoldPassword)) {
    # password�ְ㤤
    unlock();
    tempWrongPassword();
    return;
  }
  # �����ʡ�̾���ѹ�
  $HcurrentFlagName =~ s/</&lt;/g;;
  $HcurrentFlagName =~ s/>/&gt;/g;;
  $island->{'flagname'} = $HcurrentFlagName;
  $flag = 1;

  # �ǡ����񤭽Ф�
  writeIslandsFlag($HcurrentID);
  unlock();

  # �ѹ�����
  tempChange();
}

#----------------------------------------------------------------------
# ������ʹԥ⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub turnMain {
    # �ǽ��������֤򹹿�
    $HislandLastTime += $HunitTime;

    # ���ե��������ˤ��餹
    my($i, $j, $s, $d);
    for($i = ($HlogMax - 1); $i >= 0; $i--) {
	$j = $i + 1;
	my($s) = "${HdirName}/hakojima.log$i";
	my($d) = "${HdirName}/hakojima.log$j";
	unlink($d);
	rename($s, $d);
    }

    # ��ɸ�������
    makeRandomPointArray();

    # �������ֹ�
    $HislandTurn++;

    # ���ַ��
    my(@order) = randomArray($HislandNumber);

    # ����������ե�����
    for($i = 0; $i < $HislandNumber; $i++) {
	estimate($order[$i]);
	income($Hislands[$order[$i]]);

	# �����󳫻����ο͸������
	$Hislands[$order[$i]]->{'oldPop'} = $Hislands[$order[$i]]->{'pop'};
    }
    for($i = 0; $i < $HislandNumber; $i++) {
	doMonMove($Hislands[$order[$i]]);
    }
    # ���ޥ�ɽ���
    for($i = 0; $i < $HislandNumber; $i++) {
	# �����1�ˤʤ�ޤǷ����֤�
	while(doCommand($Hislands[$order[$i]]) == 0){};
    }

    # ��Ĺ�����ñ�إå����ҳ�
    for($i = 0; $i < $HislandNumber; $i++) {
estimate($order[$i]);
	doEachHex($Hislands[$order[$i]]);
doStation($Hislands[$order[$i]]); # �ż֤α��Է׻�
      
    }
$sek =0;
$seu ="";
$hek =0;
$heu ="";
$ink=0;
$inu ="";
$tei =0;
$teu ="";
$kyo =0;
$kyu ="";
$muo=0;
$muu ="";
$noo =99;
$noi =0;
$koi =0;
$koo =4;
$ooo =2;
$ooi =0;
$doi =0;
$doo =2;
$deo =2;
$dei =0;
$moo =0;
$moi =0;
$joo =0;
$joi =0;
$hoo =0;
$hoi =0;
$goo =0;
$goi =0;
$soo =0;
$soi =0;
$loo =0;
$loi =0;
$yoo =0;
$yoi =0;
$eoo =0;
$eoi =0;
$aoo =0;
$aoi =0;
$ioo =0;
$ioi =0;
$uoo =0;
$uoi =0;
$foo =0;
$foi =0;
$too =0;
$toi =0;
    # �����ν���
    my($remainNumber) = $HislandNumber;
    my($island);
    for($i = 0; $i < $HislandNumber; $i++) {
estimate($order[$i]);
	$island = $Hislands[$order[$i]];
	doIslandProcess($order[$i], $island); 

	# ����Ƚ��
	if($island->{'dead'} == 1) {
	    $island->{'pop'} = 0;
	    $remainNumber--;
	} elsif($island->{'pop'} == 0) {
	    $island->{'dead'} = 1;
	    $remainNumber--;
	    # ���ǥ�å�����
	    my($tmpid) = $island->{'id'};
	    logDead($tmpid, $island->{'name'});
	    unlink("island.$tmpid");
	}
if ($island->{'sen'} > 0){
$sek++;
$seu .="$island->{'name'}��,";
}
if ($island->{'hei'} == 1){
$hek++;
$heu .="$island->{'name'}��,";
}
if ($island->{'ino'} == 1){
$ink++;
$inu .="$island->{'name'}��,";
}
if ($island->{'sen'} == 21){
$kyo++;
$kyu .="$island->{'name'}��,";
}elsif ($island->{'sen'} == 11){
$tei++;
$teu .="$island->{'name'}��,";
}elsif ($island->{'sen'} == 1){
$muo++;
$muu .="$island->{'name'}��,";
}
$ari=$island->{'shoku'};
if ($ari > $noo){
$noo = $ari;
$noi = $island->{'id'};
$niou ="$island->{'name'}��";
}
if ($island->{'factory'}> $koo){
$koo = $island->{'factory'};
$koi = $island->{'id'};
$kiou ="$island->{'name'}��";
}
if ($island->{'onse'} > $ooo){
$ooo = $island->{'onse'};
$ooi = $island->{'id'};
$oiou ="$island->{'name'}��";
}
if ($island->{'dou'} > $doo){
$doo = $island->{'dou'};
$doi = $island->{'id'};
$diou ="$island->{'name'}��";
}
if ($island->{'dep'} > $deo){
$deo = $island->{'dep'};
$dei = $island->{'id'};
$deou ="$island->{'name'}��";
}
if ($island->{'monka'}>$moo){
$moo = $island->{'monka'};
$moi = $island->{'id'};
$moou ="$island->{'name'}��";
}
if ($island->{'Jous'}>$joo){
$joo = $island->{'Jous'};
$joi = $island->{'id'};
$joou ="$island->{'name'}��";
}
if ($island->{'hatud'}>$hoo){
$hoo = $island->{'hatud'};
$hoi = $island->{'id'};
$hoou ="$island->{'name'}��";
}
if ($island->{'gomi'}>$goo){
$goo = $island->{'gomi'};
$goi = $island->{'id'};
$goou ="$island->{'name'}��";
}
if ($island->{'seki'}>$soo){
$soo = $island->{'seki'};
$soi = $island->{'id'};
$soou ="$island->{'name'}��";
}
if ($island->{'lands'}>$loo){
$loo = $island->{'lands'};
$loi = $island->{'id'};
$loou ="$island->{'name'}��";
}
if ($island->{'forest'}>$foo){
$foo = $island->{'forest'};
$foi = $island->{'id'};
$foou ="$island->{'name'}��";
}
if ($island->{'stay'}>$too){
$too = $island->{'stay'};
$toi = $island->{'id'};
$toou ="$island->{'name'}��";
}
$island->{'yhuu'} += $island->{'shuu'};
if(($HislandTurn % 10) == 0) {
if ($island->{'yhuu'}>$yoo){
$yoo = $island->{'yhuu'};
$yoi = $island->{'id'};
$yoou ="$island->{'name'}��";
}
$island->{'yhuu'}=0;
}
if ($island->{'money'}>$eoo){
$eoo = $island->{'money'};
$eoi = $island->{'id'};
$eoou ="$island->{'name'}��";
}
if ($island->{'area'}>$aoo){
$aoo = $island->{'area'};
$aoi = $island->{'id'};
$aoou ="$island->{'name'}��";
}
if ($island->{'sigoto'}>$ioo){
$ioo = $island->{'sigoto'};
$ioi = $island->{'id'};
$ioou ="$island->{'name'}��";
}
if ($island->{'mountain'}>$uoo){
$uoo = $island->{'mountain'};
$uoi = $island->{'id'};
$uoou ="$island->{'name'}��";
}
        }
    for($i = 0; $i < $HislandNumber; $i++) {
	$island = $Hislands[$order[$i]];
if($island->{'id'} == $koi){
$island->{'king'} += 1;
if($koi != $kioa){
logkoukae($island->{'id'}, $island->{'name'});
$kioa = $koi;
}
}
if($island->{'id'} == $noi){
$island->{'king'} += 1;
if($noi != $nioa){
lognoukae($island->{'id'}, $island->{'name'});
$nioa = $noi;
}
}
if($island->{'id'} == $ooi){
$island->{'king'} += 1;
if($ooi != $oioa){
logooukae($island->{'id'}, $island->{'name'});
$oioa = $ooi;
}
}
if($island->{'id'} == $doi){
$island->{'king'} += 1;
if($doi != $dioa){
logdoukae($island->{'id'}, $island->{'name'});
$dioa = $doi;
}
}
if($island->{'id'} == $dei){
$island->{'king'} += 1;
if($dei != $deoa){
logdeukae($island->{'id'}, $island->{'name'});
$deoa = $dei;
}
}
if($island->{'id'} == $foi){
$island->{'king'} += 1;
if($foi != $fioa){
logfoukae($island->{'id'}, $island->{'name'});
$fioa = $foi;
}
}
if($island->{'id'} == $toi){
$island->{'king'} += 1;
if($toi != $tioa){
logtoukae($island->{'id'}, $island->{'name'});
$tioa = $toi;
}
}
if($island->{'id'} == $moi){
$island->{'king'} += 1;
if($moi != $mooa){
logmoukae($island->{'id'}, $island->{'name'});
$mooa = $moi;
}
}
if($island->{'id'} == $joi){
$island->{'king'} += 1;
if($joi != $jooa){
logjoukae($island->{'id'}, $island->{'name'});
$jooa = $joi;
}
}
if($island->{'id'} == $hoi){
$island->{'king'} += 1;
if($hoi != $hooa){
loghoukae($island->{'id'}, $island->{'name'});
$hooa = $hoi;
}
}
if($island->{'id'} == $goi){
$island->{'king'} += 1;
if($goi != $gooa){
loggoukae($island->{'id'}, $island->{'name'});
$gooa = $goi;
}
}
if($island->{'id'} == $soi){
$island->{'king'} += 1;
if($soi != $sooa){
logsoukae($island->{'id'}, $island->{'name'});
$sooa = $soi;
}
}
if($island->{'id'} == $loi){
$island->{'king'} += 1;
if($loi != $looa){
logloukae($island->{'id'}, $island->{'name'});
$looa = $loi;
}
}
if($island->{'id'} == $yoi){
$island->{'king'} += 1;
if($yoi != $yooa){
logyoukae($island->{'id'}, $island->{'name'});
$yooa = $yoi;
}
}
if($island->{'id'} == $eoi){
$island->{'king'} += 1;
if($eoi != $eooa){
logeoukae($island->{'id'}, $island->{'name'});
$eooa = $eoi;
}
}
if($island->{'id'} == $aoi){
$island->{'king'} += 1;
if($aoi != $aooa){
logaoukae($island->{'id'}, $island->{'name'});
$aooa = $aoi;
}
}
if($island->{'id'} == $ioi){
$island->{'king'} += 1;
if($ioi != $iooa){
logioukae($island->{'id'}, $island->{'name'});
$iooa = $ioi;
}
}
if($island->{'id'} == $uoi){
$island->{'king'} += 1;
if($uoi != $uooa){
loguoukae($island->{'id'}, $island->{'name'});
$uooa = $uoi;
}
}
}
$boi = 0;
$boo = 0;
    for($i = 0; $i < $HislandNumber; $i++) {
	$island = $Hislands[$order[$i]];
if ($island->{'king'} > $boo){
$boo = $island->{'king'};
$boi = $island->{'id'};
$biou ="$island->{'name'}��";
}
}
    for($i = 0; $i < $HislandNumber; $i++) {
	$island = $Hislands[$order[$i]];
if($island->{'id'} == $boi){
$island->{'empe'} ++;
if($boi != $booa){
logboukae($island->{'id'}, $island->{'name'});
$booa = $boi;
}
}
}
if(random(100) < 50){
$HdisEarthquake += random(4);
if($HdisEarthquake > 9){
$HdisEarthquake = 10;
}
}else{
$HdisEarthquake -= random(4);
if($HdisEarthquake < 1){
$HdisEarthquake = 0;
}
}
if(random(100) < 50){
$HdisTsunami += random(6);
if($HdisTsunami > 19){
$HdisTsunami = 20;
}
}else{
$HdisTsunami -= random(6);
if($HdisTsunami < 1){
$HdisTsunami = 0;
}
}
if(random(100) < 50){
$HdisTyphoon += random(6);
if($HdisTyphoon > 29){
$HdisTyphoon = 30;
}
}else{
$HdisTyphoon -= random(6);
if($HdisTyphoon < 1){
$HdisTyphoon = 0;
}
}
if(random(100) < 50){
$HdisMeteo += random(4);
if($HdisMeteo > 9){
$HdisMeteo = 10;
}
}else{
$HdisMeteo -= random(4);
if($HdisMeteo < 1){
$HdisMeteo = 0;
}
}
if(random(100) < 50){
$HdisHugeMeteo += random(3);
if($HdisHugeMeteo > 4){
$HdisHugeMeteo = 5;
}
}else{
$HdisHugeMeteo -= random(3);
if($HdisHugeMeteo < 1){
$HdisHugeMeteo = 0;
}
}
if(random(100) < 50){
$HdisEruption += random(4);
if($HdisEruption > 9){
$HdisEruption = 10;
}
}else{
$HdisEruption -= random(4);
if($HdisEruption < 1){
$HdisEruption = 0;
}
}
if(random(100) < 50){
$HdisFire += random(4);
if($HdisFire > 9){
$HdisFire = 10;
}
}else{
$HdisFire -= random(4);
if($HdisFire < 1){
$HdisFire = 0;
}
}
if(random(100) < 50){
$HdisMonster += random(2);
if($HdisMonster > 4){
$HdisMonster = 5;
}
}else{
$HdisMonster -= random(2);
if($HdisMonster < 1){
$HdisMonster = 0;
}
}
if(random(100) < 50){
$HdisDisa += random(3);
if($HdisDisa > 19){
$HdisDisa = 20;
}
}else{
$HdisDisa -= random(3);
if($HdisDisa < 1){
$HdisDisa = 0;
}
}
if(random(100) < 50){
$HdisHardRain += random(3);
if($HdisHardRain > 10){
$HdisHardRain = 10;
}
}else{
$HdisHardRain -= random(3);
if($HdisHardRain < 1){
$HdisHardRain = 0;
}
}
    # �͸���˥�����
    islandSort();
$island = $Hislands[0];
$island->{'top'} ++;
    # ���������оݥ�������ä��顢���ν���
    if(($HislandTurn % $HturnPrizeUnit) == 0) {

	logPrize($island->{'id'}, $island->{'name'}, "$HislandTurn${Hprize[0]}");
my($mone);
if($HislandTurn % 10000 == 0){
$mone = 10000;
}elsif($HislandTurn % 1000 == 0){
$mone = 3000;
}elsif($HislandTurn % 100 == 0){
$mone = 1000;
}else{
$mone = 100;
}
$island->{'money'} += $mone;
$island->{'shuu'} += $mone;
logPzMoney($island->{'id'}, $island->{'name'}, $mone);

	$island->{'prize'} .= "${HislandTurn},";
    }

    # ������å�
    $HislandNumber = $remainNumber;

    # �Хå����åץ�����Ǥ���С�������rename
    if(($HislandTurn % $HbackupTurn) == 0) {
	my($i);
	my($tmp) = $HbackupTimes - 1;
	myrmtree("${HdirName}.bak$tmp");
	for($i = ($HbackupTimes - 1); $i > 0; $i--) {
	    my($j) = $i - 1;
	    rename("${HdirName}.bak$j", "${HdirName}.bak$i");
	}
	rename("${HdirName}", "${HdirName}.bak0");
	mkdir("${HdirName}", $HdirMode);

	# ���ե���������᤹
	for($i = 0; $i <= $HlogMax; $i++) {
	    rename("${HdirName}.bak0/hakojima.log$i",
		   "${HdirName}/hakojima.log$i");
	}
	rename("${HdirName}.bak0/hakojima.his",
	       "${HdirName}/hakojima.his");
    }
    # �ե�����˽񤭽Ф�
    writeIslandsFile(-1);
myrmtree("${HdirName1}");
	mkdir("${HdirName1}", $HdirMode);
   writeFile(-1);

    # ���񤭽Ф�
    logFlush();

    # ��Ͽ��Ĵ��
    logHistoryTrim();

    # �ȥåפ�
    topPageMain();
}

# �ǥ��쥯�ȥ�ä�
sub myrmtree {
    my($dn) = @_;
    opendir(DIN, "$dn/");
    my($fileName);
    while($fileName = readdir(DIN)) {
	unlink("$dn/$fileName");
    } 
    closedir(DIN);
    rmdir($dn);
}

# ����������ե�����
sub income {
    my($island) = @_;
    my($pop, $farm, $factory, $mountain, $elector, $boku) = 
	(      
	 $island->{'pop'},
	 ($island->{'farm'} + $island->{'yousho'}) * 10,
	 $island->{'factory'},
	 $island->{'mountain'},
$island->{'hatud'},
$island->{'boku'}* 10
	 );
$island->{'shuu'} = 0;
	my($work) = min($elector, ($factory + $mountain));
if($island->{'denb'} >0){
if($elector <= ($factory + $mountain)){
$island->{'money'} -= ($factory + $mountain - $elector) * 2;
$island->{'shuu'} -= ($factory + $mountain - $elector) * 2;
$work = $factory + $mountain;
}else{
$island->{'money'} += ($elector - $factory - $mountain) * 2;
$island->{'shuu'} += ($elector - $factory - $mountain)  * 2;
}
}
    # ����
    if($pop > ($farm + $boku)){
	# ���Ȥ�������꤬;����
	$island->{'food'} += $farm;
$island->{'food'} += $boku * 10;
$island->{'money'} += min(int(($pop - $farm- $boku) / 10), $work)*3;
$island->{'shuu'} += min(int(($pop - $farm- $boku) / 10), $work)*3;
}elsif($pop > $farm) {
	$island->{'food'} += $farm; # ����ե��Ư
$island->{'food'} +=($pop - $farm)* 10;
    } else {
	# ���Ȥ����Ǽ���դξ��
	$island->{'food'} += $pop; # �������ɻŻ�
    }

    # ��������
    $island->{'food'} = int(($island->{'food'}) - ($pop * $HeatenFood));
$island->{'shoku'} = $farm + ($boku * 10);
}

# ���ޥ�ɥե�����
sub doCommand {
    my($island) = @_;

    # ���ޥ�ɼ��Ф�
    my($comArray, $command);
    $comArray = $island->{'command'};
    $command = $comArray->[0]; # �ǽ�Τ���Ф�
    slideFront($comArray, 0); # �ʹߤ�ͤ��

    # �����Ǥμ��Ф�
    my($kind, $target, $x, $y, $arg) = 
	(
	 $command->{'kind'},
	 $command->{'target'},
	 $command->{'x'},
	 $command->{'y'},
	 $command->{'arg'}
	 );

    # Ƴ����
    my($name) = $island->{'name'};
    my($id) = $island->{'id'};
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};
    my($landKind) = $land->[$x][$y];
    my($lv) = $landValue->[$x][$y];
    my($cost) = $HcomCost[$kind];
    my($comName) = $HcomName[$kind];
    my($point) = "($x, $y)";
    my($landName) = landName($landKind, $lv);

    if($kind == $HcomDoNothing) {
	# ��ⷫ��
	logDoNothing($id, $name, $comName);
	$island->{'money'} += 10;
$island->{'shuu'} += 10;
	$island->{'absent'} ++;
	
	# ��ư����
	if($island->{'absent'} >= $HgiveupTurn) {
	    $comArray->[0] = {
		'kind' => $HcomGiveup,
		'target' => 0,
		'x' => 0,
		'y' => 0,
		'arg' => 0
	    }
	}
	return 1;
    }

    $island->{'absent'} = 0;

    # �����ȥ����å�
    if($cost > 0) {
	# ��ξ��
	if($island->{'money'} < $cost) {
	    logNoMoney($id, $name, $comName);
	    return 0;
	}
    } elsif($cost < 0) {
	# �����ξ��
	if($island->{'food'} < (-$cost)) {
	    logNoFood($id, $name, $comName);
	    return 0;
	}
    }

    # ���ޥ�ɤ�ʬ��
    if(($kind == $HcomPrepare) ||
       ($kind == $HcomPrepare2)) {
	# ���ϡ��Ϥʤ餷
	if(($landKind == $HlandSea) || 
	   ($landKind == $HlandSbase) ||
($landKind == $HlandLake) ||
	   ($landKind == $HlandOil) ||
	   ($landKind == $HlandMountain) ||
($landKind == $HlandJirai) ||
	   ($landKind == $HlandMonster)) {
	    # ����������ϡ����ġ��������ä����ϤǤ��ʤ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# ��Ū�ξ���ʿ�Ϥˤ���
	$land->[$x][$y] = $HlandPlains;
	$landValue->[$x][$y] = 0;
	logLandSuc($id, $name, '����', $point);

	# ��򺹤�����
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
	if($kind == $HcomPrepare2) {
	    # �Ϥʤ餷
	    $island->{'prepare2'}++;
	    
	    # ��������񤻤�
	    return 0;
	} else {
	    # ���Ϥʤ顢��¢��β�ǽ������
	    if(random(1000) < $HdisMaizo) {
		my($v) = 100 + random(901);
		$island->{'money'} += $v;
$island->{'shuu'}+= $v;
		logMaizo($id, $name, $comName, $v);
	    }
	    return 1;
	}
} elsif($kind == $Hcomjoyo) {
if(!($landKind == $HlandJirai)){
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
}
	$land->[$x][$y] = $HlandPlains;
	$landValue->[$x][$y] = 0;
	logLandSuc($id, $name, $comName, $point);
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
return 1;
    } elsif($kind == $HcomMina) {
if(!(($landKind == $HlandSea) && ($lv == 0))){
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
}
	my($seaCount) =
	    countAround($land, $x, $y, $HlandSea, 5) +
	    countAround($land, $x, $y, $HlandOil, 5) +
            countAround($land, $x, $y, $HlandSbase, 5);
 if($seaCount == 5) {
	    # ���������������Ω����ǽ
	    logNoLandAround($id, $name, $comName, $point);
	    return 0;
	}
if($seaCount == 1) {
	    # ���������������Ω����ǽ
	    logNoSeaAround($id, $name, $comName, $point);
	    return 0;
	}
	    $land->[$x][$y] = $HlandMina;
	    $landValue->[$x][$y] = 1;
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
	    logLandSuc($id, $name, $comName, $point);
  } elsif($kind == $HcomChou) {
if(!((($landKind == $HlandSea) && ($lv == 1)) || ($landKind == $HlandChou))){
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
}
if($landKind == $HlandChou){
$landValue->[$x][$y] += 3; # ���� + 2000��
		if($landValue->[$x][$y] > 300) {
		    $landValue->[$x][$y] = 300; # ���� 50000��
		}
logLandSuc($id, $name, $comName, $point);
	    if($arg > 1) {
		my($command);
		$arg--;
		slideBack($comArray, 0);
		$comArray->[0] = {
		    'kind' => $kind,
		    'target' => $target,
		    'x' => $x,
		    'y' => $y,
		    'arg' => $arg
		    };
	    }
}else{
	my($seaCount) =
	    countAround($land, $x, $y, $HlandSea, 5) +
	    countAround($land, $x, $y, $HlandOil, 5) +
            countAround($land, $x, $y, $HlandSbase, 5);
 if($seaCount == 5) {
	    # ���������������Ω����ǽ
	    logNoLandAround($id, $name, $comName, $point);
	    return 0;
	}
if($seaCount == 1) {
	    # ���������������Ω����ǽ
	    logNoSeaAround($id, $name, $comName, $point);
	    return 0;
	}
	    $land->[$x][$y] = $HlandChou;
	    $landValue->[$x][$y] = 3;
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
	    logLandSuc($id, $name, $comName, $point);
	    if($arg > 1) {
		my($command);
		$arg--;
		slideBack($comArray, 0);
		$comArray->[0] = {
		    'kind' => $kind,
		    'target' => $target,
		    'x' => $x,
		    'y' => $y,
		    'arg' => $arg
		    };
	    }
}
  } elsif($kind == $HcomSuiry) {
if(!((($landKind == $HlandMountain) && ($lv == 0))|| ($landKind == $HlandSuiry))){
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
}
if($landKind == $HlandSuiry){
$landValue->[$x][$y] += 3; # ���� + 2000��
		if($landValue->[$x][$y] > 300) {
		    $landValue->[$x][$y] = 300; # ���� 50000��
		}
logLandSuc($id, $name, $comName, $point);
	    if($arg > 1) {
		my($command);
		$arg--;
		slideBack($comArray, 0);
		$comArray->[0] = {
		    'kind' => $kind,
		    'target' => $target,
		    'x' => $x,
		    'y' => $y,
		    'arg' => $arg
		    };
	    }
}else{
	    $land->[$x][$y] = $HlandSuiry;
	    $landValue->[$x][$y] = 3;
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
	    logLandSuc($id, $name, $comName, $point);
	    if($arg > 1) {
		my($command);
		$arg--;
		slideBack($comArray, 0);
		$comArray->[0] = {
		    'kind' => $kind,
		    'target' => $target,
		    'x' => $x,
		    'y' => $y,
		    'arg' => $arg
		    };
	    }
}
  } elsif($kind == $HcomTuri) {
if(!(($landKind == $HlandLake) && ($lv != 2))){
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
}
	    $landValue->[$x][$y] = 2;
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
	    logLandSuc($id, $name, $comName, $point);
    } elsif(($kind == $HcomReclaim) ||
            ($kind == $HcomUmeta)) {
	# ���Ω��
	if(($landKind != $HlandSea) &&
($landKind != $HlandLake) &&
	   ($landKind != $HlandOil) &&
	   ($landKind != $HlandSbase)) {
	    # ����������ϡ����Ĥ������Ω�ƤǤ��ʤ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# �����Φ�����뤫�����å�
	my($seaCount) =
	    countAround($land, $x, $y, $HlandSea, 5) +
	    countAround($land, $x, $y, $HlandOil, 5) +
            countAround($land, $x, $y, $HlandSbase, 5);

        if($seaCount == 5) {
	    # ���������������Ω����ǽ
	    logNoLandAround($id, $name, $comName, $point);
	    return 0;
	}

	if((($landKind == $HlandSea) && ($lv == 1))||(($landKind == $HlandOil) &&($lv > 1))||($landKind == $HlandLake)){
	    # �����ξ��
	    # ��Ū�ξ�����Ϥˤ���
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
	    logLandSuc($id, $name, '���Ω��', $point);
	    $island->{'area'}++;

	    if($seaCount <= 4) {
		# ����γ���3�إå�������ʤΤǡ������ˤ���
		my($i, $sx, $sy);

		for($i = 1; $i < 5; $i++) {
		    $sx = $x + $ax[$i];
		    $sy = $y + $ay[$i];


		    if(($sx < 0) || ($sx >= $HislandSize) ||
		       ($sy < 0) || ($sy >= $HislandSize)) {
		    } else {
			# �ϰ���ξ��
			if($land->[$sx][$sy] == $HlandSea) {
			    $landValue->[$sx][$sy] = 1;
			}
		    }
		}
	    }
	} else {
	    # ���ʤ顢��Ū�ξ��������ˤ���
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 1;
	    logLandSuc($id, $name, '���Ω��', $point);
	}
	
	# ��򺹤�����
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
	if($kind == $HcomUmeta) {
	    # �Ϥʤ餷
	    $island->{'prepare2'}++;
	    
	    # ��������񤻤�
	    return 0;
	} else {
 return 1;
	   }
	
    } elsif($kind == $HcomOnse) {


	if($landKind == $HlandPlains) {
	    if($arg == 0) { $arg = 1; }
	    my($value, $str);
	    $value = min($arg * ($cost), $island->{'money'});
	    $str = "$value$HunitMoney";
	    $island->{'money'} -= $value;
$island->{'shuu'} -= $value;
	    # ���Ĥ��뤫Ƚ��
	    if(2 >random(10)) {
		# ���ĸ��Ĥ���
		logOnseFound($id, $name, $point, $comName, $str);
		$land->[$x][$y] = $Hlanddoubutu;
		$landValue->[$x][$y] = 0;
	    } else {
		# ̵�̷���˽����
		logOnseFail($id, $name, $point, $comName, $str);
	    } 
return 1;
}else {
	    logLandFail($id, $name, $comName, $landName, $point);
return 1;
}
    } elsif($kind == $HcomDestroy) {
	# ����
	if(($landKind == $HlandSbase) ||
	   ($landKind == $HlandOil) ||
	   ($landKind == $HlandMonster)) {
	    # ������ϡ����ġ����äϷ���Ǥ��ʤ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	if(($landKind == $HlandSea) && ($lv == 0)) {
	    # ���ʤ顢����õ��
	    # ���۷���
	    if($arg == 0) { $arg = 1; }
	    my($value, $str, $p);
	    $value = min($arg * ($cost), $island->{'money'});
	    $str = "$value$HunitMoney";
	    $p = int($value / $cost) * 2;
	    $island->{'money'} -= $value;
$island->{'shuu'} -= $value;
	    # ���Ĥ��뤫Ƚ��
	    if($p > random(100)) {
		# ���ĸ��Ĥ���
		logOilFound($id, $name, $point, $comName, $str);
		$land->[$x][$y] = $HlandOil;
		$landValue->[$x][$y] = 0;
	    } else {
		# ̵�̷���˽����
		logOilFail($id, $name, $point, $comName, $str);
	    }
	    return 1;
	}

	# ��Ū�ξ��򳤤ˤ��롣���ʤ���Ϥˡ������ʤ鳤�ˡ�
	if($landKind == $HlandMountain) {
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
	} elsif($landKind == $HlandSea) {
	    $landValue->[$x][$y] = 0;
	} else {
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 1;
	    $island->{'area'}--;
	}
	logLandSuc($id, $name, $comName, $point);

	# ��򺹤�����
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
	return 1;
    } elsif($kind == $HcomDestroy2) {
	# ����
	if(($landKind == $HlandSbase) ||
	   ($landKind == $HlandOil) ||
(($landKind == $HlandSea) && ($lv == 0))||
	   ($landKind == $HlandMonster)) {
	    # ������ϡ����ġ����äϷ���Ǥ��ʤ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# ��Ū�ξ��򳤤ˤ��롣���ʤ���Ϥˡ������ʤ鳤�ˡ�
	if($landKind == $HlandMountain) {
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
	} elsif($landKind == $HlandSea) {
	    $landValue->[$x][$y] = 0;
	} else {
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 1;
	    $island->{'area'}--;
	}
	logLandSuc($id, $name, '����', $point);

	# ��򺹤�����
 $island->{'prepare2'}++;
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
	return 0;
} elsif($kind == $Hcomkaitetu) {
if(($landKind == $HlandOil)&& ($lv == 0)){
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 0;
logOitekyo($id, $name, $point);
}elsif(($landKind == $HlandOil)&& ($lv > 0)){
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 1;
logyotekyo($id, $name, $point);
}elsif($landKind == $HlandMina){
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 0;
logminatekyo($id, $name, $point);
}else{
logtekyoFail($id, $name, $point);
}
} elsif($kind == $Hcomyousho) {
	if(($landKind == $HlandSea) && ($lv == 1)) {
	    $island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
		$land->[$x][$y] = $HlandOil;
		$landValue->[$x][$y] = 10;
logLandSuc($id, $name, $comName, $point);
	# ����դ��ʤ顢���ޥ�ɤ��᤹
	    if($arg > 1) {
		my($command);
		$arg--;
		slideBack($comArray, 0);
		$comArray->[0] = {
		    'kind' => $kind,
		    'target' => $target,
		    'x' => $x,
		    'y' => $y,
		    'arg' => $arg
		    };
	    }
	    } elsif (($landKind == $HlandOil) && ($lv >0)){
		$landValue->[$x][$y] += 2; # ���� + 2000��
		if($landValue->[$x][$y] > 50) {
		    $landValue->[$x][$y] = 50; # ���� 50000��
logLandSuc($id, $name, $comName, $point);
}
	# ����դ��ʤ顢���ޥ�ɤ��᤹
	    if($arg > 1) {
		my($command);
		$arg--;
		slideBack($comArray, 0);
		$comArray->[0] = {
		    'kind' => $kind,
		    'target' => $target,
		    'x' => $x,
		    'y' => $y,
		    'arg' => $arg
		    };
	    }
}else{
logyoushoFail($id, $name, $point, $comName);
	    }
	    return 1;
	
    } elsif($kind == $HcomSellTree) {
	# Ȳ��
	if($landKind != $HlandForest) {
	    # ���ʳ���Ȳ�ΤǤ��ʤ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# ��Ū�ξ���ʿ�Ϥˤ���
	$land->[$x][$y] = $HlandPlains;
	$landValue->[$x][$y] = 0;
	logLandSuc($id, $name, $comName, $point);

	# ��Ѷ������
	$island->{'money'} += $HtreeValue * $lv;
$island->{'shuu'} += $HtreeValue * $lv;
	return 1;
}elsif($kind == $HcomBouh){
if(!(($landKind == $HlandSea)&&($landValue->[$x][$y] == 1))){
logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
}
$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;

$land->[$x][$y] = $HlandBouh;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point); 
    } elsif(($kind == $HcomPlant) ||
	    ($kind == $HcomFarm) ||
	    ($kind == $HcomFactory) ||
	    ($kind == $HcomBase) ||
($kind == $Hcomdoubutu) ||
($kind == $HcomOmise) ||
($kind == $Hcomkishou) ||
($kind == $Hcomkiken) ||
	    ($kind == $HcomMonument) ||
	    ($kind == $HcomHaribote) ||
($kind == $HcomBank) ||
($kind == $Hcomkukou) ||
($kind == $HcomPori) ||
	    ($kind == $HcomDbase) ||
	    ($kind == $HcomUbase) ||
($kind == $HcomGoyu) ||
($kind == $HcomBoku) ||
($kind == $Hcomhospit) ||
($kind == $HcomOnpa) ||
($kind == $HcomInok) ||
($kind == $HcomJous) ||
($kind == $HcomHatu) ||
($kind == $HcomGomi) ||
($kind == $HcomJusi) ||
($kind == $HcomEisei) ||
($kind == $HcomTaiy) ||
($kind == $HcomFuha) ||
($kind == $HcomDenb) ||
($kind == $HcomReho) ||
($kind == $HcomTinet) ||
($kind == $HcomKoku) ||
($kind == $HcomKeiba) ||
($kind == $HcomFoot) ||
($kind == $HcomYakyu) ||
($kind == $HcomSki) ||
($kind == $HcomSuiz) ||
($kind == $HcomHotel) ||
($kind == $HcomGolf) ||
($kind == $HcomYuu) ||
($kind == $HcomTenj) ||
($kind == $HcomKaji) ||
($kind == $HcomKouen) ||
($kind == $HcomShok) ||
($kind == $HcomShou) ||
($kind == $HcomTou) ||
($kind == $HcomShiro) ||
($kind == $HcomStation) ||
($kind == $HcomRail) ||
($kind == $HcomMine) ||
($kind == $HcomMineSuper) ||
($kind == $HcomMineWrpe) ||
($kind == $HcomTbase)) {

	# �Ͼ���߷�
	if(!
	   (($landKind == $HlandPlains) ||
	    ($landKind == $HlandTown) ||
	    (($landKind == $HlandMonument) && ($kind == $HcomMonument)) ||
	    (($landKind == $HlandHaribote) && ($kind == $HcomBank)) ||
	    (($landKind == $HlandFarm) && ($kind == $HcomFarm)) ||
	    (($landKind == $HlandFactory) && ($kind == $HcomFactory)) ||
	    (($landKind == $HlandOnpa) && ($kind == $HcomOnpa)) ||
	    (($landKind == $HlandDefence) && ($kind == $HcomDbase)) ||
	    (($landKind == $HlandSefence) && ($kind == $HcomUbase)) ||
	    (($landKind == $HlandInok) && ($kind == $HcomInok)) ||
	    (($landKind == $Hlandkiken) && ($kind == $Hcomkiken)) ||
	    (($landKind == $Hlandkishou) && ($kind == $Hcomkishou)) ||
	    (($landKind == $HlandBoku) && ($kind == $HcomBoku)) ||
(($landKind == $HlandReho) && ($kind == $HcomReho)) ||
 	    (($landKind == $HlandJous) && ($kind == $HcomJous)) ||
	    (($landKind == $HlandHatu) && ($kind == $HcomHatu)) ||
	    (($landKind == $HlandGomi) && ($kind == $HcomGomi)) ||
	    (($landKind == $HlandTaiy) && ($kind == $HcomTaiy)) ||
	    (($landKind == $HlandFuha) && ($kind == $HcomFuha)) ||
(($landKind == $HlandTinet) && ($kind == $HcomTinet)) ||
  (($landKind == $Hlandkukou) && ($kind == $Hcomkukou)) ||
(($landKind == $HlandDefence) && ($kind == $HcomTbase)))) {
	    # ��Ŭ�����Ϸ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# �����ʬ��
	if($kind == $HcomPlant) {
	    # ��Ū�ξ��򿹤ˤ��롣
	    $land->[$x][$y] = $HlandForest;
	    $landValue->[$x][$y] = 1; # �ڤϺ���ñ��
	    logPBSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomBase) {
	    # ��Ū�ξ���ߥ�������Ϥˤ��롣
	    $land->[$x][$y] = $HlandBase;
	    $landValue->[$x][$y] = 0; # �и���0
	    logPBSuc($id, $name, $comName, $point);
} elsif($kind == $Hcomdoubutu) { # ��������

$land->[$x][$y] = $Hlanddoubutu;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point); 
	}elsif($kind == $HcomShou) {
	    # ��Ū�ξ��򿹤ˤ��롣
	    $land->[$x][$y] = $HlandShou;
	    $landValue->[$x][$y] = 1; # �ڤϺ���ñ��
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomTaiy) {
	    # ����
	    if($landKind == $HlandTaiy) {
		# ���Ǥ�����ξ��
		$landValue->[$x][$y] += 5; # ���� + 2000��
		if($landValue->[$x][$y] > 100) {
		    $landValue->[$x][$y] = 100; # ���� 50000��
		}
	    } else {
		# ��Ū�ξ��������
		$land->[$x][$y] = $HlandTaiy;
		$landValue->[$x][$y] = 5; # ���� = 10000��
	    }
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomTinet) {
	    # ����
	    if($landKind == $HlandTinet) {
		# ���Ǥ�����ξ��
		$landValue->[$x][$y] += 3; # ���� + 2000��
		if($landValue->[$x][$y] > 300) {
		    $landValue->[$x][$y] = 300; # ���� 50000��
		}
logLandSuc($id, $name, $comName, $point);
	    } else {
my($mouCount) =countAround($land, $x, $y, $HlandMountain, 5);
if($mouCount == 0) {
	    # ���������������Ω����ǽ
	    logNoMounAround($id, $name, $comName, $point);
	    return 0;
	}
		# ��Ū�ξ��������
		$land->[$x][$y] = $HlandTinet;
		$landValue->[$x][$y] = 3; # ���� = 10000��
logLandSuc($id, $name, $comName, $point);
	    }
	} elsif($kind == $HcomFuha) {
	    # ����
	    if($landKind == $HlandFuha) {
		# ���Ǥ�����ξ��
		$landValue->[$x][$y] += 1; # ���� + 2000��
		if($landValue->[$x][$y] > 10) {
		    $landValue->[$x][$y] = 10; # ���� 50000��
		}
	    } else {
		# ��Ū�ξ��������
		$land->[$x][$y] = $HlandFuha;
		$landValue->[$x][$y] = 1; # ���� = 10000��
	    }
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomReho) {
	    # ����
	    if($landKind == $HlandReho) {
		# ���Ǥ�����ξ��
		$landValue->[$x][$y] += 1; # ���� + 2000��
		if($landValue->[$x][$y] > 10) {
		    $landValue->[$x][$y] = 10; # ���� 50000��
		}
	    } else {
		# ��Ū�ξ��������
		$land->[$x][$y] = $HlandReho;
		$landValue->[$x][$y] = 1; # ���� = 10000��
	    }
	    logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomJusi) { # ��������

$land->[$x][$y] = $HlandJusi;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomEisei) { # ��������

$land->[$x][$y] = $HlandEisei;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomDenb) { # ��������

$land->[$x][$y] = $HlandDenb;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomKeiba) { # ��������

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 5;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomFoot) { # ��������

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 4;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomYakyu) { # ��������

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 3;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomSki) { # ��������

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 2;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomSuiz) { # ��������

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomHotel) { # ��������

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 0;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomGolf) { # ��������

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 6;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomYuu) { # ��������

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 7;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomTenj) { # ��������

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 8;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomKaji) { # ��������

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 9;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomKouen) { # ��������

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 10;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomShok) { # ��������

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 11;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomTou) { # ��������

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 12;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomShiro) { # ��������

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 13;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomGoyu) { # ��������

$land->[$x][$y] = $HlandGoyu;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomKoku) { # ��������

$land->[$x][$y] = $HlandKoku;
$landValue->[$x][$y] = 1;
logPBSuc($id, $name, $comName, $point);
} elsif($kind == $Hcomhospit) { # ��������

$land->[$x][$y] = $Hlandhos;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point); 
} elsif($kind == $HcomOmise) { # ��������

$land->[$x][$y] = $Hlanddoubutu;
$landValue->[$x][$y] = 2;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomPori) { # ��������

$land->[$x][$y] = $HlandPori;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $Hcomkiken) { # ��������

if($landKind == $Hlandkiken) {
$landValue->[$x][$y]++;
if($landValue->[$x][$y] > 10) {
$landValue->[$x][$y] = 10; 
}
logzoukyou($id, $name, $point);
}else{
if($island->{'kiken'} >0){
logLanddame($id, $name, $comName, $point);
}else{
$land->[$x][$y] = $Hlandkiken;
$landValue->[$x][$y] = 1;
logPBSuc($id, $name, $comName, $point);
}
}
} elsif($kind == $Hcomkishou) {
if($landKind == $Hlandkishou) {
$landValue->[$x][$y]++;
if($landValue->[$x][$y] > 10) {
$landValue->[$x][$y] = 10; 
}
logLandSuc($id, $name, $comName, $point);
}else{# ��������
if($island->{'kishou'} >0){
logLanddeme($id, $name, $comName, $point);
}else{

$land->[$x][$y] = $Hlandkishou;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point);
}
}
} elsif($kind == $HcomOnpa) {
if($island->{'Inok'} >0){
if($landKind == $HlandOnpa) {
$landValue->[$x][$y]++;
if($landValue->[$x][$y] > 10) {
$landValue->[$x][$y] = 10; 
}
logLandSuc($id, $name, $comName, $point);
}else{
if($island->{'Onpa'} >0){
logLanddime($id, $name, $comName, $point);
}else{

$land->[$x][$y] = $HlandOnpa;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point);
}
}
}else{
logInoknasi($id, $name, $comName);
}
} elsif($kind == $HcomInok) { 
if($landKind == $HlandInok) {
$landValue->[$x][$y]++;
if($landValue->[$x][$y] > 10) {
$landValue->[$x][$y] = 10; 
}
logLandSuc($id, $name, $comName, $point);
}else{# ��������
if($island->{'Inok'} >0){
logLanddume($id, $name, $comName, $point);
}else{

$land->[$x][$y] = $HlandInok;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point);
}
}	} elsif($kind == $HcomHaribote) {
	    # ��Ū�ξ���ϥ�ܥƤˤ���
	    $land->[$x][$y] = $HlandHaribote;
	    $landValue->[$x][$y] = 0;
	    logHariSuc($id, $name, $comName, $HcomName[$HcomDbase], $point);
} elsif($kind == $HcomBank) {
# ���
if($landKind == $HlandHaribote) {
$landValue->[$x][$y]++;
if($landValue->[$x][$y] > 10) {
$landValue->[$x][$y] = 10; 
}
} else {
$land->[$x][$y] = $HlandHaribote;
$landValue->[$x][$y] = 1;
}
logPBSuc($id, $name, $comName, $point);
} elsif($kind == $Hcomkukou) {
# ���
if($landKind == $Hlandkukou) {
$landValue->[$x][$y]++;
if($landValue->[$x][$y] > 2) {
$landValue->[$x][$y] = 2; 
}
} else {
$land->[$x][$y] = $Hlandkukou;
$landValue->[$x][$y] = 1;
}
logLandSuc($id, $name, $comName, $point);
 } elsif($kind == $HcomMine) {
            # ��Ū�ξ�������ˤ���
             $land->[$x][$y] = $HlandJirai;
             $landValue->[$x][$y] = 0;
             logABSuc($id, $name, $comName, $point);
         } elsif($kind == $HcomMineSuper) {
             # ��Ū�ξ������ǽ����ˤ���
            $land->[$x][$y] = $HlandJirai;
             $landValue->[$x][$y] = 1;
logABSuc($id, $name, $comName, $point);
        } elsif($kind == $HcomMineWrpe) {
             # ��Ū�ξ������ǽ����ˤ���
            $land->[$x][$y] = $HlandJirai;
             $landValue->[$x][$y] = 2;
logABSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomFarm) {
	    # ����
	    if($landKind == $HlandFarm) {
		# ���Ǥ�����ξ��
		$landValue->[$x][$y] += 2; # ���� + 2000��
		if($landValue->[$x][$y] > 50) {
		    $landValue->[$x][$y] = 50; # ���� 50000��
		}
	    } else {
		# ��Ū�ξ��������
		$land->[$x][$y] = $HlandFarm;
		$landValue->[$x][$y] = 10; # ���� = 10000��
	    }
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomBoku) {
	    # ����
	    if($landKind == $HlandBoku) {
		# ���Ǥ�����ξ��
		$landValue->[$x][$y] += 1; # ���� + 2000��
		if($landValue->[$x][$y] > 10) {
		    $landValue->[$x][$y] = 10; # ���� 50000��
		}
	    } else {
		# ��Ū�ξ��������
		$land->[$x][$y] = $HlandBoku;
		$landValue->[$x][$y] = 1; # ���� = 10000��
	    }
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomHatu) {
	    # ����
	    if($landKind == $HlandHatu) {
		# ���Ǥ�����ξ��
		$landValue->[$x][$y] += 5; # ���� + 2000��
		if($landValue->[$x][$y] > 100) {
		    $landValue->[$x][$y] = 100; # ���� 50000��
		}
	    } else {
		# ��Ū�ξ��������
		$land->[$x][$y] = $HlandHatu;
		$landValue->[$x][$y] = 10; # ���� = 10000��
	    }
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomGomi) {
	    # ����
	    if($landKind == $HlandGomi) {
		# ���Ǥ�����ξ��
		$landValue->[$x][$y] += 5; # ���� + 2000��
		if($landValue->[$x][$y] > 100) {
		    $landValue->[$x][$y] = 100; # ���� 50000��
		}
	    } else {
		# ��Ū�ξ��������
		$land->[$x][$y] = $HlandGomi;
		$landValue->[$x][$y] = 10; # ���� = 10000��
	    }
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomJous) {
	    # ����
	    if($landKind == $HlandJous) {
		# ���Ǥ�����ξ��
		$landValue->[$x][$y] += 5;
		if($landValue->[$x][$y] > 50) {
		    $landValue->[$x][$y] = 50; # ���� 50000��
		}
	    } else {
		# ��Ū�ξ��������
		$land->[$x][$y] = $HlandJous;
		$landValue->[$x][$y] = 5; # ���� = 10000��
	    }
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomFactory) {
	    # ����
	    if($landKind == $HlandFactory) {
		# ���Ǥ˹���ξ��
		$landValue->[$x][$y] += 10; # ���� + 10000��
		if($landValue->[$x][$y] > 200) {
		    $landValue->[$x][$y] = 200; 0000��
		}
	    } else {
		# ��Ū�ξ��򹩾��
		$land->[$x][$y] = $HlandFactory;
		$landValue->[$x][$y] = 30; # ���� = 10000��
	    }
	    logLandSuc($id, $name, $comName, $point);
 } elsif($kind == $HcomStation) {
             # ��Ū�ξ���ؤˤ���
             $land->[$x][$y] = $HlandStation;
             $landValue->[$x][$y] = 100;
             logStationSuc($id, $name, $comName, $point);
         } elsif($kind == $HcomRail) {           

            $land->[$x][$y] = $HlandStation;
           $landValue->[$x][$y] = 0;
             logRailSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomDbase) {
	    # �ɱһ���
	    if($landKind == $HlandDefence) {
		# ���Ǥ��ɱһ��ߤξ��
		$landValue->[$x][$y] = 1; # �������֥��å�
		logBombSet($id, $name, $landName, $point);
	    } else {
		# ��Ū�ξ����ɱһ��ߤ�
		$land->[$x][$y] = $HlandDefence;
		$landValue->[$x][$y] = 0;
		logLandSuc($id, $name, $comName, $point);
	    }
	} elsif($kind == $HcomUbase) {
	    # �ɱһ���
	    if($landKind == $HlandSefence) {
		# ���Ǥ��ɱһ��ߤξ��
		$landValue->[$x][$y] = 1; # �������֥��å�
		logBombSet($id, $name, $landName, $point);
	    } else {
		# ��Ū�ξ����ɱһ��ߤ�
		$land->[$x][$y] = $HlandSefence;
		$landValue->[$x][$y] = 0;
		logLandSuc($id, $name, $comName, $point);
	    }
	} elsif($kind == $HcomTbase) {
	    # �ɱһ���
	    if($landKind == $HlandDefence) {
		# ���Ǥ��ɱһ��ߤξ��
		$landValue->[$x][$y] = 1; # �������֥��å�
		logBombSet($id, $name, $landName, $point);
	    } else {
		# ��Ū�ξ����ɱһ��ߤ�
		$land->[$x][$y] = $HlandDefence;
		$landValue->[$x][$y] = 2;
		logPBSuc($id, $name, $comName, $point);
	    }
	} elsif($kind == $HcomMonument) {
	    # ��ǰ��
	    if($landKind == $HlandMonument) {
		# ���Ǥ˵�ǰ��ξ��
		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
		    # �������åȤ����Ǥˤʤ�
		    # ������鷺�����
		    return 0;
		}
		my($tIsland) = $Hislands[$tn];
		$tIsland->{'bigmissile'}++;

		# ���ξ��Ϲ��Ϥ�
		$land->[$x][$y] = $HlandWaste;
		$landValue->[$x][$y] = 0;
		logMonFly($id, $name, $landName, $point);
	    } else {
		# ��Ū�ξ���ǰ���
		$land->[$x][$y] = $HlandMonument;
		if($arg >= $HmonumentNumber) {
		    $arg = 0;
		}
		$landValue->[$x][$y] = $arg;
		logLandSuc($id, $name, $comName, $point);
	    }
	}

	# ��򺹤�����
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
	# ����դ��ʤ顢���ޥ�ɤ��᤹
	if(($kind == $HcomFarm) ||
($kind == $HcomOnpa) ||
($kind == $HcomInok) ||
($kind == $Hcomkiken) ||
($kind == $Hcomkishou) ||
($kind == $HcomTinet) ||
($kind == $HcomBoku) ||
($kind == $HcomJous) ||
($kind == $HcomHatu) ||
($kind == $HcomGomi) ||
($kind == $HcomTaiy) ||
($kind == $HcomFuha) ||
($kind == $HcomReho) ||
($kind == $HcomBank) ||
	   ($kind == $HcomFactory)) {
	    if($arg > 1) {
		my($command);
		$arg--;
		slideBack($comArray, 0);
		$comArray->[0] = {
		    'kind' => $kind,
		    'target' => $target,
		    'x' => $x,
		    'y' => $y,
		    'arg' => $arg
		    };
	    }
	}

	return 1;
    } elsif($kind == $HcomMountain) {
	# �η���
	if($landKind != $HlandMountain) {
	    # ���ʳ��ˤϺ��ʤ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	$landValue->[$x][$y] += 5; # ���� + 5000��
	if($landValue->[$x][$y] > 200) {
	    $landValue->[$x][$y] = 200; # ���� 200000��
	}
	logLandSuc($id, $name, $comName, $point);

	# ��򺹤�����
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
	if($arg > 1) {
	    my($command);
	    $arg--;
	    slideBack($comArray, 0);
	    $comArray->[0] = {
		'kind' => $kind,
		'target' => $target,
		'x' => $x,
		'y' => $y,
		'arg' => $arg
		};
	}
	return 1;
    } elsif($kind == $HcomSbase) {
	# �������
	if(($landKind != $HlandSea) || ($lv != 0)){
	    # ���ʳ��ˤϺ��ʤ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	$land->[$x][$y] = $HlandSbase;
	$landValue->[$x][$y] = 0; # �и���0
	logLandSuc($id, $name, $comName, '(?, ?)');

	# ��򺹤�����
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
	return 1;
    } elsif(($kind == $HcomMissileNM) ||
	    ($kind == $HcomMissilePP) ||
	    ($kind == $HcomMissileST) ||
	    ($kind == $HcomMissileLD)||
($kind == $HcomMissileMK)||
($kind == $HcomMissileUC)||
($kind == $HcomMissileEM)||
($kind == $HcomMissileNC)||
($kind == $HcomMissileNEB)||
($kind == $HcomMissileUB)||
($kind == $HcomRazer)||
($kind == $HcomPMS)||
($kind == $HcomMissileRE)) {

	# �ߥ������
	# �ߥ�����ȯ�͵��ĳ�ǧ
	if (($HislandTurn - $island->{'birth'}) <= $HdisableMissileTurn) {
	    logNotPermitted($id, $name, $comName);
	    return 1;
	}
	if ($island->{'gun'} == 0) {
	    logNoKoku($id, $name, $comName);
	    return 0;
	}
if ($kind == $HcomRazer){
if($island->{'reiei'} == 0){
logNoRazer($id, $name, $comName);
return 0;
} elsif ($island->{'reiei'} > 10) {
logUnRazer($id, $name, $comName);
return 0;
}else{
$arg = 1;
my($rei) = 100 - ($island->{'reiei'} * 10);
$island->{'reiei'} +=$rei;
}
}
if ($kind == $HcomPMS){
if($island->{'pmsei'} == 0){
logNoPMS($id, $name, $comName);
return 0;
} elsif ($island->{'pmsei'} > 10) {
logUnPMS($id, $name, $comName);
return 0;
}else{
$arg = 1;
my($rei) = 100 - ($island->{'pmsei'} * 10);
$island->{'pmsei'} +=$rei;
}
}
	# �������åȼ���
	my($tn) = $HidToNumber{$target};
	if($tn eq '') {
	    # �������åȤ����Ǥˤʤ�
	    logMsNoTarget($id, $name, $comName);
	    return 0;
	}
if($kind == $HcomMissileEM){
if(random(1000) < 100){
    my($oldtarget) = $target;
    $i = random($HislandNumber);
    $target = $Hislands[$i]->{'id'};
      logMsMistake($id, $target, $name, $Hislands[$HidToNumber{$oldtarget}]->{'name'});
}
}
	my($flag) = 0;
	if($arg == 0) {
	    # 0�ξ��Ϸ�Ƥ����
	    $arg = 10000;
	}

	# ��������
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
	my($tLand) = $tIsland->{'land'};
	my($tLandValue) = $tIsland->{'landValue'};
	my($tx, $ty, $err);
if($tIsland->{'teikou'} >0){
logteidame($id, $target, $name, $tName, $comName);
}elsif($island->{'teikou'} >0){
logteideme($id, $name, $comName);
}else{
	# ��̱�ο�
	my($boat) = 0;
my($mei) = ($island->{'kouei'} * 2.5) + 25;
	# ��
	if($kind == $HcomMissilePP) {
if($island->{'kouei'} >0) {
if(random(100) < $mei){
	    $err = 1;
} else {
$err = 5;
}
} else {
$err = 5;
}
} elsif($kind == $HcomRazer) {
$err = 1;
} elsif($kind == $HcomPMS) {
$err = 1;
} elsif($kind == $HcomMissileNC) {
if($island->{'kouei'} >0) {
if(random(100) < $mei){
	    $err = 13;
} else {
$err = 25;
}
} else {
$err = 25;
}

	} else {
if($island->{'kouei'} >0) {
if(random(100) < $mei){
	    $err = 5;
} else {
$err = 13;
}
} else {
$err = 13;
}
	}

	# �⤬�Ԥ��뤫�������­��뤫������������Ĥޤǥ롼��
	my($bx, $by, $count) = (0,0,0);
	while(($arg > 0) &&
	      ($island->{'money'} >= $cost)) {
	    # ���Ϥ򸫤Ĥ���ޤǥ롼��
	    while($count < $HpointNumber) {
		$bx = $Hrpx[$count];
		$by = $Hrpy[$count];
		if(($land->[$bx][$by] == $HlandBase) ||
		   ($land->[$bx][$by] == $HlandSbase)) {
		    last;
		}
		$count++;
	    }
	    if($count >= $HpointNumber) {
		# ���Ĥ���ʤ��ä��餽���ޤ�
		last;
	    }
	    # �����Ĵ��Ϥ����ä��Τǡ�flag��Ω�Ƥ�
	    $flag = 1;	   

	    # ���ϤΥ�٥�򻻽�
	    my($level) = expToLevel($land->[$bx][$by], $landValue->[$bx][$by]);
	    # ������ǥ롼��
	    while(($level > 0) &&
		  ($arg > 0) &&
		  ($island->{'money'} > $cost)) {
		# ��ä��Τ�����ʤΤǡ����ͤ���פ�����
		$level--;
		$arg--;
		$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
		# ����������
		my($r) = random($err);
		$tx = $x + $ax[$r];
		$ty = $y + $ay[$r];

		# �������ϰ��⳰�����å�
		if(($tx < 0) || ($tx >= $HislandSize) ||
		   ($ty < 0) || ($ty >= $HislandSize)) {
		    # �ϰϳ�
		    if(($kind == $HcomMissileST)|| ($kind == $HcomRazer)|| ($kind == $HcomPMS)){
			# ���ƥ륹
			logMsOutS($id, $target, $name, $tName,
				   $comName, $point);
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}
		    } else {
			# �̾��
			logMsOut($id, $target, $name, $tName,
				  $comName, $point);
		    }
		    next;
		}

		# ���������Ϸ�������
		my($tL) = $tLand->[$tx][$ty];
		my($tLv) = $tLandValue->[$tx][$ty];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($tx, $ty)";

		# �ɱһ���Ƚ��
		my($defence) = 0;
		if($HdefenceHex[$id][$tx][$ty] == 1) {
		    $defence = 1;
		} elsif($HdefenceHex[$id][$tx][$ty] == -1) {
		    $defence = 0;
		} else {
		    if($tL == $HlandDefence) {
			# �ɱһ��ߤ�̿��
			# �ե饰�򥯥ꥢ
			my($i, $count, $sx, $sy);
			for($i = 0; $i < 13; $i++) {
			    $sx = $tx + $ax[$i];
			    $sy = $ty + $ay[$i];


			    if(($sx < 0) || ($sx >= $HislandSize) ||
			       ($sy < 0) || ($sy >= $HislandSize)) {
				# �ϰϳ��ξ�粿�⤷�ʤ�
			    } else {
				# �ϰ���ξ��
				$HdefenceHex[$id][$sx][$sy] = 0;
			    }
			}
}elsif($tL == $HlandSefence) {
			# �ɱһ��ߤ�̿��
			# �ե饰�򥯥ꥢ
			my($i, $count, $sx, $sy);
			for($i = 0; $i < 25; $i++) {
			    $sx = $tx + $ax[$i];
			    $sy = $ty + $ay[$i];

			    if(($sx < 0) || ($sx >= $HislandSize) ||
			       ($sy < 0) || ($sy >= $HislandSize)) {
				# �ϰϳ��ξ�粿�⤷�ʤ�
			    } else {
				# �ϰ���ξ��
				$HdefenceHex[$id][$sx][$sy] = 0;
			    }
			}
}elsif(($tL == $HlandMonster)&&($tLv > 190)&&($tLv <= 199)) {
			$HdefenceHex[$id][$tx][$ty] = 1;
			$defence = 1;
		    } elsif(countAround($tLand, $tx, $ty, $HlandMonster, 25)) {
			my($i, $count, $sx, $sy);
$kaikai = 0;
			for($i = 0; $i < 25; $i++) {
			    $sx = $tx + $ax[$i];
			    $sy = $ty + $ay[$i];


			    if(($sx < 0) || ($sx >= $HislandSize) ||
			       ($sy < 0) || ($sy >= $HislandSize)) {
				# �ϰϳ��ξ�粿�⤷�ʤ�
			    } else {
				# �ϰ���ξ��
				$HdefenceHex[$id][$sx][$sy] = 0;
			    }
if(($tLand->[$sx][$sy] == $HlandMonster)&&($tLandValue->[$sx][$sy] > 190)&&($tLandValue->[$sx][$sy] <= 199)){
$kaikai++;
}
			}
if($kaikai > 0){
	$HdefenceHex[$id][$tx][$ty] = 1;
			$defence = 1;
}
		    } elsif(countAround($tLand, $tx, $ty, $HlandDefence, 13)) {
			$HdefenceHex[$id][$tx][$ty] = 1;
			$defence = 1;
		    } elsif(countAround($tLand, $tx, $ty, $HlandSefence, 25)) {
			$HdefenceHex[$id][$tx][$ty] = 1;
			$defence = 1;
		    } else {
			$HdefenceHex[$id][$tx][$ty] = -1;
			$defence = 0;
		    }
		}
if($tIsland->{'bouei'} > 0){
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
my($nii) =($tIsland->{'bouei'} * 1.5) + 10;
if(random(100) < $nii){
$defence = 1;
}
}
if($kind == $HcomMissileUB){
$defence = 0;
}
		if($defence == 1) {
		    # ��������
		    if(($kind == $HcomMissileST)|| ($kind == $HcomRazer)|| ($kind == $HcomPMS)) {
			# ���ƥ륹
			logMsCaughtS($id, $target, $name, $tName,
				      $comName, $point, $tPoint);
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}
		    } else {
			# �̾��
			logMsCaught($id, $target, $name, $tName,
				     $comName, $point, $tPoint);
		    }
		    next;
		}

		# �ָ��̤ʤ���hex��ǽ��Ƚ��

      if(($kind != $HcomMissileRE) &&
         ((($tL == $HlandSea) && ($tLv == 0)) || # ������
         ((($tL == $HlandSea) ||   # ���ޤ��ϡ�����
           ($tL == $HlandSbase) ||   # ������Ϥޤ��ϡ�����
($tL == $HlandLake) ||
           ($tL == $HlandMountain)) # ���ǡ�����
          && ($kind != $HcomMissileLD)))){ # Φ���ưʳ�
		    # ������Ϥξ�硢���Υե�
		    if($tL == $HlandSbase) {
			$tL = $HlandSea;
		    }
		    $tLname = landName($tL, $tLv);

		    # ̵����
		    if(($kind == $HcomMissileST)|| ($kind == $HcomRazer)|| ($kind == $HcomPMS)) {
			# ���ƥ륹
			logMsNoDamageS($id, $target, $name, $tName,
					$comName, $tLname, $point, $tPoint);
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}
		    } else {
			# �̾��
			logMsNoDamage($id, $target, $name, $tName,
				       $comName, $tLname, $point, $tPoint);
		    }
		    next;
		}

		# �Ƥμ����ʬ��# �Ƥμ����ʬ��
      if($kind == $HcomMissileRE) {
        if($tL == $HlandMountain){
          # �������Ƥ������̵��
          logMsNoDamage($id, $target, $name, $tName,
                        $comName, $tLname, $point, $tPoint);
          next;
       } elsif($tL == $HlandSbase){
          
          $tLand->[$tx][$ty] = $HlandSea;
        $tLandValue->[$tx][$ty] = 1;
          logMsRESbase($id, $target, $name, $tName,
                       $comName, $tLname, $point, $tPoint);
          next;
        } elsif($tL == $HlandOil) {
if($tLv ==0){
          
          $tLand->[$tx][$ty] = $HlandSea;
         $tLandValue->[$tx][$ty] = 1;
          logMsREOil($id, $target, $name, $tName,
                     $comName, $tLname, $point, $tPoint);
          next;
}else{
        
 $tLand->[$tx][$ty] = $HlandWaste;
            $tLandValue->[$tx][$ty] = 0;
          logMsREYou($id, $target, $name, $tName,
                     $comName, $tLname, $point, $tPoint);
          next;
}
        } elsif(($tL == $HlandSea)|| ($tL == $HlandLake)) {
          if($tLv == 1){
            # �����ξ��
            $tLand->[$tx][$ty] = $HlandWaste;
            $tLandValue->[$tx][$ty] = 0;
            logMsRESea1($id, $target, $name, $tName,
                        $comName, $tLname, $point, $tPoint);

            $tIsland->{'area'}++;

            if($seaCount <= 4) {
              # ����γ���3�إå�������ʤΤǡ������ˤ���
              my($i, $sx, $sy);
              for($i = 1; $i < 5; $i++) {
                $sx = $x + $ax[$i];
                $sy = $y + $ay[$i];


                if(($sx < 0) || ($sx >= $HislandSize) ||
                   ($sy < 0) || ($sy >= $HislandSize)) {
                } else {
                # �ϰ���ξ��
                  if($tLand->[$sx][$sy] == $HlandSea) {
                    $tLandValue->[$sx][$sy] = 1;
                  }
                }
              }
            }
            next;
          } else {
            # ���ʤ顢��Ū�ξ��������ˤ���
            $tLand->[$tx][$ty] = $HlandSea;
            $tLandValue->[$tx][$ty] = 1;
            logMsRESea($id, $target, $name, $tName,
                       $comName, $tLname, $point, $tPoint);

            next;

          }
        } elsif($tL == $HlandMonster){
          logMsREMonster($id, $target, $name, $tName,
                         $comName, $tLname, $point, $tPoint);
          # ���ˤʤ�
          $tLand->[$tx][$ty] = $HlandMountain;
          $tLandValue->[$tx][$ty] = 0;
          next;
        }else{

        logMsRELand($id, $target, $name, $tName,
                    $comName, $tLname, $point, $tPoint);
        # ���ˤʤ�
        $tLand->[$tx][$ty] = $HlandMountain;
        $tLandValue->[$tx][$ty] = 0;
        next;
}
} elsif($kind == $HcomMissileNEB) {
logMsNeutron($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint);
wideDamageNeutron($id, $target, $tName, $tLand, $tLandValue, $tx, $ty);
next;
} elsif($kind == $HcomMissileUC) {
logUCmiss($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint);
wideDamage($target, $tName, $tLand, $tLandValue, $tx, $ty);
next;
} elsif($kind == $HcomMissileLD) {
		    # Φ���˲���
		    if($tL == $HlandMountain) {
			# ��(���Ϥˤʤ�)
			logMsLDMountain($id, $target, $name, $tName,
					 $comName, $tLname, $point, $tPoint);
			# ���Ϥˤʤ�
			$tLand->[$tx][$ty] = $HlandWaste;
			$tLandValue->[$tx][$ty] = 0;
			next;

		    } elsif($tL == $HlandSbase) {
			# �������
			logMsLDSbase($id, $target, $name, $tName,
				      $comName, $tLname, $point, $tPoint);
		    } elsif($tL == $HlandMonster) {
			# ����
			logMsLDMonster($id, $target, $name, $tName,
					$comName, $tLname, $point, $tPoint);
		    } elsif(($tL == $HlandSea)|| ($tL == $HlandLake)) {
			# ����
			logMsLDSea1($id, $target, $name, $tName,
				    $comName, $tLname, $point, $tPoint);
		    } else {
			# ����¾
			logMsLDLand($id, $target, $name, $tName,
				     $comName, $tLname, $point, $tPoint);
		    }
		    
		    # �и���
		    if($tL == $HlandTown) {
			if(($land->[$bx][$by] == $HlandBase) ||
			   ($land->[$bx][$by] == $HlandSbase)) {
			    # �ޤ����Ϥξ��Τ�
			    $landValue->[$bx][$by] += int($tLv / 20);
			    if($landValue->[$bx][$by] > $HmaxExpPoint) {
				$landValue->[$bx][$by] = $HmaxExpPoint;
			    }
			}
		    }

		    # �����ˤʤ�
		    $tLand->[$tx][$ty] = $HlandSea;
		    $tIsland->{'area'}--;
		    $tLandValue->[$tx][$ty] = 1;

		    # �Ǥ����ġ�������������Ϥ��ä��鳤
		    if(($tL == $HlandOil) ||
			($tL == $HlandSea) ||
($tL == $HlandLake)||
		       ($tL == $HlandSbase)) {
			$tLandValue->[$tx][$ty] = 0;
		    }
		} else {
		    # ����¾�ߥ�����
		    if($tL == $HlandWaste) {
			# ����(�ﳲ�ʤ�)
			if(($kind == $HcomMissileST)|| ($kind == $HcomRazer)|| ($kind == $HcomPMS)) {
			    # ���ƥ륹
			    logMsWasteS($id, $target, $name, $tName,
					 $comName, $tLname, $point, $tPoint);
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}
			} else {
			    # �̾�
			    logMsWaste($id, $target, $name, $tName,
					$comName, $tLname, $point, $tPoint);
			}
		    } elsif(($tL == $HlandMonster) || ($tL == $Hlandhokak)){
			# ����
			my($mKind, $mName, $mHp) = monsterSpec($tLv);
			my($special) = $HmonsterSpecial[$mKind];
if(($HmonsterSpecial[$mKind] == 14)&&(random(1000) == 0)){
logmonkami($id, $target, $name, $tName,$comName, $mName, $point,$tPoint);
next;
}elsif(($HmonsterSpecial[$mKind] == 18)&&(random(10) > 5)){
logmonkami($id, $target, $name, $tName,$comName, $mName, $point,$tPoint);
next;
}else{
if($kind == $HcomMissileMK){
if(random(100) < 10){
$tLand->[$tx][$ty] = $Hlandhokak;
logmonhoka($id, $target, $name, $tName,$comName, $mName, $point,$tPoint);
next;
} else {
logmonhosi($id, $target, $name, $tName,$comName, $mName, $point,$tPoint);
next;
}
} else {
			# �Ų���?
			if((($special == 3) && (($HislandTurn % 2) == 1)) ||
			   (($special == 4) && (($HislandTurn % 2) == 0))||
			   (($special == 12) && (random (100) < 50))) {
			    # �Ų���
			    if(($kind == $HcomMissileST)|| ($kind == $HcomRazer)) {
				# ���ƥ륹
				logMsMonNoDamageS($id, $target, $name, $tName,
					     $comName, $mName, $point,
					     $tPoint);
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}
			    } else {
				# �̾���
				logMsMonNoDamage($id, $target, $name, $tName,
					     $comName, $mName, $point,
					     $tPoint);
			    }
			    next;
			} else {
			    # �Ų��椸��ʤ�
my($hit) = random(5)+1;
			    if(($mHp == 1)&& ($kind != $HcomMissileHP)&&($kind != $HcomPMS)) {
				# ���ä��Ȥ᤿
				if(($land->[$bx][$by] == $HlandBase) ||
				   ($land->[$bx][$by] == $HlandSbase)) {
				    # �и���
				    $landValue->[$bx][$by] += $HmonsterExp[$mKind];
				    if($landValue->[$bx][$by] > $HmaxExpPoint) {
					$landValue->[$bx][$by] = $HmaxExpPoint;
				    }
				}

				if(($kind == $HcomMissileST)||($kind == $HcomRazer)) {
				    # ���ƥ륹
				    logMsMonKillS($id, $target, $name, $tName,
						  $comName, $mName, $point,
						  $tPoint);
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}
				} else {
				    # �̾�
				    logMsMonKill($id, $target, $name, $tName,
						 $comName, $mName, $point,
						 $tPoint);
				}

				# ����
				my($value) = $HmonsterValue[$mKind];
				if($value > 0) {
				    $tIsland->{'money'} += $value;
$tIsland->{'shuu'} += $value;
                                    $island->{'money'} += $value;
$island->{'shuu'} += $value;
				    logMsMonMoney($target, $mName, $value, $name);
				}

				# �޴ط�
				my($prize) = $island->{'prize'};
				$prize =~ /([0-9]*),([0-9]*),(.*)/;
				my($flags) = $1;
				my($monsters) = $2;
				my($turns) = $3;
				my($v) = 2 ** $mKind;
				$monsters |= $v;
				$island->{'prize'} = "$flags,$monsters,$turns";
my($monsnumber) = $island->{'monsnumber'};
my($i);
my(@monsnumber) = split(/,/ ,$monsnumber);
for($i = 0; $i < $HmonsterNumber; $i++) {
if($i == $mKind) {
$monsnumber[$i]++
}
}
$island->{'monsnumber'} = join (',',@monsnumber);
$island->{'monka'} ++;
}elsif(($mHp <= $hit)&&($kind == $HcomPMS)) {
				# ���ä��Ȥ᤿
				if(($land->[$bx][$by] == $HlandBase) ||
				   ($land->[$bx][$by] == $HlandSbase)) {
				    # �и���
				    $landValue->[$bx][$by] += $HmonsterExp[$mKind];
				    if($landValue->[$bx][$by] > $HmaxExpPoint) {
					$landValue->[$bx][$by] = $HmaxExpPoint;
				    }
				}
				    # ���ƥ륹
				    logMsMonKillS($id, $target, $name, $tName,
						  $comName, $mName, $point,
						  $tPoint);
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}


				# ����
				my($value) = $HmonsterValue[$mKind];
				if($value > 0) {
				    $tIsland->{'money'} += $value;
$tIsland->{'shuu'} += $value;
                                    $island->{'money'} += $value;
$island->{'shuu'} += $value;
				    logMsMonMoney($target, $mName, $value, $name);
				}

				# �޴ط�
				my($prize) = $island->{'prize'};
				$prize =~ /([0-9]*),([0-9]*),(.*)/;
				my($flags) = $1;
				my($monsters) = $2;
				my($turns) = $3;
				my($v) = 2 ** $mKind;
				$monsters |= $v;
				$island->{'prize'} = "$flags,$monsters,$turns";
my($monsnumber) = $island->{'monsnumber'};
my($i);
my(@monsnumber) = split(/,/ ,$monsnumber);
for($i = 0; $i < $HmonsterNumber; $i++) {
if($i == $mKind) {
$monsnumber[$i]++
}
}
$island->{'monsnumber'} = join (',',@monsnumber);
$island->{'monka'} ++;
			    } else {
				# ���������Ƥ�
				if(($kind == $HcomMissileST)|| ($kind == $HcomRazer)|| ($kind == $HcomPMS)) {
				    # ���ƥ륹
				    logMsMonsterS($id, $target, $name, $tName,
						  $comName, $mName, $point,
						  $tPoint);
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}
} elsif($kind == $HcomMissileHP) {
if(($mHp < 9)|| (($special == 21)&&($mHp < 5))){
# ����
logMsMonsterH($id, $target, $name, $tName,
$comName, $mName, $point,
$tPoint);
} else {#���Ϥ�9���ä��餳���������
logMsMonsterM($id, $target, $name, $tName,
$comName, $mName, $point,
$tPoint);
}
				} else {
				    # �̾�
				    logMsMonster($id, $target, $name, $tName,
						 $comName, $mName, $point,
						 $tPoint);
				}
if($special == 13){
if($mHp != 9){
$tLandValue->[$tx][$ty]++;
next;
}
}else{
if($kind == $HcomMissileHP){
# HP��1������
if($mHp < 9) {#���Ϥ�9�ʲ��ξ��������롣
$tLandValue->[$tx][$ty]++;
}
#���Ϥ�9���ä���ʤˤ⤻���˽�λ
next;
}
				# HP��1����
if($kind == $HcomPMS){
	$tLandValue->[$tx][$ty] -= $hit;
				next;
}else{
				$tLandValue->[$tx][$ty]--;
				next;
}
}
	if(($land->[$bx][$by] == $HlandBase) ||
				   ($land->[$bx][$by] == $HlandSbase)) {
				    # �и���
				    $landValue->[$bx][$by] += 1;
				    if($landValue->[$bx][$by] > $HmaxExpPoint) {
					$landValue->[$bx][$by] = $HmaxExpPoint;
				    }
				}
			    }
}
}
			}
		    } else {
			# �̾��Ϸ�
			if(($kind == $HcomMissileST)|| ($kind == $HcomRazer)|| ($kind == $HcomPMS)) {
			    # ���ƥ륹
			    logMsNormalS($id, $target, $name, $tName,
					   $comName, $tLname, $point,
					   $tPoint);
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}
			} else {
			    # �̾�
			    logMsNormal($id, $target, $name, $tName,
					 $comName, $tLname, $point,
					 $tPoint);
			}
		    }
		    # �и���
		    if($tL == $HlandTown) {
			if(($land->[$bx][$by] == $HlandBase) ||
			    ($land->[$bx][$by] == $HlandSbase)) {
			    $landValue->[$bx][$by] += int($tLv / 20);
			    $boat += $tLv; # �̾�ߥ�����ʤΤ���̱�˥ץ饹
			    if($landValue->[$bx][$by] > $HmaxExpPoint) {
				$landValue->[$bx][$by] = $HmaxExpPoint;
			    }
			}
		    }
		    if($tL == $HlandHaribote) {
if($tLv >0) { # ��Ԥ��˲�������
$value =$tLv * 500;
$island->{'money'} +=  $value;
$island->{'shuu'} +=  $value;
logMsBank($id, $name, $value);
}
}
                    # ���Ϥˤʤ�
		    $tLand->[$tx][$ty] = $HlandWaste;
		    $tLandValue->[$tx][$ty] = 1; # ������

		    # �Ǥ����Ĥ��ä��鳤
		    if($tL == $HlandOil) {
			$tLand->[$tx][$ty] = $HlandSea;
			$tLandValue->[$tx][$ty] = 0;
		    }
		} 
	    }

	    # ����������䤷�Ȥ�
	    $count++;
	}


	if($flag == 0) {
	    # ���Ϥ���Ĥ�̵���ä����
	    logMsNoBase($id, $name, $comName);
	    return 0;
	}

	# ��̱Ƚ��
	$boat = int($boat / 2);
	if(($boat > 0) && ($id != $target) && ($kind != $HcomMissileST)) {
	    # ��̱ɺ��
	    my($achive); # ��ã��̱
	    my($i);
	    for($i = 0; ($i < $HpointNumber && $boat > 0); $i++) {
		$bx = $Hrpx[$i];
		$by = $Hrpy[$i];
		if($land->[$bx][$by] == $HlandTown) {
		    # Į�ξ��
		    my($lv) = $landValue->[$bx][$by];
		    if($boat > 50) {
			$lv += 50;
			$boat -= 50;
			$achive += 50;
		    } else {
			$lv += $boat;
			$achive += $boat;
			$boat = 0;
		    }
		    if($lv > 200) {
			$boat += ($lv - 200);
			$achive -= ($lv - 200);
			$lv = 200;
		    }
		    $landValue->[$bx][$by] = $lv;
		} elsif($land->[$bx][$by] == $HlandPlains) {
		    # ʿ�Ϥξ��
		    $land->[$bx][$by] = $HlandTown;;
		    if($boat > 10) {
			$landValue->[$bx][$by] = 5;
			$boat -= 10;
			$achive += 10;
		    } elsif($boat > 5) {
			$landValue->[$bx][$by] = $boat - 5;
			$achive += $boat;
			$boat = 0;
		    }
		}
		if($boat <= 0) {
		    last;
		}
	    }
	    if($achive > 0) {
		# �����Ǥ����夷����硢�����Ǥ�
		logMsBoatPeople($id, $name, $achive);

		# ��̱�ο���������ʾ�ʤ顢ʿ�¾ޤβ�ǽ������
		if($achive >= 200) {
		    my($prize) = $island->{'prize'};
		    $prize =~ /([0-9]*),([0-9]*),(.*)/;
		    my($flags) = $1;
		    my($monsters) = $2;
		    my($turns) = $3;

		    if((!($flags & 8)) &&  $achive >= 200){
			$flags |= 8;
			logPrize($id, $name, $Hprize[4]);
$island->{'money'} += 300;
$island->{'shuu'} += 300;
logPzMoney($id, $name, 300); 
		    } elsif((!($flags & 16)) &&  $achive > 500){
			$flags |= 16;
			logPrize($id, $name, $Hprize[5]);
$island->{'money'} += 500;
$island->{'shuu'} += 500;
logPzMoney($id, $name, 500); 
		    } elsif((!($flags & 32)) &&  $achive > 800){
			$flags |= 32;
			logPrize($id, $name, $Hprize[6]);
$island->{'money'} += 1000;
$island->{'shuu'} += 1000;
logPzMoney($id, $name, 1000);
  } elsif((!($flags & 1024)) &&  $achive > 2000){
			$flags |= 1024;
			logPrize($id, $name, $Hprize[11]);
$island->{'money'} += 10000;
$island->{'shuu'} += 10000;
logPzMoney($id, $name, 10000); 
		    }
		    $island->{'prize'} = "$flags,$monsters,$turns";
		}
	    }
	}
	return 1;
}
    } elsif(($kind == $HcomSendMonster) || ($kind == $HcomSendMonster2)|| ($kind == $HcomSendMonster3)|| ($kind == $HcomSendMonster4)|| ($kind == $HcomSendMonster5)){
	# �����ɸ�
	# �����ɸ����ĳ�ǧ
	if (($HislandTurn - $island->{'birth'}) <= $HdisableSendMonsterTurn) {
	    logNotPermitted($id, $name, $comName);
	    return 1;
	}
	if ($island->{'gun'} == 0) {
	    logNoKoku($id, $name, $comName);
	    return 0;
	}

	# �������åȼ���
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};

	if($tn eq '') {
	    # �������åȤ����Ǥˤʤ�
	    logMsNoTarget($id, $name, $comName);
	    return 0;
	}
if($tIsland->{'teikou'} >0){
logteidame($id, $target, $name, $tName, $comName);
}elsif($island->{'teikou'} >0){
logteideme($id, $name, $comName);
}else{
	# ��å�����
if($kind == $HcomSendMonster){
if($island->{'Inok'} >1){
$tIsland->{'monstersend'}++;
logMonsSend($id, $target, $name, $tName);
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
	return 1;
}else{
logMonsSendDamez($id, $target, $name, $tName);
return 0;
}
}elsif($kind == $HcomSendMonster2){
if($island->{'Inok'} >3){
$tIsland->{'monstersend2'}++;
logMonsSend($id, $target, $name, $tName);
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
	return 1;
}else{
logMonsSendDamez($id, $target, $name, $tName);
return 0;
}
}elsif($kind == $HcomSendMonster3){
if($island->{'Inok'} >5){
$tIsland->{'monstersend3'}++;
logMonsSend($id, $target, $name, $tName);
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
	return 1;
}else{
logMonsSendDamez($id, $target, $name, $tName);
return 0;
}
}elsif($kind == $HcomSendMonster4){
if($island->{'Inok'} >7){
$tIsland->{'monstersend4'}++;
logMonsSend($id, $target, $name, $tName);
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
	return 1;
}else{
logMonsSendDamez($id, $target, $name, $tName);
return 0;
}
} else {
if($island->{'Inok'} >9){
$tIsland->{'monstersend5'}++;
logMonsSend($id, $target, $name, $tName);
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
	return 1;
}else{
logMonsSendDamez($id, $target, $name, $tName);
return 0;
}
}
}
    } elsif($kind == $HcomOilSell) {
if($island->{'mina'} > 0){
	# ͢���̷���
	if($arg == 0) { $arg = 1; }
	my($value) = min($arg*10 , $island->{'oil'});

	# ͢�Х�
	logOilSell($id, $name, $comName, $value);
	$island->{'oil'} -=  $value;
	$island->{'money'} += $value;
$island->{'shuu'} += $value;
	return 0;
}else{
lognasimina($id, $name, $comName);
return 0;
}
    } elsif($kind == $HcomSell) {
if($island->{'mina'} > 0){
	# ͢���̷���
	if($arg == 0) { $arg = 1; }
	my($value) = min($arg * (-$cost), $island->{'food'});

	# ͢�Х�
	logSell($id, $name, $comName, $value);
	$island->{'food'} -=  $value;
	$island->{'money'} += ($value / 10);
$island->{'shuu'} += ($value / 10);
	return 0;
}else{
lognasimina($id, $name, $comName);
return 0;
}
    } elsif($kind == $HcomOilImport) {
if($island->{'mina'} > 0){
# ͢���̷���
if($arg == 0) { $arg = 1; }
my($value) = $arg*10;

# ͢����
logOilSell($id, $name, $comName, $value);
$island->{'oil'} += $value;
$island->{'money'} -= $value;
$island->{'shuu'} -= $value;
return 0;
}else{
lognasimina($id, $name, $comName);
return 0;
}
    } elsif($kind == $HcomImport) {
if($island->{'mina'} > 0){
# ͢���̷���
if($arg == 0) { $arg = 1; }
my($value) = $arg * $cost;

# ͢����
logSell($id, $name, $comName, $value);
$island->{'food'} += $value;
$island->{'money'} -= ($value / 5);
$island->{'shuu'} -= ($value / 5);
return 0;
}else{
lognasimina($id, $name, $comName);
return 0;
}
} elsif(($kind == $HcomShakufi) ||
($kind == $HcomShakuse) ||
($kind == $HcomShakuth)) {
if($arg == 0) { $arg = 100; }
my($value) = 0;
if($island->{'shaka'} == 0){
$value = $arg * 100;
$island->{'money'} += $value;
$island->{'shuu'} += $value;
if($kind == $HcomShakufi){
$island->{'shaka'} += 10;
$island->{'shamo'} += $value / 9;
logShaku($id, $name, $comName, $value);
}elsif($kind == $HcomShakuse){
$island->{'shaka'} += 50;
$island->{'shamo'} += $value / 35;
logShaku($id, $name, $comName, $value);
}elsif($kind == $HcomShakuth){
$island->{'shaka'} += 100;
$island->{'shamo'} += $value / 50;
logShaku($id, $name, $comName, $value);
}
$island->{'shafl'} = 1;
}else{
logShakubame($id, $name, $comName);
}
return 0;
} elsif(($kind == $HcomRob) || ($kind == $HcomRobST)){
	if ($island->{'gun'} == 0) {
	    logNoKoku($id, $name, $comName);
	    return 0;
	}
# ��å
if($arg == 0) { $arg = 1; }
# �������åȼ���
my($tn) = $HidToNumber{$target};
my($tIsland) = $Hislands[$tn];
my($tName) = $tIsland->{'name'};
my($RobFood, $RobMoney) = ($arg * 100, $arg * 100);
$island->{'money'} -= $arg * $cost;
$island->{'shuu'} -= $arg * $cost;
if($tn eq '') {
# �������åȤ����Ǥˤʤ�
logMsNoTarget($id, $name, $comName);
return 0;
}
my($saef) = 100 - $arg;
if(((random(200) <= $saef) && ($kind == $HcomRob)) ||
((random(300) <= $saef) && ($kind == $HcomRobST))){
# ��å����
# ���å
if($tIsland->{'money'} >= $RobMoney){
$tIsland->{'money'} -= $RobMoney;
$tIsland->{'shuu'} -= $RobMoney;
$island->{'money'} += $RobMoney;
$island->{'shuu'} += $RobMoney;
if($kind == $HcomRob){
logRobMoney($id, $target, $name, $tName, $comName, $RobMoney);
} else {
logRobSTMoney($id, $target, $name, $tName, $comName, $RobMoney);
}
} else {
# ��å�����̤������礭���������
$RobMoney = $tIsland->{'money'};
$tIsland->{'money'} = 0;
$island->{'money'} += $RobMoney;
$island->{'shuu'} += $RobMoney;
if($kind == $HcomRob){
logRobMoney($id, $target, $name, $tName, $comName, $RobMoney);
} else {
logRobSTMoney($id, $target, $name, $tName, $comName, $RobMoney);
}
}

# �����⶯å
if($tIsland->{'food'} >= $RobFood){
$tIsland->{'food'} -= $RobFood;
$island->{'food'} += $RobFood;
if($kind == $HcomRob){
logRobFood($id, $target, $name, $tName, $comName, $RobFood);
} else {
logRobSTFood($id, $target, $name, $tName, $comName, $RobFood);
}
} else {
# ��å�����̤������礭���������
$RobFood = $tIsland->{'food'};
$tIsland->{'food'} = 0;
$island->{'food'} += $RobFood;
if($kind == $HcomRob){
logRobFood($id, $target, $name, $tName, $comName, $RobFood);
} else {
logRobSTFood($id, $target, $name, $tName, $comName, $RobFood);
}
}
} else {
# ��å����
logMissRob($id, $target, $name, $tName, $comName);
}
return 1;
} elsif(($kind == $HcomOil)||
($kind == $HcomOilH)){
	# �����
	if (($HislandTurn - $island->{'birth'}) <= $HdisableMonsterTurn) {
	    logNotPermitted($id, $name, $comName);
	    return 1;
	}
if($island->{'mina'} > 0){
	# �������åȼ���
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
	# ����̷���
	if($arg == 0) { $arg = 1; }
	my($value, $str);
	    $value = min($arg*10, $island->{'oil'});
	    $str = "$value�ȥ�";
	    $island->{'oil'} -= $value;
	    $tIsland->{'oil'} += $value;
		if($kind == $HcomOil){
	logAid($id, $target, $name, $tName, $comName, $str);
}else{
logAidH($id, $target, $name, $tName, $comName, $str);
}
}else{
lognasimina($id, $name, $comName);
}
return 0;
} elsif($kind == $HcomSlag){
	# �����
	if (($HislandTurn - $island->{'birth'}) <= $HdisableMonsterTurn) {
	    logNotPermitted($id, $name, $comName);
	    return 1;
	}
if($island->{'mina'} > 0){
	# �������åȼ���
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
	# ����̷���
	if($arg == 0) { $arg = 1; }
	my($value, $str);
	    $value = min($arg * 100, $island->{'slag'});
	    $str = "$value�ȥ�";
	    $island->{'slag'} -= $value;
	    $tIsland->{'slag'} += $value;
	logAid($id, $target, $name, $tName, $comName, $str);
}else{
lognasimina($id, $name, $comName);
}
return 0;
} elsif(($kind == $HcomFood) ||
($kind == $HcomFoodH)||
($kind == $HcomMoneyH)||
	    ($kind == $HcomMoney)) {
	# �����
	if (($HislandTurn - $island->{'birth'}) <= $HdisableMonsterTurn) {
	    logNotPermitted($id, $name, $comName);
	    return 1;
	}

	# �������åȼ���
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};

	# ����̷���
	if($arg == 0) { $arg = 1; }
	my($value, $str);
	if($cost < 0) {
	    $value = min($arg * (-$cost), $island->{'food'});
	    $str = "$value$HunitFood";
	} else {
	    $value = min($arg * ($cost), $island->{'money'});
	    $str = "$value$HunitMoney";
	}


	if($cost < 0) {
if($island->{'mina'} > 0){
	    $island->{'food'} -= $value;
	    $tIsland->{'food'} += $value;
if($kind == $HcomFood){
	logAid($id, $target, $name, $tName, $comName, $str);
}else{
logAidH($id, $target, $name, $tName, $comName, $str);
}
}else{
lognasimina($id, $name, $comName);
}	# �����
	} else {
	    $island->{'money'} -= $value;
$island->{'shuu'} -= $value;
	    $tIsland->{'money'} += $value;
	    $tIsland->{'shuu'} += $value;
	# �����
if($kind == $HcomMoney){
	logAid($id, $target, $name, $tName, $comName, $str);
}else{
logAidH($id, $target, $name, $tName, $comName, $str);
}
	}
	return 0;
    } elsif($kind == $HcomPropaganda) {
	# Ͷ�׳�ư
	logPropaganda($id, $name, $comName);
	$island->{'propaganda'} += 1;
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
if($arg > 1) {
my($command);
$arg--;
slideBack($comArray, 0);
$comArray->[0] = {
'kind' => $kind,
'target' => $target,
'x' => $x,
'y' => $y,
'arg' => $arg
};
}
	return 1;
    } elsif($kind == $Hcomteikou) {
if(($island->{'pop'} <500)&&($island->{'miu'}<5)){
if($island->{'teikou'} == 0){
	my($str) = random(5);
$island->{'teikou'} = $str;
	logteikou($id, $name,$str);
}else{
my($str) = random(5);
$island->{'teikou'} += $str;
logteitas($id, $name,$str);
}
}else{
logteimis($id, $name);
}
	return 0;
    } elsif($kind == $HcomGiveup) {
	# ����
	logGiveup($id, $name);
	$island->{'dead'} = 1;
	unlink("island.$id");
	return 1;
    } elsif ($kind == $Hcomkouei) {
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
if($island->{'kouei'} >0){
$island->{'kouei'} ++;
logkouk($id, $name);
if($island->{'kouei'} >10){
$island->{'kouei'} = 10;
}
} else {
if(random(4) > 0){
$island->{'kouei'}=1;
logkouei($id, $name, $comName);
} else {
logdamekouei($id, $name, $comName);
}
}
    } elsif ($kind == $Hcomkanei) {
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
if($island->{'kanei'} >0){
$island->{'kanei'} ++;
logkank($id, $name);
if($island->{'kanei'} >10){
$island->{'kanei'} = 10;
}
} else {
if(random(4) > 0){
$island->{'kanei'}=1;
logkouei($id, $name, $comName);
} else {
logdamekouei($id, $name, $comName);
}
}
    } elsif ($kind == $Hcombouei) {
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
if($island->{'bouei'} >0){
$island->{'bouei'} ++;
logbouk($id, $name);
if($island->{'bouei'} >10){
$island->{'bouei'} = 10;
}
} else {
if(random(4) > 0){
$island->{'bouei'}=1;
logkouei($id, $name, $comName);
} else {
logdamekouei($id, $name, $comName);
}
}
} elsif ($kind == $Hcomreiei) {
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
if($island->{'pmsei'} == 0){
if($island->{'reiei'} >0){
$island->{'reiei'} = $island->{'reiei'} % 10;
$island->{'reiei'} ++;
logreik($id, $name);
if($island->{'reiei'} >10){
$island->{'reiei'} = 10;
}
} else {
if(random(4) > 0){
$island->{'reiei'}=1;
logkouei($id, $name, $comName);
} else {
logdamekouei($id, $name, $comName);
}
}
}else{
logkoueikurukuru($id, $name, $comName);
}
} elsif ($kind == $Hcomhatei) {
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
if($island->{'hatei'} >0){
$island->{'hatei'} ++;
loghatk($id, $name);
if($island->{'hatei'} >10){
$island->{'hatei'} = 10;
}
} else {
if(random(4) > 0){
$island->{'hatei'}=1;
logkouei($id, $name, $comName);
} else {
logdamekouei($id, $name, $comName);
}
}
} elsif ($kind == $HcomPMSei) {
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
if($island->{'pmsei'} >0){
$island->{'pmsei'} = $island->{'pmsei'} % 10;
$island->{'pmsei'}++;
logemtk($id, $name);
if($island->{'pmsei'} >10){
$island->{'pmsei'} = 10;
}
}elsif($island->{'reiei'} >0){
$island->{'pmsei'} = 1;
$island->{'reiei'} = 0;
logemtx($id, $name);
} else {
logemty($id, $name);
}
} elsif ($kind == $HcomPMSuti) {
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
if(random(4) == 0){
$tIsland->{'pmsei'}= 0;
logpmsuti($id, $target, $name, $tName);
} else {
logdamepmsuti($id, $target, $name, $tName);
}
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}
} elsif ($kind == $Hcomkouuti) {
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
if(random(4) == 0){
$tIsland->{'kouei'}= 0;
logkouuti($id, $target, $name, $tName);
} else {
logdamekouuti($id, $target, $name, $tName);
}
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}
} elsif ($kind == $Hcombouuti) {
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
if(random(4) == 0){
$tIsland->{'bouei'}= 0;
logbouuti($id, $target, $name, $tName);
} else {
logdamebouuti($id, $target, $name, $tName);
}
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}
} elsif ($kind == $HcomHatuti) {
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
if(random(4) == 0){
$tIsland->{'hatei'}= 0;
loghatuti($id, $target, $name, $tName);
} else {
logdamehatuti($id, $target, $name, $tName);
}
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}
} elsif ($kind == $Hcomreiuti) {
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
if(random(4) == 0){
$tIsland->{'reiei'}= 0;
logreiuti($id, $target, $name, $tName);
} else {
logdamereiuti($id, $target, $name, $tName);
}
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}
} elsif ($kind == $Hcomkanuti) {
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};

if(random(4) == 0){
$tIsland->{'kanei'}= 0;
logkanuti($id, $target, $name, $tName);
} else {
logdamekanuti($id, $target, $name, $tName);
}
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}
} elsif ($kind == $Hcomsennyu) {
if($island->{'hei'} ==0){
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
$island->{'sen'}=1;
logdoumei($id, $name, $comName);
}else{
logsen($id, $name);
}
} elsif ($kind == $Hcomheinyu) {
if($island->{'sen'} ==0){
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
$island->{'hei'}=1;
logdoumei($id, $name, $comName);
}else{
loghei($id, $name);
}
}elsif ($kind == $Hcominonyu) {
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
$island->{'ino'}=1;
logdoumei($id, $name, $comName);
} elsif ($kind == $Hcomsende) {
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
$island->{'sen'}=0;
logdoumei($id, $name, $comName);
} elsif ($kind == $Hcomheide) {
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
$island->{'hei'}=0;
logdoumei($id, $name, $comName);
}elsif ($kind == $Hcominode) {
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
$island->{'ino'}=0;
logdoumei($id, $name, $comName);
}elsif ($kind == $Hcomteiko) {
if($island->{'sen'} ==1){
$island->{'sen'} = 11;
logteiko($id, $name, $comName);
}elsif($island->{'sen'} ==21){
logteikyo($id, $name, $comName);
}else{
logteimu($id, $name, $comName);
}
}elsif ($kind == $Hcomkyouko) {
if($island->{'sen'} ==1){
$island->{'sen'} = 21;
logteiko($id, $name, $comName);
}elsif($island->{'sen'} ==11){
logteikyo($id, $name, $comName);
}else{
logteimu($id, $name, $comName);
}
}elsif ($kind == $HcomGeki) {
if($island->{'Inok'} > 0) {
my($geki) = 5 + ($island->{'Inok'}*2);
if(random(100) < $geki){
$island->{'monfl'} = 1;
logGeki($id, $name, $comName);
} else {
$island->{'monfl'} = 0;
logGekidame($id, $name, $comName);
}
}else{
logInoknasi($id, $name, $comName);
return 0;
}
}elsif ($kind == $Hcomtimya) {
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
my($kaku) =$island->{'kiken'} * 9;
my($jikaku)=40 - ($island->{'kiken'} * 4);
my($bareku)=$tIsland->{'kishou'} * 10;
	my($tLand) = $tIsland->{'land'};
	my($tLandValue) = $tIsland->{'landValue'};
		my($tL) = $tLand->[$x][$y];
		my($tLv) = $tLandValue->[$x][$y];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($x, $y)";
if($island->{'kiken'} >0){
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
if(random(100) < $kaku){
        if($tL == $HlandMountain){
          # �������Ƥ������̵��
          logXsNoDamage($id, $target, $name, $tName,
                        $comName, $tLname, $point, $tPoint);
          next;
       } elsif($tL == $HlandSbase){
          
          $tLand->[$x][$y] = $HlandSea;
        $tLandValue->[$x][$y] = 1;
          logXsRESbase($id, $target, $name, $tName,
                       $comName, $tLname, $point, $tPoint);
          next;
        } elsif($tL == $HlandOil) {
if($tLv ==0){
          
          $tLand->[$x][$y] = $HlandSea;
         $tLandValue->[$x][$y] = 1;
          logXsREOil($id, $target, $name, $tName,
                     $comName, $tLname, $point, $tPoint);
          next;
}else{
        
 $tLand->[$x][$y] = $HlandWaste;
            $tLandValue->[$x][$y] = 0;
          logXsREYou($id, $target, $name, $tName,
                     $comName, $tLname, $point, $tPoint);
          next;
}
        } elsif(($tL == $HlandSea)|| ($tL == $HlandLake)) {
          if($tLv == 1){
            # �����ξ��
            $tLand->[$x][$y] = $HlandWaste;
            $tLandValue->[$x][$y] = 0;
            logXsRESea1($id, $target, $name, $tName,
                        $comName, $tLname, $point, $tPoint);

            $tIsland->{'area'}++;

            if($seaCount <= 4) {
              # ����γ���3�إå�������ʤΤǡ������ˤ���
              my($i, $sx, $sy);
              for($i = 1; $i < 5; $i++) {
                $sx = $x + $ax[$i];
                $sy = $y + $ay[$i];


                if(($sx < 0) || ($sx >= $HislandSize) ||
                   ($sy < 0) || ($sy >= $HislandSize)) {
                } else {
                # �ϰ���ξ��
                  if($tLand->[$sx][$sy] == $HlandSea) {
                    $tLandValue->[$sx][$sy] = 1;
                  }
                }
              }
            }
            next;
          } else {
            # ���ʤ顢��Ū�ξ��������ˤ���
            $tLand->[$x][$y] = $HlandSea;
            $tLandValue->[$x][$y] = 1;
            logXsRESea($id, $target, $name, $tName,
                       $comName, $tLname, $point, $tPoint);

            next;

          }
        } elsif($tL == $HlandMonster){
          logXsREMonster($id, $target, $name, $tName,
                         $comName, $tLname, $point, $tPoint);
          # ���ˤʤ�
          $tLand->[$x][$y] = $HlandMountain;
          $tLandValue->[$x][$y] = 0;
          next;
        }else{

        logXsRELand($id, $target, $name, $tName,
                    $comName, $tLname, $point, $tPoint);
        # ���ˤʤ�
        $tLand->[$x][$y] = $HlandMountain;
        $tLandValue->[$x][$y] = 0;
        next;
}
if(random(100)<$bareku){
logsaimitu($id, $target,$name, $tName, $comName);
}
} else {
if(random(100) < $jikaku){
$island->{'jisin'} ++;
$island->{'funka'} ++;
logjisaikou($id, $target, $name, $tName, $comName);
}else{
logsisai($id, $target, $name, $tName, $comName);
}
}
}else{
lognasi($id, $name, $comName);
}
}elsif(($kind ==$Hcomtaifuu) ||
	    ($kind ==$Hcomtunami) ||
	    ($kind ==$Hcomfunka) ||
	    ($kind ==$Hcominseki) ||
	    ($kind ==$Hcomdaiinseki) ||
	    ($kind ==$Hcomjisin) ||
	    ($kind ==$Hcomkasai) ||
	    ($kind ==$HcomOoame) ||
	    ($kind ==$Hcomjibantinka)){
if($tIsland->{'teikou'} >0){
logteidame($id, $target, $name, $tName, $comName);
}elsif($island->{'teikou'} >0){
logteideme($id, $name, $comName);
}else{
if ($kind == $Hcomtaifuu) {

	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
my($kaku) =$island->{'kiken'} * 9;
my($jikaku)=40 - ($island->{'kiken'} * 4);
my($bareku)=$tIsland->{'kishou'} * 10;
if($island->{'kiken'} >0){
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
if(random(100) < $kaku){
$tIsland->{'taifu'} ++;
logsaikou($id, $target, $name, $tName, $comName);
if(random(100)<$bareku){
logsaimitu($id, $target,$name, $tName, $comName);
}
} else {
if(random(100) < $jikaku){
$island->{'taifu'} ++;
logjisaikou($id, $target, $name, $tName, $comName);
}else{
logsisai($id, $target, $name, $tName, $comName);
}
}
}else{
lognasi($id, $name, $comName);
}
}elsif ($kind == $Hcomtunami) {

	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
my($kaku) =$island->{'kiken'} * 9;
my($jikaku)=40 -($island->{'kiken'} * 4);
my($bareku)=$tIsland->{'kishou'} * 10;
if($island->{'kiken'} >0){
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
if(random(100) < $kaku){
$tIsland->{'tunami'} ++;
logsaikou($id, $target, $name, $tName, $comName);
if(random(100)<$bareku){
logsaimitu($id, $target,$name, $tName, $comName);
}
} else {
if(random(100) < $jikaku){
$island->{'tunami'} ++;
logjisaikou($id, $target, $name, $tName, $comName);
}else{
logsisai($id, $target, $name, $tName, $comName);
}
}

}else{
lognasi($id, $name, $comName);
}
}elsif ($kind == $Hcomfunka) {

	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
my($kaku) =$island->{'kiken'} * 9;
my($jikaku)=40 -($island->{'kiken'} * 4);
my($bareku)=$tIsland->{'kishou'} * 10;
if($island->{'kiken'} >0){
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
if(random(100)< $kaku){
$tIsland->{'funka'} ++;
logsaikou($id, $target, $name, $tName, $comName);
if(random(100)<$bareku){
logsaimitu($id, $target,$name, $tName, $comName);
}
} else {
if(random(100) < $jikaku){
$island->{'funka'} ++;
logjisaikou($id, $target, $name, $tName, $comName);
}else{
logsisai($id, $target, $name, $tName, $comName);
}
}

}else{
lognasi($id, $name, $comName);
}
}elsif ($kind == $HcomOoame) {

	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
my($kaku) =$island->{'kiken'} * 9;
my($jikaku)=40 -($island->{'kiken'} * 4);
my($bareku)=$tIsland->{'kishou'} * 10;
if($island->{'kiken'} >0){
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
if(random(100)< $kaku){
$tIsland->{'ooame'} ++;
logsaikou($id, $target, $name, $tName, $comName);
if(random(100)<$bareku){
logsaimitu($id, $target,$name, $tName, $comName);
}
} else {
if(random(100) < $jikaku){
$island->{'ooame'} ++;
logjisaikou($id, $target, $name, $tName, $comName);
}else{
logsisai($id, $target, $name, $tName, $comName);
}
}
}else{
lognasi($id, $name, $comName);
}
}elsif ($kind == $Hcominseki){
	
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
my($kaku) =$island->{'kiken'} * 9;
my($jikaku)=40 -($island->{'kiken'} * 4);
my($bareku)=$tIsland->{'kishou'} * 10;
if($island->{'kiken'} >0){
$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
if(random(100)< $kaku){
$tIsland->{'inseki'} ++;
logsaikou($id, $target, $name, $tName, $comName);
if(random(100)<$bareku){
logsaimitu($id, $target,$name, $tName, $comName);
}
} else {
if(random(100)< $jikaku){
$island->{'inseki'} ++;
logjisaikou($id, $target, $name, $tName, $comName);
}else{
logsisai($id, $target, $name, $tName, $comName);
}
}

}else{
lognasi($id, $name, $comName);
}
}elsif ($kind == $Hcomdaiinseki){

	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
my($kaku) =$island->{'kiken'} * 9;
my($jikaku)=40 -($island->{'kiken'} * 4);
my($bareku)=$tIsland->{'kishou'} * 10;
if($island->{'kiken'} >0){
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
if(random(100) < $kaku){
$tIsland->{'daiin'} ++;
logsaikou($id, $target, $name, $tName, $comName);
if(random(100)<$bareku){
logsaimitu($id, $target,$name, $tName, $comName);
}
} else {
if(random(100) < $jikaku){
$island->{'daiin'} ++;
logjisaikou($id, $target, $name, $tName, $comName);
}else{
logsisai($id, $target, $name, $tName, $comName);
}
}

}else{
lognasi($id, $name, $comName);
}
}elsif ($kind == $Hcomjisin) {

	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
my($kaku) =$island->{'kiken'} * 9;
my($jikaku)=40 -($island->{'kiken'} * 4);
my($bareku)=$tIsland->{'kishou'} * 10;
if($island->{'kiken'} >0){
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
if(random(100) < $kaku){
$tIsland->{'jisin'} ++;
logsaikou($id, $target, $name, $tName, $comName);
if(random(100)<$bareku){
logsaimitu($id, $target,$name, $tName, $comName);
}
} else {
if(random(100) < $jikaku){
$island->{'jisin'} ++;
logjisaikou($id, $target, $name, $tName, $comName);
}else{
logsisai($id, $target, $name, $tName, $comName);
}
}

}else{
lognasi($id, $name, $comName);
}
}elsif ($kind == $Hcomkasai){

	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
my($kaku) =$island->{'kiken'} * 9;
my($jikaku)=40 -($island->{'kiken'} * 4);
my($bareku)=$tIsland->{'kishou'} * 10;
if($island->{'kiken'} >0){
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
if(random(100) < $kaku){
$tIsland->{'kasai'} ++;
logsaikou($id, $target, $name, $tName, $comName);
if(random(100)<$bareku){
logsaimitu($id, $target,$name, $tName, $comName);
}
} else {
if(random(100) < $jikaku){
$island->{'kasai'} ++;
logjisaikou($id, $target, $name, $tName, $comName);
}else{
logsisai($id, $target, $name, $tName, $comName);
}
}

}else{
lognasi($id, $name, $comName);
}
}elsif ($kind == $Hcomjibantinka){

	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
my($kaku) =$island->{'kiken'} * 9;
my($jikaku)=40 -($island->{'kiken'} * 4);
my($bareku)=$tIsland->{'kishou'} * 10;
if($island->{'kiken'} >0){
	$island->{'money'} -= $cost;
$island->{'shuu'}-= $cost;
if(random(100) < $kaku){
$tIsland->{'jiban'} ++;
logsaikou($id, $target, $name, $tName, $comName);
if(random(100)<$bareku){
logsaimitu($id, $target,$name, $tName, $comName);
}
} else {
if(random(100)< $jikaku){
$island->{'jiban'} ++;
logjisaikou($id, $target, $name, $tName, $comName);
}else{
logsisai($id, $target, $name, $tName, $comName);
}
}

}else{
lognasi($id, $name, $comName);
}
}
}
}
  return 1;
}

sub doMonMove {
    my($island) = @_;
    my(@monsterMove);

    # Ƴ����
    my($name) = $island->{'name'};
    my($id) = $island->{'id'};
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};

    my($x, $y, $i);
    for($i = 0; $i < $HpointNumber; $i++) {
	$x = $Hrpx[$i];
	$y = $Hrpy[$i];
	my($landKind) = $land->[$x][$y];
	my($lv) = $landValue->[$x][$y];	
if($landKind == $Hlandhokak) {
	    my($lName) = landName($l, $lv);
	    if(random(3) == 0) {
		    $land->[$x][$y] = $HlandMonster;
loghobakukaijo($id, $name, $lName, "($x, $y)");
	    }
	} elsif($landKind == $HlandMonster) {
	    if($monsterMove[$x][$y] == 2) {
		# ���Ǥ�ư������
		next;
	    }

	    # �����Ǥμ��Ф�
	    my($mKind, $mName, $mHp) = monsterSpec($landValue->[$x][$y]);
	    my($special) = $HmonsterSpecial[$mKind];

            # ����ǵ��äƤ�餦 # ��������
  if($HmonsterSpecial[$mKind] == 5) {
} elsif($HmonsterSpecial[$mKind] == 14){ 
if($island->{'pop'} < 8000){
            logkaeru($id, $name, $mName, "($x, $y)");
            $land->[$x][$y] = $HlandWaste;
            $landValue->[$x][$y] = 0;
            last;
}
} else {
my($kae) = ($island->{'Onpa'} * 1.5) + 10;
            if(random(1000) < $kae) {
            logkaeru($id, $name, $mName, "($x, $y)");
            $land->[$x][$y] = $HlandWaste;
            $landValue->[$x][$y] = 0;
            last;
            } 
}
	    # �Ų���?
	    if((($special == 3) && (($HislandTurn % 2) == 1)) ||
	       (($special == 4) && (($HislandTurn % 2) == 0))) {
		# �Ų���
		next;
	    }

	    # ư�����������
	    my($d, $sx, $sy);
	    my($i);
	    for($i = 0; $i < 3; $i++) {
		$d = random(4) + 1;
		$sx = $x + $ax[$d];
		$sy = $y + $ay[$d];



		# �ϰϳ�Ƚ��
		if(($sx < 0) || ($sx >= $HislandSize) ||
		   ($sy < 0) || ($sy >= $HislandSize)) {
		    next;
		}

		# �����������ġ����á�������ǰ��ʳ�
		if(($land->[$sx][$sy] != $HlandSea) &&
		   ($land->[$sx][$sy] != $HlandSbase) &&
		   ($land->[$sx][$sy] != $HlandOil) &&
		   ($land->[$sx][$sy] != $HlandLake)&&
		   ($land->[$sx][$sy] != $HlandMountain) &&
		   ($land->[$sx][$sy] != $HlandMonument) &&
		   ($land->[$sx][$sy] != $HlandMonster)) {
		    last;
		}
	    }

	    if($i == 3) {
		# ư���ʤ��ä�
		next;
	    }

	    # ư��������Ϸ��ˤ���å�����
	    my($l) = $land->[$sx][$sy];
	    my($lv) = $landValue->[$sx][$sy];
	    my($lName) = landName($l, $lv);
	    my($point) = "($sx, $sy)";
if($HmonsterSpecial[$mKind] == 5) {
if(random(40) < 2) {
$landValue->[$x][$y] = 69;
logEgg($id, $name, "($x, $y)");

} else {
($point) = "($x, $y)";
logmada($id, $name, "($x, $y)", $mName);
}
} elsif($HmonsterSpecial[$mKind] == 6) {
my($kind);
if(random(80) < 10) {
if(random(20) < 16) {
$kind = random(4) + 1;
$landValue->[$x][$y] = $kind * 10
		+ $HmonsterBHP[$kind] + random($HmonsterDHP[$kind]);
	    my($mKind, $mName, $mHp) = monsterSpec($landValue->[$x][$y]);

loghenka($id, $name, $mName, "($sx, $sy)");
} else {
if(random(100) == 0){
if(random(10) < 5){
$landValue->[$x][$y] = 219;
	    my($mKind, $mName, $mHp) = monsterSpec($landValue->[$x][$y]);
loghenka($id, $name, $mName, "($sx, $sy)");
}else{
if(random(10)<5){
$landValue->[$x][$y] = 209;
	    my($mKind, $mName, $mHp) = monsterSpec($landValue->[$x][$y]);
loghenka($id, $name, $mName, "($sx, $sy)");
}else{
$landValue->[$x][$y] = 199;
	    my($mKind, $mName, $mHp) = monsterSpec($landValue->[$x][$y]);
loghenka($id, $name, $mName, "($sx, $sy)");
}
}
}else{
$kind = random(12) + 7;
$landValue->[$x][$y] = $kind * 10
		+ $HmonsterBHP[$kind] + random($HmonsterDHP[$kind]);
	    my($mKind, $mName, $mHp) = monsterSpec($landValue->[$x][$y]);
loghenka($id, $name, $mName, "($sx, $sy)");
}
}
}
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # ��ȵ錄���֤���Ϥ�
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
} elsif($HmonsterSpecial[$mKind] == 7) {
if(random(20) < 16) {
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # ��ȵ錄���֤���Ϥ�
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;

} else {
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # ��ȵ錄���֤���Ϥ�
	    $land->[$x][$y] = $HlandMonster;
	    $landValue->[$x][$y] = 59;
logQee($id, $name, "($x, $y)", $mName);
}

} elsif ($HmonsterSpecial[$mKind] == 10) {
	    # ��ư
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # ��ȵ錄���֤���Ϥ�
	    $land->[$x][$y] = $HlandPlains;
	    $landValue->[$x][$y] = 0;
} elsif ($HmonsterSpecial[$mKind] == 11) {
if(random(100) < 10) {
$landValue->[$x][$y] += 20;
logMonsterkak($id, $name, $point, $mName);
}	    # ��ư
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # ��ȵ錄���֤���Ϥ�
	    $land->[$x][$y] = $HlandPlains;
	    $landValue->[$x][$y] = 0;
} elsif ($HmonsterSpecial[$mKind] == 13) {
	    # ��ư
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # ��ȵ錄���֤���Ϥ�
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
} elsif ($HmonsterSpecial[$mKind] == 15) {
my($sji) = random(8) + 5;
		$jx = $x + $ax[$sji];
		$jy = $y + $ay[$sji];


		# �������ϰ��⳰�����å�
		if(($jx < 0) || ($jx >= $HislandSize) ||
		   ($jy < 0) || ($jy >= $HislandSize)) {
		    # �ϰϳ�

			# �̾��
logMonUtiDame($id, $name, "($x, $y)", $mName);
		    }else{
		my($tL) = $land->[$jx][$jy];
		my($tLv) = $landValue->[$jx][$jy];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($jx, $jy)";
         if(($tL == $HlandSea) ||   # ���ޤ��ϡ�����
           ($tL == $HlandSbase) ||   # ������Ϥޤ��ϡ�����
(($tL == $HlandLake)&& ($tLv == 0))  ||
           ($tL == $HlandMountain)){ # Φ���ưʳ�
		    # ������Ϥξ�硢���Υե�
		    if($tL == $HlandSbase) {
			$tL = $HlandSea;
		    }
		    $tLname = landName($tL, $tLv);

			# ���ƥ륹
			logMsNoDamageT($id, $name, $tLname, $mName, $point, $tPoint);
}else{
if($tL == $HlandWaste) {
logMsNoDamageT($id, $name, $tLname, $mName, $point, $tPoint);
 } elsif(($tL == $HlandMonster) || ($tL == $Hlandhokak)){
my($kKind, $kName, $kHp) = monsterSpec($tLv);
			my($kspecial) = $HmonsterSpecial[$kKind];
if(($HmonsterSpecial[$kKind] == 14)&&(random(1000) == 0)){
logmonkamiT($id, $name, $kName, $mName, $point,$tPoint);
}elsif(($HmonsterSpecial[$kKind] == 18)&&(random(10) > 5)){
logmonkamiT($id, $name, $kName, $mName, $point,$tPoint);
}else{
			if((($kspecial == 3) && (($HislandTurn % 2) == 1)) ||
			   (($kspecial == 4) && (($HislandTurn % 2) == 0))||
			   (($kspecial == 12) && (random (100) < 50))) {
			    # �Ų���
lognodamageT($id, $name, $kName, $mName, $point,$tPoint);
}else{
if($kHp == 1){
logMsMonKillT($id, $name, $kName, $mName, $point,$tPoint);
		    $land->[$jx][$jy] = $HlandWaste;
		    $landValue->[$jx][$jy] = 1; # ������
}else{
logMsMonsterT($id, $name, $kName, $mName, $point,$tPoint);
	$landValue->[$jx][$jy]--;
}
}
}
}else{
logMsNormalT($id, $name, $tLname, $mName, $point,$tPoint);
		    $land->[$jx][$jy] = $HlandWaste;
		    $landValue->[$jx][$jy] = 1; # ������
  if($tL == $HlandOil) {
			$land->[$jx][$jy] = $HlandSea;
			$landValue->[$jx][$jy] = 0;
		    }
		} 
	    }
}

	    # ��ư
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # ��ȵ錄���֤���Ϥ�
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
}elsif($HmonsterSpecial[$mKind] == 19) {
my($sji) = random(8) + 5;
		$jx = $x + $ax[$sji];
		$jy = $y + $ay[$sji];

		# �������ϰ��⳰�����å�
		if(($jx < 0) || ($jx >= $HislandSize) ||
		   ($jy < 0) || ($jy >= $HislandSize)) {
		    # �ϰϳ�

			# �̾��
logMonUtiDameU($id, $name, "($x, $y)", $mName);
		    }else{
		my($tL) = $land->[$jx][$jy];
		my($tLv) = $landValue->[$jx][$jy];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($jx, $jy)";
         if(($tL == $HlandSea) ||   # ���ޤ��ϡ�����
           ($tL == $HlandSbase) ||   # ������Ϥޤ��ϡ�����
(($tL == $HlandLake)&& ($tLv == 0))  ||
           ($tL == $HlandMountain)){ # Φ���ưʳ�
		    # ������Ϥξ�硢���Υե�
		    if($tL == $HlandSbase) {
			$tL = $HlandSea;
		    }
		    $tLname = landName($tL, $tLv);

			# ���ƥ륹
			logMsNoDamageU($id, $name, $tLname, $mName, $point, $tPoint);
}else{
if($tL == $HlandWaste) {
logMsNoDamageU($id, $name, $tLname, $mName, $point, $tPoint);
 } elsif(($tL == $HlandMonster) || ($tL == $Hlandhokak)){
my($kKind, $kName, $kHp) = monsterSpec($tLv);
			my($kspecial) = $HmonsterSpecial[$kKind];
if(($HmonsterSpecial[$kKind] == 14)&&(random(1000) == 0)){
logmonkamiU($id, $name, $kName, $mName, $point,$tPoint);
}elsif(($HmonsterSpecial[$kKind] == 18)&&(random(10) > 5)){
logmonkamiU($id, $name, $kName, $mName, $point,$tPoint);
}else{
			if((($kspecial == 3) && (($HislandTurn % 2) == 1)) ||
			   (($kspecial == 4) && (($HislandTurn % 2) == 0))||
			   (($kspecial == 12) && (random (100) < 50))) {
			    # �Ų���
lognodamageU($id, $name, $kName, $mName, $point,$tPoint);
}else{
if($kHp == 1){
logMsMonKillU($id, $name, $kName, $mName, $point,$tPoint);
		    $land->[$jx][$jy] = $HlandWaste;
		    $landValue->[$jx][$jy] = 1; # ������
}else{
logMsMonsterU($id, $name, $kName, $mName, $point,$tPoint);
	$landValue->[$jx][$jy]--;
}
}
}
}else{
logMsNormalU($id, $name, $tLname, $mName, $point,$tPoint);
		    $land->[$jx][$jy] = $HlandWaste;
		    $landValue->[$jx][$jy] = 1; # ������
  if($tL == $HlandOil) {
			$land->[$jx][$jy] = $HlandSea;
			$landValue->[$jx][$jy] = 0;
		    }
		} 
	    }
}

	    # ��ư
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # ��ȵ錄���֤���Ϥ�
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
}elsif($HmonsterSpecial[$mKind] == 20) {
my($sji) = random(8) + 5;
		$jx = $x + $ax[$sji];
		$jy = $y + $ay[$sji];


		# �������ϰ��⳰�����å�
		if(($jx < 0) || ($jx >= $HislandSize) ||
		   ($jy < 0) || ($jy >= $HislandSize)) {
		    # �ϰϳ�

			# �̾��
logMonUtiDameV($id, $name, "($x, $y)", $mName);
		    }else{
		my($tL) = $land->[$jx][$jy];
		my($tLv) = $landValue->[$jx][$jy];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($jx, $jy)";
         if(($tL == $HlandSea) ||   # ���ޤ��ϡ�����
           ($tL == $HlandSbase) ||   # ������Ϥޤ��ϡ�����
(($tL == $HlandLake)&& ($tLv == 0))  ||
           ($tL == $HlandMountain)){ # Φ���ưʳ�
		    # ������Ϥξ�硢���Υե�
		    if($tL == $HlandSbase) {
			$tL = $HlandSea;
		    }
		    $tLname = landName($tL, $tLv);

			# ���ƥ륹
			logMsNoDamageV($id, $name, $tLname, $mName, $point, $tPoint);
}else{
if($tL == $HlandWaste) {
logMsNoDamageV($id, $name, $tLname, $mName, $point, $tPoint);
 } elsif(($tL == $HlandMonster) || ($tL == $Hlandhokak)){
my($kKind, $kName, $kHp) = monsterSpec($tLv);
			my($kspecial) = $HmonsterSpecial[$kKind];
if(($HmonsterSpecial[$kKind] == 14)&&(random(1000) == 0)){
logmonkamiV($id, $name, $kName, $mName, $point,$tPoint);
}elsif(($HmonsterSpecial[$kKind] == 18)&&(random(10) > 5)){
logmonkamiV($id, $name, $kName, $mName, $point,$tPoint);
}else{
			if((($kspecial == 3) && (($HislandTurn % 2) == 1)) ||
			   (($kspecial == 4) && (($HislandTurn % 2) == 0))||
			   (($kspecial == 12) && (random (100) < 50))) {
			    # �Ų���
lognodamageV($id, $name, $kName, $mName, $point,$tPoint);
}else{
if($kHp == 1){
logMsMonKillV($id, $name, $kName, $mName, $point,$tPoint);
		    $land->[$jx][$jy] = $HlandWaste;
		    $landValue->[$jx][$jy] = 1; # ������
}else{
logMsMonsterV($id, $name, $kName, $mName, $point,$tPoint);
	$landValue->[$jx][$jy]--;
}
}
}
}else{
logMsNormalV($id, $name, $tLname, $mName, $point,$tPoint);
		    $land->[$jx][$jy] = $HlandWaste;
		    $landValue->[$jx][$jy] = 1; # ������
  if($tL == $HlandOil) {
			$land->[$jx][$jy] = $HlandSea;
			$landValue->[$jx][$jy] = 0;
		    }
		} 
	    }
}

	    # ��ư
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # ��ȵ錄���֤���Ϥ�
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
}elsif($HmonsterSpecial[$mKind] == 18) {
if(random(10) < 5){
my($sji) = random(12) + 13;
		$jx = $x + $ax[$sji];
		$jy = $y + $ay[$sji];


		# �������ϰ��⳰�����å�
		if(($jx < 0) || ($jx >= $HislandSize) ||
		   ($jy < 0) || ($jy >= $HislandSize)) {
		    # �ϰϳ�

			# �̾��
logMonUtiDameX($id, $name, "($x, $y)", $mName);
		    }else{
		my($tL) = $land->[$jx][$jy];
		my($tLv) = $landValue->[$jx][$jy];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($jx, $jy)";
         if(($tL == $HlandSea) ||   # ���ޤ��ϡ�����
           ($tL == $HlandSbase) ||   # ������Ϥޤ��ϡ�����
(($tL == $HlandLake)&& ($tLv == 0))){ # Φ���ưʳ�
		    # ������Ϥξ�硢���Υե�
		    if($tL == $HlandSbase) {
			$tL = $HlandSea;
		    }
		    $tLname = landName($tL, $tLv);

			# ���ƥ륹
			logMsNoDamageX($id, $name, $tLname, $mName, $point, $tPoint);
}else{
logMsNormalX($id, $name, $tLname, $mName, $point,$tPoint);
		    $land->[$jx][$jy] = $HlandSea;
		    $landValue->[$jx][$jy] = 0; # ������
  if($tL == $HlandOil) {
			$land->[$jx][$jy] = $HlandSea;
			$landValue->[$jx][$jy] = 0;
		    }
	    }
}
}else{
my($suussu) = random(5) + 1;
for($i = 1; $i < $suussu; $i++) {
my($sji) = random(12) + 13;
		$jx = $x + $ax[$sji];
		$jy = $y + $ay[$sji];


		# �������ϰ��⳰�����å�
		if(($jx < 0) || ($jx >= $HislandSize) ||
		   ($jy < 0) || ($jy >= $HislandSize)) {
		    # �ϰϳ�

			# �̾��
logMonUtiDameY($id, $name, "($x, $y)", $mName);
}else{
	my($tL) = $land->[$jx][$jy];
		my($tLv) = $landValue->[$jx][$jy];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($jx, $jy)";

logdasuyo($id, $name, $mName, "($x, $y)",$tPoint,$tLname);
wideDamage($id, $name, $land, $landValue, $jx, $jy);
}
}
}
	    # ��ư
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # ��ȵ錄���֤���Ϥ�
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
}elsif($HmonsterSpecial[$mKind] == 21) {
my($sji) = random(12) + 13;
		$jx = $x + $ax[$sji];
		$jy = $y + $ay[$sji];


		# �������ϰ��⳰�����å�
		if(($jx < 0) || ($jx >= $HislandSize) ||
		   ($jy < 0) || ($jy >= $HislandSize)) {
		    # �ϰϳ�

			# �̾��
logMonUtiDameZ($id, $name, "($x, $y)", $mName);
}else{
	my($tL) = $land->[$jx][$jy];
		my($tLv) = $landValue->[$jx][$jy];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($jx, $jy)";
logdasuyoZ($id, $name, $mName, "($x, $y)",$tPoint,$tLname);
wideDamage($id, $name, $land, $landValue, $jx, $jy);
}

	    # ��ư
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # ��ȵ錄���֤���Ϥ�
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
}elsif($HmonsterSpecial[$mKind] == 17) {
for($i = 1; $i < 5; $i++) {
			    $fx = $x + $ax[$i];
			    $fy = $y + $ay[$i];
	my($tL) = $land->[$fx][$fy];
		my($tLv) = $landValue->[$fx][$fy];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($fx, $fy)";
     if(($tL == $HlandSea) ||   # ���ޤ��ϡ�����
           ($tL == $HlandSbase) ||   # ������Ϥޤ��ϡ�����
(($tL == $HlandLake)&& ($tLv == 0))  ||
           ($tL == $HlandMountain)){
}else{
	$land->[$fx][$fy] = $HlandWaste;
	$landValue->[$fx][$fy] = 2;
logsandoi($id, $name, $tLname,$mName, $point,$tPoint);
}
}
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # ��ȵ錄���֤���Ϥ�
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 2;
} elsif ($HmonsterSpecial[$mKind] == 16) {
for($i = 1; $i < 5; $i++) {
			    $fx = $x + $ax[$i];
			    $fy = $y + $ay[$i];
	my($tL) = $land->[$fx][$fy];
		my($tLv) = $landValue->[$fx][$fy];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($fx, $fy)";
     if(($tL == $HlandSea) ||   # ���ޤ��ϡ�����
           ($tL == $HlandSbase) ||   # ������Ϥޤ��ϡ�����
(($tL == $HlandLake)&& ($tLv == 0))  ||
           ($tL == $HlandMountain)){
}else{
	$land->[$fx][$fy] = $HlandWaste;
	$landValue->[$fx][$fy] = 0;
logmoerui($id, $name, $tLname,$mName, $point,$tPoint);
}
}
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # ��ȵ錄���֤���Ϥ�
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
} else {
my($value,$str);
if($HmonsterSpecial[$mKind] == 8) {
$value=random(11) * 100;
$island->{'money'} += $value;
$island->{'shuu'} += $value;
$str = "$value$HunitMoney";
logMonmon($id, $name, "($sx, $sy)", $mName, $str);
} elsif($HmonsterSpecial[$mKind] == 9) {
$value=random(11) * 100;
$island->{'money'} -= $value;
$island->{'shuu'} -= $value;
$str = "$value$HunitMoney";
logMontue($id, $name, "($sx, $sy)", $mName, $str);
}

	    # ��ư
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # ��ȵ錄���֤���Ϥ�
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
}

	    # ��ư�Ѥߥե饰
	    if($HmonsterSpecial[$mKind] == 2) {
		# ��ư�Ѥߥե饰��Ω�Ƥʤ�
	    } elsif($HmonsterSpecial[$mKind] == 14) {
my($kkk)=random(80);
if($kkk < 10){
$island->{'taifu'} ++;
logkamifuu($id, $name,$point);
}elsif($kkk < 20){
$island->{'kasai'} ++;
logkamikas($id, $name,$point);
}elsif($kkk < 30){
$island->{'tunami'} ++;
logkaminam($id, $name,$point);
}elsif($kkk < 40){
$island->{'funka'} ++;
logkamifun($id, $name,$point);
}elsif($kkk < 50){
$island->{'inseki'} ++;
logkamiins($id, $name,$point);
}elsif($kkk < 60){
$island->{'daiin'} ++;
logkamidai($id, $name,$point);
}elsif($kkk < 70){
$island->{'jisin'} ++;
logkamijis($id, $name,$point);
}elsif($kkk < 80){
$island->{'jiban'} ++;
logkamijib($id, $name,$point);
}
	    } elsif($HmonsterSpecial[$mKind] == 1) {

		$monsterMove[$sx][$sy] = $monsterMove[$x][$y] + 1;
 } elsif($HmonsterSpecial[$mKind] == 20) {
} elsif($HmonsterSpecial[$mKind] == 21) {
} elsif($HmonsterSpecial[$mKind] == 22) {
} elsif($HmonsterSpecial[$mKind] == 8) {
if(random(100) < 10) {
logMonsterBom($id, $name, $mName, $point);
wideDamage($id, $name, $land, $landValue, $sx, $sy);
$jibaku = 1;
}
$monsterMove[$sx][$sy] = 2;
} elsif($HmonsterSpecial[$mKind] == 13){
$landValue->[$sx][$sy] --;
if($landValue->[$sx][$sy] ==150){
logMonsterBom($id, $name, $mName, $point);
wideDamage($id, $name, $land, $landValue, $sx, $sy);
$jibaku = 1;
}
$monsterMove[$sx][$sy] = 2;
	    } else {
		# ���̤β���
		$monsterMove[$sx][$sy] = 2;

	    }

	    if((($l == $HlandDefence) && ($HdBaseAuto == 1)&&
($jibaku == 0)) || (($l == $HlandSefence) && ($HdBaseAuto == 1)&&
($jibaku == 0))){
		logMonsMoveDefence($id, $name, $lName, $point, $mName);
		wideDamage($id, $name, $land, $landValue, $sx, $sy);
             } elsif($l == $HlandJirai) {
                    if($lv == 0) {
                        # �����Ƨ���
           logMonsMoveMine($id, $name, $lName, $point, $mName);
if ($mHp <= 2){
                    if ($mHp== 2) {
                      logMonsMoveMineDead($id, $name, $lName, $point, $mName);
                         # ����
                        my($value) = $HmonsterValue[$mKind];
                         if($value > 0) {
                             $tIsland->{'money'} += $value;
                            logMsMonMoney($target, $mName, $value);                         }
                     } else {
                   logMonsMoveMineScatter($id, $name, $lName, $point, $mName);
                     }
                    $land->[$sx][$sy] = $HlandWaste;
                     $landValue->[$sx][$sy] = 1;

                     # �޴ط�
                     my($prize) = $island->{'prize'};
                     $prize =~ /([0-9]*),([0-9]*),(.*)/;
                     my($flags) = $1;
                     my($monsters) = $2;
                     my($turns) = $3;
                     my($v) = 2 ** $mKind;
                     $monsters |= $v;
                     $island->{'prize'} = "$flags,$monsters,$turns";
                 } else {
                     # ���ä������Ĥä�
                     logMonsMoveMineAlive($id, $name, $lName, $point, $mName);
$landValue->[$sx][$sy] -= 2;
                 }
                    } elsif($lv == 1) {
           logMonsMoveMine($id, $name, $lName, $point, $mName);
if ($mHp <= 4){
                     # ���ä��ݤ���
                    if ($mHp== 4) {
                      logMonsMoveMineDead($id, $name, $lName, $point, $mName);
                         # ����
                        my($value) = $HmonsterValue[$mKind];
                         if($value > 0) {
                             $tIsland->{'money'} += $value;
                            logMsMonMoney($target, $mName, $value);                         }
                     } else {
                    # ���ä����Ϥ�Ķ���ƥ��᡼����Ϳ�����Τǻ��Τ��᤭�����
                   logMonsMoveMineScatter($id, $name, $lName, $point, $mName);
                     }

                     # �Ϸ������(�ƺ�)�ˤ���
                    $land->[$sx][$sy] = $HlandWaste;
                     $landValue->[$sx][$sy] = 1;

                     # �޴ط�
                     my($prize) = $island->{'prize'};
                     $prize =~ /([0-9]*),([0-9]*),(.*)/;
                     my($flags) = $1;
                     my($monsters) = $2;
                     my($turns) = $3;
                     my($v) = 2 ** $mKind;
                     $monsters |= $v;
                     $island->{'prize'} = "$flags,$monsters,$turns";
                 } else {
                     # ���ä������Ĥä�
                     logMonsMoveMineAlive($id, $name, $lName, $point, $mName);
$landValue->[$sx][$sy] -= 4;
                 }
                     } elsif($lv ==2) {
                         # ��������Ƨ���
                         # ž��������������˷���
                         my($i) = int(rand($HislandNumber));
                         my($tIsland) = $Hislands[$i];
                         my($tId) = $tIsland->{'id'};
                         my($tLand) = $tIsland->{'land'};
                         my($tLandValue) = $tIsland->{'landValue'};
                         # ���ä�ž������(ž������Ϸ���̵��)
                         $tLand->[$sx][$sy]      = $land->[$sx][$sy];
                         $tLandValue->[$sx][$sy] = $landValue->[$sx][$sy];
logMonsMoveMineWarp($id, $name, $lName, $point, $mName, $tId, $tIsland->{'name'});
                         if ($id != $tId) {
                             $land->[$sx][$sy] = $HlandJirai;
                             $landValue->[$sx][$sy] = 2;
                         }
                     }

                 

	    } elsif ($l == $HlandFarm){
my($str) = $landValue->[$sx][$sy] % 10;
if ($str ==9){
logMonsFarm($id, $name,  $point, $mName);
} elsif($str == 8){
$landValue->[$sx][$sy] ++;
logMonsFarm($id, $name, $point, $mName);
} elsif($str == 7){
my($p) = random(3);
$landValue->[$sx][$sy] += $p;
logMonsFarm($id, $name, $point, $mName);
}else{
my($p) = random(4);
$landValue->[$sx][$sy] += $p;
logMonsFarm($id, $name, $point, $mName);
}
}else{
	if($HmonsterSpecial[$mKind] == 5) {

	} else {
		logMonsMove($id, $name, $lName, $point, $mName);
	    }
	}
	}
	}
	}
# ��Ĺ�����ñ�إå����ҳ�
sub doEachHex {
    my($island) = @_;
    my(@monsterMove);

    # Ƴ����
    my($name) = $island->{'name'};
    my($id) = $island->{'id'};
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};
    my($Miz) = $island->{'Jous'} * 100;
    # ������͸��Υ�����
    my($addpop)  = 0; # ¼��Į
my($addpop2) = 0;
if($island->{'pop'} > $Miz){
$addpop  += ($island->{'kukou'} * 5) - 3;
    $addpop2 -= 20 - ($island->{'kukou'} * 3);
logMizrve($id, $name);
} else{
$addpop  += ($island->{'kukou'} * 5) + 10; 
    $addpop2 += ($island->{'kukou'} * 3);
}
$island->{'slag'} += $island->{'pop'};
$island->{'slag'} -= $island->{'gomi'}*100;
if($island->{'slag'} <0){
$island->{'slag'} = 0;
}
if(($island->{'slag'} > 0) && ($island->{'goyu'} > 0)){
$island->{'money'} -= $island->{'slag'} * 10;
$island->{'shuu'} -= $island->{'slag'} * 10;
$island->{'slag'} = 0;
}
if($island->{'slag'} > $island->{'pop'}*10){
	$addpop -= 10;
	$addpop2 -= 15;
logGomi($id, $name);
}
    if($island->{'food'} < 0) {
	# ������­
	$addpop += -30;
$addpop2 += -50;
}
if($island->{'propaganda'} == 1) {
	# Ͷ�׳�ư��
	$addpop += 30;
	$addpop2 += 3;
}
my($shooo) = $island->{'sigoto'}  * 10;
my($shouo) = $island->{'pop'} * 0.6;

    if($shooo <= $shouo) {
	$addpop += -20;
$addpop2 += -40;
}
    # �롼��
    my($x, $y, $i);
    for($i = 0; $i < $HpointNumber; $i++) {
	$x = $Hrpx[$i];
	$y = $Hrpy[$i];
	my($landKind) = $land->[$x][$y];
	my($lv) = $landValue->[$x][$y];

	if($landKind == $HlandTown) {
	    # Į��
if($lv < 100) {
if($addpop < 0) {
$lv -= (random(-$addpop) + 1);
	if($lv <= 0) {
		    # ʿ�Ϥ��᤹
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}
}else{
 $lv += random($addpop) + 1;
		    if($lv > 100) {
			$lv = 100;
		    }
}
} else {
if($addpop2 < 0) {
$lv -= (random(-$addpop2) + 1);
}else{
	    # �ԻԤˤʤ����Ĺ�٤�
                     if (countStation($land, $landValue, $x, $y))
                     {
                         # ���Ϥ˱ؤ�����
                        $lv += random(3 + $addpop2) + 1;
                   }
                    elsif($addpop2 > 0) {
                          $lv += random($addpop2) + 1;
		    }
		}
}
    if($lv > 200) {
		$lv = 200;
	    }
	    $landValue->[$x][$y] = $lv;
	} elsif($landKind == $HlandPlains) {
	    # ʿ��
	    if(random(5) == 0) {
	if(random(50) < countAround($land, $x, $y, $HlandForest, 5)){
for($i = 0; $i < 5; $i++) {
			    $sx = $x + $ax[$i];
			    $sy = $y + $ay[$i];
if(($landValue->[$sx][$sy] == 200)&&($landValue->[$sx][$sy] == $HlandForest)){
 $land->[$x][$y] = $HlandForest;
		    $landValue->[$x][$y] = 1;
logForest($id, $name, $lName, "($x, $y)");
}
}
}else{
		# ��������졢Į������С�������Į�ˤʤ�
	        if(countGrow($land, $landValue, $x, $y)){
		    $land->[$x][$y] = $HlandTown;
		    $landValue->[$x][$y] = 1;
logMati($id, $name, $lName, "($x, $y)");
		}
}
	    }elsif(countsabaku($land, $landValue, $x, $y)){
if(random(20) == 0) {
my($lName) = &landName($landKind, $lv);
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 2;
logsabaku($id, $name, $lName, "($x, $y)");
}
}
	} elsif($landKind == $HlandWaste) {
	    # ʿ��
if($landValue->[$x][$y] != 2){
if(countsabaku($land, $landValue, $x, $y)){
if(random(10) == 0) {
my($lName) = &landName($landKind, $lv);
$landValue->[$x][$y] = 2;
logsabaku($id, $name, $lName, "($x, $y)");
}
} else {
if(random(500) == 0) {
my($lName) = &landName($landKind, $lv);
$landValue->[$x][$y] = 2;
logsabaku($id, $name, $lName, "($x, $y)");
	    }
}
}elsif(random(100) < countAround($land, $x, $y, $HlandForest, 5)){
for($i = 0; $i < 5; $i++) {
			    $sx = $x + $ax[$i];
			    $sy = $y + $ay[$i];
if(($landValue->[$sx][$sy] == 200)&&($landValue->[$sx][$sy] == $HlandForest)){
$landValue->[$x][$y] = 0;
}
}
}
	} elsif($landKind == $HlandForest) {
	    # ��
	    if($lv < 200) {
		# �ڤ����䤹
		$landValue->[$x][$y]++;
	    }
	} elsif($landKind == $HlandDefence) {
	    if($lv == 1) {
		# �ɱһ��߼���
		my($lName) = &landName($landKind, $lv);
		logBombFire($id, $name, $lName, "($x, $y)");

		# �����ﳲ�롼����
		wideDamage($id, $name, $land, $landValue, $x, $y);
	    }
	} elsif($landKind == $Hlandkukou) {
	    if($lv == 1) {
$island->{'money'} -= 20;
$island->{'shuu'} -= 20;
	    }else{
$island->{'money'} -= 60;
$island->{'shuu'} -= 20;
}
	} elsif($landKind == $HlandSefence) {
	    if($lv == 1) {
		# �ɱһ��߼���
		my($lName) = &landName($landKind, $lv);
		logBombFire($id, $name, $lName, "($x, $y)");

		# �����ﳲ�롼����
		wideDamage($id, $name, $land, $landValue, $x, $y);
	    }
} elsif($landKind == $Hlanddoubutu) { # ��������
# ưʪ��
if($lv == 1) {
my($value, $str, $lName);
$lName = landName($landKind, $lv);
$value = 30 - random(29);
$island->{'money'} += $value;
$island->{'shuu'} += $value;
$str = "$value$HunitMoney";
$island->{'food'} -=100;
# ������
logdoubutuMoney($id, $name, $lName, "($x, $y)", $str); 

} elsif ($lv == 2){ # ��������
# ưʪ��
my($value, $str, $lName);
$lName = landName($landKind, $lv);
$value = int(($island->{'pop'} / 20) - 5);
$island->{'money'} += $value;
$island->{'shuu'} += $value;
$str = "$value$HunitMoney";
# ������
logOmiseMoney($id, $name, $lName, "($x, $y)", $str); 
} else {
	    # ��������
	    my($value, $str, $lName);
	    $lName = landName($landKind, $lv);
	    $value = $island->{'area'}/4;
	    $island->{'money'} += $value;
$island->{'shuu'} += $value;
	    $str = "$value$HunitMoney";

	    # ������
	    logOnseMoney($id, $name, $lName, "($x, $y)", $str);
}
} elsif($landKind == $HlandHaribote) {
# ���
if($lv > 0){
my($value, $str, $lName);
$lName = landName($landKind, $lv);
$value = $lv * 50;
$island->{'money'} += $value;
$island->{'shuu'} += $value;
$str = "$value$HunitMoney";
logBankMoney($id, $name, $lName, "($x, $y)", $str);
}
} elsif($landKind == $HlandMonster) {
if($island->{'monfl'} ==1){
logkaeru($id, $name, landName($landKind, $lv),
$point);
$land->[$x][$y] = $HlandWaste;
$landValue->[$x][$y] = 0;
}
if((countAround($land, $x, $y, $HlandReho, 25)) > 0){
	if ($island->{'gun'} == 0) {
	    logNoKoku($id, $name, $comName);
	    next;
	}
my($ai, $cx, $cy, $arg);
    for($ai = 1; $ai < 25; $ai++) {
	 $cx = $x + $ax[$ai];
	 $cy = $y + $ay[$ai];

	 if(($cx < 0) || ($cx >= $HislandSize) ||
	    ($cy < 0) || ($cy >= $HislandSize)) {
	 } else {
	     if($land->[$cx][$cy] == $HlandReho) {
$arg = $landValue->[$cx][$cy]+1;
    for($si = 1; $si < $arg; $si++) {
		my($r) = random(5);
		$tx = $x + $ax[$r];
		$ty = $y + $ay[$r];

		if(($tx < 0) || ($tx >= $HislandSize) ||
		   ($ty < 0) || ($ty >= $HislandSize)) {
			logNsOut($id, $name, "($x, $y)", "($cx, $cy)");
}else{
if((($land->[$tx][$ty] == $HlandSea) && ($landValue->[$tx][$ty] == 0)) ||
($land->[$tx][$ty] == $HlandSea) ||   # ���ޤ��ϡ�����
($land->[$tx][$ty] == $HlandSbase) ||   # ������Ϥޤ��ϡ�����
($land->[$tx][$ty] == $HlandLake) ||
($land->[$tx][$ty] == $HlandMountain)){ # Φ���ưʳ�
if($land->[$tx][$ty] == $HlandSbase) {
$land->[$tx][$ty] = $HlandSea;
}
$tLname = landName($land->[$tx][$ty], $landValue->[$tx][$ty]);
logNsNoDamage($id, $name, $tLname, "($x, $y)","($cx, $cy)", "($tx, $ty)");
}elsif($land->[$tx][$ty] == $HlandWaste) {
$tLname = landName($land->[$tx][$ty], $landValue->[$tx][$ty]);
logNsWaste($id, $name, $tLname, "($x, $y)","($cx, $cy)", "($tx, $ty)");
} elsif(($land->[$tx][$ty] == $HlandMonster) || ($land->[$tx][$ty] == $Hlandhokak)){
my($mKind, $mName, $mHp) = monsterSpec($landValue->[$tx][$ty]);
			my($special) = $HmonsterSpecial[$mKind];
			if((($special == 3) && (($HislandTurn % 2) == 1)) ||
			   (($special == 4) && (($HislandTurn % 2) == 0))||
			   (($special == 12) && (random (100) < 50))) {
logNsMonNoDamage($id, $name, $mName, "($x, $y)","($cx, $cy)", "($tx, $ty)");
}elsif(($special == 14)||(($special == 18) && (random (100) < 50))){
logNsMonNoDamageKami($id, $name, $mName, "($x, $y)","($cx, $cy)", "($tx, $ty)");
}else{
if($mHp == 1){
logNsMonKill($id, $name,  $mName, "($x, $y)","($cx, $cy)", "($tx, $ty)");
		    $land->[$tx][$ty] = $HlandWaste;
		    $landValue->[$tx][$ty] = 1; # ������
} else {
logNsMonster($id, $name,  $mName, "($x, $y)","($cx, $cy)", "($tx, $ty)");
$landValue->[$tx][$ty]--;
}
}
} else {
$tLname = landName($land->[$tx][$ty], $landValue->[$tx][$ty]);
logNsNormal($id, $name, $tLname, "($x, $y)","($cx, $cy)", "($tx, $ty)");
		    $land->[$tx][$ty] = $HlandWaste;
		    $landValue->[$tx][$ty] = 1; # ������
		    if($land->[$tx][$ty] == $HlandOil) {
if($landValue->[$tx][$ty] >9){
			$land->[$tx][$ty] = $HlandSea;
			$landValue->[$tx][$ty] = 1;
} else {
			$land->[$tx][$ty] = $HlandSea;
			$landValue->[$tx][$ty] = 0;
}
}
}
}
}
}
}
}
}
	} elsif(($landKind == $HlandOil) &&($lv == 0)){
	    # ��������
	    my($value, $str, $lName);
	    $lName = landName($landKind, $lv);
	    $value = 200 + random(101);
	    $island->{'oil'} += $value;
	    $str = "$value�ȥ�";

	    # ������
	    logOilMoney($id, $name, $lName, "($x, $y)", $str);

	    # �ϳ�Ƚ��
	    if(random(1000) < $HoilRatio) {
		# �ϳ�
		logOilEnd($id, $name, $lName, "($x, $y)");
		$land->[$x][$y] = $HlandSea;
		$landValue->[$x][$y] = 0;
	    }


}
if($landKind == $HlandTown){
my($daisas) = $HdisDisa - ($island->{'hospit'} * 2);
		    my($l) = $land->[$x][$y];
		    my($lv) = $landValue->[$x][$y];
		    my($lName) = landName($l, $lv);
if(random(10000) < $daisas){
$landValue->[$x][$y] -= (random(100)+1);
logDis($id, $name, $lName,"($x, $y)");
if($landValue->[$x][$y] < 1){
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
}
}
}
if(($landKind == $HlandOil) && ($lv > 9)) {
my($marsh) = $lv * 7.5;
		    my($l) = $land->[$x][$y];
		    my($lv) = $landValue->[$x][$y];
		    my($lName) = landName($l, $lv);
if(random(1000) < 10){
$island->{'food'} -= $marsh;
logaka($id, $name, $lName,"($x, $y)");
}
}
if($landKind == $HlandSea){
if(((countAround($land, $x, $y, $HlandSea, 5)+ countAround($land, $x, $y, $HlandOil, 5)+ countAround($land, $x, $y, $HlandSbase, 5))== 1) && (countAround($land, $x, $y, $HlandLake, 5)== 0)){
$land->[$x][$y] = $HlandLake;
}
}
if($landKind == $HlandLake){
if(((countAround($land, $x, $y, $HlandSea, 5)+ countAround($land, $x, $y, $HlandOil, 5)+ countAround($land, $x, $y, $HlandSbase, 5)) != 0) || (countAround($land, $x, $y, $HlandLake, 5) > 1)) {
$land->[$x][$y] = $HlandSea;
}
}
	# �к�Ƚ��
	if((($landKind == $HlandTown) && ($lv > 30)) ||
	   ($landKind == $HlandHaribote) ||
           ($landKind == $HlandStation) ||
	   ($landKind == $HlandFactory)) {
	    if((random(1000) < $HdisFire)||
	   ($island->{'kasai'} >0)){
		# ���Ϥο��ȵ�ǰ��������
		if(((countAround($land, $x, $y, $HlandForest, 5) +
		    countAround($land, $x, $y, $HlandMonument, 5)) == 0)&&
(countAround($land, $x, $y, $HlandShou, 25) == 0)) {
		    # ̵���ä���硢�кҤǲ���
		    my($l) = $land->[$x][$y];
		    my($lv) = $landValue->[$x][$y];
		    my($point) = "($x, $y)";
		    my($lName) = landName($l, $lv);
		    logFire($id, $name, $lName, $point);
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
		}
	    }
	}
    }
}
 # �ż֤α��Է׻�
 # (����� CPU ���֤���񤹤�Ť������Ǥ�)
 sub doStation {
     my($island) = @_;
     my(@monsterMove);
     # Ƴ����
     my($name) = $island->{'name'};
     my($id) = $island->{'id'};
     my($land) = $island->{'land'};
     my($landValue) = $island->{'landValue'};
     my($x, $y, $i, $j, $n, $station);
     # ������ξ�Ҥ򥯥ꥢ
     $station = 0;
     for($i = 0; $i < $HpointNumber; $i++) {
         $x = $Hrpx[$i];
         $y = $Hrpy[$i];
         my($landKind) = $land->[$x][$y];
         my($lv) = $landValue->[$x][$y];
         if($landKind == $HlandStation)
         {
             if($lv < 100)
             {
                 # ��ϩ
                 $landValue->[$x][$y] = 0;
             }
             else
             {
                 # ��
                 $station++;
                 $landValue->[$x][$y] = 100;
             }
         }
     }
     # �ؤ����İʾ�ʤ�����ż֤ϱ��Ԥ��ʤ�
     return if ($station < 2);
     # ��ϩ���ż֤��֤�
     $n = 0;
     for($i = 0; $i < $HpointNumber; $i++) {
         $x = $Hrpx[$i];
         $y = $Hrpy[$i];
         my($landKind) = $land->[$x][$y];
         my($lv) = $landValue->[$x][$y];
         if($landKind == $HlandStation)
         {
             # �ż֤��֤�
             if($lv < 100)
             {
                 # ��ϩ
                 $n = 1;
                 goTrain($land, $landValue, $x, $y, 100 - 1);
                 last;
             }
         }
     }
     # ��ϩ���ʤ���б��Ԥ��ʤ�
     return if (!$n);
     # �ż֤����餻��
     # (����� 20 �إå�����ޤ�)
     for ($j = 0; $j < 20; $j++)
     {
         $n = 1;
         for($i = 0; $i < $HpointNumber; $i++) {
             $x = $Hrpx[$i];
             $y = $Hrpy[$i];
             my($landKind) = $land->[$x][$y];
             my($lv) = $landValue->[$x][$y];

             if($landKind == $HlandStation)
             {
                 # �ż֤��ư����
                 if(($lv > 0) && ($lv < 100))
                 {
                     # ��ϩ
                     goTrain($land, $landValue, $x, $y, $lv - 1);
                 }
                 elsif($lv == 100)
                 {
                     # �ҤΤ��ʤ��ؤ�����(��ϩ���ڤ�Ƥ����ǽ��������)
                     $n = 0;
                 }
             }
         }
     }

     # ���Ƥαؤ���ϩ����³����Ƥ��ʤ���б��Ԥ��ʤ�
     return if (!$n);
     # �ؤ����夷����ҿ���׻�����
     my($value, $str, $lName, $pop);
     $pop = int($island->{'pop'} / 100) + 1; # ��̱10���ͤ��Ȥ˼��ץ��å�
     for($i = 0; $i < $HpointNumber; $i++) {
         $x = $Hrpx[$i];
         $y = $Hrpy[$i];
         my($landKind) = $land->[$x][$y];
         my($lv) = $landValue->[$x][$y];
         if($landKind == $HlandStation)
         {
             if($lv >= 100)
             {
                 # ��
                 $value = int((200 - $landValue->[$x][$y]) / $station);
                 if ($value > 0)
                 {
                     # ���פ��夬�ä�
                     $value = $pop * $value;
                     $island->{'money'} += $value;

                     $lName = landName($landKind, $lv);
                     $str = "$value$HunitMoney";
                     logStationMoney($id, $name, $lName, "($x, $y)", $str);
                 }
             }
         }
     }
 }
 
 # �ż֤��ư����
 # (��ϩ��ξ�Ҥ�ή���׻�����)
 sub goTrain {
     my($land, $landValue, $x, $y, $unit) = @_;
     my($i, $sx, $sy);
     for($i = 1; $i < 5; $i++) {
          $sx = $x + $ax[$i];
          $sy = $y + $ay[$i];



          if(($sx < 0) || ($sx >= $HislandSize) ||
             ($sy < 0) || ($sy >= $HislandSize)) {
          } else {
              # �ϰ���ξ��
              my($lv) = $landValue->[$sx][$sy];
              if($land->[$sx][$sy] == $HlandStation)
              {
                  if($lv < 100)
                  {
                      # ��ϩ
                      if (!($lv || ($lv > $unit)))
                      {
                         # �٤���ϩ���ż֤��ư����
                          $landValue->[$sx][$sy] = $unit;
                     }
                  }
                  else
                  {
                      # ��
                      if (($lv == 100) || ($lv > $unit + 100))
                      {
                          # �ؤ��ż֤��ư����
                          $landValue->[$sx][$sy] = $unit + 100;
                      }
                  }
              }
          }
      }
 }
 # (�ؤ�ޤ�)
# ���Ϥ�Į�����줬���뤫Ƚ��
sub countGrow {
    my($land, $landValue, $x, $y) = @_;
    my($i, $sx, $sy);
    for($i = 1; $i < 5; $i++) {
	 $sx = $x + $ax[$i];
	 $sy = $y + $ay[$i];



	 if(($sx < 0) || ($sx >= $HislandSize) ||
	    ($sy < 0) || ($sy >= $HislandSize)) {
	 } else {
	     # �ϰ���ξ��
	     if(($land->[$sx][$sy] == $HlandTown) ||
              (($land->[$sx][$sy] == $HlandStation) && ($landValue->[$sx][$sy] >= 100)) ||
		($land->[$sx][$sy] == $HlandFarm)) {
		 if($landValue->[$sx][$sy] != 1) {
		     return 1;
		 }
	     }
	 }
    }
    return 0;
}
sub countsabaku {
    my($land, $landValue, $x, $y) = @_;
    my($i, $sx, $sy);
    for($i = 1; $i < 5; $i++) {
	 $sx = $x + $ax[$i];
	 $sy = $y + $ay[$i];



	 if(($sx < 0) || ($sx >= $HislandSize) ||
	    ($sy < 0) || ($sy >= $HislandSize)) {
	 } else {
	     # �ϰ���ξ��
	     if($land->[$sx][$sy] == $HlandWaste) {
		 if($landValue->[$sx][$sy] == 2) {
		     return 1;
		 }
	     }
	 }
    }
    return 0;
}
 # ���Ϥ˱ؤ����뤫Ƚ��
 sub countStation {
     my($land, $landValue, $x, $y) = @_;
     my($i, $sx, $sy);
     for($i = 1; $i < 5; $i++) {
          $sx = $x + $ax[$i];
          $sy = $y + $ay[$i];

          if(($sx < 0) || ($sx >= $HislandSize) ||
             ($sy < 0) || ($sy >= $HislandSize)) {
          } else {
              # �ϰ���ξ��
              if(($land->[$sx][$sy] == $HlandStation) && ($landValue->[$sx][$sy] >= 100))
              {
                # �ؤǤ���
                  return 1;
              }
          }
     }
     return 0;
 }

# ������
sub doIslandProcess {
    my($number, $island) = @_;

    # Ƴ����
    my($name) = $island->{'name'};
    my($id) = $island->{'id'};
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};

    # �Ͽ�Ƚ��
    if((random(1000) < (($island->{'prepare2'} + 1) * $HdisEarthquake)||($island->{'jisin'} >0))) {
	# �Ͽ�ȯ��
	logEarthquake($id, $name);

	my($x, $y, $landKind, $lv, $i,$j);
	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];

	    if((($landKind == $HlandTown) && ($lv >= 100)) ||
	       ($landKind == $HlandHaribote) ||
($landKind == $HlandBouh) ||
($landKind == $HlandStation) ||
	       ($landKind == $HlandFactory)) {
		# 1/4�ǲ���
		if(random(4) == 0) {
if($landKind == $HlandBouh){
logBODamage($id, $name, landName($landKind, $lv),
				"($x, $y)");
}else{
		    logEQDamage($id, $name, landName($landKind, $lv),
				"($x, $y)");
}
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
		}
	    }
if(($landKind == $HlandMountain) && (random(100)<10)){
# �ں�����ȯ��
logEQfall($id, $name, landName($landKind, $lv),"($x, $y)");
for($j = 1; $j < 5; $j++) {
$sx = $x + $ax[$j];
$sy = $y + $ay[$j];

$landKind = $land->[$sx][$sy];
$lv = $landValue->[$sx][$sy];
$point = "($sx, $sy)";

if(($sx < 0) || ($sx >= $HislandSize) ||
($sy < 0) || ($sy >= $HislandSize)) {
} else {
# �ϰ���ξ��
$landKind = $land->[$sx][$sy];
$lv = $landValue->[$sx][$sy];
$point = "($sx, $sy)";
if(($landKind == $HlandSea) ||
($landKind == $HlandOil) ||
($landKind == $HlandSbase) ||
($landKind == $HlandLake) ||
($landKind == $HlandMountain) ||
($landKind == $HlandMonster) ||
($landKind == $HlandWaste)) {
# ���̤ʤ��Ϸ�
next;
} else {
# ����ʳ��ξ��
logEQfalldamage($id, $name, landName($landKind, $lv),$point);
$land->[$sx][$sy] = $HlandWaste;
$landValue->[$sx][$sy] = 0;
}# �Ϸ�
}# �ϰ�
}# �����֤�(����1�إå���)
}# ��

	}
    }
my($shoko) = $island->{'sigoto'}  * 10;
my($shopo) = $island->{'pop'} * 0.6;
    if($shoko <= $shopo) {
	# ��­��å�����
	logShorve($id, $name);
	my($x, $y, $landKind, $lv, $i);
	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];

	    if((($landKind == $Hlanddoubutu)&&($lv != 2)) ||
(($landKind == $HlandHaribote)&&($lv != 0))||
	       ($landKind == $HlandBase) ||
($landKind == $HlandSefence) ||
	       ($landKind == $HlandDefence)) {
my($KUYI);
$KUYI = 25;
if($island->{'Pori'} > 0){
$KUYI = 15;
}
		# 1/4�ǲ���
		if(random(100) < $KUYI){
if(!(countAround($land, $x, $y, $HlandPori, 25))){
		    logSyDamage($id, $name, landName($landKind, $lv),
				"($x, $y)");
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
}
		}
	    }
	}
    }
    # ������­
    if($island->{'food'} <= 0) {
	# ��­��å�����
	logStarve($id, $name);
	$island->{'food'} = 0;

	my($x, $y, $landKind, $lv, $i);
	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];

	    if(($landKind == $HlandFarm) ||
	       ($landKind == $HlandFactory) ||
	       ($landKind == $HlandBase) ||
($landKind == $HlandSefence) ||
	       ($landKind == $HlandDefence)) {
		# 1/4�ǲ���
$KUYI = 25;
if($island->{'Pori'} > 0){
$KUYI = 10;
}
		if(random(100) < $KUYI){
		    logSvDamage($id, $name, landName($landKind, $lv),
				"($x, $y)");
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
		}
	    }
	}
    }
# �籫Ƚ��
if((random(1000) < $HdisHardRain)||($island->{'ooame'} >0)) {
logHardRain($id, $name);
my($x, $y, $i, $landKind);
my($flag) = 0;
for($i = 0; $i < $HpointNumber; $i++) {
$x = $Hrpx[$i];
$y = $Hrpy[$i];
$landKind = $land->[$x][$y];
$lv = $landValue->[$x][$y];
if(($landKind == $HlandForest) &&
 ($landValue->[$x][$y] < 200)){
$landValue->[$x][$y] +=5;
$flag = 1;
}
if(random(100)<10){
if($landKind == $HlandWaste){
my($lName) = &landName($landKind, $lv);
if($landValue->[$x][$y] != 2){
$land->[$x][$y]= $HlandPlains;
logsougen($id, $name, $lName, "($x, $y)");
}else{
logareti($id, $name, $lName, "($x, $y)");
$landValue->[$x][$y] = 2;
}
}
}
}
if($flag == 1){
logtree($id, $name);
}
}
    # ����Ƚ��
    if((random(1000) < $HdisTsunami)||($island->{'tunami'} >0)) {
	# ����ȯ��
	logTsunami($id, $name);

	my($x, $y, $landKind, $lv, $i);
	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];

	    if(!(($landKind == $HlandOil) ||
	       ($landKind == $HlandSbase) ||
	       ($landKind == $HlandLake) ||
	       ($landKind == $HlandWaste) ||
	       ($landKind == $HlandPlains) ||
	       ($landKind == $HlandMountain) ||
	       ($landKind == $HlandMonster) ||
	       ($landKind == $HlandMonument) ||
	       ($landKind == $HlandSea))) {
		# 1d12 <= (���Ϥγ� - 1) ������
		if(random(12) <
		   (countAround($land, $x, $y, $HlandOil, 5) +
		    countAround($land, $x, $y, $HlandSbase, 5) +
		    countAround($land, $x, $y, $HlandSea, 5) - 1)) {
if($landKind != $HlandBouh){
		    logTsunamiDamage($id, $name, landName($landKind, $lv),
				     "($x, $y)");
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
}
		}
	    }

	}
    }

    # ����Ƚ��
    my($r) = random(10000);
    my($pop) = $island->{'pop'};
    my($f) = random(100);
if($island->{'Onpa'} >0){
    my($a) = ($island->{'Onpa'} * 4) + 10;
}else{
my($a) = 0;
}
    do{
	if((($r < ($HdisMonster * $island->{'area'} / 4)) &&($f > $a)&&($pop >= $HdisMonsBorder1)) ||
	   ($island->{'monstersend'} > 0) || ($island->{'monstersend2'} > 0)|| ($island->{'monstersend3'} > 0)|| ($island->{'monstersend4'} > 0)|| ($island->{'monstersend5'} > 0)) {
	    # ���ýи�
	    # ��������
	    my($lv, $kind);
	    if($island->{'monstersend'} > 0) {
		# ��¤
		$kind = 0;
		$island->{'monstersend'}--;
 } elsif ($island->{'monstersend2'} > 0) {
		# ��¤
		$kind = 22;
		$island->{'monstersend2'}--;
 } elsif ($island->{'monstersend3'} > 0) {
		# ��¤
		$kind = 23;
		$island->{'monstersend3'}--;
 } elsif ($island->{'monstersend4'} > 0) {
		# ��¤
		$kind = 24;
		$island->{'monstersend4'}--;
 } elsif ($island->{'monstersend5'} > 0) {
		# ��¤
		$kind = 25;
		$island->{'monstersend5'}--;
	    } elsif($pop >= $HdisMonsBorder9) {
		# level3�ޤ�
		$kind = random($HmonsterLevel9) + 1;
	    } elsif($pop >= $HdisMonsBorder8) {
		# level3�ޤ�
		$kind = random($HmonsterLevel8) + 1;
	    } elsif($pop >= $HdisMonsBorder7) {
		# level3�ޤ�
		$kind = random($HmonsterLevel7) + 1;
	    } elsif($pop >= $HdisMonsBorder6) {
		# level2�ޤ�
		$kind = random($HmonsterLevel6) + 1;
	    } elsif($pop >= $HdisMonsBorder5) {
		# level3�ޤ�
		$kind = random($HmonsterLevel5) + 1;
	    } elsif($pop >= $HdisMonsBorder4) {
		# level2�ޤ�
		$kind = random($HmonsterLevel4) + 1;
	    } elsif($pop >= $HdisMonsBorder3) {
		# level3�ޤ�
		$kind = random($HmonsterLevel3) + 1;
	    } elsif($pop >= $HdisMonsBorder2) {
		# level2�ޤ�
		$kind = random($HmonsterLevel2) + 1;
	    } else {
		# level1�Τ�
		$kind = random($HmonsterLevel1) + 1;
	    }

	    # lv���ͤ����
	    $lv = $kind * 10
		+ $HmonsterBHP[$kind] + random($HmonsterDHP[$kind]);

	    # �ɤ��˸���뤫����
	    my($bx, $by, $i);
	    for($i = 0; $i < $HpointNumber; $i++) {
		$bx = $Hrpx[$i];
		$by = $Hrpy[$i];
		if($land->[$bx][$by] == $HlandTown) {

		    # �Ϸ�̾
		    my($lName) = landName($HlandTown, $landValue->[$bx][$by]);

		    # ���Υإå�������ä�
		    $land->[$bx][$by] = $HlandMonster;
		    $landValue->[$bx][$by] = $lv;

		    # ���þ���
		    my($mKind, $mName, $mHp) = monsterSpec($lv);

		    # ��å�����
		    logMonsCome($id, $name, $mName, "($bx, $by)", $lName);
		    last;
		}
	    }
	}
    } while($island->{'monstersend'} > 0);

    # ��������Ƚ��
    if((($island->{'area'} > $HdisFallBorder) &&
       (random(1000) < $HdisFalldown)) ||($island->{'jiban'} >0)){
	# ��������ȯ��
	logFalldown($id, $name);

	my($x, $y, $landKind, $lv, $i);
	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];

	    if(($landKind != $HlandSea) &&
	       ($landKind != $HlandSbase) &&
	       ($landKind != $HlandOil) &&
	       ($landKind != $HlandMountain)) {

		# ���Ϥ˳�������С��ͤ�-1��
		if(countAround($land, $x, $y, $HlandSea, 5) + 
		   countAround($land, $x, $y, $HlandSbase, 5)) {
		    logFalldownLand($id, $name, landName($landKind, $lv),
				"($x, $y)");
		    $land->[$x][$y] = -1;
		    $landValue->[$x][$y] = 0;
		}
	    }
	}

	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];

	    if($landKind == -1) {
		# -1�ˤʤäƤ�����������
		$land->[$x][$y] = $HlandSea;
		$landValue->[$x][$y] = 1;
	    } elsif ($landKind == $HlandSea) {
		# �����ϳ���
		$landValue->[$x][$y] = 0;
	    }

	}
    }

    # ����Ƚ��
    if((random(1000) < $HdisTyphoon)||($island->{'taifu'} >0)) {
	# ����ȯ��
	logTyphoon($id, $name);

	my($x, $y, $landKind, $lv, $i);
	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];

	    if(($landKind == $HlandFarm) ||
	       ($landKind == $HlandHaribote)) {

		# 1d12 <= (6 - ���Ϥο�) ������
		if(random(12) < 
		   (4
		    - countAround($land, $x, $y, $HlandForest, 5)
		    - countAround($land, $x, $y, $HlandMonument, 5))) {
		    logTyphoonDamage($id, $name, landName($landKind, $lv),
				     "($x, $y)");
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		}
	    }
if(($landKind == $HlandOil)&&($lv>0)){
if(random(100) <10){
$land->[$x][$y] = $HlandSea;
$landValue->[$x][$y] = 1;
logTyphoonDamage($id, $name, landName($landKind, $lv),"($x, $y)");
}
}
	}
    }

    # �������Ƚ��
    if((random(1000) < $HdisHugeMeteo)||($island->{'daiin'} >0)) {
	my($x, $y, $landKind, $lv, $point);

	# �
	$x = random($HislandSize);
	$y = random($HislandSize);
	$landKind = $land->[$x][$y];
	$lv = $landValue->[$x][$y];
	$point = "($x, $y)";

	# ��å�����
	logHugeMeteo($id, $name, $point);

	# �����ﳲ�롼����
	wideDamage($id, $name, $land, $landValue, $x, $y);
    }

    # ����ߥ�����Ƚ��
    while($island->{'bigmissile'} > 0) {
	$island->{'bigmissile'} --;

	my($x, $y, $landKind, $lv, $point);

	# �
	$x = random($HislandSize);
	$y = random($HislandSize);
	$landKind = $land->[$x][$y];
	$lv = $landValue->[$x][$y];
	$point = "($x, $y)";

	# ��å�����
	logMonDamage($id, $name, $point);

	# �����ﳲ�롼����
	wideDamage($id, $name, $land, $landValue, $x, $y);
    }

    # ���Ƚ��
    if((random(1000) < $HdisMeteo)||($island->{'inseki'} >0)) {
	my($x, $y, $landKind, $lv, $point, $first);
	$first = 1;
	while(random(2) == 0) {
	    $first = 0;
	    
	    # �
	    $x = random($HislandSize);
	    $y = random($HislandSize);
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];
	    $point = "($x, $y)";

	    if(($landKind == $HlandSea) && ($lv == 0)){
		# ���ݥ���
		logMeteoSea($id, $name, landName($landKind, $lv),
			    $point);
 } elsif($landKind == $HlandLake){
logMeteoSea($id, $name, landName($landKind, $lv),
			    $point);
next;
	    } elsif($landKind == $HlandMountain) {
		# ���˲�
		logMeteoMountain($id, $name, landName($landKind, $lv),
				 $point);
		$land->[$x][$y] = $HlandWaste;
		$landValue->[$x][$y] = 0;
		next;
	    } elsif($landKind == $HlandSbase) {
		logMeteoSbase($id, $name, landName($landKind, $lv),
			      $point);
	    } elsif($landKind == $HlandMonster) {
		logMeteoMonster($id, $name, landName($landKind, $lv),
				$point);
	    } elsif($landKind == $HlandSea) {
		# ����
		logMeteoSea1($id, $name, landName($landKind, $lv),
			     $point);
	    } else {
		logMeteoNormal($id, $name, landName($landKind, $lv),
			       $point);
	    }
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 0;
	}
    }

    # ʮ��Ƚ��
    if((random(1000) < $HdisEruption)||($island->{'funka'} >0)) {
	my($x, $y, $sx, $sy, $i, $landKind, $lv, $point);
	$x = random($HislandSize);
	$y = random($HislandSize);
	$landKind = $land->[$x][$y];
	$lv = $landValue->[$x][$y];
	$point = "($x, $y)";
	logEruption($id, $name, landName($landKind, $lv),
		    $point);
	$land->[$x][$y] = $HlandMountain;
	$landValue->[$x][$y] = 0;

	for($i = 1; $i < 5; $i++) {
	    $sx = $x + $ax[$i];
	    $sy = $y + $ay[$i];



	    $landKind = $land->[$sx][$sy];
	    $lv = $landValue->[$sx][$sy];
	    $point = "($sx, $sy)";

	    if(($sx < 0) || ($sx >= $HislandSize) ||
	       ($sy < 0) || ($sy >= $HislandSize)) {
	    } else {
		# �ϰ���ξ��
		$landKind = $land->[$sx][$sy];
		$lv = $landValue->[$sx][$sy];
		$point = "($sx, $sy)";
		if(($landKind == $HlandSea) ||
		   ($landKind == $HlandOil) ||
		   ($landKind == $HlandSbase)) {
		    # ���ξ��
		    if($lv == 1) {
			# ����
			logEruptionSea1($id, $name, landName($landKind, $lv),
					$point);
		    } else {
			logEruptionSea($id, $name, landName($landKind, $lv),
				       $point);
			$land->[$sx][$sy] = $HlandSea;
			$landValue->[$sx][$sy] = 1;
			next;
		    }
		} elsif(($landKind == $HlandMountain) ||
			($landKind == $HlandMonster) ||
			($landKind == $HlandWaste)) {
		    next;
		} else {
		    # ����ʳ��ξ��
		    logEruptionNormal($id, $name, landName($landKind, $lv),
				      $point);
		}
		$land->[$sx][$sy] = $HlandWaste;
		$landValue->[$sx][$sy] = 0;
	    }
	}
    }
if($island->{'sen'} > 1) {
$island->{'money'} -= 10;
$island->{'shuu'} -= 10;
}
if($island->{'hei'} == 1) {
$island->{'money'} -= 10;
$island->{'shuu'} -= 10;
}
if($island->{'ino'} == 1) {
$island->{'money'} -= 10;
$island->{'shuu'} -= 10;
}
if($island->{'kouei'} > 0) {
if(random(100000) < 10){
$island->{'kouei'} = 0;
logkouoti($id, $name);
}
}
if($island->{'bouei'} > 0) {
if(random(100000) < 10){
$island->{'bouei'} = 0;
logbouoti($id, $name);
}
}
if($island->{'kanei'} > 0) {
if(random(100000) < 10){
$island->{'kanei'} = 0;
logkanoti($id, $name);
}
}
if($island->{'hatei'} > 0) {
if(random(100000) < 10){
$island->{'hatei'} = 0;
loghatoti($id, $name);
}
}
if($island->{'reiei'} > 0) {
if(random(100000) < 10){
$island->{'reiei'} = 0;
logreioti($id, $name);
}
}
if($island->{'pmsei'} > 0) {
if(random(100000) < 10){
$island->{'pmsei'} = 0;
logpmsoti($id, $name);
}
}
if(($island->{'reiei'} > 10)&& ($island->{'reiei'} < 100)){
$island->{'reiei'} -= 10;
if($island->{'reiei'} < 11) {
logsiyou($id, $name);
}
}
if(($island->{'pmsei'} > 10)&& ($island->{'pmsei'} < 100)){
$island->{'pmsei'} -= 10;
if($island->{'pmsei'} < 11) {
logsiyouZ($id, $name);
}
}
if(($island->{'shafl'} == 0) && ($island->{'shaka'} != 0)){
$island->{'shaka'} -= 1;
$island->{'money'} -= $island->{'shamo'};
$island->{'shuu'} -= $island->{'shamo'};
$str = $island->{'shamo'};
logshamo($id, $name, $str);
}

    # ���������դ�Ƥ��鴹��
    if($island->{'food'} > 999999999) {
	$island->{'money'} += int(($island->{'food'} - 999999999) / 10);
$island->{'shuu'} += int(($island->{'food'} - 999999999) / 10);
	$island->{'food'} = 999999999;
    } 

    # �⤬���դ�Ƥ����ڤ�Τ�
    if($island->{'money'} > 999999999) {
	$island->{'money'} = 999999999;
    } 

    # �Ƽ���ͤ�׻�
    estimate($number);

    # �˱ɡ������
    $pop = $island->{'pop'};
    my($damage) = $island->{'oldPop'} - $pop;
    my($prize) = $island->{'prize'};
    $prize =~ /([0-9]*),([0-9]*),(.*)/;
    my($flags) = $1;
    my($monsters) = $2;
    my($turns) = $3;

    # �˱ɾ�
    if((!($flags & 1)) &&  $pop >= 3000){
	$flags |= 1;
	logPrize($id, $name, $Hprize[1]);
$island->{'money'} += 300;
$island->{'shuu'} += 300;
logPzMoney($id, $name, 300); 
    } elsif((!($flags & 2)) &&  $pop >= 5000){
	$flags |= 2;
	logPrize($id, $name, $Hprize[2]);
$island->{'money'} += 500;
$island->{'shuu'} += 500;
logPzMoney($id, $name, 500); 
    } elsif((!($flags & 4)) &&  $pop >= 10000){
	$flags |= 4;
	logPrize($id, $name, $Hprize[3]);
$island->{'money'} += 1000;
$island->{'shuu'} += 1000;
logPzMoney($id, $name, 1000);
   } elsif((!($flags & 512)) &&  $pop >= 20000){
	$flags |= 512;
	logPrize($id, $name, $Hprize[10]);
$island->{'money'} += 10000;
$island->{'shuu'} += 10000;
logPzMoney($id, $name, 10000);
    }

    # �����
    if((!($flags & 64)) &&  $damage >= 500){
	$flags |= 64;
	logPrize($id, $name, $Hprize[7]);
$island->{'money'} += 300;
$island->{'shuu'} += 300;
logPzMoney($id, $name, 300); 
    } elsif((!($flags & 128)) &&  $damage >= 1000){
	$flags |= 128;
	logPrize($id, $name, $Hprize[8]);
$island->{'money'} += 500;
$island->{'shuu'} += 500;
logPzMoney($id, $name, 500); 
    } elsif((!($flags & 256)) &&  $damage >= 2000){
	$flags |= 256;
	logPrize($id, $name, $Hprize[9]);
$island->{'money'} += 1000;
$island->{'shuu'} += 1000;
logPzMoney($id, $name, 1000);
  } elsif((!($flags & 2048)) &&  $damage >= 5000){
	$flags |= 2048;
	logPrize($id, $name, $Hprize[12]);
$island->{'money'} += 10000;
$island->{'shuu'} += 10000;
logPzMoney($id, $name, 10000); 
    }

    $island->{'prize'} = "$flags,$monsters,$turns";
}

# �͸���˥�����
sub islandSort {
    my($flag, $i, $tmp);

    # �͸���Ʊ���Ȥ���ľ���Υ�����ν��֤Τޤ�
    my @idx = (0..$#Hislands);
    @idx = sort { $Hislands[$b]->{'pop'} <=> $Hislands[$a]->{'pop'} || $a <=> $b } @idx;
    @Hislands = @Hislands[@idx];
}

# �����ﳲ�롼����
sub wideDamage {
    my($id, $name, $land, $landValue, $x, $y) = @_;
    my($sx, $sy, $i, $landKind, $landName, $lv, $point);

    for($i = 0; $i < 13; $i++) {
	$sx = $x + $ax[$i];
	$sy = $y + $ay[$i];


    
	$landKind = $land->[$sx][$sy];
	$lv = $landValue->[$sx][$sy];
	$landName = landName($landKind, $lv);
	$point = "($sx, $sy)";

	# �ϰϳ�Ƚ��
	if(($sx < 0) || ($sx >= $HislandSize) ||
	   ($sy < 0) || ($sy >= $HislandSize)) {
	    next;
	}

	# �ϰϤˤ��ʬ��
	if($i < 7) {
	    # �濴�������1�إå���
	    if($landKind == $HlandSea) {
		$landValue->[$sx][$sy] = 0;
		next;
	    } elsif(($landKind == $HlandSbase) ||
		    ($landKind == $HlandOil)) {
		logWideDamageSea2($id, $name, $landName, $point);
		$land->[$sx][$sy] = $HlandSea;
		$landValue->[$sx][$sy] = 0;
	    } else {
		if($landKind == $HlandMonster) {
		    logWideDamageMonsterSea($id, $name, $landName, $point);
		} else {
		    logWideDamageSea($id, $name, $landName, $point);
		}
		$land->[$sx][$sy] = $HlandSea;
		if($i == 0) {
		    # ��
		    $landValue->[$sx][$sy] = 0;
		} else {
		    # ����
		    $landValue->[$sx][$sy] = 1;
		}
	    }
	} else {
	    # 2�إå���
	    if(($landKind == $HlandSea) ||
	       ($landKind == $HlandOil) ||
	       ($landKind == $HlandWaste) ||
	       ($landKind == $HlandMountain) ||
	       ($landKind == $HlandSbase)) {
		next;
	    } elsif($landKind == $HlandMonster) {
		logWideDamageMonster($id, $name, $landName, $point);
		$land->[$sx][$sy] = $HlandWaste;
		$landValue->[$sx][$sy] = 0;
	    } else {
		logWideDamageWaste($id, $name, $landName, $point);
		$land->[$sx][$sy] = $HlandWaste;
		$landValue->[$sx][$sy] = 0;
	    }
	}
    }
}
sub wideDamageNeutron {
    my($id, $target, $name, $land, $landValue, $x, $y) = @_;
    my($sx, $sy, $i, $landKind, $landName, $lv, $point);

    for($i = 0; $i < 25; $i++) {
	$sx = $x + $ax[$i];
	$sy = $y + $ay[$i];


    
	$landKind = $land->[$sx][$sy];
	$lv = $landValue->[$sx][$sy];
	$landName = landName($landKind, $lv);
	$point = "($sx, $sy)";

	# �ϰϳ�Ƚ��
	if(($sx < 0) || ($sx >= $HislandSize) ||
	   ($sy < 0) || ($sy >= $HislandSize)) {
	    next;
	}

	# �ϰϤˤ��ʬ��
	    # �濴�������1�إå���
if(($landKind == $HlandTown)||
($landKind == $HlandOil)||
($landKind == $HlandForest)||
($landKind ==$HlandFarm)||
($landKind == $HlandMonster)||
($landKind == $Hlandhokak)||
($landKind == $HlandBoku)){
if($i < 19) {
if($landKind == $HlandTown){
logWideDamageDead($id, $target, $name, $landName, $point);
$landValue->[$sx][$sy] = 0;
$land->[$sx][$sy] = $HlandWaste;
}elsif($landKind == $HlandOil) {
if($landValue->[$sx][$sy] !=0){
logWideDamageSeaDead($id, $target, $name, $landName, $point);
$land->[$sx][$sy] = $HlandSea;
$landValue->[$sx][$sy] = 1;
}
} elsif(($landKind == $HlandMonster) ||($landKind == $Hlandhokak)){
logWideDamageMonsterDead($id, $target, $name, $landName, $point);
$land->[$sx][$sy] = $HlandWaste;
$landValue->[$sx][$sy] = 0;
} else {
logWideDamageSeaDead($id, $target, $name, $landName, $point);
$land->[$sx][$sy] = $HlandWaste;
$landValue->[$sx][$sy] = 0;
}
} else {
if($landKind == $HlandTown){
if($landValue->[$sx][$sy] == 1){
logWideDamageDead($id, $target, $name, $landName, $point);
$landValue->[$sx][$sy] = 0;
$land->[$sx][$sy] = $HlandWaste;
}else{
logWideDamageSeaDead2($id, $target, $name, $landName, $point);
$landValue->[$sx][$sy] = $landValue->[$sx][$sy] / 2;
}
}elsif($landKind == $HlandOil) {
if($landValue->[$sx][$sy] !=0){
logWideDamageSeaDead2($id, $target, $name, $landName, $point);
$landValue->[$sx][$sy] = $landValue->[$sx][$sy] / 2;
}
} elsif(($landKind == $HlandMonster) ||($landKind == $Hlandhokak)){
my($mKind, $mName, $mHp) = monsterSpec($landValue->[$sx][$sy]);
if($mHp <=2){
logWideDamageMonsterDead($id, $target, $name, $landName, $point);
$land->[$sx][$sy] = $HlandWaste;
$landValue->[$sx][$sy] = 0;
}else{
$landValue->[$sx][$sy] -= int($mHp / 2);
logWideDamageMonsterDead2($id, $target, $name, $landName, $point);
}
} else {
logWideDamageSeaDead2($id, $target, $name, $landName, $point);
$landValue->[$sx][$sy] = $landValue->[$sx][$sy] / 2;
}
	}
}
    }
}

# ���ؤν���
# ��1����:��å�����
# ��2����:������
# ��3����:���
# �̾��
sub logOut {
    push(@HlogPool,"0,$HislandTurn,$_[1],$_[2],$_[0]");
}

# �ٱ��
sub logLate {
    push(@HlateLogPool,"0,$HislandTurn,$_[1],$_[2],$_[0]");
}

# ��̩��
sub logSecret {
    push(@HsecretLogPool,"1,$HislandTurn,$_[1],$_[2],$_[0]");
}

# ��Ͽ��
sub logHistory {
    open(HOUT, ">>${HdirName}/hakojima.his");
    print HOUT "$HislandTurn,$_[0]\n";
    close(HOUT);
}

# ��Ͽ��Ĵ��
sub logHistoryTrim {
    open(HIN, "${HdirName}/hakojima.his");
    my(@line, $l, $count);
    $count = 0;
    while($l = <HIN>) {
	chomp($l);
	push(@line, $l);
	$count++;
    }
    close(HIN);

    if($count > $HhistoryMax) {
	open(HOUT, ">${HdirName}/hakojima.his");
	my($i);
	for($i = ($count - $HhistoryMax); $i < $count; $i++) {
	    print HOUT "$line[$i]\n";
	}
	close(HOUT);
    }
}

# ���񤭽Ф�
sub logFlush {
    open(LOUT, ">${HdirName}/hakojima.log0");

    # �����ս�ˤ��ƽ񤭽Ф�
    my($i);
    for($i = $#HsecretLogPool; $i >= 0; $i--) {
	print LOUT $HsecretLogPool[$i];
	print LOUT "\n";
    }
    for($i = $#HlateLogPool; $i >= 0; $i--) {
	print LOUT $HlateLogPool[$i];
	print LOUT "\n";
    }
    for($i = $#HlogPool; $i >= 0; $i--) {
	print LOUT $HlogPool[$i];
	print LOUT "\n";
    }
    close(LOUT);
}

#----------------------------------------------------------------------
# ���ƥ�ץ졼��
#----------------------------------------------------------------------
# ���­��ʤ�
sub logNoMoney {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ������­�Τ�����ߤ���ޤ�����",$id);
}
sub lognooil {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}����������­���Ƥ��ޤ���",$id);
}
# ����­��ʤ�
sub logNoFood {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ����߿�����­�Τ�����ߤ���ޤ�����",$id);
}
sub lognasimina {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ������뤤�ϻ��Ѳ�ǽ�ʹ����ʤ�������ߤ���ޤ�����",$id);
}
sub logGomi {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ϥ��ߤ�Į������Ƥ���Τǿ͡�������äƤ��äƤ��ޤ���",$id);
}
# �о��Ϸ��μ���ˤ�뼺��
sub logLandFail {
    my($id, $name, $comName, $kind, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�ͽ���Ϥ�${HtagName_}$point${H_tagName}��<B>$kind</B>���ä�������ߤ���ޤ�����",$id);
END
}
sub logNoKoku {
my($id, $name, $comName) = @_;
logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�������������ʤ�������ߤ���ޤ�����",$id);
}
# �����Φ���ʤ������Ω�Ƽ���
sub logNoLandAround {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�ͽ���Ϥ�${HtagName_}$point${H_tagName}�μ��դ�Φ�Ϥ��ʤ��ä�������ߤ���ޤ�����",$id);
END
}
sub logNoMounAround {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�ͽ���Ϥ�${HtagName_}$point${H_tagName}�μ��դ˻����ʤ��ä�������ߤ���ޤ�����",$id);
END
}
sub logNoSeaAround {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�ͽ���Ϥ�${HtagName_}$point${H_tagName}�μ��դ˳����ʤ��ä�������ߤ���ޤ�����",$id);
END
}
# ���Ϸ�����
sub logLandSuc {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
END
}
 # ��
 sub logStationSuc {
     my($id, $name, $comName, $point) = @_;
     logOut("${HtagName_}${name}��$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
END
}
 # ��ϩ
 sub logRailSuc {
     my($id, $name, $comName, $point) = @_;
     logOut("${HtagName_}${name}��$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
 END
 }
# ����ȯ��
sub logOilFound {
    my($id, $name, $point, $comName, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$str</B>��ͽ����Ĥ������${HtagComName_}${comName}${H_tagComName}���Ԥ�졢<B>���Ĥ��������Ƥ��ޤ���</B>��",$id);
END
}
sub logOnseFound {
    my($id, $name, $point, $comName, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$str</B>��ͽ����Ĥ������${HtagComName_}${comName}${H_tagComName}���Ԥ�졢<B>�������������Ƥ��ޤ���</B>��",$id);
END
}
# ����ȯ���ʤ餺
sub logOilFail {
    my($id, $name, $point, $comName, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$str</B>��ͽ����Ĥ������${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ����������Ĥϸ��Ĥ���ޤ���Ǥ�����",$id);
END
}

sub logOnseFail {
    my($id, $name, $point, $comName, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$str</B>��ͽ����Ĥ������${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ������������ϸ��Ĥ���ޤ���Ǥ�����",$id);
END
}

# ���Ĥ���μ���
sub logOilMoney {
    my($id, $name, $lName, $point, $str) = @_;
    logSecret("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>���顢<B>$str</B>�����������Ф���ޤ�����",$id);
END
}
sub logOnseMoney {
    my($id, $name, $lName, $point, $str) = @_;
    logSecret("${HtagName_}${name}��$point${H_tagName}��<B>����</B>���顢<B>$str</B>�μ��פ��夬��ޤ�����",$id);
END
}

# ���ĸϳ�
sub logOilEnd {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�ϸϳ餷���褦�Ǥ���",$id);
END
}

# �ɱһ��ߡ��������å�
sub logBombSet {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>�������֤����å�</B>����ޤ�����",$id);
END
}

# �ɱһ��ߡ�������ư
sub logBombFire {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�������ֺ�ư����${H_tagDisaster}",$id);
END
}

# ��ǰ�ꡢȯ��
sub logMonFly {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>�첻�ȤȤ������Ω���ޤ���</B>��",$id);
END
}

# ��ǰ�ꡢ�
sub logMonDamage {
    my($id, $name, $point) = @_;
    logOut("<B>�����ȤƤĤ�ʤ����</B>��${HtagName_}${name}��$point${H_tagName}����������ޤ�������",$id);
}

# ����or�ߥ��������
sub logPBSuc {
    my($id, $name, $comName, $point) = @_;
    logSecret("${HtagName_}${name}��$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
    logOut("������ʤ�����${HtagName_}${name}��${H_tagName}��<B>��</B>���������褦�Ǥ���",$id);
END
}
sub logABSuc {
    my($id, $name, $comName, $point) = @_;
    logSecret("${HtagName_}${name}��$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
    logOut("${HtagName_}${name}��$point${H_tagName}��<${HtagComName_}����${H_tagComName}���Ԥ��ޤ�����",$id);
END
}
# �ϥ�ܥ�
sub logHariSuc {
    my($id, $name, $comName, $comName2, $point) = @_;
    logSecret("${HtagName_}${name}��$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
    logLandSuc($id, $name, $comName2, $point);
END
}

# �ػ߹԰�
sub logNotPermitted {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ����Ԥ���${HtagDisaster_}˸��${H_tagDisaster}�ˤ��<B>�˻�</B>����ޤ�����",$id);
}

# �ߥ������Ȥ��Ȥ���(or �����ɸ����褦�Ȥ���)���������åȤ����ʤ�
sub logMsNoTarget {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ���ɸ����˿ͤ���������ʤ�������ߤ���ޤ�����",$id);
END
}
sub logNoRazer {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ��졼�����������ͭ���Ƥ��ʤ�������ߤ���ޤ�����",$id);
END
}
sub logUnRazer {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ��졼����������������ǽ�Τ�����ߤ���ޤ�����",$id);
END
}
sub logNoPMS {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ�PMS�������ͭ���Ƥ��ʤ�������ߤ���ޤ�����",$id);
END
}
sub logUnPMS {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ�PMS������������ǽ�Τ�����ߤ���ޤ�����",$id);
END
}
# �ߥ������Ȥ��Ȥ��������Ϥ��ʤ�
sub logMsNoBase {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ�<B>�ߥ�������������ͭ���Ƥ��ʤ�</B>����˼¹ԤǤ��ޤ���Ǥ�����",$id);
END
}

sub logyoushoFail {
    my($id, $name, $point, $comName)= @_;
    logSecret("${HtagName_}${name}��$point${H_tagName}�������Ǥʤ��Τ�${HtagComName_}${comName}${H_tagComName}����ߤ���ޤ�����",$id);
END
}
sub logzoukyou {
    my($id, $name, $point) = @_;
    logSecret("${HtagName_}${name}��$point${H_tagName}�λ��ߤ��������ޤ�����",$id);
    logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}Ͷ�׳�ư${H_tagComName}���Ԥ��ޤ�����",$id);
END
}
sub logLanddeme {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ�<B>���Ǥ˵��ݴ�¬����ͭ���Ƥ���</B>���ᡢ�¹ԤǤ��ޤ���Ǥ�����",$id);
END
}
sub logLanddume {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ�<B>���Ǥˤ��Τ鸦�����ͭ���Ƥ���</B>���ᡢ�¹ԤǤ��ޤ���Ǥ�����",$id);
END
}
sub logLanddime {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ�<B>���Ǥ��ü첻�Ȼ��ߤ��ͭ���Ƥ���</B>���ᡢ�¹ԤǤ��ޤ���Ǥ�����",$id);
END
}
sub logLanddame {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ�<B>���Ǥ˵��ݸ������ͭ���Ƥ���</B>���ᡢ�¹ԤǤ��ޤ���Ǥ�����",$id);
END
}
# �ߥ������ä����ϰϳ�
sub logMsOut {
    my($id, $tId, $name, $tName, $comName, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������<B>�ΰ賰�γ�</B>����������ͤǤ���",$id, $tId);
}
sub logNsOut {
    my($id, $name, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��$tPoint${H_tagName}�����«�졼����ˤ��${HtagName_}$point${H_tagName}�����˸����ƥ졼������ȯ�ͤ��ޤ�������<B>�ΰ賰�γ�</B>����������ͤǤ���",$id);
}

# ���ƥ륹�ߥ������ä����ϰϳ�
sub logMsOutS {
    my($id, $tId, $name, $tName, $comName, $point) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������<B>�ΰ賰�γ�</B>����������ͤǤ���",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��$point${H_tagName}�ظ�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������<B>�ΰ賰�γ�</B>����������ͤǤ���",$tId);
}

# �ߥ������ä����ɱһ��ߤǥ���å�
sub logMsCaught {
    my($id, $tId, $name, $tName, $comName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��������ˤ��Ͼ��ª����졢<B>������ȯ</B>���ޤ�����",$id, $tId);
}
# �ߥ������ä�����ƻ�����졢�̤����
sub logMsMistake {
  my($id, $tId, $name, $oldtName) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${oldtName}��${H_tagName}�˸�����ȯ�ͤ����ߥ�����ϡ�����ǵ�ƻ���Ѥ��ޤ�����",$id, $tId);
}
# ���ƥ륹�ߥ������ä����ɱһ��ߤǥ���å�
sub logMsCaughtS {
    my($id, $tId, $name, $tName, $comName, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��������ˤ��Ͼ��ª����졢<B>������ȯ</B>���ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��$point${H_tagName}�ظ�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��������ˤ��Ͼ��ª����졢<B>������ȯ</B>���ޤ�����",$tId);
}

# �ߥ������ä������̤ʤ�
sub logMsNoDamage {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��������Τ��ﳲ������ޤ���Ǥ�����",$id, $tId);
}
sub logXsNoDamage {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$tPoint${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������<B>$tLname</B>�ˤ��ä��Τ��ﳲ������ޤ���Ǥ�����",$id, $tId);
}
sub logNsNoDamage {
    my($id, $name, $tLname,$tPoint, $point, $cPoint) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}�������٥졼����ˤ��${HtagName_}$tPoint${H_tagName}�����˸����ƥ졼����ȯ�ͤ�Ԥ��ޤ�������${HtagName_}$cPoint${H_tagName}��<B>$tLname</B>��������Τ��ﳲ������ޤ���Ǥ�����",$id);
}
# ���ƥ륹�ߥ������ä������̤ʤ�
sub logMsNoDamageS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��������Τ��ﳲ������ޤ���Ǥ�����",$id, $tId);

    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��������Τ��ﳲ������ޤ���Ǥ�����",$tId);
}
sub logMsNoDamageT {
    my($id, $name, $tLname, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>���Фζ̤��Ǥ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��������Τ��ﳲ������ޤ���Ǥ�����",$id);
}
sub logdasuyo {
    my($id, $name, $mName, $point,$tPoint,$tLname) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>����ʼ���ȯ�ͤ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�����ơ�",$id);
}
sub logdasuyoZ {
    my($id, $name, $mName, $point,$tPoint,$tLname) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>���˥Х���������ȯ�ͤ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�����ơ�",$id);
}
sub logmonkamiT {
    my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>���Фζ̤��Ǥ���${HtagName_}$tPoint${H_tagName}��<B>����$kName</B>��̿�桢�������Хꥢ�����ˤޤ���̤�����ޤ���Ǥ�����",$id);
}
sub lognodamageT {
    my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>���Фζ̤��Ǥ���${HtagName_}$tPoint${H_tagName}��<B>����$kName</B>��̿�桢�������Ų�����ä�������̤�����ޤ���Ǥ�����",$id);
}
sub logMsMonKillT {
    my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>���Фζ̤��Ǥ���${HtagName_}$tPoint${H_tagName}��<B>����$kName</B>��̿�档<B>����$kName</B>���ϿԤ����ݤ�ޤ�����",$id);
}
sub logMsMonsterT {
my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>���Фζ̤��Ǥ���${HtagName_}$tPoint${H_tagName}��<B>����$kName</B>��̿�档<B>����$kName</B>�϶줷��������Ӭ���ޤ�����",$id);
}
sub logMsNormalT {
my($id, $name, $tLname, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>���Фζ̤��Ǥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�桢���Ӥ����Ǥ��ޤ�����",$id, $tId);
}
sub logMsNoDamageU {
    my($id, $name, $tLname, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>��ˤ�Ƥ�ȯ�ͤ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��������Τ��ﳲ������ޤ���Ǥ�����",$id);
}
sub logmonkamiU {
    my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>��ˤ�Ƥ�ȯ�ͤ���${HtagName_}$tPoint${H_tagName}��<B>����$kName</B>��̿�桢�������Хꥢ�����ˤޤ���̤�����ޤ���Ǥ�����",$id);
}
sub lognodamageU {
    my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>��ˤ�Ƥ�ȯ�ͤ���${HtagName_}$tPoint${H_tagName}��<B>����$kName</B>��̿�桢�������Ų�����ä�������̤�����ޤ���Ǥ�����",$id);
}
sub logMsMonKillU {
    my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>��ˤ�Ƥ�ȯ�ͤ���${HtagName_}$tPoint${H_tagName}��<B>����$kName</B>��̿�档<B>����$kName</B>���ϿԤ����ݤ�ޤ�����",$id);
}
sub logMsMonsterU {
my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>��ˤ�Ƥ�ȯ�ͤ���${HtagName_}$tPoint${H_tagName}��<B>����$kName</B>��̿�档<B>����$kName</B>�϶줷��������Ӭ���ޤ�����",$id);
}
sub logMsNormalU {
my($id, $name, $tLname, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>��ˤ�Ƥ�ȯ�ͤ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�桢���Ӥ����Ǥ��ޤ�����",$id, $tId);
}
sub logMsNoDamageV {
    my($id, $name, $tLname, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>���饤�ե��ȯ�ͤ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��������Τ��ﳲ������ޤ���Ǥ�����",$id);
}
sub logmonkamiV {
    my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>���饤�ե��ȯ�ͤ���${HtagName_}$tPoint${H_tagName}��<B>����$kName</B>��̿�桢�������Хꥢ�����ˤޤ���̤�����ޤ���Ǥ�����",$id);
}
sub lognodamageV {
    my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>���饤�ե��ȯ�ͤ���${HtagName_}$tPoint${H_tagName}��<B>����$kName</B>��̿�桢�������Ų�����ä�������̤�����ޤ���Ǥ�����",$id);
}
sub logMsMonKillV {
    my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>���饤�ե��ȯ�ͤ���${HtagName_}$tPoint${H_tagName}��<B>����$kName</B>��̿�档<B>����$kName</B>���ϿԤ����ݤ�ޤ�����",$id);
}
sub logMsMonsterV {
my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>���饤�ե��ȯ�ͤ���${HtagName_}$tPoint${H_tagName}��<B>����$kName</B>��̿�档<B>����$kName</B>�϶줷��������Ӭ���ޤ�����",$id);
}
sub logMsNormalV {
my($id, $name, $tLname, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>���饤�ե��ȯ�ͤ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�桢���Ӥ����Ǥ��ޤ�����",$id);
}
sub logMsNoDamageX {
    my($id, $name, $tLname, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>��̤�Τ�ʼ���ȯ�ͤ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��������Τ��ﳲ������ޤ���Ǥ�����",$id);
}
sub logMsNormalX {
my($id, $name, $tLname, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}${HtagName_}$point${H_tagName}��<B>����$mName</B>��̤�Τ�ʼ���ȯ�ͤ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�桢���פ��ޤ�����",$id, $tId);
}
# Φ���˲��ơ�����̿��
sub logMsLDMountain {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�档<B>$tLname</B>�Ͼä����ӡ����ϤȲ����ޤ�����",$id, $tId);
}

# Φ���˲��ơ�������Ϥ�̿��
sub logMsLDSbase {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��������ȯ��Ʊ�����ˤ��ä�<B>$tLname</B>���׷���ʤ��᤭���Ӥޤ�����",$id, $tId);
}

# Φ���˲��ơ����ä�̿��
sub logMsLDMonster {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}�����Ƥ���ȯ��Φ�Ϥ�<B>����$tLname</B>���Ȥ���פ��ޤ�����",$id, $tId);
}

# Φ���˲��ơ�������̿��
sub logMsLDSea1 {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�����ơ����줬�������ޤ�����",$id, $tId);
}

# Φ���˲��ơ�����¾���Ϸ���̿��
sub logMsLDLand {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�����ơ�Φ�ϤϿ��פ��ޤ�����",$id, $tId);
}

# �̾�ߥ����롢���Ϥ�����
sub logMsWaste {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>������ޤ�����",$id, $tId);
}
sub logNsWaste {
    my($id, $name, $tLname,$tPoint, $point, $cPoint) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}�������٥졼����ˤ��${HtagName_}$tPoint${H_tagName}�����˸����ƥ졼����ȯ�ͤ�Ԥ��ޤ�������${HtagName_}$cPoint${H_tagName}��<B>$tLname</B>������ޤ�����",$id);
}

# ���ƥ륹�ߥ����롢���Ϥ�����
sub logMsWasteS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>������ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>������ޤ�����",$tId);
}

# �̾�ߥ����롢���ä�̿�桢�Ų���ˤ�̵��
sub logMsMonNoDamage {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�桢�������Ų����֤��ä�������̤�����ޤ���Ǥ�����",$id, $tId);
}
sub logNsMonNoDamage {
    my($id, $name, $tLname,$tPoint, $point, $cPoint) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}�������٥졼����ˤ��${HtagName_}$tPoint${H_tagName}�����˸����ƥ졼����ȯ�ͤ�Ԥ���${HtagName_}$cPoint${H_tagName}��<B>����$tLname</B>��̿�桢�������Ų����֤��ä�������̤�����ޤ���Ǥ�����",$id);
}
sub logNsMonNoDamageKami {
    my($id, $name, $tLname,$tPoint, $point, $cPoint) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}�������٥졼����ˤ��${HtagName_}$tPoint${H_tagName}�����˸����ƥ졼����ȯ�ͤ�Ԥ���${HtagName_}$cPoint${H_tagName}��<B>����$tLname</B>��̿�桢�������Хꥢ�����ˤޤ���̤�����ޤ���Ǥ�����",$id);
}
# ���ƥ륹�ߥ����롢���ä�̿�桢�Ų���ˤ�̵��
sub logMsMonNoDamageS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�桢�������Ų����֤��ä�������̤�����ޤ���Ǥ�����",$id, $tId);
    logOut("<B>���Ԥ�</B>��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�桢�������Ų����֤��ä�������̤�����ޤ���Ǥ�����",$tId);
}
sub logmonkami {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�桢�������Хꥢ�����ˤޤ���̤�����ޤ���Ǥ�����",$id, $tId);
}
# �̾�ߥ����롢���ä�̿�桢����
sub logMsMonKill {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>���ϿԤ����ݤ�ޤ�����",$id, $tId);
}
sub logNsMonKill {
    my($id, $name, $tLname,$tPoint, $point, $cPoint) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}�������٥졼����ˤ��${HtagName_}$tPoint${H_tagName}�����˸����ƥ졼����ȯ�ͤ�Ԥ���${HtagName_}$cPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>���ϿԤ����ݤ�ޤ�����",$id);}

# ���ƥ륹�ߥ����롢���ä�̿�桢����
sub logMsMonKillS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>���ϿԤ����ݤ�ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>���ϿԤ����ݤ�ޤ�����", $tId);
}

# �̾�ߥ����롢���ä�̿�桢���᡼��
sub logMsMonster {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>�϶줷��������Ӭ���ޤ�����",$id, $tId);
}
sub logNsMonster {
    my($id, $name, $tLname,$tPoint, $point, $cPoint) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}�������٥졼����ˤ��${HtagName_}$tPoint${H_tagName}�����˸����ƥ졼����ȯ�ͤ�Ԥ���${HtagName_}$cPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>�϶줷��������Ӭ���ޤ�����",$id);
}
# ���ܡ����ä�̿�桢����
sub logMsMonsterH {
my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>�Ϥߤ�ߤ븵���ˤʤ�ޤ�����",$id, $tId);
}

# ���ܡ����ä�̿�桢����ʾ�������ʤ�
sub logMsMonsterM {
my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档�������ʤˤⵯ����ޤ���Ǥ�����",$id, $tId);
}
# ���ƥ륹�ߥ����롢���ä�̿�桢���᡼��
sub logMsMonsterS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>�϶줷��������Ӭ���ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>�϶줷��������Ӭ���ޤ�����",$tId);
}
# Φ�������ơ����ä�̿��
sub logMsREMonster {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�����ơ�����<B>$tLname</B>��δ���˰��ߤ��ޤ�ޤ�����",$id, $tId);
}
sub logXsREMonster {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$tPoint${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ�������<B>$tLname</B>��δ���˰��ߤ��ޤ�ޤ�����",$id, $tId);
}
# Φ�������ơ�����̿��
sub logMsRESea {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�����ơ����줬δ�����������ˤʤ�ޤ�����",$id, $tId);
}
sub logXsRESea {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$tPoint${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���<B>$tLname</B>��δ��,�����ˤʤ�ޤ�����",$id, $tId);
}
# Φ�������ơ�������̿��
sub logMsRESea1 {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�����ơ�������δ����Φ�Ϥˤʤ�ޤ�����",$id, $tId);
}
sub logXsRESea1 {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$tPoint${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���<B>$tLname</B>��δ��,Φ�Ϥˤʤ�ޤ�����",$id, $tId);
}
# Φ�������ơ�������Ϥ�̿��
sub logMsRESbase {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�����ơ�δ���Τ��᳤����Ϥ��˲�����ޤ���",$id, $tId);
}
sub logXsRESbase {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$tPoint${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���<B>$tLname</B>��δ����������Ϥ��˲�����ޤ���",$id, $tId);
}

# Φ�������ơ����Ĥ�̿��
sub logMsREOil {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�����ơ�δ���Τ������Ĥ��˲�����ޤ�����",$id, $tId);
}
sub logMsREYou {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�����ơ�δ���Τ����ܿ�����˲�����ޤ�����",$id, $tId);
}
sub logXsREOil {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$tPoint${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���<B>$tLname</B>��δ�������Ĥ��˲�����ޤ�����",$id, $tId);
}
sub logXsREYou {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$tPoint${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���<B>$tLname</B>��δ�����ܿ�����˲�����ޤ�����",$id, $tId);
}
# Φ�������ơ�����¾���Ϸ���̿��
sub logMsRELand {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�����ơ�Φ�Ϥ�δ���������Ǥ��ޤ�����",$id, $tId);
}
sub logXsRELand {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$tPoint${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���<B>$tLname</B>��δ���������Ǥ��ޤ�����",$id, $tId);
}
# ���äλ���
sub logMsMonMoney {
    my($tId, $mName, $value, $name) = @_;
    logOut("<B>����$mName</B>�λĳ��ˤϡ�<B>$value$HunitMoney</B>���ͤ��դ��ޤ������ޤ����ä��ݤ���${HtagName_}${name}��${H_tagName}�ˤ�<B>$value$HunitMoney</B>�η��޶⤬ʧ���ޤ�����",$tId);
}

# �̾�ߥ������̾��Ϸ���̿��
sub logMsNormal {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�桢���Ӥ����Ǥ��ޤ�����",$id, $tId);
}
sub logNsNormal {
    my($id, $name, $tLname,$tPoint, $point, $cPoint) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}�������٥졼����ˤ��${HtagName_}$tPoint${H_tagName}�����˸����ƥ졼����ȯ�ͤ�Ԥ���${HtagName_}$cPoint${H_tagName}��<B>$tLname</B>��̿�桢���Ӥ����Ǥ��ޤ�����",$id);
}
# ���ƥ륹�ߥ������̾��Ϸ���̿��
sub logMsNormalS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�桢���Ӥ����Ǥ��ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�桢���Ӥ����Ǥ��ޤ�����",$tId);
}
# �������ơ�����
sub logMsNeutron {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}����������������ޤ�����",$id, $tId);
}
# �ߥ�������̱����
sub logMsBoatPeople {
    my($id, $name, $achive) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ˤɤ�����Ȥ�ʤ�<B>$achive${HunitPop}�����̱</B>��ɺ�夷�ޤ�����${HtagName_}${name}��${H_tagName}�ϲ����������줿�褦�Ǥ���",$id);
}
sub logWideDamageSeaDead {
    my($id, $tId, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>����</B>�����褦�Ǥ���",$id,$tId);
}
sub logWideDamageSeaDead2 {
    my($id, $tId, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>����᡼��</B>��������褦�Ǥ���",$id,$tId);
}
sub logWideDamageMonsterDead {
    my($id, $tId,$name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����$lName</B>��©�䤨�ޤ�����",$id,$tId);
}
sub logWideDamageMonsterDead2 {
    my($id, $tId,$name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����$lName</B>����᡼��</B>��������褦�Ǥ���",$id,$tId);
}
sub logWideDamageDead {
    my($id, $tId, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�ˤ����͡���<B>����</B>�����褦�Ǥ���",$id,$tId);
}
sub logsandoi {
    my($id, $name, $tLname,$mName, $point,$tPoint) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����$mName</B>�νФ�����${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ϰ��߹��ޤ�ޤ�����",$id);
}

sub logmoerui {
    my($id, $name, $tLname,$mName, $point,$tPoint) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����$mName</B>�νФ���ˤ�ä�${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��ǳ���Ԥ��ޤ�����",$id);
}
# �����ɸ�
sub logMonsSend {
    my($id, $tId, $name, $tName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>��¤����</B>���¤��${HtagName_}${tName}��${H_tagName}�����ꤳ�ߤޤ�����",$id, $tId);
}
sub logMonsSendDamez {
    my($id, $tId, $name, $tName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>��¤����</B>���¤���褦�Ȥ��ޤ�����<b>���Τ鸦���</b>�Υ�٥뤬­��ޤ���Ǥ�����",$id, $tId);
}

# ��ⷫ��
sub logDoNothing {
    my($id, $name, $comName) = @_;
#    logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
}

# ͢��
sub logSell {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>$value$HunitFood</B>��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",$id);
}
sub logOilSell {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>$value�ȥ�</B>��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",$id);
}
# ���
sub logAid {
    my($id, $tId, $name, $tName, $comName, $str) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}��<B>$str</B>��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",$id, $tId);
}
sub logAidH {
my($id, $tId, $name, $tName, $comName, $str) = @_;
logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}��<B>$str</B>��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",$id, $tId);
logLate("���Ԥ���${HtagName_}${tName}��${H_tagName}��<B>$str</B>��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",$tId);
}
sub logshamo {
    my($id, $name, $str) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��<B>$str����</B>���֤��ޤ�����",$id);
}
sub logShaku {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>$value����</B>��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",$id);
}
sub logShakubame {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}��Ԥ����Ȥ��ޤ��������Ǥ˼ڤ�����򤷤Ƥ���ΤǷײ����ߤ��ޤ�����",$id);
}
sub logOitekyo {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}�����Ĥ�ű��ޤ�����",$id,);
}
sub logyotekyo {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}���ܿ����ű��ޤ�����",$id,);
}
sub logminatekyo {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}�ι���ű��ޤ�����",$id,);
}
sub logtekyoFail {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}�ˤϳ�����ۤϤʤ��ΤǷײ����ߤ��ޤ�����",$id,);
}
# Ͷ�׳�ư
sub logPropaganda {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
}
 # ���á������Ƨ��
 sub logMonsMoveMine {
     my($id, $name, $lName, $point, $mName) = @_;
     logOut("<B>����$mName</B>��${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��Ƨ�ߡ�<B>${lName}����ȯ���ޤ�������</B>",$id);
}

 # ���á������Ƨ��������¸
 sub logMonsMoveMineAlive {
     my($id, $name, $lName, $point, $mName) = @_;
     logOut("<B>����$mName</B>�϶줷��������Ӭ���ޤ�����",$id);
}

 # ���á������Ƨ�����˻�˴
 sub logMonsMoveMineDead {
     my($id, $name, $lName, $point, $mName) = @_;
     logOut("<B>����$mName</B>���ϿԤ����ݤ�ޤ�����",$id);
}

 # ���á������Ƨ�����˿᤭����
 sub logMonsMoveMineScatter {
     my($id, $name, $lName, $point, $mName) = @_;
     logOut("<B>����$mName</B>���׷���ʤ��᤭���Ӥޤ�����",$id);
}

# ����
sub logGiveup {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}���������졢<B>̵����</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}����������<B>̵����</B>�Ȥʤ롣");
}
sub logsen {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>ʿ�°���Ʊ��</B>�˲������Ƥ��뤿�ᡢ<B>���谦��Ʊ��</B>�ˤϲ����Ǥ��ޤ���",$id);
}
sub loghei {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>���谦��Ʊ��</B>�˲������Ƥ��뤿�ᡢ<B>ʿ�°���Ʊ��</B>�ˤϲ����Ǥ��ޤ���",$id);
}
sub logkouk {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>�������</B>�϶�������ޤ�����",$id);
}
sub logkank {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>�ƻ����</B>�϶�������ޤ�����",$id);
}
sub logbouk {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>�ɸ����</B>�϶�������ޤ�����",$id);
}
sub logreik {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>�졼��������</B>�϶�������ޤ�����",$id);
}
sub loghatk {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>ȯ�ű���</B>�϶�������ޤ�����",$id);
}
sub logemtk {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>PMS����</B>�϶�������ޤ�����",$id);
}
sub logemtx {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>�졼��������</B>��<B>PMS����</B>�˲�¤����ޤ�����",$id);
}
sub logemty {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>�졼��������</B>���ͭ���Ƥ��ʤ��ΤǷײ����ߤ���ޤ�����",$id);
}
sub logkouei {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}���������ޤ�����",$id);
}
sub logdamekouei {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}�ϼ��Ԥ��ޤ�����",$id);
}
sub logkouuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}�ι������������Ȥ��ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��${H_tagName}�ι������������Ȥ��ޤ���",$tId);
}
sub logpmsuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}��PMS����������Ȥ��ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��${H_tagName}��PMS����������Ȥ��ޤ���",$tId);
}

sub logkoueikurukuru {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�Ϥ��Ǥ�PMS��������äƤ��뤿��${HtagComName_}${comName}${H_tagComName}�ϼ¹ԤǤ��ޤ���Ǥ�����",$id, $tId);
}
sub logkanuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}�δƻ����������Ȥ��ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��${H_tagName}�δƻ����������Ȥ��ޤ���",$tId);
}
sub logbouuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}���ɸ����������Ȥ��ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��${H_tagName}���ɸ����������Ȥ��ޤ���",$tId);
}
sub logreiuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}�Υ졼��������������Ȥ��ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��${H_tagName}�Υ졼��������������Ȥ��ޤ���",$tId);
}
sub loghatuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}��ȯ�ű���������Ȥ��ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��${H_tagName}��ȯ�ű���������Ȥ��ޤ���",$tId);
}
sub logdamebouuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}���ɸ����������Ȥ����Ȥ��ޤ��������Ԥ��ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��${H_tagName}���ɸ����������Ȥ����Ȥ��ޤ��������Ԥ��ޤ�����",$tId);
}
sub logdamehatuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}��ȯ�ű���������Ȥ����Ȥ��ޤ��������Ԥ��ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��${H_tagName}��ȯ�ű���������Ȥ����Ȥ��ޤ��������Ԥ��ޤ�����",$tId);
}
sub logdamereiuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}�Υ졼��������������Ȥ����Ȥ��ޤ��������Ԥ��ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��${H_tagName}�Υ졼��������������Ȥ����Ȥ��ޤ��������Ԥ��ޤ�����",$tId);
}
sub logdamekouuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}�ι������������Ȥ����Ȥ��ޤ��������Ԥ��ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��${H_tagName}�ι������������Ȥ����Ȥ��ޤ��������Ԥ��ޤ�����",$tId);
}
sub logdamepmsuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}��PMS����������Ȥ����Ȥ��ޤ��������Ԥ��ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��${H_tagName}��PMS����������Ȥ����Ȥ��ޤ��������Ԥ��ޤ�����",$tId);
}
sub logsaikou {
    my($id, $target,$name, $tName, $comName) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}�˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",$id, $tId);
    logOut("<B>���Ԥ�</B>��${HtagName_}${tName}��${H_tagName}�˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",$tId);
}
sub logjisaikou {
    my($id, $target,$name, $tName, $comName) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}�˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ��������Ԥ���������˽�����ޤ�����",$id, $tId);
}

sub logsiyou {
    my($id, $name) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}�Υ졼���������ϻ��Ѳ�ǽ�ˤʤ�ޤ�����",$id);
}
sub logsiyouZ {
    my($id, $name) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��PMS�����ϻ��Ѳ�ǽ�ˤʤ�ޤ�����",$id);
}
sub lognasi {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ϵ��ݸ������ͭ���Ƥ��ʤ����ᡢ${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ���",$id);
}
sub logsisai {
    my($id, $target,$name, $tName, $comName) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}�˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ��������Ԥ��ޤ�����",$id, $tId);
    logOut("<B>���Ԥ�</B>��${HtagName_}${tName}��${H_tagName}�˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ��������Ԥ��ޤ�����",$tId);
}
sub logsaimitu {
    my($id, $target,$name, $tName, $comName) = @_;
    logOut("${HtagName_}${tName}��${H_tagName}�ε��ݴ�¬��β��Ϥη�̡�${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}�˸�����${HtagComName_}${comName}${H_tagComName}��Ԥä����Ȥ��狼��ޤ�����",$id, $tId);
}
sub logdamekanuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}�δƻ����������Ȥ����Ȥ��ޤ��������Ԥ��ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��${H_tagName}�δƻ����������Ȥ����Ȥ��ޤ��������Ԥ��ޤ�����",$tId);
}

sub logmitukaru {
my($id, $tId, $name, $tName, $comName) = @_;
logLate("${HtagName_}${tName}��${H_tagName}�δƻ��������Υǡ����β��Ϥη�̡�${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}�򤷤����Ȥ��狼��ޤ�����",$id, $tId);}
sub logteiko {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}���ޤ�����",$id);
}
sub logteikyo {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��¾�رĤ�°���Ƥ��뤿��${HtagComName_}${comName}${H_tagComName}�ϤǤ��ޤ���",$id);
}
sub logteimu {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�����谦��Ʊ�������äƤ��ʤ�����${HtagComName_}${comName}${H_tagComName}�ϤǤ��ޤ���",$id);
}
sub logInoknasi {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}��Ԥ����Ȥ��ޤ�����<b>���Τ鸦���</b>���ʤ����ᡢ�¹ԤǤ��ޤ���Ǥ�����",$id);
}
sub logForest {
my($id, $name, $lName, $point) = @_;
logSecret("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�ϡ�<B>��</B>�ˤʤ�ޤ�����",$id);
}
sub logsabaku {
my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�ϡ�<B>����</B>�ˤʤ�ޤ�����",$id);
}
sub logMati {
my($id, $name, $lName, $point) = @_;
logSecret("${HtagName_}${name}��$point${H_tagName}��<B>¼</B>���Ǥ��ޤ�����",$id);
}
sub logsougen {
my($id, $name, $lName, $point) = @_;
logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�ϡ�<B>ʿ��</B>�ˤʤ�ޤ�����",$id);
}
sub logareti {
my($id, $name, $lName, $point) = @_;
logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�ϡ�<B>����</B>�ˤʤ�ޤ�����",$id);
}
sub logGeki {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}��Ԥ��������ޤ�����",$id);
}
sub logGekidame {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ��������Ԥ��ޤ�����",$id);
}

# ����
sub logDead {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}����ͤ����ʤ��ʤꡢ<B>̵����</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}���ͤ����ʤ��ʤ�<B>̵����</B>�Ȥʤ롣");
}

# ȯ��
sub logDiscover {
    my($name) = @_;
    logHistory("${HtagName_}${name}��${H_tagName}��ȯ������롣");
}

# ̾�����ѹ�
sub logChangeName {
    my($name1, $name2) = @_;
    logHistory("${HtagName_}${name1}��${H_tagName}��̾�Τ�${HtagName_}${name2}��${H_tagName}���ѹ����롣");
}

# ����
sub logStarve {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}��������­${H_tagDisaster}���Ƥ��ޤ�����",$id);
}
# ����
sub logShorve {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}�Ż�����­${H_tagDisaster}���Ƥ��ޤ�����",$id);
}
sub logMizrve {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}�夬��­${H_tagDisaster}���Ƥ��ޤ�����",$id);
}
# ���ø���
sub logMonsCome {
    my($id, $name, $mName, $point, $lName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>����$mName</B>�и�����${HtagName_}$point${H_tagName}��<B>$lName</B>��Ƨ�߹Ӥ餵��ޤ�����",$id);
}
sub logkamikas {
    my($id, $name,$point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>���ä��Τ��</B>��<B>�к�</B>������������ޤ�����",$id);
}
sub logkamifuu {
    my($id, $name,$point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>���ä��Τ��</B>��<B>����</B>��ƤӤޤ�����",$id);
}
sub logkaminam {
    my($id, $name,$point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>���ä��Τ��</B>��<B>����</B>��ƤӤޤ�����",$id);
}
sub logkamifun {
    my($id, $name,$point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>���ä��Τ��</B>��<B>ʮ��</B>������������ޤ�����",$id);
}
sub logkamiins {
    my($id, $name,$point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>���ä��Τ��</B>��<B>���</B>��ƤӤޤ�����",$id);
}
sub logkamidai {
    my($id, $name,$point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>���ä��Τ��</B>��<B>�����</B>��ƤӤޤ�����",$id);
}
sub logkamijis {
    my($id, $name,$point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>���ä��Τ��</B>��<B>�Ͽ�</B>��ƤӤޤ�����",$id);
}
sub logkamijib {
    my($id, $name,$point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>���ä��Τ��</B>��<B>��������</B>������������ޤ�����",$id);
}
# ���á��������ˤ�ä�ž�������
 sub logMonsMoveMineWarp {
     my($id, $name, $lName, $point, $mName, $tId, $tName) = @_;
     logOut("<B>����$mName</B>��${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��Ƨ�ߡ�<B>${lName}��ȯư���ޤ�������</B>",$id);
     logOut("<B>����$mName</B>��${HtagName_}${name}��${H_tagName}��<B>$lName</B>�ˤ�ä�${HtagName_}${tName}��${H_tagName}��ž������ޤ�����",$id, $tId);
}
sub logMonsterkak {
    my($id, $name, $point, $mName) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����$mName</B>�ϳ��ä���������ȥ����󤤤Τ�ˤʤ�ޤ�����",$id);
}
# ����ư��
sub logMonsMove {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>����$mName</B>��Ƨ�߹Ӥ餵��ޤ�����",$id);
}
sub logMonsFarm {
    my($id, $name, $point, $mName) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����</B>��<B>����$mName</B>�˿����Ӥ餵��ޤ�����",$id);
}
# ���õ���
sub logQee {
    my($id, $name, $point, $mName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>����$mName</B>��${HtagName_}$point${H_tagName}�ˤ��Τ饨�å������ߤޤ�����",$id);
}
sub logmada {
    my($id, $name, $point, $mName) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$mName</B>�Ϥޤ���ΤޤޤǤ���",$id);
}

sub logEgg {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}$point${H_tagName}�ˤ���<B>���Τ饨�å�</B>���ۤ�<B>���Τ�٥��ӡ�</B>�����ޤ�ޤ�����",$id);
}
sub loghenka {
    my($id, $name, $mName, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}$point${H_tagName}�ˤ���<B>���ä��Τ�٥��ӡ�</B>��<B>$mName</B>����Ĺ���ޤ�����",$id);
}
# ���á��ɱһ��ߤ�Ƨ��
sub logMonsMoveDefence {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("<B>����$mName</B>��${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>����ã��<B>${lName}�μ������֤���ư����</B>",$id);
}
# ���õ���
sub logkaeru {
    my($id, $name, $mName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����$mName</B>�������ޤ�����",$id);
}
# �к�
sub logFire {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�к�${H_tagDisaster}�ˤ����Ǥ��ޤ�����",$id);
}
sub logDis {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}������${H_tagDisaster}��̢�䤷�ޤ�����",$id);
}
# ��¢��
sub logaka {
    my($id, $name, $lName,$point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}��Ĭ${H_tagDisaster}��ȯ�������Ϥ��㸺���ޤ�����",$id);
}
sub logMaizo {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�Ǥ�${HtagComName_}$comName${H_tagComName}��ˡ�<B>$value$HunitMoney�����¢��</B>��ȯ������ޤ�����",$id);
}

# �Ͽ�ȯ��
sub logEarthquake {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}���絬�Ϥ�${HtagDisaster_}�Ͽ�${H_tagDisaster}��ȯ������",$id);
}
# �ں�����
sub logEQfall {
my($id, $name, $lName, $point) = @_;
logLate("${HtagName_}${name}��$point${H_tagName}������<B>$lname</B>��${HtagDisaster_}�ں�����${H_tagDisaster}��ȯ����",$id);
}
# �ں����졢�ﳲ
sub logEQfalldamage {
my($id, $name, $lName, $point) = @_;
logLate("${HtagName_}${name}��$point${H_tagName}������<B>$lName</B>�ϡ�${HtagDisaster_}�ں�����${H_tagDisaster}�αƶ��ǲ��Ǥ��ޤ�����",$id);
}
# �Ͽ��ﳲ
sub logEQDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�Ͽ�${H_tagDisaster}�ˤ����Ǥ��ޤ�����",$id);
}
sub logBODamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�Ͽ�${H_tagDisaster}�ˤ������ޤ�����",$id);
}
# ������­�ﳲ
sub logSvDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>��������ƽ�̱������</B>��<B>$lName</B>�ϲ��Ǥ��ޤ�����",$id);
}
sub logSyDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>���ȼԤ�˽�̤Ȥʤ��轱</B>��<B>$lName</B>�ϲ��Ǥ��ޤ�����",$id);
}
# ����ȯ��
sub logTsunami {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ն��${HtagDisaster_}����${H_tagDisaster}ȯ������",$id);
}
sub logHardRain {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}�籫${H_tagDisaster}ȯ������",$id);
}
sub logtree {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>����</B>�Ͻᤤ�ޤ�����",$id);
}
# �����ﳲ
sub logTsunamiDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}����${H_tagDisaster}�ˤ���������ޤ�����",$id);
}

# ����ȯ��
sub logTyphoon {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}����${H_tagDisaster}��Φ����",$id);
}

# �����ﳲ
sub logTyphoonDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}����${H_tagDisaster}�����Ф���ޤ�����",$id);
}

# ��С���
sub logMeteoSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}���${H_tagDisaster}������ޤ�����",$id);
}

# ��С���
sub logMeteoMountain {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}���${H_tagDisaster}�����<B>$lName</B>�Ͼä����Ӥޤ�����",$id);
}

# ��С��������
sub logMeteoSbase {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}���${H_tagDisaster}�����<B>$lName</B>���������ޤ�����",$id);
}

# ��С�����
sub logMeteoMonster {
    my($id, $name, $lName, $point) = @_;
    logOut("<B>����$lName</B>������${HtagName_}${name}��$point${H_tagName}������${HtagDisaster_}���${H_tagDisaster}�����Φ�Ϥ�<B>����$lName</B>���Ȥ���פ��ޤ�����",$id);
}

# ��С�����
sub logMeteoSea1 {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}������${HtagDisaster_}���${H_tagDisaster}��������줬�������ޤ�����",$id);
}

# ��С�����¾
sub logMeteoNormal {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}������<B>$lName</B>��${HtagDisaster_}���${H_tagDisaster}��������Ӥ����פ��ޤ�����",$id);
}

# ��С�����¾
sub logHugeMeteo {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}������${HtagDisaster_}�������${H_tagDisaster}�������",$id);
}
sub logUCmiss {
my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}�����ơ�",$id, $tId);
}
sub logkanoti {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>�ƻ����</B>���絤�������������Ǥ��ޤ�����",$id);
}
sub loghatoti {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>ȯ�ű���</B>���絤�������������Ǥ��ޤ�����",$id);
}
sub logreioti {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>�졼��������</B>���絤�������������Ǥ��ޤ�����",$id);
}
sub logpmsoti {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>PMS����</B>���絤�������������Ǥ��ޤ�����",$id);
}
sub logkouoti {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>�������</B>���絤�������������Ǥ��ޤ�����",$id);
}
sub logbouoti {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>�ɸ����</B>���絤�������������Ǥ��ޤ�����",$id);
}
# ʮ��
sub logEruption {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}������${HtagDisaster_}�л���ʮ��${H_tagDisaster}��<B>��</B>������ޤ�����",$id);
}

# ʮ�С�����
sub logEruptionSea1 {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}������<B>$lName</B>�ϡ�${HtagDisaster_}ʮ��${H_tagDisaster}�αƶ���Φ�Ϥˤʤ�ޤ�����",$id);
}

# ʮ�С���or����
sub logEruptionSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}������<B>$lName</B>�ϡ�${HtagDisaster_}ʮ��${H_tagDisaster}�αƶ��ǳ��줬δ���������ˤʤ�ޤ�����",$id);
}

# ʮ�С�����¾
sub logEruptionNormal {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}������<B>$lName</B>�ϡ�${HtagDisaster_}ʮ��${H_tagDisaster}�αƶ��ǲ��Ǥ��ޤ�����",$id);
}

# ��������ȯ��
sub logFalldown {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}��������${H_tagDisaster}��ȯ�����ޤ�������",$id);
}

# ���������ﳲ
sub logFalldownLand {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�ϳ���������ߤޤ�����",$id);
}

# �����ﳲ������
sub logWideDamageSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>����</B>���ޤ�����",$id);
}

# �����ﳲ�����η���
sub logWideDamageSea2 {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>���׷���ʤ��ʤ�ޤ�����",$id);
}

# �����ﳲ�����ÿ���
sub logWideDamageMonsterSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��Φ�Ϥ�<B>����$lName</B>���Ȥ���פ��ޤ�����",$id);
}
sub logMonsterBom {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����$lName</B>�ϼ�����������˿�����ﳲ��ڤܤ��ޤ�����",$id);
}
sub logMonmon {
    my($id, $name, $point,$mName, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����$mName</B>��<b>$str</b>����Ȥ��ޤ�����",$id);
}
sub logMonUtiDame {
    my($id, $name, $point,$mName) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����$mName</B>�ϲФζ̤�Ϥ��ޤ�������<B>�ΰ賰�γ�</B>����������ͤǤ���",$id);
}
sub logMonUtiDameU {
    my($id, $name, $point,$mName) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����$mName</B>��ˤ�Ƥ�ȯ�ͤ��ޤ�������<B>�ΰ賰�γ�</B>����������ͤǤ���",$id);
}
sub logMonUtiDameV {
    my($id, $name, $point,$mName) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����$mName</B>���饤�ե��ȯ�ͤ��ޤ�������<B>�ΰ賰�γ�</B>����������ͤǤ���",$id);
}
sub logMonUtiDameX {
    my($id, $name, $point,$mName) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����$mName</B>��̤�Τ�ʼ���ȯ�ͤ��ޤ�������<B>�ΰ賰�γ�</B>����������ͤǤ���",$id);
}
sub logMonUtiDameZ {
    my($id, $name, $point,$mName) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����$mName</B>�ϳ˥Х���������ȯ�ͤ��ޤ�������<B>�ΰ賰�γ�</B>����������ͤǤ���",$id);
}
sub logMonUtiDameY {
    my($id, $name, $point,$mName) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����$mName</B>�ϳ�ʼ���ȯ�ͤ��ޤ�������<B>�ΰ賰�γ�</B>����������ͤǤ���",$id);
}
sub logMontue {
    my($id, $name, $point,$mName, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����$mName</B>��$str��å���ޤ�����",$id);
}
# �����ﳲ������
sub logWideDamageMonster {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����$lName</B>�Ͼä����Ӥޤ�����",$id);
}

# �����ﳲ������
sub loghobakukaijo {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����$lName</B>����������ƨ��ޤ�����",$id);
}
# �����ﳲ������
sub logWideDamageWaste {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�ϰ�֤ˤ���<B>����</B>�Ȳ����ޤ�����",$id);
}
# ưʪ�फ��μ��� # ��������
sub logdoubutuMoney {
my($id, $name, $lName, $point, $str) = @_;
logSecret("${HtagName_}${name}��$point${H_tagName}��<B>ưʪ��</B>���顢<B>$str</B>�μ��פ��夬��ޤ�����",$id);
END
} 
# ưʪ�फ��μ��� # ��������
sub logOmiseMoney {
my($id, $name, $lName, $point, $str) = @_;
logSecret("${HtagName_}${name}��$point${H_tagName}��<B>�ǥѡ���</B>���顢<B>$str</B>�μ��פ��夬��ޤ�����",$id);
END
}
sub logBankMoney {
my($id, $name, $lName, $point, $str) = @_;
logSecret("${HtagName_}${name}��$point${H_tagName}��<B>���</B>���顢<B>$str</B>�����Ҥ�����ޤ�����",$id);
}
sub logMsBank {
my($id, $name, $value) = @_;
logOut("${HtagName_}${name}��${H_tagName}�ˤɤ�����Ȥ�ʤ�<B>$value${HunitMoney}��Τ���</B>��ɺ�夷�ޤ�����${HtagName_}${name}��${H_tagName}�ϲ��������Ȥä��褦�Ǥ���",$id);
} 
 
sub logdoumei {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>$comName</B>���ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>$comName</B>");
}
# ��å ��
sub logRobMoney {
  my($id, $tId, $name, $tName, $comName, $RobMoney) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}��Ư����<B>$RobMoney${HunitMoney}</B>å���ޤ�����",$id, $tId);
}
# ��å ����
sub logRobFood {
  my($id, $tId, $name, $tName, $comName, $RobMoney) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}��Ư����<B>$RobMoney${HunitFood}</B>å���ޤ�����",$id, $tId);
}

# ST��å ��
sub logRobSTMoney {
  my($id, $tId, $name, $tName, $comName, $RobMoney) = @_;
  logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}��Ư����<B>$RobMoney${HunitMoney}</B>å���ޤ�����",$id, $tId);
  logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��${H_tagName}${HtagComName_}${comName}${H_tagComName}��Ư����<B>$RobMoney${HunitMoney}</B>å���ޤ�����",$tId);
}
# ST��å ����
sub logRobSTFood {
  my($id, $tId, $name, $tName, $comName, $RobMoney) = @_;
  logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}��Ư����<B>$RobMoney${HunitFood}</B>å���ޤ�����",$id, $tId);
  logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��${H_tagName}${HtagComName_}${comName}${H_tagComName}��Ư����<B>$RobMoney${HunitFood}</B>å���ޤ�����",$tId);
}
sub logMissRob {
  my($id, $tId, $name, $tName, $comName) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}��Ư�����Ȥ��ޤ��������Ԥ��ޤ�����",$id, $tId);
}
sub logteikou {
    my($id, $name,$str) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��Ȣ����Ϣ����<B>������ߤ�����</B>����<B>$str</B>������ι������̿�᤬�Ф���ޤ�����",$id);
}
sub logteimis {
    my($id, $name,$str) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��Ȣ����Ϣ����<B>������ߤ�����</B>���ޤ��������˹��ʤ����᾵ǧ����ޤ���Ǥ�����",$id);
}
sub logteitas {
    my($id, $name,$str) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��Ȣ����Ϣ����<B>�������̿��α�Ĺ������</B>����<B>$str</B>������ι������̿�᤬��Ĺ����ޤ�����",$id);
}
sub logteidame {
    my($id, $target, $name, $tName, $comName)= @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}��<B>$comName</B>���褦�Ȥ��ޤ������������̿�᤬�ФƤ���ΤǼ¹ԤǤ��ޤ���",$id, $tId);
}
sub logteideme {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�Ϲ������̿�᤬�ФƤ���Τ�<B>$comName</B>�ϼ¹ԤǤ��ޤ���",$id);
}
# ����
sub logPrize {
    my($id, $name, $pName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>$pName</B>����ޤ��ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>$pName</B>�����");
}
sub logkoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>���Ȳ�</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>���Ȳ�</B>��");
}
sub lognoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>������</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>������</B>��");
}
sub logooukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>������</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>������</B>��");
}
sub logdoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>ưʪ�ದ</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>ưʪ�ದ</B>��");
}
sub logdeukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>�ǥѡ��Ȳ�</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>�ǥѡ��Ȳ�</B>��");
}
sub logfoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>���Ӳ�</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>���Ӳ�</B>��");
}
sub logtoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>Ŵƻ��</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>Ŵƻ��</B>��");
}
sub logmoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>���Τ饭�顼��</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>���Τ饭�顼��</B>��");
}
sub logjoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>����첦</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>����첦</B>��");
}
sub loghoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>ȯ�Ų�</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>ȯ�Ų�</B>��");
}
sub loggoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>���߽����첦</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>���߽����첦</B>��");
}
sub logsoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>������</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>������</B>��");
}
sub logloukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>�쥸�㡼��</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>�쥸�㡼��</B>��");
}
sub logyoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>������</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>������</B>��");
}
sub logeoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>��Ⲧ</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>��Ⲧ</B>��");
}
sub logaoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>���Ѳ�</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>���Ѳ�</B>��");
}
sub logioukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>��Ͳ�</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>��Ͳ�</B>��");
}
sub logboukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>����</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>����</B>��");
}
sub loguoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>�η���</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>�η���</B>��");
}
# �޶�
sub logPzMoney {
my($id, $name, $pMoney) = @_;
logOut("${HtagName_}${name}��${H_tagName}�ˤϾ޶�Ȥ���<B>$pMoney$HunitMoney</B>���ٵ뤵��ޤ�����",$id);
}


# �礬���äѤ��ʾ��
sub tempNewIslandFull {
    out(<<END);
${HtagBig_}����������ޤ����礬���դ���Ͽ�Ǥ��ޤ��󡪡�${H_tagBig}$HtempBack
END
}

# ������̾�����ʤ����
sub tempNewIslandNoName {
    out(<<END);
${HtagBig_}��ˤĤ���̾����ɬ�פǤ���${H_tagBig}$HtempBack
END
}

# ������̾���������ʾ��
sub tempNewIslandBadName {
    out(<<END);
${HtagBig_}',?()<>\$'�Ȥ����äƤ��ꡢ��̵����פȤ����ä��Ѥ�̾���Ϥ��ޤ��礦���${H_tagBig}$HtempBack
END
}

# ���Ǥˤ���̾�����礬������
sub tempNewIslandAlready {
    out(<<END);
${HtagBig_}������ʤ餹�Ǥ�ȯ������Ƥ��ޤ���${H_tagBig}$HtempBack
END
}

# �ѥ���ɤ��ʤ����
sub tempNewIslandNoPassword {
    out(<<END);
${HtagBig_}�ѥ���ɤ�ɬ�פǤ���${H_tagBig}$HtempBack
END
}

# ���ȯ�����ޤ���!!
sub tempNewIslandHead {
    out(<<END);
<CENTER>
${HtagBig_}���ȯ�����ޤ�������${H_tagBig}<BR>
${HtagBig_}${HtagName_}��${HcurrentName}���${H_tagName}��̿̾���ޤ���${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
END
}

# �Ϸ��θƤ���
sub landName {
    my($land, $lv) = @_;
    if($land == $HlandSea) {
	if($lv == 1) {
            return '����';
        } else {
            return '��';
	}
    } elsif($land == $HlandWaste) {
if($lv == 2) {
return '����';
} else{
	return '����';
}
    } elsif($land == $HlandLake) {
	return '��';
    } elsif($land == $HlandPlains) {
	return 'ʿ��';
    } elsif($land == $HlandTown) {
	if($lv < 30) {
	    return '¼';
	} elsif($lv < 100) {
	    return 'Į';
	} else {
	    return '�Ի�';
	}
    } elsif($land == $HlandForest) {
	return '��';
    } elsif($land == $HlandFarm) {
	return '����';
    } elsif($land == $HlandBoku) {
	return '�Ҿ�';
    } elsif($land == $HlandGoyu) {
	return '����͢�е���';
    } elsif($land == $HlandFactory) {
	return '����';
    } elsif($land == $HlandBase) {
	return '�ߥ��������';
    } elsif($land == $HlandSefence){
	return '�����ɱһ���';
    } elsif($land == $HlandDefence) {
	if($lv < 2) {
	    return '�ɱһ���';
	} else {
	    return 'ST�ɱһ���';
	}
    } elsif($land == $HlandMountain) {
	return '��';
    } elsif($land == $HlandHatu) {
	return '����ȯ�Ž�';
  } elsif($land == $HlandChou) {
	return '����ȯ�Ž�';
 } elsif($land == $HlandSuiry) {
	return '����ȯ�Ž�';
 } elsif($land == $HcomTinet) {
	return '��Ǯȯ�Ž�';
    } elsif($land == $HlandGomi) {
	return '���߽�������';
    } elsif($land == $HlandMonster) {
	my($kind, $name, $hp) = monsterSpec($lv);
	return $name;
    } elsif($land == $Hlandhokak) {
	my($kind, $name, $hp) = monsterSpec($lv);
	return '$name������';
     } elsif($land == $HlandSbase) {
	return '�������';
     } elsif($land == $HlandPori) {
	return '�ٻ���';
  } elsif($land == $HlandShou) {
	return '���ɽ�';
     } elsif($land == $HlandInok) {
	return '���Τ鸦���';
     } elsif($land == $HlandOnpa) {
	return '�ü첻�Ȼ���';
    } elsif($land == $HlandOil) {
if($lv == 0) {
	return '��������';
}else {
return '�ܿ���';
}
    } elsif($land == $HlandMonument) {
	return $HmonumentName[$lv];
} elsif($land == $HlandStation) {
         if($lv < 100) {
             return '��ϩ';
         } else {
             return '��';
         }
    } elsif($land == $Hlandhos) {
return '�±�';
} elsif($land == $HlandLand) { 
if($lv == 0) {
return '�꥾���ȥۥƥ�';
}elsif($lv == 1) {
return '��²��';
}elsif($lv == 2) {
return '���⥹������';
}elsif($lv == 3) {
return '����';
}elsif($lv == 4) {
return '���å�������������';
}elsif($lv == 5) {
return '���Ͼ�';
}elsif($lv == 6) {
return '����վ�';
}elsif($lv == 7) {
return 'ͷ����';
}elsif($lv == 8) {
return 'Ÿ����';
}elsif($lv == 9) {
return '������';
}elsif($lv == 10) {
return '����';
}elsif($lv == 11) {
return '��ʪ��';
}elsif($lv == 12) {
return '��';
}elsif($lv == 13) {
return '��';
}
    } elsif($land == $Hlanddoubutu) {
	if($lv == 0) {
	    return '����';
	}elsif($lv == 1){
	    return 'ưʪ��';
	} elsif($lv == 2) {
	    return '�ǥѡ���';
	}
    } elsif($land == $HlandHaribote) {
	if($lv == 0) {
	    return '�ϥ�ܥ�';
	} else {
	    return '���';
	}

  } elsif($land == $HlandJirai) {
         if($lv ==0) {
              return '����';
         } elsif($lv == 1) {
             return '����ǽ����';
         } elsif($lv == 2) {
             return '�������';
}
}elsif($land == $Hlandkiken){
return '���ݸ����';
}elsif($land == $Hlandkishou){
return '���ݴ�¬��';
}elsif($land == $HlandJous){
return '�����';
}elsif($land == $HlandReho){
return '���«�졼����ˤ';
}elsif($land == $HlandBouh){
return '������';
}elsif($land == $HlandKoku){
return '���������';
}elsif($land == $HlandMina){
return '��';
}elsif($land == $HlandDenb){
return '�����������';
}elsif($land == $HlandJusi){
return '�ޥ������ȼ�������';
}elsif($land == $HlandEisei){
return '�������״�������';
}elsif($land == $HlandTaiy){
return '���۸�ȯ�Ž�';
}elsif($land == $HlandFuha){
return '����ȯ�Ž�';
}elsif($land == $Hlandkukou){
if($lv == 1) {
	    return '����';
	} else {
	    return '��ݶ���';
	}
}
}
# �͸�����¾���ͤ򻻽�
sub estimate {
    my($number) = $_[0];
    my($island);
    my($pop, $area, $farm, $factory, $mountain, $score,$kiken,$kishou,$kukou,$yousho,$onse,$dou,$dep,$miu,$hospit,$Onpa,$Inok,$Pori,$Jous,$hatu,$gomi,$jusi,$goyu,$boku,$mina,$denb,$gun,$seki,$lands,$forest,$stay,$Shou,$Den,$har,$def,$reh,$sei,$eki) = (0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);

    # �Ϸ������
    $island = $Hislands[$number];
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};

    # ������
    my($x, $y, $kind, $value);
    for($y = 0; $y < $HislandSize; $y++) {
	for($x = 0; $x < $HislandSize; $x++) {
	    $kind = $land->[$x][$y];
	    $value = $landValue->[$x][$y];
	    if(($kind != $HlandSea) &&
($kind != $HlandLake) &&
	       ($kind != $HlandSbase) &&
	       ($kind != $HlandOil)){
		$area++;
		if($kind == $HlandTown) {
		    # Į
		    $pop += $value;
		} elsif($kind == $HlandFarm) {
		    # ����
		    $farm += $value;
		} elsif($kind == $HlandFactory) {
		    # ����
		    $factory += $value;
		} elsif($kind == $HlandBase) {
		    # ����
		    $miu ++;
} elsif($kind == $HlandStation) {
if($value < 100) {
     $stay ++;
         } else {
$eki ++;
         }
	} elsif($kind == $HlandForest) {
		    # ����
		    $forest += $value;
		} elsif($kind == $HlandMountain) {
		    # ��
		    $mountain += $value;
} elsif(($kind == $HlandMonster) || ($kind == $Hlandhokak)){
$score += 1;
} elsif($kind == $Hlandkiken) {
$kiken += $value;
} elsif($kind == $HlandJous) {
$Jous += $value;
} elsif($kind == $HlandDenb) {
$denb += 1;
} elsif($kind == $Hlandkishou) {
$kishou += $value;
} elsif($kind == $HlandKoku) {
$gun += 1;
} elsif($kind ==$HlandDefence) {
$def ++;
} elsif($kind ==$HlandSefence) {
$def ++;
} elsif($kind ==$HlandReho){
$reh ++;
} elsif($kind ==$HlandEisei){
$sei ++;
} elsif($kind == $HlandPori) {
$Pori += $value;
} elsif($kind == $HlandShou) {
$Shou += 1;
} elsif($kind == $Hlandhos) {
$hospit += $value;
} elsif($kind == $HlandLand) {
$lands ++;
} elsif($kind == $HlandHatu) {
$Den += $value;
if($island->{'oifl'} == 0){
if($island->{'oil'} > $value){
$hatu += $value;
$island->{'oil'} -= $value;
}else{
$hatu += $island->{'oil'};
$island->{'oil'} = 0;
}
if(($island->{'oil'} == 0) && ($island->{'oif'} != 1)){
lognooil($island->{'id'}, $island->{'name'});
$island->{'oif'} = 1;
}
}else{
$hatu += $value;
}
} elsif($kind == $HlandBoku) {
$boku += $value;
} elsif($kind == $HlandTaiy) {
$hatu += $value;
$Den += $value;
} elsif($kind == $HlandFuha) {
$hatu += $value;
$Den += $value;
} elsif($kind == $HlandChou) {
$hatu += $value;
$Den += $value;
} elsif($kind == $HlandTinet) {
$hatu += $value;
$Den += $value;
} elsif($kind == $HlandSuiry) {
$hatu += $value;
$Den += $value;
} elsif($kind == $HlandGomi) {
$gomi += $value;
} elsif($kind == $HlandJusi) {
$jusi += $value;
} elsif($kind == $HlandGoyu) {
$goyu += $value;
} elsif($kind == $Hlandkukou) {
$kukou += $value;
} elsif($kind == $HlandMina) {
$har += 1;
if(countAround($land, $x, $y, $HlandSea, 5)){
$mina += $value;
}
} elsif($kind == $HlandOnpa) {
$Onpa += $value;
} elsif($kind == $HlandInok) {
$Inok += $value;
}elsif($kind == $Hlanddoubutu){
if ($value == 0){
$onse ++;
}elsif($value == 1){
$dou ++;
}else{
$dep ++;
}
}
}
if($kind == $HlandOil) {
if($value == 0){
$seki ++;
}else{
$yousho += $value;
}
}
if($kind == $HlandSbase) {
$miu ++;
}
	}
    }
$island->{'oifl'} = 1;
if(($island->{'hatei'} >0) ||($island->{'jusi'} >0)){
$hatu += $island->{'hatei'} * 100;
}

    # ����
    $island->{'pop'}      = $pop;
    $island->{'area'}     = $area;
    $island->{'farm'}     = $farm;
    $island->{'factory'}  = $factory;
    $island->{'mountain'} = $mountain;
$island->{'score'} = $score;
    $island->{'kiken'} = $kiken;
$island->{'kishou'} = $kishou;
$island->{'yousho'} =$yousho;
    $island->{'onse'} = $onse;
$island->{'dou'} = $dou;
$island->{'dep'} =$dep;
$island->{'miu'} =$miu;
$island->{'hospit'} =$hospit;
$island->{'Onpa'} =$Onpa;
$island->{'Inok'} =$Inok;
$island->{'Pori'} =$Pori;
$island->{'Jous'} =$Jous;
$island->{'hatud'} =$hatu;
$island->{'kukou'} =$kukou;
$island->{'gomi'} =$gomi;
$island->{'goyu'} =$goyu;
$island->{'boku'} =$boku;
$island->{'mina'} =$mina;
$island->{'denb'} =$denb;
$island->{'gun'} =$gun;
$island->{'sigoto'} =$farm + $factory + $mountain + $yousho + $boku;
$island->{'seki'} =$seki;
$island->{'lands'} =$lands;
$island->{'forest'} =$forest;
$island->{'stay'} =$stay;
$island->{'koukyo'} = ($Pori + $Shou + $hospit + $goyu + $gomi + $Jous) * 10;
$island->{'hatuden'} = $Den + (($denb + $jusi) * 10);
$island->{'nougyo'} = ($farm + $yousho + $boku) * 10;
$island->{'kouzan'} = ($mountain * 10) + ($seki * 100);
$island->{'koujyou'} = $factory * 10;
$island->{'gunji'} = ($gun + $miu + $def + $reh)* 10;
$island->{'tokushu'} = ($kiken + $kishou + $Onpa + $Inok + $sei)* 10;
$island->{'koutuu'} = ($har + $kukou + $eki) * 10;
$island->{'sonota'} = ($dep + $lands + $onse + $dou) * 10;
}


# �ϰ�����Ϸ��������
sub countAround {
    my($land, $x, $y, $kind, $range) = @_;
    my($i, $count, $sx, $sy);
    $count = 0;
    for($i = 0; $i < $range; $i++) {
	 $sx = $x + $ax[$i];
	 $sy = $y + $ay[$i];



	 if(($sx < 0) || ($sx >= $HislandSize) ||
	    ($sy < 0) || ($sy >= $HislandSize)) {
	     # �ϰϳ��ξ��
	     if($kind == $HlandSea) {
		 # ���ʤ�û�
		 $count++;
	     }
	 } else {
	     # �ϰ���ξ��
	     if($land->[$sx][$sy] == $kind) {
		 $count++;
	     }
	 }
    }
    return $count;
}

# 0����(n - 1)�ޤǤο��������ŤĽФƤ���������
sub randomArray {
    my($n) = @_;
    my(@list, $i);

    # �����
    if($n == 0) {
	$n = 1;
    }
    @list = (0..$n-1);

    # ����åե�
    for ($i = $n; --$i; ) {
	my($j) = int(rand($i+1));
	if($i == $j) { next; };
	@list[$i,$j] = @list[$j,$i];
    }

    return @list;
}

# ̾���ѹ�����
sub tempChangeNothing {
    out(<<END);
${HtagBig_}̾�����ѥ���ɤȤ�˶���Ǥ�${H_tagBig}$HtempBack
END
}

# ̾���ѹ����­�ꤺ
sub tempChangeNoMoney {
    out(<<END);
${HtagBig_}�����­�Τ����ѹ��Ǥ��ޤ���${H_tagBig}$HtempBack
END
}

# ̾���ѹ�����
sub tempChange {
    out(<<END);
${HtagBig_}�ѹ���λ���ޤ���${H_tagBig}$HtempBack
END
}
 sub logStationMoney {
     my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>���顢<B>$str</B>�μ��פ��夬��ޤ�����",$id);
  END
  }
1;
