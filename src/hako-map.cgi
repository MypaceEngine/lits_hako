#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# 地図モードモジュール(ver1.00)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Lits箱庭用改造
# 改造者：MT
# スクリプトの再配布は禁止します。
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# 観光モード
#----------------------------------------------------------------------
# メイン
sub printIslandMain {
    # 開放
    unlock();

    # idから島番号を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};

    # なぜかその島がない場合
    if($HcurrentNumber eq '') {
	tempProblem();
unlock(); 
	return;
    }
$Hislands[$HcurrentNumber]->{'kanko'}++; # ここから
writeIslandskanko($HcurrentID);
# 開放
unlock(); 
    # 名前の取得
    $HcurrentName = $Hislands[$HcurrentNumber]->{'name'};
$kanko= $Hislands[$HcurrentNumber]->{'kanko'};
    # 観光画面
    tempPrintIslandHead(); # ようこそ!!
    islandInfo(); # 島の情報
    islandMap(0); # 島の地図、観光モード
$ref = $ENV{'REMOTE_ADDR'};
$reb = $ENV{'REMOTE_HOST'};
$rec = $ENV{'HTTP_USER_AGENT'};
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
$rea = "$year/$mon/$mday $hour\:$min";
open(KLOG,">> doukana.log");
print KLOG "$rea . $ref . $reb . $rec\n";
close(KLOG);
    # ○○島ローカル掲示板
    if($HuseLbbs) {
	tempLbbsHead();     # ローカル掲示板
	tempLbbsInput();   # 書き込みフォーム
	tempLbbsContents(); # 掲示板内容
    }

    # 近況
    tempRecent(0);
}

#----------------------------------------------------------------------
# 開発モード
#----------------------------------------------------------------------
# メイン
sub ownerMain {
    # 開放
    unlock();

    # モードを明示
    $HmainMode = 'owner';

    # idから島を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # パスワード
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password間違い
	tempWrongPassword();
	return;
    }

    # 開発画面
    tempOwner(); # 「開発計画」

    # ○○島ローカル掲示板
    if($HuseLbbs) {
	tempLbbsHead();     # ローカル掲示板
	tempLbbsInputOW();   # 書き込みフォーム
	tempLbbsContents(); # 掲示板内容
    }

    # 近況
    tempRecent(1);
}
sub ownerMainb {
    # 開放
    unlock();

    # モードを明示
    $HmainMode = 'owner';

    # idから島を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # 開発画面
    tempOwner(); # 「開発計画」

$ref = $ENV{'REMOTE_ADDR'};
$reb = $ENV{'REMOTE_HOST'};
$rec = $ENV{'HTTP_USER_AGENT'};
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
$rea = "$year/$mon/$mday $hour\:$min";
open(KLOG,">> doukana.log");
print KLOG "$rea . $ref . $reb . $rec\n";
close(KLOG);

    # ○○島ローカル掲示板
    if($HuseLbbs) {
	tempLbbsHead();     # ローカル掲示板
	tempLbbsInputOW();   # 書き込みフォーム
	tempLbbsContents(); # 掲示板内容
    }

    # 近況
    tempRecent(1);
}
#----------------------------------------------------------------------
# コマンドモード
#----------------------------------------------------------------------
# メイン
sub commandMain {
    # idから島を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # パスワード
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password間違い
	unlock();
	tempWrongPassword();
	return;
    }

    # モードで分岐
    my($command) = $island->{'command'};

    if($HcommandMode eq 'delete') {
	slideFront($command, $HcommandPlanNumber);
	tempCommandDelete();
    } elsif(($HcommandKind == $HcomAutoPrepare) ||
	    ($HcommandKind == $HcomAutoPrepare2)) {
	# フル整地、フル地ならし
	# 座標配列を作る
	makeRandomPointArray();
	my($land) = $island->{'land'};

	# コマンドの種類決定
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
	# 全消し
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
	# コマンドを登録
	$command->[$HcommandPlanNumber] = {
	    'kind' => $HcommandKind,
	    'target' => $HcommandTarget,
	    'x' => $HcommandX,
	    'y' => $HcommandY,
	    'arg' => $HcommandArg
	    };
    }

    # データの書き出し
    writeIslandsrocal($HcurrentID);

    # owner modeへ
    ownerMain();

}
sub ShuuMain {
    # idから島を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # パスワード
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password間違い
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
    # データの書き出し
    writeIslandsshuu($HcurrentID);
    $HmainMode = 'owner';
    # owner modeへ
    ownerMain();

}
#----------------------------------------------------------------------
# コメント入力モード
#----------------------------------------------------------------------
# メイン
sub commentMain {
    # idから島を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # パスワード
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password間違い
	unlock();
	tempWrongPassword();
	return;
    }

    # メッセージを更新
    $island->{'comment'} = htmlEscape($Hmessage);

    # データの書き出し
    writeIslandscomment($HcurrentID);

    # コメント更新メッセージ
    tempComment();

    # owner modeへ
    ownerMain();
}

#----------------------------------------------------------------------
# ローカル掲示板モード
#----------------------------------------------------------------------
# メイン

sub localBbsMain {
    # idから島番号を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    my($foreignName);

    # なぜかその島がない場合
    if($HcurrentNumber eq '') {
	unlock();
	tempProblem();
	return;
    }

    # 削除モードじゃなくて名前かメッセージがない場合
    if($HlbbsMode != 2) {
	if(($HlbbsName eq '') || ($HlbbsName eq '')) {
	    unlock();
	    tempLbbsNoMessage();
	    return;
	}
    }

    # 観光者モードじゃない時はパスワードチェック
    if($HlbbsMode != 0) {
	if ($HlbbsMode == 3) {
	    # 外国者モード
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
	    # 島主モード
	    if(!checkPassword($island->{'password'},$HinputPassword)) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	    }
	}
    }

    my($lbbs);
    $lbbs = $island->{'lbbs'};

    # モードで分岐
    if($HlbbsMode == 2) {
	# 削除モード
	# メッセージを前にずらす
	slideBackLbbsMessage($lbbs, $HcommandPlanNumber);
	tempLbbsDelete();
    } else {
	# 記帳モード
	# メッセージを後ろにずらす
	slideLbbsMessage($lbbs);

	# メッセージ書き込み
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
	    $HlbbsName = "${HislandTurn} from ${foreignName}島：" . htmlEscape($HlbbsName);
	} else {
	    $HlbbsName = "${HislandTurn}：" . htmlEscape($HlbbsName);
	}
	$HlbbsMessage = htmlEscape($HlbbsMessage);
	$lbbs->[0] = "$message>$HlbbsName>$HlbbsMessage";

	tempLbbsAdd();
    }

    # データ書き出し
    writeIslandsrocal($HcurrentID);

    # もとのモードへ
    if(($HlbbsMode == 1) || ($HlbbsMode == 2)) {
	ownerMain();
    } else {
	printIslandMain();
    }
}

# ローカル掲示板のメッセージを一つ後ろにずらす
sub slideLbbsMessage {
    my($lbbs) = @_;
    my($i);
#    pop(@$lbbs);
#    push(@$lbbs, $lbbs->[0]);
    pop(@$lbbs);
    unshift(@$lbbs, $lbbs->[0]);
}

# ローカル掲示板のメッセージを一つ前にずらす
sub slideBackLbbsMessage {
    my($lbbs, $number) = @_;
    my($i);
    splice(@$lbbs, $number, 1);
    $lbbs->[$HlbbsMax - 1] = '0>>';
}

#----------------------------------------------------------------------
# 島の地図
#----------------------------------------------------------------------

# 情報の表示
sub islandInfo {
    my($island) = $Hislands[$HcurrentNumber];
    # 情報表示
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
	$boku = ($boku == 0) ? "保有せず" : "${boku}0$HunitPop";
	$hatu = ($hatu == 0) ? "保有せず" : "${hatu}000Kw";
	$gomi = ($gomi == 0) ? "保有せず" : "${gomi}00トン";
	$Oil = ($Oil == 0) ? "保有せず" : "${Oil}トン";
	$shoku = ($shoku == 0) ? "保有せず" : "${shoku}00トン";
$yousho = ($yousho == 0) ? "保有せず" : "${yousho}0$HunitPop";
    $farm = ($farm == 0) ? "保有せず" : "${farm}0$HunitPop";
    $factory = ($factory == 0) ? "保有せず" : "${factory}0$HunitPop";
    $mountain = ($mountain == 0) ? "保有せず" : "${mountain}0$HunitPop";
$Jous = ($Jous == 0) ? "保有せず" : "${Jous}0000��";
my($ei) = "";
if ($island->{'kouei'} >= 1){
if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
$ei = "レベル$island->{'kouei'}";
  } elsif($HhideMoneyMode == 2) {
$ei = "保有中";
}
} else {
$ei = "保有せず";
}
my($ei2) = "";
if ($island->{'kanei'} >= 1){
if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
$ei2 = "レベル$island->{'kanei'}";
 } elsif($HhideMoneyMode == 2) {
$ei2 = "保有中";
}
}else {
$ei2 = "保有せず";
}
my($ei3) = "";
if ($island->{'bouei'} >= 1){
if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
$ei3 = "レベル$island->{'bouei'}";
 } elsif($HhideMoneyMode == 2) {
$ei3 = "保有中";
}
}else {
$ei3 = "保有せず";
}
my($ei4) = "";
if ($island->{'reiei'} >= 1){
if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
if ($island->{'reiei'} < 11){
$ei4 = "レベル$island->{'reiei'}(使用可能)";
}else{
my($res) = $island->{'reiei'} % 10;
my($rer) = int($island->{'reiei'} / 10);
if($res == 0){
$res = 10;
}
$ei4 = "レベル$res(あと$rerターン)";
}
 } elsif($HhideMoneyMode == 2) {
$ei4 = "保有中";
}
}else {
$ei4 = "保有せず";
}
my($ei6) = "";
if ($island->{'pmsei'} >= 1){
if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
if ($island->{'pmsei'} < 11){
$ei6 = "レベル$island->{'pmsei'}(使用可能)";
}else{
my($rei) = $island->{'pmsei'} % 10;
my($rea) = int($island->{'pmsei'} / 10);
if($res == 0){
$res = 10;
}
$ei6 = "レベル$rei(あと$reaターン)";
}
 } elsif($HhideMoneyMode == 2) {
$ei6 = "保有中";
}
}else {
$ei6 = "保有せず";
}
my($ei5) = "";
if ($island->{'hatei'} >= 1){
if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
$ei5 = "$island->{'hatei'}00000Kw";
 } elsif($HhideMoneyMode == 2) {
$ei5 = "保有中";
}
}else {
$ei5 = "保有せず";
}
my($shuusi) = "";
if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
$shuusi = "$island->{'shuu'}$HunitMoney";
} elsif($HhideMoneyMode == 2) {
if($island->{'shuu'} < 0){
$shuusi = "赤字";
}elsif($island->{'shuu'} == 0){
$shuusi = "0億円";
}else{
$shuusi = "黒字";
}
}
my($shak) = "";
my($shau) = "";
if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
$shak = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}借入金${H_tagTH}</NOBR></TH>";
if($island->{'shaka'} > 0){
$shau = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'shamo'}＊$island->{'shaka'}億円</NOBR></TH>";
}else{
$shau = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>なし</NOBR></TH>";
}
}
my($shuu) = 0;
my($shuo) = "";
$shuu =int(($island->{'sigoto'} / $island->{'pop'}) * 1000);
if($shuu >= 100){
$shuo = "100％"
} else {
$shuo = "約$shuu％"
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
	# 無条件またはownerモード
	$mStr1 = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}資金${H_tagTH}</NOBR></TH>";
	$mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'money'}$HunitMoney</NOBR></TD>";
$island->{'ADDRE'} = "$ENV{'REMOTE_ADDR'}";
writeIslandsAddre($HcurrentID);
    } elsif($HhideMoneyMode == 2) {
	my($mTmp) = aboutMoney($island->{'money'});

	# 1000億単位モード
	$mStr1 = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}資金${H_tagTH}</NOBR></TH>";
	$mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$mTmp</NOBR></TD>";
$kanke ="<br><center><b>あなたは$kanko人目の訪問者です。</b></center>";
    }
    out(<<END);
<CENTER>
<table>
<left>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}順位${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}島旗${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}就業率${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}食料${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}面積${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}ゴミ蓄積量${H_tagTH}</NOBR></TH><TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}石油貯蓄量${H_tagTH}</NOBR></TH>
</TR>
<TR>
<TD $HbgNumberCell align=middle nowrap=nowrap><NOBR>${HtagNumber_}$rank${H_tagNumber}</NOBR></TD>
<TD $HbgNumberCell align=middle nowrap=nowrap><NOBR>$fStr</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'pop'}$HunitPop</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$shuo</NOBR></TD>
$mStr2
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'food'}$HunitFood</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'area'}$HunitArea</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'slag'}トン</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$Oil</NOBR></TD>
</tr>
</TABLE>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}今ターンの収支${H_tagTH}</NOBR></TH>
$shak
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}最大発電量${H_tagTH}</NOBR></TH><TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}ゴミ処理施設規模${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}浄水場規模${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}最大食料生産規模${H_tagTH}</NOBR></TH></TR>
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
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}農場規模${H_tagTH}</NOBR></TH><TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}養殖場規模${H_tagTH}</NOBR></TH><TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}牧場規模${H_tagTH}</NOBR></TH><TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}工場規模${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}採掘場規模${H_tagTH}</NOBR></TH></tr>
<TR>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${farm}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${yousho}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${boku}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${factory}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${mountain}</NOBR></TD>
</tr>
</TABLE>
<TABLE BORDER><tr>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}攻撃衛星${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}監視衛星${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}防御衛星${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}レーザー衛星${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}PMS衛星${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}発電衛星${H_tagTH}</NOBR></TH>
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
    # 情報表示
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
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}　${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}公共系${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}発電系${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}食料生産系${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}鉱山系${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}工場系${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}軍事系${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}特殊系${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}交通系${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}その他${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}合計${H_tagTH}</NOBR></TH>
</TR>
<TR>
<TD $HbgNumberCell align=middle nowrap=nowrap><NOBR>${HtagTH_}最大就職可能人数${H_tagTH}</NOBR></TD>
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
<TD $HbgNumberCell align=middle nowrap=nowrap><NOBR>${HtagTH_}現在の割り当て人数${H_tagTH}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$aaa人</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$bbb人</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$ccc人</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$ddd人</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$eee人</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$fff人</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$ggg人</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$hhh人</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$iii人</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$sousuu人</NOBR></TD>
</tr>
<TR>
<TD $HbgNumberCell align=middle nowrap=nowrap><NOBR>${HtagTH_}稼働率${H_tagTH}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><SELECT NAME=paraa>
END

    # 数量
    for($i = 0; $i < 101; $i++) {
if($i == $koukpase){
	out("<OPTION VALUE=$i SELECTED>$i\n");
}else{
	out("<OPTION VALUE=$i>$i\n");
}
    }

    out(<<END);
</SELECT>％</TD>
<TD $HbgInfoCell align=right nowrap=nowrap><SELECT NAME=parab>
END

    # 数量
    for($i = 0; $i < 101; $i++) {
if($i == $hatupase){
	out("<OPTION VALUE=$i SELECTED>$i\n");
}else{
	out("<OPTION VALUE=$i>$i\n");
}
    }

    out(<<END);
</SELECT>％</TD>
<TD $HbgInfoCell align=right nowrap=nowrap><SELECT NAME=parac>
END

    # 数量
    for($i = 0; $i < 101; $i++) {
if($i == $noupase){
	out("<OPTION VALUE=$i SELECTED>$i\n");
}else{
	out("<OPTION VALUE=$i>$i\n");
}
    }

    out(<<END);
</SELECT>％</TD>
<TD $HbgInfoCell align=right nowrap=nowrap><SELECT NAME=parad>
END

    # 数量
    for($i = 0; $i < 101; $i++) {
if($i == $kouzpase){
	out("<OPTION VALUE=$i SELECTED>$i\n");
}else{
	out("<OPTION VALUE=$i>$i\n");
}
    }

    out(<<END);
</SELECT>％</TD>
<TD $HbgInfoCell align=right nowrap=nowrap><SELECT NAME=parae>
END

    # 数量
    for($i = 0; $i < 101; $i++) {
if($i == $koujpase){
	out("<OPTION VALUE=$i SELECTED>$i\n");
}else{
	out("<OPTION VALUE=$i>$i\n");
}
    }

    out(<<END);
</SELECT>％</TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR><SELECT NAME=paraf>
END

    # 数量
    for($i = 0; $i < 101; $i++) {
if($i == $gunpase){
	out("<OPTION VALUE=$i SELECTED>$i\n");
}else{
	out("<OPTION VALUE=$i>$i\n");
}
    }

    out(<<END);
</SELECT>％</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><SELECT NAME=parag>
END

    # 数量
    for($i = 0; $i < 101; $i++) {
if($i == $tokupase){
	out("<OPTION VALUE=$i SELECTED>$i\n");
}else{
	out("<OPTION VALUE=$i>$i\n");
}
    }

    out(<<END);
</SELECT>％</TD>
<TD $HbgInfoCell align=right nowrap=nowrap><SELECT NAME=parah>
END

    # 数量
    for($i = 0; $i < 101; $i++) {
if($i == $koutpase){
	out("<OPTION VALUE=$i SELECTED>$i\n");
}else{
	out("<OPTION VALUE=$i>$i\n");
}
    }

    out(<<END);
</SELECT>％</TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$sonopase％</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap></TD>
</tr>
</TABLE>
<B>パスワード</B>
<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE=submit VALUE="変更" NAME=ShuuButton$Hislands[$HcurrentNumber]->{'id'}>
</form>
</CENTER>
<hr>
END
}
# 地図の表示
# 引数が1なら、ミサイル基地等をそのまま表示
sub islandMap {
    my($mode) = @_;
    my($island);
    $island = $Hislands[$HcurrentNumber];

    out(<<END);
<CENTER><TABLE BORDER><TR><TD>
END
    # 地形、地形値を取得
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};
    my($l, $lv);

    # コマンド取得
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

    # 座標(上)を出力
    out("<IMG SRC=\"xbar.gif\" width=1008 height=16><BR>");

    # 各地形および改行を出力
    my($x, $y);
    for($y = 0; $y < $HislandSize; $y++) {
	# 行の番号を出力
	    out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");

	# 各地形を出力
	for($x = 0; $x < $HislandSize; $x++) {
	    $l = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];
	    landString($l, $lv, $x, $y, $mode, $comStr[$x][$y]);
	}

	# 改行を出力
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
	    # 浅瀬
	    $image = 'land14.gif';
	    $alt = '海(浅瀬)';
        } else {
            # 海
	    $image = 'land0.gif';
	    $alt = '海';
        }
    } elsif($l == $HlandWaste) {
	# 荒地
	if($lv == 1) {
	    $image = 'land13.gif'; # 着弾点
	    $alt = '荒地';
} elsif($lv == 2){
	    $image = 'land36.gif'; # 着弾点
	    $alt = '砂地';
	} else {
	    $image = 'land1.gif';
	    $alt = '荒地';
	}
    } elsif($l == $HlandPlains) {
	# 平地
	$image = 'land2.gif';
	$alt = '平地';
    } elsif($l == $HlandBouh) {
	# 平地
	$image = 'land40.gif';
	$alt = '防波堤';
    } elsif($l == $HlandForest) {
	# 森
	if($mode == 1) {
	    $image = 'land6.gif';
	    $alt = "森(${lv}$HunitTree)";
	} else {
	    # 観光者の場合は木の本数隠す
	    $image = 'land6.gif';
	    $alt = '森';
	}
    } elsif($l == $HlandTown) {
	# 町
	my($p, $n);
	if($lv < 30) {
	    $p = 3;
	    $n = '村';
	} elsif($lv < 100) {
	    $p = 4;
	    $n = '町';
	} else {
	    $p = 5;
	    $n = '都市';
	}

	$image = "land${p}.gif";
	$alt = "$n(${lv}$HunitPop)";
    } elsif($l == $HlandFarm) {
	# 農場
	$image = 'land7.gif';
	$alt = "農場(${lv}0${HunitPop}規模)";
 } elsif($l == $HlandShou) {
	# 農場
	$image = 'land72.gif';
	$alt = "消防署";
    } elsif($l == $HlandLake) {
if($lv == 2) {
$image = 'land71.gif';
	$alt = "釣り堀";
}else{
	$image = 'land32.gif';
	$alt = "湖";
}
} elsif($l == $Hlanddoubutu) { # ここ追加
if($lv == 0) {
	    # 浅瀬
	    $image = 'land22.gif';
	    $alt = '温泉';
}elsif($lv == 1) {
	    # 浅瀬
	    $image = 'land19.gif';
	    $alt = '動物園';
        } else {
            # 海
	    $image = 'land20.gif';
	    $alt = 'デパート';
}
} elsif($l == $HlandLand) { # ここ追加
if($lv == 0) {
	    # 浅瀬
	    $image = 'land54.gif';
	    $alt = 'リゾートホテル';
}elsif($lv == 1) {
	    # 浅瀬
	    $image = 'land53.gif';
	    $alt = '水族館';
}elsif($lv == 2) {
	    # 浅瀬
	    $image = 'land52.gif';
	    $alt = '屋内スキー場';
}elsif($lv == 3) {
	    # 浅瀬
	    $image = 'land51.gif';
	    $alt = '野球場';
}elsif($lv == 4) {
	    # 浅瀬
	    $image = 'land50.gif';
	    $alt = 'サッカースタジアム';
}elsif($lv == 5) {
	    # 浅瀬
	    $image = 'land49.gif';
	    $alt = '競馬場';
}elsif($lv == 6) {
	    # 浅瀬
	    $image = 'land56.gif';
	    $alt = 'ゴルフ場';
}elsif($lv == 7) {
	    # 浅瀬
	    $image = 'land57.gif';
	    $alt = '遊園地';
}elsif($lv == 8) {
	    # 浅瀬
	    $image = 'land58.gif';
	    $alt = '展示場';
}elsif($lv == 9) {
	    # 浅瀬
	    $image = 'land59.gif';
	    $alt = 'カジノ';
}elsif($lv == 10) {
	    # 浅瀬
	    $image = 'land61.gif';
	    $alt = '公園';
}elsif($lv == 11) {
	    # 浅瀬
	    $image = 'land62.gif';
	    $alt = '植物園';
}elsif($lv == 12) {
	    # 浅瀬
	    $image = 'land63.gif';
	    $alt = '塔';
}elsif($lv == 13) {
	    # 浅瀬
	    $image = 'land64.gif';
	    $alt = '城';
}
} elsif($l == $HlandStation) {
if($lv < 100) {
# 線路
$image = 'senro.gif'; # 海底基地の画像を流用
$alt = "線路(${lv})";
         } else {
             # 駅
             $image = 'eki.gif'; # 海底油田の画像を流用
             $alt = "駅(${lv})";
}
} elsif($l == $Hlandhos) {
$image = 'land29.gif';
$alt = '病院';
} elsif($l == $HlandMina) {
$image = 'land41.gif';
$alt = '港';
} elsif($l == $HlandGoyu) {
$image = 'land45.gif';
$alt = 'ゴミ輸出機構';
} elsif($l == $HlandBoku) {
$image = 'land46.gif';
$alt = "牧場(${lv}0${HunitPop}規模)";
} elsif($l == $HlandTaiy) {
$image = 'land44.gif';
$alt = "太陽光発電所(${lv}000KW)";
} elsif($l == $HlandFuha) {
$image = 'land60.gif';
$alt = "風力発電所(${lv}000KW)";
} elsif($l == $HlandSuiry) {
$image = 'land68.gif';
$alt = "水力発電所(${lv}000KW)";
} elsif($l == $HlandTinet) {
$image = 'land69.gif';
$alt = "地熱発電所(${lv}000KW)";
} elsif($l == $HlandChou) {
$image = 'land70.gif';
$alt = "波力発電所(${lv}000KW)";
} elsif($l == $HlandJusi) {
$image = 'land42.gif';
$alt = 'マイクロ波受信施設';
} elsif($l == $HlandEisei) {
$image = 'land73.gif';
$alt = '衛星追跡管制施設';
} elsif($l == $HlandDenb) {
$image = 'land43.gif';
$alt = '電力売買公社';
} elsif($l == $HlandJous) {
$image = 'land37.gif';
$alt = "浄水所(${lv}0000�筏�模)";
} elsif($l == $Hlandkukou) { # ここ追加
if($lv == 1) {
	    # 浅瀬
	    $image = 'land25.gif';
	    $alt = '空港';
}else {
	    # 浅瀬
	    $image = 'land26.gif';
	    $alt = '国際空港';
        }

    } elsif($l == $Hlandkiken) {
	# 工場
if($mode == 0) {
$image = 'land6.gif';
$alt = '森';
} else {
	$image = 'land23.gif';
	$alt = "気象研究所(強化レベル:${lv})";
}
    } elsif($l == $Hlandkishou) {
	# 工場
	$image = 'land24.gif';
	$alt = "気象観測所(強化レベル:${lv})";
    } elsif($l == $HlandHatu) {
	# 工場
	$image = 'land38.gif';
	$alt = "火力発電所(${lv}000KW)";
    } elsif($l == $HlandGomi) {
	# 工場
	$image = 'land39.gif';
	$alt = "ごみ処理施設(${lv}00トン)";
    } elsif($l == $HlandFactory) {
	# 工場
	$image = 'land8.gif';
	$alt = "工場(${lv}0${HunitPop}規模)";
    } elsif($l == $HlandBase) {
	if($mode == 0) {
	    # 観光者の場合は森のふり
	    $image = 'land6.gif';
	    $alt = '森';
	} else {
	    # ミサイル基地
	    my($level) = expToLevel($l, $lv);
	    $image = 'land9.gif';
	    $alt = "ミサイル基地 (レベル ${level}/経験値 $lv)";
	}
    } elsif($l == $HlandKoku) {
	if($mode == 0) {
	    # 観光者の場合は森のふり
	    $image = 'land6.gif';
	    $alt = '森';
	} else {
	    # ミサイル基地
	    $image = 'land47.gif';
	    $alt = '軍総司令部';
	}
    } elsif($l == $HlandSbase) {
	# 海底基地
	if($mode == 0) {
	    # 観光者の場合は海のふり
	    $image = 'land0.gif';
	    $alt = '海';
	} else {
	    my($level) = expToLevel($l, $lv);
	    $image = 'land12.gif';
	    $alt = "海底基地 (レベル ${level}/経験値 $lv)";
	}
    } elsif($l == $HlandDefence) {
if($lv < 2) {
	# 防衛施設
	$image = 'land10.gif';
	$alt = '防衛施設';
} elsif($lv == 2){
if($mode == 0) {
# 観光者の場合は森のふり
$image = 'land6.gif';
$alt = '森';
} else {
# ST防衛施設
$image = 'land10.gif';
$alt = 'ST防衛施設';
}
}
   } elsif($l == $HlandSefence) {
	# 防衛施設
	$image = 'land30.gif';
	$alt = '広域防衛施設';
   } elsif($l == $HlandReho) {
	# 防衛施設
	$image = 'land48.gif';
	$alt = "低収束レーザー砲(強化レベル:${lv})";
   } elsif($l == $HlandOnpa) {
	# 防衛施設
	$image = 'land33.gif';
	$alt = "特殊音波施設(強化レベル:${lv})";
   } elsif($l == $HlandInok) {
	# 防衛施設
	$image = 'land34.gif';
	$alt = "いのら研究所(施設レベル:${lv})";
   } elsif($l == $HlandPori) {
	# 防衛施設
	$image = 'land35.gif';
	$alt = '警察署';
    } elsif($l == $HlandHaribote) {
if($lv == 0) {
	# ハリボテ
	$image = 'land10.gif';
	if($mode == 0) {
	    # 観光者の場合は防衛施設のふり
	    $alt = '防衛施設';
	} else {
	    $alt = 'ハリボテ';
	}
} else {
if($mode == 0) {
# 観光者の場合は森のふり
$image = 'land6.gif';
$alt = '森';
} else {
# 銀行
$image = 'land21.gif';
$alt = "銀行(投資額${lv}000億)";
}
}
     } elsif($l == $HlandJirai) {
if($lv ==0) {
         # 地雷
         if($mode == 0) {
             # 観光者の場合は森のふり
	$image = 'land2.gif';
	$alt = '平地';
         } else {
             $image = 'land65.gif';
             $alt = '地雷';
         }
     } elsif($lv ==1) {
         # 高性能地雷
         if($mode == 0) {
             # 観光者の場合は森のふり
  	$image = 'land2.gif';
	$alt = '平地';
         } else {
            $image = 'land66.gif';
          
   $alt = '高性能地雷';
}
          }elsif($lv ==2) {
         # 高性能地雷
         if($mode == 0) {
             # 観光者の場合は森のふり
  	$image = 'land2.gif';
	$alt = '平地';
         } else {
            $image = 'land67.gif';
             $alt = 'ワープ地雷';
          }
}
    } elsif($l == $HlandOil) {
if($lv == 0) {
	# 海底油田
	$image = 'land16.gif';
	$alt = '海底油田';
}else{
	$image = 'land27.gif';
	$alt = "養殖場(${lv}0${HunitPop}規模)";
}
    } elsif($l == $HlandMountain) {
	# 山
	my($str);
	$str = '';
	if($lv > 0) {
	    $image = 'land15.gif';
	    $alt = "山(採掘場${lv}0${HunitPop}規模)";
	} else {
	    $image = 'land11.gif';
	    $alt = '山';
	}
    } elsif($l == $HlandMonument) {
	# 記念碑
	$image = $HmonumentImage[$lv];
	$alt = $HmonumentName[$lv];
     } elsif($l == $Hlandhokak) {
	# 怪獣
	my($kind, $name, $hp) = monsterSpec($lv);
	my($special) = $HmonsterSpecial[$kind];
	$image = $HmonsterImage[$kind];

	$alt = "怪獣（捕縛中）$name(体力${hp})";

   } elsif($l == $HlandMonster) {
	# 怪獣
	my($kind, $name, $hp) = monsterSpec($lv);
	my($special) = $HmonsterSpecial[$kind];
	$image = $HmonsterImage[$kind];

	# 硬化中?
	if((($special == 3) && (($HislandTurn % 2) == 1)) ||
	   (($special == 4) && (($HislandTurn % 2) == 0))) {
	    # 硬化中
	    $image = $HmonsterImage2[$kind];
	}
	$alt = "怪獣$name(体力${hp})";
    }


    # 開発画面の場合は、座標設定
    if($mode == 1) {
	out("<A HREF=\"JavaScript:void(0);\" onclick=\"ps($x,$y)\">");
    }

    out("<IMG SRC=\"$image\" ALT=\"$point $alt $comStr\" width=32 height=32 BORDER=0>");

    # 座標設定閉じ
    if($mode == 1) {
	out("</A>");
    }
}


#----------------------------------------------------------------------
# テンプレートその他
#----------------------------------------------------------------------
# 個別ログ表示
sub logPrintLocal {
    my($mode) = @_;
    my($i);
    for($i = 0; $i < $HlogMax; $i++) {
	logFilePrint($i, $HcurrentID, $mode);
    }
}

# ○○島へようこそ！！
sub tempPrintIslandHead {
    out(<<END);
<CENTER>
${HtagBig_}${HtagName_}「${HcurrentName}島」${H_tagName}へようこそ！！${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
END
}

# ○○島開発計画
sub tempOwner {
    out(<<END);
<CENTER>
${HtagBig_}${HtagName_}${HcurrentName}島${H_tagName}開発計画${H_tagBig}<BR>
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
	    $cost = '無料'
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
	    $cost = '無料'
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
	    $cost = '無料'
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
	    $cost = '無料'
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
	    $cost = '無料'
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
	    $cost = '無料'
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
	    $cost = '無料'
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
	    $cost = '無料'
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
	    $cost = '無料'
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
	    $cost = '無料'
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
	    $cost = '無料'
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
	    $cost = '無料'
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
	    $cost = '無料'
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
	    $cost = '無料'
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
	    $cost = '無料'
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
	    $cost = '無料'
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
	    $cost = '無料'
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
	    $cost = '無料'
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
	    $cost = '無料'
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
	    $cost = '無料'
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
<INPUT TYPE=submit VALUE="計画送信" NAME=CommandButton$Hislands[$HcurrentNumber]->{'id'}>
<HR>
<B>パスワード</B></BR>
<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<HR>
<B>計画番号</B><SELECT NAME=NUMBER>
END
    # 計画番号
    my($j, $i);
    for($i = 0; $i < $HcommandMax; $i++) {
	$j = $i + 1;
	out("<OPTION VALUE=$i>$j\n");
    }

    out(<<END);
</SELECT><BR>
<HR>
<B>開発計画</B><BR>
END
if($Hnmo == 0){
    out(<<END);
<SELECT onchange=loadOption(form.COMMAND,this.value);showValue(form.COMMAND,form.tt,form.tv); onclick=loadOption(form.COMMAND,this.value);showValue(form.COMMAND,form.tt,form.tv); name=r1><OPTION value=0>基礎工事系</OPTION>
END
if($HdefaultKindB == 1){
out("<OPTION value=1 SELECTED>建設系</OPTION>\n");
}else{
out("<OPTION value=1>建設系</OPTION>\n");
}
if($HdefaultKindB == 2){
out("<OPTION value=2 SELECTED> 　├食料生産系</OPTION>\n");
}else{
out("<OPTION value=2> 　├食料生産系</OPTION>\n");
}
if($HdefaultKindB == 3){
out("<OPTION value=3 SELECTED> 　├工業系</OPTION>\n");
}else{
out("<OPTION value=3> 　├工業系</OPTION>\n");
}
if($HdefaultKindB == 4){
out("<OPTION value=4 SELECTED> 　├鉱山系</OPTION>\n");
}else{
out("<OPTION value=4> 　├鉱山系</OPTION>\n");
}
if($HdefaultKindB == 5){
out("<OPTION value=5 SELECTED> 　├発電系</OPTION>\n");
}else{
out("<OPTION value=5> 　├発電系</OPTION>\n");
}
if($HdefaultKindB == 6){
out("<OPTION value=6 SELECTED> 　├公共系</OPTION>\n");
}else{
out("<OPTION value=6> 　├公共系</OPTION>\n");
}
if($HdefaultKindB == 7){
out("<OPTION value=7 SELECTED> 　├交通系</OPTION>\n");
}else{
out("<OPTION value=7> 　├交通系</OPTION>\n");
}
if($HdefaultKindB == 8){
out("<OPTION value=8 SELECTED> 　├軍事系</OPTION>\n");
}else{
out("<OPTION value=8> 　├軍事系</OPTION>\n");
}
if($HdefaultKindB == 9){
out("<OPTION value=9 SELECTED> 　├特殊系</OPTION>\n");
}else{
out("<OPTION value=9> 　├特殊系</OPTION>\n");
}
if($HdefaultKindB == 10){
out("<OPTION value=10 SELECTED> 　└その他</OPTION>\n");
}else{
out("<OPTION value=10> 　└その他</OPTION>\n");
}
if($HdefaultKindB == 11){
out("<OPTION value=11 SELECTED>貿易系</OPTION>\n");
}else{
out("<OPTION value=11>貿易系</OPTION>\n");
}
if($HdefaultKindB == 12){
out("<OPTION value=12 SELECTED>援助系</OPTION>\n");
}else{
out("<OPTION value=12>援助系</OPTION>\n");
}
if($HdefaultKindB == 13){
out("<OPTION value=13 SELECTED>ミサイル系</OPTION>\n");
}else{
out("<OPTION value=13>ミサイル系</OPTION>\n");
}
if($HdefaultKindB == 14){
out("<OPTION value=14 SELECTED>怪獣派遣系</OPTION>\n");
}else{
out("<OPTION value=14>怪獣派遣系</OPTION>\n");
}
if($HdefaultKindB == 15){
out("<OPTION value=15 SELECTED>衛星系</OPTION>\n");
}else{
out("<OPTION value=15>衛星系</OPTION>\n");
}
if($HdefaultKindB == 16){
out("<OPTION value=16 SELECTED>気象兵器系</OPTION>\n");
}else{
out("<OPTION value=16>気象兵器系</OPTION>\n");
}
if($HdefaultKindB == 17){
out("<OPTION value=17 SELECTED>同盟系</OPTION>\n");
}else{
out("<OPTION value=17>同盟系</OPTION>\n");
}
if($HdefaultKindB == 18){
out("<OPTION value=18 SELECTED>その他</OPTION>\n");
}else{
out("<OPTION value=18>その他</OPTION>\n");
}
if($HdefaultKindB == 19){
out("<OPTION value=19 SELECTED>自動入力系</OPTION>\n");
}else{
out("<OPTION value=19>自動入力系</OPTION>\n");
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
	    $cost = '無料'
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
<INPUT TYPE="radio" NAME="nmo" VALUE="iti" CHECKED><font sizu=2>Mode1</font><INPUT TYPE="radio" NAME="nmo" VALUE="nii"><font sizu=2>Mode2</font><INPUT TYPE="submit" VALUE="モード変更" NAME="ChangeMode$Hislands[$HcurrentNumber]->{'id'}"><BR>
END
}else{
if(($HcommandPoti == 1)||($HcommandPoti == 0)){
out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="zousei" CHECKED>基礎工事系<br>
END
}else{
out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="zousei">基礎工事系<br>
END
}
out(<<END);
<SELECT NAME=COMMANDa length="50">
END

    #コマンド
    my($kind, $cost, $s);
    for($i = 0; $i < $HcommandTotala; $i++) {
	$kind = $HcomLista[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '無料'
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
<INPUT TYPE="radio" NAME="eku" VALUE="kensetu" CHECKED>建設系<BR>
END
}else{
   out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="kensetu">建設系<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDb>
END

    #コマンド

    for($i = 0; $i < $HcommandTotalb; $i++) {
	$kind = $HcomListb[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '無料'
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
<INPUT TYPE="radio" NAME="eku" VALUE="boueki" CHECKED>貿易系<BR>
END
}else{
   out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="boueki">貿易系<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDc>
END

    #コマンド

    for($i = 0; $i < $HcommandTotalc; $i++) {
	$kind = $HcomListc[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '無料'
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
<INPUT TYPE="radio" NAME="eku" VALUE="enjyo" CHECKED>援助系<BR>
END
}else{
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="enjyo">援助系<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDd>
END

    #コマンド

    for($i = 0; $i < $HcommandTotald; $i++) {
	$kind = $HcomListd[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '無料'
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
<INPUT TYPE="radio" NAME="eku" VALUE="misairu" CHECKED>ミサイル系<BR>
END
}else{
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="misairu">ミサイル系<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDe>
END

    #コマンド

    for($i = 0; $i < $HcommandTotale; $i++) {
	$kind = $HcomListe[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '無料'
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
<INPUT TYPE="radio" NAME="eku" VALUE="kaijyu" CHECKED>怪獣派遣系<BR>
END
}else{
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="kaijyu">怪獣派遣系<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDf>
END

    #コマンド

    for($i = 0; $i < $HcommandTotalf; $i++) {
	$kind = $HcomListf[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '無料'
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
<INPUT TYPE="radio" NAME="eku" VALUE="eisei" CHECKED>衛星系<BR>
END
}else{
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="eisei">衛星系<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDg>
END

    #コマンド

    for($i = 0; $i < $HcommandTotalg; $i++) {
	$kind = $HcomListg[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '無料'
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
<INPUT TYPE="radio" NAME="eku" VALUE="kishou" CHECKED>気象兵器系<BR>
END
}else{
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="kishou">気象兵器系<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDh>
END

    #コマンド

    for($i = 0; $i < $HcommandTotalh; $i++) {
	$kind = $HcomListh[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '無料'
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
<INPUT TYPE="radio" NAME="eku" VALUE="doumei" CHECKED>同盟系<BR>
END
}else{
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="doumei">同盟系<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDi>
END

    #コマンド

    for($i = 0; $i < $HcommandTotali; $i++) {
	$kind = $HcomListi[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '無料'
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
<INPUT TYPE="radio" NAME="eku" VALUE="sonota" CHECKED>その他<BR>
END
}else{
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="sonota">その他<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDj>
END

    #コマンド

    for($i = 0; $i < $HcommandTotalj; $i++) {
	$kind = $HcomListj[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '無料'
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
<INPUT TYPE="radio" NAME="eku" VALUE="jidou" CHECKED>自動入力系<BR>
END
}else{
    out(<<END);
<INPUT TYPE="radio" NAME="eku" VALUE="jidou">自動入力系<BR>
END
}
    out(<<END);
<SELECT NAME=COMMANDk>
END

    #コマンド
    for($i = 0; $i < $HcommandTotalk; $i++) {
	$kind = $HcomListk[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '無料'
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
<INPUT TYPE="radio" NAME="nmo" VALUE="iti"><font sizu=2>Mode1</font><INPUT TYPE="radio" NAME="nmo" VALUE="nii" CHECKED><font sizu=2>Mode2</font><INPUT TYPE="submit" VALUE="モード変更" NAME="ChangeMode$Hislands[$HcurrentNumber]->{'id'}"><BR>
END
}
out(<<END);
<HR>
<B>座標(</B>
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
<B>数量</B><SELECT NAME=AMOUNT>
END

    # 数量
    for($i = 0; $i < 999; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>
<HR>
<B>目標の島</B><BR>
<SELECT NAME=TARGETID>
$HtargetList<BR>
</SELECT>
<HR>
<B>動作</B><BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=insert CHECKED>挿入
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=write>上書き<BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=delete>削除
<HR>
<INPUT TYPE=submit VALUE="計画送信" NAME=CommandButton$Hislands[$HcurrentNumber]->{'id'}>

</CENTER>
</FORM>
</TD>
<TD $HbgMapCell>
END
    islandMap(1);    # 島の地図、所有者モード
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
${HtagBig_}コメント更新${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
コメント<INPUT TYPE=text NAME=MESSAGE SIZE=80><BR>
パスワード<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE=submit VALUE="コメント更新" NAME=MessageButton$Hislands[$HcurrentNumber]->{'id'}>
</FORM>
</CENTER>
END

}

# 入力済みコマンド表示
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
	$target = "無人";
    }
    $target = "$HtagName_${target}島$H_tagName";
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

    my($j) = sprintf("%02d：", $number + 1);

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
	# ミサイル系
	my($n) = ($arg == 0 ? '無制限' : "${arg}発");
	out("$target$pointへ$name($HtagName_$n$H_tagName)");
    } elsif (($kind == $HcomSendMonster) ||
($kind == $HcomSendMonster3) || 
($kind == $HcomSendMonster4) || 
($kind == $HcomSendMonster5) || 
($kind == $HcomSendMonster2)){
	# 怪獣派遣
	out("$targetへ$name");
    } elsif($kind == $HcomSell) {
	# 食料輸出
	out("$name$value");
    } elsif($kind == $HcomImport) {
# 食料輸入
out("$name$value");
    } elsif($kind == $HcomOilSell) {
	# 食料輸出
	out("$name$value");
    } elsif($kind == $HcomOilImport) {
# 食料輸入
out("$name$value");

} elsif($kind == $HcomPropaganda) {
	# 誘致活動
	out("$name");
if($arg != 0){
    out("($arg回)");
}


  } elsif(($kind == $HcomRob) || ($kind == $HcomRobST)){
    my($rateRob, $buf);
    if($kind == $HcomRob){
      $rateRob = int((100 - $arg) / 2);
    } else {
      $rateRob = int((100 - $arg) / 3);
    }
    out("$targetへ$name(成功確率 約$rateRob%)");
  } elsif(($kind == $HcomShakufi) ||($kind == $HcomShakuse) || ($kind == $HcomShakuth)){
my($kane);
$kane = $arg * 100;
out("$name($kane億円)");
    } elsif(($kind == $HcomMoney) ||
($kind == $HcomMoneyH) ||
($kind == $HcomFoodH) ||
($kind == $HcomSlag) ||
	    ($kind == $HcomFood)) {
	# 援助
	out("$targetへ$name$value");
    } elsif($kind == $HcomDestroy) {
	# 掘削
	if($arg != 0) {
	    out("$pointで$name(予算${value})");
	} else {
	    out("$pointで$name");
	}
}elsif(($kind == $HcomOilH) ||
($kind == $HcomOil)){
	out("$targetへ$name$value");
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
	# 回数付き
	if($arg == 0) {
	    out("$pointで$name");
	} else {
	    out("$pointで$name($arg回)");
	}
    } elsif(($kind == $Hcomkouei)||
($kind == $Hcombouei)||
($kind == $Hcomreiei)||
($kind == $Hcomhatei)||
($kind == $HcomPMSei)||
($kind == $Hcomkanei)){
out("$name");
} elsif($kind == $Hcomtimya){
out("$target$pointへ$name");
} elsif(($kind == $Hcomtaifuu)||
($kind == $Hcomtunami)||
($kind == $Hcomfunka)||
($kind == $Hcominseki)||
($kind == $Hcomdaiinseki)||
($kind == $Hcomjisin)||
($kind == $HcomOoame)||
($kind == $Hcomkasai)||
($kind == $Hcomjibantinka)){
out("$targetに向けて$name");
} elsif($kind == $Hcomkouuti){
out("$targetの攻撃衛星を攻撃");
} elsif($kind == $Hcombouuti){
out("$targetの防御衛星を攻撃");
} elsif($kind == $Hcomreiuti){
out("$targetのレーザー衛星を攻撃");
}elsif($kind == $Hcomkanuti){
out("$targetの監視衛星を攻撃");
}elsif($kind == $HcomPMSuti){
out("$targetのPMS衛星を攻撃");
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
	# 座標付き
	out("$pointで$name");
    }

    out("</FONT></NOBR></A><BR>");
}

# ローカル掲示板
sub tempLbbsHead {
    out(<<END);
<HR>
<CENTER>
${HtagBig_}${HtagName_}${HcurrentName}島${H_tagName}観光者通信${H_tagBig}<BR>
</CENTER>
END
}

# ローカル掲示板入力フォーム
sub tempLbbsInput {
    if ($HlbbsAuth) {
	out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH>名前</TH>
<TH>内容</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD><TEXTAREA NAME="LBBSMESSAGE" ROWS=2 COLS=60></TEXTAREA></TD>
</TR>
<TR>
<TD colspan="2">自分の島：<SELECT NAME="ISLANDID">$HislandList</SELECT>
　パスワード：<INPUT TYPE="password" SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword"><INPUT TYPE="radio" NAME="see" VALUE="public" CHECKED>公開
<INPUT TYPE="radio" NAME="see" VALUE="secret">極秘<br>
<INPUT TYPE="submit" VALUE="記帳する" NAME="LbbsButtonFO$HcurrentID">

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
<TH>名前</TH>
<TH>内容</TH>
<TH>動作</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD><TEXTAREA NAME="LBBSMESSAGE" ROWS=2 COLS=60></TEXTAREA></TD>
<TD><INPUT TYPE="radio" NAME="see" VALUE="public" CHECKED>公開
<INPUT TYPE="radio" NAME="see" VALUE="secret">極秘<br><INPUT TYPE="submit" VALUE="記帳する" NAME="LbbsButtonSS$HcurrentID">
</TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
    }
}

# ローカル掲示板入力フォーム owner mode用
sub tempLbbsInputOW {
    out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH>名前</TH>
<TH COLSPAN=2>内容</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD COLSPAN=2>
<TEXTAREA NAME="LBBSMESSAGE" ROWS=2 COLS=60></TEXTAREA></TD>
</TR>
<TR>
<TH>パスワード</TH>
<TH COLSPAN=2>動作</TH>
</TR>
<TR>
<TD><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword"></TD>
<TD align=right>
<INPUT TYPE="submit" VALUE="記帳する" NAME="LbbsButtonOW$HcurrentID">
</TD>
<TD align=right>
番号
<SELECT NAME=NUMBER>
END
    # 発言番号
    my($j, $i);
    for($i = 0; $i < $HlbbsMax; $i++) {
	$j = $i + 1;
	out("<OPTION VALUE=$i>$j\n");
    }
    out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="削除する" NAME="LbbsButtonDL$HcurrentID">
</TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
}

# ローカル掲示板内容
sub tempLbbsContents {
    my($lbbs, $line);
    $lbbs = $Hislands[$HcurrentNumber]->{'lbbs'};
    out(<<END);
<CENTER>
<TABLE BORDER>
<TR>
<TH>番号</TH>
<TH>記帳内容</TH>
</TR>
END

    my($i);
    for($i = 0; $i < $HlbbsMax; $i++) {
	$line = $lbbs->[$i];
	if($line =~ /([0-9]*)\>(.*)\>(.*)$/) {
	    my($j) = $i + 1;
	    out("<TR><TD align=center>$HtagNumber_$j$H_tagNumber</TD>");

                if ($1 == 5) {
                    # 秘話
if($HmainMode ne 'owner'){
                    out("<TD><center>$HtagLbbsXX_ *** 極秘 ***$H_tagLbbsXX</center></TD></TR>");
                } else {

                    out("<TD>$HtagLbbsXX_ $2 > $3$H_tagLbbsXX</TD></TR>");
                }
}elsif($1 == 0) {
                # 観光者
out("<TD>$HtagLbbsSS_$2 > $3$H_tagLbbsSS</TD></TR>");
	    } else {
		# 島主
		out("<TD>$HtagLbbsOW_$2 > $3$H_tagLbbsOW</TD></TR>");
	    }
	}
    }

    out(<<END);
</TD></TR></TABLE></CENTER>
END
}

# ローカル掲示板で名前かメッセージがない場合
sub tempLbbsNoMessage {
    out(<<END);
${HtagBig_}名前または内容の欄が空欄です。${H_tagBig}$HtempBack
END
}

# 書きこみ削除
sub tempLbbsDelete {
    out(<<END);
${HtagBig_}記帳内容を削除しました${H_tagBig}<HR>
END
}

# コマンド登録
sub tempLbbsAdd {
    out(<<END);
${HtagBig_}記帳を行いました${H_tagBig}<HR>
END
}

# コマンド削除
sub tempCommandDelete {
    out(<<END);
${HtagBig_}コマンドを削除しました${H_tagBig}<HR>
END
}

# コマンド登録
sub tempCommandAdd {
    out(<<END);
${HtagBig_}コマンドを登録しました${H_tagBig}<HR>
END
}

# コメント変更成功
sub tempComment {
    out(<<END);
${HtagBig_}コメントを更新しました${H_tagBig}<HR>
END
}

# 近況
sub tempRecent {
    my($mode) = @_;
    out(<<END);
<HR>
${HtagBig_}${HtagName_}${HcurrentName}島${H_tagName}の近況${H_tagBig}<BR>
END
    logPrintLocal($mode);
}

1;
