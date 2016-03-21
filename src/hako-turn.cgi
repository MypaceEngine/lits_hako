#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# ターン進行モジュール(ver1.02)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Lits箱庭用改造
# 改造者：MT
# スクリプトの再配布は禁止します。
#----------------------------------------------------------------------

#周囲2ヘックスの座標
my(@ax) = (0,-1, 1, 0, 0,-2,-1, 0, 1, 2, 1, 0,-1, 0, 1, 2, 3, 2, 1, 0,-1,-2,-3, -2,-1);
my(@ay) = (0, 0, 0, 1,-1, 0, 1, 2, 1, 0,-1,-2,-1, 3, 2, 1, 0,-1,-2,-3,-2,-1, 0,  1, 2);

#----------------------------------------------------------------------
# 島の新規作成モード
#----------------------------------------------------------------------
# メイン
sub newIslandMain {
    # 島がいっぱいでないかチェック
    if($HislandNumber >= $HmaxIsland) {
	unlock();
	tempNewIslandFull();
	return;
    }

    # 名前があるかチェック
    if($HcurrentName eq '') {
	unlock();
	tempNewIslandNoName();
	return;
    }

    # 名前が正当かチェック
    if($HcurrentName =~ /[,\?\(\)\<\>\$]|^無人$/) {
	# 使えない名前
	unlock();
	tempNewIslandBadName();
	return;
    }

    # 名前の重複チェック
    if(nameToNumber($HcurrentName) != -1) {
	# すでに発見ずみ
	unlock();
	tempNewIslandAlready();
	return;
    }

    # passwordの存在判定
    if($HinputPassword eq '') {
	# password無し
	unlock();
	tempNewIslandNoPassword();
	return;
    }

    # 確認用パスワード
    if($HinputPassword2 ne $HinputPassword) {
	# password間違い
	unlock();
	tempWrongPassword();
	return;
    }

    # 新しい島の番号を決める
    $HcurrentNumber = $HislandNumber;
    $HislandNumber++;
    $Hislands[$HcurrentNumber] = makeNewIsland();
    my($island) = $Hislands[$HcurrentNumber];

    # 各種の値を設定
    $island->{'name'} = $HcurrentName;
    $island->{'id'} = $HislandNextID;
    $HislandNextID ++;
    $island->{'absent'} = $HgiveupTurn - 3;
    $island->{'comment'} = '(未登録)';
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

    # 人口その他算出
    estimate($HcurrentNumber);

    # データ書き出し
    writeIslandsFile($island->{'id'});
    logDiscover($HcurrentName); # ログ

    # 開放
    unlock();

    # 発見画面
    tempNewIslandHead($HcurrentName); # 発見しました!!
    islandInfo(); # 島の情報
    islandMap(1); # 島の地図、ownerモード
}

# 新しい島を作成する
sub makeNewIsland {
    # 地形を作る
    my($land, $landValue) = makeNewLand();

    # 初期コマンドを生成
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

    # 初期掲示板を作成
    my(@lbbs);
    for($i = 0; $i < $HlbbsMax; $i++) {
	 $lbbs[$i] = "0>>";
    }

    # 島にして返す
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

# 新しい島の地形を作成する
sub makeNewLand {
    # 基本形を作成
    my(@land, @landValue, $x, $y, $i);

    # 海に初期化
    for($y = 0; $y < $HislandSize; $y++) {
	 for($x = 0; $x < $HislandSize; $x++) {
	     $land[$x][$y] = $HlandSea;
	     $landValue[$x][$y] = 0;
	 }
    }

    # 中央の4*4に荒地を配置
    my($center) = $HislandSize / 2 - 1;
    for($y = $center - 1; $y < $center + 3; $y++) {
	 for($x = $center - 1; $x < $center + 3; $x++) {
	     $land[$x][$y] = $HlandWaste;
	 }
    }

    # 8*8範囲内に陸地を増殖
    for($i = 0; $i < 120; $i++) {
	 # ランダム座標
	 $x = random(6) + $center - 3;
	 $y = random(6) + $center - 3;

	 my($tmp) = countAround(\@land, $x, $y, $HlandSea, 5);
	 if(countAround(\@land, $x, $y, $HlandSea, 5) != 5){
	     # 周りに陸地がある場合、浅瀬にする
	     # 浅瀬は荒地にする
	     # 荒地は平地にする
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

    # 森を作る
    my($count) = 0;
    while($count < 4) {
	 # ランダム座標
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # そこがすでに森でなければ、森を作る
	 if($land[$x][$y] != $HlandForest) {
	     $land[$x][$y] = $HlandForest;
	     $landValue[$x][$y] = 5; # 最初は500本
	     $count++;
	 }
    }

    # 町を作る
    $count = 0;
    while($count < 2) {
	 # ランダム座標
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # そこが森か町でなければ、町を作る
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest)) {
	     $land[$x][$y] = $HlandTown;
	     $landValue[$x][$y] = 5; # 最初は500人
	     $count++;
	 }
    }

    # 山を作る
    $count = 0;
    while($count < 1) {
	 # ランダム座標
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # そこが森か町でなければ、町を作る
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest)) {
	     $land[$x][$y] = $HlandMountain;
	     $landValue[$x][$y] = 0; # 最初は採掘場なし
	     $count++;
	 }
    }

    # 基地を作る
    $count = 0;
    while($count < 1) {
	 # ランダム座標
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # そこが森か町か山でなければ、基地
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
# 情報変更モード
#----------------------------------------------------------------------
# メイン
sub changeMain {
    # idから島を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    my($flag) = 0;

    # パスワードチェック
    if($HoldPassword eq $HspecialPassword) {
	# 特殊パスワード
	$island->{'money'} = 9999;
	$island->{'food'} = 9999;
    } elsif(!checkPassword($island->{'password'},$HoldPassword)) {
	# password間違い
	unlock();
	tempWrongPassword();
	return;
    }

    # 確認用パスワード
    if($HinputPassword2 ne $HinputPassword) {
	# password間違い
	unlock();
	tempWrongPassword();
	return;
    }

    if($HcurrentName ne '') {
	# 名前変更の場合	
	# 名前が正当かチェック
	if($HcurrentName =~ /[,\?\(\)\<\>]|^無人$/) {
	    # 使えない名前
	    unlock();
	    tempNewIslandBadName();
	    return;
	}

	# 名前の重複チェック
	if(nameToNumber($HcurrentName) != -1) {
	    # すでに発見ずみ
	    unlock();
	    tempNewIslandAlready();
	    return;
	}

	if($island->{'money'} < $HcostChangeName) {
	    # 金が足りない
	    unlock();
	    tempChangeNoMoney();
	    return;
	}

	# 代金
	if($HoldPassword ne $HspecialPassword) {
	    $island->{'money'} -= $HcostChangeName;
$island->{'shuu'}-= $HcostChangeName;
	}

	# 名前を変更
	logChangeName($island->{'name'}, $HcurrentName);
	$island->{'name'} = $HcurrentName;
	$flag = 1;
    }

    # password変更の場合
    if($HinputPassword ne '') {
	# パスワードを変更
	$island->{'password'} = encode($HinputPassword);
	$flag = 1;
    }

    if(($flag == 0) && ($HoldPassword ne $HspecialPassword)) {
	# どちらも変更されていない
	unlock();
	tempChangeNothing();
	return;
    }

    # データ書き出し
    writeIslandsFile($HcurrentID);
    unlock();

    # 変更成功
    tempChange();
}
sub changeOwner {
  # idから島を取得
  $HcurrentNumber = $HidToNumber{$HcurrentID};
  my($island) = $Hislands[$HcurrentNumber];
  my($flag) = 0;

  if(!checkPassword($island->{'password'},$HoldPassword)) {
    # password間違い
    unlock();
    tempWrongPassword();
    return;
  }
  # オーナー名を変更
  $HcurrentOwnerName =~ s/</&lt;/g;;
  $HcurrentOwnerName =~ s/>/&gt;/g;;
  $island->{'ownername'} = $HcurrentOwnerName;
  $flag = 1;

  # データ書き出し
  writeIslandsOwner($HcurrentID);
  unlock();

  # 変更成功
  tempChange();
}
sub changeFlag {
  # idから島を取得
  $HcurrentNumber = $HidToNumber{$HcurrentID};
  my($island) = $Hislands[$HcurrentNumber];
  my($flag) = 0;

  if(!checkPassword($island->{'password'},$HoldPassword)) {
    # password間違い
    unlock();
    tempWrongPassword();
    return;
  }
  # オーナー名を変更
  $HcurrentFlagName =~ s/</&lt;/g;;
  $HcurrentFlagName =~ s/>/&gt;/g;;
  $island->{'flagname'} = $HcurrentFlagName;
  $flag = 1;

  # データ書き出し
  writeIslandsFlag($HcurrentID);
  unlock();

  # 変更成功
  tempChange();
}

#----------------------------------------------------------------------
# ターン進行モード
#----------------------------------------------------------------------
# メイン
sub turnMain {
    # 最終更新時間を更新
    $HislandLastTime += $HunitTime;

    # ログファイルを後ろにずらす
    my($i, $j, $s, $d);
    for($i = ($HlogMax - 1); $i >= 0; $i--) {
	$j = $i + 1;
	my($s) = "${HdirName}/hakojima.log$i";
	my($d) = "${HdirName}/hakojima.log$j";
	unlink($d);
	rename($s, $d);
    }

    # 座標配列を作る
    makeRandomPointArray();

    # ターン番号
    $HislandTurn++;

    # 順番決め
    my(@order) = randomArray($HislandNumber);

    # 収入、消費フェイズ
    for($i = 0; $i < $HislandNumber; $i++) {
	estimate($order[$i]);
	income($Hislands[$order[$i]]);

	# ターン開始前の人口をメモる
	$Hislands[$order[$i]]->{'oldPop'} = $Hislands[$order[$i]]->{'pop'};
    }
    for($i = 0; $i < $HislandNumber; $i++) {
	doMonMove($Hislands[$order[$i]]);
    }
    # コマンド処理
    for($i = 0; $i < $HislandNumber; $i++) {
	# 戻り値1になるまで繰り返し
	while(doCommand($Hislands[$order[$i]]) == 0){};
    }

    # 成長および単ヘックス災害
    for($i = 0; $i < $HislandNumber; $i++) {
estimate($order[$i]);
	doEachHex($Hislands[$order[$i]]);
doStation($Hislands[$order[$i]]); # 電車の運行計算
      
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
    # 島全体処理
    my($remainNumber) = $HislandNumber;
    my($island);
    for($i = 0; $i < $HislandNumber; $i++) {
estimate($order[$i]);
	$island = $Hislands[$order[$i]];
	doIslandProcess($order[$i], $island); 

	# 死滅判定
	if($island->{'dead'} == 1) {
	    $island->{'pop'} = 0;
	    $remainNumber--;
	} elsif($island->{'pop'} == 0) {
	    $island->{'dead'} = 1;
	    $remainNumber--;
	    # 死滅メッセージ
	    my($tmpid) = $island->{'id'};
	    logDead($tmpid, $island->{'name'});
	    unlink("island.$tmpid");
	}
if ($island->{'sen'} > 0){
$sek++;
$seu .="$island->{'name'}島,";
}
if ($island->{'hei'} == 1){
$hek++;
$heu .="$island->{'name'}島,";
}
if ($island->{'ino'} == 1){
$ink++;
$inu .="$island->{'name'}島,";
}
if ($island->{'sen'} == 21){
$kyo++;
$kyu .="$island->{'name'}島,";
}elsif ($island->{'sen'} == 11){
$tei++;
$teu .="$island->{'name'}島,";
}elsif ($island->{'sen'} == 1){
$muo++;
$muu .="$island->{'name'}島,";
}
$ari=$island->{'shoku'};
if ($ari > $noo){
$noo = $ari;
$noi = $island->{'id'};
$niou ="$island->{'name'}島";
}
if ($island->{'factory'}> $koo){
$koo = $island->{'factory'};
$koi = $island->{'id'};
$kiou ="$island->{'name'}島";
}
if ($island->{'onse'} > $ooo){
$ooo = $island->{'onse'};
$ooi = $island->{'id'};
$oiou ="$island->{'name'}島";
}
if ($island->{'dou'} > $doo){
$doo = $island->{'dou'};
$doi = $island->{'id'};
$diou ="$island->{'name'}島";
}
if ($island->{'dep'} > $deo){
$deo = $island->{'dep'};
$dei = $island->{'id'};
$deou ="$island->{'name'}島";
}
if ($island->{'monka'}>$moo){
$moo = $island->{'monka'};
$moi = $island->{'id'};
$moou ="$island->{'name'}島";
}
if ($island->{'Jous'}>$joo){
$joo = $island->{'Jous'};
$joi = $island->{'id'};
$joou ="$island->{'name'}島";
}
if ($island->{'hatud'}>$hoo){
$hoo = $island->{'hatud'};
$hoi = $island->{'id'};
$hoou ="$island->{'name'}島";
}
if ($island->{'gomi'}>$goo){
$goo = $island->{'gomi'};
$goi = $island->{'id'};
$goou ="$island->{'name'}島";
}
if ($island->{'seki'}>$soo){
$soo = $island->{'seki'};
$soi = $island->{'id'};
$soou ="$island->{'name'}島";
}
if ($island->{'lands'}>$loo){
$loo = $island->{'lands'};
$loi = $island->{'id'};
$loou ="$island->{'name'}島";
}
if ($island->{'forest'}>$foo){
$foo = $island->{'forest'};
$foi = $island->{'id'};
$foou ="$island->{'name'}島";
}
if ($island->{'stay'}>$too){
$too = $island->{'stay'};
$toi = $island->{'id'};
$toou ="$island->{'name'}島";
}
$island->{'yhuu'} += $island->{'shuu'};
if(($HislandTurn % 10) == 0) {
if ($island->{'yhuu'}>$yoo){
$yoo = $island->{'yhuu'};
$yoi = $island->{'id'};
$yoou ="$island->{'name'}島";
}
$island->{'yhuu'}=0;
}
if ($island->{'money'}>$eoo){
$eoo = $island->{'money'};
$eoi = $island->{'id'};
$eoou ="$island->{'name'}島";
}
if ($island->{'area'}>$aoo){
$aoo = $island->{'area'};
$aoi = $island->{'id'};
$aoou ="$island->{'name'}島";
}
if ($island->{'sigoto'}>$ioo){
$ioo = $island->{'sigoto'};
$ioi = $island->{'id'};
$ioou ="$island->{'name'}島";
}
if ($island->{'mountain'}>$uoo){
$uoo = $island->{'mountain'};
$uoi = $island->{'id'};
$uoou ="$island->{'name'}島";
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
$biou ="$island->{'name'}島";
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
    # 人口順にソート
    islandSort();
$island = $Hislands[0];
$island->{'top'} ++;
    # ターン杯対象ターンだったら、その処理
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

    # 島数カット
    $HislandNumber = $remainNumber;

    # バックアップターンであれば、書く前にrename
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

	# ログファイルだけ戻す
	for($i = 0; $i <= $HlogMax; $i++) {
	    rename("${HdirName}.bak0/hakojima.log$i",
		   "${HdirName}/hakojima.log$i");
	}
	rename("${HdirName}.bak0/hakojima.his",
	       "${HdirName}/hakojima.his");
    }
    # ファイルに書き出し
    writeIslandsFile(-1);
myrmtree("${HdirName1}");
	mkdir("${HdirName1}", $HdirMode);
   writeFile(-1);

    # ログ書き出し
    logFlush();

    # 記録ログ調整
    logHistoryTrim();

    # トップへ
    topPageMain();
}

# ディレクトリ消し
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

# 収入、消費フェイズ
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
    # 収入
    if($pop > ($farm + $boku)){
	# 農業だけじゃ手が余る場合
	$island->{'food'} += $farm;
$island->{'food'} += $boku * 10;
$island->{'money'} += min(int(($pop - $farm- $boku) / 10), $work)*3;
$island->{'shuu'} += min(int(($pop - $farm- $boku) / 10), $work)*3;
}elsif($pop > $farm) {
	$island->{'food'} += $farm; # 農場フル稼働
$island->{'food'} +=($pop - $farm)* 10;
    } else {
	# 農業だけで手一杯の場合
	$island->{'food'} += $pop; # 全員野良仕事
    }

    # 食料消費
    $island->{'food'} = int(($island->{'food'}) - ($pop * $HeatenFood));
$island->{'shoku'} = $farm + ($boku * 10);
}

# コマンドフェイズ
sub doCommand {
    my($island) = @_;

    # コマンド取り出し
    my($comArray, $command);
    $comArray = $island->{'command'};
    $command = $comArray->[0]; # 最初のを取り出し
    slideFront($comArray, 0); # 以降を詰める

    # 各要素の取り出し
    my($kind, $target, $x, $y, $arg) = 
	(
	 $command->{'kind'},
	 $command->{'target'},
	 $command->{'x'},
	 $command->{'y'},
	 $command->{'arg'}
	 );

    # 導出値
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
	# 資金繰り
	logDoNothing($id, $name, $comName);
	$island->{'money'} += 10;
$island->{'shuu'} += 10;
	$island->{'absent'} ++;
	
	# 自動放棄
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

    # コストチェック
    if($cost > 0) {
	# 金の場合
	if($island->{'money'} < $cost) {
	    logNoMoney($id, $name, $comName);
	    return 0;
	}
    } elsif($cost < 0) {
	# 食料の場合
	if($island->{'food'} < (-$cost)) {
	    logNoFood($id, $name, $comName);
	    return 0;
	}
    }

    # コマンドで分岐
    if(($kind == $HcomPrepare) ||
       ($kind == $HcomPrepare2)) {
	# 整地、地ならし
	if(($landKind == $HlandSea) || 
	   ($landKind == $HlandSbase) ||
($landKind == $HlandLake) ||
	   ($landKind == $HlandOil) ||
	   ($landKind == $HlandMountain) ||
($landKind == $HlandJirai) ||
	   ($landKind == $HlandMonster)) {
	    # 海、海底基地、油田、山、怪獣は整地できない
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# 目的の場所を平地にする
	$land->[$x][$y] = $HlandPlains;
	$landValue->[$x][$y] = 0;
	logLandSuc($id, $name, '整地', $point);

	# 金を差し引く
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
	if($kind == $HcomPrepare2) {
	    # 地ならし
	    $island->{'prepare2'}++;
	    
	    # ターン消費せず
	    return 0;
	} else {
	    # 整地なら、埋蔵金の可能性あり
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
	    # 全部海だから埋め立て不能
	    logNoLandAround($id, $name, $comName, $point);
	    return 0;
	}
if($seaCount == 1) {
	    # 全部海だから埋め立て不能
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
$landValue->[$x][$y] += 3; # 規模 + 2000人
		if($landValue->[$x][$y] > 300) {
		    $landValue->[$x][$y] = 300; # 最大 50000人
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
	    # 全部海だから埋め立て不能
	    logNoLandAround($id, $name, $comName, $point);
	    return 0;
	}
if($seaCount == 1) {
	    # 全部海だから埋め立て不能
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
$landValue->[$x][$y] += 3; # 規模 + 2000人
		if($landValue->[$x][$y] > 300) {
		    $landValue->[$x][$y] = 300; # 最大 50000人
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
	# 埋め立て
	if(($landKind != $HlandSea) &&
($landKind != $HlandLake) &&
	   ($landKind != $HlandOil) &&
	   ($landKind != $HlandSbase)) {
	    # 海、海底基地、油田しか埋め立てできない
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# 周りに陸があるかチェック
	my($seaCount) =
	    countAround($land, $x, $y, $HlandSea, 5) +
	    countAround($land, $x, $y, $HlandOil, 5) +
            countAround($land, $x, $y, $HlandSbase, 5);

        if($seaCount == 5) {
	    # 全部海だから埋め立て不能
	    logNoLandAround($id, $name, $comName, $point);
	    return 0;
	}

	if((($landKind == $HlandSea) && ($lv == 1))||(($landKind == $HlandOil) &&($lv > 1))||($landKind == $HlandLake)){
	    # 浅瀬の場合
	    # 目的の場所を荒地にする
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
	    logLandSuc($id, $name, '埋め立て', $point);
	    $island->{'area'}++;

	    if($seaCount <= 4) {
		# 周りの海が3ヘックス以内なので、浅瀬にする
		my($i, $sx, $sy);

		for($i = 1; $i < 5; $i++) {
		    $sx = $x + $ax[$i];
		    $sy = $y + $ay[$i];


		    if(($sx < 0) || ($sx >= $HislandSize) ||
		       ($sy < 0) || ($sy >= $HislandSize)) {
		    } else {
			# 範囲内の場合
			if($land->[$sx][$sy] == $HlandSea) {
			    $landValue->[$sx][$sy] = 1;
			}
		    }
		}
	    }
	} else {
	    # 海なら、目的の場所を浅瀬にする
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 1;
	    logLandSuc($id, $name, '埋め立て', $point);
	}
	
	# 金を差し引く
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
	if($kind == $HcomUmeta) {
	    # 地ならし
	    $island->{'prepare2'}++;
	    
	    # ターン消費せず
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
	    # 見つかるか判定
	    if(2 >random(10)) {
		# 油田見つかる
		logOnseFound($id, $name, $point, $comName, $str);
		$land->[$x][$y] = $Hlanddoubutu;
		$landValue->[$x][$y] = 0;
	    } else {
		# 無駄撃ちに終わる
		logOnseFail($id, $name, $point, $comName, $str);
	    } 
return 1;
}else {
	    logLandFail($id, $name, $comName, $landName, $point);
return 1;
}
    } elsif($kind == $HcomDestroy) {
	# 掘削
	if(($landKind == $HlandSbase) ||
	   ($landKind == $HlandOil) ||
	   ($landKind == $HlandMonster)) {
	    # 海底基地、油田、怪獣は掘削できない
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	if(($landKind == $HlandSea) && ($lv == 0)) {
	    # 海なら、油田探し
	    # 投資額決定
	    if($arg == 0) { $arg = 1; }
	    my($value, $str, $p);
	    $value = min($arg * ($cost), $island->{'money'});
	    $str = "$value$HunitMoney";
	    $p = int($value / $cost) * 2;
	    $island->{'money'} -= $value;
$island->{'shuu'} -= $value;
	    # 見つかるか判定
	    if($p > random(100)) {
		# 油田見つかる
		logOilFound($id, $name, $point, $comName, $str);
		$land->[$x][$y] = $HlandOil;
		$landValue->[$x][$y] = 0;
	    } else {
		# 無駄撃ちに終わる
		logOilFail($id, $name, $point, $comName, $str);
	    }
	    return 1;
	}

	# 目的の場所を海にする。山なら荒地に。浅瀬なら海に。
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

	# 金を差し引く
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
	return 1;
    } elsif($kind == $HcomDestroy2) {
	# 掘削
	if(($landKind == $HlandSbase) ||
	   ($landKind == $HlandOil) ||
(($landKind == $HlandSea) && ($lv == 0))||
	   ($landKind == $HlandMonster)) {
	    # 海底基地、油田、怪獣は掘削できない
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# 目的の場所を海にする。山なら荒地に。浅瀬なら海に。
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
	logLandSuc($id, $name, '掘削', $point);

	# 金を差し引く
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
	# 回数付きなら、コマンドを戻す
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
		$landValue->[$x][$y] += 2; # 規模 + 2000人
		if($landValue->[$x][$y] > 50) {
		    $landValue->[$x][$y] = 50; # 最大 50000人
logLandSuc($id, $name, $comName, $point);
}
	# 回数付きなら、コマンドを戻す
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
	# 伐採
	if($landKind != $HlandForest) {
	    # 森以外は伐採できない
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# 目的の場所を平地にする
	$land->[$x][$y] = $HlandPlains;
	$landValue->[$x][$y] = 0;
	logLandSuc($id, $name, $comName, $point);

	# 売却金を得る
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

	# 地上建設系
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
	    # 不適当な地形
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# 種類で分岐
	if($kind == $HcomPlant) {
	    # 目的の場所を森にする。
	    $land->[$x][$y] = $HlandForest;
	    $landValue->[$x][$y] = 1; # 木は最低単位
	    logPBSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomBase) {
	    # 目的の場所をミサイル基地にする。
	    $land->[$x][$y] = $HlandBase;
	    $landValue->[$x][$y] = 0; # 経験値0
	    logPBSuc($id, $name, $comName, $point);
} elsif($kind == $Hcomdoubutu) { # ここから

$land->[$x][$y] = $Hlanddoubutu;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point); 
	}elsif($kind == $HcomShou) {
	    # 目的の場所を森にする。
	    $land->[$x][$y] = $HlandShou;
	    $landValue->[$x][$y] = 1; # 木は最低単位
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomTaiy) {
	    # 農場
	    if($landKind == $HlandTaiy) {
		# すでに農場の場合
		$landValue->[$x][$y] += 5; # 規模 + 2000人
		if($landValue->[$x][$y] > 100) {
		    $landValue->[$x][$y] = 100; # 最大 50000人
		}
	    } else {
		# 目的の場所を農場に
		$land->[$x][$y] = $HlandTaiy;
		$landValue->[$x][$y] = 5; # 規模 = 10000人
	    }
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomTinet) {
	    # 農場
	    if($landKind == $HlandTinet) {
		# すでに農場の場合
		$landValue->[$x][$y] += 3; # 規模 + 2000人
		if($landValue->[$x][$y] > 300) {
		    $landValue->[$x][$y] = 300; # 最大 50000人
		}
logLandSuc($id, $name, $comName, $point);
	    } else {
my($mouCount) =countAround($land, $x, $y, $HlandMountain, 5);
if($mouCount == 0) {
	    # 全部海だから埋め立て不能
	    logNoMounAround($id, $name, $comName, $point);
	    return 0;
	}
		# 目的の場所を農場に
		$land->[$x][$y] = $HlandTinet;
		$landValue->[$x][$y] = 3; # 規模 = 10000人
logLandSuc($id, $name, $comName, $point);
	    }
	} elsif($kind == $HcomFuha) {
	    # 農場
	    if($landKind == $HlandFuha) {
		# すでに農場の場合
		$landValue->[$x][$y] += 1; # 規模 + 2000人
		if($landValue->[$x][$y] > 10) {
		    $landValue->[$x][$y] = 10; # 最大 50000人
		}
	    } else {
		# 目的の場所を農場に
		$land->[$x][$y] = $HlandFuha;
		$landValue->[$x][$y] = 1; # 規模 = 10000人
	    }
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomReho) {
	    # 農場
	    if($landKind == $HlandReho) {
		# すでに農場の場合
		$landValue->[$x][$y] += 1; # 規模 + 2000人
		if($landValue->[$x][$y] > 10) {
		    $landValue->[$x][$y] = 10; # 最大 50000人
		}
	    } else {
		# 目的の場所を農場に
		$land->[$x][$y] = $HlandReho;
		$landValue->[$x][$y] = 1; # 規模 = 10000人
	    }
	    logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomJusi) { # ここから

$land->[$x][$y] = $HlandJusi;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomEisei) { # ここから

$land->[$x][$y] = $HlandEisei;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomDenb) { # ここから

$land->[$x][$y] = $HlandDenb;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomKeiba) { # ここから

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 5;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomFoot) { # ここから

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 4;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomYakyu) { # ここから

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 3;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomSki) { # ここから

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 2;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomSuiz) { # ここから

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomHotel) { # ここから

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 0;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomGolf) { # ここから

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 6;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomYuu) { # ここから

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 7;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomTenj) { # ここから

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 8;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomKaji) { # ここから

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 9;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomKouen) { # ここから

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 10;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomShok) { # ここから

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 11;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomTou) { # ここから

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 12;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomShiro) { # ここから

$land->[$x][$y] = $HlandLand;
$landValue->[$x][$y] = 13;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomGoyu) { # ここから

$land->[$x][$y] = $HlandGoyu;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomKoku) { # ここから

$land->[$x][$y] = $HlandKoku;
$landValue->[$x][$y] = 1;
logPBSuc($id, $name, $comName, $point);
} elsif($kind == $Hcomhospit) { # ここから

$land->[$x][$y] = $Hlandhos;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point); 
} elsif($kind == $HcomOmise) { # ここから

$land->[$x][$y] = $Hlanddoubutu;
$landValue->[$x][$y] = 2;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $HcomPori) { # ここから

$land->[$x][$y] = $HlandPori;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point);
} elsif($kind == $Hcomkiken) { # ここから

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
}else{# ここから
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
}else{# ここから
if($island->{'Inok'} >0){
logLanddume($id, $name, $comName, $point);
}else{

$land->[$x][$y] = $HlandInok;
$landValue->[$x][$y] = 1;
logLandSuc($id, $name, $comName, $point);
}
}	} elsif($kind == $HcomHaribote) {
	    # 目的の場所をハリボテにする
	    $land->[$x][$y] = $HlandHaribote;
	    $landValue->[$x][$y] = 0;
	    logHariSuc($id, $name, $comName, $HcomName[$HcomDbase], $point);
} elsif($kind == $HcomBank) {
# 銀行
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
# 銀行
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
            # 目的の場所を地雷にする
             $land->[$x][$y] = $HlandJirai;
             $landValue->[$x][$y] = 0;
             logABSuc($id, $name, $comName, $point);
         } elsif($kind == $HcomMineSuper) {
             # 目的の場所を高性能地雷にする
            $land->[$x][$y] = $HlandJirai;
             $landValue->[$x][$y] = 1;
logABSuc($id, $name, $comName, $point);
        } elsif($kind == $HcomMineWrpe) {
             # 目的の場所を高性能地雷にする
            $land->[$x][$y] = $HlandJirai;
             $landValue->[$x][$y] = 2;
logABSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomFarm) {
	    # 農場
	    if($landKind == $HlandFarm) {
		# すでに農場の場合
		$landValue->[$x][$y] += 2; # 規模 + 2000人
		if($landValue->[$x][$y] > 50) {
		    $landValue->[$x][$y] = 50; # 最大 50000人
		}
	    } else {
		# 目的の場所を農場に
		$land->[$x][$y] = $HlandFarm;
		$landValue->[$x][$y] = 10; # 規模 = 10000人
	    }
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomBoku) {
	    # 農場
	    if($landKind == $HlandBoku) {
		# すでに農場の場合
		$landValue->[$x][$y] += 1; # 規模 + 2000人
		if($landValue->[$x][$y] > 10) {
		    $landValue->[$x][$y] = 10; # 最大 50000人
		}
	    } else {
		# 目的の場所を農場に
		$land->[$x][$y] = $HlandBoku;
		$landValue->[$x][$y] = 1; # 規模 = 10000人
	    }
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomHatu) {
	    # 農場
	    if($landKind == $HlandHatu) {
		# すでに農場の場合
		$landValue->[$x][$y] += 5; # 規模 + 2000人
		if($landValue->[$x][$y] > 100) {
		    $landValue->[$x][$y] = 100; # 最大 50000人
		}
	    } else {
		# 目的の場所を農場に
		$land->[$x][$y] = $HlandHatu;
		$landValue->[$x][$y] = 10; # 規模 = 10000人
	    }
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomGomi) {
	    # 農場
	    if($landKind == $HlandGomi) {
		# すでに農場の場合
		$landValue->[$x][$y] += 5; # 規模 + 2000人
		if($landValue->[$x][$y] > 100) {
		    $landValue->[$x][$y] = 100; # 最大 50000人
		}
	    } else {
		# 目的の場所を農場に
		$land->[$x][$y] = $HlandGomi;
		$landValue->[$x][$y] = 10; # 規模 = 10000人
	    }
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomJous) {
	    # 農場
	    if($landKind == $HlandJous) {
		# すでに農場の場合
		$landValue->[$x][$y] += 5;
		if($landValue->[$x][$y] > 50) {
		    $landValue->[$x][$y] = 50; # 最大 50000人
		}
	    } else {
		# 目的の場所を農場に
		$land->[$x][$y] = $HlandJous;
		$landValue->[$x][$y] = 5; # 規模 = 10000人
	    }
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomFactory) {
	    # 工場
	    if($landKind == $HlandFactory) {
		# すでに工場の場合
		$landValue->[$x][$y] += 10; # 規模 + 10000人
		if($landValue->[$x][$y] > 200) {
		    $landValue->[$x][$y] = 200; 0000人
		}
	    } else {
		# 目的の場所を工場に
		$land->[$x][$y] = $HlandFactory;
		$landValue->[$x][$y] = 30; # 規模 = 10000人
	    }
	    logLandSuc($id, $name, $comName, $point);
 } elsif($kind == $HcomStation) {
             # 目的の場所を駅にする
             $land->[$x][$y] = $HlandStation;
             $landValue->[$x][$y] = 100;
             logStationSuc($id, $name, $comName, $point);
         } elsif($kind == $HcomRail) {           

            $land->[$x][$y] = $HlandStation;
           $landValue->[$x][$y] = 0;
             logRailSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomDbase) {
	    # 防衛施設
	    if($landKind == $HlandDefence) {
		# すでに防衛施設の場合
		$landValue->[$x][$y] = 1; # 自爆装置セット
		logBombSet($id, $name, $landName, $point);
	    } else {
		# 目的の場所を防衛施設に
		$land->[$x][$y] = $HlandDefence;
		$landValue->[$x][$y] = 0;
		logLandSuc($id, $name, $comName, $point);
	    }
	} elsif($kind == $HcomUbase) {
	    # 防衛施設
	    if($landKind == $HlandSefence) {
		# すでに防衛施設の場合
		$landValue->[$x][$y] = 1; # 自爆装置セット
		logBombSet($id, $name, $landName, $point);
	    } else {
		# 目的の場所を防衛施設に
		$land->[$x][$y] = $HlandSefence;
		$landValue->[$x][$y] = 0;
		logLandSuc($id, $name, $comName, $point);
	    }
	} elsif($kind == $HcomTbase) {
	    # 防衛施設
	    if($landKind == $HlandDefence) {
		# すでに防衛施設の場合
		$landValue->[$x][$y] = 1; # 自爆装置セット
		logBombSet($id, $name, $landName, $point);
	    } else {
		# 目的の場所を防衛施設に
		$land->[$x][$y] = $HlandDefence;
		$landValue->[$x][$y] = 2;
		logPBSuc($id, $name, $comName, $point);
	    }
	} elsif($kind == $HcomMonument) {
	    # 記念碑
	    if($landKind == $HlandMonument) {
		# すでに記念碑の場合
		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
		    # ターゲットがすでにない
		    # 何も言わずに中止
		    return 0;
		}
		my($tIsland) = $Hislands[$tn];
		$tIsland->{'bigmissile'}++;

		# その場所は荒地に
		$land->[$x][$y] = $HlandWaste;
		$landValue->[$x][$y] = 0;
		logMonFly($id, $name, $landName, $point);
	    } else {
		# 目的の場所を記念碑に
		$land->[$x][$y] = $HlandMonument;
		if($arg >= $HmonumentNumber) {
		    $arg = 0;
		}
		$landValue->[$x][$y] = $arg;
		logLandSuc($id, $name, $comName, $point);
	    }
	}

	# 金を差し引く
	$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
	# 回数付きなら、コマンドを戻す
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
	# 採掘場
	if($landKind != $HlandMountain) {
	    # 山以外には作れない
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	$landValue->[$x][$y] += 5; # 規模 + 5000人
	if($landValue->[$x][$y] > 200) {
	    $landValue->[$x][$y] = 200; # 最大 200000人
	}
	logLandSuc($id, $name, $comName, $point);

	# 金を差し引く
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
	# 海底基地
	if(($landKind != $HlandSea) || ($lv != 0)){
	    # 海以外には作れない
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	$land->[$x][$y] = $HlandSbase;
	$landValue->[$x][$y] = 0; # 経験値0
	logLandSuc($id, $name, $comName, '(?, ?)');

	# 金を差し引く
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

	# ミサイル系
	# ミサイル発射許可確認
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
	# ターゲット取得
	my($tn) = $HidToNumber{$target};
	if($tn eq '') {
	    # ターゲットがすでにない
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
	    # 0の場合は撃てるだけ
	    $arg = 10000;
	}

	# 事前準備
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
	# 難民の数
	my($boat) = 0;
my($mei) = ($island->{'kouei'} * 2.5) + 25;
	# 誤差
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

	# 金が尽きるか指定数に足りるか基地全部が撃つまでループ
	my($bx, $by, $count) = (0,0,0);
	while(($arg > 0) &&
	      ($island->{'money'} >= $cost)) {
	    # 基地を見つけるまでループ
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
		# 見つからなかったらそこまで
		last;
	    }
	    # 最低一つ基地があったので、flagを立てる
	    $flag = 1;	   

	    # 基地のレベルを算出
	    my($level) = expToLevel($land->[$bx][$by], $landValue->[$bx][$by]);
	    # 基地内でループ
	    while(($level > 0) &&
		  ($arg > 0) &&
		  ($island->{'money'} > $cost)) {
		# 撃ったのが確定なので、各値を消耗させる
		$level--;
		$arg--;
		$island->{'money'} -= $cost;
$island->{'shuu'} -= $cost;
		# 着弾点算出
		my($r) = random($err);
		$tx = $x + $ax[$r];
		$ty = $y + $ay[$r];

		# 着弾点範囲内外チェック
		if(($tx < 0) || ($tx >= $HislandSize) ||
		   ($ty < 0) || ($ty >= $HislandSize)) {
		    # 範囲外
		    if(($kind == $HcomMissileST)|| ($kind == $HcomRazer)|| ($kind == $HcomPMS)){
			# ステルス
			logMsOutS($id, $target, $name, $tName,
				   $comName, $point);
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}
		    } else {
			# 通常系
			logMsOut($id, $target, $name, $tName,
				  $comName, $point);
		    }
		    next;
		}

		# 着弾点の地形等算出
		my($tL) = $tLand->[$tx][$ty];
		my($tLv) = $tLandValue->[$tx][$ty];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($tx, $ty)";

		# 防衛施設判定
		my($defence) = 0;
		if($HdefenceHex[$id][$tx][$ty] == 1) {
		    $defence = 1;
		} elsif($HdefenceHex[$id][$tx][$ty] == -1) {
		    $defence = 0;
		} else {
		    if($tL == $HlandDefence) {
			# 防衛施設に命中
			# フラグをクリア
			my($i, $count, $sx, $sy);
			for($i = 0; $i < 13; $i++) {
			    $sx = $tx + $ax[$i];
			    $sy = $ty + $ay[$i];


			    if(($sx < 0) || ($sx >= $HislandSize) ||
			       ($sy < 0) || ($sy >= $HislandSize)) {
				# 範囲外の場合何もしない
			    } else {
				# 範囲内の場合
				$HdefenceHex[$id][$sx][$sy] = 0;
			    }
			}
}elsif($tL == $HlandSefence) {
			# 防衛施設に命中
			# フラグをクリア
			my($i, $count, $sx, $sy);
			for($i = 0; $i < 25; $i++) {
			    $sx = $tx + $ax[$i];
			    $sy = $ty + $ay[$i];

			    if(($sx < 0) || ($sx >= $HislandSize) ||
			       ($sy < 0) || ($sy >= $HislandSize)) {
				# 範囲外の場合何もしない
			    } else {
				# 範囲内の場合
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
				# 範囲外の場合何もしない
			    } else {
				# 範囲内の場合
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
		    # 空中爆破
		    if(($kind == $HcomMissileST)|| ($kind == $HcomRazer)|| ($kind == $HcomPMS)) {
			# ステルス
			logMsCaughtS($id, $target, $name, $tName,
				      $comName, $point, $tPoint);
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}
		    } else {
			# 通常系
			logMsCaught($id, $target, $name, $tName,
				     $comName, $point, $tPoint);
		    }
		    next;
		}

		# 「効果なし」hexを最初に判定

      if(($kind != $HcomMissileRE) &&
         ((($tL == $HlandSea) && ($tLv == 0)) || # 深い海
         ((($tL == $HlandSea) ||   # 海または・・・
           ($tL == $HlandSbase) ||   # 海底基地または・・・
($tL == $HlandLake) ||
           ($tL == $HlandMountain)) # 山で・・・
          && ($kind != $HcomMissileLD)))){ # 陸破弾以外
		    # 海底基地の場合、海のフリ
		    if($tL == $HlandSbase) {
			$tL = $HlandSea;
		    }
		    $tLname = landName($tL, $tLv);

		    # 無効化
		    if(($kind == $HcomMissileST)|| ($kind == $HcomRazer)|| ($kind == $HcomPMS)) {
			# ステルス
			logMsNoDamageS($id, $target, $name, $tName,
					$comName, $tLname, $point, $tPoint);
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}
		    } else {
			# 通常系
			logMsNoDamage($id, $target, $name, $tName,
				       $comName, $tLname, $point, $tPoint);
		    }
		    next;
		}

		# 弾の種類で分岐# 弾の種類で分岐
      if($kind == $HcomMissileRE) {
        if($tL == $HlandMountain){
          # 山に着弾した場合無効
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
            # 浅瀬の場合
            $tLand->[$tx][$ty] = $HlandWaste;
            $tLandValue->[$tx][$ty] = 0;
            logMsRESea1($id, $target, $name, $tName,
                        $comName, $tLname, $point, $tPoint);

            $tIsland->{'area'}++;

            if($seaCount <= 4) {
              # 周りの海が3ヘックス以内なので、浅瀬にする
              my($i, $sx, $sy);
              for($i = 1; $i < 5; $i++) {
                $sx = $x + $ax[$i];
                $sy = $y + $ay[$i];


                if(($sx < 0) || ($sx >= $HislandSize) ||
                   ($sy < 0) || ($sy >= $HislandSize)) {
                } else {
                # 範囲内の場合
                  if($tLand->[$sx][$sy] == $HlandSea) {
                    $tLandValue->[$sx][$sy] = 1;
                  }
                }
              }
            }
            next;
          } else {
            # 海なら、目的の場所を浅瀬にする
            $tLand->[$tx][$ty] = $HlandSea;
            $tLandValue->[$tx][$ty] = 1;
            logMsRESea($id, $target, $name, $tName,
                       $comName, $tLname, $point, $tPoint);

            next;

          }
        } elsif($tL == $HlandMonster){
          logMsREMonster($id, $target, $name, $tName,
                         $comName, $tLname, $point, $tPoint);
          # 山になる
          $tLand->[$tx][$ty] = $HlandMountain;
          $tLandValue->[$tx][$ty] = 0;
          next;
        }else{

        logMsRELand($id, $target, $name, $tName,
                    $comName, $tLname, $point, $tPoint);
        # 山になる
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
		    # 陸地破壊弾
		    if($tL == $HlandMountain) {
			# 山(荒地になる)
			logMsLDMountain($id, $target, $name, $tName,
					 $comName, $tLname, $point, $tPoint);
			# 荒地になる
			$tLand->[$tx][$ty] = $HlandWaste;
			$tLandValue->[$tx][$ty] = 0;
			next;

		    } elsif($tL == $HlandSbase) {
			# 海底基地
			logMsLDSbase($id, $target, $name, $tName,
				      $comName, $tLname, $point, $tPoint);
		    } elsif($tL == $HlandMonster) {
			# 怪獣
			logMsLDMonster($id, $target, $name, $tName,
					$comName, $tLname, $point, $tPoint);
		    } elsif(($tL == $HlandSea)|| ($tL == $HlandLake)) {
			# 浅瀬
			logMsLDSea1($id, $target, $name, $tName,
				    $comName, $tLname, $point, $tPoint);
		    } else {
			# その他
			logMsLDLand($id, $target, $name, $tName,
				     $comName, $tLname, $point, $tPoint);
		    }
		    
		    # 経験値
		    if($tL == $HlandTown) {
			if(($land->[$bx][$by] == $HlandBase) ||
			   ($land->[$bx][$by] == $HlandSbase)) {
			    # まだ基地の場合のみ
			    $landValue->[$bx][$by] += int($tLv / 20);
			    if($landValue->[$bx][$by] > $HmaxExpPoint) {
				$landValue->[$bx][$by] = $HmaxExpPoint;
			    }
			}
		    }

		    # 浅瀬になる
		    $tLand->[$tx][$ty] = $HlandSea;
		    $tIsland->{'area'}--;
		    $tLandValue->[$tx][$ty] = 1;

		    # でも油田、浅瀬、海底基地だったら海
		    if(($tL == $HlandOil) ||
			($tL == $HlandSea) ||
($tL == $HlandLake)||
		       ($tL == $HlandSbase)) {
			$tLandValue->[$tx][$ty] = 0;
		    }
		} else {
		    # その他ミサイル
		    if($tL == $HlandWaste) {
			# 荒地(被害なし)
			if(($kind == $HcomMissileST)|| ($kind == $HcomRazer)|| ($kind == $HcomPMS)) {
			    # ステルス
			    logMsWasteS($id, $target, $name, $tName,
					 $comName, $tLname, $point, $tPoint);
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}
			} else {
			    # 通常
			    logMsWaste($id, $target, $name, $tName,
					$comName, $tLname, $point, $tPoint);
			}
		    } elsif(($tL == $HlandMonster) || ($tL == $Hlandhokak)){
			# 怪獣
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
			# 硬化中?
			if((($special == 3) && (($HislandTurn % 2) == 1)) ||
			   (($special == 4) && (($HislandTurn % 2) == 0))||
			   (($special == 12) && (random (100) < 50))) {
			    # 硬化中
			    if(($kind == $HcomMissileST)|| ($kind == $HcomRazer)) {
				# ステルス
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
				# 通常弾
				logMsMonNoDamage($id, $target, $name, $tName,
					     $comName, $mName, $point,
					     $tPoint);
			    }
			    next;
			} else {
			    # 硬化中じゃない
my($hit) = random(5)+1;
			    if(($mHp == 1)&& ($kind != $HcomMissileHP)&&($kind != $HcomPMS)) {
				# 怪獣しとめた
				if(($land->[$bx][$by] == $HlandBase) ||
				   ($land->[$bx][$by] == $HlandSbase)) {
				    # 経験値
				    $landValue->[$bx][$by] += $HmonsterExp[$mKind];
				    if($landValue->[$bx][$by] > $HmaxExpPoint) {
					$landValue->[$bx][$by] = $HmaxExpPoint;
				    }
				}

				if(($kind == $HcomMissileST)||($kind == $HcomRazer)) {
				    # ステルス
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
				    # 通常
				    logMsMonKill($id, $target, $name, $tName,
						 $comName, $mName, $point,
						 $tPoint);
				}

				# 収入
				my($value) = $HmonsterValue[$mKind];
				if($value > 0) {
				    $tIsland->{'money'} += $value;
$tIsland->{'shuu'} += $value;
                                    $island->{'money'} += $value;
$island->{'shuu'} += $value;
				    logMsMonMoney($target, $mName, $value, $name);
				}

				# 賞関係
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
				# 怪獣しとめた
				if(($land->[$bx][$by] == $HlandBase) ||
				   ($land->[$bx][$by] == $HlandSbase)) {
				    # 経験値
				    $landValue->[$bx][$by] += $HmonsterExp[$mKind];
				    if($landValue->[$bx][$by] > $HmaxExpPoint) {
					$landValue->[$bx][$by] = $HmaxExpPoint;
				    }
				}
				    # ステルス
				    logMsMonKillS($id, $target, $name, $tName,
						  $comName, $mName, $point,
						  $tPoint);
if($tIsland->{'kanei'} > 0){
my($mii) =($tIsland->{'kanei'} * 5) + 25;
if(random(100) < $mii){
logmitukaru($id, $target,$name, $tName, $comName);
}
}


				# 収入
				my($value) = $HmonsterValue[$mKind];
				if($value > 0) {
				    $tIsland->{'money'} += $value;
$tIsland->{'shuu'} += $value;
                                    $island->{'money'} += $value;
$island->{'shuu'} += $value;
				    logMsMonMoney($target, $mName, $value, $name);
				}

				# 賞関係
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
				# 怪獣生きてる
				if(($kind == $HcomMissileST)|| ($kind == $HcomRazer)|| ($kind == $HcomPMS)) {
				    # ステルス
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
# 栄養
logMsMonsterH($id, $target, $name, $tName,
$comName, $mName, $point,
$tPoint);
} else {#体力が9だったらこちらに入る
logMsMonsterM($id, $target, $name, $tName,
$comName, $mName, $point,
$tPoint);
}
				} else {
				    # 通常
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
# HPが1増える
if($mHp < 9) {#体力が9以下の場合は増える。
$tLandValue->[$tx][$ty]++;
}
#体力が9だったらなにもせずに終了
next;
}
				# HPが1減る
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
				    # 経験値
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
			# 通常地形
			if(($kind == $HcomMissileST)|| ($kind == $HcomRazer)|| ($kind == $HcomPMS)) {
			    # ステルス
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
			    # 通常
			    logMsNormal($id, $target, $name, $tName,
					 $comName, $tLname, $point,
					 $tPoint);
			}
		    }
		    # 経験値
		    if($tL == $HlandTown) {
			if(($land->[$bx][$by] == $HlandBase) ||
			    ($land->[$bx][$by] == $HlandSbase)) {
			    $landValue->[$bx][$by] += int($tLv / 20);
			    $boat += $tLv; # 通常ミサイルなので難民にプラス
			    if($landValue->[$bx][$by] > $HmaxExpPoint) {
				$landValue->[$bx][$by] = $HmaxExpPoint;
			    }
			}
		    }
		    if($tL == $HlandHaribote) {
if($tLv >0) { # 銀行を破壊した時
$value =$tLv * 500;
$island->{'money'} +=  $value;
$island->{'shuu'} +=  $value;
logMsBank($id, $name, $value);
}
}
                    # 荒地になる
		    $tLand->[$tx][$ty] = $HlandWaste;
		    $tLandValue->[$tx][$ty] = 1; # 着弾点

		    # でも油田だったら海
		    if($tL == $HlandOil) {
			$tLand->[$tx][$ty] = $HlandSea;
			$tLandValue->[$tx][$ty] = 0;
		    }
		} 
	    }

	    # カウント増やしとく
	    $count++;
	}


	if($flag == 0) {
	    # 基地が一つも無かった場合
	    logMsNoBase($id, $name, $comName);
	    return 0;
	}

	# 難民判定
	$boat = int($boat / 2);
	if(($boat > 0) && ($id != $target) && ($kind != $HcomMissileST)) {
	    # 難民漂着
	    my($achive); # 到達難民
	    my($i);
	    for($i = 0; ($i < $HpointNumber && $boat > 0); $i++) {
		$bx = $Hrpx[$i];
		$by = $Hrpy[$i];
		if($land->[$bx][$by] == $HlandTown) {
		    # 町の場合
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
		    # 平地の場合
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
		# 少しでも到着した場合、ログを吐く
		logMsBoatPeople($id, $name, $achive);

		# 難民の数が一定数以上なら、平和賞の可能性あり
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
	# 怪獣派遣
	# 怪獣派遣許可確認
	if (($HislandTurn - $island->{'birth'}) <= $HdisableSendMonsterTurn) {
	    logNotPermitted($id, $name, $comName);
	    return 1;
	}
	if ($island->{'gun'} == 0) {
	    logNoKoku($id, $name, $comName);
	    return 0;
	}

	# ターゲット取得
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};

	if($tn eq '') {
	    # ターゲットがすでにない
	    logMsNoTarget($id, $name, $comName);
	    return 0;
	}
if($tIsland->{'teikou'} >0){
logteidame($id, $target, $name, $tName, $comName);
}elsif($island->{'teikou'} >0){
logteideme($id, $name, $comName);
}else{
	# メッセージ
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
	# 輸出量決定
	if($arg == 0) { $arg = 1; }
	my($value) = min($arg*10 , $island->{'oil'});

	# 輸出ログ
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
	# 輸出量決定
	if($arg == 0) { $arg = 1; }
	my($value) = min($arg * (-$cost), $island->{'food'});

	# 輸出ログ
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
# 輸入量決定
if($arg == 0) { $arg = 1; }
my($value) = $arg*10;

# 輸入ログ
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
# 輸入量決定
if($arg == 0) { $arg = 1; }
my($value) = $arg * $cost;

# 輸入ログ
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
# 強奪
if($arg == 0) { $arg = 1; }
# ターゲット取得
my($tn) = $HidToNumber{$target};
my($tIsland) = $Hislands[$tn];
my($tName) = $tIsland->{'name'};
my($RobFood, $RobMoney) = ($arg * 100, $arg * 100);
$island->{'money'} -= $arg * $cost;
$island->{'shuu'} -= $arg * $cost;
if($tn eq '') {
# ターゲットがすでにない
logMsNoTarget($id, $name, $comName);
return 0;
}
my($saef) = 100 - $arg;
if(((random(200) <= $saef) && ($kind == $HcomRob)) ||
((random(300) <= $saef) && ($kind == $HcomRobST))){
# 強奪成功
# 金を強奪
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
# 強奪する量の方が大きければ全額
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

# 食料も強奪
if($tIsland->{'food'} >= $RobFood){
$tIsland->{'food'} -= $RobFood;
$island->{'food'} += $RobFood;
if($kind == $HcomRob){
logRobFood($id, $target, $name, $tName, $comName, $RobFood);
} else {
logRobSTFood($id, $target, $name, $tName, $comName, $RobFood);
}
} else {
# 強奪する量の方が大きければ全部
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
# 強奪失敗
logMissRob($id, $target, $name, $tName, $comName);
}
return 1;
} elsif(($kind == $HcomOil)||
($kind == $HcomOilH)){
	# 援助系
	if (($HislandTurn - $island->{'birth'}) <= $HdisableMonsterTurn) {
	    logNotPermitted($id, $name, $comName);
	    return 1;
	}
if($island->{'mina'} > 0){
	# ターゲット取得
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
	# 援助量決定
	if($arg == 0) { $arg = 1; }
	my($value, $str);
	    $value = min($arg*10, $island->{'oil'});
	    $str = "$valueトン";
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
	# 援助系
	if (($HislandTurn - $island->{'birth'}) <= $HdisableMonsterTurn) {
	    logNotPermitted($id, $name, $comName);
	    return 1;
	}
if($island->{'mina'} > 0){
	# ターゲット取得
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
	# 援助量決定
	if($arg == 0) { $arg = 1; }
	my($value, $str);
	    $value = min($arg * 100, $island->{'slag'});
	    $str = "$valueトン";
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
	# 援助系
	if (($HislandTurn - $island->{'birth'}) <= $HdisableMonsterTurn) {
	    logNotPermitted($id, $name, $comName);
	    return 1;
	}

	# ターゲット取得
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};

	# 援助量決定
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
}	# 援助ログ
	} else {
	    $island->{'money'} -= $value;
$island->{'shuu'} -= $value;
	    $tIsland->{'money'} += $value;
	    $tIsland->{'shuu'} += $value;
	# 援助ログ
if($kind == $HcomMoney){
	logAid($id, $target, $name, $tName, $comName, $str);
}else{
logAidH($id, $target, $name, $tName, $comName, $str);
}
	}
	return 0;
    } elsif($kind == $HcomPropaganda) {
	# 誘致活動
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
	# 放棄
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
          # 山に着弾した場合無効
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
            # 浅瀬の場合
            $tLand->[$x][$y] = $HlandWaste;
            $tLandValue->[$x][$y] = 0;
            logXsRESea1($id, $target, $name, $tName,
                        $comName, $tLname, $point, $tPoint);

            $tIsland->{'area'}++;

            if($seaCount <= 4) {
              # 周りの海が3ヘックス以内なので、浅瀬にする
              my($i, $sx, $sy);
              for($i = 1; $i < 5; $i++) {
                $sx = $x + $ax[$i];
                $sy = $y + $ay[$i];


                if(($sx < 0) || ($sx >= $HislandSize) ||
                   ($sy < 0) || ($sy >= $HislandSize)) {
                } else {
                # 範囲内の場合
                  if($tLand->[$sx][$sy] == $HlandSea) {
                    $tLandValue->[$sx][$sy] = 1;
                  }
                }
              }
            }
            next;
          } else {
            # 海なら、目的の場所を浅瀬にする
            $tLand->[$x][$y] = $HlandSea;
            $tLandValue->[$x][$y] = 1;
            logXsRESea($id, $target, $name, $tName,
                       $comName, $tLname, $point, $tPoint);

            next;

          }
        } elsif($tL == $HlandMonster){
          logXsREMonster($id, $target, $name, $tName,
                         $comName, $tLname, $point, $tPoint);
          # 山になる
          $tLand->[$x][$y] = $HlandMountain;
          $tLandValue->[$x][$y] = 0;
          next;
        }else{

        logXsRELand($id, $target, $name, $tName,
                    $comName, $tLname, $point, $tPoint);
        # 山になる
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

    # 導出値
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
		# すでに動いた後
		next;
	    }

	    # 各要素の取り出し
	    my($mKind, $mName, $mHp) = monsterSpec($landValue->[$x][$y]);
	    my($special) = $HmonsterSpecial[$mKind];

            # 途中で帰ってもらう # ここから
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
	    # 硬化中?
	    if((($special == 3) && (($HislandTurn % 2) == 1)) ||
	       (($special == 4) && (($HislandTurn % 2) == 0))) {
		# 硬化中
		next;
	    }

	    # 動く方向を決定
	    my($d, $sx, $sy);
	    my($i);
	    for($i = 0; $i < 3; $i++) {
		$d = random(4) + 1;
		$sx = $x + $ax[$d];
		$sy = $y + $ay[$d];



		# 範囲外判定
		if(($sx < 0) || ($sx >= $HislandSize) ||
		   ($sy < 0) || ($sy >= $HislandSize)) {
		    next;
		}

		# 海、海基、油田、怪獣、山、記念碑以外
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
		# 動かなかった
		next;
	    }

	    # 動いた先の地形によりメッセージ
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

	    # もと居た位置を荒地に
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
} elsif($HmonsterSpecial[$mKind] == 7) {
if(random(20) < 16) {
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # もと居た位置を荒地に
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;

} else {
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # もと居た位置を荒地に
	    $land->[$x][$y] = $HlandMonster;
	    $landValue->[$x][$y] = 59;
logQee($id, $name, "($x, $y)", $mName);
}

} elsif ($HmonsterSpecial[$mKind] == 10) {
	    # 移動
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # もと居た位置を荒地に
	    $land->[$x][$y] = $HlandPlains;
	    $landValue->[$x][$y] = 0;
} elsif ($HmonsterSpecial[$mKind] == 11) {
if(random(100) < 10) {
$landValue->[$x][$y] += 20;
logMonsterkak($id, $name, $point, $mName);
}	    # 移動
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # もと居た位置を荒地に
	    $land->[$x][$y] = $HlandPlains;
	    $landValue->[$x][$y] = 0;
} elsif ($HmonsterSpecial[$mKind] == 13) {
	    # 移動
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # もと居た位置を荒地に
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
} elsif ($HmonsterSpecial[$mKind] == 15) {
my($sji) = random(8) + 5;
		$jx = $x + $ax[$sji];
		$jy = $y + $ay[$sji];


		# 着弾点範囲内外チェック
		if(($jx < 0) || ($jx >= $HislandSize) ||
		   ($jy < 0) || ($jy >= $HislandSize)) {
		    # 範囲外

			# 通常系
logMonUtiDame($id, $name, "($x, $y)", $mName);
		    }else{
		my($tL) = $land->[$jx][$jy];
		my($tLv) = $landValue->[$jx][$jy];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($jx, $jy)";
         if(($tL == $HlandSea) ||   # 海または・・・
           ($tL == $HlandSbase) ||   # 海底基地または・・・
(($tL == $HlandLake)&& ($tLv == 0))  ||
           ($tL == $HlandMountain)){ # 陸破弾以外
		    # 海底基地の場合、海のフリ
		    if($tL == $HlandSbase) {
			$tL = $HlandSea;
		    }
		    $tLname = landName($tL, $tLv);

			# ステルス
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
			    # 硬化中
lognodamageT($id, $name, $kName, $mName, $point,$tPoint);
}else{
if($kHp == 1){
logMsMonKillT($id, $name, $kName, $mName, $point,$tPoint);
		    $land->[$jx][$jy] = $HlandWaste;
		    $landValue->[$jx][$jy] = 1; # 着弾点
}else{
logMsMonsterT($id, $name, $kName, $mName, $point,$tPoint);
	$landValue->[$jx][$jy]--;
}
}
}
}else{
logMsNormalT($id, $name, $tLname, $mName, $point,$tPoint);
		    $land->[$jx][$jy] = $HlandWaste;
		    $landValue->[$jx][$jy] = 1; # 着弾点
  if($tL == $HlandOil) {
			$land->[$jx][$jy] = $HlandSea;
			$landValue->[$jx][$jy] = 0;
		    }
		} 
	    }
}

	    # 移動
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # もと居た位置を荒地に
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
}elsif($HmonsterSpecial[$mKind] == 19) {
my($sji) = random(8) + 5;
		$jx = $x + $ax[$sji];
		$jy = $y + $ay[$sji];

		# 着弾点範囲内外チェック
		if(($jx < 0) || ($jx >= $HislandSize) ||
		   ($jy < 0) || ($jy >= $HislandSize)) {
		    # 範囲外

			# 通常系
logMonUtiDameU($id, $name, "($x, $y)", $mName);
		    }else{
		my($tL) = $land->[$jx][$jy];
		my($tLv) = $landValue->[$jx][$jy];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($jx, $jy)";
         if(($tL == $HlandSea) ||   # 海または・・・
           ($tL == $HlandSbase) ||   # 海底基地または・・・
(($tL == $HlandLake)&& ($tLv == 0))  ||
           ($tL == $HlandMountain)){ # 陸破弾以外
		    # 海底基地の場合、海のフリ
		    if($tL == $HlandSbase) {
			$tL = $HlandSea;
		    }
		    $tLname = landName($tL, $tLv);

			# ステルス
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
			    # 硬化中
lognodamageU($id, $name, $kName, $mName, $point,$tPoint);
}else{
if($kHp == 1){
logMsMonKillU($id, $name, $kName, $mName, $point,$tPoint);
		    $land->[$jx][$jy] = $HlandWaste;
		    $landValue->[$jx][$jy] = 1; # 着弾点
}else{
logMsMonsterU($id, $name, $kName, $mName, $point,$tPoint);
	$landValue->[$jx][$jy]--;
}
}
}
}else{
logMsNormalU($id, $name, $tLname, $mName, $point,$tPoint);
		    $land->[$jx][$jy] = $HlandWaste;
		    $landValue->[$jx][$jy] = 1; # 着弾点
  if($tL == $HlandOil) {
			$land->[$jx][$jy] = $HlandSea;
			$landValue->[$jx][$jy] = 0;
		    }
		} 
	    }
}

	    # 移動
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # もと居た位置を荒地に
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
}elsif($HmonsterSpecial[$mKind] == 20) {
my($sji) = random(8) + 5;
		$jx = $x + $ax[$sji];
		$jy = $y + $ay[$sji];


		# 着弾点範囲内外チェック
		if(($jx < 0) || ($jx >= $HislandSize) ||
		   ($jy < 0) || ($jy >= $HislandSize)) {
		    # 範囲外

			# 通常系
logMonUtiDameV($id, $name, "($x, $y)", $mName);
		    }else{
		my($tL) = $land->[$jx][$jy];
		my($tLv) = $landValue->[$jx][$jy];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($jx, $jy)";
         if(($tL == $HlandSea) ||   # 海または・・・
           ($tL == $HlandSbase) ||   # 海底基地または・・・
(($tL == $HlandLake)&& ($tLv == 0))  ||
           ($tL == $HlandMountain)){ # 陸破弾以外
		    # 海底基地の場合、海のフリ
		    if($tL == $HlandSbase) {
			$tL = $HlandSea;
		    }
		    $tLname = landName($tL, $tLv);

			# ステルス
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
			    # 硬化中
lognodamageV($id, $name, $kName, $mName, $point,$tPoint);
}else{
if($kHp == 1){
logMsMonKillV($id, $name, $kName, $mName, $point,$tPoint);
		    $land->[$jx][$jy] = $HlandWaste;
		    $landValue->[$jx][$jy] = 1; # 着弾点
}else{
logMsMonsterV($id, $name, $kName, $mName, $point,$tPoint);
	$landValue->[$jx][$jy]--;
}
}
}
}else{
logMsNormalV($id, $name, $tLname, $mName, $point,$tPoint);
		    $land->[$jx][$jy] = $HlandWaste;
		    $landValue->[$jx][$jy] = 1; # 着弾点
  if($tL == $HlandOil) {
			$land->[$jx][$jy] = $HlandSea;
			$landValue->[$jx][$jy] = 0;
		    }
		} 
	    }
}

	    # 移動
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # もと居た位置を荒地に
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
}elsif($HmonsterSpecial[$mKind] == 18) {
if(random(10) < 5){
my($sji) = random(12) + 13;
		$jx = $x + $ax[$sji];
		$jy = $y + $ay[$sji];


		# 着弾点範囲内外チェック
		if(($jx < 0) || ($jx >= $HislandSize) ||
		   ($jy < 0) || ($jy >= $HislandSize)) {
		    # 範囲外

			# 通常系
logMonUtiDameX($id, $name, "($x, $y)", $mName);
		    }else{
		my($tL) = $land->[$jx][$jy];
		my($tLv) = $landValue->[$jx][$jy];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($jx, $jy)";
         if(($tL == $HlandSea) ||   # 海または・・・
           ($tL == $HlandSbase) ||   # 海底基地または・・・
(($tL == $HlandLake)&& ($tLv == 0))){ # 陸破弾以外
		    # 海底基地の場合、海のフリ
		    if($tL == $HlandSbase) {
			$tL = $HlandSea;
		    }
		    $tLname = landName($tL, $tLv);

			# ステルス
			logMsNoDamageX($id, $name, $tLname, $mName, $point, $tPoint);
}else{
logMsNormalX($id, $name, $tLname, $mName, $point,$tPoint);
		    $land->[$jx][$jy] = $HlandSea;
		    $landValue->[$jx][$jy] = 0; # 着弾点
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


		# 着弾点範囲内外チェック
		if(($jx < 0) || ($jx >= $HislandSize) ||
		   ($jy < 0) || ($jy >= $HislandSize)) {
		    # 範囲外

			# 通常系
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
	    # 移動
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # もと居た位置を荒地に
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
}elsif($HmonsterSpecial[$mKind] == 21) {
my($sji) = random(12) + 13;
		$jx = $x + $ax[$sji];
		$jy = $y + $ay[$sji];


		# 着弾点範囲内外チェック
		if(($jx < 0) || ($jx >= $HislandSize) ||
		   ($jy < 0) || ($jy >= $HislandSize)) {
		    # 範囲外

			# 通常系
logMonUtiDameZ($id, $name, "($x, $y)", $mName);
}else{
	my($tL) = $land->[$jx][$jy];
		my($tLv) = $landValue->[$jx][$jy];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($jx, $jy)";
logdasuyoZ($id, $name, $mName, "($x, $y)",$tPoint,$tLname);
wideDamage($id, $name, $land, $landValue, $jx, $jy);
}

	    # 移動
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # もと居た位置を荒地に
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
     if(($tL == $HlandSea) ||   # 海または・・・
           ($tL == $HlandSbase) ||   # 海底基地または・・・
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

	    # もと居た位置を荒地に
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
     if(($tL == $HlandSea) ||   # 海または・・・
           ($tL == $HlandSbase) ||   # 海底基地または・・・
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

	    # もと居た位置を荒地に
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

	    # 移動
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # もと居た位置を荒地に
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
}

	    # 移動済みフラグ
	    if($HmonsterSpecial[$mKind] == 2) {
		# 移動済みフラグは立てない
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
		# 普通の怪獣
		$monsterMove[$sx][$sy] = 2;

	    }

	    if((($l == $HlandDefence) && ($HdBaseAuto == 1)&&
($jibaku == 0)) || (($l == $HlandSefence) && ($HdBaseAuto == 1)&&
($jibaku == 0))){
		logMonsMoveDefence($id, $name, $lName, $point, $mName);
		wideDamage($id, $name, $land, $landValue, $sx, $sy);
             } elsif($l == $HlandJirai) {
                    if($lv == 0) {
                        # 地雷を踏んだ
           logMonsMoveMine($id, $name, $lName, $point, $mName);
if ($mHp <= 2){
                    if ($mHp== 2) {
                      logMonsMoveMineDead($id, $name, $lName, $point, $mName);
                         # 収入
                        my($value) = $HmonsterValue[$mKind];
                         if($value > 0) {
                             $tIsland->{'money'} += $value;
                            logMsMonMoney($target, $mName, $value);                         }
                     } else {
                   logMonsMoveMineScatter($id, $name, $lName, $point, $mName);
                     }
                    $land->[$sx][$sy] = $HlandWaste;
                     $landValue->[$sx][$sy] = 1;

                     # 賞関係
                     my($prize) = $island->{'prize'};
                     $prize =~ /([0-9]*),([0-9]*),(.*)/;
                     my($flags) = $1;
                     my($monsters) = $2;
                     my($turns) = $3;
                     my($v) = 2 ** $mKind;
                     $monsters |= $v;
                     $island->{'prize'} = "$flags,$monsters,$turns";
                 } else {
                     # 怪獣は生き残った
                     logMonsMoveMineAlive($id, $name, $lName, $point, $mName);
$landValue->[$sx][$sy] -= 2;
                 }
                    } elsif($lv == 1) {
           logMonsMoveMine($id, $name, $lName, $point, $mName);
if ($mHp <= 4){
                     # 怪獣を倒した
                    if ($mHp== 4) {
                      logMonsMoveMineDead($id, $name, $lName, $point, $mName);
                         # 収入
                        my($value) = $HmonsterValue[$mKind];
                         if($value > 0) {
                             $tIsland->{'money'} += $value;
                            logMsMonMoney($target, $mName, $value);                         }
                     } else {
                    # 怪獣の体力を超えてダメージを与えたので死体が吹き飛んだ
                   logMonsMoveMineScatter($id, $name, $lName, $point, $mName);
                     }

                     # 地形を荒地(弾痕)にする
                    $land->[$sx][$sy] = $HlandWaste;
                     $landValue->[$sx][$sy] = 1;

                     # 賞関係
                     my($prize) = $island->{'prize'};
                     $prize =~ /([0-9]*),([0-9]*),(.*)/;
                     my($flags) = $1;
                     my($monsters) = $2;
                     my($turns) = $3;
                     my($v) = 2 ** $mKind;
                     $monsters |= $v;
                     $island->{'prize'} = "$flags,$monsters,$turns";
                 } else {
                     # 怪獣は生き残った
                     logMonsMoveMineAlive($id, $name, $lName, $point, $mName);
$landValue->[$sx][$sy] -= 4;
                 }
                     } elsif($lv ==2) {
                         # ワープ地雷を踏んだ
                         # 転送する島をランダムに決める
                         my($i) = int(rand($HislandNumber));
                         my($tIsland) = $Hislands[$i];
                         my($tId) = $tIsland->{'id'};
                         my($tLand) = $tIsland->{'land'};
                         my($tLandValue) = $tIsland->{'landValue'};
                         # 怪獣を転送する(転送先の地形は無視)
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
# 成長および単ヘックス災害
sub doEachHex {
    my($island) = @_;
    my(@monsterMove);

    # 導出値
    my($name) = $island->{'name'};
    my($id) = $island->{'id'};
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};
    my($Miz) = $island->{'Jous'} * 100;
    # 増える人口のタネ値
    my($addpop)  = 0; # 村、町
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
	# 食料不足
	$addpop += -30;
$addpop2 += -50;
}
if($island->{'propaganda'} == 1) {
	# 誘致活動中
	$addpop += 30;
	$addpop2 += 3;
}
my($shooo) = $island->{'sigoto'}  * 10;
my($shouo) = $island->{'pop'} * 0.6;

    if($shooo <= $shouo) {
	$addpop += -20;
$addpop2 += -40;
}
    # ループ
    my($x, $y, $i);
    for($i = 0; $i < $HpointNumber; $i++) {
	$x = $Hrpx[$i];
	$y = $Hrpy[$i];
	my($landKind) = $land->[$x][$y];
	my($lv) = $landValue->[$x][$y];

	if($landKind == $HlandTown) {
	    # 町系
if($lv < 100) {
if($addpop < 0) {
$lv -= (random(-$addpop) + 1);
	if($lv <= 0) {
		    # 平地に戻す
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
	    # 都市になると成長遅い
                     if (countStation($land, $landValue, $x, $y))
                     {
                         # 周囲に駅がある
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
	    # 平地
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
		# 周りに農場、町があれば、ここも町になる
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
	    # 平地
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
	    # 森
	    if($lv < 200) {
		# 木を増やす
		$landValue->[$x][$y]++;
	    }
	} elsif($landKind == $HlandDefence) {
	    if($lv == 1) {
		# 防衛施設自爆
		my($lName) = &landName($landKind, $lv);
		logBombFire($id, $name, $lName, "($x, $y)");

		# 広域被害ルーチン
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
		# 防衛施設自爆
		my($lName) = &landName($landKind, $lv);
		logBombFire($id, $name, $lName, "($x, $y)");

		# 広域被害ルーチン
		wideDamage($id, $name, $land, $landValue, $x, $y);
	    }
} elsif($landKind == $Hlanddoubutu) { # ここから
# 動物園
if($lv == 1) {
my($value, $str, $lName);
$lName = landName($landKind, $lv);
$value = 30 - random(29);
$island->{'money'} += $value;
$island->{'shuu'} += $value;
$str = "$value$HunitMoney";
$island->{'food'} -=100;
# 収入ログ
logdoubutuMoney($id, $name, $lName, "($x, $y)", $str); 

} elsif ($lv == 2){ # ここから
# 動物園
my($value, $str, $lName);
$lName = landName($landKind, $lv);
$value = int(($island->{'pop'} / 20) - 5);
$island->{'money'} += $value;
$island->{'shuu'} += $value;
$str = "$value$HunitMoney";
# 収入ログ
logOmiseMoney($id, $name, $lName, "($x, $y)", $str); 
} else {
	    # 海底油田
	    my($value, $str, $lName);
	    $lName = landName($landKind, $lv);
	    $value = $island->{'area'}/4;
	    $island->{'money'} += $value;
$island->{'shuu'} += $value;
	    $str = "$value$HunitMoney";

	    # 収入ログ
	    logOnseMoney($id, $name, $lName, "($x, $y)", $str);
}
} elsif($landKind == $HlandHaribote) {
# 銀行
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
($land->[$tx][$ty] == $HlandSea) ||   # 海または・・・
($land->[$tx][$ty] == $HlandSbase) ||   # 海底基地または・・・
($land->[$tx][$ty] == $HlandLake) ||
($land->[$tx][$ty] == $HlandMountain)){ # 陸破弾以外
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
		    $landValue->[$tx][$ty] = 1; # 着弾点
} else {
logNsMonster($id, $name,  $mName, "($x, $y)","($cx, $cy)", "($tx, $ty)");
$landValue->[$tx][$ty]--;
}
}
} else {
$tLname = landName($land->[$tx][$ty], $landValue->[$tx][$ty]);
logNsNormal($id, $name, $tLname, "($x, $y)","($cx, $cy)", "($tx, $ty)");
		    $land->[$tx][$ty] = $HlandWaste;
		    $landValue->[$tx][$ty] = 1; # 着弾点
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
	    # 海底油田
	    my($value, $str, $lName);
	    $lName = landName($landKind, $lv);
	    $value = 200 + random(101);
	    $island->{'oil'} += $value;
	    $str = "$valueトン";

	    # 収入ログ
	    logOilMoney($id, $name, $lName, "($x, $y)", $str);

	    # 枯渇判定
	    if(random(1000) < $HoilRatio) {
		# 枯渇
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
	# 火災判定
	if((($landKind == $HlandTown) && ($lv > 30)) ||
	   ($landKind == $HlandHaribote) ||
           ($landKind == $HlandStation) ||
	   ($landKind == $HlandFactory)) {
	    if((random(1000) < $HdisFire)||
	   ($island->{'kasai'} >0)){
		# 周囲の森と記念碑を数える
		if(((countAround($land, $x, $y, $HlandForest, 5) +
		    countAround($land, $x, $y, $HlandMonument, 5)) == 0)&&
(countAround($land, $x, $y, $HlandShou, 25) == 0)) {
		    # 無かった場合、火災で壊滅
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
 # 電車の運行計算
 # (これは CPU 時間を消費する重い処理です)
 sub doStation {
     my($island) = @_;
     my(@monsterMove);
     # 導出値
     my($name) = $island->{'name'};
     my($id) = $island->{'id'};
     my($land) = $island->{'land'};
     my($landValue) = $island->{'landValue'};
     my($x, $y, $i, $j, $n, $station);
     # 運行中の乗客をクリア
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
                 # 線路
                 $landValue->[$x][$y] = 0;
             }
             else
             {
                 # 駅
                 $station++;
                 $landValue->[$x][$y] = 100;
             }
         }
     }
     # 駅が２つ以上なければ電車は運行しない
     return if ($station < 2);
     # 線路に電車を置く
     $n = 0;
     for($i = 0; $i < $HpointNumber; $i++) {
         $x = $Hrpx[$i];
         $y = $Hrpy[$i];
         my($landKind) = $land->[$x][$y];
         my($lv) = $landValue->[$x][$y];
         if($landKind == $HlandStation)
         {
             # 電車を置く
             if($lv < 100)
             {
                 # 線路
                 $n = 1;
                 goTrain($land, $landValue, $x, $y, 100 - 1);
                 last;
             }
         }
     }
     # 線路がなければ運行しない
     return if (!$n);
     # 電車を走らせる
     # (最大で 20 ヘックス先まで)
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
                 # 電車を移動する
                 if(($lv > 0) && ($lv < 100))
                 {
                     # 線路
                     goTrain($land, $landValue, $x, $y, $lv - 1);
                 }
                 elsif($lv == 100)
                 {
                     # 客のいない駅がある(線路が切れている可能性がある)
                     $n = 0;
                 }
             }
         }
     }

     # 全ての駅が線路で接続されていなければ運行しない
     return if (!$n);
     # 駅に到着した乗客数を計算する
     my($value, $str, $lName, $pop);
     $pop = int($island->{'pop'} / 100) + 1; # 住民10万人ごとに収益アップ
     for($i = 0; $i < $HpointNumber; $i++) {
         $x = $Hrpx[$i];
         $y = $Hrpy[$i];
         my($landKind) = $land->[$x][$y];
         my($lv) = $landValue->[$x][$y];
         if($landKind == $HlandStation)
         {
             if($lv >= 100)
             {
                 # 駅
                 $value = int((200 - $landValue->[$x][$y]) / $station);
                 if ($value > 0)
                 {
                     # 収益が上がった
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
 
 # 電車を移動する
 # (線路上の乗客の流れを計算する)
 sub goTrain {
     my($land, $landValue, $x, $y, $unit) = @_;
     my($i, $sx, $sy);
     for($i = 1; $i < 5; $i++) {
          $sx = $x + $ax[$i];
          $sy = $y + $ay[$i];



          if(($sx < 0) || ($sx >= $HislandSize) ||
             ($sy < 0) || ($sy >= $HislandSize)) {
          } else {
              # 範囲内の場合
              my($lv) = $landValue->[$sx][$sy];
              if($land->[$sx][$sy] == $HlandStation)
              {
                  if($lv < 100)
                  {
                      # 線路
                      if (!($lv || ($lv > $unit)))
                      {
                         # 隣の線路に電車を移動する
                          $landValue->[$sx][$sy] = $unit;
                     }
                  }
                  else
                  {
                      # 駅
                      if (($lv == 100) || ($lv > $unit + 100))
                      {
                          # 駅に電車を移動する
                          $landValue->[$sx][$sy] = $unit + 100;
                      }
                  }
              }
          }
      }
 }
 # (駅も含む)
# 周囲の町、農場があるか判定
sub countGrow {
    my($land, $landValue, $x, $y) = @_;
    my($i, $sx, $sy);
    for($i = 1; $i < 5; $i++) {
	 $sx = $x + $ax[$i];
	 $sy = $y + $ay[$i];



	 if(($sx < 0) || ($sx >= $HislandSize) ||
	    ($sy < 0) || ($sy >= $HislandSize)) {
	 } else {
	     # 範囲内の場合
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
	     # 範囲内の場合
	     if($land->[$sx][$sy] == $HlandWaste) {
		 if($landValue->[$sx][$sy] == 2) {
		     return 1;
		 }
	     }
	 }
    }
    return 0;
}
 # 周囲に駅があるか判定
 sub countStation {
     my($land, $landValue, $x, $y) = @_;
     my($i, $sx, $sy);
     for($i = 1; $i < 5; $i++) {
          $sx = $x + $ax[$i];
          $sy = $y + $ay[$i];

          if(($sx < 0) || ($sx >= $HislandSize) ||
             ($sy < 0) || ($sy >= $HislandSize)) {
          } else {
              # 範囲内の場合
              if(($land->[$sx][$sy] == $HlandStation) && ($landValue->[$sx][$sy] >= 100))
              {
                # 駅である
                  return 1;
              }
          }
     }
     return 0;
 }

# 島全体
sub doIslandProcess {
    my($number, $island) = @_;

    # 導出値
    my($name) = $island->{'name'};
    my($id) = $island->{'id'};
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};

    # 地震判定
    if((random(1000) < (($island->{'prepare2'} + 1) * $HdisEarthquake)||($island->{'jisin'} >0))) {
	# 地震発生
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
		# 1/4で壊滅
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
# 土砂崩れ発生
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
# 範囲内の場合
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
# 効果なし地形
next;
} else {
# それ以外の場合
logEQfalldamage($id, $name, landName($landKind, $lv),$point);
$land->[$sx][$sy] = $HlandWaste;
$landValue->[$sx][$sy] = 0;
}# 地形
}# 範囲
}# 繰り返し(周囲1ヘックス)
}# 山

	}
    }
my($shoko) = $island->{'sigoto'}  * 10;
my($shopo) = $island->{'pop'} * 0.6;
    if($shoko <= $shopo) {
	# 不足メッセージ
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
		# 1/4で壊滅
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
    # 食料不足
    if($island->{'food'} <= 0) {
	# 不足メッセージ
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
		# 1/4で壊滅
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
# 大雨判定
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
    # 津波判定
    if((random(1000) < $HdisTsunami)||($island->{'tunami'} >0)) {
	# 津波発生
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
		# 1d12 <= (周囲の海 - 1) で崩壊
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

    # 怪獣判定
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
	    # 怪獣出現
	    # 種類を決める
	    my($lv, $kind);
	    if($island->{'monstersend'} > 0) {
		# 人造
		$kind = 0;
		$island->{'monstersend'}--;
 } elsif ($island->{'monstersend2'} > 0) {
		# 人造
		$kind = 22;
		$island->{'monstersend2'}--;
 } elsif ($island->{'monstersend3'} > 0) {
		# 人造
		$kind = 23;
		$island->{'monstersend3'}--;
 } elsif ($island->{'monstersend4'} > 0) {
		# 人造
		$kind = 24;
		$island->{'monstersend4'}--;
 } elsif ($island->{'monstersend5'} > 0) {
		# 人造
		$kind = 25;
		$island->{'monstersend5'}--;
	    } elsif($pop >= $HdisMonsBorder9) {
		# level3まで
		$kind = random($HmonsterLevel9) + 1;
	    } elsif($pop >= $HdisMonsBorder8) {
		# level3まで
		$kind = random($HmonsterLevel8) + 1;
	    } elsif($pop >= $HdisMonsBorder7) {
		# level3まで
		$kind = random($HmonsterLevel7) + 1;
	    } elsif($pop >= $HdisMonsBorder6) {
		# level2まで
		$kind = random($HmonsterLevel6) + 1;
	    } elsif($pop >= $HdisMonsBorder5) {
		# level3まで
		$kind = random($HmonsterLevel5) + 1;
	    } elsif($pop >= $HdisMonsBorder4) {
		# level2まで
		$kind = random($HmonsterLevel4) + 1;
	    } elsif($pop >= $HdisMonsBorder3) {
		# level3まで
		$kind = random($HmonsterLevel3) + 1;
	    } elsif($pop >= $HdisMonsBorder2) {
		# level2まで
		$kind = random($HmonsterLevel2) + 1;
	    } else {
		# level1のみ
		$kind = random($HmonsterLevel1) + 1;
	    }

	    # lvの値を決める
	    $lv = $kind * 10
		+ $HmonsterBHP[$kind] + random($HmonsterDHP[$kind]);

	    # どこに現れるか決める
	    my($bx, $by, $i);
	    for($i = 0; $i < $HpointNumber; $i++) {
		$bx = $Hrpx[$i];
		$by = $Hrpy[$i];
		if($land->[$bx][$by] == $HlandTown) {

		    # 地形名
		    my($lName) = landName($HlandTown, $landValue->[$bx][$by]);

		    # そのヘックスを怪獣に
		    $land->[$bx][$by] = $HlandMonster;
		    $landValue->[$bx][$by] = $lv;

		    # 怪獣情報
		    my($mKind, $mName, $mHp) = monsterSpec($lv);

		    # メッセージ
		    logMonsCome($id, $name, $mName, "($bx, $by)", $lName);
		    last;
		}
	    }
	}
    } while($island->{'monstersend'} > 0);

    # 地盤沈下判定
    if((($island->{'area'} > $HdisFallBorder) &&
       (random(1000) < $HdisFalldown)) ||($island->{'jiban'} >0)){
	# 地盤沈下発生
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

		# 周囲に海があれば、値を-1に
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
		# -1になっている所を浅瀬に
		$land->[$x][$y] = $HlandSea;
		$landValue->[$x][$y] = 1;
	    } elsif ($landKind == $HlandSea) {
		# 浅瀬は海に
		$landValue->[$x][$y] = 0;
	    }

	}
    }

    # 台風判定
    if((random(1000) < $HdisTyphoon)||($island->{'taifu'} >0)) {
	# 台風発生
	logTyphoon($id, $name);

	my($x, $y, $landKind, $lv, $i);
	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];

	    if(($landKind == $HlandFarm) ||
	       ($landKind == $HlandHaribote)) {

		# 1d12 <= (6 - 周囲の森) で崩壊
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

    # 巨大隕石判定
    if((random(1000) < $HdisHugeMeteo)||($island->{'daiin'} >0)) {
	my($x, $y, $landKind, $lv, $point);

	# 落下
	$x = random($HislandSize);
	$y = random($HislandSize);
	$landKind = $land->[$x][$y];
	$lv = $landValue->[$x][$y];
	$point = "($x, $y)";

	# メッセージ
	logHugeMeteo($id, $name, $point);

	# 広域被害ルーチン
	wideDamage($id, $name, $land, $landValue, $x, $y);
    }

    # 巨大ミサイル判定
    while($island->{'bigmissile'} > 0) {
	$island->{'bigmissile'} --;

	my($x, $y, $landKind, $lv, $point);

	# 落下
	$x = random($HislandSize);
	$y = random($HislandSize);
	$landKind = $land->[$x][$y];
	$lv = $landValue->[$x][$y];
	$point = "($x, $y)";

	# メッセージ
	logMonDamage($id, $name, $point);

	# 広域被害ルーチン
	wideDamage($id, $name, $land, $landValue, $x, $y);
    }

    # 隕石判定
    if((random(1000) < $HdisMeteo)||($island->{'inseki'} >0)) {
	my($x, $y, $landKind, $lv, $point, $first);
	$first = 1;
	while(random(2) == 0) {
	    $first = 0;
	    
	    # 落下
	    $x = random($HislandSize);
	    $y = random($HislandSize);
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];
	    $point = "($x, $y)";

	    if(($landKind == $HlandSea) && ($lv == 0)){
		# 海ポチャ
		logMeteoSea($id, $name, landName($landKind, $lv),
			    $point);
 } elsif($landKind == $HlandLake){
logMeteoSea($id, $name, landName($landKind, $lv),
			    $point);
next;
	    } elsif($landKind == $HlandMountain) {
		# 山破壊
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
		# 浅瀬
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

    # 噴火判定
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
		# 範囲内の場合
		$landKind = $land->[$sx][$sy];
		$lv = $landValue->[$sx][$sy];
		$point = "($sx, $sy)";
		if(($landKind == $HlandSea) ||
		   ($landKind == $HlandOil) ||
		   ($landKind == $HlandSbase)) {
		    # 海の場合
		    if($lv == 1) {
			# 浅瀬
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
		    # それ以外の場合
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

    # 食料があふれてたら換金
    if($island->{'food'} > 999999999) {
	$island->{'money'} += int(($island->{'food'} - 999999999) / 10);
$island->{'shuu'} += int(($island->{'food'} - 999999999) / 10);
	$island->{'food'} = 999999999;
    } 

    # 金があふれてたら切り捨て
    if($island->{'money'} > 999999999) {
	$island->{'money'} = 999999999;
    } 

    # 各種の値を計算
    estimate($number);

    # 繁栄、災難賞
    $pop = $island->{'pop'};
    my($damage) = $island->{'oldPop'} - $pop;
    my($prize) = $island->{'prize'};
    $prize =~ /([0-9]*),([0-9]*),(.*)/;
    my($flags) = $1;
    my($monsters) = $2;
    my($turns) = $3;

    # 繁栄賞
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

    # 災難賞
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

# 人口順にソート
sub islandSort {
    my($flag, $i, $tmp);

    # 人口が同じときは直前のターンの順番のまま
    my @idx = (0..$#Hislands);
    @idx = sort { $Hislands[$b]->{'pop'} <=> $Hislands[$a]->{'pop'} || $a <=> $b } @idx;
    @Hislands = @Hislands[@idx];
}

# 広域被害ルーチン
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

	# 範囲外判定
	if(($sx < 0) || ($sx >= $HislandSize) ||
	   ($sy < 0) || ($sy >= $HislandSize)) {
	    next;
	}

	# 範囲による分岐
	if($i < 7) {
	    # 中心、および1ヘックス
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
		    # 海
		    $landValue->[$sx][$sy] = 0;
		} else {
		    # 浅瀬
		    $landValue->[$sx][$sy] = 1;
		}
	    }
	} else {
	    # 2ヘックス
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

	# 範囲外判定
	if(($sx < 0) || ($sx >= $HislandSize) ||
	   ($sy < 0) || ($sy >= $HislandSize)) {
	    next;
	}

	# 範囲による分岐
	    # 中心、および1ヘックス
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

# ログへの出力
# 第1引数:メッセージ
# 第2引数:当事者
# 第3引数:相手
# 通常ログ
sub logOut {
    push(@HlogPool,"0,$HislandTurn,$_[1],$_[2],$_[0]");
}

# 遅延ログ
sub logLate {
    push(@HlateLogPool,"0,$HislandTurn,$_[1],$_[2],$_[0]");
}

# 機密ログ
sub logSecret {
    push(@HsecretLogPool,"1,$HislandTurn,$_[1],$_[2],$_[0]");
}

# 記録ログ
sub logHistory {
    open(HOUT, ">>${HdirName}/hakojima.his");
    print HOUT "$HislandTurn,$_[0]\n";
    close(HOUT);
}

# 記録ログ調整
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

# ログ書き出し
sub logFlush {
    open(LOUT, ">${HdirName}/hakojima.log0");

    # 全部逆順にして書き出す
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
# ログテンプレート
#----------------------------------------------------------------------
# 資金足りない
sub logNoMoney {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、資金不足のため中止されました。",$id);
}
sub lognooil {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で石油が不足しています。",$id);
}
# 食料足りない
sub logNoFood {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、備蓄食料不足のため中止されました。",$id);
}
sub lognasimina {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、港あるいは使用可能な港がないため中止されました。",$id);
}
sub logGomi {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}はゴミで町が汚れているので人々は島を去っていっています。",$id);
}
# 対象地形の種類による失敗
sub logLandFail {
    my($id, $name, $comName, $kind, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、予定地の${HtagName_}$point${H_tagName}が<B>$kind</B>だったため中止されました。",$id);
END
}
sub logNoKoku {
my($id, $name, $comName) = @_;
logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、軍総司令部がないため中止されました。",$id);
}
# 周りに陸がなくて埋め立て失敗
sub logNoLandAround {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、予定地の${HtagName_}$point${H_tagName}の周辺に陸地がなかったため中止されました。",$id);
END
}
sub logNoMounAround {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、予定地の${HtagName_}$point${H_tagName}の周辺に山がなかったため中止されました。",$id);
END
}
sub logNoSeaAround {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、予定地の${HtagName_}$point${H_tagName}の周辺に海がなかったため中止されました。",$id);
END
}
# 整地系成功
sub logLandSuc {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
END
}
 # 駅
 sub logStationSuc {
     my($id, $name, $comName, $point) = @_;
     logOut("${HtagName_}${name}島$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
END
}
 # 線路
 sub logRailSuc {
     my($id, $name, $comName, $point) = @_;
     logOut("${HtagName_}${name}島$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
 END
 }
# 油田発見
sub logOilFound {
    my($id, $name, $point, $comName, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}で<B>$str</B>の予算をつぎ込んだ${HtagComName_}${comName}${H_tagComName}が行われ、<B>油田が掘り当てられました</B>。",$id);
END
}
sub logOnseFound {
    my($id, $name, $point, $comName, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}で<B>$str</B>の予算をつぎ込んだ${HtagComName_}${comName}${H_tagComName}が行われ、<B>温泉が掘り当てられました</B>。",$id);
END
}
# 油田発見ならず
sub logOilFail {
    my($id, $name, $point, $comName, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}で<B>$str</B>の予算をつぎ込んだ${HtagComName_}${comName}${H_tagComName}が行われましたが、油田は見つかりませんでした。",$id);
END
}

sub logOnseFail {
    my($id, $name, $point, $comName, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}で<B>$str</B>の予算をつぎ込んだ${HtagComName_}${comName}${H_tagComName}が行われましたが、温泉は見つかりませんでした。",$id);
END
}

# 油田からの収入
sub logOilMoney {
    my($id, $name, $lName, $point, $str) = @_;
    logSecret("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>から、<B>$str</B>の石油が産出されました。",$id);
END
}
sub logOnseMoney {
    my($id, $name, $lName, $point, $str) = @_;
    logSecret("${HtagName_}${name}島$point${H_tagName}の<B>温泉</B>から、<B>$str</B>の収益が上がりました。",$id);
END
}

# 油田枯渇
sub logOilEnd {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は枯渇したようです。",$id);
END
}

# 防衛施設、自爆セット
sub logBombSet {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>の<B>自爆装置がセット</B>されました。",$id);
END
}

# 防衛施設、自爆作動
sub logBombFire {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>、${HtagDisaster_}自爆装置作動！！${H_tagDisaster}",$id);
END
}

# 記念碑、発射
sub logMonFly {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>が<B>轟音とともに飛び立ちました</B>。",$id);
END
}

# 記念碑、落下
sub logMonDamage {
    my($id, $name, $point) = @_;
    logOut("<B>何かとてつもないもの</B>が${HtagName_}${name}島$point${H_tagName}地点に落下しました！！",$id);
}

# 植林orミサイル基地
sub logPBSuc {
    my($id, $name, $comName, $point) = @_;
    logSecret("${HtagName_}${name}島$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
    logOut("こころなしか、${HtagName_}${name}島${H_tagName}の<B>森</B>が増えたようです。",$id);
END
}
sub logABSuc {
    my($id, $name, $comName, $point) = @_;
    logSecret("${HtagName_}${name}島$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
    logOut("${HtagName_}${name}島$point${H_tagName}で<${HtagComName_}整地${H_tagComName}が行われました。",$id);
END
}
# ハリボテ
sub logHariSuc {
    my($id, $name, $comName, $comName2, $point) = @_;
    logSecret("${HtagName_}${name}島$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
    logLandSuc($id, $name, $comName2, $point);
END
}

# 禁止行為
sub logNotPermitted {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、何者かの${HtagDisaster_}妨害${H_tagDisaster}により<B>阻止</B>されました。",$id);
}

# ミサイル撃とうとした(or 怪獣派遣しようとした)がターゲットがいない
sub logMsNoTarget {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、目標の島に人が見当たらないため中止されました。",$id);
END
}
sub logNoRazer {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、レーザー衛星を所有していないため中止されました。",$id);
END
}
sub logUnRazer {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、レーザー衛星が使用不能のため中止されました。",$id);
END
}
sub logNoPMS {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、PMS衛星を所有していないため中止されました。",$id);
END
}
sub logUnPMS {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、PMS衛星が使用不能のため中止されました。",$id);
END
}
# ミサイル撃とうとしたが基地がない
sub logMsNoBase {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、<B>ミサイル設備を保有していない</B>ために実行できませんでした。",$id);
END
}

sub logyoushoFail {
    my($id, $name, $point, $comName)= @_;
    logSecret("${HtagName_}${name}島$point${H_tagName}は浅瀬でないので${HtagComName_}${comName}${H_tagComName}は中止されました。",$id);
END
}
sub logzoukyou {
    my($id, $name, $point) = @_;
    logSecret("${HtagName_}${name}島$point${H_tagName}の施設を増強しました。",$id);
    logOut("${HtagName_}${name}島${H_tagName}で${HtagComName_}誘致活動${H_tagComName}が行われました。",$id);
END
}
sub logLanddeme {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、<B>すでに気象観測所を所有している</B>ため、実行できませんでした。",$id);
END
}
sub logLanddume {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、<B>すでにいのら研究所を所有している</B>ため、実行できませんでした。",$id);
END
}
sub logLanddime {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、<B>すでに特殊音波施設を所有している</B>ため、実行できませんでした。",$id);
END
}
sub logLanddame {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、<B>すでに気象研究所を所有している</B>ため、実行できませんでした。",$id);
END
}
# ミサイル撃ったが範囲外
sub logMsOut {
    my($id, $tId, $name, $tName, $comName, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、<B>領域外の海</B>に落ちた模様です。",$id, $tId);
}
sub logNsOut {
    my($id, $name, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島$tPoint${H_tagName}の低収束レーザー砲が${HtagName_}$point${H_tagName}地点に向けてレーザーを発射しましたが、<B>領域外の海</B>に落ちた模様です。",$id);
}

# ステルスミサイル撃ったが範囲外
sub logMsOutS {
    my($id, $tId, $name, $tName, $comName, $point) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、<B>領域外の海</B>に落ちた模様です。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島$point${H_tagName}へ向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、<B>領域外の海</B>に落ちた模様です。",$tId);
}

# ミサイル撃ったが防衛施設でキャッチ
sub logMsCaught {
    my($id, $tId, $name, $tName, $comName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}地点上空にて力場に捉えられ、<B>空中爆発</B>しました。",$id, $tId);
}
# ミサイル撃ったが軌道がそれ、別に島に
sub logMsMistake {
  my($id, $tId, $name, $oldtName) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${oldtName}島${H_tagName}に向けて発射したミサイルは、途中で軌道を変えました。",$id, $tId);
}
# ステルスミサイル撃ったが防衛施設でキャッチ
sub logMsCaughtS {
    my($id, $tId, $name, $tName, $comName, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}地点上空にて力場に捉えられ、<B>空中爆発</B>しました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島$point${H_tagName}へ向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}地点上空にて力場に捉えられ、<B>空中爆発</B>しました。",$tId);
}

# ミサイル撃ったが効果なし
sub logMsNoDamage {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちたので被害がありませんでした。",$id, $tId);
}
sub logXsNoDamage {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$tPoint${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、<B>$tLname</B>にだったので被害がありませんでした。",$id, $tId);
}
sub logNsNoDamage {
    my($id, $name, $tLname,$tPoint, $point, $cPoint) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の低精度レーザー砲が${HtagName_}$tPoint${H_tagName}地点に向けてレーザー発射を行いましたが、${HtagName_}$cPoint${H_tagName}の<B>$tLname</B>に落ちたので被害がありませんでした。",$id);
}
# ステルスミサイル撃ったが効果なし
sub logMsNoDamageS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちたので被害がありませんでした。",$id, $tId);

    logLate("<B>何者か</B>が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちたので被害がありませんでした。",$tId);
}
sub logMsNoDamageT {
    my($id, $name, $tLname, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>が火の玉を吐きましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちたので被害がありませんでした。",$id);
}
sub logdasuyo {
    my($id, $name, $mName, $point,$tPoint,$tLname) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>が核兵器を発射し、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。",$id);
}
sub logdasuyoZ {
    my($id, $name, $mName, $point,$tPoint,$tLname) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>が核バズーカーを発射し、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。",$id);
}
sub logmonkamiT {
    my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>が火の玉を吐き、${HtagName_}$tPoint${H_tagName}の<B>怪獣$kName</B>に命中、しかしバリアーに阻まれ効果がありませんでした。",$id);
}
sub lognodamageT {
    my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>が火の玉を吐き、${HtagName_}$tPoint${H_tagName}の<B>怪獣$kName</B>に命中、しかし硬化中だったため効果がありませんでした。",$id);
}
sub logMsMonKillT {
    my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>が火の玉を吐き、${HtagName_}$tPoint${H_tagName}の<B>怪獣$kName</B>に命中。<B>怪獣$kName</B>は力尽き、倒れました。",$id);
}
sub logMsMonsterT {
my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>が火の玉を吐き、${HtagName_}$tPoint${H_tagName}の<B>怪獣$kName</B>に命中。<B>怪獣$kName</B>は苦しそうに咆哮しました。",$id);
}
sub logMsNormalT {
my($id, $name, $tLname, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>が火の玉を吐き、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、一帯が壊滅しました。",$id, $tId);
}
sub logMsNoDamageU {
    my($id, $name, $tLname, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>が砲弾を発射しましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちたので被害がありませんでした。",$id);
}
sub logmonkamiU {
    my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>が砲弾を発射し、${HtagName_}$tPoint${H_tagName}の<B>怪獣$kName</B>に命中、しかしバリアーに阻まれ効果がありませんでした。",$id);
}
sub lognodamageU {
    my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>が砲弾を発射し、${HtagName_}$tPoint${H_tagName}の<B>怪獣$kName</B>に命中、しかし硬化中だったため効果がありませんでした。",$id);
}
sub logMsMonKillU {
    my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>が砲弾を発射し、${HtagName_}$tPoint${H_tagName}の<B>怪獣$kName</B>に命中。<B>怪獣$kName</B>は力尽き、倒れました。",$id);
}
sub logMsMonsterU {
my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>が砲弾を発射し、${HtagName_}$tPoint${H_tagName}の<B>怪獣$kName</B>に命中。<B>怪獣$kName</B>は苦しそうに咆哮しました。",$id);
}
sub logMsNormalU {
my($id, $name, $tLname, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>が砲弾を発射し、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、一帯が壊滅しました。",$id, $tId);
}
sub logMsNoDamageV {
    my($id, $name, $tLname, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>がライフルを発射しましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちたので被害がありませんでした。",$id);
}
sub logmonkamiV {
    my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>がライフルを発射し、${HtagName_}$tPoint${H_tagName}の<B>怪獣$kName</B>に命中、しかしバリアーに阻まれ効果がありませんでした。",$id);
}
sub lognodamageV {
    my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>がライフルを発射し、${HtagName_}$tPoint${H_tagName}の<B>怪獣$kName</B>に命中、しかし硬化中だったため効果がありませんでした。",$id);
}
sub logMsMonKillV {
    my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>がライフルを発射し、${HtagName_}$tPoint${H_tagName}の<B>怪獣$kName</B>に命中。<B>怪獣$kName</B>は力尽き、倒れました。",$id);
}
sub logMsMonsterV {
my($id, $name, $kName, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>がライフルを発射し、${HtagName_}$tPoint${H_tagName}の<B>怪獣$kName</B>に命中。<B>怪獣$kName</B>は苦しそうに咆哮しました。",$id);
}
sub logMsNormalV {
my($id, $name, $tLname, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>がライフルを発射し、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、一帯が壊滅しました。",$id);
}
sub logMsNoDamageX {
    my($id, $name, $tLname, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>が未知の兵器を発射しましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちたので被害がありませんでした。",$id);
}
sub logMsNormalX {
my($id, $name, $tLname, $mName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}${HtagName_}$point${H_tagName}の<B>怪獣$mName</B>が未知の兵器を発射し、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、水没しました。",$id, $tId);
}
# 陸地破壊弾、山に命中
sub logMsLDMountain {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は消し飛び、荒地と化しました。",$id, $tId);
}

# 陸地破壊弾、海底基地に命中
sub logMsLDSbase {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}に着水後爆発、同地点にあった<B>$tLname</B>は跡形もなく吹き飛びました。",$id, $tId);
}

# 陸地破壊弾、怪獣に命中
sub logMsLDMonster {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}に着弾し爆発。陸地は<B>怪獣$tLname</B>もろとも水没しました。",$id, $tId);
}

# 陸地破壊弾、浅瀬に命中
sub logMsLDSea1 {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。海底がえぐられました。",$id, $tId);
}

# 陸地破壊弾、その他の地形に命中
sub logMsLDLand {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。陸地は水没しました。",$id, $tId);
}

# 通常ミサイル、荒地に着弾
sub logMsWaste {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちました。",$id, $tId);
}
sub logNsWaste {
    my($id, $name, $tLname,$tPoint, $point, $cPoint) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の低精度レーザー砲が${HtagName_}$tPoint${H_tagName}地点に向けてレーザー発射を行いましたが、${HtagName_}$cPoint${H_tagName}の<B>$tLname</B>に落ちました。",$id);
}

# ステルスミサイル、荒地に着弾
sub logMsWasteS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちました。",$tId);
}

# 通常ミサイル、怪獣に命中、硬化中にて無傷
sub logMsMonNoDamage {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中、しかし硬化状態だったため効果がありませんでした。",$id, $tId);
}
sub logNsMonNoDamage {
    my($id, $name, $tLname,$tPoint, $point, $cPoint) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の低精度レーザー砲が${HtagName_}$tPoint${H_tagName}地点に向けてレーザー発射を行い、${HtagName_}$cPoint${H_tagName}の<B>怪獣$tLname</B>に命中、しかし硬化状態だったため効果がありませんでした。",$id);
}
sub logNsMonNoDamageKami {
    my($id, $name, $tLname,$tPoint, $point, $cPoint) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の低精度レーザー砲が${HtagName_}$tPoint${H_tagName}地点に向けてレーザー発射を行い、${HtagName_}$cPoint${H_tagName}の<B>怪獣$tLname</B>に命中、しかしバリアーに阻まれ効果がありませんでした。",$id);
}
# ステルスミサイル、怪獣に命中、硬化中にて無傷
sub logMsMonNoDamageS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中、しかし硬化状態だったため効果がありませんでした。",$id, $tId);
    logOut("<B>何者か</B>が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中、しかし硬化状態だったため効果がありませんでした。",$tId);
}
sub logmonkami {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中、しかしバリアーに阻まれ効果がありませんでした。",$id, $tId);
}
# 通常ミサイル、怪獣に命中、殺傷
sub logMsMonKill {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中。<B>怪獣$tLname</B>は力尽き、倒れました。",$id, $tId);
}
sub logNsMonKill {
    my($id, $name, $tLname,$tPoint, $point, $cPoint) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の低精度レーザー砲が${HtagName_}$tPoint${H_tagName}地点に向けてレーザー発射を行い、${HtagName_}$cPoint${H_tagName}の<B>怪獣$tLname</B>に命中。<B>怪獣$tLname</B>は力尽き、倒れました。",$id);}

# ステルスミサイル、怪獣に命中、殺傷
sub logMsMonKillS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中。<B>怪獣$tLname</B>は力尽き、倒れました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中。<B>怪獣$tLname</B>は力尽き、倒れました。", $tId);
}

# 通常ミサイル、怪獣に命中、ダメージ
sub logMsMonster {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中。<B>怪獣$tLname</B>は苦しそうに咆哮しました。",$id, $tId);
}
sub logNsMonster {
    my($id, $name, $tLname,$tPoint, $point, $cPoint) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の低精度レーザー砲が${HtagName_}$tPoint${H_tagName}地点に向けてレーザー発射を行い、${HtagName_}$cPoint${H_tagName}の<B>怪獣$tLname</B>に命中。<B>怪獣$tLname</B>は苦しそうに咆哮しました。",$id);
}
# 栄養、怪獣に命中、回復
sub logMsMonsterH {
my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中。<B>怪獣$tLname</B>はみるみる元気になりました。",$id, $tId);
}

# 栄養、怪獣に命中、これ以上回復しない
sub logMsMonsterM {
my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中。しかしなにも起こりませんでした。",$id, $tId);
}
# ステルスミサイル、怪獣に命中、ダメージ
sub logMsMonsterS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中。<B>怪獣$tLname</B>は苦しそうに咆哮しました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中。<B>怪獣$tLname</B>は苦しそうに咆哮しました。",$tId);
}
# 陸地生成弾、怪獣に命中
sub logMsREMonster {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。怪獣<B>$tLname</B>は隆起に飲みこまれました。",$id, $tId);
}
sub logXsREMonster {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$tPoint${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、怪獣<B>$tLname</B>は隆起に飲みこまれました。",$id, $tId);
}
# 陸地生成弾、海に命中
sub logMsRESea {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。海底が隆起して浅瀬になりました。",$id, $tId);
}
sub logXsRESea {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$tPoint${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、<B>$tLname</B>が隆起,浅瀬になりました。",$id, $tId);
}
# 陸地生成弾、浅瀬に命中
sub logMsRESea1 {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。浅瀬が隆起し陸地になりました。",$id, $tId);
}
sub logXsRESea1 {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$tPoint${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、<B>$tLname</B>が隆起,陸地になりました。",$id, $tId);
}
# 陸地生成弾、海底基地に命中
sub logMsRESbase {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。隆起のため海底基地は破壊されました",$id, $tId);
}
sub logXsRESbase {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$tPoint${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、<B>$tLname</B>が隆起、海底基地は破壊されました",$id, $tId);
}

# 陸地生成弾、油田に命中
sub logMsREOil {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。隆起のため油田は破壊されました。",$id, $tId);
}
sub logMsREYou {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。隆起のため養殖場は破壊されました。",$id, $tId);
}
sub logXsREOil {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$tPoint${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、<B>$tLname</B>が隆起、油田は破壊されました。",$id, $tId);
}
sub logXsREYou {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$tPoint${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、<B>$tLname</B>が隆起、養殖場は破壊されました。",$id, $tId);
}
# 陸地生成弾、その他の地形に命中
sub logMsRELand {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。陸地が隆起し山ができました。",$id, $tId);
}
sub logXsRELand {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$tPoint${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、<B>$tLname</B>が隆起、山ができました。",$id, $tId);
}
# 怪獣の死体
sub logMsMonMoney {
    my($tId, $mName, $value, $name) = @_;
    logOut("<B>怪獣$mName</B>の残骸には、<B>$value$HunitMoney</B>の値が付きました。また怪獣を倒した${HtagName_}${name}島${H_tagName}には<B>$value$HunitMoney</B>の懸賞金が払われました。",$tId);
}

# 通常ミサイル通常地形に命中
sub logMsNormal {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、一帯が壊滅しました。",$id, $tId);
}
sub logNsNormal {
    my($id, $name, $tLname,$tPoint, $point, $cPoint) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の低精度レーザー砲が${HtagName_}$tPoint${H_tagName}地点に向けてレーザー発射を行い、${HtagName_}$cPoint${H_tagName}の<B>$tLname</B>に命中、一帯が壊滅しました。",$id);
}
# ステルスミサイル通常地形に命中
sub logMsNormalS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、一帯が壊滅しました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、一帯が壊滅しました。",$tId);
}
# 中性子弾、着弾
sub logMsNeutron {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}地点上空で炸裂しました。",$id, $tId);
}
# ミサイル難民到着
sub logMsBoatPeople {
    my($id, $name, $achive) = @_;
    logOut("${HtagName_}${name}島${H_tagName}にどこからともなく<B>$achive${HunitPop}もの難民</B>が漂着しました。${HtagName_}${name}島${H_tagName}は快く受け入れたようです。",$id);
}
sub logWideDamageSeaDead {
    my($id, $tId, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は<B>全滅</B>したようです。",$id,$tId);
}
sub logWideDamageSeaDead2 {
    my($id, $tId, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は<B>大ダメージ</B>を受けたようです。",$id,$tId);
}
sub logWideDamageMonsterDead {
    my($id, $tId,$name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣$lName</B>は息絶えました。",$id,$tId);
}
sub logWideDamageMonsterDead2 {
    my($id, $tId,$name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣$lName</B>大ダメージ</B>を受けたようです。",$id,$tId);
}
sub logWideDamageDead {
    my($id, $tId, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>にいた人々は<B>全滅</B>したようです。",$id,$tId);
}
sub logsandoi {
    my($id, $name, $tLname,$mName, $point,$tPoint) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣$mName</B>の出す砂に${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>は飲み込まれました。",$id);
}

sub logmoerui {
    my($id, $name, $tLname,$mName, $point,$tPoint) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣$mName</B>の出す炎によって${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>は燃え尽きました。",$id);
}
# 怪獣派遣
sub logMonsSend {
    my($id, $tId, $name, $tName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>人造怪獣</B>を建造。${HtagName_}${tName}島${H_tagName}へ送りこみました。",$id, $tId);
}
sub logMonsSendDamez {
    my($id, $tId, $name, $tName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>人造怪獣</B>を建造しようとしましたが<b>いのら研究所</b>のレベルが足りませんでした。",$id, $tId);
}

# 資金繰り
sub logDoNothing {
    my($id, $name, $comName) = @_;
#    logOut("${HtagName_}${name}島${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
}

# 輸出
sub logSell {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>$value$HunitFood</B>の${HtagComName_}${comName}${H_tagComName}を行いました。",$id);
}
sub logOilSell {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>$valueトン</B>の${HtagComName_}${comName}${H_tagComName}を行いました。",$id);
}
# 援助
sub logAid {
    my($id, $tId, $name, $tName, $comName, $str) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}へ<B>$str</B>の${HtagComName_}${comName}${H_tagComName}を行いました。",$id, $tId);
}
sub logAidH {
my($id, $tId, $name, $tName, $comName, $str) = @_;
logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}へ<B>$str</B>の${HtagComName_}${comName}${H_tagComName}を行いました。",$id, $tId);
logLate("何者かが${HtagName_}${tName}島${H_tagName}に<B>$str</B>の${HtagComName_}${comName}${H_tagComName}を行いました。",$tId);
}
sub logshamo {
    my($id, $name, $str) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}は<B>$str億円</B>を返しました。",$id);
}
sub logShaku {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>$value億円</B>の${HtagComName_}${comName}${H_tagComName}を行いました。",$id);
}
sub logShakubame {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagComName_}${comName}${H_tagComName}を行おうとしましたがすでに借り入れをしているので計画を中止しました。",$id);
}
sub logOitekyo {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の油田を撤去しました。",$id,);
}
sub logyotekyo {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の養殖場を撤去しました。",$id,);
}
sub logminatekyo {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の港を撤去しました。",$id,);
}
sub logtekyoFail {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}には海上建築はないので計画を中止しました。",$id,);
}
# 誘致活動
sub logPropaganda {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
}
 # 怪獣、地雷を踏む
 sub logMonsMoveMine {
     my($id, $name, $lName, $point, $mName) = @_;
     logOut("<B>怪獣$mName</B>が${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>を踏み、<B>${lName}が爆発しました！！</B>",$id);
}

 # 怪獣、地雷を踏んだ後も生存
 sub logMonsMoveMineAlive {
     my($id, $name, $lName, $point, $mName) = @_;
     logOut("<B>怪獣$mName</B>は苦しそうに咆哮しました。",$id);
}

 # 怪獣、地雷を踏んだ後に死亡
 sub logMonsMoveMineDead {
     my($id, $name, $lName, $point, $mName) = @_;
     logOut("<B>怪獣$mName</B>は力尽き、倒れました。",$id);
}

 # 怪獣、地雷を踏んだ後に吹き飛ぶ
 sub logMonsMoveMineScatter {
     my($id, $name, $lName, $point, $mName) = @_;
     logOut("<B>怪獣$mName</B>は跡形もなく吹き飛びました。",$id);
}

# 放棄
sub logGiveup {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}は放棄され、<B>無人島</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、放棄され<B>無人島</B>となる。");
}
sub logsen {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}は<B>平和愛好同盟</B>に加盟しているため、<B>戦争愛好同盟</B>には加盟できません。",$id);
}
sub loghei {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}は<B>戦争愛好同盟</B>に加盟しているため、<B>平和愛好同盟</B>には加盟できません。",$id);
}
sub logkouk {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>攻撃衛星</B>は強化されました。",$id);
}
sub logkank {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>監視衛星</B>は強化されました。",$id);
}
sub logbouk {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>防御衛星</B>は強化されました。",$id);
}
sub logreik {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>レーザー衛星</B>は強化されました。",$id);
}
sub loghatk {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>発電衛星</B>は強化されました。",$id);
}
sub logemtk {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>PMS衛星</B>は強化されました。",$id);
}
sub logemtx {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>レーザー衛星</B>は<B>PMS衛星</B>に改造されました。",$id);
}
sub logemty {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}は<B>レーザー衛星</B>を所有していないので計画は中止されました。",$id);
}
sub logkouei {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の${HtagComName_}${comName}${H_tagComName}は成功しました。",$id);
}
sub logdamekouei {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の${HtagComName_}${comName}${H_tagComName}は失敗しました。",$id);
}
sub logkouuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}の攻撃衛星を撃ち落としました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島${H_tagName}の攻撃衛星を撃ち落としました",$tId);
}
sub logpmsuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}のPMS衛星を撃ち落としました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島${H_tagName}のPMS衛星を撃ち落としました",$tId);
}

sub logkoueikurukuru {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}はすでにPMS衛星を持っているため${HtagComName_}${comName}${H_tagComName}は実行できませんでした。",$id, $tId);
}
sub logkanuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}の監視衛星を撃ち落としました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島${H_tagName}の監視衛星を撃ち落としました",$tId);
}
sub logbouuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}の防御衛星を撃ち落としました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島${H_tagName}の防御衛星を撃ち落としました",$tId);
}
sub logreiuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}のレーザー衛星を撃ち落としました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島${H_tagName}のレーザー衛星を撃ち落としました",$tId);
}
sub loghatuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}の発電衛星を撃ち落としました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島${H_tagName}の発電衛星を撃ち落としました",$tId);
}
sub logdamebouuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}の防御衛星を撃ち落とそうとしましたが失敗しました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島${H_tagName}の防御衛星を撃ち落とそうとしましたが失敗しました。",$tId);
}
sub logdamehatuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}の発電衛星を撃ち落とそうとしましたが失敗しました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島${H_tagName}の発電衛星を撃ち落とそうとしましたが失敗しました。",$tId);
}
sub logdamereiuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}のレーザー衛星を撃ち落とそうとしましたが失敗しました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島${H_tagName}のレーザー衛星を撃ち落とそうとしましたが失敗しました。",$tId);
}
sub logdamekouuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}の攻撃衛星を撃ち落とそうとしましたが失敗しました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島${H_tagName}の攻撃衛星を撃ち落とそうとしましたが失敗しました。",$tId);
}
sub logdamepmsuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}のPMS衛星を撃ち落とそうとしましたが失敗しました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島${H_tagName}のPMS衛星を撃ち落とそうとしましたが失敗しました。",$tId);
}
sub logsaikou {
    my($id, $target,$name, $tName, $comName) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}に向けて${HtagComName_}${comName}${H_tagComName}を行いました。",$id, $tId);
    logOut("<B>何者か</B>が${HtagName_}${tName}島${H_tagName}に向けて${HtagComName_}${comName}${H_tagComName}を行いました。",$tId);
}
sub logjisaikou {
    my($id, $target,$name, $tName, $comName) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが失敗し、機械が暴走しました。",$id, $tId);
}

sub logsiyou {
    my($id, $name) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}のレーザー衛星は使用可能になりました。",$id);
}
sub logsiyouZ {
    my($id, $name) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}のPMS衛星は使用可能になりました。",$id);
}
sub lognasi {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}は気象研究所を所有していないため、${HtagComName_}${comName}${H_tagComName}を行えません。",$id);
}
sub logsisai {
    my($id, $target,$name, $tName, $comName) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが失敗しました。",$id, $tId);
    logOut("<B>何者か</B>が${HtagName_}${tName}島${H_tagName}に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが失敗しました。",$tId);
}
sub logsaimitu {
    my($id, $target,$name, $tName, $comName) = @_;
    logOut("${HtagName_}${tName}島${H_tagName}の気象観測所の解析の結果、${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}に向けて${HtagComName_}${comName}${H_tagComName}を行ったことがわかりました。",$id, $tId);
}
sub logdamekanuti {
    my($id, $tId, $name, $tName) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}の監視衛星を撃ち落とそうとしましたが失敗しました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島${H_tagName}の監視衛星を撃ち落とそうとしましたが失敗しました。",$tId);
}

sub logmitukaru {
my($id, $tId, $name, $tName, $comName) = @_;
logLate("${HtagName_}${tName}島${H_tagName}の監視衛星からのデータの解析の結果、${HtagName_}${name}島${H_tagName}が${HtagComName_}${comName}${H_tagComName}をしたことがわかりました。",$id, $tId);}
sub logteiko {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}は${HtagComName_}${comName}${H_tagComName}しました。",$id);
}
sub logteikyo {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}は他陣営に属しているため${HtagComName_}${comName}${H_tagComName}はできません。",$id);
}
sub logteimu {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}は戦争愛好同盟に入っていないため${HtagComName_}${comName}${H_tagComName}はできません。",$id);
}
sub logInoknasi {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}は${HtagComName_}${comName}${H_tagComName}を行おうとしましたが<b>いのら研究所</b>がないため、実行できませんでした。",$id);
}
sub logForest {
my($id, $name, $lName, $point) = @_;
logSecret("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は、<B>森</B>になりました。",$id);
}
sub logsabaku {
my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は、<B>砂地</B>になりました。",$id);
}
sub logMati {
my($id, $name, $lName, $point) = @_;
logSecret("${HtagName_}${name}島$point${H_tagName}に<B>村</B>ができました。",$id);
}
sub logsougen {
my($id, $name, $lName, $point) = @_;
logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は、<B>平地</B>になりました。",$id);
}
sub logareti {
my($id, $name, $lName, $point) = @_;
logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は、<B>荒地</B>になりました。",$id);
}
sub logGeki {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}は${HtagComName_}${comName}${H_tagComName}を行い成功しました。",$id);
}
sub logGekidame {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}は${HtagComName_}${comName}${H_tagComName}を行いましたが失敗しました。",$id);
}

# 死滅
sub logDead {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}から人がいなくなり、<B>無人島</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、人がいなくなり<B>無人島</B>となる。");
}

# 発見
sub logDiscover {
    my($name) = @_;
    logHistory("${HtagName_}${name}島${H_tagName}が発見される。");
}

# 名前の変更
sub logChangeName {
    my($name1, $name2) = @_;
    logHistory("${HtagName_}${name1}島${H_tagName}、名称を${HtagName_}${name2}島${H_tagName}に変更する。");
}

# 飢餓
sub logStarve {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の${HtagDisaster_}食料が不足${H_tagDisaster}しています！！",$id);
}
# 飢餓
sub logShorve {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の${HtagDisaster_}仕事が不足${H_tagDisaster}しています！！",$id);
}
sub logMizrve {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の${HtagDisaster_}水が不足${H_tagDisaster}しています！！",$id);
}
# 怪獣現る
sub logMonsCome {
    my($id, $name, $mName, $point, $lName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}に<B>怪獣$mName</B>出現！！${HtagName_}$point${H_tagName}の<B>$lName</B>が踏み荒らされました。",$id);
}
sub logkamikas {
    my($id, $name,$point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣いのら神</B>は<B>火災</B>を引き起こしました。",$id);
}
sub logkamifuu {
    my($id, $name,$point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣いのら神</B>は<B>台風</B>を呼びました。",$id);
}
sub logkaminam {
    my($id, $name,$point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣いのら神</B>は<B>津波</B>を呼びました。",$id);
}
sub logkamifun {
    my($id, $name,$point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣いのら神</B>は<B>噴火</B>を引き起こしました。",$id);
}
sub logkamiins {
    my($id, $name,$point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣いのら神</B>は<B>隕石</B>を呼びました。",$id);
}
sub logkamidai {
    my($id, $name,$point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣いのら神</B>は<B>大隕石</B>を呼びました。",$id);
}
sub logkamijis {
    my($id, $name,$point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣いのら神</B>は<B>地震</B>を呼びました。",$id);
}
sub logkamijib {
    my($id, $name,$point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣いのら神</B>は<B>地盤沈下</B>を引き起こしました。",$id);
}
# 怪獣、ワープ地雷によって転送される
 sub logMonsMoveMineWarp {
     my($id, $name, $lName, $point, $mName, $tId, $tName) = @_;
     logOut("<B>怪獣$mName</B>が${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>を踏み、<B>${lName}が発動しました！！</B>",$id);
     logOut("<B>怪獣$mName</B>が${HtagName_}${name}島${H_tagName}の<B>$lName</B>によって${HtagName_}${tName}島${H_tagName}へ転送されました。",$id, $tId);
}
sub logMonsterkak {
    my($id, $name, $point, $mName) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣$mName</B>は覚醒し、カウントダウンいのらになりました。",$id);
}
# 怪獣動く
sub logMonsMove {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>が<B>怪獣$mName</B>に踏み荒らされました。",$id);
}
sub logMonsFarm {
    my($id, $name, $point, $mName) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>農場</B>が<B>怪獣$mName</B>に食い荒らされました。",$id);
}
# 怪獣帰る
sub logQee {
    my($id, $name, $point, $mName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>怪獣$mName</B>が${HtagName_}$point${H_tagName}にいのらエッグを生みました。",$id);
}
sub logmada {
    my($id, $name, $point, $mName) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$mName</B>はまだ卵のままです。",$id);
}

sub logEgg {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の${HtagName_}$point${H_tagName}にある<B>いのらエッグ</B>が孵り<B>いのらベイビー</B>が生まれました。",$id);
}
sub loghenka {
    my($id, $name, $mName, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の${HtagName_}$point${H_tagName}にいる<B>怪獣いのらベイビー</B>が<B>$mName</B>に成長しました。",$id);
}
# 怪獣、防衛施設を踏む
sub logMonsMoveDefence {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("<B>怪獣$mName</B>が${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>へ到達、<B>${lName}の自爆装置が作動！！</B>",$id);
}
# 怪獣帰る
sub logkaeru {
    my($id, $name, $mName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣$mName</B>が島を去りました。",$id);
}
# 火災
sub logFire {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>が${HtagDisaster_}火災${H_tagDisaster}により壊滅しました。",$id);
}
sub logDis {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>で${HtagDisaster_}伝染病${H_tagDisaster}が蔓延しました。",$id);
}
# 埋蔵金
sub logaka {
    my($id, $name, $lName,$point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>で${HtagDisaster_}赤潮${H_tagDisaster}が発生、収穫が激減しました。",$id);
}
sub logMaizo {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}島${H_tagName}での${HtagComName_}$comName${H_tagComName}中に、<B>$value$HunitMoneyもの埋蔵金</B>が発見されました。",$id);
}

# 地震発生
sub logEarthquake {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で大規模な${HtagDisaster_}地震${H_tagDisaster}が発生！！",$id);
}
# 土砂崩れ
sub logEQfall {
my($id, $name, $lName, $point) = @_;
logLate("${HtagName_}${name}島$point${H_tagName}地点の<B>$lname</B>で${HtagDisaster_}土砂崩れ${H_tagDisaster}が発生！",$id);
}
# 土砂崩れ、被害
sub logEQfalldamage {
my($id, $name, $lName, $point) = @_;
logLate("${HtagName_}${name}島$point${H_tagName}地点の<B>$lName</B>は、${HtagDisaster_}土砂崩れ${H_tagDisaster}の影響で壊滅しました。",$id);
}
# 地震被害
sub logEQDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}地震${H_tagDisaster}により壊滅しました。",$id);
}
sub logBODamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}地震${H_tagDisaster}により崩れました。",$id);
}
# 食料不足被害
sub logSvDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>に<B>食料を求めて住民が殺到</B>。<B>$lName</B>は壊滅しました。",$id);
}
sub logSyDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>に<B>失業者が暴徒となり来襲</B>。<B>$lName</B>は壊滅しました。",$id);
}
# 津波発生
sub logTsunami {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}付近で${HtagDisaster_}津波${H_tagDisaster}発生！！",$id);
}
sub logHardRain {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で${HtagDisaster_}大雨${H_tagDisaster}発生！！",$id);
}
sub logtree {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>森林</B>は潤いました。",$id);
}
# 津波被害
sub logTsunamiDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}津波${H_tagDisaster}により崩壊しました。",$id);
}

# 台風発生
sub logTyphoon {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}に${HtagDisaster_}台風${H_tagDisaster}上陸！！",$id);
}

# 台風被害
sub logTyphoonDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}台風${H_tagDisaster}で飛ばされました。",$id);
}

# 隕石、海
sub logMeteoSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>に${HtagDisaster_}隕石${H_tagDisaster}が落下しました。",$id);
}

# 隕石、山
sub logMeteoMountain {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>に${HtagDisaster_}隕石${H_tagDisaster}が落下、<B>$lName</B>は消し飛びました。",$id);
}

# 隕石、海底基地
sub logMeteoSbase {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>に${HtagDisaster_}隕石${H_tagDisaster}が落下、<B>$lName</B>は崩壊しました。",$id);
}

# 隕石、怪獣
sub logMeteoMonster {
    my($id, $name, $lName, $point) = @_;
    logOut("<B>怪獣$lName</B>がいた${HtagName_}${name}島$point${H_tagName}地点に${HtagDisaster_}隕石${H_tagDisaster}が落下、陸地は<B>怪獣$lName</B>もろとも水没しました。",$id);
}

# 隕石、浅瀬
sub logMeteoSea1 {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}地点に${HtagDisaster_}隕石${H_tagDisaster}が落下、海底がえぐられました。",$id);
}

# 隕石、その他
sub logMeteoNormal {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}地点の<B>$lName</B>に${HtagDisaster_}隕石${H_tagDisaster}が落下、一帯が水没しました。",$id);
}

# 隕石、その他
sub logHugeMeteo {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}地点に${HtagDisaster_}巨大隕石${H_tagDisaster}が落下！！",$id);
}
sub logUCmiss {
my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}に着弾。",$id, $tId);
}
sub logkanoti {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>監視衛星</B>が大気圏に突入、消滅しました。",$id);
}
sub loghatoti {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>発電衛星</B>が大気圏に突入、消滅しました。",$id);
}
sub logreioti {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>レーザー衛星</B>が大気圏に突入、消滅しました。",$id);
}
sub logpmsoti {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>PMS衛星</B>が大気圏に突入、消滅しました。",$id);
}
sub logkouoti {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>攻撃衛星</B>が大気圏に突入、消滅しました。",$id);
}
sub logbouoti {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>防御衛星</B>が大気圏に突入、消滅しました。",$id);
}
# 噴火
sub logEruption {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}地点で${HtagDisaster_}火山が噴火${H_tagDisaster}、<B>山</B>が出来ました。",$id);
}

# 噴火、浅瀬
sub logEruptionSea1 {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}地点の<B>$lName</B>は、${HtagDisaster_}噴火${H_tagDisaster}の影響で陸地になりました。",$id);
}

# 噴火、海or海基
sub logEruptionSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}地点の<B>$lName</B>は、${HtagDisaster_}噴火${H_tagDisaster}の影響で海底が隆起、浅瀬になりました。",$id);
}

# 噴火、その他
sub logEruptionNormal {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}地点の<B>$lName</B>は、${HtagDisaster_}噴火${H_tagDisaster}の影響で壊滅しました。",$id);
}

# 地盤沈下発生
sub logFalldown {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で${HtagDisaster_}地盤沈下${H_tagDisaster}が発生しました！！",$id);
}

# 地盤沈下被害
sub logFalldownLand {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は海の中へ沈みました。",$id);
}

# 広域被害、水没
sub logWideDamageSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は<B>水没</B>しました。",$id);
}

# 広域被害、海の建設
sub logWideDamageSea2 {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は跡形もなくなりました。",$id);
}

# 広域被害、怪獣水没
sub logWideDamageMonsterSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の陸地は<B>怪獣$lName</B>もろとも水没しました。",$id);
}
sub logMonsterBom {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣$lName</B>は自爆し、周りに甚大な被害を及ぼしました。",$id);
}
sub logMonmon {
    my($id, $name, $point,$mName, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣$mName</B>は<b>$str</b>を落としました。",$id);
}
sub logMonUtiDame {
    my($id, $name, $point,$mName) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣$mName</B>は火の玉をはきましたが，<B>領域外の海</B>に落ちた模様です。",$id);
}
sub logMonUtiDameU {
    my($id, $name, $point,$mName) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣$mName</B>が砲弾を発射しましたが，<B>領域外の海</B>に落ちた模様です。",$id);
}
sub logMonUtiDameV {
    my($id, $name, $point,$mName) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣$mName</B>がライフルを発射しましたが，<B>領域外の海</B>に落ちた模様です。",$id);
}
sub logMonUtiDameX {
    my($id, $name, $point,$mName) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣$mName</B>は未知の兵器を発射しましたが，<B>領域外の海</B>に落ちた模様です。",$id);
}
sub logMonUtiDameZ {
    my($id, $name, $point,$mName) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣$mName</B>は核バズーカーを発射しましたが，<B>領域外の海</B>に落ちた模様です。",$id);
}
sub logMonUtiDameY {
    my($id, $name, $point,$mName) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣$mName</B>は核兵器を発射しましたが，<B>領域外の海</B>に落ちた模様です。",$id);
}
sub logMontue {
    my($id, $name, $point,$mName, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣$mName</B>は$strを奪いました。",$id);
}
# 広域被害、怪獣
sub logWideDamageMonster {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣$lName</B>は消し飛びました。",$id);
}

# 広域被害、怪獣
sub loghobakukaijo {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>怪獣$lName</B>は捕縛から逃れました。",$id);
}
# 広域被害、荒地
sub logWideDamageWaste {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は一瞬にして<B>荒地</B>と化しました。",$id);
}
# 動物園からの収入 # ここから
sub logdoubutuMoney {
my($id, $name, $lName, $point, $str) = @_;
logSecret("${HtagName_}${name}島$point${H_tagName}の<B>動物園</B>から、<B>$str</B>の収益が上がりました。",$id);
END
} 
# 動物園からの収入 # ここから
sub logOmiseMoney {
my($id, $name, $lName, $point, $str) = @_;
logSecret("${HtagName_}${name}島$point${H_tagName}の<B>デパート</B>から、<B>$str</B>の収益が上がりました。",$id);
END
}
sub logBankMoney {
my($id, $name, $lName, $point, $str) = @_;
logSecret("${HtagName_}${name}島$point${H_tagName}の<B>銀行</B>から、<B>$str</B>の利子が入りました。",$id);
}
sub logMsBank {
my($id, $name, $value) = @_;
logOut("${HtagName_}${name}島${H_tagName}にどこからともなく<B>$value${HunitMoney}ものお金</B>が漂着しました。${HtagName_}${name}島${H_tagName}は快く受けとったようです。",$id);
} 
 
sub logdoumei {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>$comName</B>しました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>$comName</B>");
}
# 強奪 金
sub logRobMoney {
  my($id, $tId, $name, $tName, $comName, $RobMoney) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}へ${HtagComName_}${comName}${H_tagComName}を働き、<B>$RobMoney${HunitMoney}</B>奪いました。",$id, $tId);
}
# 強奪 食料
sub logRobFood {
  my($id, $tId, $name, $tName, $comName, $RobMoney) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}へ${HtagComName_}${comName}${H_tagComName}を働き、<B>$RobMoney${HunitFood}</B>奪いました。",$id, $tId);
}

# ST強奪 金
sub logRobSTMoney {
  my($id, $tId, $name, $tName, $comName, $RobMoney) = @_;
  logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}へ${HtagComName_}${comName}${H_tagComName}を働き、<B>$RobMoney${HunitMoney}</B>奪いました。",$id, $tId);
  logLate("<B>何者か</B>が${HtagName_}${tName}島${H_tagName}${HtagComName_}${comName}${H_tagComName}を働き、<B>$RobMoney${HunitMoney}</B>奪いました。",$tId);
}
# ST強奪 食料
sub logRobSTFood {
  my($id, $tId, $name, $tName, $comName, $RobMoney) = @_;
  logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}へ${HtagComName_}${comName}${H_tagComName}を働き、<B>$RobMoney${HunitFood}</B>奪いました。",$id, $tId);
  logLate("<B>何者か</B>が${HtagName_}${tName}島${H_tagName}${HtagComName_}${comName}${H_tagComName}を働き、<B>$RobMoney${HunitFood}</B>奪いました。",$tId);
}
sub logMissRob {
  my($id, $tId, $name, $tName, $comName) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}へ${HtagComName_}${comName}${H_tagComName}を働こうとしましたが失敗しました。",$id, $tId);
}
sub logteikou {
    my($id, $name,$str) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が箱島国際連盟に<B>攻撃停止を要請</B>し、<B>$str</B>ターンの攻撃停止命令が出されました。",$id);
}
sub logteimis {
    my($id, $name,$str) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が箱島国際連盟に<B>攻撃停止を要請</B>しましたが条件に合わないため承認されませんでした。",$id);
}
sub logteitas {
    my($id, $name,$str) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が箱島国際連盟に<B>攻撃停止命令の延長を要請</B>し、<B>$str</B>ターンの攻撃停止命令が延長されました。",$id);
}
sub logteidame {
    my($id, $target, $name, $tName, $comName)= @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}に<B>$comName</B>しようとしましたが攻撃停止命令が出ているので実行できません。",$id, $tId);
}
sub logteideme {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}は攻撃停止命令が出ているので<B>$comName</B>は実行できません。",$id);
}
# 受賞
sub logPrize {
    my($id, $name, $pName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>$pName</B>を受賞しました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>$pName</B>を受賞");
}
sub logkoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>工業王</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>工業王</B>に");
}
sub lognoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>食料王</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>食料王</B>に");
}
sub logooukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>温泉王</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>温泉王</B>に");
}
sub logdoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>動物園王</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>動物園王</B>に");
}
sub logdeukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>デパート王</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>デパート王</B>に");
}
sub logfoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>森林王</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>森林王</B>に");
}
sub logtoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>鉄道王</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>鉄道王</B>に");
}
sub logmoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>いのらキラー王</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>いのらキラー王</B>に");
}
sub logjoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>浄水場王</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>浄水場王</B>に");
}
sub loghoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>発電王</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>発電王</B>に");
}
sub loggoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>ゴミ処理場王</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>ゴミ処理場王</B>に");
}
sub logsoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>石油王</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>石油王</B>に");
}
sub logloukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>レジャー王</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>レジャー王</B>に");
}
sub logyoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>収入王</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>収入王</B>に");
}
sub logeoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>資金王</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>資金王</B>に");
}
sub logaoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>面積王</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>面積王</B>に");
}
sub logioukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>求人王</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>求人王</B>に");
}
sub logboukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>皇帝</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>皇帝</B>に");
}
sub loguoukae {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>採掘王</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>採掘王</B>に");
}
# 賞金
sub logPzMoney {
my($id, $name, $pMoney) = @_;
logOut("${HtagName_}${name}島${H_tagName}には賞金として<B>$pMoney$HunitMoney</B>が支給されました。",$id);
}


# 島がいっぱいな場合
sub tempNewIslandFull {
    out(<<END);
${HtagBig_}申し訳ありません、島が一杯で登録できません！！${H_tagBig}$HtempBack
END
}

# 新規で名前がない場合
sub tempNewIslandNoName {
    out(<<END);
${HtagBig_}島につける名前が必要です。${H_tagBig}$HtempBack
END
}

# 新規で名前が不正な場合
sub tempNewIslandBadName {
    out(<<END);
${HtagBig_}',?()<>\$'とか入ってたり、「無人島」とかいった変な名前はやめましょうよ〜${H_tagBig}$HtempBack
END
}

# すでにその名前の島がある場合
sub tempNewIslandAlready {
    out(<<END);
${HtagBig_}その島ならすでに発見されています。${H_tagBig}$HtempBack
END
}

# パスワードがない場合
sub tempNewIslandNoPassword {
    out(<<END);
${HtagBig_}パスワードが必要です。${H_tagBig}$HtempBack
END
}

# 島を発見しました!!
sub tempNewIslandHead {
    out(<<END);
<CENTER>
${HtagBig_}島を発見しました！！${H_tagBig}<BR>
${HtagBig_}${HtagName_}「${HcurrentName}島」${H_tagName}と命名します。${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
END
}

# 地形の呼び方
sub landName {
    my($land, $lv) = @_;
    if($land == $HlandSea) {
	if($lv == 1) {
            return '浅瀬';
        } else {
            return '海';
	}
    } elsif($land == $HlandWaste) {
if($lv == 2) {
return '砂地';
} else{
	return '荒地';
}
    } elsif($land == $HlandLake) {
	return '湖';
    } elsif($land == $HlandPlains) {
	return '平地';
    } elsif($land == $HlandTown) {
	if($lv < 30) {
	    return '村';
	} elsif($lv < 100) {
	    return '町';
	} else {
	    return '都市';
	}
    } elsif($land == $HlandForest) {
	return '森';
    } elsif($land == $HlandFarm) {
	return '農場';
    } elsif($land == $HlandBoku) {
	return '牧場';
    } elsif($land == $HlandGoyu) {
	return 'ゴミ輸出機構';
    } elsif($land == $HlandFactory) {
	return '工場';
    } elsif($land == $HlandBase) {
	return 'ミサイル基地';
    } elsif($land == $HlandSefence){
	return '広域防衛施設';
    } elsif($land == $HlandDefence) {
	if($lv < 2) {
	    return '防衛施設';
	} else {
	    return 'ST防衛施設';
	}
    } elsif($land == $HlandMountain) {
	return '山';
    } elsif($land == $HlandHatu) {
	return '火力発電所';
  } elsif($land == $HlandChou) {
	return '波力発電所';
 } elsif($land == $HlandSuiry) {
	return '水力発電所';
 } elsif($land == $HcomTinet) {
	return '地熱発電所';
    } elsif($land == $HlandGomi) {
	return 'ごみ処理施設';
    } elsif($land == $HlandMonster) {
	my($kind, $name, $hp) = monsterSpec($lv);
	return $name;
    } elsif($land == $Hlandhokak) {
	my($kind, $name, $hp) = monsterSpec($lv);
	return '$name捕縛中';
     } elsif($land == $HlandSbase) {
	return '海底基地';
     } elsif($land == $HlandPori) {
	return '警察署';
  } elsif($land == $HlandShou) {
	return '消防署';
     } elsif($land == $HlandInok) {
	return 'いのら研究所';
     } elsif($land == $HlandOnpa) {
	return '特殊音波施設';
    } elsif($land == $HlandOil) {
if($lv == 0) {
	return '海底油田';
}else {
return '養殖場';
}
    } elsif($land == $HlandMonument) {
	return $HmonumentName[$lv];
} elsif($land == $HlandStation) {
         if($lv < 100) {
             return '線路';
         } else {
             return '駅';
         }
    } elsif($land == $Hlandhos) {
return '病院';
} elsif($land == $HlandLand) { 
if($lv == 0) {
return 'リゾートホテル';
}elsif($lv == 1) {
return '水族館';
}elsif($lv == 2) {
return '屋内スキー場';
}elsif($lv == 3) {
return '野球場';
}elsif($lv == 4) {
return 'サッカースタジアム';
}elsif($lv == 5) {
return '競馬場';
}elsif($lv == 6) {
return 'ゴルフ場';
}elsif($lv == 7) {
return '遊園地';
}elsif($lv == 8) {
return '展示場';
}elsif($lv == 9) {
return 'カジノ';
}elsif($lv == 10) {
return '公園';
}elsif($lv == 11) {
return '植物園';
}elsif($lv == 12) {
return '塔';
}elsif($lv == 13) {
return '城';
}
    } elsif($land == $Hlanddoubutu) {
	if($lv == 0) {
	    return '温泉';
	}elsif($lv == 1){
	    return '動物園';
	} elsif($lv == 2) {
	    return 'デパート';
	}
    } elsif($land == $HlandHaribote) {
	if($lv == 0) {
	    return 'ハリボテ';
	} else {
	    return '銀行';
	}

  } elsif($land == $HlandJirai) {
         if($lv ==0) {
              return '地雷';
         } elsif($lv == 1) {
             return '高性能地雷';
         } elsif($lv == 2) {
             return 'ワープ地雷';
}
}elsif($land == $Hlandkiken){
return '気象研究所';
}elsif($land == $Hlandkishou){
return '気象観測所';
}elsif($land == $HlandJous){
return '浄水所';
}elsif($land == $HlandReho){
return '低収束レーザー砲';
}elsif($land == $HlandBouh){
return '防波堤';
}elsif($land == $HlandKoku){
return '軍総司令部';
}elsif($land == $HlandMina){
return '港';
}elsif($land == $HlandDenb){
return '電力売買公社';
}elsif($land == $HlandJusi){
return 'マイクロ波受信施設';
}elsif($land == $HlandEisei){
return '衛星追跡管制施設';
}elsif($land == $HlandTaiy){
return '太陽光発電所';
}elsif($land == $HlandFuha){
return '風力発電所';
}elsif($land == $Hlandkukou){
if($lv == 1) {
	    return '空港';
	} else {
	    return '国際空港';
	}
}
}
# 人口その他の値を算出
sub estimate {
    my($number) = $_[0];
    my($island);
    my($pop, $area, $farm, $factory, $mountain, $score,$kiken,$kishou,$kukou,$yousho,$onse,$dou,$dep,$miu,$hospit,$Onpa,$Inok,$Pori,$Jous,$hatu,$gomi,$jusi,$goyu,$boku,$mina,$denb,$gun,$seki,$lands,$forest,$stay,$Shou,$Den,$har,$def,$reh,$sei,$eki) = (0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);

    # 地形を取得
    $island = $Hislands[$number];
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};

    # 数える
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
		    # 町
		    $pop += $value;
		} elsif($kind == $HlandFarm) {
		    # 農場
		    $farm += $value;
		} elsif($kind == $HlandFactory) {
		    # 工場
		    $factory += $value;
		} elsif($kind == $HlandBase) {
		    # 工場
		    $miu ++;
} elsif($kind == $HlandStation) {
if($value < 100) {
     $stay ++;
         } else {
$eki ++;
         }
	} elsif($kind == $HlandForest) {
		    # 工場
		    $forest += $value;
		} elsif($kind == $HlandMountain) {
		    # 山
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

    # 代入
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


# 範囲内の地形を数える
sub countAround {
    my($land, $x, $y, $kind, $range) = @_;
    my($i, $count, $sx, $sy);
    $count = 0;
    for($i = 0; $i < $range; $i++) {
	 $sx = $x + $ax[$i];
	 $sy = $y + $ay[$i];



	 if(($sx < 0) || ($sx >= $HislandSize) ||
	    ($sy < 0) || ($sy >= $HislandSize)) {
	     # 範囲外の場合
	     if($kind == $HlandSea) {
		 # 海なら加算
		 $count++;
	     }
	 } else {
	     # 範囲内の場合
	     if($land->[$sx][$sy] == $kind) {
		 $count++;
	     }
	 }
    }
    return $count;
}

# 0から(n - 1)までの数字が一回づつ出てくる数列を作る
sub randomArray {
    my($n) = @_;
    my(@list, $i);

    # 初期値
    if($n == 0) {
	$n = 1;
    }
    @list = (0..$n-1);

    # シャッフル
    for ($i = $n; --$i; ) {
	my($j) = int(rand($i+1));
	if($i == $j) { next; };
	@list[$i,$j] = @list[$j,$i];
    }

    return @list;
}

# 名前変更失敗
sub tempChangeNothing {
    out(<<END);
${HtagBig_}名前、パスワードともに空欄です${H_tagBig}$HtempBack
END
}

# 名前変更資金足りず
sub tempChangeNoMoney {
    out(<<END);
${HtagBig_}資金不足のため変更できません${H_tagBig}$HtempBack
END
}

# 名前変更成功
sub tempChange {
    out(<<END);
${HtagBig_}変更完了しました${H_tagBig}$HtempBack
END
}
 sub logStationMoney {
     my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>から、<B>$str</B>の収益が上がりました。",$id);
  END
  }
1;
