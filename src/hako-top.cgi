#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �ȥåץ⥸�塼��(ver1.00)
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
# �ȥåץڡ����⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub topPageMain {
    # ����
    unlock();

    # �ƥ�ץ졼�Ƚ���
    tempTopPage();
}

# �ȥåץڡ���
sub tempTopPage {
    # �����ȥ�
    out(<<END);
${HtagTitle_}$Htitle${H_tagTitle}
END

    # �ǥХå��⡼�ɤʤ�֥������ʤ��ץܥ���
    if($Hdebug == 1) {
        out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="submit" VALUE="�������ʤ��" NAME="TurnButton">
</FORM>
END
    }

    my($mStr1) = '';
    if($HhideMoneyMode != 0) {
	$mStr1 = "<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>";
    }

    # �ե�����
    my($remain) = $HunitTime + $HislandLastTime - time;
    out(<<END);
<H1>${HtagHeader_}������$HislandTurn${H_tagHeader}��</H1>
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
return "���Υ�����ޤǻĤ�" + hour + ":" + min + ":" + sec;}
//-->
</SCRIPT>
<hr>
<H1>${HtagHeader_}��ʬ�����${H_tagHeader}</H1>
<FORM action="$HthisFile" method="POST">
���ʤ������̾���ϡ�<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR>

�ѥ���ɤ�ɤ�������<BR>
<INPUT TYPE="password" NAME="PASSWORD" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="radio" NAME="nmo" VALUE="iti" CHECKED>Mode1<INPUT TYPE="radio" NAME="nmo" VALUE="nii">Mode2<BR>
<INPUT TYPE="submit" VALUE="��ȯ���˹Ԥ�" NAME="OwnerButton">
</FORM>

<H1>${HtagHeader_}Java�Ƿײ��${H_tagHeader}</H1>�ʥ���ȥ�ͥåȡ�UNIX�ޥ���䤫��ǤϤ����Ѥ��������ޤ����

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
���ʤ������̾���ϡ�<BR>
<SELECT NAME="island">
$HislandList
</SELECT><BR>

�ѥ���ɤ�ɤ�������<BR>
<INPUT TYPE="hidden" NAME="action" VALUE="login">
<INPUT TYPE="hidden" NAME="windowmode" VALUE="normal">
<INPUT TYPE="password" NAME="password" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="Java�Ƿײ�" NAME="OwnerButton">��<INPUT TYPE="button" VALUE="������Window" onClick="newProjectWindow()"><BR>
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
<hr><H1>${HtagHeader_}�ҳ��ڤӲ���ȯ����Ψ${H_tagHeader}��HKKĴ�١�</H1>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�ҳ�̾${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�Ͽ�${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}ʮ��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�к�${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�籫${H_tagTH}</NOBR></TH>
</TR>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}��Ψ${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$kai��</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$jis��</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$tun��</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$tai��</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$in��</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$din��</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$fun��</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$kas��</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$dis��</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$ooa��</NOBR></TH>
</TR>
</table>

<script language="JavaScript">
<!--

function _ses() {
 m1 = "���谦��Ʊ���ˤĤ���";
 m2 = "���谦��Ʊ�������谦���ԤΤ����Ʊ���Ǥ���";
 m3 = "����Ʊ���ˤϤ����Ʊ��������δ֤������";
 m4 = "�Ԥ��ޤ������ʤߤˤ���Ʊ���ˤϤ��뤳�Ȥ�";
 m5 = "��ä�ʿ�°���Ʊ���ˤ�����ʤ��ʤ�ޤ�";
m6= "                                            ��������������������������������";
  alert(m1+m6+m2+m3+m4+m5);
}

//-->
</script><script language="JavaScript">
<!--

function _heis() {
 m1 = "ʿ�°���Ʊ���ˤĤ���";
 m2 = "ʿ�°���Ʊ����ʿ�°����ԤΤ����Ʊ���Ǥ���";
 m3 = "����Ʊ���ˤϤ���ȼ�ʬ���礬ʿ�¼����";
 m4 = "���뤳�Ȥ�����Ǥ��ޤ������ʤߤˤ���Ʊ����";
 m5 = "�Ϥ��뤳�Ȥ�ä����谦��Ʊ���ˤ�����ʤ�";
 m6 = "�ʤ�ޤ���";
m7 =  "     ������                                 ������������������������������";

    alert(m1+m7+m2+m3+m4+m5+m6);
}

//-->
</script><script language="JavaScript">
<!--

function _inos() {
 m1 = "ȿ���Τ�Ʊ���ˤĤ���";
 m2 = "ȿ���Τ�Ʊ���Ϥ��Τ�����οͤΤ����Ʊ���Ǥ���";
 m3 = "����Ʊ���ˤϤ���ȼ�ʬ����ˤ��Τ餬�Ф��Ȥ���";
 m4 = "�ۤ�����ν�����ڤ�뤳�Ȥ��Ǥ��ޤ���������";
 m5 = "�˽����礤�����Τ���ǤΤ�����������ʤ��Ƥ���������";
 m6= "          ������                            ������������������������������";
  alert(m1+m6+m2+m3+m4+m5);
}

//-->
</script>
<HR>
<H1>${HtagHeader_}Ʊ��ɽ${H_tagHeader}</H1>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}Ʊ��̾${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}������${H_tagTH}</NOBR></TH>
</TR>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR><IMG SRC=\"sei.gif\"  WIDTH=16 HEIGHT=16><A STYlE=\"text-decoration:none\" HREF=\"JavaScript:_ses()\">${HtagTH_}���谦��Ʊ��${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$sek${HtagTH_}��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$seu${H_tagTH}</NOBR></TH>
</tr>
<tr>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR><IMG SRC=\"hei.gif\"  WIDTH=16 HEIGHT=16><A STYlE=\"text-decoration:none\" HREF=\"JavaScript:_heis()\">${HtagTH_}ʿ�°���Ʊ��${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$hek${HtagTH_}��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$heu${H_tagTH}</NOBR></TH>
</tr>
<tr>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR><IMG SRC=\"ino.gif\"  WIDTH=16 HEIGHT=16><A STYlE=\"text-decoration:none\" HREF=\"JavaScript:_inos()\">${HtagTH_}ȿ���Τ�Ʊ��${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$ink${HtagTH_}��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$inu${H_tagTH}</NOBR></TH>
</tr>
</TABLE>
<hr>
<H1>${HtagHeader_}���谦��Ʊ���ر�ɽ${H_tagHeader}</H1>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�ر�̾${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}������${H_tagTH}</NOBR></TH>
</TR>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$tei${HtagTH_}��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$teu${H_tagTH}</NOBR></TH>
</tr>
<tr>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���¹�${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$kyo${HtagTH_}��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$kyu${H_tagTH}</NOBR></TH>
</tr>
<tr>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}̵��°${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>$muo${HtagTH_}��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}$muu${H_tagTH}</NOBR></TH>
</tr>
</TABLE>
<hr>
<H1>${HtagHeader_}���ߤβ��̽�ͭ��${H_tagHeader}</H1>
<TABLE BORDER>
<tr>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}������${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���Ȳ�${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�η���${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}������${H_tagTH}</A><R></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}ưʪ�ದ${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�ǥѡ��Ȳ�${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���Τ饭�顼��${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����첦${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}ȯ�Ų�${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���߽����첦${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}������${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�쥸�㡼��${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}������${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}��Ⲧ${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���Ѳ�${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}��Ͳ�${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���Ӳ�${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}Ŵƻ��${H_tagTH}</A></NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}��Ĺ${H_tagTH}</A></NOBR></TH></tr>
<tr>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}��ͭ��${H_tagTH}</A></NOBR></TH>
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
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���󥿡��ͥ���${H_tagTH}</A></NOBR></TH></tr>
</table>
<hr>
<H1>${HtagHeader_}����ξ���${H_tagHeader}</H1>
<P>
���̾���򥯥�å�����ȡ�<B>�Ѹ�</B>���뤳�Ȥ��Ǥ��ޤ���
</P>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����Ψ${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���ÿ�${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����ȯ����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���߽������ߵ���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���翩����������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���͵���${H_tagTH}</NOBR></TH>

<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}��ͭ����${H_tagTH}</NOBR></TH>
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
	$shoku = ($shoku == 0) ? "��ͭ����" : "${shoku}00�ȥ�";
	$sigoto = ($sigoto == 0) ? "�ʤ�" : "${sigoto}0$HunitPop";
	$Jous = ($Jous == 0) ? "��ͭ����" : "${Jous}0000��";
	$hatu = ($hatu == 0) ? "��ͭ����" : "${hatu}000Kw";
	$gomi = ($gomi == 0) ? "��ͭ����" : "${gomi}00�ȥ�";
	$Oil = ($Oil == 0) ? "��ͭ����" : "${Oil}�ȥ�";

	if($island->{'absent'}  == 0) {
if($island->{'sen'} == 11){
		$name = "${HtagName_}(��)$island->{'name'}��${H_tagName}";
}elsif($island->{'sen'} == 21){
$name = "${HtagName_}(��)$island->{'name'}��${H_tagName}";
}elsif($island->{'sen'} == 1){
$name = "${HtagName_}(̵)$island->{'name'}��${H_tagName}";
}else{
$name = "${HtagName_}$island->{'name'}��${H_tagName}";
}
	} else {
if($island->{'sen'} == 11){
		$name = "${HtagName2_}(��)$island->{'name'}��($island->{'absent'})${H_tagName2}";
}elsif($island->{'sen'} == 21){
$name = "${HtagName2_}(��)$island->{'name'}��($island->{'absent'})${H_tagName2}";
}elsif($island->{'sen'} == 1){
$name = "${HtagName2_}(̵)$island->{'name'}��($island->{'absent'})${H_tagName2}";
}else{
$name = "${HtagName2_}$island->{'name'}��($island->{'absent'})${H_tagName2}";
}
	}
  my($oStr) = '';
  if($island->{'ownername'} eq ''){
    $oStr = "<TD $HbgCommentCell COLSPAN=18 align=left nowrap=nowrap><NOBR>${HtagTH_}������ : ${H_tagTH}$island->{'comment'}</NOBR></TD>";
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
$ou .="<IMG SRC=\"king.gif\" ALT=\"����\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == 38){
$ou .="<IMG SRC=\"kai.gif\" ALT=\"��Ĺ\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $nioa){
$ou .= "<IMG SRC=\"land7.gif\" ALT=\"������\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $kioa){
$ou .="<IMG SRC=\"land8.gif\" ALT=\"���Ȳ�\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $oioa){
$ou .="<IMG SRC=\"land22.gif\" ALT=\"������\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $dioa){
$ou .="<IMG SRC=\"land19.gif\" ALT=\"ưʪ�ದ\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $deoa){
$ou .="<IMG SRC=\"land20.gif\" ALT=\"�ǥѡ��Ȳ�\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $mooa){
$ou .="<IMG SRC=\"kira.gif\" ALT=\"���Τ饭�顼��\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $jooa){
$ou .="<IMG SRC=\"land37.gif\" ALT=\"����첦\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $hooa){
$ou .="<IMG SRC=\"land38.gif\" ALT=\"ȯ�Ų�\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $gooa){
$ou .="<IMG SRC=\"land39.gif\" ALT=\"���߽����첦\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $sooa){
$ou .="<IMG SRC=\"land16.gif\" ALT=\"������\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $looa){
$ou .="<IMG SRC=\"land54.gif\" ALT=\"�쥸�㡼��\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $yooa){
$ou .="<IMG SRC=\"kane.gif\" ALT=\"������\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $eooa){
$ou .="<IMG SRC=\"sikin.gif\" ALT=\"��Ⲧ\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $aooa){
$ou .="<IMG SRC=\"menseki.gif\" ALT=\"���Ѳ�\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $iooa){
$ou .="<IMG SRC=\"hito.gif\" ALT=\"��Ͳ�\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $uooa){
$ou .="<IMG SRC=\"land15.gif\" ALT=\"�η���\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $fioa){
$ou .="<IMG SRC=\"land6.gif\" ALT=\"���Ӳ�\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'id'} == $tioa){
$ou .="<IMG SRC=\"senro.gif\" ALT=\"Ŵƻ��\" WIDTH=16 HEIGHT=16> ";
}
my($shuu) = 0;
my($shuo) = "";
$shuu =int(($island->{'sigoto'}  / $island->{'pop'}) * 1000);
if($shuu >= 100){
$shuo = "100��"
} else {
$shuo = "��$shuu��"
}
my($teou) = "";
if($island->{'teikou'} >0){
$teou ="��$island->{'teikou'}��";
}
my($poke) = 0;
my($poke2) = "";
if ($island->{'score'} >= 1){
$poke = $island->{'score'};
# $poke = "$poke"
$poke2 = "����${poke}ɤ";
} else {
$poke2 = "¸�ߤ���";
}
my($ei) = "";
if ($island->{'kouei'} >= 1){
$ei .= "<IMG SRC=\"eisei3.gif\" ALT=\"�������\" WIDTH=16 HEIGHT=16>";
}
if ($island->{'kanei'} >= 1){
$ei .= "<IMG SRC=\"eisei5.gif\" ALT=\"�ƻ����\" WIDTH=16 HEIGHT=16>";
}
if ($island->{'bouei'} >= 1){
$ei .= "<IMG SRC=\"eisei2.gif\" ALT=\"�ɸ����\" WIDTH=16 HEIGHT=16>";
}
if ($island->{'reiei'} >= 1){
$ei .= "<IMG SRC=\"eisei4.gif\" ALT=\"�졼��������\" WIDTH=16 HEIGHT=16>";
}
if ($island->{'pmsei'} >= 1){
$ei .= "<IMG SRC=\"eisei6.gif\" ALT=\"PMS����\" WIDTH=16 HEIGHT=16>";
}
if ($island->{'hatei'} >= 1){
$ei .= "<IMG SRC=\"eisei1.gif\" ALT=\"ȯ�ű���\" WIDTH=16 HEIGHT=16>";
}
my($senmei) = "";
if ($island->{'sen'} > 0){
$senmei = "<IMG SRC=\"sei.gif\" ALT=\"���谦��Ʊ��\" WIDTH=16 HEIGHT=16>";
}
my($heimei) = "";
if ($island->{'hei'} == 1){
$heimei = "<IMG SRC=\"hei.gif\" ALT=\"ʿ�°���Ʊ��\" WIDTH=16 HEIGHT=16>";
}
my($inomei) = "";
if ($island->{'ino'} == 1){
$inomei = "<IMG SRC=\"ino.gif\" ALT=\"ȿ���Τ�Ʊ��\" WIDTH=16 HEIGHT=16>";
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
$prize .= "<IMG SRC=\"koutei.gif\" ALT=\"$island->{'empe'}��\" WIDTH=16 HEIGHT=16> ";
}
if($island->{'top'} > 0){
$prize .= "<IMG SRC=\"top.gif\" ALT=\"$island->{'top'}��\" WIDTH=16 HEIGHT=16> ";
}
	# �������դ�ɽ��
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
	# ̾���˾ޤ�ʸ�����ɲ�
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

	# �ݤ������åꥹ��
	$f = 1;
	my($max) = -1;
	my($mNameList) = '';
my($monsnumber) = $island->{'monsnumber'};
my(@monsnumber) = split(/,/ ,$monsnumber);
	for($i = 0; $i < $HmonsterNumber; $i++) {
	    if($monsters & $f) {
		$mNameList .= "[$HmonsterName[$i],($monsnumber[$i]Ƭ)] ";
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
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'slag'}�ȥ�</NOBR></TD>
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
<H1>${HtagHeader_}���������õ��${H_tagHeader}</H1>
END
if($HislandNumber < $HmaxIsland) {
if($HdefaultPassword eq ''){
	out(<<END);
<FORM action="$HthisFile" method="POST">
�ɤ��̾����Ĥ���ͽ�ꡩ<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>��<BR>
�ѥ���ɤϡ�<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
ǰ�Τ���ѥ���ɤ�⤦���<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>

<INPUT TYPE="submit" VALUE="õ���˹Ԥ�" NAME="NewIslandButton">
</FORM>
END
}else{
out(<<END);
���Ǥ������Ͽ���Ƥ���Τ���Ͽ�Ǥ��ޤ���
��Ͽ���Ƥ��ʤ��Τˤ��줬ɽ�����줿���ϷǼ��Ĥˤ��񤭤���������
END
}
    } else {
	out(<<END);
        ��ο���������Ǥ�������������Ͽ�Ǥ��ޤ���
END
    }

    out(<<END);
<HR>
<H1>${HtagHeader_}���̾���ȥѥ���ɤ��ѹ�${H_tagHeader}</H1>
<P>
(���)̾�����ѹ��ˤ�$HcostChangeName${HunitMoney}������ޤ���
</P>
<FORM action="$HthisFile" method="POST">
�ɤ���Ǥ�����<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<BR>
�ɤ��̾�����Ѥ��ޤ�����(�ѹ�������Τ�)<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>��<BR>
�ѥ���ɤϡ�(ɬ��)<BR>
<INPUT TYPE="password" NAME="OLDPASS" SIZE=32 MAXLENGTH=32><BR>
�������ѥ���ɤϡ�(�ѹ�������Τ�)<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
ǰ�Τ���ѥ���ɤ�⤦���(�ѹ�������Τ�)<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>

<INPUT TYPE="submit" VALUE="�ѹ�����" NAME="ChangeInfoButton">
</FORM><HR>
<H1>${HtagHeader_}�����ʡ�̾���ѹ�${H_tagHeader}</H1>
<FORM action="$HthisFile" method="POST">
�ɤ���Ǥ�����<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<BR>
�����ʡ�̾
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=32 MAXLENGTH=32><BR>
�ѥ����
<INPUT TYPE="password" NAME="OLDPASS" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="�ѹ�����" NAME="ChangeOwnerButton">
</FORM><HR>
<H1>${HtagHeader_}������ѹ�${H_tagHeader}</H1>
<FORM action="$HthisFile" method="POST">
�ɤ���Ǥ�����<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<BR>
�����URL
<INPUT TYPE="text" NAME="FLAGNAME" VALUE="http://" SIZE=64 MAXLENGTH=64><BR>
�ѥ����
<INPUT TYPE="password" NAME="OLDPASS" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="�ѹ�����" NAME="ChangeFlagButton">
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
<H1>${HtagHeader_}�Ƕ�ν����${H_tagHeader}</H1>
END
    logPrintTop();
    out(<<END);
<H1>${HtagHeader_}ȯ���ε�Ͽ${H_tagHeader}</H1>
END
    historyPrint();
}

# �ȥåץڡ����ѥ�ɽ��
sub logPrintTop {
    my($i);
    for($i = 0; $i < $HtopLogTurn; $i++) {
	logFilePrint($i, 0, 0);
    }
}

# ��Ͽ�ե�����ɽ��
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
	out("<NOBR>${HtagNumber_}������${1}${H_tagNumber}��${2}</NOBR><BR>\n");
    }
    close(HIN);
}

1;
