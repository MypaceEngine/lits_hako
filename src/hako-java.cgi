#!/bin/perl

#----------------------------------------------------------------------
# Ȣ����� for Java
#
# ���ץ�å��̿�������ץ�($Revision: 1.7.2.5 $)
# ���Ѿ�������ˡ���ϰʲ��� WWW�ڡ����򻲾Ȥ��Ƥ���������
#
# Ȣ����� for Java ���ۥڡ���:
# SCENERY AND FISH - http://www16.cds.ne.jp/i/ohno/
#
# Ȣ����磲�Υ�����ץȤϰʲ��� WWW�ڡ��������ۤ���Ƥ��ޤ���
#
# Ȣ����磲�Υڡ���:
#   http://t.pos.to/hako/
#
# $Log: hako-java.cgi,v $
# Revision 1.7.2.5  2000/07/10 12:39:52  ohno
# a little bug fixed.
#
# Revision 1.7.2.4  2000/07/10 05:40:08  ohno
# change comment auth string.(from xxxIsland -> (xxxIsland))
#
#----------------------------------------------------------------------

$rcsid = '$Id: hako-java.cgi,v 1.7.2.5 2000/07/10 12:39:52 ohno Exp $';

#----------------------------------------------------------------------
# �Ƽ�������
#  ����Ū���ȼ���������ʬ�Ϥ��ޤꤢ��ޤ���
#  hako-main.cgi ��Ʊ������ˤ��Ƥ���������
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �ʲ���ɬ�����ꤹ����ʬ��
#----------------------------------------------------------------------

# ���Υե�������֤��ǥ��쥯�ȥ�
#  hako-java.cgi �� hako-main.cgi ��Ʊ���ǥ��쥯�ȥ���֤����Ȥ����ꤷ
#  �ƤĤ��äƤ��ޤ���
#  hako-main.cgi �� baseDir �������Ʊ���ˤ��Ƥ���������
#  �Ǹ�� / ���դ��ޤ���

# ���֤�����ˤ��碌��URL���ѹ����Ƥ���������
$cgiBase  = 'http://hoge.com/cgi-bin/hoge/';


# HakoApp.jar ���֤��ǥ��쥯�ȥ�
#  hako-main.cgi ��Ʊ�������С���Ǥʤ����ư���ޤ���
# �̾� hako-main.cgi $imageDir �������Ʊ���ˤ��ơ�
# .gif �ե������Ʊ������ HakoApp.jar �����֤��ޤ���

# ���֤�����ˤ��碌��URL���ѹ����Ƥ�������
$codeBase = 'http://hoge.com/hoge/hakogif';


# jcode.pl �ΰ���
#  hako-main.cgi ��Ʊ������ˤ��Ƥ�������

$jcode = './jcode.pl';


# �ǥ��쥯�ȥ�Υѡ��ߥå����
# �ǥ��쥯�ȥ꼰��å����ѻ��ΤȤ��Τ�

$dirMode = 0755;


# �ǡ����ǥ��쥯�ȥ��̾��
#  hako-main.cgi ��Ʊ������ˤ��Ƥ�������

$dirName  = 'storne';


# ��å�������
#  hako-main.cgi ��Ʊ������ˤ��Ƥ�������

$lockMode = 2;

#----------------------------------------------------------------------
# ɬ�����ꤹ����ʬ�ϰʾ�Ǥ���
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �ʲ��Ϲ��ߤ����ꤹ����ʬ�Ǥ�����
# hako-main.cgi �ǰʲ��ι��ܤ�Ĵ�����Ƥ����硢Ʊ������ˤ��Ƥ�������
#----------------------------------------------------------------------

# 1�����󤬲��ä�
# �����󹹿�Ƚ��˻ȤäƤ��ޤ���
# hako-main.cgi ��Ʊ���ͤˤ��Ƥ���������

$unitTime      = 21600;


# �۾ｪλ������(��å��岿�äǡ�����������뤫)
# ���� hako-java.cgi �ǤϻȤäƤ��ޤ���
# ���ʤ餺 hako-top.cgi ����ƤФ��Τ�ɬ�פ��ؤ�̵������Ǥ���

$unlockTime    = 120;


# ��ɽ�������å�
# ���줬 1 ���� �ᶷ��ɽ������ޤ���
# 0 �ʤ�ᶷɽ������ޤ��󡣳�ȯ���̤�ɽ�����٤��ȷ��äƿͤ�
# ����� 0 �ˤ��Ƥ���������

$logView = 1;


# ����ɽ���������
# ���ο��ͤ� hako-main.cgi ���⾮�����������ޤ���
# ���ͤ򾮤������뤳�Ȥǡ�Java��ȯ���̤�ɽ������ݤ���٤�ڸ��Ǥ��ޤ���

$logMax = 4;


# ���ޥ�����ϸ³���
# hako-main.cgi ��Ʊ���ͤˤ��Ƥ���������

$commandMax    = 50;


# ������Ǽ���(�Ѹ����̿�)�λ���
# 0 �ˤ���� ������Ǽ��Ǥ����ѽ���ʤ���ޤ���
# 1 �ʤ���Ѳ�ǽ�Ǥ���

$useLbbs = 1;


# ������Ǽ��Ǥ�ǧ�ڥ⡼��
# �����ͤ� 1 �����ꤹ��ȡ�������Ǽ��Ǥν񤭹��߻��˥ѥ���ɤ�
# ��ǧ�����褦�ˤʤꡢ�񤭹��ߤ�̾���θ��� '��xxxxx��' ���ղä���ޤ���

$lbbsAuth = 1;


# ������Ǽ��ǹԿ�
# hako-main.cgi ��Ʊ���ͤˤ��Ƥ���������

$lbbsMax = 10;


# ����礭��
# hako-main.cgi ��Ʊ���ͤˤ��Ƥ���������

$islandSize = 31;


# ¾�ͤ�����򸫤��ʤ����뤫
# hako-main.cgi ��Ʊ���ͤˤ��Ƥ���������

$hideMoneyMode = 2;


# �ѥ���ɤΰŹ沽
# hako-main.cgi ��Ʊ���ͤˤ��Ƥ���������

$cryptOn       =  1;


# �����դ���FORM�ǡ����κ���Ĺ
# 100�������塼���������ԤʤäƤ� 2048�Х��ȤϤ����ʤ��Τ�
# ����ʤ��Ǥ��礦���ɤ��Ȼפ��ޤ���

$maxContentLength = 2048;


# ������BBS�Ǽ����դ���̾���κ���Ĺ

$maxName       = 32;


# ������BBS�Ǽ����դ����å������κ���Ĺ

$maxMessage    = 80;


# �����ȤǼ����դ����å������κ���Ĺ

$maxComment    = 80;


# redirect ����
# Java��ȯ���̤�ɽ�����褦�Ȥ����Ȥ��ˡ������󹹿����֤��᤮�Ƥ����顢
# �����󹹿�������褦�ˤ��ޤ����̾� 1 ���ɤ��Ȼפ��ޤ���

$redirectNewTurn = 1;


# ��Ĥ���ιԿ�
# hakojima.dat �ե�����ΰ�Ĥ���ξ���ιԿ��Ǥ���
# ��¤���Ǿ�������䤷�Ƥ�����Ϥ����Ĵ�����Ƥ���������

$islandLines = 13;

# �ޥå�ʸ����η��
# �ޥå�ʸ����η�����ѹ����Ƥ�����˻��Ѥ��Ƥ���������
$landDigits = 2;
$landValueDigits = 2;


#----------------------------------------
# �����ط�
#----------------------------------------

# <BODY> �����Υ��ץ����

$htmlBody      = 'BGCOLOR="#EEFFFF"';


# ������Υ����ȥ�ʸ��

$title         = 'Ȣ����� for Java';


# �礭��ʸ��

$tagBig_ = '<FONT SIZE=6>';
$_tagBig = '</FONT>';


# ���̾���ʤ�

$tagName_ = '<FONT COLOR="#a06040"><B>';
$_tagName = '</B></FONT>';


# ��̤��ֹ�ʤ�

$tagNumber_ = '<FONT COLOR="#800000"><B>';
$_tagNumber = '</B></FONT>';

# ���������

$islandSuffix = '��';

# ���ץ�åȤ���

$appletWidth  = '760';


# ���ץ�åȤι⤵

$appletHeight = '770';


#----------------------------------------------------------------------
# hako-main.cgi ��Ʊ������ˤ���ΤϤ����ޤǤǤ���
#----------------------------------------------------------------------


#----------------------------------------------------------------------
# �Ƽ����
#  ����ʸ�ν񤭴����� Java���ץ�åȤرƶ����Фޤ���
#  �ޤ�Ʊ��������ͤ� hako-main.cgi �ˤ⤢���Τ�
#  Ʊ������ˤ��Ƥ���������
#----------------------------------------------------------------------

# �ե�����̾
#  .jar .cgi�ե������̾��

$archive = "HakoApp.zip";
$cgiJava = "hako-java.cgi";
$cgiMain = "hako-main.cgi";


# ���ץ�åȴط�

$appletName = "HakoApplet";
$appletClass= "y_ohno.game.hakoniwa.HakoApplet.class";


# Applet �Ȥ��̿����Υ��ơ������ֹ�

$CANNOT_LOCK="001";
$MISSING_ID ="002";
$WRONG_PASS ="003";
$FATAL_ERROR="004";
$DISABLED   ="005";


# �Ϸ��ֹ�

$landSea      =  0;
$landWaste    =  1;
$landPlains   =  2;
$landTown     =  3;
$landForest   =  4;
$landFarm     =  5;
$landFactory  =  6;
$landBase     =  7;
$landDefence  =  8;
$landMountain =  9;
$landMonster  = 10;
$landSbase    = 11;
$landOil      = 12;
$landMonument = 13;
$landDummy    = 14;
$landdoubutu  = 15;
$landkiken   = 16;
$landkishou   = 17;
$landKoku   = 37;
$landJira   = 41;
# �����ե������̾��

$dataName     = 'hakojima.dat';


# �����ե�����񤭹��߻��Υƥ�ݥ��ե�����

$dataTemp     = 'hakojima.tmp';


# island�ե�����񤭹��߻��Υƥ�ݥ��ե�����

$tempName     = 'island.tmp';


#----------------------------------------------------------------------
# main()
#----------------------------------------------------------------------

# ��å��Ѥߥե饰�ν����

$locked = 0;


# jcode.pl �Υ���

require($jcode);


# FORM �ν���

if (! treatPostedData())
{
    exit 1;
}


# ���������ˤ�ä�ʬ��

my ($action) = $FORM{'action'};

if ($action eq 'login')
{
    login();
}
elsif ($action eq 'comment')
{
    comment();
}
else
{
    printHeader();

    if ($action eq 'version')
    {
	print $rcsid;
    }
    elsif ($action eq 'inspect')
    {
	inspect();
    }
    elsif ($action eq 'sightseeing')
    {
	sightseeing();
    }
    elsif ($action eq 'plan')
    {
	plan();
    }
    elsif ($action eq 'communication')
    {
	communication();
    }
}

hakounlock();
exit;


#----------------------------------------------------------------------
# ������
#----------------------------------------------------------------------
# ���ե�����˥���񤭹��ߤޤ�

#sub logprint
#{
#    open LOGWRITE, ">>${dirName}/log";
#    print LOGWRITE @_;
#    close(LOGWRITE);
#}

#----------------------------------------------------------------------
# ���������
#----------------------------------------------------------------------
# memo:
#  ���ץ�åȤ�ɽ������HTML�ɥ�����Ȥ��֤��ޤ���

sub login
{
    my ($id, $password, $reload, $javacgi);

    $id = $FORM{'island'};
    $password = $FORM{'password'};
    $reload = $cgiBase . "/" . $cgiMain;
    $javacgi= $cgiBase . "/" . $cgiJava;

    # ɬ�פʤ���ξ�����ɤ߹���
    if ($logView || $redirectNewTurn)
    {
	if (! hakolock())
	{
	    printHtmlHeader();
	    printError('��å��μ����˼��Ԥ��ޤ���');
	    printHtmlFooter();
	    return 0;
	}

	if (! readIslandsFile($id, 0))
	{
	    printHtmlHeader();
	    printError('�ǡ����ե�������ɤ߹��ߤ˼��Ԥ��ޤ���');
	    printHtmlFooter();
	    return 0;
	}
    }

    # Turn ���������å�
    if ($redirectNewTurn)
    {
	if ($nextTurn == 0)
	{
	    # window mode �ʤ� JavaScript ��
	    if ($FORM{'windowmode'} eq 'window')
	    {
		print "Content-type: text/html\n\n";
		print "<HTML><HEAD><TITLE>${title}</TITLE></HEAD>\n";
		print "<BODY><SCRIPT language=\"JavaScript\">\n";
		print "<!--\n";
		print "window.opener.document.location = \"${reload}\";\n";
		print "window.close();\n";
		print "//-->\n";
		print "</SCRIPT>\n";
		print "</BODY></HTML>\n";
		return 1;
	    }
	    else
	    {
		print "Location: ${reload}\n\n";
		return 1;
	    }
	}
    }

    printHtmlHeader();
    printSJIS("<CENTER>");

    # window mode �Ǥʤ���� �ȥåפ���� ��ɽ��
    if ($FORM{'windowmode'} ne 'window')
    {
	printSJIS("<A HREF=\"${reload}\">${tagBig_}�ȥåפ����${_tagBig}</A><HR>\n");
    }

    # log ɽ�����ϥѥ���ɥ����å�
    if ($logView)
    {
	if ($islandPassword ne encrypt($password))
	{
	    hakounlock();
	    printError('�ѥ���ɤ����פ��ޤ���');
	    printHtmlFooter();
	    return 0;
	}
    }
    # ���ץ�åȤ� TAG�����
    if ($FORM{'tag'} eq 'PLUGIN')
    {
	# PLUGIN��Ȥ�
	print "<OBJECT CLASSID=\"clsid:8AD9C840-044E-11D1-B3E9-00805F499D93\"\n";
	print "WIDTH=\"${appletWidth}\"\n";
	print "HEIGHT=\"${appletHeight}\"\n";
	print "NAME=\"${appletName}\"\n";
	print "ALT=\"${appletName}\"\n";
	print "CODEBASE=\"http://java.sun.com/products/plugin/1.2/jinstall-12-win32.cab#Version=1,2,0,0\">\n";

	print "<PARAM NAME=\"CODE\"     VALUE=\"${appletClass}\">\n";
	print "<PARAM NAME=\"CODEBASE\" VALUE=\"${codeBase}\">\n";
	print "<PARAM NAME=\"ARCHIVE\"  VALUE=\"${archive}\">\n";
	print "<PARAM NAME=\"NAME\"     VALUE=\"${appletName}>\"\n";
	print "<PARAM NAME=\"TYPE\"     VALUE=\"application/x-java-applet;version=1.2\">\n";

	# Applet Parameter
	print "<PARAM NAME=\"CommandMax\" VALUE=\"${commandMax}\">\n";
	print "<PARAM NAME=\"ID\"         VALUE=\"${id}\">\n";
	print "<PARAM NAME=\"Password\"   VALUE=\"${password}\">\n";
	print "<PARAM NAME=\"CGIURL\"     VALUE=\"${javacgi}\">\n";
	print "<PARAM NAME=\"LDIGITS\"    VALUE=\"${landDigits}\">\n";
	print "<PARAM NAME=\"VDIGITS\"    VALUE=\"${landValueDigits}\">\n";

	print "<COMMENT>\n";
	print "<EMBED type=\"application/x-java-applet;version=1.2\"\n";
	print "java_CODE=\"${appletClass}\"\n";
	print "java_CODEBASE=\"${codeBase}\"\n";
	print "java_ARCHIVE=\"${archive}\"\n";
	print "ALT=\"${appletName}\"\n";
	print "NAME=\"${appletName}\"\n";
	print "WIDTH=\"${appletWidth}\"\n";
	print "HEIGHT=\"${appletHeight}\"\n";

	# Applet Parameter
	print "CommandMax=\"${commandMax}\"\n";
	print "ID=\"${id}\"\n";
	print "Password=\"${password}\"\n";
	print "CGIURL=\"${cgiBase}/${cgiJava}\"\n";
	print "LDIGITS=\"${landDigits}\"\n";
	print "VDIGITS=\"${landValueDigits}\"\n";

	print "pluginspage=\"http://java.sun.com/products/plugin/1.2/plugin-install.html\">\n";
	printSJIS("<NOEMBED></COMMENT>�ץ饰����ϻȤ��ʤ��ߤ����Ǥ�</NOEMBED></EMBED></OBJECT>\n");
    }
    else
    {
	# ���ץ�åȥ�����Ȥ�
	print "<APPLET\n";
	print "CODEBASE=\"${codeBase}\"\n";
	print "ARCHIVE=\"${archive}\"\n";
	print "CODE=\"${appletClass}\"\n";
	print "ALT=\"${appletName}\"\n";
	print "NAME=\"${appletName}\"\n";
	print "WIDTH=\"${appletWidth}\"";
	print "HEIGHT=\"${appletHeight}\">\n";

	# Applet Parameter
	print "<PARAM NAME=\"CommandMax\" VALUE=\"${commandMax}\">\n";
	print "<PARAM NAME=\"ID\"         VALUE=\"${id}\">\n";
	print "<PARAM NAME=\"Password\"   VALUE=\"${password}\">\n";
	print "<PARAM NAME=\"CGIURL\"     VALUE=\"${javacgi}\">\n";
	print "<PARAM NAME=\"LDIGITS\"    VALUE=\"${landDigits}\">\n";
	print "<PARAM NAME=\"VDIGITS\"    VALUE=\"${landValueDigits}\">\n";

	print "</APPLET>\n";
    }
    printSJIS("<BR><FONT SIZE=-2><A HREF=\"mailto:y_ohno\@geocities.co.jp\">HakoApplet - Written by Yasuo OHNO</A></FONT>\n");

    print "<HR>";
    # �������ѹ� FORM�ν���
    print "<SCRIPT language=JavaScript>\n<!--\nfunction commentPost()\n";
    print "{\n  postWindow = window.open(\"\", \"postWindow\", \"menubar=no,toolbar=no,location=no,directories=no,status=no,scrollbars=yes,resizable=yes,width=640,height=80\");\n}\n//-->\n</SCRIPT>\n";
 print "<IMG SRC=\"jyu.cgi?page=${id}&name=${id}\" WIDTH=\"2\" HEIGHT=\"2\">\n";
    printSJIS("${tagBig_}�����Ȥ��ѹ�${_tagBig}<BR>\n");
    printSJIS("<FONT SIZE=-1>�����ϰ��٤��������Ƥ���������</FONT><BR>");
    printSJIS("<FORM NAME=\"commentForm\" METHOD=POST ACTION=\"$javacgi\" TARGET=\"postWindow\">\n");
    printSJIS("<INPUT TYPE=hidden NAME=\"action\" VALUE=\"comment\">\n");
    printSJIS("<INPUT TYPE=hidden NAME=\"island\" VALUE=\"${id}\">\n");
    printSJIS("<INPUT TYPE=hidden NAME=\"password\" VALUE=\"${password}\">\n");
    printSJIS("<INPUT TYPE=text NAME=\"comment\" VALUE=\"${islandComment}\" SIZE=80 MAXLENGTH=${maxComment}>\n");
    printSJIS("<INPUT TYPE=submit VALUE=\"����\" onClick=\"commentPost()\">\n");
    printSJIS("</FORM></CENTER>\n");

    if ($logView)
    {
	print "<HR>";
	printSJIS("${tagBig_}${tagName_}${islandName[$islandIndex]}${islandSuffix}${_tagName}�ζᶷ${_tagBig}<BR>\n");
	printAllLog($id);
    }

    printHtmlFooter();

    return 1;
}


#----------------------------------------------------------------------
# �����ȹ���
#----------------------------------------------------------------------
# memo:
#  �����Ȥ򹹿����ޤ���
#  $FORM{'action'}   = 'comment'
#  $FORM{'comment'}  = '������'
#  $FORM{'island'}   = ���ID
#  $FORM{'password'} = ��Υѥ����

sub comment
{
    my ($id, $password, $comment);

    # FORM ������Ф�
    $id = $FORM{'island'};
    $password = $FORM{'password'};
    $comment = $FORM{'comment'};

    printHtmlHeader();

    # �ե�����Υ�å�
    if (! hakolock())
    {
	printError('��å��˼��Ԥ��ޤ���');
    }
    else
    {
	# �����Ȥν񤭴���
	writeComment($id, $password, $comment);
	hakounlock();
    }

    printSJIS("<BR><CENTER><A HREF=\"javascript:void(0)\" onClick=\"window.close();\">�Ĥ���</A></CENTER>");
    printHtmlFooter();
}


#----------------------------------------------------------------------
# �������塼���������
#----------------------------------------------------------------------
# memo:
#  �������塼�������򤷤ޤ���

sub plan
{
    my ($id, $password, @plans);
    my ($i, $line, $length, $readfile, $tempfile);

    # FORM�ǡ������ɤ߹���
    $id = $FORM{'island'};
    $password = encrypt($FORM{'password'});
    @plans = split(/\\/,$FORM{'plan'});

    $length = @plans;
    $readfile = "${dirName}/island.${id}";
    $tempfile = "${dirName}/${tempName}";

    # ��å��μ���
    if (! hakolock())
    {
	nack($CANNOT_LOCK);
    }

    # ��ǡ��������������ɤ߹���
    if (! readIslandsFile($id, 0))
    {
	nack($FATAL_ERROR);
    }

    # �ѥ���ɤ��ǧ
    if ($islandPassword ne $password)
    {
	nack($WRONG_PASS);
    }

    # �������塼��Ĺ���ǧ
    if ($length != $commandMax)
    {
	nack($FATAL_ERROR);
    }

    # �ե�����Υ����ץ�
    if (! open(READ, "$readfile"))
    {
	nack($FATAL_ERROR);
    }

    if (! open(WRITE, ">$tempfile"))
    {
	nack($FATAL_ERROR);
    }

    # ���Ͽޥǡ����ν񤭤���
    for ($i = 0; $i < $islandSize; $i++)
    {
	$line = <READ>;
	print WRITE $line;
    }

    # �������塼����ɤ����Ф��Ƚ񤭹���
    for ($i = 0; $i < $commandMax; $i++)
    {
	$line = <READ>;
	print WRITE $plans[$i] . "\n";
    }

    # �����Ȥν񤭤���
    print WRITE <READ>;

    # �ե�����Υ�����
    close(WRITE);
    close(READ);

    # rename����
    if (! rename("$tempfile", "$readfile"))
    {
	nack($FATAL_ERROR);
    }

    # unlock����
    hakounlock();

    # ��λ����
    ack();
    print "${nextTurn}\n";
}


#----------------------------------------------------------------------
# �̿������
#----------------------------------------------------------------------

sub communication
{
    my ($id, $password, $name, $comment, $auth);
    my ($owner, $readfile, $tempfile, @lbbs);

    # ���Ѷػ߳�ǧ
    if ($useLbbs == 0)
    {
	nack($DISABLED);
    }

    # FORM�ǡ������ɤ߹���
    $id = $FORM{'island'};
    $password = $FORM{'password'};
    $name     = $FORM{'name'};
    $comment  = $FORM{'comment'};
    $ownerid  = $FORM{'ownerid'};
    $auth = "";

    $readfile = "${dirName}/island.${id}";
    $tempfile = "${dirName}/${tempName}";

    # �ǡ����ե�����Υ�å�
    if (! hakolock())
    {
	nack($CANNOT_LOCK);
    }

    # �񤭹��ॳ���Ȥ�¸�ߤ��뤫��
    if ($comment ne "")
    {
	# �Ȥꤢ�����������Ȥ���
	$owner = 0;

	# �ѥ���ɤ����ꤵ��Ƥ����� encrypt����
	if ($password ne "")
	{
	    $password = encrypt($password);
	}

	# $name �� $comment �� ������
	$name = cutColumn(jcode::euc($name, 'sjis'), $maxName);
	$comment = cutColumn(jcode::euc($comment, 'sjis'), $maxMessage);

	if ($lbbsAuth)
	{
	    # ǧ�ڥ⡼��
	    if ($ownerid eq '')
	    {
		nack($FATAL_ERROR);
	    }

	    # ���å⡼�ɤ��ɤ߹���
	    if (! readIslandsFile($ownerid, 0))
	    {
		nack($FATAL_ERROR);
	    }

	    # �ѥ���ɤ��԰��פʤ饨�顼
	    if ($islandPassword ne $password)
	    {
		nack($WRONG_PASS);
	    }

	    # ownerid == id �ʤ� ownermode
	    if ($ownerid == $id)
	    {
		$owner = 1;
	    }

	    # ̾���βù�
	    $auth = '(' . $islandName[$islandIndex] . $islandSuffix . ')';
	}
	else
	{
	    # ƿ̾�⡼��
	    # ���å⡼�ɤ��ɤ߹���
	    if (! readIslandsFile($id, 0))
	    {
		nack($FATAL_ERROR);
	    }

	    # �ѥ���ɤ����פ��ơ����� $id == $ownerid �ʤ� owner�⡼��
	    if (($islandPassword eq $password) &&
		($id == $ownerid))
	    {
		$owner = 1;
	    }
	}

	# name �� comment �� HTML��
	$name = encodeHTML($name);
	$comment = encodeHTML($comment);

	# �ե�����Υ����ץ�
	if (! open(READ, "$readfile"))
	{
	    nack($FATAL_ERROR);
	}

	if (! open(WRITE, ">$tempfile"))
	{
	    nack($FATAL_ERROR);
	}

	# ���Ͽޥǡ����ν񤭤���
	for ($i = 0; $i < $islandSize; $i++)
	{
	    $line = <READ>;
	    print WRITE $line;
	}

	# �������塼����ɤ����Ф��Ƚ񤭹���
	for ($i = 0; $i < $commandMax; $i++)
	{
	    $line = <READ>;
	    print WRITE $line;
	}

	# ���������Ȥν񤭹���
	$lbbs[0] = "${owner}>${islandTurn}${auth}��${name}>${comment}\n";
	print WRITE $lbbs[0];

	# �Ĥ�Υ����Ȥν񤭤���
	for ($i = 1; $i < $lbbsMax; $i++)
	{
	    $lbbs[$i] = <READ>;
	    print WRITE $lbbs[$i];
	}

	# �ե�����Υ�����
	close(WRITE);
	close(READ);

	# rename����
	if (! rename("$tempfile", "$readfile"))
	{
	    nack($FATAL_ERROR);
	}
    }
    else
    {
	# island�ե�������ɤ߹���
	if (! open(READ, "$readfile"))
	{
	    nack($FATAL_ERROR);
	}

	# �����Ȱʳ����ɤ����Ф�
	for ($i = 0; $i < ($islandSize + $commandMax); $i++)
	{
	    $dummy = <READ>;
	}

	# �����Ȥ��ɤ߹��ߤȽ񤭤���
	for ($i = 0; $i < $lbbsMax; $i++)
	{
	    $lbbs[$i] = <READ>;
	}

	# �ե�������Ĥ���
	close(READ);
    }

    hakounlock();

    # ack���ֿ�
    ack();

    # LocalBBS�κ���Կ�
    print "${lbbsMax}\n";

    # ��̤ν���
    for ($i = 0; $i < $lbbsMax; $i++)
    {
$lbbs[$i] =~ /([0-9]*)\>(.*)\>(.*)$/;
if ($1 == '5') {
$gokuhi = "5> >������ ���� ������\n";
print jcode::sjis(${gokuhi}, 'euc');
}else{
print jcode::sjis($lbbs[$i], 'euc');
}
}
}

#----------------------------------------------------------------------
# ����Υǡ����ܼ���Υޥåץǡ����μ���
#----------------------------------------------------------------------

sub inspect
{
    my ($id, $password);

    $id = $FORM{'island'};
    $password = encrypt($FORM{'password'});

    # �ǡ����ե�����Υ�å�
    if (! hakolock())
    {
	nack($CANNOT_LOCK);
    }

    # ��ǡ��������������ɤ߹���
    if (! readIslandsFile($id, 0))
    {
	nack($FATAL_ERROR);
    }

    if (! readMapFile($id, 0))
    {
	nack($FATAL_ERROR);
    }

    hakounlock();

    # �ѥ���ɤ��ǧ
    if ($islandPassword ne $password)
    {
	nack($WRONG_PASS);
    }

    ack();

    print "${nextTurn}\n";

    # ��ξ��������
    print "${islandNumber}\n";

    my ($i, $lines);
    for ($i = 0; $i < $islandNumber; $i++)
    {
	print jcode::sjis("${islandName[$i]}\n${islandID[$i]}\n", 'euc');
    }

    $lines = 11 + $islandSize;

    print "${lines}\n";

    print "${islandTurn}\n";
    print "${islandRank}\n";
    print "${islandMoney}\n";
    print "${islandFood}\n";
    print "${islandPop}\n";
    print "${islandArea}\n";
    print "${islandFarm}\n";
    print "${islandFactory}\n";
    print "${islandMountain}\n";
    print "${islandSize}\n";
    print "${islandSize}\n";

    # ����Ϸ�������
    for ($i = 0; $i < $islandSize; $i++)
    {
	print $islandMap[$i] . "\n";
    }

    # ��Υ������塼�������
    print "${commandMax}\n";

    for ($i = 0; $i < $commandMax; $i++)
    {
	print $islandPlan[$i] . "\n";
    }
}


#----------------------------------------------------------------------
# ��Υޥåפμ���
#----------------------------------------------------------------------

sub sightseeing
{
    my ($id);

    $id = $FORM{'island'};

    if (! hakolock())
    {
	nack($CANNOT_LOCK);
    }

    # �������ɤ߹��� ���å⡼��
    if (! readIslandsFile($id, 1))
    {
	nack($FATAL_ERROR);
    }

    # �Ͽޥǡ������ɹ� ���å⡼��
    if (! readMapFile($id, 1))
    {
	nack($FATAL_ERROR);
    }

    hakounlock();

    ack();

    print "${nextTurn}\n";

    my ($i, $lines);

    # ��ξ��������

    $lines = 11 + $islandSize;	# �Կ��η׻�

    print "${lines}\n";		# �Կ�

    print "${islandTurn}\n";	# 1
    print "${islandRank}\n";	# 2
    print "${islandMoney}\n";	# 3
    print "${islandFood}\n";	# 4
    print "${islandPop}\n";	# 5
    print "${islandArea}\n";	# 6
    print "${islandFarm}\n";	# 7
    print "${islandFactory}\n";	# 8
    print "${islandMountain}\n";# 9
    print "${islandSize}\n";	# 10
    print "${islandSize}\n";	# 11

    # ����Ϸ�������
    for ($i = 0; $i < $islandSize; $i++)
    {
	print $islandMap[$i] . "\n";
    }
}

#----------------------------------------------------------------------
# ���֥롼����
#----------------------------------------------------------------------

#----------------------------------------
# SJIS�ˤ�����
#----------------------------------------
# argument:
#  $string - ɸ����Ϥ˽��Ϥ�����EUCʸ����
# memo:
#  EUCʸ����� SJIS�Ѵ����ƽ��Ϥ��ޤ���

sub printSJIS
{
    print jcode::sjis($_[0], 'euc');
}


#----------------------------------------
# HTML ʸ�Ϥ��Ѵ�����
#----------------------------------------
# argument:
#  $string - HTML��ɽ����ǽ�ʾ��֤��Ѵ�����ʸ��
# memo:
#  HTML�Ȥ���ɽ����ǽ��ʸ�Ϥ��Ѵ�����
#  &   = &amp;
#  "   = &quot;
#  <   = &lt;
#  >   = &gt;
#
#  [\x00-\x1F] �Ϻ��
#  SJIS�Ǥ�����פʤϤ��Ǥ��������������ɤ� EUC����Ѥ���褦�ˤ��Ƥ���������

sub encodeHTML
{
    my ($string) = @_;

    $string =~ s/&/&amp;/g;
    $string =~ s/"/&quot;/g;
    $string =~ s/</&lt;/g;
    $string =~ s/>/&gt;/g;

    $string =~ s/[\x00-\x1F\x7F\xFF]//g;

    return $string;
}


#----------------------------------------
# ����η����ʸ������ڤ�
#----------------------------------------
# argument:
#  $string    - �ڤ�Ȥ�ʸ����
#  $maxlength - ����Ĺ(�Х��ȿ�)
# return:
#  �ڤ�Ȥä�ʸ����
# memo:
#  ���������ɤξ�̲���Ƚ��򤷤Ƥ��뤿�� EUC�Ǥʤ���Фʤ�ޤ���

sub cutColumn
{
    my ($string, $maxlength) = @_;

    if (length($string) <= $maxlength)
    {
	return $string;
    }

    # $maxlength �Х����ܤ� 2byte code �� 2byte �ܤʤ�
    # $maxlength - 1 �ޤǤ�ͭ���ϰϡ�����ʳ��� $maxlength �ޤǡ�
    if (isEUCSecondByte($string, $maxlength))
    {
	$maxlength--;
    }

    return substr($string, 0, $maxlength);
}


#----------------------------------------
# ���ꤵ�줿ʸ����EUC������2byte�ܤ�Ƚ��
#----------------------------------------
# argument:
#  $string - Ƚ�ꤹ��ʸ����
#  $offset - Ƚ�ꤹ��ʸ���ΰ���
# return:
#  0 - $offset �ܤ�ʸ���� EUC���������ɤΣ��Х����ܤ�Ⱦ��ʸ��
#  1 - $offset �ܤ�ʸ���� EUC���������ɤΣ��Х�����

sub isEUCSecondByte
{
    my ($string, $offset) = @_;
    my ($c, $result);

    $result = 0;

    # ���ʤ󤫸�Ψ����
    $c = ord(substr($string, $offset, 1));

    if (($c < 0xA1) || ($c > 0xFE))
    {
	return 0;
    }
    $offset--;

    SEARCH: while ($offset >= 0)
    {
	$c = ord(substr($string, $offset, 1));
	last SEARCH if (($c < 0xA1) || ($c > 0xFE));

	$offset--;
	$result = $result ^ 1;
    }

    return $result;
}


#----------------------------------------
# �ݥ��Ȥ��줿�ǡ����ν���
#----------------------------------------
# global reference:
#  $maxContentLength - �����������Υե�����ǡ���
#
# return:
#  FORM - name��key�ˤ���Ϣ������

sub treatPostedData
{
    my ($buffer, @pairs, $name, $value, $length);

    $length = $ENV{'CONTENT_LENGTH'};

    # �۾��Ĺ���ǡ������褿�饨�顼��λ������
    # �̾�ɤ�ʤ˹ͤ��Ƥ� 2K ��ۤ��뤳�Ȥ�̵���Ϥ�
    if ($length > $maxContentLength)
    {
	return 0;
    }

    read(STDIN, $buffer, $length);

    @pairs = split(/&/,$buffer);
    foreach $pair (@pairs)
    {
	($name,$value) = split(/=/,$pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;

	$FORM{$name} = $value;
    }

    return 1;
}


#----------------------------------------
# �إå������֤�
#----------------------------------------
# memo:
#  Java �Ȥ� �̿��ϴ���Ū�� text/plain �ǹԤ��ޤ���

sub printHeader
{
    print "Content-type: text/plain\n\n";
}


#----------------------------------------
# ACK���֤�
#----------------------------------------
# memo:
#  Java ���ץ�åȤ��Ф����׵᤬�������줿���Ȥ�����

sub ack
{
    print "ACK\n";
}


#----------------------------------------
# NACK�ȥ��顼�ֹ���֤�
#----------------------------------------
# memo:
#  Java���ץ�åȤ��Ф����׵᤬��������ʤ��ä����Ȥ�����

sub nack
{
    hakounlock();
    print "NACK $_[0]\n";
    exit 0;
}


#----------------------------------------
# HTML Header �ν���
#----------------------------------------
# memo:
#  HTML Header ����Ϥ��ޤ�

sub printHtmlHeader
{
if($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/ and $ENV{HTTP_USER_AGENT}=~/Windows/){
print qq{Content-type: text/html; charset=Shift_JIS\n};
print qq{Content-encoding: gzip\n\n};

# gzip�ؤΥѥ��ν�����ɬ�פǤ���
open(STDOUT,"| /bin/gzip -1 -c");
print " " x 2048 if($ENV{HTTP_USER_AGENT}=~/MSIE/);
print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
}else{
print qq{Content-type: text/html; charset=Shift_JIS\n\n};
print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
}

    printSJIS("<HTML><HEAD><TITLE>${title}</TITLE></HEAD>\n");
    printSJIS("<BODY ${htmlBody}>");

    # ---v--- ����ػߤǤ����ä��ʤ��Ǥ�m(_ _)m ---v---
    printSJIS("<A HREF=\"http://t.pos.to/hako/\">Ȣ����祹����ץ����۸�</A>��\n");
    # ---^--- ����ػߤǤ����ä��ʤ��Ǥ�m(_ _)m ---^---

    printSJIS("<A HREF=\"http://www16.cds.ne.jp/~ohno/\">Ȣ����� for Java ���۸�</A><HR>\n");
}


#----------------------------------------
# HTML Footer �ν���
#----------------------------------------
# memo:
#  HTML Footer ����Ϥ��ޤ�

sub printHtmlFooter
{
    # �Ǽ������ؤΥ�󥯤Ϥ������ɲ�
    printSJIS("<HR></BODY></HTML>\n");
}


#----------------------------------------
# HTML�ǤΥ��顼����
#----------------------------------------
# memo:
#  ���顼ʸ�Ϥ�ɽ�����ޤ���
    
sub printError
{
    my($message) = @_;

    printSJIS("${tagBig_}${message}${_tagBig}");
}


#----------------------------------------
# �����Ȥν񤭹���
#----------------------------------------
# argument:
#  $id       - �����Ȥ�񤭹������ ID
#  $password - �����Ȥ�񤭹������ �ѥ����
#  $comment  - ������
# memo:
#  $comment == "" �ʤ� (̤��Ͽ) �Ȥ��ޤ���

sub writeComment
{
    my ($id, $password, $comment) = @_;
    my ($i, $l, $n, $found, $readline, $readid, $readfile, $tempfile);

    # $comment �� ������
    $comment = cutColumn(jcode::euc($comment), $maxComment);
    $comment = encodeHTML($comment);

    if ($comment eq "")
    {
	$comment = "(̤��Ͽ)";
    }

    $readfile = "${dirName}/${dataName}";
    $tempfile = "${dirName}/${dataTemp}";
    $found = 0;

    # �ɤ߹���¦�����ץ�
    if (! open(READ, "$readfile"))
    {
	printError('�ǡ����ե�����򳫤��ޤ���');
	return 0;
    }

    # �񤭹���¦�����ץ�
    if (! open(WRITE, ">$tempfile"))
    {
	close(READ);
	printError('�ƥ�ݥ��ե�����򳫤��ޤ���');
	return 0;
    }

    # ���������ʤɤ��ɤ߹���
    $readline = <READ>;		# �������
    print WRITE $readline;
    $readline = <READ>;		# �ǽ���������
    print WRITE $readline;
    $readline = <READ>;		# ������
    print WRITE $readline;
    $n = int($readline);
     $readline = <READ>;		# ���˳�����Ƥ�ID
    print WRITE $readline;

   # �񤭴�������θ���
    SEARCH: for ($i = 0; $i < $n; $i++)
    {
	$l = $islandLines;

	$readline = <READ>; $l--; # ���̾��
	print WRITE $readline;
	$readline = <READ>; $l--; # ���ID
	print WRITE $readline;
	$readid = int($readline);

	# õ���Ƥ��� ID ����
	if ($id == $readid)
	{
	    $readline = <READ>; $l--; # ���ޥǡ���
	    print WRITE $readline;
	    $readline = <READ>; $l--; # Ϣ³��ⷫ��
	    print WRITE $readline;

	    $readline = <READ>; $l--; # �쥳����
	    $readline = <READ>; $l--; # �ѥ����
	    chomp($readline);

	    # �ѥ���ɳ�ǧ
	    if ($readline ne encrypt($password))
	    {
		close(READ);
		close(WRITE);
		printError('�ѥ���ɤ��㤤�ޤ�');
		return 0;
	    }

	    # �����Ȥȥѥ���ɤν���
	    print WRITE "${comment}\n";
	    print WRITE "${readline}\n";

	    $found = 1;
	    last SEARCH;
	}

	# �Ĥ�Υǡ�����񤭽Ф�

	while ($l > 0)
	{
	    $readline = <READ>; $l--;
	    print WRITE $readline;
	}
    }

    # �����Ȥ��񤭴������Ƥ�����
    if ($found)
    {
	# �ե�����λĤ�����ƥ��ԡ�����
	while (<READ>)
	{
	    print WRITE $_;
	}
    }

    # �ե�����Υ�����
    close(WRITE);
    close(READ);

    if ($found)
    {
	# �ե�������֤�����
	if (! rename("$tempfile", "$readfile"))
	{
	    printError('�ǡ������֤������˼��Ԥ��ޤ���');
	    return 0;
	}
    }
    else
    {
	# �����ID�����Ĥ���ʤ��ä�
	printError('�񤭴����˼��Ԥ��ޤ���');
	return 0;
    }

    printSJIS("<CENTER>${tagBig_}�����Ȥ�񤭴����ޤ���${_tagBig}</CENTER>");

    return 1;
}


#----------------------------------------
# �������ɤ߹���
#----------------------------------------
# argument:
#   $id      - ���ID�ֹ�
#   $conceal - ����α���ư��
# return:
#   0 - ����
#   1 - �����Х��ѿ��˰ʲ��Υǡ��������ꤵ��롣
#   $islandTurn        = ���Υǡ����Υ�����
#   $islandNumber      = ��ο�
#   $islandNextID      = ��������˳�����Ƥ�ID
#   $islandLastTime    = �Ǹ�˹������줿����
#   $nextTurn          = ���Υ�����ޤǤλ���
#   $islandName[index] = ���̾��
#   $islandID[index]   = ���ID
#
#   �ʲ� $id �� ��ξ���
#
#   $islandIndex       = ���Index
#   $islandPassword    = �Ź沽�Ѥߥѥ����
#   $islandComment     = ������
#   $islandMoney       = ���($conceal != 0 �ΤȤ� $hideMoneyMode�ˤ�걣��)
#   $islandFood        = ����
#   $islandPop         = �͸�
#   $islandArea        = ����
#   $islandFarm        = ���쵬��
#   $islandFactory     = ���쵬��
#   $islandMountain    = �η���

sub readIslandsFile
{
    my ($id, $conceal) = @_;

    # �ǡ����ե�����򳫤�
    if (! open(IN, "${dirName}/${dataName}"))
    {
	return 0;
    }

    # �������
    $islandTurn = int(<IN>); # �������
    if ($islandTurn == 0)
    {
	close(IN);
	return 0;
    }

    # �ǽ���������
    $islandLastTime = int(<IN>);
    if ($islandLastTime == 0)
    {
	close(IN);
	return 0;
    }

    # ������
    $islandNumber   = int(<IN>); # ������
    $islandNextID   = int(<IN>); # ���˳�����Ƥ�ID

    # ���������Ƚ��
    $nextTurn = $unitTime - (time - $islandLastTime);
    if ($nextTurn < 0)
    {
	$nextTurn = 0;
    }

    # ����ɤߤ���
    my ($i, $l, $skip, $dummy, $found);
    for ($i = 0; $i < $islandNumber; $i++)
    {
	$l = $islandLines;

	# ̾����SCORE ���ɤ߹���
	$islandName[$i] = <IN>;
	$l--;
	chomp ($islandName[$i]);

	# ���ζ�˴�б�
	$islandName[$i] =~ s/<[^<]*>//g;
	$islandName[$i] =~ s/\r//g;

	if ($islandName[$i] =~ s/,(.*)$//g)
	{
	    $islandScore[$i] = int($1);
	}
	else
	{
	    $islandScore[$i] = 0;
	}

	# $id���ɤ߹���
	$islandID[$i] = int(<IN>);
	$l--;

	# �ɤ߹����оݤ��礫��
	if ($islandID[$i] == $id)
	{
	    # �оݤ���򸫤Ĥ���
	    $islandIndex = $i;
	    $islandRank = $i + 1;

	    # ���ޥǡ���
	    $dummy = <IN>;
	    $l--;

	    # Ϣ³��ⷫ��
	    $dummy = <IN>;
	    $l--;

	    # ������
	    $islandComment = <IN>;
	    $l--;
	    chomp($islandComment);

	    # �ѥ����
	    $islandPassword = <IN>;
	    $l--;
	    chomp($islandPassword);

	    # ���
	    if ($conceal)
	    {
		$islandMoney = concealMoney(int(<IN>));
	    }
	    else
	    {
		$islandMoney = int(<IN>);
	    }
	    $l--;

	    # ����
	    $islandFood  = int(<IN>);
	    $l--;

	    # �͸�
	    $islandPop   = int(<IN>);
	    $l--;

	    # ����
	    $islandArea  = int(<IN>);
	    $l--;

	    # ����
	    $islandFarm  = int(<IN>);
	    $l--;

	    # ����
	    $islandFactory = int(<IN>);
	    $l--;

	    # �η���
	    $islandMountain = int(<IN>);
	    $l--;

	    $found = 1;
	}

	# ������ޤ��ɤ����Ф�
	while ($l > 0)
	{
	    $dummy = <IN>;
	    $l--;
	}
    }
    close(IN);

    if (! $found)
    {
	nack($MISSING_ID);
    }

    return $found;
}


#----------------------------------------
# �Ͽޤ��ɤ߹���
#----------------------------------------
# argument:
#  $id      = ���ID�ֹ�
#  $conceal = ����α���ư��
# return:
#  0 - ����
#  1 - �����Х��ѿ��˰ʲ��Υǡ��������ꤵ��롣
#  $islandMap[]       = �Ͽ�($conceal != 0 �ʤ鱣��)
#  $islandPlan[]      = �ײ�($conceal != 0 �ʤ����ꤵ��ʤ�)
#  $islandComm[]      = �̿���

sub readMapFile
{
    my ($id, $conceal) = @_;
    my ($i, $line);

    # �ե�����򳫤�
    if (! open(MAPID, "${dirName}/island.${id}"))
    {
	nack($FATAL_ERROR);
    }

    # �ǽ�� $islandSize �Ԥ� MAP�ǡ���
    for ($i = 0; $i < $islandSize; $i++)
    {
	$line = <MAPID>;
	chomp ($line);

	if ($conceal)
	{
	    $islandMap[$i] = concealMap($line);
	}
	else
	{
	    $islandMap[$i] = $line;
	}
    }

    # ���� $commandMax �Ԥ� Plan�ǡ���
    for ($i = 0; $i < $commandMax; $i++)
    {
	$line = <MAPID>;
	chomp($line);

	if (! $conceal)
	{
	    $islandPlan[$i] = $line;
	}
    }

    # ���ιԤ��� $lbbsMax �Ԥ� �̿���
    for ($i = 0; $i < $lbbsMax; $i++)
    {
	$line = <MAPID>;
	chomp($line);

	$islandComm[$i] = $line;
    }

    close(MAPID);

    return 1;
}


#----------------------------------------
# MAPʸ����α���
#----------------------------------------
# argument:
#  $string - �����Σ���
# memo:
#  ����ʳ��ξܺ٤򱣤��ޤ���

sub concealMap
{
my ($mapstring) = @_;
my ($x, $result, $land, $landV);
my ($mrexp) = "^(.{${landDigits}})(.{${landValueDigits}})";
my ($mform) = "%0${landDigits}x%0${landValueDigits}x";

    $result = "";


    for ($x = 0; $x < $islandSize; $x++)
    {
        $mapstring =~ s/${mrexp}//;    # ���ιԤ��ѹ�
        $land  = hex($1);
        $landV = hex($2);

	if ($land == $landForest)
	{
	    # �ڤ��ܿ��򱣤�
	    $landV = 0;
	}
	elsif ($land == $landBase)
	{
	    # �ڤΤդ�
	    $land = $landForest;
	    $landV= 0;
	}elsif ($land == $landDefence)
	{
if($landV >1){	    # �ڤΤդ�
	    $land = $landForest;
	    $landV= 0;
	}
}
	elsif ($land == $landSbase)
	{
	    # ���Τդ�
	    $land = $landSea;
	    $landV = 0;
	}
	elsif ($land == $landkiken)
	{
	    # ���Τդ�
	    $land = $landForest;
	    $landV = 0;
	}
elsif ($land == $landKoku)
	{
	    # ���Τդ�
	    $land = $landForest;
	    $landV = 0;
	}
elsif ($land == $landJira)
	{
	    # ���Τդ�
	    $land = $landPlains;
	    $landV = 0;
	}
	elsif ($land == $landDummy)
	{
if($landV <1){	    # �ɱҴ��ϤΤդ�
	    $land = $landDefence;
} else{
# �ڤΤդ�
	    $land = $landForest;
	    $landV= 0;
	}
	}

$result = $result . sprintf($mform, $land, $landV); # ���ιԤ��ѹ�
    }

    return $result;
}


#----------------------------------------
# ���α���
#----------------------------------------
# memo:
# hideMoneyMode = 0 �� ���ϸ����ʤ�
#               = 1 �� ���ϸ�����
#               = 2 �� ����1000����ñ�̤ǻͼθ���

sub concealMoney
{
    my ($money) = @_;

    if ($hideMoneyMode == 0)
    {
	# ��������
	$money = 0;
    }
    elsif ($hideMoneyMode == 1)
    {
	# ������
	$money = -($money+1);
    }
    else # if ($hideMoneyMode == 2)
    {
	if ($money < 500)
	{
	    # 500����̤��
	    $money = 1;
	}
	else
	{
	    $money = int(($money + 500) / 1000) * 1000;
	}
    }

    return $money;
}


#----------------------------------------
# ���ե�����Υ���ɽ��
#----------------------------------------
# argument:
#  $id - ����ɽ���������ID
# memo:
#  $id �� ����ɽ������

sub printAllLog
{
    my($id) = @_;
    my($i);

    for($i = 0; $i < $logMax; $i++)
    {
	printLog($i, $id);
    }
}


#----------------------------------------
# ���ե�����Υ���ɽ��
#----------------------------------------
# argument:
#  $fileNumber - ɽ������ե���������
#  $id - ����ɽ��������� id
# memo:
#  ���ꤵ�줿����Υ�����Ϥ���

sub printLog
{
    my($fileNumber, $id) = @_;
    my($line, $m, $turn, $id1, $id2, $message);

    if (! open(LIN, "${dirName}/hakojima.log${fileNumber}"))
    {
	# ���ե����뤬¸�ߤ��ʤ�
	return;
    }

    while ($line = <LIN>)
    {
	$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),(.*)$/;
	($m, $turn, $id1, $id2, $message) = ($1, $2, $3, $4, $5);

	# ɽ���оݤ��礫��
	if (($id != $id1) &&
	    ($id != $id2))
	{
	    next;
	}

	# ��̩�ط�
	if ($m == 1)
	{
	    if ($id1 != $id)
	    {
		# ��̩ɽ�������ʤ�
		next;
	    }
	    $m = '<B>(��̩)</B>';
	}
	else
	{
	    $m = '';
	}

	# ɽ���ι���
	printSJIS("<NOBR>${tagNumber_}������$turn$m${_tagNumber}��$message</NOBR><BR>\n");
    }
    close(LIN);
}


#----------------------------------------
# �ѥ���ɤΰŹ沽
#----------------------------------------
# memo:
#  hako-main.cgi ��Ʊ������

sub encrypt
{
    my ($plainpass) = @_;

    if ($cryptOn == 1)
    {
        return crypt($plainpass, 'h2');
    }
    else
    {
        return $plainpass;
    }
}


#----------------------------------------
# �ǡ����ե�����Υ�å��������å�
#----------------------------------------
# memo:
#  hako-main.cgi �Ȥۤ�Ʊ������

sub hakolock
{
    if (! $locked)
    {
	if ($lockMode == 1)
	{
	    # directory����å�
	    $locked = hakolock1();
	}
	elsif ($lockMode == 2)
	{
	    # flock����å�
	    $locked = hakolock2();
	}
	elsif ($lockMode == 3)
	{
	    # symlink����å�
	    $locked = hakolock3();
	}
	else
	{
	    # �̾�ե����뼰��å�
	    $locked = hakolock4();
	}
    }

    return $locked;
}


sub hakounlock
{
    if ($locked)
    {
	if ($lockMode == 1)
	{
	    hakounlock1();
	}
	elsif ($lockMode == 2)
	{
	    hakounlock2();
	}
	elsif ($lockMode == 3)
	{
	    hakounlock3();
	}
	else
	{
	    hakounlock4();
	}
    }

    $locked = 0;
}


# directory����å�

sub hakolock1
{
    # ��å���
    if (mkdir('hakojimalock', $dirMode))
    {
	# ����
	return 1;
    }
    else
    {
	return 0;
    }
}

sub hakounlock1
{
    rmdir('hakojimalock');
}


# flock����å�

sub hakolock2
{
    open(LOCKID, '>>hakojimalockflock');

    if (flock(LOCKID, 2))
    {
	# ����
	return 1;
    }
    else
    {
	# ����
	return 0;
    }
}

sub hakounlock2
{
    close(LOCKID);
}


# symlink����å�

sub hakolock3
{
    # ��å���
    if (symlink('hakojimalockdummy', 'hakojimalock'))
    {
	# ����
	return 1;
    }
    else
    {
	# ����
	return 0;
    }
}

sub hakounlock3
{
    unlink('hakojimalock');
}


# �ե����뼰�Υ�å�

sub hakolock4
{
    # ��å���
    if (unlink('key-free'))
    {
	# ����
	open(OUT, '>key-locked');
	print OUT time;
	close(OUT);
	return 1;
    }
    else
    {
	# ����
	return 0;
    }
}

sub hakounlock4
{
    my($i);
    $i = rename('key-locked', 'key-free');
}
