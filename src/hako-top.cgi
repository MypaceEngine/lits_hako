#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# トップモジュール(ver1.00)
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
# トップページモード
#----------------------------------------------------------------------
# メイン
sub topPageMain {
    # 開放
    unlock();

    # テンプレート出力
    tempTopPage();
}

# トップページ
sub tempTopPage {
    # タイトル
    out(<<END);
${HtagTitle_}$Htitle${H_tagTitle}
END

    # デバッグモードなら「ターンを進める」ボタン
    if($Hdebug == 1) {
        out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="submit" VALUE="ターンを進める" NAME="TurnButton">
</FORM>
END
    }

    my($mStr1) = '';
    if($HhideMoneyMode != 0) {
	$mStr1 = "<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}資金${H_tagTH}</NOBR></TH>";
    }

    # フォーム
    my($remain) = $HunitTime + $HislandLastTime - time;
    out(<<END);
<H1>${HtagHeader_}ターン$HislandTurn${H_tagHeader}　</H1>
<FORM name="RemainForm"><INPUT name="RemainTime" size="30" type="text" readonly></FORM><SCRIPT language="JavaScript">
<!--
nextTurn = ${remain}; loadDate = new Date();
timerID = setTimeout('dispRemainTime()', 100);
function dispRemainTime() { clearTimeout(timerID);
document.RemainForm.RemainTime.value = getRemainTime();
timerID = setTimeout('dispRemainTime()', 1000);}
function getRemainTime() {
now = new Date();msec = now.getTime() - loadDate.getTime();
msec -= msec % 1000; msec /= 1000;msec = nextTurn - msec;
if (msec < 0) {msec = 0;}
sec = msec % 60; msec = (msec - sec) / 60;
min = msec % 60; hour = (msec - min) / 60;
if (hour < 10) {hour = "0" + hour;}
if (min < 10) {min = "0" + min;}
if (sec < 10) {sec = "0" + sec;}
return "次のターンまで残り" + hour + ":" + min + ":" + sec;}
//-->
</SCRIPT>
<hr>
<H1>${HtagHeader_}自分の島へ${H_tagHeader}</H1>
<FORM action="$HthisFile" method="POST">
あなたの島の名前は？<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR>

パスワードをどうぞ！！<BR>
<INPUT TYPE="password" NAME="PASSWORD" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="radio" NAME="nmo" VALUE="iti" CHECKED>Mode1<INPUT TYPE="radio" NAME="nmo" VALUE="nii">Mode2<BR>
<INPUT TYPE="submit" VALUE="開発しに行く" NAME="OwnerButton">
</FORM>

<H1>${HtagHeader_}Javaで計画へ${H_tagHeader}</H1>（イントラネット＜UNIXマシン＞からではご使用いただけません）

<SCRIPT language="JavaScript">
<!--
function newProjectWindow()
{
  projectWindow = window.open("", "projectWindow", "menubar=no,toolbar=no,location=no,directories=no,status=yes,scrollbars=yes,resizable=yes,width=800,height=640");
  document.javaForm.windowmode.value = "window";
  document.javaForm.target = "projectWindow";
  document.javaForm.submit();
  document.javaForm.windowmode.value = "normal";
  document.javaForm.target = "";
}
//-->
</SCRIPT>

<FORM name="javaForm" action="$HjavaFile" method="POST">
あなたの島の名前は？<BR>
<SELECT NAME="island">
$HislandList
</SELECT><BR>

パスワードをどうぞ！！<BR>
<INPUT TYPE="hidden" NAME="action" VALUE="login">
<INPUT TYPE="hidden" NAME="windowmode" VALUE="normal">
<INPUT TYPE="password" NAME="password" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="Javaで計画" NAME="OwnerButton">　<INPUT TYPE="button" VALUE="新しいWindow" onClick="newProjectWindow()"><BR>
<INPUT TYPE="radio"  VALUE="APPLET" NAME="tag" CHECKED>Default VM
<INPUT TYPE="radio"  VALUE="PLUGIN" NAME="tag">Java Plug-in

</FORM>
END
my($kai,$jis,$tun,$tai,$in,$din,$fun,$kas,$dis,$ooa);
$kai = $HdisMonster * 0.1;
$jis = $HdisEarthquake * 0.1;
$tun = $HdisTsunami * 0.1;
$tai = $HdisTyphoon * 0.1;
$in = $HdisMeteo * 0.1;
$din = $HdisHugeMeteo * 0.1;
$fun = $HdisEruption * 0.1;
$kas = $HdisFire * 0.1;
$dis = $HdisDisa * 0.1;
$ooa = $HdisHardRain * 0.1;

	out(<<END);
<hr><H1>${HtagHeader_}災害及び怪獣発生確率${H_tagHeader}＜HKK調べ＞</H1>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}災害名${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}怪獣${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}地震${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}津波${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}台風${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}隕石${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}巨大隕石${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}噴火${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}火災${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}伝染病${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}大雨${H_tagTH}</NOBR></TH>
</TR>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}確率${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$kai％</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$jis％</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$tun％</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$tai％</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$in％</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$din％</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$fun％</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$kas％</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$dis％</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$ooa％</NOBR></TH>
</TR>
</table>

<script language="JavaScript">
<!--

function _ses() {
 m1 = "戦争愛好同盟について";
 m2 = "戦争愛好同盟は戦争愛好者のための同盟です。";
 m3 = "この同盟にはいると同盟加入島の間で戦争を";
 m4 = "行えます。ちなみにこの同盟にはいることに";
 m5 = "よって平和愛好同盟には入れなくなります";
m6= "                                            　　　　　　　　　　　　　　　　";
  alert(m1+m6+m2+m3+m4+m5);
}

//-->
</script><script language="JavaScript">
<!--

function _heis() {
 m1 = "平和愛好同盟について";
 m2 = "平和愛好同盟は平和愛好者のための同盟です。";
 m3 = "この同盟にはいると自分の島が平和主義で";
 m4 = "あることを宣言できます。ちなみにこの同盟に";
 m5 = "はいることよって戦争愛好同盟には入れなく";
 m6 = "なります。";
m7 =  "     　　　                                 　　　　　　　　　　　　　　　";

    alert(m1+m7+m2+m3+m4+m5+m6);
}

//-->
</script><script language="JavaScript">
<!--

function _inos() {
 m1 = "反いのら同盟について";
 m2 = "反いのら同盟はいのら嫌いの人のための同盟です。";
 m3 = "この同盟にはいると自分の島にいのらが出たときに";
 m4 = "ほかの島の助けを借りることができます。たがい";
 m5 = "に助け合い、いのら撃滅のために日々精進してください。";
 m6= "          　　　                            　　　　　　　　　　　　　　　";
  alert(m1+m6+m2+m3+m4+m5);
}

//-->
</script>
<HR>
<H1>${HtagHeader_}同盟表${H_tagHeader}</H1>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}同盟名${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}加入数${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}加入島${H_tagTH}</NOBR></TH>
</TR>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR><IMG SRC=\"sei.gif\"  WIDTH=16 HEIGHT=16><A STYlE=\"text-decoration:none\" HREF=\"JavaScript:_ses()\">${HtagTH_}戦争愛好同盟${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$sek${HtagTH_}島${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$seu${H_tagTH}</NOBR></TH>
</tr>
<tr>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR><IMG SRC=\"hei.gif\"  WIDTH=16 HEIGHT=16><A STYlE=\"text-decoration:none\" HREF=\"JavaScript:_heis()\">${HtagTH_}平和愛好同盟${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$hek${HtagTH_}島${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$heu${H_tagTH}</NOBR></TH>
</tr>
<tr>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR><IMG SRC=\"ino.gif\"  WIDTH=16 HEIGHT=16><A STYlE=\"text-decoration:none\" HREF=\"JavaScript:_inos()\">${HtagTH_}反いのら同盟${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$ink${HtagTH_}島${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$inu${H_tagTH}</NOBR></TH>
</tr>
</TABLE>
<hr>
<H1>${HtagHeader_}戦争愛好同盟陣営表${H_tagHeader}</H1>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}陣営名${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}島数${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}加入島${H_tagTH}</NOBR></TH>
</TR>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}帝国軍${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$tei${HtagTH_}島${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$teu${H_tagTH}</NOBR></TH>
</tr>
<tr>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}共和国軍${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$kyo${HtagTH_}島${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$kyu${H_tagTH}</NOBR></TH>
</tr>
<tr>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}無所属${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$muo${HtagTH_}島${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$muu${H_tagTH}</NOBR></TH>
</tr>
</TABLE>
<hr>
<H1>${HtagHeader_}現在の王位所有島${H_tagHeader}</H1>
<TABLE BORDER>
<tr>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}王位${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}皇帝${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}食料王${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}工業王${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}採掘王${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}温泉王${H_tagTH}</A><R></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}動物園王${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}デパート王${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}いのらキラー王${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}浄水場王${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}発電王${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}ゴミ処理場王${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}石油王${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}レジャー王${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}収入王${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}資金王${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}面積王${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}求人王${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}森林王${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}鉄道王${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}会長${H_tagTH}</A></NOBR></TH></tr>
<tr>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}所有島${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$biou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$niou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$kiou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$uoou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$oiou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$diou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$deou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$moou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$joou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$hoou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$goou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$soou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$loou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$yoou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$eoou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$aoou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$ioou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$foou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$toou${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}インターネッ島${H_tagTH}</A></NOBR></TH></tr>
</table>
<hr>
<H1>${HtagHeader_}諸島の状況${H_tagHeader}</H1>
<P>
島の名前をクリックすると、<B>観光</B>することができます。
</P>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}順位${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}島${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}島旗${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}就業率${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}面積${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}怪獣数${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}食料${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}最大発電量${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}浄水場規模${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}ゴミ処理施設規模${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}ゴミ蓄積量${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}石油貯蓄量${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}最大食料生産規模${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}総求人規模${H_tagTH}</NOBR></TH>

<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}保有衛星${H_tagTH}</NOBR></TH>
</TR>
END

    my($island, $j, $farm, $factory, $mountain, $name, $id, $prize, $ii);
    for($ii = 0; $ii < $HislandNumber; $ii++) {
	$j = $ii + 1;
	$island = $Hislands[$ii];

	$id = $island->{'id'};
	$shoku = $island->{'shoku'};
	$sigoto = $island->{'sigoto'};
$Jous = $island->{'Jous'};
$hatu = $island->{'hatud'};
$gomi = $island->{'gomi'};
$Oil = $island->{'oil'};
	$shoku = ($shoku == 0) ? "保有せず" : "${shoku}00トン";
	$sigoto = ($sigoto == 0) ? "なし" : "${sigoto}0$HunitPop";
	$Jous = ($Jous == 0) ? "保有せず" : "${Jous}0000��";
	$hatu = ($hatu == 0) ? "保有せず" : "${hatu}000Kw";
	$gomi = ($gomi == 0) ? "保有せず" : "${gomi}00トン";
	$Oil = ($Oil == 0) ? "保有せず" : "${Oil}トン";

	if($island->{'absent'}  == 0) {
if($island->{'sen'} == 11){
		$name = "${HtagName_}(帝)$island->{'name'}島${H_tagName}";
}elsif($island->{'sen'} == 21){
$name = "${HtagName_}(共)$island->{'name'}島${H_tagName}";
}elsif($island->{'sen'} == 1){
$name = "${HtagName_}(無)$island->{'name'}島${H_tagName}";
}else{
$name = "${HtagName_}$island->{'name'}島${H_tagName}";
}
	} else {
if($island->{'sen'} == 11){
		$name = "${HtagName2_}(帝)$island->{'name'}島($island->{'absent'})${H_tagName2}";
}elsif($island->{'sen'} == 21){
$name = "${HtagName2_}(共)$island->{'name'}島($island->{'absent'})${H_tagName2}";
}elsif($island->{'sen'} == 1){
$name = "${HtagName2_}(無)$island->{'name'}島($island->{'absent'})${H_tagName2}";
}else{
$name = "${HtagName2_}$island->{'name'}島($island->{'absent'})${H_tagName2}";
}
	}
  my($oStr) = '';
  if($island->{'ownername'} eq ''){
    $oStr = "<TD $HbgCommentCell COLSPAN=18 align=left nowrap=nowrap><NOBR>${HtagTH_}コメント : ${H_tagTH}$island->{'comment'}</NOBR></TD>";
  } else {
    $oStr = "<TD $HbgCommentCell COLSPAN=18 align=left nowrap=nowrap><NOBR><font color=#0000ff>$island->{'ownername'} : </font>$island->{'comment'}</NOBR></TD>";
  }
my($fStr) = '';
  if($island->{'flagname'} eq ''){
    $fStr = "";
  } else {
    $fStr = "<img src=$island->{'flagname'} width = 56 height = 42>";
  }
my($ou) = "";
if($island->{'id'} == $booa){
$ou .="<IMG SRC=\"king.gif\" ALT=\"皇帝\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == 38){
$ou .="<IMG SRC=\"kai.gif\" ALT=\"会長\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $nioa){
$ou .= "<IMG SRC=\"land7.gif\" ALT=\"食料王\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $kioa){
$ou .="<IMG SRC=\"land8.gif\" ALT=\"工業王\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $oioa){
$ou .="<IMG SRC=\"land22.gif\" ALT=\"温泉王\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $dioa){
$ou .="<IMG SRC=\"land19.gif\" ALT=\"動物園王\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $deoa){
$ou .="<IMG SRC=\"land20.gif\" ALT=\"デパート王\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $mooa){
$ou .="<IMG SRC=\"kira.gif\" ALT=\"いのらキラー王\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $jooa){
$ou .="<IMG SRC=\"land37.gif\" ALT=\"浄水場王\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $hooa){
$ou .="<IMG SRC=\"land38.gif\" ALT=\"発電王\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $gooa){
$ou .="<IMG SRC=\"land39.gif\" ALT=\"ゴミ処理場王\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $sooa){
$ou .="<IMG SRC=\"land16.gif\" ALT=\"石油王\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $looa){
$ou .="<IMG SRC=\"land54.gif\" ALT=\"レジャー王\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $yooa){
$ou .="<IMG SRC=\"kane.gif\" ALT=\"収入王\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $eooa){
$ou .="<IMG SRC=\"sikin.gif\" ALT=\"資金王\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $aooa){
$ou .="<IMG SRC=\"menseki.gif\" ALT=\"面積王\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $iooa){
$ou .="<IMG SRC=\"hito.gif\" ALT=\"求人王\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $uooa){
$ou .="<IMG SRC=\"land15.gif\" ALT=\"採掘王\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $fioa){
$ou .="<IMG SRC=\"land6.gif\" ALT=\"森林王\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $tioa){
$ou .="<IMG SRC=\"senro.gif\" ALT=\"鉄道王\" WIDTH=16 HEIGHT=16> ";
}
my($shuu) = 0;
my($shuo) = "";
$shuu =int(($island->{'sigoto'}  / $island->{'pop'}) * 1000);
if($shuu >= 100){
$shuo = "100％"
} else {
$shuo = "約$shuu％"
}
my($teou) = "";
if($island->{'teikou'} >0){
$teou ="＜$island->{'teikou'}＞";
}
my($poke) = 0;
my($poke2) = "";
if ($island->{'score'} >= 1){
$poke = $island->{'score'};
# $poke = "$poke"
$poke2 = "現在${poke}匹";
} else {
$poke2 = "存在せず";
}
my($ei) = "";
if ($island->{'kouei'} >= 1){
$ei .= "<IMG SRC=\"eisei3.gif\" ALT=\"攻撃衛星\" WIDTH=16 HEIGHT=16>";
}
if ($island->{'kanei'} >= 1){
$ei .= "<IMG SRC=\"eisei5.gif\" ALT=\"監視衛星\" WIDTH=16 HEIGHT=16>";
}
if ($island->{'bouei'} >= 1){
$ei .= "<IMG SRC=\"eisei2.gif\" ALT=\"防御衛星\" WIDTH=16 HEIGHT=16>";
}
if ($island->{'reiei'} >= 1){
$ei .= "<IMG SRC=\"eisei4.gif\" ALT=\"レーザー衛星\" WIDTH=16 HEIGHT=16>";
}
if ($island->{'pmsei'} >= 1){
$ei .= "<IMG SRC=\"eisei6.gif\" ALT=\"PMS衛星\" WIDTH=16 HEIGHT=16>";
}
if ($island->{'hatei'} >= 1){
$ei .= "<IMG SRC=\"eisei1.gif\" ALT=\"発電衛星\" WIDTH=16 HEIGHT=16>";
}
my($senmei) = "";
if ($island->{'sen'} > 0){
$senmei = "<IMG SRC=\"sei.gif\" ALT=\"戦争愛好同盟\" WIDTH=16 HEIGHT=16>";
}
my($heimei) = "";
if ($island->{'hei'} == 1){
$heimei = "<IMG SRC=\"hei.gif\" ALT=\"平和愛好同盟\" WIDTH=16 HEIGHT=16>";
}
my($inomei) = "";
if ($island->{'ino'} == 1){
$inomei = "<IMG SRC=\"ino.gif\" ALT=\"反いのら同盟\" WIDTH=16 HEIGHT=16>";
}
	$prize = $island->{'prize'};
	my($flags, $monsters, $turns);
	$prize =~ /([0-9]*),([0-9]*),(.*)/;
	$flags = $1;
	$monsters= $2;
	$turns = $3;
	$prize = '';
$Prime = '';
$Pranu = '';
$Prera = '';
$Prini = '';
if($island->{'empe'} > 0){
$prize .= "<IMG SRC=\"koutei.gif\" ALT=\"$island->{'empe'}回\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'top'} > 0){
$prize .= "<IMG SRC=\"top.gif\" ALT=\"$island->{'top'}回\" WIDTH=16 HEIGHT=16> ";
}
	# ターン杯の表示
	while($turns =~ s/([0-9]*),//) {
if($1 % 10000 == 0){
$Prini .= "$1${Hprize[0]},";
}elsif ($1 % 1000 == 0){
$Pranu .= "$1${Hprize[0]},";
}elsif ($1 % 100 == 0){
$Prera .= "$1${Hprize[0]},";
}else{
$Prime .= "$1${Hprize[0]},";
}
}
if($Prime  eq ''){
} else {
$prize .= "<IMG SRC=\"prize0.gif\" ALT=\"$Prime\" WIDTH=16 HEIGHT=16> ";
}
if($Prera  eq ''){
} else {
$prize .= "<IMG SRC=\"prize10.gif\" ALT=\"$Prera\" WIDTH=16 HEIGHT=16> ";
}
if($Pranu  eq ''){
} else {
$prize .= "<IMG SRC=\"prize11.gif\" ALT=\"$Pranu\" WIDTH=16 HEIGHT=16> ";
}
if($Prini  eq ''){
} else {
$prize .= "<IMG SRC=\"prize12.gif\" ALT=\"$Prime\" WIDTH=16 HEIGHT=16> ";
}
	# 名前に賞の文字を追加
	my($f) = 1;
	my($i);
	for($i = 1; $i < 10; $i++) {
if($i == 8){
if($flags & $f) {
$prize .= "<IMG SRC=\"prize15.gif\" ALT=\"${Hprize[8]}\" WIDTH=16 HEIGHT=16> ";
}
}elsif($i == 9){
if($flags & $f) {
$prize .= "<IMG SRC=\"prize8.gif\" ALT=\"${Hprize[9]}\" WIDTH=16 HEIGHT=16> ";
}
}else{
	    if($flags & $f) {
		$prize .= "<IMG SRC=\"prize${i}.gif\" ALT=\"${Hprize[$i]}\" WIDTH=16 HEIGHT=16> ";
	    }
}
if($i == 3){
  if($flags & 512) {
		$prize .= "<IMG SRC=\"prize13.gif\" ALT=\"${Hprize[10]}\" WIDTH=16 HEIGHT=16> ";
	    }
}
if($i == 6){
 if($flags & 1024) {
	$prize .= "<IMG SRC=\"prize14.gif\" ALT=\"${Hprize[11]}\" WIDTH=16 HEIGHT=16> ";
	    }
}
if($i == 9){
if($flags & 2048) {
		$prize .= "<IMG SRC=\"prize9.gif\" ALT=\"${Hprize[12]}\" WIDTH=16 HEIGHT=16> ";
	    }
}
	    $f *= 2;
	}

	# 倒した怪獣リスト
	$f = 1;
	my($max) = -1;
	my($mNameList) = '';
my($monsnumber) = $island->{'monsnumber'};
my(@monsnumber) = split(/,/ ,$monsnumber);
	for($i = 0; $i < $HmonsterNumber; $i++) {
	    if($monsters & $f) {
		$mNameList .= "[$HmonsterName[$i],($monsnumber[$i]頭)] ";
		$max = $i;
	    }
	    $f *= 2;
	}
	if($max != -1) {
	    $prize .= "<IMG SRC=\"${HmonsterImage[$max]}\" ALT=\"$mNameList\" WIDTH=16 HEIGHT=16> ";
	}


	my($mStr1) = '';
	if($HhideMoneyMode == 1) {
	    $mStr1 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'money'}$HunitMoney</NOBR></TD>";
	} elsif($HhideMoneyMode == 2) {
	    my($mTmp) = aboutMoney($island->{'money'});
	    $mStr1 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$mTmp</NOBR></TD>";
	}

	out(<<END);
<TR>
<TD $HbgNumberCell ROWSPAN=2 align=center nowrap=nowrap><NOBR>${HtagNumber_}$j${H_tagNumber}</NOBR></TD>
<TD $HbgNameCell ROWSPAN=2 align=left nowrap=nowrap>
<NOBR>
<A STYlE=\"text-decoration:none\" HREF="${HthisFile}?Sight=${id}">
$name
</A>
<A STYlE=\"text-decoration:none\" >
$senmei
</A>
<A STYlE=\"text-decoration:none\" >
$heimei
</A>
<A STYlE=\"text-decoration:none\" >
$inomei
</A>
</NOBR><BR>
$prize
<A STYlE=\"text-decoration:none\" >
$ou
</A>
</TD>
<TD $HbgNumberCell ROWSPAN=2 align=center nowrap=nowrap><NOBR>$fStr
</TD><TD $HbgInfoCell align=right nowrap=nowrap>
<NOBR>$island->{'pop'}$HunitPop</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$shuo</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'area'}$HunitArea</NOBR></TD>
$mStr1
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$poke2</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'food'}$HunitFood</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$hatu</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$Jous</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$gomi</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'slag'}トン</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$Oil</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$shoku</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$sigoto</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$ei</NOBR></TD>
</TR>
<TR>
$oStr
</TR>
END
    }

    out(<<END);
</TABLE>

<HR>
<H1>${HtagHeader_}新しい島を探す${H_tagHeader}</H1>
END
if($HislandNumber < $HmaxIsland) {
if($HdefaultPassword eq ''){
	out(<<END);
<FORM action="$HthisFile" method="POST">
どんな名前をつける予定？<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>島<BR>
パスワードは？<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
念のためパスワードをもう一回<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>

<INPUT TYPE="submit" VALUE="探しに行く" NAME="NewIslandButton">
</FORM>
END
}else{
out(<<END);
すでに島を登録しているので登録できません。
登録していないのにこれが表示された方は掲示板にお書きください。
END
}
    } else {
	out(<<END);
        島の数が最大数です・・・現在登録できません。
END
    }

    out(<<END);
<HR>
<H1>${HtagHeader_}島の名前とパスワードの変更${H_tagHeader}</H1>
<P>
(注意)名前の変更には$HcostChangeName${HunitMoney}かかります。
</P>
<FORM action="$HthisFile" method="POST">
どの島ですか？<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<BR>
どんな名前に変えますか？(変更する場合のみ)<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>島<BR>
パスワードは？(必須)<BR>
<INPUT TYPE="password" NAME="OLDPASS" SIZE=32 MAXLENGTH=32><BR>
新しいパスワードは？(変更する時のみ)<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
念のためパスワードをもう一回(変更する時のみ)<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>

<INPUT TYPE="submit" VALUE="変更する" NAME="ChangeInfoButton">
</FORM><HR>
<H1>${HtagHeader_}オーナー名の変更${H_tagHeader}</H1>
<FORM action="$HthisFile" method="POST">
どの島ですか？<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<BR>
オーナー名
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=32 MAXLENGTH=32><BR>
パスワード
<INPUT TYPE="password" NAME="OLDPASS" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="変更する" NAME="ChangeOwnerButton">
</FORM><HR>
<H1>${HtagHeader_}島旗の変更${H_tagHeader}</H1>
<FORM action="$HthisFile" method="POST">
どの島ですか？<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<BR>
島旗のURL
<INPUT TYPE="text" NAME="FLAGNAME" VALUE="http://" SIZE=64 MAXLENGTH=64><BR>
パスワード
<INPUT TYPE="password" NAME="OLDPASS" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="変更する" NAME="ChangeFlagButton">
</FORM>
<hr>
END
$ref = $ENV{'REMOTE_ADDR'};
$reb = $ENV{'REMOTE_HOST'};
$rec = $ENV{'HTTP_USER_AGENT'};
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
$rea = "$year/$mon/$mday $hour\:$min";
open(KLOG,">> doukana.log");
print KLOG "$rea . $ref . $reb . $rec\n";
close(KLOG);
    out(<<END);
<H1>${HtagHeader_}最近の出来事${H_tagHeader}</H1>
END
    logPrintTop();
    out(<<END);
<H1>${HtagHeader_}発見の記録${H_tagHeader}</H1>
END
    historyPrint();
}

# トップページ用ログ表示
sub logPrintTop {
    my($i);
    for($i = 0; $i < $HtopLogTurn; $i++) {
	logFilePrint($i, 0, 0);
    }
}

# 記録ファイル表示
sub historyPrint {
    open(HIN, "${HdirName}/hakojima.his");
    my(@line, $l);
    while($l = <HIN>) {
	chomp($l);
	push(@line, $l);
    }
    @line = reverse(@line);

    foreach $l (@line) {
	$l =~ /^([0-9]*),(.*)$/;
	out("<NOBR>${HtagNumber_}ターン${1}${H_tagNumber}：${2}</NOBR><BR>\n");
    }
    close(HIN);
}

1;
