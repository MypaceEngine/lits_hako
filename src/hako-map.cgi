#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �Ͽޥ⡼�ɥ⥸�塼��(ver1.00)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# LitsȢ���Ѳ�¤
# ��¤�ԡ�MT
# ������ץȤκ����ۤ϶ػߤ��ޤ���
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# �Ѹ��⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub printIslandMain {
    # ����
    unlock();

    # id�������ֹ�����
    $HcurrentNumber = $HidToNumber{$HcurrentID};

    # �ʤ��������礬�ʤ����
    if($HcurrentNumber eq '') {
	tempProblem();
unlock(); 
	return;
    }
$Hislands[$HcurrentNumber]->{'kanko'}++; # ��������
writeIslandskanko($HcurrentID);
# ����
unlock(); 
    # ̾���μ���
    $HcurrentName = $Hislands[$HcurrentNumber]->{'name'};
$kanko= $Hislands[$HcurrentNumber]->{'kanko'};
    # �Ѹ�����
    tempPrintIslandHead(); # �褦����!!
    islandInfo(); # ��ξ���
    islandMap(0); # ����Ͽޡ��Ѹ��⡼��
$ref = $ENV{'REMOTE_ADDR'};
$reb = $ENV{'REMOTE_HOST'};
$rec = $ENV{'HTTP_USER_AGENT'};
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
$rea = "$year/$mon/$mday $hour\:$min";
open(KLOG,">> doukana.log");
print KLOG "$rea . $ref . $reb . $rec\n";
close(KLOG);
    # �����������Ǽ���
    if($HuseLbbs) {
	tempLbbsHead();     # ������Ǽ���
	tempLbbsInput();   # �񤭹��ߥե�����
	tempLbbsContents(); # �Ǽ�������
    }

    # �ᶷ
    tempRecent(0);
}

#----------------------------------------------------------------------
# ��ȯ�⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub ownerMain {
    # ����
    unlock();

    # �⡼�ɤ�����
    $HmainMode = 'owner';

    # id����������
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # �ѥ����
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password�ְ㤤
	tempWrongPassword();
	return;
    }

    # ��ȯ����
    tempOwner(); # �ֳ�ȯ�ײ��

    # �����������Ǽ���
    if($HuseLbbs) {
	tempLbbsHead();     # ������Ǽ���
	tempLbbsInputOW();   # �񤭹��ߥե�����
	tempLbbsContents(); # �Ǽ�������
    }

    # �ᶷ
    tempRecent(1);
}
sub ownerMainb {
    # ����
    unlock();

    # �⡼�ɤ�����
    $HmainMode = 'owner';

    # id����������
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # ��ȯ����
    tempOwner(); # �ֳ�ȯ�ײ��

$ref = $ENV{'REMOTE_ADDR'};
$reb = $ENV{'REMOTE_HOST'};
$rec = $ENV{'HTTP_USER_AGENT'};
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
$rea = "$year/$mon/$mday $hour\:$min";
open(KLOG,">> doukana.log");
print KLOG "$rea . $ref . $reb . $rec\n";
close(KLOG);

    # �����������Ǽ���
    if($HuseLbbs) {
	tempLbbsHead();     # ������Ǽ���
	tempLbbsInputOW();   # �񤭹��ߥե�����
	tempLbbsContents(); # �Ǽ�������
    }

    # �ᶷ
    tempRecent(1);
}
#----------------------------------------------------------------------
# ���ޥ�ɥ⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub commandMain {
    # id����������
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # �ѥ����
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password�ְ㤤
	unlock();
	tempWrongPassword();
	return;
    }

    # �⡼�ɤ�ʬ��
    my($command) = $island->{'command'};

    if($HcommandMode eq 'delete') {
	slideFront($command, $HcommandPlanNumber);
	tempCommandDelete();
    } elsif(($HcommandKind == $HcomAutoPrepare) ||
	    ($HcommandKind == $HcomAutoPrepare2)) {
	# �ե����ϡ��ե��Ϥʤ餷
	# ��ɸ�������
	makeRandomPointArray();
	my($land) = $island->{'land'};

	# ���ޥ�ɤμ������
	my($kind) = $HcomPrepare;
	if($HcommandKind == $HcomAutoPrepare2) {
	    $kind = $HcomPrepare2;
	}

	my($i) = 0;
	my($j) = 0;
	while(($j < $HpointNumber) && ($i < $HcommandMax)) {
	    my($x) = $Hrpx[$j];
	    my($y) = $Hrpy[$j];
	    if($land->[$x][$y] == $HlandWaste) {
		slideBack($command, $HcommandPlanNumber);
		$command->[$HcommandPlanNumber] = {
		    'kind' => $kind,
		    'target' => 0,
		    'x' => $x,
		    'y' => $y,
		    'arg' => 0
		    };
		$i++;
	    }
	    $j++;
	}
	tempCommandAdd();
} elsif (($HcommandKind == $HcomReclaim2)||
	    ($HcommandKind == $HcomReclaim3)){
makeRandomPointArray();
my($land) = $island->{'land'};
my($kind) = $HcomReclaim;
	if($HcommandKind == $HcomReclaim3) {
	    $kind = $HcomUmeta;
	}
	my($i) = 0;
	my($j) = 0;
	while(($j < $HpointNumber) && ($i < $HcommandMax)) {
	    my($x) = $Hrpx[$j];
	    my($y) = $Hrpy[$j];
my($landValue) = $island->{'landValue'};
my($lv) = $landValue->[$x][$y];
	    if(($land->[$x][$y] == $HlandSea) && ($lv == 1)) {
		slideBack($command, $HcommandPlanNumber);
		$command->[$HcommandPlanNumber] = {
		    'kind' => $kind,
		    'target' => 0,
		    'x' => $x,
		    'y' => $y,
		    'arg' => 0
		    };
		$i++;
	    }
	    $j++;
	}
	tempCommandAdd();
    } elsif($HcommandKind == $HcomAutoDelete) {
	# ���ä�
	my($i);
	for($i = 0; $i < $HcommandMax; $i++) {
	    slideFront($command, $HcommandPlanNumber);
	}
	tempCommandDelete();
    } else {
	if($HcommandMode eq 'insert') {
	    slideBack($command, $HcommandPlanNumber);
	}
	tempCommandAdd();
	# ���ޥ�ɤ���Ͽ
	$command->[$HcommandPlanNumber] = {
	    'kind' => $HcommandKind,
	    'target' => $HcommandTarget,
	    'x' => $HcommandX,
	    'y' => $HcommandY,
	    'arg' => $HcommandArg
	    };
    }

    # �ǡ����ν񤭽Ф�
    writeIslandsrocal($HcurrentID);

    # owner mode��
    ownerMain();

}
sub ShuuMain {
    # id����������
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # �ѥ����
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password�ְ㤤
	unlock();
	tempWrongPassword();
	return;
    }
$koukyo = $island->{'koukyo'};
$hatuden = $island->{'hatuden'};
$nougyo = $island->{'nougyo'};
$kouzan = $island->{'kouzan'};
$koujyou = $island->{'koujyou'};
$gunji = $island->{'gunji'};
$tokushu = $island->{'tokushu'};
$koutuu = $island->{'koutuu'};
$sonota = $island->{'sonota'};
$aaa = $koukyo * $HparameterA / 100;
$bbb = $hatuden * $HparameterB / 100;
$ccc = $nougyo * $HparameterC / 100;
$ddd = $kouzan * $HparameterD / 100;
$eee = $koujyou * $HparameterE / 100;
$fff = $gunji * $HparameterF / 100;
$ggg = $tokushu * $HparameterG / 100;
$hhh = $koutuu * $HparameterH / 100;
$pop = $island->{'pop'};
if(($aaa + $bbb + $ccc + $ddd + $eee + $fff + $ggg + $hhh) < $pop){
$island->{'koukpase'} = $HparameterA;
$island->{'hatupase'} = $HparameterB;
$island->{'noupase'} = $HparameterC;
$island->{'kouzpase'} = $HparameterD;
$island->{'koujpase'} = $HparameterE;
$island->{'gunpase'} = $HparameterF;
$island->{'tokupase'} = $HparameterG;
$island->{'koutpase'} = $HparameterH;
}elsif(($aaa + $bbb + $ccc + $ddd + $eee + $fff + $ggg) < $pop){
if($koutuu > ($pop - ($aaa + $bbb + $ccc + $ddd + $eee + $fff + $ggg))){
$island->{'koutpase'} = int((($pop - ($aaa + $bbb + $ccc + $ddd + $eee + $fff + $ggg)) * 100)/$koutuu);
}else{
$island->{'koutpase'} = 100;
}
$island->{'koukpase'} = $HparameterA;
$island->{'hatupase'} = $HparameterB;
$island->{'noupase'} = $HparameterC;
$island->{'kouzpase'} = $HparameterD;
$island->{'koujpase'} = $HparameterE;
$island->{'gunpase'} = $HparameterF;
$island->{'tokupase'} = $HparameterG;

}elsif(($aaa + $bbb + $ccc + $ddd + $eee + $fff) < $pop){
if($tokushu > ($pop - ($aaa + $bbb + $ccc + $ddd + $eee + $fff))){
$island->{'tokupase'} = int((($pop - ($aaa + $bbb + $ccc + $ddd + $eee + $fff)) * 100)/$tokushu);
}else{
$island->{'tokupase'} = 100;
}
$island->{'koukpase'} = $HparameterA;
$island->{'hatupase'} = $HparameterB;
$island->{'noupase'} = $HparameterC;
$island->{'kouzpase'} = $HparameterD;
$island->{'koujpase'} = $HparameterE;
$island->{'gunpase'} = $HparameterF;
$island->{'koutpase'} = 0;

}elsif(($aaa + $bbb + $ccc + $ddd + $eee) < $pop){
if($gunji > ($pop - ($aaa + $bbb + $ccc + $ddd + $eee))){
$island->{'gunpase'} = int((($pop - ($aaa + $bbb + $ccc + $ddd + $eee)) * 100)/$gunji);
}else{
$island->{'gunpase'} = 100;
}
$island->{'koukpase'} = $HparameterA;
$island->{'hatupase'} = $HparameterB;
$island->{'noupase'} = $HparameterC;
$island->{'kouzpase'} = $HparameterD;
$island->{'koujpase'} = $HparameterE;
$island->{'tokupase'} = 0;
$island->{'koutpase'} = 0;

}elsif(($aaa + $bbb + $ccc + $ddd) < $pop){
if($koujyou > ($pop - ($aaa + $bbb + $ccc + $ddd))){
$island->{'koujpase'} = int((($pop - ($aaa + $bbb + $ccc + $ddd)) * 100)/$koujyou);
}else{
$island->{'koujpase'} = 100;
}
$island->{'koukpase'} = $HparameterA;
$island->{'hatupase'} = $HparameterB;
$island->{'noupase'} = $HparameterC;
$island->{'kouzpase'} = $HparameterD;
$island->{'gunpase'} = 0;
$island->{'tokupase'} = 0;
$island->{'koutpase'} = 0;

}elsif(($aaa + $bbb + $ccc) < $pop){
if($kouzan > ($pop - ($aaa + $bbb + $ccc))){
$island->{'kouzpase'} = int((($pop - ($aaa + $bbb + $ccc)) * 100)/$kouzan);
}else{
$island->{'kouzpase'} = 100;
}
$island->{'koukpase'} = $HparameterA;
$island->{'hatupase'} = $HparameterB;
$island->{'noupase'} = $HparameterC;
$island->{'koujpase'} = 0;
$island->{'gunpase'} = 0;
$island->{'tokupase'} = 0;
$island->{'koutpase'} = 0;

}elsif(($aaa + $bbb) < $pop){
if($nougyo > ($pop - ($aaa + $bbb))){
$island->{'noupase'} = int((($pop - ($aaa + $bbb))* 100)/$nougyo);
}else{
$island->{'noupase'} = 100;
}
$island->{'koukpase'} = $HparameterA;
$island->{'hatupase'} = $HparameterB;
$island->{'kouzpase'} = 0;
$island->{'koujpase'} = 0;
$island->{'gunpase'} = 0;
$island->{'tokupase'} = 0;
$island->{'koutpase'} = 0;

}elsif($aaa < $pop){
if($hatuden > ($pop - $aaa)){
$island->{'hatupase'} = int((($pop - $aaa)* 100)/$hatuden);
}else{
$island->{'hatupase'} = 100;
}
$island->{'koukpase'} = $HparameterA;
$island->{'noupase'} = 0;
$island->{'kouzpase'} = 0;
$island->{'koujpase'} = 0;
$island->{'gunpase'} = 0;
$island->{'tokupase'} = 0;
$island->{'koutpase'} = 0;

}else{
if($koukyo > ($pop - $aaa)){
$island->{'koukpase'} = int((($pop - $aaa) * 100)/$sonota);
}else{
$island->{'koukpase'} = 100;
}
$island->{'hatupase'} = 0;
$island->{'noupase'} = 0;
$island->{'kouzpase'} = 0;
$island->{'koujpase'} = 0;
$island->{'gunpase'} = 0;
$island->{'tokupase'} = 0;
$island->{'koutpase'} = 0;

}
    # �ǡ����ν񤭽Ф�
    writeIslandsshuu($HcurrentID);
    $HmainMode = 'owner';
    # owner mode��
    ownerMain();

}
#----------------------------------------------------------------------
# ���������ϥ⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub commentMain {
    # id����������
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # �ѥ����
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password�ְ㤤
	unlock();
	tempWrongPassword();
	return;
    }

    # ��å������򹹿�
    $island->{'comment'} = htmlEscape($Hmessage);

    # �ǡ����ν񤭽Ф�
    writeIslandscomment($HcurrentID);

    # �����ȹ�����å�����
    tempComment();

    # owner mode��
    ownerMain();
}

#----------------------------------------------------------------------
# ������Ǽ��ĥ⡼��
#----------------------------------------------------------------------
# �ᥤ��

sub localBbsMain {
    # id�������ֹ�����
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    my($foreignName);

    # �ʤ��������礬�ʤ����
    if($HcurrentNumber eq '') {
	unlock();
	tempProblem();
	return;
    }

    # ����⡼�ɤ���ʤ���̾������å��������ʤ����
    if($HlbbsMode != 2) {
	if(($HlbbsName eq '') || ($HlbbsName eq '')) {
	    unlock();
	    tempLbbsNoMessage();
	    return;
	}
    }

    # �Ѹ��ԥ⡼�ɤ���ʤ����ϥѥ���ɥ����å�
    if($HlbbsMode != 0) {
	if ($HlbbsMode == 3) {
	    # ����ԥ⡼��
	    my($foreignNumber) = $HidToNumber{$HforeignerID};
	    if ($foreignNumber eq '') {
		unlock();
		tempProblem();
		return;
	    }
	    my($foreignIsland) = $Hislands[$foreignNumber];
	    if (!checkPassword($foreignIsland->{'password'},$HinputPassword)) {
		unlock();
		tempWrongPassword();
		return;
	    }
	    $foreignName = $foreignIsland->{'name'};
	} else {
	    # ���⡼��
	    if(!checkPassword($island->{'password'},$HinputPassword)) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	    }
	}
    }

    my($lbbs);
    $lbbs = $island->{'lbbs'};

    # �⡼�ɤ�ʬ��
    if($HlbbsMode == 2) {
	# ����⡼��
	# ��å����������ˤ��餹
	slideBackLbbsMessage($lbbs, $HcommandPlanNumber);
	tempLbbsDelete();
    } else {
	# ��Ģ�⡼��
	# ��å���������ˤ��餹
	slideLbbsMessage($lbbs);

	# ��å������񤭹���
	my($message);
	if($HlbbsMode == 1) {
	    $message = '1';
	} else {
if($Hsee == 1){
	    $message = '5';
}else{
$message = '0';
}
	}
	if ($HlbbsMode == 3) {
	    $HlbbsName = "${HislandTurn} from ${foreignName}�硧" . htmlEscape($HlbbsName);
	} else {
	    $HlbbsName = "${HislandTurn}��" . htmlEscape($HlbbsName);
	}
	$HlbbsMessage = htmlEscape($HlbbsMessage);
	$lbbs->[0] = "$message>$HlbbsName>$HlbbsMessage";

	tempLbbsAdd();
    }

    # �ǡ����񤭽Ф�
    writeIslandsrocal($HcurrentID);

    # ��ȤΥ⡼�ɤ�
    if(($HlbbsMode == 1) || ($HlbbsMode == 2)) {
	ownerMain();
    } else {
	printIslandMain();
    }
}

# ������Ǽ��ĤΥ�å��������ĸ��ˤ��餹
sub slideLbbsMessage {
    my($lbbs) = @_;
    my($i);
#    pop(@$lbbs);
#    push(@$lbbs, $lbbs->[0]);
    pop(@$lbbs);
    unshift(@$lbbs, $lbbs->[0]);
}

# ������Ǽ��ĤΥ�å������������ˤ��餹
sub slideBackLbbsMessage {
    my($lbbs, $number) = @_;
    my($i);
    splice(@$lbbs, $number, 1);
    $lbbs->[$HlbbsMax - 1] = '0>>';
}

#----------------------------------------------------------------------
# ����Ͽ�
#----------------------------------------------------------------------

# �����ɽ��
sub islandInfo {
    my($island) = $Hislands[$HcurrentNumber];
    # ����ɽ��
    my($rank) = $HcurrentNumber + 1;
    my($farm) = $island->{'farm'};
    my($factory) = $island->{'factory'};
    my($mountain) = $island->{'mountain'};
    my($yousho) = $island->{'yousho'};
	$shoku = $island->{'shoku'};
my($Jous) = $island->{'Jous'};
$hatu = $island->{'hatud'};
$gomi = $island->{'gomi'};
$Oil = $island->{'oil'};
$boku = $island->{'boku'};
	$boku = ($boku == 0) ? "��ͭ����" : "${boku}0$HunitPop";
	$hatu = ($hatu == 0) ? "��ͭ����" : "${hatu}000Kw";
	$gomi = ($gomi == 0) ? "��ͭ����" : "${gomi}00�ȥ�";
	$Oil = ($Oil == 0) ? "��ͭ����" : "${Oil}�ȥ�";
	$shoku = ($shoku == 0) ? "��ͭ����" : "${shoku}00�ȥ�";
$yousho = ($yousho == 0) ? "��ͭ����" : "${yousho}0$HunitPop";
    $farm = ($farm == 0) ? "��ͭ����" : "${farm}0$HunitPop";
    $factory = ($factory == 0) ? "��ͭ����" : "${factory}0$HunitPop";
    $mountain = ($mountain == 0) ? "��ͭ����" : "${mountain}0$HunitPop";
$Jous = ($Jous == 0) ? "��ͭ����" : "${Jous}0000��";
my($ei) = "";
if ($island->{'kouei'} >= 1){
if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
$ei = "��٥�$island->{'kouei'}";
  } elsif($HhideMoneyMode == 2) {
$ei = "��ͭ��";
}
} else {
$ei = "��ͭ����";
}
my($ei2) = "";
if ($island->{'kanei'} >= 1){
if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
$ei2 = "��٥�$island->{'kanei'}";
 } elsif($HhideMoneyMode == 2) {
$ei2 = "��ͭ��";
}
}else {
$ei2 = "��ͭ����";
}
my($ei3) = "";
if ($island->{'bouei'} >= 1){
if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
$ei3 = "��٥�$island->{'bouei'}";
 } elsif($HhideMoneyMode == 2) {
$ei3 = "��ͭ��";
}
}else {
$ei3 = "��ͭ����";
}
my($ei4) = "";
if ($island->{'reiei'} >= 1){
if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
if ($island->{'reiei'} < 11){
$ei4 = "��٥�$island->{'reiei'}(���Ѳ�ǽ)";
}else{
my($res) = $island->{'reiei'} % 10;
my($rer) = int($island->{'reiei'} / 10);
if($res == 0){
$res = 10;
}
$ei4 = "��٥�$res(����$rer������)";
}
 } elsif($HhideMoneyMode == 2) {
$ei4 = "��ͭ��";
}
}else {
$ei4 = "��ͭ����";
}
my($ei6) = "";
if ($island->{'pmsei'} >= 1){
if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
if ($island->{'pmsei'} < 11){
$ei6 = "��٥�$island->{'pmsei'}(���Ѳ�ǽ)";
}else{
my($rei) = $island->{'pmsei'} % 10;
my($rea) = int($island->{'pmsei'} / 10);
if($res == 0){
$res = 10;
}
$ei6 = "��٥�$rei(����$rea������)";
}
 } elsif($HhideMoneyMode == 2) {
$ei6 = "��ͭ��";
}
}else {
$ei6 = "��ͭ����";
}
my($ei5) = "";
if ($island->{'hatei'} >= 1){
if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
$ei5 = "$island->{'hatei'}00000Kw";
 } elsif($HhideMoneyMode == 2) {
$ei5 = "��ͭ��";
}
}else {
$ei5 = "��ͭ����";
}
my($shuusi) = "";
if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
$shuusi = "$island->{'shuu'}$HunitMoney";
} elsif($HhideMoneyMode == 2) {
if($island->{'shuu'} < 0){
$shuusi = "�ֻ�";
}elsif($island->{'shuu'} == 0){
$shuusi = "0����";
}else{
$shuusi = "����";
}
}
my($shak) = "";
my($shau) = "";
if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
$shak = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}������${H_tagTH}</NOBR></TH>";
if($island->{'shaka'} > 0){
$shau = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'shamo'}��$island->{'shaka'}����</NOBR></TH>";
}else{
$shau = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>�ʤ�</NOBR></TH>";
}
}
my($shuu) = 0;
my($shuo) = "";
$shuu =int(($island->{'sigoto'} / $island->{'pop'}) * 1000);
if($shuu >= 100){
$shuo = "100��"
} else {
$shuo = "��$shuu��"
}
my($fStr) = '';
  if($island->{'flagname'} eq ''){
    $fStr = "";
  } else {
    $fStr = "<img src=$island->{'flagname'} width = 56 height = 42>";
  }
    my($mStr1) = '';
    my($mStr2) = '';
   my($kanke) = '';
    if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
	# ̵���ޤ���owner�⡼��
	$mStr1 = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>";
	$mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'money'}$HunitMoney</NOBR></TD>";
$island->{'ADDRE'} = "$ENV{'REMOTE_ADDR'}";
writeIslandsAddre($HcurrentID);
    } elsif($HhideMoneyMode == 2) {
	my($mTmp) = aboutMoney($island->{'money'});

	# 1000��ñ�̥⡼��
	$mStr1 = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>";
	$mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$mTmp</NOBR></TD>";
$kanke ="<br><center><b>���ʤ���$kanko���ܤ�ˬ��ԤǤ���</b></center>";
    }
    out(<<END);
<CENTER>
<table>
<left>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����Ψ${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����������${H_tagTH}</NOBR></TH><TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����������${H_tagTH}</NOBR></TH>
</TR>
<TR>
<TD $HbgNumberCell align=middle nowrap=nowrap><NOBR>${HtagNumber_}$rank${H_tagNumber}</NOBR></TD>
<TD $HbgNumberCell align=middle nowrap=nowrap><NOBR>$fStr</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'pop'}$HunitPop</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$shuo</NOBR></TD>
$mStr2
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'food'}$HunitFood</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'area'}$HunitArea</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'slag'}�ȥ�</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$Oil</NOBR></TD>
</tr>
</TABLE>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}��������μ���${H_tagTH}</NOBR></TH>
$shak
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����ȯ����${H_tagTH}</NOBR></TH><TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���߽������ߵ���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���翩����������${H_tagTH}</NOBR></TH></TR>
</TR>
<TR><TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$shuusi</NOBR></TD>
$shau
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$hatu</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$gomi</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${Jous}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$shoku</NOBR></TD></TR>
</TABLE>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH><TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�ܿ��쵬��${H_tagTH}</NOBR></TH><TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�Ҿ쵬��${H_tagTH}</NOBR></TH><TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�η��쵬��${H_tagTH}</NOBR></TH></tr>
<TR>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${farm}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${yousho}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${boku}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${factory}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${mountain}</NOBR></TD>
</tr>
</TABLE>
<TABLE BORDER><tr>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�ƻ����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�ɸ����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�졼��������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}PMS����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}ȯ�ű���${H_tagTH}</NOBR></TH>
</TR>
<tr>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$ei</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$ei2</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$ei3</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$ei4</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$ei6</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$ei5</NOBR></TD>
</TR>
</TABLE>
</left>
</TABLE></CENTER>
$kanke
<br>
END
}
sub islandShuu {
    my($island) = $Hislands[$HcurrentNumber];
    # ����ɽ��
$pop = $island->{'pop'};
$koukyo = $island->{'koukyo'};
$hatuden = $island->{'hatuden'};
$nougyo = $island->{'nougyo'};
$kouzan = $island->{'kouzan'};
$koujyou = $island->{'koujyou'};
$gunji = $island->{'gunji'};
$tokushu = $island->{'tokushu'};
$koutuu = $island->{'koutuu'};
$sonota = $island->{'sonota'};
$koukpase = $island->{'koukpase'};
$hatupase = $island->{'hatupase'};
$noupase = $island->{'noupase'};
$kouzpase = $island->{'kouzpase'};
$koujpase = $island->{'koujpase'};
$gunpase = $island->{'gunpase'};
$tokupase = $island->{'tokupase'};
$koutpase = $island->{'koutpase'};
$aaa = $koukyo * $koukpase;
$bbb = $hatuden * $hatupase;
$ccc = $nougyo * $noupase;
$ddd = $kouzan * $kouzpase;
$eee = $koujyou * $koujpase;
$fff = $gunji * $gunpase;
$ggg = $tokushu * $tokupase;
$hhh = $koutuu * $koutpase;
$goukei = $koukyo + $hatuden + $nougyo + $kouzan + $koujyou + $gunji + $tokushu + $koutuu + $sonota;
$sousuu = $aaa + $bbb + $ccc + $ddd + $eee + $fff + $ggg + $hhh;
$iii = ($pop * 100) - $sousuu;
if($iii > ($sonota * 100)){
$iii = $sonota * 100;
}
$sonopase = int($iii / $sonota);
$sousuu = $aaa + $bbb + $ccc + $ddd + $eee + $fff + $ggg + $hhh + $iii;
    out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}ȯ�ŷ�${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�ۻ���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�ü��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���̷�${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����¾${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
</TR>
<TR>
<TD $HbgNumberCell align=middle nowrap=nowrap><NOBR>${HtagTH_}���罢����ǽ�Ϳ�${H_tagTH}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$koukyo$HunitPop</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$hatuden$HunitPop</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$nougyo$HunitPop</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$kouzan$HunitPop</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$koujyou$HunitPop</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$gunji$HunitPop</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$tokushu$HunitPop</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$koutuu$HunitPop</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$sonota$HunitPop</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$goukei$HunitPop</NOBR></TD>
</tr>
<TR>
<TD $HbgNumberCell align=middle nowrap=nowrap><NOBR>${HtagTH_}���ߤγ�����ƿͿ�${H_tagTH}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$aaa��</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$bbb��</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$ccc��</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$ddd��</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$eee��</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$fff��</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$ggg��</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$hhh��</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$iii��</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$sousuu��</NOBR></TD>
</tr>
<TR>
<TD $HbgNumberCell align=middle nowrap=nowrap><NOBR>${HtagTH_}��ƯΨ${H_tagTH}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><SELECT NAME=paraa>
END

    # ����
    for($i = 0; $i < 101; $i++) {
if($i == $koukpase){
	out("<OPTION VALUE=$i SELECTED>$i\n");
}else{
	out("<OPTION VALUE=$i>$i\n");
}
    }

    out(<<END);
</SELECT>��</TD>
<TD $HbgInfoCell align=right nowrap=nowrap><SELECT NAME=parab>
END

    # ����
    for($i = 0; $i < 101; $i++) {
if($i == $hatupase){
	out("<OPTION VALUE=$i SELECTED>$i\n");
}else{
	out("<OPTION VALUE=$i>$i\n");
}
    }

    out(<<END);
</SELECT>��</TD>
<TD $HbgInfoCell align=right nowrap=nowrap><SELECT NAME=parac>
END

    # ����
    for($i = 0; $i < 101; $i++) {
if($i == $noupase){
	out("<OPTION VALUE=$i SELECTED>$i\n");
}else{
	out("<OPTION VALUE=$i>$i\n");
}
    }

    out(<<END);
</SELECT>��</TD>
<TD $HbgInfoCell align=right nowrap=nowrap><SELECT NAME=parad>
END

    # ����
    for($i = 0; $i < 101; $i++) {
if($i == $kouzpase){
	out("<OPTION VALUE=$i SELECTED>$i\n");
}else{
	out("<OPTION VALUE=$i>$i\n");
}
    }

    out(<<END);
</SELECT>��</TD>
<TD $HbgInfoCell align=right nowrap=nowrap><SELECT NAME=parae>
END

    # ����
    for($i = 0; $i < 101; $i++) {
if($i == $koujpase){
	out("<OPTION VALUE=$i SELECTED>$i\n");
}else{
	out("<OPTION VALUE=$i>$i\n");
}
    }

    out(<<END);
</SELECT>��</TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR><SELECT NAME=paraf>
END

    # ����
    for($i = 0; $i < 101; $i++) {
if($i == $gunpase){
	out("<OPTION VALUE=$i SELECTED>$i\n");
}else{
	out("<OPTION VALUE=$i>$i\n");
}
    }

    out(<<END);
</SELECT>��</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><SELECT NAME=parag>
END

    # ����
    for($i = 0; $i < 101; $i++) {
if($i == $tokupase){
	out("<OPTION VALUE=$i SELECTED>$i\n");
}else{
	out("<OPTION VALUE=$i>$i\n");
}
    }

    out(<<END);
</SELECT>��</TD>
<TD $HbgInfoCell align=right nowrap=nowrap><SELECT NAME=parah>
END

    # ����
    for($i = 0; $i < 101; $i++) {
if($i == $koutpase){
	out("<OPTION VALUE=$i SELECTED>$i\n");
}else{
	out("<OPTION VALUE=$i>$i\n");
}
    }

    out(<<END);
</SELECT>��</TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$sonopase��</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap></TD>
</tr>
</TABLE>
<B>�ѥ����</B>
<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE=submit VALUE="�ѹ�" NAME=ShuuButton$Hislands[$HcurrentNumber]->{'id'}>
</form>
</CENTER>
<hr>
END
}
# �Ͽޤ�ɽ��
# ������1�ʤ顢�ߥ�����������򤽤Τޤ�ɽ��
sub islandMap {
    my($mode) = @_;
    my($island);
    $island = $Hislands[$HcurrentNumber];

    out(<<END);
<CENTER><TABLE BORDER><TR><TD>
END
    # �Ϸ����Ϸ��ͤ����
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};
    my($l, $lv);

    # ���ޥ�ɼ���
    my($command) = $island->{'command'};
    my($com, @comStr, $i);
    if($HmainMode eq 'owner') {
	for($i = 0; $i < $HcommandMax; $i++) {
	    my($j) = $i + 1;
	    $com = $command->[$i];
	    if($com->{'kind'} < 1000) {
		$comStr[$com->{'x'}][$com->{'y'}] .=
		    " [${j}]$HcomName[$com->{'kind'}]";
	    }
	}
    }

    # ��ɸ(��)�����
    out("<IMG SRC=\"xbar.gif\" width=1008 height=16><BR>");

    # ���Ϸ�����Ӳ��Ԥ����
    my($x, $y);
    for($y = 0; $y < $HislandSize; $y++) {
	# �Ԥ��ֹ�����
	    out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");

	# ���Ϸ������
	for($x = 0; $x < $HislandSize; $x++) {
	    $l = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];
	    landString($l, $lv, $x, $y, $mode, $comStr[$x][$y]);
	}

	# ���Ԥ����
	out("<BR>");
    }
    out("</TD></TR></TABLE></CENTER>\n");
}

sub landString {
    my($l, $lv, $x, $y, $mode, $comStr) = @_;
    my($point) = "($x,$y)";
    my($image, $alt);

    if($l == $HlandSea) {

	if($lv == 1) {
	    # ����
	    $image = 'land14.gif';
	    $alt = '��(����)';
        } else {
            # ��
	    $image = 'land0.gif';
	    $alt = '��';
        }
    } elsif($l == $HlandWaste) {
	# ����
	if($lv == 1) {
	    $image = 'land13.gif'; # ������
	    $alt = '����';
} elsif($lv == 2){
	    $image = 'land36.gif'; # ������
	    $alt = '����';
	} else {
	    $image = 'land1.gif';
	    $alt = '����';
	}
    } elsif($l == $HlandPlains) {
	# ʿ��
	$image = 'land2.gif';
	$alt = 'ʿ��';
    } elsif($l == $HlandBouh) {
	# ʿ��
	$image = 'land40.gif';
	$alt = '������';
    } elsif($l == $HlandForest) {
	# ��
	if($mode == 1) {
	    $image = 'land6.gif';
	    $alt = "��(${lv}$HunitTree)";
	} else {
	    # �Ѹ��Ԥξ����ڤ��ܿ�����
	    $image = 'land6.gif';
	    $alt = '��';
	}
    } elsif($l == $HlandTown) {
	# Į
	my($p, $n);
	if($lv < 30) {
	    $p = 3;
	    $n = '¼';
	} elsif($lv < 100) {
	    $p = 4;
	    $n = 'Į';
	} else {
	    $p = 5;
	    $n = '�Ի�';
	}

	$image = "land${p}.gif";
	$alt = "$n(${lv}$HunitPop)";
    } elsif($l == $HlandFarm) {
	# ����
	$image = 'land7.gif';
	$alt = "����(${lv}0${HunitPop}����)";
 } elsif($l == $HlandShou) {
	# ����
	$image = 'land72.gif';
	$alt = "���ɽ�";
    } elsif($l == $HlandLake) {
if($lv == 2) {
$image = 'land71.gif';
	$alt = "�����";
}else{
	$image = 'land32.gif';
	$alt = "��";
}
} elsif($l == $Hlanddoubutu) { # �����ɲ�
if($lv == 0) {
	    # ����
	    $image = 'land22.gif';
	    $alt = '����';
}elsif($lv == 1) {
	    # ����
	    $image = 'land19.gif';
	    $alt = 'ưʪ��';
        } else {
            # ��
	    $image = 'land20.gif';
	    $alt = '�ǥѡ���';
}
} elsif($l == $HlandLand) { # �����ɲ�
if($lv == 0) {
	    # ����
	    $image = 'land54.gif';
	    $alt = '�꥾���ȥۥƥ�';
}elsif($lv == 1) {
	    # ����
	    $image = 'land53.gif';
	    $alt = '��²��';
}elsif($lv == 2) {
	    # ����
	    $image = 'land52.gif';
	    $alt = '���⥹������';
}elsif($lv == 3) {
	    # ����
	    $image = 'land51.gif';
	    $alt = '����';
}elsif($lv == 4) {
	    # ����
	    $image = 'land50.gif';
	    $alt = '���å�������������';
}elsif($lv == 5) {
	    # ����
	    $image = 'land49.gif';
	    $alt = '���Ͼ�';
}elsif($lv == 6) {
	    # ����
	    $image = 'land56.gif';
	    $alt = '����վ�';
}elsif($lv == 7) {
	    # ����
	    $image = 'land57.gif';
	    $alt = 'ͷ����';
}elsif($lv == 8) {
	    # ����
	    $image = 'land58.gif';
	    $alt = 'Ÿ����';
}elsif($lv == 9) {
	    # ����
	    $image = 'land59.gif';
	    $alt = '������';
}elsif($lv == 10) {
	    # ����
	    $image = 'land61.gif';
	    $alt = '����';
}elsif($lv == 11) {
	    # ����
	    $image = 'land62.gif';
	    $alt = '��ʪ��';
}elsif($lv == 12) {
	    # ����
	    $image = 'land63.gif';
	    $alt = '��';
}elsif($lv == 13) {
	    # ����
	    $image = 'land64.gif';
	    $alt = '��';
}
} elsif($l == $HlandStation) {
if($lv < 100) {
# ��ϩ
$image = 'senro.gif'; # ������Ϥβ�����ή��
$alt = "��ϩ(${lv})";
         } else {
             # ��
             $image = 'eki.gif'; # �������Ĥβ�����ή��
             $alt = "��(${lv})";
}
} elsif($l == $Hlandhos) {
$image = 'land29.gif';
$alt = '�±�';
} elsif($l == $HlandMina) {
$image = 'land41.gif';
$alt = '��';
} elsif($l == $HlandGoyu) {
$image = 'land45.gif';
$alt = '����͢�е���';
} elsif($l == $HlandBoku) {
$image = 'land46.gif';
$alt = "�Ҿ�(${lv}0${HunitPop}����)";
} elsif($l == $HlandTaiy) {
$image = 'land44.gif';
$alt = "���۸�ȯ�Ž�(${lv}000KW)";
} elsif($l == $HlandFuha) {
$image = 'land60.gif';
$alt = "����ȯ�Ž�(${lv}000KW)";
} elsif($l == $HlandSuiry) {
$image = 'land68.gif';
$alt = "����ȯ�Ž�(${lv}000KW)";
} elsif($l == $HlandTinet) {
$image = 'land69.gif';
$alt = "��Ǯȯ�Ž�(${lv}000KW)";
} elsif($l == $HlandChou) {
$image = 'land70.gif';
$alt = "����ȯ�Ž�(${lv}000KW)";
} elsif($l == $HlandJusi) {
$image = 'land42.gif';
$alt = '�ޥ������ȼ�������';
} elsif($l == $HlandEisei) {
$image = 'land73.gif';
$alt = '�������״�������';
} elsif($l == $HlandDenb) {
$image = 'land43.gif';
$alt = '�����������';
} elsif($l == $HlandJous) {
$image = 'land37.gif';
$alt = "�����(${lv}0000�ȵ���)";
} elsif($l == $Hlandkukou) { # �����ɲ�
if($lv == 1) {
	    # ����
	    $image = 'land25.gif';
	    $alt = '����';
}else {
	    # ����
	    $image = 'land26.gif';
	    $alt = '��ݶ���';
        }

    } elsif($l == $Hlandkiken) {
	# ����
if($mode == 0) {
$image = 'land6.gif';
$alt = '��';
} else {
	$image = 'land23.gif';
	$alt = "���ݸ����(������٥�:${lv})";
}
    } elsif($l == $Hlandkishou) {
	# ����
	$image = 'land24.gif';
	$alt = "���ݴ�¬��(������٥�:${lv})";
    } elsif($l == $HlandHatu) {
	# ����
	$image = 'land38.gif';
	$alt = "����ȯ�Ž�(${lv}000KW)";
    } elsif($l == $HlandGomi) {
	# ����
	$image = 'land39.gif';
	$alt = "���߽�������(${lv}00�ȥ�)";
    } elsif($l == $HlandFactory) {
	# ����
	$image = 'land8.gif';
	$alt = "����(${lv}0${HunitPop}����)";
    } elsif($l == $HlandBase) {
	if($mode == 0) {
	    # �Ѹ��Ԥξ��Ͽ��Τդ�
	    $image = 'land6.gif';
	    $alt = '��';
	} else {
	    # �ߥ��������
	    my($level) = expToLevel($l, $lv);
	    $image = 'land9.gif';
	    $alt = "�ߥ�������� (��٥� ${level}/�и��� $lv)";
	}
    } elsif($l == $HlandKoku) {
	if($mode == 0) {
	    # �Ѹ��Ԥξ��Ͽ��Τդ�
	    $image = 'land6.gif';
	    $alt = '��';
	} else {
	    # �ߥ��������
	    $image = 'land47.gif';
	    $alt = '���������';
	}
    } elsif($l == $HlandSbase) {
	# �������
	if($mode == 0) {
	    # �Ѹ��Ԥξ��ϳ��Τդ�
	    $image = 'land0.gif';
	    $alt = '��';
	} else {
	    my($level) = expToLevel($l, $lv);
	    $image = 'land12.gif';
	    $alt = "������� (��٥� ${level}/�и��� $lv)";
	}
    } elsif($l == $HlandDefence) {
if($lv < 2) {
	# �ɱһ���
	$image = 'land10.gif';
	$alt = '�ɱһ���';
} elsif($lv == 2){
if($mode == 0) {
# �Ѹ��Ԥξ��Ͽ��Τդ�
$image = 'land6.gif';
$alt = '��';
} else {
# ST�ɱһ���
$image = 'land10.gif';
$alt = 'ST�ɱһ���';
}
}
   } elsif($l == $HlandSefence) {
	# �ɱһ���
	$image = 'land30.gif';
	$alt = '�����ɱһ���';
   } elsif($l == $HlandReho) {
	# �ɱһ���
	$image = 'land48.gif';
	$alt = "���«�졼����ˤ(������٥�:${lv})";
   } elsif($l == $HlandOnpa) {
	# �ɱһ���
	$image = 'land33.gif';
	$alt = "�ü첻�Ȼ���(������٥�:${lv})";
   } elsif($l == $HlandInok) {
	# �ɱһ���
	$image = 'land34.gif';
	$alt = "���Τ鸦���(���ߥ�٥�:${lv})";
   } elsif($l == $HlandPori) {
	# �ɱһ���
	$image = 'land35.gif';
	$alt = '�ٻ���';
    } elsif($l == $HlandHaribote) {
if($lv == 0) {
	# �ϥ�ܥ�
	$image = 'land10.gif';
	if($mode == 0) {
	    # �Ѹ��Ԥξ����ɱһ��ߤΤդ�
	    $alt = '�ɱһ���';
	} else {
	    $alt = '�ϥ�ܥ�';
	}
} else {
if($mode == 0) {
# �Ѹ��Ԥξ��Ͽ��Τդ�
$image = 'land6.gif';
$alt = '��';
} else {
# ���
$image = 'land21.gif';
$alt = "���(����${lv}000��)";
}
}
     } elsif($l == $HlandJirai) {
if($lv ==0) {
         # ����
         if($mode == 0) {
             # �Ѹ��Ԥξ��Ͽ��Τդ�
	$image = 'land2.gif';
	$alt = 'ʿ��';
         } else {
             $image = 'land65.gif';
             $alt = '����';
         }
     } elsif($lv ==1) {
         # ����ǽ����
         if($mode == 0) {
             # �Ѹ��Ԥξ��Ͽ��Τդ�
  	$image = 'land2.gif';
	$alt = 'ʿ��';
         } else {
            $image = 'land66.gif';
          
   $alt = '����ǽ����';
}
          }elsif($lv ==2) {
         # ����ǽ����
         if($mode == 0) {
             # �Ѹ��Ԥξ��Ͽ��Τդ�
  	$image = 'land2.gif';
	$alt = 'ʿ��';
         } else {
            $image = 'land67.gif';
             $alt = '�������';
          }
}
    } elsif($l == $HlandOil) {
if($lv == 0) {
	# ��������
	$image = 'land16.gif';
	$alt = '��������';
}else{
	$image = 'land27.gif';
	$alt = "�ܿ���(${lv}0${HunitPop}����)";
}
    } elsif($l == $HlandMountain) {
	# ��
	my($str);
	$str = '';
	if($lv > 0) {
	    $image = 'land15.gif';
	    $alt = "��(�η���${lv}0${HunitPop}����)";
	} else {
	    $image = 'land11.gif';
	    $alt = '��';
	}
    } elsif($l == $HlandMonument) {
	# ��ǰ��
	$image = $HmonumentImage[$lv];
	$alt = $HmonumentName[$lv];
     } elsif($l == $Hlandhokak) {
	# ����
	my($kind, $name, $hp) = monsterSpec($lv);
	my($special) = $HmonsterSpecial[$kind];
	$image = $HmonsterImage[$kind];

	$alt = "���á��������$name(����${hp})";

   } elsif($l == $HlandMonster) {
	# ����
	my($kind, $name, $hp) = monsterSpec($lv);
	my($special) = $HmonsterSpecial[$kind];
	$image = $HmonsterImage[$kind];

	# �Ų���?
	if((($special == 3) && (($HislandTurn % 2) == 1)) ||
	   (($special == 4) && (($HislandTurn % 2) == 0))) {
	    # �Ų���
	    $image = $HmonsterImage2[$kind];
	}
	$alt = "����$name(����${hp})";
    }


    # ��ȯ���̤ξ��ϡ���ɸ����
    if($mode == 1) {
	out("<A HREF=\"JavaScript:void(0);\" onclick=\"ps($x,$y)\">");
    }

    out("<IMG SRC=\"$image\" ALT=\"$point $alt $comStr\" width=32 height=32 BORDER=0>");

    # ��ɸ�����Ĥ�
    if($mode == 1) {
	out("</A>");
    }
}


#----------------------------------------------------------------------
# �ƥ�ץ졼�Ȥ���¾
#----------------------------------------------------------------------
# ���̥�ɽ��
sub logPrintLocal {
    my($mode) = @_;
    my($i);
    for($i = 0; $i < $HlogMax; $i++) {
	logFilePrint($i, $HcurrentID, $mode);
    }
}

# ������ؤ褦��������
sub tempPrintIslandHead {
    out(<<END);
<CENTER>
${HtagBig_}${HtagName_}��${HcurrentName}���${H_tagName}�ؤ褦��������${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
END
}

# �����糫ȯ�ײ�
sub tempOwner {
    out(<<END);
<CENTER>
${HtagBig_}${HtagName_}${HcurrentName}��${H_tagName}��ȯ�ײ�${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
<SCRIPT Language="JavaScript">
<!--
END
if($Hnmo == 0){
    out(<<END);
function ps(x, y) {
    document.forms[0].elements[8].options[x].selected = true;
    document.forms[0].elements[9].options[y].selected = true;
    return true;
}
END
}else{
    out(<<END);
function ps(x, y) {
    document.forms[0].elements[28].options[x].selected = true;
    document.forms[0].elements[29].options[y].selected = true;
    return true;
}
END
}
   out(<<END);
function ns(x) {
    document.forms[0].elements[2].options[x].selected = true;
    return true;
}

//-->
</SCRIPT>
END
if($Hnmo == 0){
   out(<<END);
<SCRIPT language=JavaScript><!--
function DefOptions(){
  var i=0;
  this[i++] = new MyOptions1();
  this[i++] = new MyOptions2();
  this[i++] = new MyOptions3();
  this[i++] = new MyOptions4();
  this[i++] = new MyOptions5();
  this[i++] = new MyOptions6();
  this[i++] = new MyOptions7();
  this[i++] = new MyOptions8();
  this[i++] = new MyOptions9();
  this[i++] = new MyOptions10();
  this[i++] = new MyOptions11();
  this[i++] = new MyOptions12();
  this[i++] = new MyOptions13();
  this[i++] = new MyOptions14();
  this[i++] = new MyOptions15();
  this[i++] = new MyOptions16();
  this[i++] = new MyOptions17();
  this[i++] = new MyOptions18();
  this[i++] = new MyOptions19();
  this[i++] = new MyOptions20();
  this.length = i;
  return this;
}
function MyOptions1(){
  var i=0;
END
    my($kind, $cost, $s);
    for($i = 0; $i < $HcommandTotala; $i++) {
	$kind = $HcomLista[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}

	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
  this.length=i;
  return this;
}
function MyOptions2(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotalb; $i++) {
	$kind = $HcomListb[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
function MyOptions3(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotall; $i++) {
	$kind = $HcomListl[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
function MyOptions4(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotalm; $i++) {
	$kind = $HcomListm[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
function MyOptions5(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotaln; $i++) {
	$kind = $HcomListn[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
function MyOptions6(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotalo; $i++) {
	$kind = $HcomListo[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
function MyOptions7(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotalp; $i++) {
	$kind = $HcomListp[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
function MyOptions8(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotalq; $i++) {
	$kind = $HcomListq[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
function MyOptions9(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotalr; $i++) {
	$kind = $HcomListr[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
function MyOptions10(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotals; $i++) {
	$kind = $HcomLists[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
function MyOptions11(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotalt; $i++) {
	$kind = $HcomListt[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
function MyOptions12(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotalc; $i++) {
	$kind = $HcomListc[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
function MyOptions13(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotald; $i++) {
	$kind = $HcomListd[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
function MyOptions14(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotale; $i++) {
	$kind = $HcomListe[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
function MyOptions15(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotalf; $i++) {
	$kind = $HcomListf[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
function MyOptions16(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotalg; $i++) {
	$kind = $HcomListg[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
function MyOptions17(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotalh; $i++) {
	$kind = $HcomListh[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
function MyOptions18(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotali; $i++) {
	$kind = $HcomListi[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
function MyOptions19(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotalj; $i++) {
	$kind = $HcomListj[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
function MyOptions20(){
  var i=0;
END
    for($i = 0; $i < $HcommandTotalk; $i++) {
	$kind = $HcomListk[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	out("this[i++] = new MyOpt('$HcomName[$kind]($cost)',$kind);");
    }

    out(<<END);
 
  this.length=i;
  return this;
}
options   = new DefOptions();
loadedOpt = 0;
function MyOpt(text,value){
  this.text  = text;
  this.value = value;
}
function init(){
    document.f.r1[loadedOpt].checked=true;
    loadOption(document.f.COMMAND,document.f.r1[loadedOpt].value);
    showValue(document.f.COMMAND,document.f.tt,document.f.tv);
}
function showValue(so,tto,tvo){
  var o=so.options[so.selectedIndex];


}
// --></SCRIPT>

<SCRIPT language=JavaScript1.1><!--
function loadOption(obj,n){
    var ot = obj.options;
    var os = options[n];
    ot.length = os.length;
    for(var i=0; i<os.length; i++)
      ot[i] = new Option(os[i].text,os[i].value,false,false);
    ot.options[0].selected=true;
  loadedOpt = n;
}
// --></SCRIPT>
END
}

    islandInfo();

    out(<<END);
<CENTER>
<TABLE BORDER>
<TR>
<TD $HbgInputCell >
<CENTER>
<FORM action="$HthisFile" method=POST name=f>
<INPUT TYPE=submit VALUE="�ײ�����" NAME=CommandButton$Hislands[$HcurrentNumber]->{'id'}>
<HR>
<B>�ѥ����</B></BR>
<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<HR>
<B>�ײ��ֹ�</B><SELECT NAME=NUMBER>
END
    # �ײ��ֹ�
    my($j, $i);
    for($i = 0; $i < $HcommandMax; $i++) {
	$j = $i + 1;
	out("<OPTION VALUE=$i>$j\n");
    }

    out(<<END);
</SELECT><BR>
<HR>
<B>��ȯ�ײ�</B><BR>
END
if($Hnmo == 0){
    out(<<END);
<SELECT onchange=loadOption(form.COMMAND,this.value);showValue(form.COMMAND,form.tt,form.tv); onclick=loadOption(form.COMMAND,this.value);showValue(form.COMMAND,form.tt,form.tv); name=r1><OPTION value=0>���ù�����</OPTION>
END
if($HdefaultKindB == 1){
out("<OPTION value=1 SELECTED>���߷�</OPTION>\n");
}else{
out("<OPTION value=1>���߷�</OPTION>\n");
}
if($HdefaultKindB == 2){
out("<OPTION value=2 SELECTED> ��������������</OPTION>\n");
}else{
out("<OPTION value=2> ��������������</OPTION>\n");
}
if($HdefaultKindB == 3){
out("<OPTION value=3 SELECTED> �������ȷ�</OPTION>\n");
}else{
out("<OPTION value=3> �������ȷ�</OPTION>\n");
}
if($HdefaultKindB == 4){
out("<OPTION value=4 SELECTED> �����ۻ���</OPTION>\n");
}else{
out("<OPTION value=4> �����ۻ���</OPTION>\n");
}
if($HdefaultKindB == 5){
out("<OPTION value=5 SELECTED> ����ȯ�ŷ�</OPTION>\n");
}else{
out("<OPTION value=5> ����ȯ�ŷ�</OPTION>\n");
}
if($HdefaultKindB == 6){
out("<OPTION value=6 SELECTED> ����������</OPTION>\n");
}else{
out("<OPTION value=6> ����������</OPTION>\n");
}
if($HdefaultKindB == 7){
out("<OPTION value=7 SELECTED> �������̷�</OPTION>\n");
}else{
out("<OPTION value=7> �������̷�</OPTION>\n");
}
if($HdefaultKindB == 8){
out("<OPTION value=8 SELECTED> ����������</OPTION>\n");
}else{
out("<OPTION value=8> ����������</OPTION>\n");
}
if($HdefaultKindB == 9){
out("<OPTION value=9 SELECTED> �����ü��</OPTION>\n");
}else{
out("<OPTION value=9> �����ü��</OPTION>\n");
}
if($HdefaultKindB == 10){
out("<OPTION value=10 SELECTED> ��������¾</OPTION>\n");
}else{
out("<OPTION value=10> ��������¾</OPTION>\n");
}
if($HdefaultKindB == 11){
out("<OPTION value=11 SELECTED>�ǰ׷�</OPTION>\n");
}else{
out("<OPTION value=11>�ǰ׷�</OPTION>\n");
}
if($HdefaultKindB == 12){
out("<OPTION value=12 SELECTED>�����</OPTION>\n");
}else{
out("<OPTION value=12>�����</OPTION>\n");
}
if($HdefaultKindB == 13){
out("<OPTION value=13 SELECTED>�ߥ������</OPTION>\n");
}else{
out("<OPTION value=13>�ߥ������</OPTION>\n");
}
if($HdefaultKindB == 14){
out("<OPTION value=14 SELECTED>�����ɸ���</OPTION>\n");
}else{
out("<OPTION value=14>�����ɸ���</OPTION>\n");
}
if($HdefaultKindB == 15){
out("<OPTION value=15 SELECTED>������</OPTION>\n");
}else{
out("<OPTION value=15>������</OPTION>\n");
}
if($HdefaultKindB == 16){
out("<OPTION value=16 SELECTED>����ʼ���</OPTION>\n");
}else{
out("<OPTION value=16>����ʼ���</OPTION>\n");
}
if($HdefaultKindB == 17){
out("<OPTION value=17 SELECTED>Ʊ����</OPTION>\n");
}else{
out("<OPTION value=17>Ʊ����</OPTION>\n");
}
if($HdefaultKindB == 18){
out("<OPTION value=18 SELECTED>����¾</OPTION>\n");
}else{
out("<OPTION value=18>����¾</OPTION>\n");
}
if($HdefaultKindB == 19){
out("<OPTION value=19 SELECTED>��ư���Ϸ�</OPTION>\n");
}else{
out("<OPTION value=19>��ư���Ϸ�</OPTION>\n");
}
    out(<<END);
</SELECT>
<SELECT 
onchange=showValue(this,form.tt,form.tv); name=COMMAND> 
END
if($HdefaultKind == 0){
out("<OPTION value=41 selected>-------------------------------------<OPTION>\n");
}else{
	$cost = $HcomCost[$HdefaultKind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($HdefaultKind == 105) || ($HdefaultKind== 114)|| ($HdefaultKind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
out("<OPTION VALUE=$HdefaultKind selected>$HcomName[$HdefaultKind]($cost)</OPTION>\n");
}
out(<<END);
</SELECT><br>
<INPUT TYPE="radio" NAME="nmo" VALUE="iti" CHECKED><font sizu=2>Mode1</font><INPUT TYPE="radio" NAME="nmo" VALUE="nii"><font sizu=2>Mode2</font><INPUT TYPE="submit" VALUE="�⡼���ѹ�" NAME="ChangeMode$Hislands[$HcurrentNumber]->{'id'}"><BR>
END
}else{
if(($HcommandPoti == 1)||($HcommandPoti == 0)){
out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="zousei" CHECKED>���ù�����<br>
END
}else{
out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="zousei">���ù�����<br>
END
}
out(<<END);
<SELECT NAME=COMMANDa length="50">
END

    #���ޥ��
    my($kind, $cost, $s);
    for($i = 0; $i < $HcommandTotala; $i++) {
	$kind = $HcomLista[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	if($kind == $HdefaultKind) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}

	out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)</OPTION>\n");
    }

    out(<<END);
</SELECT><BR>
END
if($HcommandPoti == 2){
   out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="kensetu" CHECKED>���߷�<BR>
END
}else{
   out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="kensetu">���߷�<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDb>
END

    #���ޥ��

    for($i = 0; $i < $HcommandTotalb; $i++) {
	$kind = $HcomListb[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	if($kind == $HdefaultKind) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}

	out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n");
    }

    out(<<END);
</SELECT><BR>
END
if($HcommandPoti == 3){
   out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="boueki" CHECKED>�ǰ׷�<BR>
END
}else{
   out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="boueki">�ǰ׷�<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDc>
END

    #���ޥ��

    for($i = 0; $i < $HcommandTotalc; $i++) {
	$kind = $HcomListc[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	if($kind == $HdefaultKind) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}

	out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n");
    }

    out(<<END);
</SELECT><BR>
END
if($HcommandPoti == 4){
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="enjyo" CHECKED>�����<BR>
END
}else{
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="enjyo">�����<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDd>
END

    #���ޥ��

    for($i = 0; $i < $HcommandTotald; $i++) {
	$kind = $HcomListd[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	if($kind == $HdefaultKind) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}

	out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n");
    }

    out(<<END);
</SELECT><BR>
END
if($HcommandPoti == 5){
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="misairu" CHECKED>�ߥ������<BR>
END
}else{
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="misairu">�ߥ������<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDe>
END

    #���ޥ��

    for($i = 0; $i < $HcommandTotale; $i++) {
	$kind = $HcomListe[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	if($kind == $HdefaultKind) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}

	out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n");
    }

    out(<<END);
</SELECT><BR>
END
if($HcommandPoti == 6){
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="kaijyu" CHECKED>�����ɸ���<BR>
END
}else{
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="kaijyu">�����ɸ���<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDf>
END

    #���ޥ��

    for($i = 0; $i < $HcommandTotalf; $i++) {
	$kind = $HcomListf[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	if($kind == $HdefaultKind) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}

	out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n");
    }

    out(<<END);
</SELECT><BR>
END
if($HcommandPoti == 7){
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="eisei" CHECKED>������<BR>
END
}else{
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="eisei">������<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDg>
END

    #���ޥ��

    for($i = 0; $i < $HcommandTotalg; $i++) {
	$kind = $HcomListg[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	if($kind == $HdefaultKind) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}

	out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n");
    }

    out(<<END);
</SELECT><BR>
END
if($HcommandPoti == 8){
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="kishou" CHECKED>����ʼ���<BR>
END
}else{
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="kishou">����ʼ���<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDh>
END

    #���ޥ��

    for($i = 0; $i < $HcommandTotalh; $i++) {
	$kind = $HcomListh[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	if($kind == $HdefaultKind) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}

	out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n");
    }

    out(<<END);
</SELECT><BR>
END
if($HcommandPoti == 9){
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="doumei" CHECKED>Ʊ����<BR>
END
}else{
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="doumei">Ʊ����<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDi>
END

    #���ޥ��

    for($i = 0; $i < $HcommandTotali; $i++) {
	$kind = $HcomListi[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	if($kind == $HdefaultKind) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}

	out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n");
    }

    out(<<END);
</SELECT><BR>
END
if($HcommandPoti == 10){
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="sonota" CHECKED>����¾<BR>
END
}else{
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="sonota">����¾<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDj>
END

    #���ޥ��

    for($i = 0; $i < $HcommandTotalj; $i++) {
	$kind = $HcomListj[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	if($kind == $HdefaultKind) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}

	out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n");
    }

    out(<<END);
</SELECT><BR>
END
if($HcommandPoti == 11){
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="jidou" CHECKED>��ư���Ϸ�<BR>
END
}else{
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="jidou">��ư���Ϸ�<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDk>
END

    #���ޥ��
    for($i = 0; $i < $HcommandTotalk; $i++) {
	$kind = $HcomListk[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	if(($kind == 105) || ($kind == 114)|| ($kind == 131)){
	    $cost .= $HunitOil;
}else{
	    $cost .= $HunitMoney;
}
	}
	if($kind == $HdefaultKind) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}

	out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n");
    }
    out(<<END);
</SELECT><br>
<INPUT TYPE="radio" NAME="nmo" VALUE="iti"><font sizu=2>Mode1</font><INPUT TYPE="radio" NAME="nmo" VALUE="nii" CHECKED><font sizu=2>Mode2</font><INPUT TYPE="submit" VALUE="�⡼���ѹ�" NAME="ChangeMode$Hislands[$HcurrentNumber]->{'id'}"><BR>
END
}
out(<<END);
<HR>
<B>��ɸ(</B>
<SELECT NAME=POINTX>

END
    for($i = 0; $i < $HislandSize; $i++) {
	if($i == $HdefaultX) {
	    out("<OPTION VALUE=$i SELECTED>$i\n");
        } else {
	    out("<OPTION VALUE=$i>$i\n");
        }
    }

    out(<<END);
</SELECT>, <SELECT NAME=POINTY>
END

    for($i = 0; $i < $HislandSize; $i++) {
	if($i == $HdefaultY) {
	    out("<OPTION VALUE=$i SELECTED>$i\n");
        } else {
	    out("<OPTION VALUE=$i>$i\n");
        }
    }
    out(<<END);
</SELECT><B>)</B>
<HR>
<B>����</B><SELECT NAME=AMOUNT>
END

    # ����
    for($i = 0; $i < 999; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>
<HR>
<B>��ɸ����</B><BR>
<SELECT NAME=TARGETID>
$HtargetList<BR>
</SELECT>
<HR>
<B>ư��</B><BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=insert CHECKED>����
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=write>���<BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=delete>���
<HR>
<INPUT TYPE=submit VALUE="�ײ�����" NAME=CommandButton$Hislands[$HcurrentNumber]->{'id'}>

</CENTER>
</FORM>
</TD>
<TD $HbgMapCell>
END
    islandMap(1);    # ����Ͽޡ���ͭ�ԥ⡼��
    out(<<END);
</TD>
<TD $HbgCommandCell>
END
    for($i = 0; $i < $HcommandMax; $i++) {
	tempCommand($i, $Hislands[$HcurrentNumber]->{'command'}->[$i]);
    }

    out(<<END);

</TD>
</TR>
</TABLE>
</CENTER>
<HR>
<CENTER>
${HtagBig_}�����ȹ���${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
������<INPUT TYPE=text NAME=MESSAGE SIZE=80><BR>
�ѥ����<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE=submit VALUE="�����ȹ���" NAME=MessageButton$Hislands[$HcurrentNumber]->{'id'}>
</FORM>
</CENTER>
END

}

# ���ϺѤߥ��ޥ��ɽ��
sub tempCommand {
    my($number, $command) = @_;
    my($kind, $target, $x, $y, $arg) =
	(
	 $command->{'kind'},
	 $command->{'target'},
	 $command->{'x'},
	 $command->{'y'},
	 $command->{'arg'}
	 );
    my($name) = "$HtagComName_${HcomName[$kind]}$H_tagComName";
    my($point) = "$HtagName_($x,$y)$H_tagName";
    $target = $HidToName{$target};
    if($target eq '') {
	$target = "̵��";
    }
    $target = "$HtagName_${target}��$H_tagName";
    my($value) = $arg * $HcomCost[$kind];
    if($value == 0) {
	$value = $HcomCost[$kind];
    }
    if($value < 0) {
	$value = -$value;
	$value = "$value$HunitFood";
    } else {
if(($kind == 105) || ($kind == 114) || ($kind == 131)){
	$value = "$value$HunitOil";
}else{
	$value = "$value$HunitMoney";
}
}

    $value = "$HtagName_$value$H_tagName";

    my($j) = sprintf("%02d��", $number + 1);

    out("<A STYlE=\"text-decoration:none\" HREF=\"JavaScript:void(0);\" onClick=\"ns($number)\"><NOBR>$HtagNumber_$j$H_tagNumber<FONT COLOR=\"$HnormalColor\">");

    if(($kind == $HcomDoNothing) ||
       ($kind == $HcomGiveup)) {
	out("$name");
    } elsif(($kind == $HcomMissileNM) ||
	    ($kind == $HcomMissilePP) ||
	    ($kind == $HcomMissileST) ||
	    ($kind == $HcomMissileLD) ||
($kind == $HcomMissileUC) ||
($kind == $HcomMissileMK) ||
($kind == $HcomMissileEM) ||
($kind == $HcomMissileNC) ||
($kind == $HcomMissileHP) ||
($kind == $HcomMissileUB) ||
($kind == $HcomRazer) ||
($kind == $HcomPMS) ||
($kind == $HcomMissileNEB) ||
($kind == $HcomMissileRE)) {
	# �ߥ������
	my($n) = ($arg == 0 ? '̵����' : "${arg}ȯ");
	out("$target$point��$name($HtagName_$n$H_tagName)");
    } elsif (($kind == $HcomSendMonster) ||
($kind == $HcomSendMonster3) || 
($kind == $HcomSendMonster4) || 
($kind == $HcomSendMonster5) || 
($kind == $HcomSendMonster2)){
	# �����ɸ�
	out("$target��$name");
    } elsif($kind == $HcomSell) {
	# ����͢��
	out("$name$value");
    } elsif($kind == $HcomImport) {
# ����͢��
out("$name$value");
    } elsif($kind == $HcomOilSell) {
	# ����͢��
	out("$name$value");
    } elsif($kind == $HcomOilImport) {
# ����͢��
out("$name$value");

} elsif($kind == $HcomPropaganda) {
	# Ͷ�׳�ư
	out("$name");
if($arg != 0){
    out("($arg��)");
}


  } elsif(($kind == $HcomRob) || ($kind == $HcomRobST)){
    my($rateRob, $buf);
    if($kind == $HcomRob){
      $rateRob = int((100 - $arg) / 2);
    } else {
      $rateRob = int((100 - $arg) / 3);
    }
    out("$target��$name(������Ψ ��$rateRob%)");
  } elsif(($kind == $HcomShakufi) ||($kind == $HcomShakuse) || ($kind == $HcomShakuth)){
my($kane);
$kane = $arg * 100;
out("$name($kane����)");
    } elsif(($kind == $HcomMoney) ||
($kind == $HcomMoneyH) ||
($kind == $HcomFoodH) ||
($kind == $HcomSlag) ||
	    ($kind == $HcomFood)) {
	# ���
	out("$target��$name$value");
    } elsif($kind == $HcomDestroy) {
	# ����
	if($arg != 0) {
	    out("$point��$name(ͽ��${value})");
	} else {
	    out("$point��$name");
	}
}elsif(($kind == $HcomOilH) ||
($kind == $HcomOil)){
	out("$target��$name$value");
    } elsif(($kind == $HcomFarm) ||
	     ($kind == $HcomFactory) ||
($kind == $HcomBank) ||
($kind == $Hcomkiken) ||
($kind == $Hcomkishou) ||
($kind == $Hcomyousho)||
($kind == $HcomOnpa)||
($kind == $HcomInok)||
($kind == $HcomChou)||
($kind == $HcomTinet)||
($kind == $HcomSuiry)||
($kind == $HcomJous)||
($kind == $HcomHatu)||
($kind == $HcomFuha)||
($kind == $HcomGomi)||
($kind == $HcomTaiy)||
($kind == $HcomBoku)||
($kind == $HcomReho)||
	     ($kind == $HcomMountain)) {	
	# ����դ�
	if($arg == 0) {
	    out("$point��$name");
	} else {
	    out("$point��$name($arg��)");
	}
    } elsif(($kind == $Hcomkouei)||
($kind == $Hcombouei)||
($kind == $Hcomreiei)||
($kind == $Hcomhatei)||
($kind == $HcomPMSei)||
($kind == $Hcomkanei)){
out("$name");
} elsif($kind == $Hcomtimya){
out("$target$point��$name");
} elsif(($kind == $Hcomtaifuu)||
($kind == $Hcomtunami)||
($kind == $Hcomfunka)||
($kind == $Hcominseki)||
($kind == $Hcomdaiinseki)||
($kind == $Hcomjisin)||
($kind == $HcomOoame)||
($kind == $Hcomkasai)||
($kind == $Hcomjibantinka)){
out("$target�˸�����$name");
} elsif($kind == $Hcomkouuti){
out("$target�ι�������򹶷�");
} elsif($kind == $Hcombouuti){
out("$target���ɸ�����򹶷�");
} elsif($kind == $Hcomreiuti){
out("$target�Υ졼���������򹶷�");
}elsif($kind == $Hcomkanuti){
out("$target�δƻ�����򹶷�");
}elsif($kind == $HcomPMSuti){
out("$target��PMS�����򹶷�");
}elsif(($kind == $Hcomsennyu)||
($kind == $Hcomheinyu)||
($kind == $Hcominonyu)||
($kind == $Hcomsende)||
($kind == $Hcomheide)||
($kind == $Hcominode)||
($kind == $HcomGeki)||
($kind == $Hcomteikou)){
out("$name");
}else {
	# ��ɸ�դ�
	out("$point��$name");
    }

    out("</FONT></NOBR></A><BR>");
}

# ������Ǽ���
sub tempLbbsHead {
    out(<<END);
<HR>
<CENTER>
${HtagBig_}${HtagName_}${HcurrentName}��${H_tagName}�Ѹ����̿�${H_tagBig}<BR>
</CENTER>
END
}

# ������Ǽ������ϥե�����
sub tempLbbsInput {
    if ($HlbbsAuth) {
	out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH>̾��</TH>
<TH>����</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD><TEXTAREA NAME="LBBSMESSAGE" ROWS=2 COLS=60></TEXTAREA></TD>
</TR>
<TR>
<TD colspan="2">��ʬ���硧<SELECT NAME="ISLANDID">$HislandList</SELECT>
���ѥ���ɡ�<INPUT TYPE="password" SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword"><INPUT TYPE="radio" NAME="see" VALUE="public" CHECKED>����
<INPUT TYPE="radio" NAME="see" VALUE="secret">����<br>
<INPUT TYPE="submit" VALUE="��Ģ����" NAME="LbbsButtonFO$HcurrentID">

</TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
    }

    if ($HlbbsGuest) {
	out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH>̾��</TH>
<TH>����</TH>
<TH>ư��</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD><TEXTAREA NAME="LBBSMESSAGE" ROWS=2 COLS=60></TEXTAREA></TD>
<TD><INPUT TYPE="radio" NAME="see" VALUE="public" CHECKED>����
<INPUT TYPE="radio" NAME="see" VALUE="secret">����<br><INPUT TYPE="submit" VALUE="��Ģ����" NAME="LbbsButtonSS$HcurrentID">
</TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
    }
}

# ������Ǽ������ϥե����� owner mode��
sub tempLbbsInputOW {
    out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH>̾��</TH>
<TH COLSPAN=2>����</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD COLSPAN=2>
<TEXTAREA NAME="LBBSMESSAGE" ROWS=2 COLS=60></TEXTAREA></TD>
</TR>
<TR>
<TH>�ѥ����</TH>
<TH COLSPAN=2>ư��</TH>
</TR>
<TR>
<TD><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword"></TD>
<TD align=right>
<INPUT TYPE="submit" VALUE="��Ģ����" NAME="LbbsButtonOW$HcurrentID">
</TD>
<TD align=right>
�ֹ�
<SELECT NAME=NUMBER>
END
    # ȯ���ֹ�
    my($j, $i);
    for($i = 0; $i < $HlbbsMax; $i++) {
	$j = $i + 1;
	out("<OPTION VALUE=$i>$j\n");
    }
    out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="�������" NAME="LbbsButtonDL$HcurrentID">
</TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
}

# ������Ǽ�������
sub tempLbbsContents {
    my($lbbs, $line);
    $lbbs = $Hislands[$HcurrentNumber]->{'lbbs'};
    out(<<END);
<CENTER>
<TABLE BORDER>
<TR>
<TH>�ֹ�</TH>
<TH>��Ģ����</TH>
</TR>
END

    my($i);
    for($i = 0; $i < $HlbbsMax; $i++) {
	$line = $lbbs->[$i];
	if($line =~ /([0-9]*)\>(.*)\>(.*)$/) {
	    my($j) = $i + 1;
	    out("<TR><TD align=center>$HtagNumber_$j$H_tagNumber</TD>");

                if ($1 == 5) {
                    # ����
if($HmainMode ne 'owner'){
                    out("<TD><center>$HtagLbbsXX_ *** ���� ***$H_tagLbbsXX</center></TD></TR>");
                } else {

                    out("<TD>$HtagLbbsXX_ $2 > $3$H_tagLbbsXX</TD></TR>");
                }
}elsif($1 == 0) {
                # �Ѹ���
out("<TD>$HtagLbbsSS_$2 > $3$H_tagLbbsSS</TD></TR>");
	    } else {
		# ���
		out("<TD>$HtagLbbsOW_$2 > $3$H_tagLbbsOW</TD></TR>");
	    }
	}
    }

    out(<<END);
</TD></TR></TABLE></CENTER>
END
}

# ������Ǽ��Ĥ�̾������å��������ʤ����
sub tempLbbsNoMessage {
    out(<<END);
${HtagBig_}̾���ޤ������Ƥ��󤬶���Ǥ���${H_tagBig}$HtempBack
END
}

# �񤭤��ߺ��
sub tempLbbsDelete {
    out(<<END);
${HtagBig_}��Ģ���Ƥ������ޤ���${H_tagBig}<HR>
END
}

# ���ޥ����Ͽ
sub tempLbbsAdd {
    out(<<END);
${HtagBig_}��Ģ��Ԥ��ޤ���${H_tagBig}<HR>
END
}

# ���ޥ�ɺ��
sub tempCommandDelete {
    out(<<END);
${HtagBig_}���ޥ�ɤ������ޤ���${H_tagBig}<HR>
END
}

# ���ޥ����Ͽ
sub tempCommandAdd {
    out(<<END);
${HtagBig_}���ޥ�ɤ���Ͽ���ޤ���${H_tagBig}<HR>
END
}

# �������ѹ�����
sub tempComment {
    out(<<END);
${HtagBig_}�����Ȥ򹹿����ޤ���${H_tagBig}<HR>
END
}

# �ᶷ
sub tempRecent {
    my($mode) = @_;
    out(<<END);
<HR>
${HtagBig_}${HtagName_}${HcurrentName}��${H_tagName}�ζᶷ${H_tagBig}<BR>
END
    logPrintLocal($mode);
}

1;
