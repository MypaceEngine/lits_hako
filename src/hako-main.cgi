#!/bin/perl
# ���ϥ����С��˹�碌���ѹ����Ʋ�������
# perl5�ѤǤ���

#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �ᥤ�󥹥���ץ�(ver1.00)
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
# �Ƽ�������
# (����ʹߤ���ʬ�γ������ͤ�Ŭ�ڤ��ͤ��ѹ����Ƥ�������)
#----------------------------------------------------------------------
#my($ref_url1) = 'http://123.co.jp/game.html';
#my($ref_url2) = 'http://123.co.jp/game.html';
#my($ref_url3) = 'http://123.co.jp/game.html';
#my($ref_url4) = 'http://123.co.jp/game.html';
#my($ref_url5) = 'http://123.co.jp/game.html';
#my($ref_url6) = 'http://123.co.jp/game.html';
#���Ĥ����󥯸�������С�4,5�Ĥ��ɲäǤ��ޤ�
������ϡ�IFʬ�����������䤷�Ƥ�������
#my($ref) = $ENV{'HTTP_REFERER'};
#$ref =~ tr/+/ /;
#$ref =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
#if (!(($ref =~ /$ref_url1/i)
#|| ($ref =~ /$ref_url2/i)
#|| ($ref =~ /$ref_url3/i)
#|| ($ref =~ /$ref_url4/i)
#|| ($ref =~ /$ref_url5/i)
#|| ($ref =~ /$ref_url6/i))) { &error100; }
#sub error100 {
#if(open(KLOG,">> access.log")){
#print KLOG "$ref\n";
#close(KLOG);
#}
#print "Content-type: text/html\n\n";
#print <<'EOF';
#<HTML><HEAD><TITLE>Ȣ�祢����������</TITLE></HEAD>
#<BODY><center><H1>Ȣ�祢����������</H1><br>
#Lits�������ᥤ��ڡ����ʳ�����Υ���������ػߤ��Ƥ��ޤ���<br>
#�ȥåץڡ�����<a href='http://123.co.jp/'>������</a>
#</BODY></HTML>
#EOF
#exit;
#}
# �����ޤ� 
#----------------------------------------------------------------------
# �ʲ���ɬ�����ꤹ����ʬ
#----------------------------------------------------------------------

# ���Υե�������֤��ǥ��쥯�ȥ�
# my($baseDir) = 'http://�����С�/�ǥ��쥯�ȥ�';
#
# ��)
# http://cgi2.bekkoame.ne.jp/cgi-bin/user/u5534/hakoniwa/hako-main.cgi
# �Ȥ����֤���硢
# my($baseDir) = 'http://cgi2.bekkoame.ne.jp/cgi-bin/user/u5534/hakoniwa';
# �Ȥ��롣�Ǹ�˥���å���(/)���դ��ʤ���

my($baseDir) = 'http://www.yahoo.co.jp';

# �����ե�������֤��ǥ��쥯�ȥ�
# my($imageDir) = 'http://�����С�/�ǥ��쥯�ȥ�';
my($imageDir) = 'http://123.co.jp/***';

# jcode.pl�ΰ���

# my($jcode) = '/usr/libperl/jcode.pl';  # �٥å�����ξ��
# my($jcode) = './jcode.pl';             # Ʊ���ǥ��쥯�ȥ���֤����
my($jcode) = './jcode.pl';

# �ޥ������ѥ����
# ���Υѥ���ɤϡ����٤Ƥ���Υѥ���ɤ����ѤǤ��ޤ���
# �㤨�С���¾����Υѥ�����ѹ�������Ǥ��ޤ���
my($masterPassword) = '123456';

# �ü�ѥ����
# ���Υѥ���ɤǡ�̾���ѹ��פ�Ԥ��ȡ�������λ�⡢�����������ͤˤʤ�ޤ���
# (�ºݤ�̾�����Ѥ���ɬ�פϤ���ޤ���)
$HspecialPassword = '123456';

# ������̾
my($adminName) = 'xx';

# �����ԤΥ᡼�륢�ɥ쥹
my($email) = 'xxx@123.co.jp';

# �Ǽ��ĥ��ɥ쥹
my($bbs) = 'http://123.co.jp/xxx.cgi';

# �ۡ���ڡ����Υ��ɥ쥹
my($toppage) = 'http://123.co.jp/xxx.htm';
my($mentehtml) = 'http://123.co.jp/hako-mente.cgi';
# �ǥ��쥯�ȥ�Υѡ��ߥå����
# �̾��0755�Ǥ褤����0777��0705��0704���Ǥʤ��ȤǤ��ʤ������С��⤢��餷��
$HdirMode = 0755;

# �ǡ����ǥ��쥯�ȥ��̾��
# ���������ꤷ��̾���Υǥ��쥯�ȥ�ʲ��˥ǡ�������Ǽ����ޤ���
# �ǥե���ȤǤ�'data'�ȤʤäƤ��ޤ������������ƥ��Τ���
# �ʤ�٤��㤦̾�����ѹ����Ƥ���������
$HdirName = 'xxx';
$HdirName1 = 'xx';
$HdirName2 = 'x';
# �ǡ����ν񤭹�����

# ��å�������
# 1 �ǥ��쥯�ȥ�
# 2 �����ƥॳ����(��ǽ�ʤ�кǤ�˾�ޤ���)
# 3 ����ܥ�å����
# 4 �̾�ե�����(���ޤꤪ����Ǥʤ�)
my($lockMode) = 2;

# (��)
# 4�����򤹤���ˤϡ�'key-free'�Ȥ������ѡ��ߥ����666�ζ��Υե������
# ���Υե������Ʊ���֤��֤��Ʋ�������

#----------------------------------------------------------------------
# ɬ�����ꤹ����ʬ�ϰʾ�
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �ʲ������ߤˤ�ä����ꤹ����ʬ
#----------------------------------------------------------------------
#----------------------------------------
# ������οʹԤ�ե�����ʤ�
#----------------------------------------
# 1�����󤬲��ä�
$HunitTime = 14400;

# �۾ｪλ������
# (��å��岿�äǡ�����������뤫)
my($unlockTime) = 60;

# ��κ����
$HmaxIsland =99;

# �ȥåץڡ�����ɽ��������Υ������
$HtopLogTurn = 1;

# ���ե������ݻ��������
$HlogMax = 10; 

# �Хå����åפ򲿥����󤪤��˼�뤫
$HbackupTurn = 1;

# �Хå����åפ򲿲�ʬ�Ĥ���
$HbackupTimes = 20;

# ȯ�����ݻ��Կ�
$HhistoryMax = 30;

# �������ޥ�ɼ�ư���ϥ������
$HgiveupTurn = 10000;

# ���ޥ�����ϸ³���
# (�����ब�ϤޤäƤ����ѹ�����ȡ��ǡ����ե�����θߴ�����̵���ʤ�ޤ���)
$HcommandMax = 50;

# ������Ǽ��ĹԿ�����Ѥ��뤫�ɤ���(0:���Ѥ��ʤ���1:���Ѥ���)
$HuseLbbs = 1;

# ������Ǽ��ĹԿ�
$HlbbsMax = 20;

# ������Ǽ��ǤΥѥ����ǧ��
# ¾����Υ����ʡ����񤭹���Ȥ��˥ѥ���ɳ�ǧ��̵ͭ
$HlbbsAuth = 1;

# ������Ǽ��ǤΥ����Ȼ���
# 1 �ΤȤ�����Υ����ʡ��Ǥʤ��ͤ��񤭹��ळ�Ȥ������
$HlbbsGuest = 1;

# �����ľ��Υߥ�����ȯ�Ͷػߥ������
# 0 �ˤ���к���ľ��Ǥ�ߥ�����ȯ�ͤ���ǽ�ˤʤ�ޤ�
$HdisableMissileTurn = 0;

# �����ľ��β����ɸ��ػߥ������
# 0 �ˤ���к���ľ��Ǥ�����ɸ�����ǽ�ˤʤ�ޤ�
$HdisableSendMonsterTurn = 0;

# �����ľ��λ�����ػߥ������
# 0 �ˤ���� ����ľ��Ǥ���������ǽ�ˤʤ�ޤ�
$HdisableSupportTurn = 0;

# ����礭��
# (�ѹ��Ǥ��ʤ�����)
$HislandSize = 31;

# ¾�ͤ�����򸫤��ʤ����뤫
# 0 �����ʤ�
# 1 ������
# 2 100�ΰ̤ǻͼθ���
$HhideMoneyMode = 2;

# �ѥ���ɤΰŹ沽(0���ȰŹ沽���ʤ���1���ȰŹ沽����)
my($cryptOn) = 1;

# �ǥХå��⡼��(1���ȡ��֥������ʤ��ץܥ��󤬻��ѤǤ���)
$Hdebug = 0;

# write open �� retry ���
$HretryCount = 5;

#----------------------------------------
# ��⡢�����ʤɤ������ͤ�ñ��
#----------------------------------------
# ������
$HinitialMoney = 1000;

# �������
$HinitialFood = 100;

# �����ñ��
$HunitMoney = '����';

# ������ñ��
$HunitFood = '00�ȥ�';
$HunitOil = '�ȥ�';

# �͸���ñ��
$HunitPop = '00��';

# ������ñ��
$HunitArea = '00�إ�������';

# �ڤο���ñ��
$HunitTree = '00��';

# �ڤ�ñ�������������
$HtreeValue = 10;

# ̾���ѹ��Υ�����
$HcostChangeName = 1;

# �͸�1ñ�̤�����ο���������
$HeatenFood = 0.05;

#----------------------------------------
# ���Ϥηи���
#----------------------------------------
# �и��ͤκ�����
$HmaxExpPoint = 255; # ������������Ǥ�255�ޤ�

# ��٥�κ�����
my($maxBaseLevel) = 5;  # �ߥ��������
my($maxSBaseLevel) = 5; # �������

# �и��ͤ������Ĥǥ�٥륢�åפ�
my(@baseLevelUp, @sBaseLevelUp);
@baseLevelUp = (20, 60, 120, 200); # �ߥ��������
@sBaseLevelUp = (20, 60, 120, 200);         # �������

#----------------------------------------
# �ɱһ��ߤμ���
#----------------------------------------
# ���ä�Ƨ�ޤ줿����������ʤ�1�����ʤ��ʤ�0
$HdBaseAuto = 1;

#----------------------------------------
# �ҳ�
#----------------------------------------
# �̾�ҳ�ȯ��Ψ(��Ψ��0.1%ñ��)
$HdisMaizo      = 1; # ��¢��
# ��������
$HdisFallBorder = 600; # �����³��ι���(Hex��)
$HdisFalldown   = 30; # ���ι�����Ķ�������γ�Ψ

# ����
$HdisMonsBorder1 = 1001; # �͸����1(���å�٥�1)
$HdisMonsBorder2 = 2000; # �͸����2(���å�٥�2)
$HdisMonsBorder3 = 3000; # �͸����3(���å�٥�3)
$HdisMonsBorder4 = 4000; # �͸����2(���å�٥�2)
$HdisMonsBorder5 = 5000; # �͸����3(���å�٥�3)
$HdisMonsBorder6 = 6000; # �͸����3(���å�٥�3)
$HdisMonsBorder7 = 7000; # �͸����3(���å�٥�3)
$HdisMonsBorder8 = 8000; # �͸����3(���å�٥�3)
$HdisMonsBorder9 = 9000; # �͸����3(���å�٥�3)
# ����
$HmonsterNumber  = 26; 

# �ƴ��ˤ����ƽФƤ�����ä��ֹ�κ�����
$HmonsterLevel1  = 2; # ���󥸥�ޤ�    
$HmonsterLevel2  = 4; # ���Τ饴�����Ȥޤ�
$HmonsterLevel3  = 6; # ���󥰤��Τ�ޤ�(����)
$HmonsterLevel4  = 10; # ���Τ饴�����Ȥޤ�
$HmonsterLevel5  = 13; # ���󥰤��Τ�ޤ�(����)
$HmonsterLevel6  = 15; # ���Τ饴�����Ȥޤ�
$HmonsterLevel7  = 17; # ���󥰤��Τ�ޤ�(����)
$HmonsterLevel8  = 20; # ���Τ饴�����Ȥޤ�
$HmonsterLevel9  = 21; # ���󥰤��Τ�ޤ�(����)
# ̾��
@HmonsterName = 
    (
     '�ᥫ���Τ�',     # 0(��¤)
     '���Τ�',         # 1
     '���󥸥�',       # 2
     '��åɤ��Τ�',   # 3
     '���������Τ�',   # 4
   '���Τ饨�å�',   # 3
     '���Τ�٥��ӡ�',   # 4
     '���Τ饴������', # 5
     '������',         # 6
     '���󥰤��Τ�',    # 7
'���Τ饯������',
     'ŷ�Ȥ��Τ�',         # 1
     '���⤤�Τ�',       # 2
     '�夤�Τ�',
     '�饸��',         # 1
     '������ȥ����󤤤Τ�',
'�ɥ饴��',
'�Ф��Τ�',
'����ɤ��Τ�',
'���奷�����ʼ',
'������Ƽʼ',
     '���Τ��',
     'Ŵ��ʼ',
'�ù�����',
'FX-330',
'FX-330A'
);

# �������ϡ����Ϥ������ü�ǽ�ϡ��и��͡����Τ�����
@HmonsterBHP     = ( 2, 1, 1, 3, 2, 9, 9, 1, 4, 5, 2, 9 ,9, 1,1, 1, 9, 9, 9, 9, 9, 9,4,6,8,5);
@HmonsterDHP     = ( 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 1, 0, 0, 0,8, 8, 0,0, 0, 0, 0, 0, 0, 0, 0, 0);
@HmonsterSpecial = ( 0, 0, 3, 0, 1, 5, 6, 2, 4, 0, 7, 8, 9, 11,12,13,15,16,17,22,18,14,10,19,20,21);
@HmonsterExp     = ( 5, 5, 7,12,15,20,30,10,20,30, 40,50,50,3,20,30,30,40,40,50,100,255,10,20,30,50);
@HmonsterValue   = ( 0, 400, 500, 1000, 800, 1000, 1500, 300, 1500, 2000, 4000, 5000, 5000, 1,2000,1000,2000,3000,3000,5000,10000,999999,10,20,30,50);

# �ü�ǽ�Ϥ����Ƥϡ�
# 0 �äˤʤ�
# 1 ­��®��(����2�⤢�뤯)
# 2 ­���ȤƤ�®��(���粿�⤢�뤯������)
# 3 ���������ϹŲ�
# 4 ����������ϹŲ�

# �����ե�����
@HmonsterImage =
    (
     'monster7.gif',
     'monster0.gif',
     'monster5.gif',
     'monster1.gif',
     'monster2.gif',
    'monster9.gif',
     'monster10.gif',
     'monster8.gif',
     'monster6.gif',
     'monster3.gif',
     'monster11.gif',
     'monster13.gif',
     'monster14.gif',
     'monster12.gif',
     'monster16.gif',
     'monster17.gif',
'monster23.gif',
'monster21.gif',
'monster22.gif',
'monster26.gif',
'monster20.gif',
     'monster18.gif',
     'monster19.gif',
'monster15.gif',
'monster24.gif',
'monster25.gif'
);

# �����ե����뤽��2(�Ų���)
@HmonsterImage2 =
    ('', '', 'monster4.gif', '', '', '', '', '', 'monster4.gif', '', '', '', '', '', '', 'monster16.gif', '', '', '', '', '', '', '', '', '', '', '');


#----------------------------------------
# ����
#----------------------------------------
# ���Ĥμ���
$HoilMoney = 2000;

# ���Ĥθϳ��Ψ
$HoilRatio = 20;

#----------------------------------------
# ��ǰ��
#----------------------------------------
# �����ढ�뤫
$HmonumentNumber = 8;

# ̾��
@HmonumentName = 
    (
     '��Υꥹ', 
     '���׼԰�����',
     '�襤����',
     '������(��)',
     '������(��)',
     '������(Ƽ)',
'ŷ����(��)',
'ŷ����(��)',
    );

# �����ե�����
@HmonumentImage = 
    (
     'monument0.gif',
     'monument2.gif',
     'monument1.gif',
     'monument3.gif',
     'monument4.gif',
     'monument5.gif',
     'monument6.gif',
     'monument7.gif',

     );

#----------------------------------------
# �޴ط�
#----------------------------------------
# �������դ򲿥�������˽Ф���
$HturnPrizeUnit = 10;

# �ޤ�̾��
$Hprize[0] = '��������';
$Hprize[1] = '�˱ɾ�';
$Hprize[2] = 'Ķ�˱ɾ�';
$Hprize[3] = 'Ķ���˱ɾ�';
$Hprize[4] = 'ʿ�¾�';
$Hprize[5] = 'Ķʿ�¾�';
$Hprize[6] = 'Ķ��ʿ�¾�';
$Hprize[7] = '�����';
$Hprize[8] = 'Ķ�����';
$Hprize[9] = 'Ķ������';
$Hprize[10] = '����˱ɾ�';
$Hprize[11] = '���ʿ�¾�';
$Hprize[12] = '��˺����';

#----------------------------------------
# �����ط�
#----------------------------------------
# <BODY>�����Υ��ץ����
my($htmlBody) = 'BGCOLOR="#EEFFFF"';

# ������Υ����ȥ�ʸ��
$Htitle = 'LitsȢ��';

# ����
# �����ȥ�ʸ��
$HtagTitle_ = '<FONT SIZE=7 COLOR="#8888ff">';
$H_tagTitle = '</FONT>';

# H1������
$HtagHeader_ = '<FONT COLOR="#4444ff">';
$H_tagHeader = '</FONT>';

# �礭��ʸ��
$HtagBig_ = '<FONT SIZE=6>';
$H_tagBig = '</FONT>';

# ���̾���ʤ�
$HtagName_ = '<FONT COLOR="#a06040"><B>';
$H_tagName = '</B></FONT>';

# �����ʤä����̾��
$HtagName2_ = '<FONT COLOR="#808080"><B>';
$H_tagName2 = '</B></FONT>';

# ��̤��ֹ�ʤ�
$HtagNumber_ = '<FONT COLOR="#800000"><B>';
$H_tagNumber = '</B></FONT>';

# ���ɽ�ˤ����븫����
$HtagTH_ = '<FONT COLOR="#C00000"><B>';
$H_tagTH = '</B></FONT>';

# ��ȯ�ײ��̾��
$HtagComName_ = '<FONT COLOR="#d08000"><B>';
$H_tagComName = '</B></FONT>';

# �ҳ�
$HtagDisaster_ = '<FONT COLOR="#ff0000"><B>';
$H_tagDisaster = '</B></FONT>';

# ������Ǽ��ġ��Ѹ��Ԥν񤤤�ʸ��
$HtagLbbsSS_ = '<FONT COLOR="#0000ff"><B>';
$H_tagLbbsSS = '</B></FONT>';

# ������Ǽ��ġ����ν񤤤�ʸ��
$HtagLbbsOW_ = '<FONT COLOR="#ff0000"><B>';
$H_tagLbbsOW = '</B></FONT>';
$HtagLbbsXX_ = '<FONT COLOR="#888888"><B>';
$H_tagLbbsXX = '</B></FONT>';
# �̾��ʸ����(��������Ǥʤ���BODY�����Υ��ץ�����������ѹ����٤�
$HnormalColor = '#000000';

# ���ɽ�������°��
$HbgTitleCell   = 'BGCOLOR="#ccffcc"'; # ���ɽ���Ф�
$HbgNumberCell  = 'BGCOLOR="#ccffcc"'; # ���ɽ���
$HbgNameCell    = 'BGCOLOR="#ccffff"'; # ���ɽ���̾��
$HbgInfoCell    = 'BGCOLOR="#ccffff"'; # ���ɽ��ξ���
$HbgCommentCell = 'BGCOLOR="#ccffcc"'; # ���ɽ��������
$HbgInputCell   = 'BGCOLOR="#ccffcc"'; # ��ȯ�ײ�ե�����
$HbgMapCell     = 'BGCOLOR="#ccffcc"'; # ��ȯ�ײ��Ͽ�
$HbgCommandCell = 'BGCOLOR="#ccffcc"'; # ��ȯ�ײ����ϺѤ߷ײ�

#----------------------------------------------------------------------
# ���ߤˤ�ä����ꤹ����ʬ�ϰʾ�
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# ����ʹߤΥ�����ץȤϡ��ѹ�����뤳�Ȥ����ꤷ�Ƥ��ޤ��󤬡�
# �����äƤ⤫�ޤ��ޤ���
# ���ޥ�ɤ�̾�������ʤʤɤϲ��䤹���Ȼפ��ޤ���
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �Ƽ����
#----------------------------------------------------------------------
# ���Υե�����
$HthisFile = "$baseDir/hako-main.cgi";

# ���ץ�å��̿��� CGI
$HjavaFile = "$baseDir/hako-java.cgi";

# �Ϸ��ֹ�
$HlandSea      = 0;  # ��
$HlandWaste    = 1;  # ����
$HlandPlains   = 2;  # ʿ��
$HlandTown     = 3;  # Į��
$HlandForest   = 4;  # ��
$HlandFarm     = 5;  # ����
$HlandFactory  = 6;  # ����
$HlandBase     = 7;  # �ߥ��������
$HlandDefence  = 8;  # �ɱһ���
$HlandMountain = 9;  # ��
$HlandMonster  = 10; # ����
$HlandSbase    = 11; # �������
$HlandOil      = 12; # ��������
$HlandMonument = 13; # ��ǰ��
$HlandHaribote = 14; # �ϥ�ܥ�
$Hlanddoubutu  = 15; 
$Hlandkiken = 16; # �ϥ�ܥ�
$Hlandkishou  = 17;
$Hlandkukou  = 18; 
$Hlandhokak  = 19; 
$Hlandhos  = 20;
$HlandSefence = 21;
$HlandLake = 22;
$HlandOnpa = 23;
$HlandInok= 24;
$HlandPori= 25;
$HlandJous= 26;
$HlandHatu= 27;
$HlandGomi= 28;
$HlandBouh= 29;
$HlandMina= 30;
$HlandJusi= 31;
$HlandDenb= 32;
$HlandTaiy= 33;
$HlandGoyu= 34;
$HlandBoku= 35;
$HlandReho= 36;
$HlandKoku= 37;
$HlandLand= 38;
$HlandFuha= 39;
$HlandStation  = 40;
$HlandJirai  = 41;
$HlandSuiry  = 42;
$HlandTinet  = 43;
$HlandChou  = 44;
$HlandShou  = 45;
$HlandEisei  = 46;
# ���ޥ��

# �ײ��ֹ������
# ���Ϸ�
$HcomPrepare  = 01; # ����
$HcomPrepare2 = 02; # �Ϥʤ餷
$HcomReclaim  = 03; # ���Ω��
$HcomDestroy  = 04; # ����
$HcomSellTree = 05; # Ȳ��
$HcomOnse    = 06; # �ɱһ��߷���
$HcomUmeta   = 07;
$Hcomkaitetu   = 10;

# ����
$HcomPlant    = 11; # ����
$HcomFarm     = 12; # ��������
$HcomFactory  = 13; # �������
$HcomMountain = 14; # �η�������
$HcomBase     = 15; # �ߥ�������Ϸ���
$HcomDbase    = 16; # �ɱһ��߷���
$HcomSbase    = 17; # ������Ϸ���
$HcomMonument = 18; # ��ǰ���¤
$HcomHaribote = 19; # �ϥ�ܥ�����
$Hcomdoubutu = 20; # ưʪ����ߡ�
$HcomOmise = 21; # ưʪ�����
$HcomBank = 22;
$HcomTbase    = 23; # �ɱһ��߷���
$Hcomkiken = 24;
$Hcomkishou    = 25; # �ɱһ��߷���
$Hcomkukou    = 26; # �ɱһ��߷���
$Hcomyousho    = 27;
$Hcomhospit    = 28;
$HcomUbase    = 29;
# ȯ�ͷ�
$HcomMissileNC   = 30; # Φ��������
$HcomMissileNM   = 31; # �ߥ�����ȯ��
$HcomMissilePP   = 32; # PP�ߥ�����ȯ��
$HcomMissileST   = 33; # ST�ߥ�����ȯ��
$HcomMissileLD   = 34; # Φ���˲���ȯ��
$HcomSendMonster = 35; # �����ɸ�
$HcomSendMonster2 = 36; # �����ɸ�
$HcomMissileRE   = 37; # Φ��������
$HcomMissileMK   = 38; # Φ��������
$HcomMissileUC   = 39; # Φ��������
$HcomMissileEM   = 40; # Φ��������
# ���ķ�
$HcomDoNothing  = 41; # ��ⷫ��
$HcomSell       = 42; # ����͢��
$HcomMoney      = 43; # �����
$HcomFood       = 44; # �������
$HcomPropaganda = 45; # Ͷ�׳�ư
$HcomGiveup     = 46; # �������
$HcomImport     = 47;
$Hcomteikou     = 48;
$HcomMissileHP   = 51; # Φ��������
$HcomOnpa   = 52;
$HcomInok   = 53;
$HcomGeki   = 54;
$HcomPori   = 55;
$HcomJous   = 56;
$HcomHatu  = 57;
$HcomGomi  = 58;
$HcomBouh  = 59;
$HcomMina  = 60;

# ��ư���Ϸ�
$HcomAutoPrepare  = 61; # �ե�����
$HcomAutoPrepare2 = 62; # �ե��Ϥʤ餷
$HcomAutoDelete   = 63; # �����ޥ�ɾõ�
$HcomReclaim2     = 64;
$HcomReho  = 65;
$HcomGoyu  = 66;
$HcomBoku  = 67;
$HcomTaiy  = 68;
$HcomDenb  = 69;
$HcomJusi  = 70;
$Hcomkouei        = 71; # �ե�����
$Hcomkanei        = 72; # �ե��Ϥʤ餷
$Hcomkouuti       = 73; # �����ޥ�ɾõ�
$Hcomkanuti       = 74;
$Hcombouei       = 75; # �����ޥ�ɾõ�
$Hcombouuti       = 76;
$Hcomreiei       = 77; # �����ޥ�ɾõ�
$Hcomreiuti       = 78;
$Hcomhatei       = 79; # �����ޥ�ɾõ�
$Hcomhatuti       = 80;

$Hcomsennyu        = 81; # �ե�����
$Hcomheinyu        = 82; # �ե��Ϥʤ餷
$Hcominonyu       = 83; # �����ޥ�ɾõ�
$Hcomsende       = 84;
$Hcomheide        = 85; # �ե�����
$Hcominode        = 86; # �ե��Ϥʤ餷
$Hcomteiko        = 87; # �ե�����
$Hcomkyouko        = 88; # �ե��Ϥʤ餷

$Hcomtaifuu      = 91; # �ե��Ϥʤ餷
$Hcomtunami       = 92; # �����ޥ�ɾõ�
$Hcomfunka       = 93;
$Hcominseki        = 94; # �ե�����
$Hcomdaiinseki       = 95; # �ե��Ϥʤ餷
$Hcomjisin        = 96; # �ե�����
$Hcomjibantinka        = 97;
$Hcomkasai        = 98;
$HcomRazer        = 99;

$HcomShakufi        = 100;
$HcomShakuse       = 101;
$HcomShakuth      = 102;
$HcomRob    = 103;
$HcomRobST  = 104;
$HcomOilSell = 105;
$HcomOilImport = 106;
$HcomKoku = 107;
$HcomKeiba       = 108;
$HcomFoot      = 109;
$HcomYakyu    = 110;
$HcomSki  = 111;
$HcomSuiz = 112;
$HcomHotel = 113;
$HcomOil   =114;
$HcomSlag   =115;
$HcomGolf = 116;
$HcomYuu = 117;
$HcomTenj   =118;
$HcomKaji   =119;
$HcomFuha   =120;
$HcomKouen   =121;
$HcomShok   =122;
$HcomTou   =123;
$HcomShiro   =124;
$HcomMissileNEB = 125;
$HcomStation  = 126; # ������
$HcomRail     = 127; # ��ϩ����
$HcomMine      = 128; # ��������
$HcomMineSuper = 129; # ����ǽ��������
$HcomMineWrpe = 130; # ����ǽ��������
$HcomOilH =131;
$HcomMoneyH = 132;
$HcomFoodH = 133;
$HcomSuiry =134;
$HcomTinet = 135;
$HcomChou = 136;
$HcomTuri =137;
$HcomOoame =138;
$HcomSendMonster3 =139;
$HcomSendMonster4 =140;
$HcomSendMonster5 =141;
$HcomPMSei =142;
$HcomPMSuti =143;
$HcomPMS =144;
$HcomMissileUB = 145;
$Hcomjoyo =146;
$Hcomtimya =147;
$HcomShou =148;
$HcomDestroy2  = 149;
$HcomReclaim3   = 150;
$HcomEisei   = 151;
# ���ù���
$HcommandTotala = 10;
@HcomLista = ($HcomPrepare,$HcomPrepare2,$HcomReclaim,$HcomUmeta,$HcomDestroy,$HcomDestroy2,$Hcomjoyo,$Hcomkaitetu,$HcomPlant,$HcomSellTree);
# ����
$HcommandTotalb = 60;
@HcomListb = ($HcomFarm,$Hcomyousho,$HcomBoku,$HcomFactory,$HcomMountain,$HcomHatu,$HcomFuha,$HcomTaiy,$HcomSuiry,$HcomTinet,$HcomChou,$HcomJusi,$HcomDenb,$HcomJous,$HcomGomi,$HcomGoyu,$HcomPori,$HcomShou,$Hcomhospit,$HcomStation,$HcomRail,$Hcomkukou,$HcomBouh,$HcomMina,$HcomOnse,$Hcomdoubutu,$HcomOmise,$HcomBank,$Hcomkiken,$Hcomkishou,$HcomOnpa,$HcomInok,$HcomEisei,$HcomReho,$HcomMine,$HcomMineSuper,$HcomMineWrpe,$HcomKoku,$HcomBase,$HcomSbase,$HcomDbase,$HcomUbase,$HcomTbase,$HcomHaribote,$HcomKeiba,$HcomFoot,$HcomYakyu,$HcomSki,$HcomSuiz,$HcomHotel,$HcomGolf,$HcomYuu,$HcomTenj,$HcomKaji,$HcomKouen,$HcomShok,$HcomTou,$HcomShiro,$HcomTuri,$HcomMonument);
# �ǰ�
$HcommandTotalc = 4;
@HcomListc = ($HcomSell,$HcomOilSell,$HcomImport,$HcomOilImport);
# ���
$HcommandTotald = 7;
@HcomListd = ($HcomMoney,$HcomMoneyH,$HcomFood,$HcomFoodH,$HcomOil,$HcomOilH,$HcomSlag);
# �ߥ�����
$HcommandTotale = 12;
@HcomListe = ($HcomMissileNM,$HcomMissileEM,$HcomMissileNC,$HcomMissilePP,$HcomMissileST,$HcomMissileLD,$HcomMissileRE,$HcomMissileMK,$HcomMissileUC,$HcomMissileNEB,$HcomMissileHP,$HcomMissileUB);
# �����ɸ�
$HcommandTotalf = 5;
@HcomListf = ($HcomSendMonster,$HcomSendMonster2,$HcomSendMonster3,$HcomSendMonster4,$HcomSendMonster5);
# ����
$HcommandTotalg = 14;
@HcomListg = ($Hcomkouei,$Hcomkanei,$Hcombouei,$Hcomhatei,$Hcomreiei,$HcomPMSei,$Hcomkouuti,$Hcomkanuti,$Hcombouuti,$Hcomhatuti,$Hcomreiuti,$HcomPMSuti,$HcomRazer,$HcomPMS);
# ����ʼ��
$HcommandTotalh = 10;
@HcomListh = ($Hcomtaifuu,$Hcomtunami,$Hcomfunka,$Hcominseki,$Hcomdaiinseki,$Hcomjisin,$Hcomkasai,$HcomOoame,$Hcomtimya,$Hcomjibantinka);
# Ʊ��
$HcommandTotali = 8;
@HcomListi = ($Hcomsennyu,$Hcomheinyu,$Hcominonyu,$Hcomsende,$Hcomheide,$Hcominode,$Hcomteiko,$Hcomkyouko);
# ����¾
$HcommandTotalj = 10;
@HcomListj = ($HcomDoNothing,$HcomPropaganda,$HcomRob,$HcomRobST,$HcomShakufi,$HcomShakuse,$HcomShakuth,$HcomGeki,$Hcomteikou,$HcomGiveup);
# ��ư����
$HcommandTotalk = 5;
@HcomListk = ($HcomAutoPrepare,$HcomAutoPrepare2,$HcomReclaim2,$HcomReclaim3,$HcomAutoDelete);

$HcommandTotall = 3;
@HcomListl = ($HcomFarm,$Hcomyousho,$HcomBoku);

$HcommandTotalm = 1;
@HcomListm = ($HcomFactory);

$HcommandTotaln = 1;
@HcomListn = ($HcomMountain);

$HcommandTotalo = 8;
@HcomListo = ($HcomHatu,$HcomFuha,$HcomTaiy,$HcomSuiry,$HcomTinet,$HcomChou,$HcomJusi,$HcomDenb);

$HcommandTotalp = 7;
@HcomListp = ($HcomJous,$HcomGomi,$HcomGoyu,$HcomPori,$HcomShou,$Hcomhospit,$HcomBouh);

$HcommandTotalq = 4;
@HcomListq = ($HcomStation,$HcomRail,$Hcomkukou,$HcomMina);

$HcommandTotalr = 11;
@HcomListr = ($HcomKoku,$HcomBase,$HcomSbase,$HcomDbase,$HcomUbase,$HcomTbase,$HcomHaribote,$HcomReho,$HcomMine,$HcomMineSuper,$HcomMineWrpe);

$HcommandTotals = 5;
@HcomLists = ($Hcomkiken,$Hcomkishou,$HcomOnpa,$HcomInok,$HcomEisei);

$HcommandTotalt = 20;
@HcomListt = ($HcomOnse,$Hcomdoubutu,$HcomOmise,$HcomBank,$HcomKeiba,$HcomFoot,$HcomYakyu,$HcomSki,$HcomSuiz,$HcomHotel,$HcomGolf,$HcomYuu,$HcomTenj,$HcomKaji,$HcomKouen,$HcomShok,$HcomTou,$HcomShiro,$HcomTuri,$HcomMonument);
# �ײ��̾��������
$HcomName[$HcomPrepare]      = '����';
$HcomCost[$HcomPrepare]      = 5;
$HcomName[$HcomPrepare2]     = '�Ϥʤ餷';
$HcomCost[$HcomPrepare2]     = 100;
$HcomName[$Hcomjoyo]      = '����ű��';
$HcomCost[$Hcomjoyo]      = 500;
$HcomName[$HcomReclaim]      = '���Ω��';
$HcomCost[$HcomReclaim]      = 150;
$HcomName[$HcomUmeta] = '�ʹ����Ω��';
$HcomCost[$HcomUmeta] = 300;
$HcomName[$HcomDestroy2]      = '�ʹӷ���';
$HcomCost[$HcomDestroy2]      = 400;
$HcomName[$HcomDestroy]      = '����';
$HcomCost[$HcomDestroy]      = 200;
$HcomName[$HcomOnse] = '�����η�';
$HcomCost[$HcomOnse] = 200;
$HcomName[$HcomPlant]        = '����';
$HcomCost[$HcomPlant]        = 50;
$HcomName[$HcomSellTree]     = 'Ȳ��';
$HcomCost[$HcomSellTree]     = 0;
$HcomName[$Hcomyousho]        = '�ܿ������';
$HcomCost[$Hcomyousho]        = 100;
$HcomName[$Hcomkaitetu]     = '����ű��';
$HcomCost[$Hcomkaitetu]     = 20;
$HcomName[$HcomFarm]         = '��������';
$HcomCost[$HcomFarm]         = 20;
$HcomName[$HcomFactory]      = '�������';
$HcomCost[$HcomFactory]      = 100;
$HcomName[$HcomMountain]     = '�η�������';
$HcomCost[$HcomMountain]     = 300;
$HcomName[$Hcomdoubutu] = 'ưʪ�����';
$HcomCost[$Hcomdoubutu] = 700;
$HcomName[$HcomOmise] = '�ǥѡ��ȷ���';
$HcomCost[$HcomOmise] = 1000;
$HcomName[$HcomBank] = '��Է���';
$HcomCost[$HcomBank] = 1000;
$HcomName[$Hcomkiken] = '���ݸ�������';
$HcomCost[$Hcomkiken] = 5000;
$HcomName[$Hcomkishou] = '���ݴ�¬�����';
$HcomCost[$Hcomkishou] = 2000;
$HcomName[$Hcomkukou] = '��������';
$HcomCost[$Hcomkukou] = 4000;
$HcomName[$Hcomhospit] = '�±�����';
$HcomCost[$Hcomhospit] = 300;
$HcomName[$HcomOnpa] = '�ü첻�Ȼ��߷���';
$HcomCost[$HcomOnpa] = 3000;
$HcomName[$HcomInok] = '���Τ鸦������';
$HcomCost[$HcomInok] = 2000;
$HcomName[$HcomPori] = '�ٻ������';
$HcomCost[$HcomPori] = 2000;
$HcomName[$HcomJous] = '���������';
$HcomCost[$HcomJous] = 100;
$HcomName[$HcomHatu] = '����ȯ�Ž�����';
$HcomCost[$HcomHatu] = 100;
$HcomName[$HcomFuha] = '����ȯ�Ž�����';
$HcomCost[$HcomFuha] = 10;
$HcomName[$HcomGomi] = '���߽�����������';
$HcomCost[$HcomGomi] = 100;
$HcomName[$HcomBouh] = '����������';
$HcomCost[$HcomBouh] = 160;
$HcomName[$HcomMina] = '������';
$HcomCost[$HcomMina] = 30;
$HcomName[$HcomEisei] = '�������״�������';
$HcomCost[$HcomEisei] = 10000;
$HcomName[$HcomJusi] = '�ޥ������ȼ�����������';
$HcomCost[$HcomJusi] = 10000;
$HcomName[$HcomDenb] = '����������ҷ���';
$HcomCost[$HcomDenb] = 5000;
$HcomName[$HcomTaiy] = '���۸�ȯ�Ž�����';
$HcomCost[$HcomTaiy] = 1000;
$HcomName[$HcomSuiry] = '����ȯ�Ž�����';
$HcomCost[$HcomSuiry] = 1500;
$HcomName[$HcomTinet] = '��Ǯȯ�Ž�����';
$HcomCost[$HcomTinet] = 800;
$HcomName[$HcomChou] = '����ȯ�Ž�����';
$HcomCost[$HcomChou] = 1000;
$HcomName[$HcomTuri] = '���������';
$HcomCost[$HcomTuri] = 100;
$HcomName[$HcomGoyu] = '����͢�е�������';
$HcomCost[$HcomGoyu] = 10000;
$HcomName[$HcomBoku] = '�Ҿ�����';
$HcomCost[$HcomBoku] = 500;
$HcomName[$HcomReho] = '���«�졼����ˤ����';
$HcomCost[$HcomReho] = 1000;
$HcomName[$HcomMine]         = '��������';
$HcomCost[$HcomMine]         = 300;
$HcomName[$HcomMineSuper]    = '����ǽ��������';
$HcomCost[$HcomMineSuper]    = 600;
$HcomName[$HcomMineWrpe]    = '�����������';
$HcomCost[$HcomMineWrpe]    = 500;
$HcomName[$HcomKoku] = '�������������';
$HcomCost[$HcomKoku] = 100;
$HcomName[$HcomKeiba] = '���Ͼ����';
$HcomCost[$HcomKeiba] = 2000;
$HcomName[$HcomFoot] = '���å����������������';
$HcomCost[$HcomFoot] = 2000;
$HcomName[$HcomYakyu] = '�������';
$HcomCost[$HcomYakyu] = 1500;
$HcomName[$HcomSki] = '���⥹���������';
$HcomCost[$HcomSki] = 3000;
$HcomName[$HcomSuiz] = '��²�۷���';
$HcomCost[$HcomSuiz] = 1200;
$HcomName[$HcomHotel] = '�꥾���ȥۥƥ����';
$HcomCost[$HcomHotel] = 2000;
$HcomName[$HcomGolf] = '����վ����';
$HcomCost[$HcomGolf] = 1300;
$HcomName[$HcomYuu] = 'ͷ���Ϸ���';
$HcomCost[$HcomYuu] = 1500;
$HcomName[$HcomTenj] = 'Ÿ�������';
$HcomCost[$HcomTenj] = 1000;
$HcomName[$HcomKaji] = '�����η���';
$HcomCost[$HcomKaji] = 500;
$HcomName[$HcomKouen] = '�������';
$HcomCost[$HcomKouen] = 100;
$HcomName[$HcomShok] = '��ʪ�����';
$HcomCost[$HcomShok] = 1500;
$HcomName[$HcomTou] = '�����';
$HcomCost[$HcomTou] = 1000;
$HcomName[$HcomShiro] = '�����';
$HcomCost[$HcomShiro] = 3000;
$HcomName[$HcomShou] = '���ɽ����';
$HcomCost[$HcomShou] = 3000;
$HcomName[$HcomStation]      = '�ط���';
$HcomCost[$HcomStation]      = 500;
$HcomName[$HcomRail]         = '��ϩ����';
$HcomCost[$HcomRail]         = 100;
$HcomName[$HcomBase]         = '�ߥ�������Ϸ���';
$HcomCost[$HcomBase]         = 300;
$HcomName[$HcomSbase]        = '������Ϸ���';
$HcomCost[$HcomSbase]        = 8000;
$HcomName[$HcomDbase]        = '�ɱһ��߷���';
$HcomCost[$HcomDbase]        = 800;
$HcomName[$HcomUbase]        = '�����ɱһ��߷���';
$HcomCost[$HcomUbase]        = 3000;
$HcomName[$Hcomteikou]        = '������ߤ�����';
$HcomCost[$Hcomteikou]        = 0;
$HcomName[$HcomTbase] = 'ST�ɱһ��߷���';
$HcomCost[$HcomTbase] = 1500;
$HcomName[$HcomHaribote]     = '�ϥ�ܥ�����';
$HcomCost[$HcomHaribote]     = 1;
$HcomName[$HcomMonument]     = '��ǰ���¤';
$HcomCost[$HcomMonument]     = 9999;
$HcomName[$HcomMissileNM]    = '�ߥ�����ȯ��';
$HcomCost[$HcomMissileNM]    = 20;
$HcomName[$HcomMissilePP]    = 'PP�ߥ�����ȯ��';
$HcomCost[$HcomMissilePP]    = 50;
$HcomName[$HcomMissileST]    = 'ST�ߥ�����ȯ��';
$HcomCost[$HcomMissileST]    = 50;
$HcomName[$HcomMissileLD]    = 'Φ���˲���ȯ��';
$HcomCost[$HcomMissileLD]    = 100;
$HcomName[$HcomMissileRE]        = 'Φ��������ȯ��';
$HcomCost[$HcomMissileRE]        = 150;
$HcomName[$HcomMissileMK]        = '����������ȯ��';
$HcomCost[$HcomMissileMK]        = 50;
$HcomName[$HcomMissileUC]        = '�˥ߥ�����ȯ��';
$HcomCost[$HcomMissileUC]        = 5000;
$HcomName[$HcomMissileNEB]        = '�����ҥߥ�����ȯ��';
$HcomCost[$HcomMissileNEB]        = 4000;
$HcomName[$HcomMissileEM]        = '�ʰץߥ�����ȯ��';
$HcomCost[$HcomMissileEM]        = 10;
$HcomName[$HcomMissileNC] = '�����٥ߥ�����ȯ��';
$HcomCost[$HcomMissileNC] = 15;
$HcomName[$HcomMissileHP] = '���������ߥ�����ȯ��';
$HcomCost[$HcomMissileHP] = 50;
$HcomName[$HcomMissileUB] = '�����������ɥߥ�����ȯ��';
$HcomCost[$HcomMissileUB] = 500;
$HcomName[$HcomSendMonster]  = '�����ɸ�';
$HcomCost[$HcomSendMonster]  = 3000;
$HcomName[$HcomSendMonster2]  = 'Ŵ��ʼ�ɸ�';
$HcomCost[$HcomSendMonster2]  = 2000;
$HcomName[$HcomSendMonster3]  = '�ù������ɸ�';
$HcomCost[$HcomSendMonster3]  = 5000;
$HcomName[$HcomSendMonster4]  = 'FX-330�ɸ�';
$HcomCost[$HcomSendMonster4]  = 7000;
$HcomName[$HcomSendMonster5]  = 'FX-330A�ɸ�';
$HcomCost[$HcomSendMonster5]  = 20000;
$HcomName[$Hcomtaifuu]   = '�������';
$HcomCost[$Hcomtaifuu]   = 2500;
$HcomName[$Hcomtunami]  = '����Ͷ��';
$HcomCost[$Hcomtunami]  = 3000;
$HcomName[$Hcomfunka] = 'ʮ��Ͷ��';
$HcomCost[$Hcomfunka] = 3000;
$HcomName[$Hcominseki]   = '��о���';
$HcomCost[$Hcominseki]   = 5000;
$HcomName[$Hcomdaiinseki]   = '����о���';
$HcomCost[$Hcomdaiinseki]   = 9000;
$HcomName[$Hcomjisin]   = '�Ͽ�Ͷ��';
$HcomCost[$Hcomjisin]   = 6000;
$HcomName[$Hcomkasai]   = '�к�Ͷ��';
$HcomCost[$Hcomkasai]   = 3000;
$HcomName[$Hcomtimya]   = '��̮��ưͶ��';
$HcomCost[$Hcomtimya]   = 7000;
$HcomName[$HcomRazer]   = '�졼����ȯ��';
$HcomCost[$HcomRazer]   = 1000;
$HcomName[$HcomPMS]   = '���ƥ饤��PMSˤȯ��';
$HcomCost[$HcomPMS]   = 3000;
$HcomName[$Hcomjibantinka]   = '��������Ͷ��';
$HcomCost[$Hcomjibantinka]   = 10000;
$HcomName[$HcomOoame]   = '�籫Ͷ��';
$HcomCost[$HcomOoame]   = 500;
$HcomName[$HcomDoNothing]    = '��ⷫ��';
$HcomCost[$HcomDoNothing]    = 0;
$HcomName[$HcomSell]         = '����͢��';
$HcomCost[$HcomSell]         = -100;
$HcomName[$HcomOilSell]         = '����͢��';
$HcomCost[$HcomOilSell]         = 10;
$HcomName[$HcomMoney]        = '�����';
$HcomCost[$HcomMoney]        = 100;
$HcomName[$HcomMoneyH]        = 'ST�����';
$HcomCost[$HcomMoneyH]        = 100;
$HcomName[$HcomImport]         = '����͢��';
$HcomCost[$HcomImport]         = 100;
$HcomName[$HcomOilImport]         = '����͢��';
$HcomCost[$HcomOilImport]         = 10;
$HcomName[$HcomFood]         = '�������';
$HcomCost[$HcomFood]         = -100;
$HcomName[$HcomFoodH]         = 'ST�������';
$HcomCost[$HcomFoodH]         = -100;
$HcomName[$HcomOil]         = '�������';
$HcomCost[$HcomOil]         = 10;
$HcomName[$HcomOilH]         = 'ST�������';
$HcomCost[$HcomOilH]         = 10;
$HcomName[$HcomSlag]         = '����͢��';
$HcomCost[$HcomSlag]         = -1;
$HcomName[$HcomPropaganda]   = 'Ͷ�׳�ư';
$HcomCost[$HcomPropaganda]   = 1000;
$HcomName[$HcomGeki]         = '���÷���';
$HcomCost[$HcomGeki]         = 1000;
$HcomName[$HcomShakufi]         = '���ڤ�����(10��ʧ��)';
$HcomCost[$HcomShakufi]         = 0;
$HcomName[$HcomShakuse]   = '���ڤ�����(50��ʧ��)';
$HcomCost[$HcomShakuse]   = 0;
$HcomName[$HcomShakuth]         = '���ڤ�����(100��ʧ��)';
$HcomCost[$HcomShakuth]         = 0;
$HcomName[$HcomRob]          = '��å';
$HcomCost[$HcomRob]          = 100;
$HcomName[$HcomRobST]          = 'ST��å';
$HcomCost[$HcomRobST]          = 200;
$HcomName[$Hcomkouei]  = '��������Ǥ��夲';
$HcomCost[$Hcomkouei]  = 3000;
$HcomName[$Hcomkanei] = '�ƻ�����Ǥ��夲';
$HcomCost[$Hcomkanei] = 4000;
$HcomName[$Hcomkouuti]   = '������������Ȥ�';
$HcomCost[$Hcomkouuti]   = 1000;
$HcomName[$Hcomkanuti]   = '�ƻ���������Ȥ�';
$HcomCost[$Hcomkanuti]   = 1000;
$HcomName[$Hcombouei] = '�ɸ�����Ǥ��夲';
$HcomCost[$Hcombouei] = 10000;
$HcomName[$Hcombouuti]   = '�ɸ���������Ȥ�';
$HcomCost[$Hcombouuti]   = 1000;
$HcomName[$Hcomreiei] = '�졼���������Ǥ��夲';
$HcomCost[$Hcomreiei] = 10000;
$HcomName[$Hcomreiuti]   = '�졼�������������Ȥ�';
$HcomCost[$Hcomreiuti]   = 1000;
$HcomName[$Hcomhatei] = 'ȯ�ű����Ǥ��夲';
$HcomCost[$Hcomhatei] = 10000;
$HcomName[$Hcomhatuti]   = 'ȯ�ű��������Ȥ�';
$HcomCost[$Hcomhatuti]   = 1000;
$HcomName[$HcomPMSei] = 'PMS��������';
$HcomCost[$HcomPMSei] = 20000;
$HcomName[$HcomPMSuti]   = 'PMS���������Ȥ�';
$HcomCost[$HcomPMSuti]   = 1000;
$HcomName[$Hcomsennyu]   = '���谦��Ʊ���˲���';
$HcomCost[$Hcomsennyu]   = 1;
$HcomName[$Hcomheinyu]   = 'ʿ�°���Ʊ���˲���';
$HcomCost[$Hcomheinyu]   = 1;
$HcomName[$Hcominonyu]  = 'ȿ���Τ�Ʊ���˲���';
$HcomCost[$Hcominonyu]  = 1;
$HcomName[$Hcomsende] = '���谦��Ʊ������æ��';
$HcomCost[$Hcomsende] = 1;
$HcomName[$Hcomheide]   = 'ʿ�°���Ʊ������æ��';
$HcomCost[$Hcomheide]   = 1;
$HcomName[$Hcominode]   = 'ȿ���Τ�Ʊ������æ��';
$HcomCost[$Hcominode]   = 1;
$HcomName[$Hcomteiko]   = '��񷳤˻���';
$HcomCost[$Hcomteiko]   = 0;
$HcomName[$Hcomkyouko]   = '���¹񷳤˻���';
$HcomCost[$Hcomkyouko]   = 0;
$HcomName[$HcomGiveup]       = '�������';
$HcomCost[$HcomGiveup]       = 0;
$HcomName[$HcomAutoPrepare]  = '���ϼ�ư����';
$HcomCost[$HcomAutoPrepare]  = 0;
$HcomName[$HcomAutoPrepare2] = '�Ϥʤ餷��ư����';
$HcomCost[$HcomAutoPrepare2] = 0;
$HcomName[$HcomReclaim2]   = '�������Ω�Ƽ�ư����';
$HcomCost[$HcomReclaim2]   = 0;
$HcomName[$HcomReclaim3]   = '�����ʹ����Ω�Ƽ�ư����';
$HcomCost[$HcomReclaim3]   = 0;
$HcomName[$HcomAutoDelete]   = '���ײ�����ű��';
$HcomCost[$HcomAutoDelete]   = 0;

#----------------------------------------------------------------------
# �ѿ�
#----------------------------------------------------------------------

# COOKIE
my($defaultID);       # ���̾��
my($defaultTarget);   # �������åȤ�̾��


# ��κ�ɸ��
$HpointNumber = $HislandSize * $HislandSize;

#----------------------------------------------------------------------
# �ᥤ��
#----------------------------------------------------------------------

# jcode.pl��require
require($jcode);

# �����ץ��
$HtempBack = "<A HREF=\"$HthisFile\">${HtagBig_}�ȥåפ����${H_tagBig}</A>";

# ��å��򤫤���
if(!hakolock()) {
    # ��å�����
    # �إå�����
    tempHeader();

    # ��å����ԥ�å�����
    tempLockFail();

    # �եå�����
    tempFooter();

    # ��λ
    exit(0);
}

# ����ν����
srand(time^$$);

# COOKIE�ɤߤ���
cookieInput();

# CGI�ɤߤ���
cgiInput();

# ��ǡ������ɤߤ���
if(readIslandsFile($HcurrentID) == 0) {
    unlock();
    tempHeader();
    tempNoDataFile();
    tempFooter();
    exit(0);
}

# �ƥ�ץ졼�Ȥ�����
tempInitialize();

# COOKIE����
cookieOutput();

if($HmainMode eq 'owner') {

    # ��ȯ�⡼��
if($Hnmo == 0){
    require('hako-map.cgi');
tempHeaderB();
    ownerMain();
}else{
    require('hako-map.cgi');
tempHeader();
    ownerMain();
}
}elsif($HmainMode eq 'ownerb') {
if($Hnmo == 0){
    require('hako-map.cgi');
tempHeaderB();
    ownerMainb();
}else{
    require('hako-map.cgi');
tempHeader();
    ownerMainb();
}
}else{
# �إå�����
tempHeader();

if($HmainMode eq 'turn') {
    # ������ʹ�
    require('hako-turn.cgi');
    require('hako-top.cgi');
    turnMain();

} elsif($HmainMode eq 'new') {
    # ��ο�������
    require('hako-turn.cgi');
    require('hako-map.cgi');
    newIslandMain();

} elsif($HmainMode eq 'print') {
    # �Ѹ��⡼��
    require('hako-map.cgi');
    printIslandMain();


} elsif($HmainMode eq 'command') {
    # ���ޥ�����ϥ⡼��
    require('hako-map.cgi');
    commandMain();
} elsif($HmainMode eq 'Shuu') {
    # ���ޥ�����ϥ⡼��
    require('hako-map.cgi');
    ShuuMain();
} elsif($HmainMode eq 'comment') {
    # ���������ϥ⡼��
    require('hako-map.cgi');
    commentMain();

} elsif($HmainMode eq 'lbbs') {

    # ������Ǽ��ĥ⡼��
    require('hako-map.cgi');
    localBbsMain();

} elsif($HmainMode eq 'change') {
    # �����ѹ��⡼��
    require('hako-turn.cgi');
    require('hako-top.cgi');
    changeMain();

} elsif($HmainMode eq 'chowner') {
  # �����ʡ�̾�ѹ��⡼��
  require('hako-turn.cgi');
  require('hako-top.cgi');
  changeOwner();

} elsif($HmainMode eq 'chflag') {
  # �����ʡ�̾�ѹ��⡼��
  require('hako-turn.cgi');
  require('hako-top.cgi');
  changeFlag();

} else {
    # ����¾�ξ��ϥȥåץڡ����⡼��
    require('hako-top.cgi');
    topPageMain();
}
}
# �եå�����
tempFooter();

# ��λ
exit(0);

# ���ޥ�ɤ����ˤ��餹
sub slideFront {
    my($command, $number) = @_;
    my($i);

    # ���줾�줺�餹
    splice(@$command, $number, 1);

    # �Ǹ�˻�ⷫ��
    $command->[$HcommandMax - 1] = {
	'kind' => $HcomDoNothing,
	'target' => 0,
	'x' => 0,
	'y' => 0,
	'arg' => 0
	};
}

# ���ޥ�ɤ��ˤ��餹
sub slideBack {
    my($command, $number) = @_;
    my($i);

    # ���줾�줺�餹
    return if $number == $#$command;
    pop(@$command);
    splice(@$command, $number, 0, $command->[$number]);
}

#----------------------------------------------------------------------
# ��ǡ���������
#----------------------------------------------------------------------

# ����ǡ����ɤߤ���
sub readIslandsFile {
    my($num) = @_; # 0�����Ϸ��ɤߤ��ޤ�
                   # -1�������Ϸ����ɤ�
                   # �ֹ���Ȥ�������Ϸ��������ɤߤ���

    # �ǡ����ե�����򳫤�
    if(!open(IN, "${HdirName}/hakojima.dat")) {
	rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");
	if(!open(IN, "${HdirName}/hakojima.dat")) {
if(!open(IN, "${HdirName1}/hakojima.dat")) {
	    return 0;
}
	}
    }
    if(!open(OIN, "${HdirName2}/hflag.dat")) {
	rename("${HdirName2}/hflag.tmp", "${HdirName2}/hflag.dat");
	if(!open(OIN, "${HdirName2}/hflag.dat")) {
	if(!open(OIN, "${HdirName1}/hflag.dat")) {
	    return 0;
}
	}
    }
    if(!open(FIN, "${HdirName2}/howner.dat")) {
	rename("${HdirName2}/howner.tmp", "${HdirName2}/howner.dat");
	if(!open(FIN, "${HdirName2}/howner.dat")) {
	if(!open(FIN, "${HdirName1}/howner.dat")) {
	    return 0;
}
	}
    }
    if(!open(GIN, "${HdirName2}/haddre.dat")) {
	rename("${HdirName2}/haddre.tmp", "${HdirName2}/haddre.dat");
	if(!open(GIN, "${HdirName2}/haddre.dat")) {
	if(!open(GIN, "${HdirName1}/haddre.dat")) {
	    return 0;
}
	}
    }
    if(!open(SIN, "${HdirName2}/hkanko.dat")) {
	rename("${HdirName2}/hkanko.tmp", "${HdirName2}/hkanko.dat");
	if(!open(SIN, "${HdirName2}/hkanko.dat")) {
	if(!open(SIN, "${HdirName1}/hkanko.dat")) {
	    return 0;
	}
    }
}
    if(!open(YIN, "${HdirName}/hprize.dat")) {
	rename("${HdirName}/hprize.tmp", "${HdirName}/hprize.dat");
	if(!open(YIN, "${HdirName}/hprize.dat")) {
	if(!open(YIN, "${HdirName1}/hprize.dat")) {
	    return 0;
}
	}
    }
    if(!open(XIN, "${HdirName}/heisei.dat")) {
	rename("${HdirName}/heiseil.tmp", "${HdirName}/heisei.dat");
	if(!open(XIN, "${HdirName}/heisei.dat")) {
if(!open(XIN, "${HdirName1}/heisei.dat")) {
	    return 0;
}
	}
    }
    if(!open(ZIN, "${HdirName}/hshoyu.dat")) {
	rename("${HdirName}/hshoyu.tmp", "${HdirName}/hshoyu.dat");
	if(!open(ZIN, "${HdirName}/hshoyu.dat")) {
	if(!open(ZIN, "${HdirName1}/hshoyu.dat")) {
	    return 0;
}
	}
    }
     if(!open(UIN, "${HdirName}/hsonota.dat")) {
	rename("${HdirName}/hsonota.tmp", "${HdirName}/hsonota.dat");
	if(!open(UIN, "${HdirName}/hsonota.dat")) {
	if(!open(UIN, "${HdirName1}/hsonota.dat")) {
	    return 0;
}
	}
    }
    if(!open(VIN, "${HdirName}/hpara.dat")) {
	rename("${HdirName}/hpara.tmp", "${HdirName}/hpara.dat");
	if(!open(VIN, "${HdirName}/hpara.dat")) {
	if(!open(VIN, "${HdirName1}/hpara.dat")) {
	    return 0;
}
	}
    }
    if(!open(AIN, "${HdirName}/hpase.dat")) {
	rename("${HdirName}/hpase.tmp", "${HdirName}/hpase.dat");
	if(!open(AIN, "${HdirName}/hpase.dat")) {
	if(!open(AIN, "${HdirName1}/hpase.dat")) {
	    return 0;
}
	}
    }
    # �ƥѥ�᡼�����ɤߤ���
    $HislandTurn = int(<IN>); # �������
    if($HislandTurn == 0) {
	return 0;
    }
    $HislandLastTime = int(<IN>); # �ǽ���������
    if($HislandLastTime == 0) {
	return 0;
    }
    $HislandNumber   = int(<IN>); 
    $HislandNextID   = int(<IN>); # ���˳�����Ƥ�ID
    $jooa   = int(<YIN>); 
    $joou  = <YIN>; 
 chomp($joou);
    $hooa   = int(<YIN>); 
    $hoou  = <YIN>; 
 chomp($hoou);
    $gooa   = int(<YIN>); 
    $goou  = <YIN>; 
 chomp($goou);
    $sooa   = int(<YIN>); 
    $soou  = <YIN>; 
 chomp($soou);
    $looa   = int(<YIN>); 
    $loou  = <YIN>; 
 chomp($loou);
    $yooa   = int(<YIN>); 
    $yoou  = <YIN>; 
 chomp($yoou);
    $eooa   = int(<YIN>); 
    $eoou  = <YIN>; 
 chomp($eoou);
    $aooa   = int(<YIN>); 
    $aoou  = <YIN>; 
 chomp($aoou);
    $iooa   = int(<YIN>); 
    $ioou  = <YIN>; 
 chomp($ioou);
    $booa   = int(<YIN>); 
    $biou  = <YIN>; 
 chomp($biou);
    $uooa   = int(<YIN>); 
    $uoou  = <YIN>; 
 chomp($uoou);
    $fioa   = int(<YIN>); 
    $foou  = <YIN>; 
 chomp($foou);
    $tioa   = int(<YIN>); 
    $toou  = <YIN>; 
 chomp($toou);
   $nioa   = int(<YIN>); 
    $niou   = <YIN>; 
 chomp($niou);
    $kioa   = int(<YIN>); 
    $kiou  = <YIN>; 
 chomp($kiou);
   $oioa  = int(<YIN>); 
    $oiou = <YIN>; 
 chomp($oiou);
    $dioa   = int(<YIN>); 
    $diou   = <YIN>; 
 chomp($diou);
    $deoa   = int(<YIN>); 
    $deou  = <YIN>; 
 chomp($deou);
    $mooa   = int(<YIN>); 
    $moou  = <YIN>; 
 chomp($moou);
  $sek   = int(<XIN>); 
    $seu  = <XIN>; 
 chomp($seu);
    $hek   = int(<XIN>); 
    $heu   = <XIN>; 
 chomp($heu);
    $ink   = int(<XIN>); 
    $inu  = <XIN>; 
 chomp($inu);
   $tei   = int(<ZIN>); 
    $teu  = <ZIN>; 
 chomp($teu);
    $kyo   = int(<ZIN>); 
    $kyu   = <ZIN>; 
 chomp($kyu);
    $muo   = int(<ZIN>); 
    $muu  = <ZIN>; 
 chomp($muu);
$HdisEarthquake   = int(<UIN>); 
$HdisTsunami   = int(<UIN>); 
$HdisTyphoon   = int(<UIN>); 
$HdisMeteo   = int(<UIN>); 
$HdisHugeMeteo   = int(<UIN>); 
$HdisEruption   = int(<UIN>); 
$HdisFire   = int(<UIN>); 
$HdisMonster   = int(<UIN>); 
$HdisDisa   = int(<UIN>); 
$HdisHardRain= int(<UIN>);

   # ���������Ƚ��
    my($now) = time;
    if((($Hdebug == 1) && 
	($HmainMode eq 'Hdebugturn')) ||
       (($now - $HislandLastTime) >= $HunitTime)) {
	$HmainMode = 'turn';
	$num = -1; 
    }

    # ����ɤߤ���
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	 $Hislands[$i] = readIsland($num);
	 $HidToNumber{$Hislands[$i]->{'id'}} = $i;
    }

    # �ե�������Ĥ���
    close(IN);

    return 1;
}

# ��ҤȤ��ɤߤ���
sub readIsland {
    my($num) = @_;
    my($name, $id, $prize, $absent, $comment, $password, $money, $food,
       $pop, $area, $farm, $factory, $mountain, $birth, $score, $monsnumber,
       $kouei, $kanei, $sen, $hei, $ino);
    $name = <IN>;		# ���̾��,�礬�������줿������
    chomp($name);
    $name =~ s/,(.*)$//g;	# -���̾��
    $birth = int($1);		# -�礬�������줿������
    $id = int(<IN>);		# ID�ֹ�
    $prize = <IN>;		# ����
    chomp($prize);
    $absent = int(<IN>);	# Ϣ³��ⷫ���
    $comment = <IN>;		# ������
    chomp($comment);
    $password = <IN>;		# �Ź沽�ѥ����
    chomp($password);
    $money = int(<IN>);		# ���
    $food = int(<IN>);		# ����
    $pop = int(<IN>);		# �͸�
    $area = int(<IN>);		# ����
    $farm = int(<IN>);		# ����
    $factory = int(<IN>);	# ����
    $mountain = int(<IN>);	# �η���
   $id1= int(<OIN>);
 $flagname = <OIN>;
chomp($flagname);
$id2= int(<FIN>);
$ownername = <FIN>;
chomp($ownername);
$id3= int(<GIN>);
$ADDRE = <GIN>; 
chomp($ADDRE);
$id4= int(<SIN>);
$kanko = int(<SIN>);
$id5= int(<YIN>);
$monsnumber = <YIN>;
chomp($monsnumber);
$monka = int(<YIN>);
$top = int(<YIN>);
$emp = int(<YIN>);
$id6= int(<XIN>);
$kouei = int(<XIN>);
$kanei = int(<XIN>);
$bouei = int(<XIN>);
$reiei = int(<XIN>);
$hatei = int(<XIN>);
$pmsi = int(<XIN>);
  $id7= int(<ZIN>);
$yousho = int(<ZIN>);
$Jous = int(<ZIN>);
  $hatud = int(<ZIN>);
  $gomi = int(<ZIN>);
  $slag= int(<ZIN>);
  $shoku= int(<ZIN>);
$sigoto= int(<ZIN>);
$oil= int(<ZIN>);
$boku= int(<ZIN>);
  $id8= int(<UIN>);
$sen = int(<UIN>);
$hei = int(<UIN>);
$ino = int(<UIN>);
$teikou= int(<UIN>);
  $score = int(<UIN>);
  $shaka = int(<UIN>);
  $shamo= int(<UIN>);
$shuu= int(<UIN>);
$yhuu= int(<UIN>);
$id9= int(<VIN>);
$koukyo= int(<VIN>);
$hatuden= int(<VIN>);
$nougyo= int(<VIN>);
$kouzan= int(<VIN>);
$koujyou= int(<VIN>);
$gunji= int(<VIN>);
$tokushu= int(<VIN>);
$koutuu= int(<VIN>);
$sonota= int(<VIN>);
$id10= int(<AIN>);
$koukpase= int(<AIN>);
$hatupase= int(<AIN>);
$noupase= int(<AIN>);
$kouzpase= int(<AIN>);
$koujpase= int(<AIN>);
$gunpase= int(<AIN>);
$tokupase= int(<AIN>);
$koutpase= int(<AIN>);
$sonopase= int(<AIN>);
# HidToName�ơ��֥����¸
    $HidToName{$id} = $name;	# 

    # �Ϸ�
    my(@land, @landValue, $line, @command, @lbbs);

    if(($num == -1) || ($num == $id)) {
	if(!open(IIN, "${HdirName}/island.$id")) {
	    rename("${HdirName}/islandtmp.$id", "${HdirName}/island.$id");
	    if(!open(IIN, "${HdirName}/island.$id")) {
	    if(!open(IIN, "${HdirName1}/island.$id")) {
		exit(0);
}
	    }
	}
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
	    $line = <IIN>;
	    for($x = 0; $x < $HislandSize; $x++) {
		$line =~ s/^(..)(..)//;
		$land[$x][$y] = hex($1);
		$landValue[$x][$y] = hex($2);
	    }
	}

	# ���ޥ��
	my($i);
	for($i = 0; $i < $HcommandMax; $i++) {
	    $line = <IIN>;
	    $line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*)$/;
	    $command[$i] = {
		'kind' => int($1),
		'target' => int($2),
		'x' => int($3),
		'y' => int($4),
		'arg' => int($5)
		}
	}

	# ������Ǽ���
	for($i = 0; $i < $HlbbsMax; $i++) {
	    $line = <IIN>;
	    chomp($line);
	    $lbbs[$i] = $line;
	}

	close(IIN);
    }

    # �緿�ˤ����֤�
    return {
	 'name' => $name,
	 'id' => $id,
	 'birth' => $birth,
	 'prize' => $prize,
	 'absent' => $absent,
	 'comment' => $comment,
	 'password' => $password,
	 'money' => $money,
	 'food' => $food,
	 'pop' => $pop,
	 'area' => $area,
	 'farm' => $farm,
	 'factory' => $factory,
	 'mountain' => $mountain,
         'score' => $score,
	 'land' => \@land,
	 'landValue' => \@landValue,
	 'command' => \@command,
	 'lbbs' => \@lbbs,
'monsnumber' => $monsnumber, 
'kouei' => $kouei,
'kanei' => $kanei,
'sen' => $sen, 
'hei' => $hei,
'ino' => $ino,
'kanko' => $kanko,
'yousho' => $yousho,
'monka' => $monka,
'teikou'=> $teikou,
'ADDRE'=> $ADDRE,
'bouei' => $bouei,
'reiei' => $reiei,
'Jous' => $Jous,
'ownername' => $ownername,
'flagname' => $flagname,
'top' => $top,
'hatei' => $hatei,
'hatud' => $hatud,
'gomi' => $gomi,
'shaka' => $shaka,
'shamo' => $shamo,
'slag' => $slag,
'shoku' => $shoku,
'sigoto' => $sigoto,
'oil' => $oil,
'boku' => $boku,
'shuu' => $shuu,
'yhuu' => $yhuu,
'empe' => $emp,
'pmsei' => $pmsi,
'koukyo' => $koukyo,
'hatuden' => $hatuden,
'nougyo' => $nougyo,
'kouzan' => $kouzan,
'koujyou' => $koujyou,
'gunji' => $gunji,
'tokushu' => $tokushu,
'koutuu' => $koutuu,
'sonota' => $sonota,
'koukpase' => $koukpase,
'hatupase' => $hatupase,
'noupase' => $noupase,
'kouzpase' => $kouzpase,
'koujpase' => $koujpase,
'gunpase' => $gunpase,
'tokupase' => $tokupase,
'koutpase' => $koutpase,
'sonopase' => $sonopase,
};
}
# ����ǡ����񤭹���
sub writeIslandsFile {
    my($num) = @_;

    # �ե�����򳫤�
    my($retry) = $HretryCount;
    while (! open(OUT, ">${HdirName}/hakojima.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 ����Ū�˽�λ�����ޤ�
	    return 1;
	}

	# 0.2 �� sleep
	select undef, undef, undef, 0.2;
    }
   while (! open(MOUT, ">${HdirName2}/hflag.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 ����Ū�˽�λ�����ޤ�
	    return 1;
	}

	# 0.2 �� sleep
	select undef, undef, undef, 0.2;
    }
   while (! open(HOUT, ">${HdirName2}/howner.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 ����Ū�˽�λ�����ޤ�
	    return 1;
	}

	# 0.2 �� sleep
	select undef, undef, undef, 0.2;
    }
   while (! open(GOUT, ">${HdirName2}/haddre.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 ����Ū�˽�λ�����ޤ�
	    return 1;
	}

	# 0.2 �� sleep
	select undef, undef, undef, 0.2;
    }
   while (! open(SOUT, ">${HdirName2}/hkanko.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 ����Ū�˽�λ�����ޤ�
	    return 1;
	}

	# 0.2 �� sleep
	select undef, undef, undef, 0.2;
    }

    while (! open(BOUT, ">${HdirName}/hprize.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 ����Ū�˽�λ�����ޤ�
	    return 1;
	}

	# 0.2 �� sleep
	select undef, undef, undef, 0.2;
    }
    while (! open(COUT, ">${HdirName}/heisei.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 ����Ū�˽�λ�����ޤ�
	    return 1;
	}

	# 0.2 �� sleep
	select undef, undef, undef, 0.2;
    }
    while (! open(DOUT, ">${HdirName}/hshoyu.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 ����Ū�˽�λ�����ޤ�
	    return 1;
	}

	# 0.2 �� sleep
	select undef, undef, undef, 0.2;
    }
    while (! open(EOUT, ">${HdirName}/hsonota.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 ����Ū�˽�λ�����ޤ�
	    return 1;
	}

	# 0.2 �� sleep
	select undef, undef, undef, 0.2;
    }
   while (! open(FOUT, ">${HdirName}/hpara.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 ����Ū�˽�λ�����ޤ�
	    return 1;
	}

	# 0.2 �� sleep
	select undef, undef, undef, 0.2;
    }
   while (! open(TOUT, ">${HdirName}/hpase.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 ����Ū�˽�λ�����ޤ�
	    return 1;
	}

	# 0.2 �� sleep
	select undef, undef, undef, 0.2;
    }
    # �ƥѥ�᡼���񤭹���
    print OUT "$HislandTurn\n";
    print OUT "$HislandLastTime\n";
    print OUT "$HislandNumber\n";
    print OUT "$HislandNextID\n";
    print BOUT "$jooa\n";
    print BOUT "$joou\n";
    print BOUT "$hooa\n";
    print BOUT "$hoou\n";
    print BOUT "$gooa\n";
    print BOUT "$goou\n";
    print BOUT "$sooa\n";
    print BOUT "$soou\n";
    print BOUT "$looa\n";
    print BOUT "$loou\n";
    print BOUT "$yooa\n";
    print BOUT "$yoou\n";
    print BOUT "$eooa\n";
    print BOUT "$eoou\n";
    print BOUT "$aooa\n";
    print BOUT "$aoou\n";
    print BOUT "$iooa\n";
    print BOUT "$ioou\n";
    print BOUT "$booa\n";
    print BOUT "$biou\n";
    print BOUT "$uooa\n";
    print BOUT "$uoou\n";
    print BOUT "$fioa\n";
    print BOUT "$foou\n";
    print BOUT "$tioa\n";
    print BOUT "$toou\n";
    print BOUT "$nioa\n";
    print BOUT "$niou\n";
    print BOUT "$kioa\n";
    print BOUT "$kiou\n";
    print BOUT "$oioa\n";
    print BOUT "$oiou\n";
    print BOUT "$dioa\n";
    print BOUT "$diou\n";
    print BOUT "$deoa\n";
    print BOUT "$deou\n";
    print BOUT "$mooa\n";
    print BOUT "$moou\n";
   print COUT "$sek\n";
    print COUT "$seu\n";
    print COUT "$hek\n";
    print COUT "$heu\n";
    print COUT "$ink\n";
    print COUT "$inu\n";
    print DOUT "$tei\n";
    print DOUT "$teu\n";
    print DOUT "$kyo\n";
    print DOUT "$kyu\n";
    print DOUT "$muo\n";
    print DOUT "$muu\n";
    print EOUT "$HdisEarthquake\n";
    print EOUT "$HdisTsunami\n";
    print EOUT "$HdisTyphoon\n";
    print EOUT "$HdisMeteo\n";
    print EOUT "$HdisHugeMeteo\n";
    print EOUT "$HdisEruption\n";
    print EOUT "$HdisFire\n";
    print EOUT "$HdisMonster\n";
print EOUT "$HdisDisa\n";
print EOUT "$HdisHardRain\n";
     # ��ν񤭤���
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	 writeIsland($Hislands[$i], $num);
    }

    # �ե�������Ĥ���
   close(OUT);
close(MOUT);
close(HOUT);
close(GOUT);
close(BOUT);
close(SOUT);
close(COUT);
close(DOUT);
close(EOUT);
close(FOUT);
close(TOUT);
    # �����̾���ˤ���
    unlink("${HdirName}/hakojima.dat");
    rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");
 unlink("${HdirName2}/hflag.dat");
  rename("${HdirName2}/hflag.tmp", "${HdirName2}/hflag.dat");
unlink("${HdirName2}/howner.dat");
  rename("${HdirName2}/howner.tmp", "${HdirName2}/howner.dat");
  unlink("${HdirName2}/haddre.dat");
  rename("${HdirName2}/haddre.tmp", "${HdirName2}/haddre.dat");
  unlink("${HdirName2}/hkanko.dat");
  rename("${HdirName2}/hkanko.tmp", "${HdirName2}/hkanko.dat");
  unlink("${HdirName}/hprize.dat");
  rename("${HdirName}/hprize.tmp", "${HdirName}/hprize.dat");
  unlink("${HdirName}/heisei.dat");
  rename("${HdirName}/heisei.tmp", "${HdirName}/heisei.dat");
  unlink("${HdirName}/hshoyu.dat");
  rename("${HdirName}/hshoyu.tmp", "${HdirName}/hshoyu.dat");
  unlink("${HdirName}/hsonota.dat");
  rename("${HdirName}/hsonota.tmp", "${HdirName}/hsonota.dat");
 unlink("${HdirName}/hpara.dat");
  rename("${HdirName}/hpara.tmp", "${HdirName}/hpara.dat");
 unlink("${HdirName}/hpase.dat");
  rename("${HdirName}/hpase.tmp", "${HdirName}/hpase.dat");
}
sub writeFile {
    my($num) = @_;

    # �ե�����򳫤�
open(OUT, ">${HdirName1}/hakojima.tmp");
open(MOUT, ">${HdirName1}/hflag.tmp");
open(HOUT, ">${HdirName1}/howner.tmp");
open(GOUT, ">${HdirName1}/haddre.tmp");
open(SOUT, ">${HdirName1}/hkanko.tmp");
open(BOUT, ">${HdirName1}/hprize.tmp");
open(COUT, ">${HdirName1}/heisei.tmp");
open(DOUT, ">${HdirName1}/hshoyu.tmp");
open(EOUT, ">${HdirName1}/hsonota.tmp");
open(FOUT, ">${HdirName1}/hpara.tmp");
open(TOUT, ">${HdirName1}/hpase.tmp");
    # �ƥѥ�᡼���񤭹���
    print OUT "$HislandTurn\n";
    print OUT "$HislandLastTime\n";
    print OUT "$HislandNumber\n";
    print OUT "$HislandNextID\n";
    print BOUT "$jooa\n";
    print BOUT "$joou\n";
    print BOUT "$hooa\n";
    print BOUT "$hoou\n";
    print BOUT "$gooa\n";
    print BOUT "$goou\n";
    print BOUT "$sooa\n";
    print BOUT "$soou\n";
    print BOUT "$looa\n";
    print BOUT "$loou\n";
    print BOUT "$yooa\n";
    print BOUT "$yoou\n";
    print BOUT "$eooa\n";
    print BOUT "$eoou\n";
    print BOUT "$aooa\n";
    print BOUT "$aoou\n";
    print BOUT "$iooa\n";
    print BOUT "$ioou\n";
    print BOUT "$booa\n";
    print BOUT "$biou\n";
    print BOUT "$uooa\n";
    print BOUT "$uoou\n";
    print BOUT "$fioa\n";
    print BOUT "$foou\n";
    print BOUT "$tioa\n";
    print BOUT "$toou\n";
    print BOUT "$nioa\n";
    print BOUT "$niou\n";
    print BOUT "$kioa\n";
    print BOUT "$kiou\n";
    print BOUT "$oioa\n";
    print BOUT "$oiou\n";
    print BOUT "$dioa\n";
    print BOUT "$diou\n";
    print BOUT "$deoa\n";
    print BOUT "$deou\n";
    print BOUT "$mooa\n";
    print BOUT "$moou\n";
   print COUT "$sek\n";
    print COUT "$seu\n";
    print COUT "$hek\n";
    print COUT "$heu\n";
    print COUT "$ink\n";
    print COUT "$inu\n";
    print DOUT "$tei\n";
    print DOUT "$teu\n";
    print DOUT "$kyo\n";
    print DOUT "$kyu\n";
    print DOUT "$muo\n";
    print DOUT "$muu\n";
    print EOUT "$HdisEarthquake\n";
    print EOUT "$HdisTsunami\n";
    print EOUT "$HdisTyphoon\n";
    print EOUT "$HdisMeteo\n";
    print EOUT "$HdisHugeMeteo\n";
    print EOUT "$HdisEruption\n";
    print EOUT "$HdisFire\n";
    print EOUT "$HdisMonster\n";
print EOUT "$HdisDisa\n";
print EOUT "$HdisHardRain\n";
     # ��ν񤭤���
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	 writeIslands($Hislands[$i], $num);
    }

    # �ե�������Ĥ���
    close(OUT);
close(MOUT);
close(HOUT);
close(GOUT);
close(BOUT);
close(SOUT);
close(COUT);
close(DOUT);
close(EOUT);
close(FOUT);
close(TOUT);
    # �����̾���ˤ���
    unlink("${HdirName1}/hakojima.dat");
    rename("${HdirName1}/hakojima.tmp", "${HdirName1}/hakojima.dat");
  unlink("${HdirName1}/hflag.dat");
  rename("${HdirName1}/hflag.tmp", "${HdirName1}/hflag.dat");
unlink("${HdirName1}/howner.dat");
  rename("${HdirName1}/howner.tmp", "${HdirName1}/howner.dat");
  unlink("${HdirName1}/haddre.dat");
  rename("${HdirName1}/haddre.tmp", "${HdirName1}/haddre.dat");
  unlink("${HdirName1}/hkanko.dat");
  rename("${HdirName1}/hkanko.tmp", "${HdirName1}/hkanko.dat");
  unlink("${HdirName1}/hprize.dat");
  rename("${HdirName1}/hprize.tmp", "${HdirName1}/hprize.dat");
  unlink("${HdirName1}/heisei.dat");
  rename("${HdirName1}/heisei.tmp", "${HdirName1}/heisei.dat");
  unlink("${HdirName1}/hshoyu.dat");
  rename("${HdirName1}/hshoyu.tmp", "${HdirName1}/hshoyu.dat");
  unlink("${HdirName1}/hsonota.dat");
  rename("${HdirName1}/hsonota.tmp", "${HdirName1}/hsonota.dat");
 unlink("${HdirName1}/hpara.dat");
  rename("${HdirName1}/hpara.tmp", "${HdirName1}/hpara.dat");
 unlink("${HdirName1}/hpase.dat");
  rename("${HdirName1}/hpase.tmp", "${HdirName1}/hpase.dat");
}
# ��ҤȤĽ񤭹���
sub writeIsland {
    my($island, $num) = @_;
    my($birth);
    $birth = int($island->{'birth'});
    print OUT $island->{'name'} . ",$birth\n";
    print OUT $island->{'id'} . "\n";
    print OUT $island->{'prize'} . "\n";
    print OUT $island->{'absent'} . "\n";
    print OUT $island->{'comment'} . "\n";
    print OUT $island->{'password'} . "\n";
    print OUT $island->{'money'} . "\n";
    print OUT $island->{'food'} . "\n";
    print OUT $island->{'pop'} . "\n";
    print OUT $island->{'area'} . "\n";
    print OUT $island->{'farm'} . "\n";
    print OUT $island->{'factory'} . "\n";
    print OUT $island->{'mountain'} . "\n";
print MOUT $island->{'id'} . "\n";
print MOUT $island->{'flagname'} . "\n";
print HOUT $island->{'id'} . "\n";
print HOUT $island->{'ownername'} . "\n";
print GOUT $island->{'id'} . "\n";
print GOUT $island->{'ADDRE'} . "\n";
print SOUT $island->{'id'} . "\n";
print SOUT $island->{'kanko'} . "\n";
print BOUT $island->{'id'} . "\n";
print BOUT $island->{'monsnumber'} . "\n"; 
print BOUT $island->{'monka'} . "\n";
print BOUT $island->{'top'} . "\n";
print BOUT $island->{'empe'} . "\n";
print COUT $island->{'id'} . "\n";
print COUT $island->{'kouei'} . "\n";
print COUT $island->{'kanei'} . "\n"; 
print COUT $island->{'bouei'} . "\n";
print COUT $island->{'reiei'} . "\n";
print COUT $island->{'hatei'} . "\n";
print COUT $island->{'pmsei'} . "\n";
print DOUT $island->{'id'} . "\n";
print DOUT $island->{'yousho'} . "\n";
print DOUT $island->{'Jous'} . "\n";
print DOUT $island->{'hatud'} . "\n";
print DOUT $island->{'gomi'} . "\n";
print DOUT $island->{'slag'} . "\n";
print DOUT $island->{'shoku'} . "\n";
print DOUT $island->{'sigoto'} . "\n";
print DOUT $island->{'oil'} . "\n";
print DOUT $island->{'boku'} . "\n";
print EOUT $island->{'id'} . "\n";
print EOUT $island->{'sen'} . "\n"; 
print EOUT $island->{'hei'} . "\n";
print EOUT $island->{'ino'} . "\n";
print EOUT $island->{'teikou'} . "\n";
print EOUT $island->{'score'} . "\n";
print EOUT $island->{'shaka'} . "\n";
print EOUT $island->{'shamo'} . "\n";
print EOUT $island->{'shuu'} . "\n";
print EOUT $island->{'yhuu'} . "\n";
print FOUT $island->{'id'} . "\n";
print FOUT $island->{'koukyo'} . "\n";
print FOUT $island->{'hatuden'} . "\n";
print FOUT $island->{'nougyo'} . "\n";
print FOUT $island->{'kouzan'} . "\n";
print FOUT $island->{'koujyou'} . "\n";
print FOUT $island->{'gunji'} . "\n";
print FOUT $island->{'tokushu'} . "\n";
print FOUT $island->{'koutuu'} . "\n";
print FOUT $island->{'sonota'} . "\n";
print TOUT $island->{'id'} . "\n";
print TOUT $island->{'koukpase'} . "\n";
print TOUT $island->{'hatupase'} . "\n";
print TOUT $island->{'noupase'} . "\n";
print TOUT $island->{'kouzpase'} . "\n";
print TOUT $island->{'koujpase'} . "\n";
print TOUT $island->{'gunpase'} . "\n";
print TOUT $island->{'tokupase'} . "\n";
print TOUT $island->{'koutpase'} . "\n";
print TOUT $island->{'sonopase'} . "\n";
# �Ϸ�
    if(($num <= -1) || ($num == $island->{'id'})) {
	my ($retry) = $HretryCount;

	while (! open(IOUT, ">${HdirName}/islandtmp.$island->{'id'}"))
	{
	    $retry--;
	    if ($retry <= 0)
	    {
		# 2.02 ����Ū�˽�λ�����ޤ�
		return 1;
	    }

	    # 0.2 �� sleep
	    select undef, undef, undef, 0.2;
	}

	my($land, $landValue);
	$land = $island->{'land'};
	$landValue = $island->{'landValue'};
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
	    for($x = 0; $x < $HislandSize; $x++) {
		printf IOUT ("%02x%02x", $land->[$x][$y], $landValue->[$x][$y]);
	    }
	    print IOUT "\n";
	}

	# ���ޥ��
	my($command, $cur, $i);
	$command = $island->{'command'};
	for($i = 0; $i < $HcommandMax; $i++) {
	    printf IOUT ("%d,%d,%d,%d,%d\n", 
			 $command->[$i]->{'kind'},
			 $command->[$i]->{'target'},
			 $command->[$i]->{'x'},
			 $command->[$i]->{'y'},
			 $command->[$i]->{'arg'}
			 );
	}

	# ������Ǽ���
	my($lbbs);
	$lbbs = $island->{'lbbs'};
	for($i = 0; $i < $HlbbsMax; $i++) {
	    print IOUT $lbbs->[$i] . "\n";
	}

	close(IOUT);
	unlink("${HdirName}/island.$island->{'id'}");
	rename("${HdirName}/islandtmp.$island->{'id'}", "${HdirName}/island.$island->{'id'}");
    }
}
sub writeIslands {
    my($island, $num) = @_;
    my($birth);
    $birth = int($island->{'birth'});
   print OUT $island->{'name'} . ",$birth\n";
    print OUT $island->{'id'} . "\n";
    print OUT $island->{'prize'} . "\n";
    print OUT $island->{'absent'} . "\n";
    print OUT $island->{'comment'} . "\n";
    print OUT $island->{'password'} . "\n";
    print OUT $island->{'money'} . "\n";
    print OUT $island->{'food'} . "\n";
    print OUT $island->{'pop'} . "\n";
    print OUT $island->{'area'} . "\n";
    print OUT $island->{'farm'} . "\n";
    print OUT $island->{'factory'} . "\n";
    print OUT $island->{'mountain'} . "\n";
print MOUT $island->{'id'} . "\n";
print MOUT $island->{'flagname'} . "\n";
print HOUT $island->{'id'} . "\n";
print HOUT $island->{'ownername'} . "\n";
print GOUT $island->{'id'} . "\n";
print GOUT $island->{'ADDRE'} . "\n";
print SOUT $island->{'id'} . "\n";
print SOUT $island->{'kanko'} . "\n";
print BOUT $island->{'id'} . "\n";
print BOUT $island->{'monsnumber'} . "\n"; 
print BOUT $island->{'monka'} . "\n";
print BOUT $island->{'top'} . "\n";
print BOUT $island->{'empe'} . "\n";
print COUT $island->{'id'} . "\n";
print COUT $island->{'kouei'} . "\n";
print COUT $island->{'kanei'} . "\n"; 
print COUT $island->{'bouei'} . "\n";
print COUT $island->{'reiei'} . "\n";
print COUT $island->{'hatei'} . "\n";
print COUT $island->{'pmsei'} . "\n";
print DOUT $island->{'id'} . "\n";
print DOUT $island->{'yousho'} . "\n";
print DOUT $island->{'Jous'} . "\n";
print DOUT $island->{'hatud'} . "\n";
print DOUT $island->{'gomi'} . "\n";
print DOUT $island->{'slag'} . "\n";
print DOUT $island->{'shoku'} . "\n";
print DOUT $island->{'sigoto'} . "\n";
print DOUT $island->{'oil'} . "\n";
print DOUT $island->{'boku'} . "\n";
print EOUT $island->{'id'} . "\n";
print EOUT $island->{'sen'} . "\n"; 
print EOUT $island->{'hei'} . "\n";
print EOUT $island->{'ino'} . "\n";
print EOUT $island->{'teikou'} . "\n";
print EOUT $island->{'score'} . "\n";
print EOUT $island->{'shaka'} . "\n";
print EOUT $island->{'shamo'} . "\n";
print EOUT $island->{'shuu'} . "\n";
print EOUT $island->{'yhuu'} . "\n";
print FOUT $island->{'id'} . "\n";
print FOUT $island->{'koukyo'} . "\n";
print FOUT $island->{'hatuden'} . "\n";
print FOUT $island->{'nougyo'} . "\n";
print FOUT $island->{'kouzan'} . "\n";
print FOUT $island->{'koujyou'} . "\n";
print FOUT $island->{'gunji'} . "\n";
print FOUT $island->{'tokushu'} . "\n";
print FOUT $island->{'koutuu'} . "\n";
print FOUT $island->{'sonota'} . "\n";
print TOUT $island->{'id'} . "\n";
print TOUT $island->{'koukpase'} . "\n";
print TOUT $island->{'hatupase'} . "\n";
print TOUT $island->{'noupase'} . "\n";
print TOUT $island->{'kouzpase'} . "\n";
print TOUT $island->{'koujpase'} . "\n";
print TOUT $island->{'gunpase'} . "\n";
print TOUT $island->{'tokupase'} . "\n";
print TOUT $island->{'koutpase'} . "\n";
print TOUT $island->{'sonopase'} . "\n";
open(IOUT, ">${HdirName1}/islandtmp.$island->{'id'}");
	my($land, $landValue);
	$land = $island->{'land'};
	$landValue = $island->{'landValue'};
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
	    for($x = 0; $x < $HislandSize; $x++) {
		printf IOUT ("%02x%02x", $land->[$x][$y], $landValue->[$x][$y]);
	    }
	    print IOUT "\n";
	}

	# ���ޥ��
	my($command, $cur, $i);
	$command = $island->{'command'};
	for($i = 0; $i < $HcommandMax; $i++) {
	    printf IOUT ("%d,%d,%d,%d,%d\n", 
			 $command->[$i]->{'kind'},
			 $command->[$i]->{'target'},
			 $command->[$i]->{'x'},
			 $command->[$i]->{'y'},
			 $command->[$i]->{'arg'}
			 );
	}

	# ������Ǽ���
	my($lbbs);
	$lbbs = $island->{'lbbs'};
	for($i = 0; $i < $HlbbsMax; $i++) {
	    print IOUT $lbbs->[$i] . "\n";
	}

	close(IOUT);
	unlink("${HdirName1}/island.$island->{'id'}");
	rename("${HdirName1}/islandtmp.$island->{'id'}", "${HdirName1}/island.$island->{'id'}");
    
}
sub writeIslandscomment {
    my($num) = @_;

    # �ե�����򳫤�
    my($retry) = $HretryCount;
    while (! open(OUT, ">${HdirName}/hakojima.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 ����Ū�˽�λ�����ޤ�
	    return 1;
	}

	# 0.2 �� sleep
	select undef, undef, undef, 0.2;
    }

    # �ƥѥ�᡼���񤭹���
    print OUT "$HislandTurn\n";
    print OUT "$HislandLastTime\n";
    print OUT "$HislandNumber\n";
    print OUT "$HislandNextID\n";

     # ��ν񤭤���
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
    $birth = int($Hislands[$i]->{'birth'});
    print OUT $Hislands[$i]->{'name'} . ",$birth\n";
    print OUT $Hislands[$i]->{'id'} . "\n";
    print OUT $Hislands[$i]->{'prize'} . "\n";
    print OUT $Hislands[$i]->{'absent'} . "\n";
    print OUT $Hislands[$i]->{'comment'} . "\n";
    print OUT $Hislands[$i]->{'password'} . "\n";
    print OUT $Hislands[$i]->{'money'} . "\n";
    print OUT $Hislands[$i]->{'food'} . "\n";
    print OUT $Hislands[$i]->{'pop'} . "\n";
    print OUT $Hislands[$i]->{'area'} . "\n";
    print OUT $Hislands[$i]->{'farm'} . "\n";
    print OUT $Hislands[$i]->{'factory'} . "\n";
    print OUT $Hislands[$i]->{'mountain'} . "\n";
    }

    # �ե�������Ĥ���
    close(OUT);

    # �����̾���ˤ���
    unlink("${HdirName}/hakojima.dat");
    rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");
}
sub writeIslandsrocal {
    my($HcurrentID) = @_;
	my ($retry) = $HretryCount;
  $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
	while (! open(IOUT, ">${HdirName}/islandtmp.$island->{'id'}"))
	{
	    $retry--;
	    if ($retry <= 0)
	    {
		# 2.02 ����Ū�˽�λ�����ޤ�
		return 1;
	    }

	    # 0.2 �� sleep
	    select undef, undef, undef, 0.2;
	}

	my($land, $landValue);
	$land = $island->{'land'};
	$landValue = $island->{'landValue'};
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
	    for($x = 0; $x < $HislandSize; $x++) {
		printf IOUT ("%02x%02x", $land->[$x][$y], $landValue->[$x][$y]);
	    }
	    print IOUT "\n";
	}

	# ���ޥ��
	my($command, $cur, $i);
	$command = $island->{'command'};
	for($i = 0; $i < $HcommandMax; $i++) {
	    printf IOUT ("%d,%d,%d,%d,%d\n", 
			 $command->[$i]->{'kind'},
			 $command->[$i]->{'target'},
			 $command->[$i]->{'x'},
			 $command->[$i]->{'y'},
			 $command->[$i]->{'arg'}
			 );
	}

	# ������Ǽ���
	my($lbbs);
	$lbbs = $island->{'lbbs'};
	for($i = 0; $i < $HlbbsMax; $i++) {
	    print IOUT $lbbs->[$i] . "\n";
	}

	close(IOUT);
	unlink("${HdirName}/island.$island->{'id'}");
	rename("${HdirName}/islandtmp.$island->{'id'}", "${HdirName}/island.$island->{'id'}");
    
}
#----------------------------------------------------------------------
# ������
#----------------------------------------------------------------------

# ɸ����Ϥؤν���
sub out {
    print STDOUT jcode::sjis($_[0]);
}

# �ǥХå���
sub HdebugOut {
   open(DOUT, ">>debug.log");
   print DOUT ($_[0]);
   close(DOUT);
}

# CGI���ɤߤ���
sub cgiInput {
    my($line, $getLine);

    # ���Ϥ������ä����ܸ쥳���ɤ�EUC��
    $line = <>;
    $line =~ tr/+/ /;
    $line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    $line = jcode::euc($line);
    $line =~ s/[\x00-\x1f\,]//g;

    # GET�Τ�Ĥ�������
    $getLine = $ENV{'QUERY_STRING'};

    # �оݤ���
    if($line =~ /CommandButton([0-9]+)=/) {
	# ���ޥ�������ܥ���ξ��
	$HcurrentID = $1;
	$defaultID = $1;
    }
    if($line =~ /ShuuButton([0-9]+)=/) {
	# ���ޥ�������ܥ���ξ��
	$HcurrentID = $1;
	$defaultID = $1;
    }
if($line =~ /ChangeMode([0-9]+)=/) {
	$HcurrentID = $1;
	$defaultID = $1;
}
    if($line =~ /ISLANDNAME=([^\&]*)\&/){
	# ̾������ξ��
	$HcurrentName = cutColumn($1, 32);
    }
if($line =~ /FLAGNAME=([^\&]*)\&/){
  # �����ʡ�̾�ξ��
  $HcurrentFlagName = cutColumn($1, 64);
}
if($line =~ /OWNERNAME=([^\&]*)\&/){
  # �����ʡ�̾�ξ��
  $HcurrentOwnerName = cutColumn($1, 32);
}

    if($line =~ /ISLANDID=([0-9]+)\&/){
	# ����¾�ξ��
	$HcurrentID = $1;
	$defaultID = $1;
    }

    # �ѥ����
    if($line =~ /OLDPASS=([^\&]*)\&/) {
	$HoldPassword = $1;
	$HdefaultPassword = $1;
    }
    if($line =~ /PASSWORD=([^\&]*)\&/) {
	$HinputPassword = $1;
	$HdefaultPassword = $1;
    }
    if($line =~ /PASSWORD2=([^\&]*)\&/) {
	$HinputPassword2 = $1;
    }

    # ��å�����
    if($line =~ /MESSAGE=([^\&]*)\&/) {
	$Hmessage = cutColumn($1, 160);
    }

    # ������Ǽ���
    if($line =~ /LBBSNAME=([^\&]*)\&/) {
	$HlbbsName = $1;
	$HdefaultName = $1;
    }
    if($line =~ /LBBSMESSAGE=([^\&]*)\&/) {
	$HlbbsMessage = $1;
    }

    # main mode�μ���
    if($line =~ /TurnButton/) {
	if($Hdebug == 1) {
	    $HmainMode = 'Hdebugturn';
	}
  } elsif($line =~ /ChangeOwnerButton/) {
    $HmainMode = 'chowner';
  } elsif($line =~ /ChangeFlagButton/) {
    $HmainMode = 'chflag';
    } elsif($line =~ /OwnerButton/) {
	$HmainMode = 'owner';
$Hnmo = 0;
if($line =~ /nmo=nii\&/){
$Hnmo = 1;
}
    } elsif($line =~ /ChangeMode/) {
	$HmainMode = 'ownerb';
$Hnmo = 0;
if($line =~ /nmo=nii\&/){
$Hnmo = 1;
}
    } elsif($getLine =~ /Sight=([0-9]*)/) {
	$HmainMode = 'print';
	$HcurrentID = $1;
    } elsif($line =~ /NewIslandButton/) {
	$HmainMode = 'new';
    } elsif($line =~ /LbbsButton(..)([0-9]*)/) {
	$HmainMode = 'lbbs';
	if($1 eq 'SS') {
$Hsee = 0;
if($line =~ /see=secret\&/){
$Hsee = 1;
}
	    # �Ѹ���
	    $HlbbsMode = 0;
	} elsif($1 eq 'OW') {
	    # ���
	    $HlbbsMode = 1;
	} elsif($1 eq 'FO') {
	    # ¾�����
$Hsee = 0;
if($line =~ /see=secret\&/){
$Hsee = 1;
}
	    $HlbbsMode = 3;
	    $HforeignerID = $HcurrentID;
	} else {
	    # ���
	    $HlbbsMode = 2;
	}
	$HcurrentID = $2;

	# ������⤷��ʤ��Τǡ��ֹ�����
	$line =~ /NUMBER=([^\&]*)\&/;
	$HcommandPlanNumber = $1;

    } elsif($line =~ /ChangeInfoButton/) {
	$HmainMode = 'change';
    } elsif($line =~ /MessageButton([0-9]*)/) {
	$HmainMode = 'comment';
	$HcurrentID = $1;
    } elsif($line =~ /ShuuButton/) {
	$HmainMode = 'Shuu';
	$line =~ /paraa=([^\&]*)\&/;
$HparameterA = $1;
	$line =~ /parab=([^\&]*)\&/;
$HparameterB = $1;
	$line =~ /parac=([^\&]*)\&/;
$HparameterC = $1;
	$line =~ /parad=([^\&]*)\&/;
$HparameterD = $1;
	$line =~ /parae=([^\&]*)\&/;
$HparameterE = $1;
	$line =~ /paraf=([^\&]*)\&/;
$HparameterF = $1;
	$line =~ /parag=([^\&]*)\&/;
$HparameterG = $1;
	$line =~ /parah=([^\&]*)\&/;
$HparameterH = $1;
    } elsif($line =~ /CommandButton/) {
	$HmainMode = 'command';

	# ���ޥ�ɥ⡼�ɤξ�硢���ޥ�ɤμ���
	$line =~ /NUMBER=([^\&]*)\&/;
	$HcommandPlanNumber = $1;
$Hnmo = 0;
if($line =~ /nmo=nii\&/){
$Hnmo = 1;
$HcommandPoti = 0;
if($line =~ /eku=zousei\&/){
$HcommandPoti = 1;
	$line =~ /COMMANDa=([^\&]*)\&/;
	$HcommandKind = $1;
	$HdefaultKind = $1;
}elsif($line =~ /eku=kensetu\&/){
$HcommandPoti = 2;
	$line =~ /COMMANDb=([^\&]*)\&/;
	$HcommandKind = $1;
	$HdefaultKind = $1;
}elsif($line =~ /eku=boueki\&/){
$HcommandPoti = 3;
	$line =~ /COMMANDc=([^\&]*)\&/;
	$HcommandKind = $1;
	$HdefaultKind = $1;
}elsif($line =~ /eku=enjyo\&/){
$HcommandPoti = 4;
	$line =~ /COMMANDd=([^\&]*)\&/;
	$HcommandKind = $1;
	$HdefaultKind = $1;
}elsif($line =~ /eku=misairu\&/){
$HcommandPoti = 5;
	$line =~ /COMMANDe=([^\&]*)\&/;
	$HcommandKind = $1;
	$HdefaultKind = $1;
}elsif($line =~ /eku=kaijyu\&/){
$HcommandPoti = 6;
	$line =~ /COMMANDf=([^\&]*)\&/;
	$HcommandKind = $1;
	$HdefaultKind = $1;
}elsif($line =~ /eku=eisei\&/){
$HcommandPoti = 7;
	$line =~ /COMMANDg=([^\&]*)\&/;
	$HcommandKind = $1;
	$HdefaultKind = $1;
}elsif($line =~ /eku=kishou\&/){
$HcommandPoti = 8;
	$line =~ /COMMANDh=([^\&]*)\&/;
	$HcommandKind = $1;
	$HdefaultKind = $1;
}elsif($line =~ /eku=doumei\&/){
$HcommandPoti = 9;
	$line =~ /COMMANDi=([^\&]*)\&/;
	$HcommandKind = $1;
	$HdefaultKind = $1;
}elsif($line =~ /eku=sonota\&/){
$HcommandPoti = 10;
	$line =~ /COMMANDj=([^\&]*)\&/;
	$HcommandKind = $1;
	$HdefaultKind = $1;
}elsif($line =~ /eku=jidou\&/){
$HcommandPoti = 11;
	$line =~ /COMMANDk=([^\&]*)\&/;
	$HcommandKind = $1;
	$HdefaultKind = $1;
}else{
$HcommandPoti = 1;
$HcommandKind = 41;
$HdefaultKind = 41;
}
}else{
	$line =~ /COMMAND=([^\&]*)\&/;
	$HcommandKind = $1;
	$HdefaultKind = $1;
}
	$line =~ /r1=([^\&]*)\&/;
	$HdefaultKindB = $1;
	$line =~ /AMOUNT=([^\&]*)\&/;
	$HcommandArg = $1;
	$line =~ /TARGETID=([^\&]*)\&/;
	$HcommandTarget = $1;
	$defaultTarget = $1;
	$line =~ /POINTX=([^\&]*)\&/;
	$HcommandX = $1;
	$HdefaultX = $1;
        $line =~ /POINTY=([^\&]*)\&/;
	$HcommandY = $1;
	$HdefaultY = $1;
	$line =~ /COMMANDMODE=(write|insert|delete)/;
	$HcommandMode = $1;
    } else {
	$HmainMode = 'top';
    }

}
sub writeIslandsOwner {
  my($num) = @_;
  # File Open
  open(OUT, ">${HdirName2}/howner.tmp");
  my($i);
  for($i = 0; $i < $HislandNumber; $i++){
    print OUT "$Hislands[$i]->{'id'}\n";
    print OUT "$Hislands[$i]->{'ownername'}\n";
  }

  close(OUT);

  # �����̾���ˤ���
  unlink("${HdirName2}/howner.dat");
  rename("${HdirName2}/howner.tmp", "${HdirName2}/howner.dat");
}
sub writeIslandsFlag {
  my($num) = @_;
  # File Open
  open(OUT, ">${HdirName2}/hflag.tmp");
  my($i);
  for($i = 0; $i < $HislandNumber; $i++){
    print OUT "$Hislands[$i]->{'id'}\n";
    print OUT "$Hislands[$i]->{'flagname'}\n";
  }

  close(OUT);

  # �����̾���ˤ���
  unlink("${HdirName2}/hflag.dat");
  rename("${HdirName2}/hflag.tmp", "${HdirName2}/hflag.dat");
}
sub writeIslandsshuu {
  my($num) = @_;
  # File Open
  open(OUT, ">${HdirName}/hpase.tmp");
  my($i);
  for($i = 0; $i < $HislandNumber; $i++){
print OUT $Hislands[$i]->{'id'} . "\n";
print OUT $Hislands[$i]->{'koukpase'} . "\n";
print OUT $Hislands[$i]->{'hatupase'} . "\n";
print OUT $Hislands[$i]->{'noupase'} . "\n";
print OUT $Hislands[$i]->{'kouzpase'} . "\n";
print OUT $Hislands[$i]->{'koujpase'} . "\n";
print OUT $Hislands[$i]->{'gunpase'} . "\n";
print OUT $Hislands[$i]->{'tokupase'} . "\n";
print OUT $Hislands[$i]->{'koutpase'} . "\n";
print OUT $Hislands[$i]->{'sonopase'} . "\n";
  }

  close(OUT);

  # �����̾���ˤ���
 unlink("${HdirName}/hpase.dat");
  rename("${HdirName}/hpase.tmp", "${HdirName}/hpase.dat");
}
sub writeIslandsAddre {
  my($num) = @_;
  # File Open
  open(OUT, ">${HdirName2}/haddre.tmp");
  my($i);
  for($i = 0; $i < $HislandNumber; $i++){
    print OUT "$Hislands[$i]->{'id'}\n";
    print OUT "$Hislands[$i]->{'ADDRE'}\n";
  }

  close(OUT);

  # �����̾���ˤ���
  unlink("${HdirName2}/haddre.dat");
  rename("${HdirName2}/haddre.tmp", "${HdirName2}/haddre.dat");
}
sub writeIslandskanko {
  my($num) = @_;
  # File Open
  open(OUT, ">${HdirName2}/hkanko.tmp");
  my($i);
  for($i = 0; $i < $HislandNumber; $i++){
    print OUT "$Hislands[$i]->{'id'}\n";
    print OUT "$Hislands[$i]->{'kanko'}\n";
  }

  close(OUT);

  # �����̾���ˤ���
  unlink("${HdirName2}/hkanko.dat");
  rename("${HdirName2}/hkanko.tmp", "${HdirName2}/hkanko.dat");
}
#cookie����
sub cookieInput {
    my($cookie);

    $cookie = jcode::euc($ENV{'HTTP_COOKIE'});

    if($cookie =~ /${HthisFile}OWNISLANDID=\(([^\)]*)\)/) {
	$defaultID = $1;
    }
    if($cookie =~ /${HthisFile}OWNISLANDPASSWORD=\(([^\)]*)\)/) {
	$HdefaultPassword = $1;
    }
    if($cookie =~ /${HthisFile}TARGETISLANDID=\(([^\)]*)\)/) {
	$defaultTarget = $1;
    }
    if($cookie =~ /${HthisFile}LBBSNAME=\(([^\)]*)\)/) {
	$HdefaultName = $1;
    }
    if($cookie =~ /${HthisFile}POINTX=\(([^\)]*)\)/) {
	$HdefaultX = $1;
    }
    if($cookie =~ /${HthisFile}POINTY=\(([^\)]*)\)/) {
	$HdefaultY = $1;
    }
    if($cookie =~ /${HthisFile}KIND=\(([^\)]*)\)/) {
	$HdefaultKind = $1;
    }

}

#cookie����
sub cookieOutput {
    my($cookie, $info);

    # �ä�����¤�����
    my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	gmtime(time + 30 * 86400); # ���� + 30��

    # 2������
    $year += 1900;
    if ($date < 10) { $date = "0$date"; }
    if ($hour < 10) { $hour = "0$hour"; }
    if ($min < 10) { $min  = "0$min"; }
    if ($sec < 10) { $sec  = "0$sec"; }

    # ������ʸ����
    $day = ("Sunday", "Monday", "Tuesday", "Wednesday",
	    "Thursday", "Friday", "Saturday")[$day];

    # ���ʸ����
    $mon = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
	    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")[$mon];

    # �ѥ��ȴ��¤Υ��å�
    $info = "; expires=$day, $date\-$mon\-$year $hour:$min:$sec GMT\n";
    $cookie = '';
    
    if(($HcurrentID) && ($HmainMode eq 'owner')){
	$cookie .= "Set-Cookie: ${HthisFile}OWNISLANDID=($HcurrentID) $info";
    }
    if($HinputPassword) {
	$cookie .= "Set-Cookie: ${HthisFile}OWNISLANDPASSWORD=($HinputPassword) $info";
    }
    if($HcommandTarget) {
	$cookie .= "Set-Cookie: ${HthisFile}TARGETISLANDID=($HcommandTarget) $info";
    }
    if($HlbbsName) {
	$cookie .= "Set-Cookie: ${HthisFile}LBBSNAME=($HlbbsName) $info";
    }
    if($HcommandX) {
	$cookie .= "Set-Cookie: ${HthisFile}POINTX=($HcommandX) $info";
    }
    if($HcommandY) {
	$cookie .= "Set-Cookie: ${HthisFile}POINTY=($HcommandY) $info";
    }
    if($HcommandKind) {
	# ��ư�ϰʳ�
	$cookie .= "Set-Cookie: ${HthisFile}KIND=($HcommandKind) $info";
    }

    out($cookie);
}

#------------------
#----------------------------------------------------------------------
# �桼�ƥ���ƥ�
#----------------------------------------------------------------------
sub hakolock {
    if($lockMode == 1) {
	# directory����å�
	return hakolock1();

    } elsif($lockMode == 2) {
	# flock����å�
	return hakolock2();
    } elsif($lockMode == 3) {
	# symlink����å�
	return hakolock3();
    } else {
	# �̾�ե����뼰��å�
	return hakolock4();
    }
}

sub hakolock1 {
    # ��å���
    if(mkdir('hakojimalock', $HdirMode)) {
	# ����
	return 1;
    } else {
	# ����
	my($b) = (stat('hakojimalock'))[9];
	if(($b > 0) && ((time() -  $b)> $unlockTime)) {
	    # �������
	    unlock();

	    # �إå�����
	    tempHeader();

	    # ���������å�����
	    tempUnlock();

	    # �եå�����
	    tempFooter();

	    # ��λ
	    exit(0);
	}
	return 0;
    }
}

sub hakolock2 {
    open(LOCKID, '>>hakojimalockflock');
    if(flock(LOCKID, 2)) {
	# ����
	return 1;
    } else {
	# ����
	return 0;
    }
}

sub hakolock3 {
    # ��å���
    if(symlink('hakojimalockdummy', 'hakojimalock')) {
	# ����
	return 1;
    } else {
	# ����
	my($b) = (lstat('hakojimalock'))[9];
	if(($b > 0) && ((time() -  $b)> $unlockTime)) {
	    # �������
	    unlock();

	    # �إå�����
	    tempHeader();

	    # ���������å�����
	    tempUnlock();

	    # �եå�����
	    tempFooter();

	    # ��λ
	    exit(0);
	}
	return 0;
    }
}

sub hakolock4 {
    # ��å���
    if(unlink('key-free')) {
	# ����
	open(OUT, '>key-locked');
	print OUT time;
	close(OUT);
	return 1;
    } else {
	# ��å����֥����å�
	if(!open(IN, 'key-locked')) {
	    return 0;
	}

	my($t);
	$t = <IN>;
	close(IN);
	if(($t != 0) && (($t + $unlockTime) < time)) {
	    # 120�ðʾ�вᤷ�Ƥ��顢����Ū�˥�å��򳰤�
	    unlock();

	    # �إå�����
	    tempHeader();

	    # ���������å�����
	    tempUnlock();

	    # �եå�����
	    tempFooter();

	    # ��λ
	    exit(0);
	}
	return 0;
    }
}

# ��å��򳰤�
sub unlock {
    if($lockMode == 1) {
	# directory����å�
	rmdir('hakojimalock');

    } elsif($lockMode == 2) {
	# flock����å�
	close(LOCKID);

    } elsif($lockMode == 3) {
	# symlink����å�
	unlink('hakojimalock');
    } else {
	# �̾�ե����뼰��å�
	my($i);
	$i = rename('key-locked', 'key-free');
    }
}

# �����������֤�
sub min {
    return ($_[0] < $_[1]) ? $_[0] : $_[1];
}

# �ѥ���ɥ��󥳡���
sub encode {
    if($cryptOn == 1) {
	return crypt($_[0], 'h2');
    } else {
	return $_[0];
    }
}

# �ѥ���ɥ����å�
sub checkPassword {
    my($p1, $p2) = @_;

    # null�����å�
    if($p2 eq '') {
	return 0;
    }

    # �ޥ������ѥ���ɥ����å�
    if($masterPassword eq $p2) {
	return 1;
    }

    # ����Υ����å�
    if($p1 eq encode($p2)) {
	return 1;
    }

    return 0;
}

# 1000��ñ�̴ݤ�롼����
sub aboutMoney {
    my($m) = @_;
    if($m < 500) {
	return "����500${HunitMoney}̤��";
    } else {
	$m = int(($m + 500) / 1000);
	return "����${m}000${HunitMoney}";
    }
}

# ����������ʸ���ν���
sub htmlEscape {
    my($s) = @_;
    $s =~ s/&/&amp;/g;
    $s =~ s/</&lt;/g;
    $s =~ s/>/&gt;/g;
    $s =~ s/\"/&quot;/g; #"
    return $s;
}

# 80�������ڤ�·��
sub cutColumn {
    my($s, $c) = @_;
    if(length($s) <= $c) {
	return $s;
    } else {
	# ���80�����ˤʤ�ޤ��ڤ���
	my($ss) = '';
	my($count) = 0;
	while($count < $c) {
	    $s =~ s/(^[\x80-\xFF][\x80-\xFF])|(^[\x00-\x7F])//;
	    if($1) {
		$ss .= $1;
		$count ++;
	    } else {
		$ss .= $2;
	    }
	    $count ++;
	}
	return $ss;
    }
}

# ���̾�������ֹ������(ID����ʤ����ֹ�)
sub nameToNumber {
    my($name) = @_;

    # ���礫��õ��
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	if($Hislands[$i]->{'name'} eq $name) {
	    return $i;
	}
    }

    # ���Ĥ���ʤ��ä����
    return -1;
}

# ���äξ���
sub monsterSpec {
    my($lv) = @_;

    # ����
    my($kind) = int($lv / 10);

    # ̾��
    my($name);
    $name = $HmonsterName[$kind];

    # ����
    my($hp) = $lv - ($kind * 10);
    
    return ($kind, $name, $hp);
}

# �и��Ϥ����٥�򻻽�
sub expToLevel {
    my($kind, $exp) = @_;
    my($i);
    if($kind == $HlandBase) {
	# �ߥ��������
	for($i = $maxBaseLevel; $i > 1; $i--) {
	    if($exp >= $baseLevelUp[$i - 2]) {
		return $i;
	    }
	}
	return 1;
    } else {
	# �������
	for($i = $maxSBaseLevel; $i > 1; $i--) {
	    if($exp >= $sBaseLevelUp[$i - 2]) {
		return $i;
	    }
	}
	return 1;
    }

}

# (0,0)����(size - 1, size - 1)�ޤǤο��������ŤĽФƤ���褦��
# (@Hrpx, @Hrpy)������
sub makeRandomPointArray {
    # �����
    my($y);
    @Hrpx = (0..$HislandSize-1) x $HislandSize;
    for($y = 0; $y < $HislandSize; $y++) {
	push(@Hrpy, ($y) x $HislandSize);
    }

    # ����åե�
    my ($i);
    for ($i = $HpointNumber; --$i; ) {
	my($j) = int(rand($i+1)); 
	if($i == $j) { next; }
	@Hrpx[$i,$j] = @Hrpx[$j,$i];
	@Hrpy[$i,$j] = @Hrpy[$j,$i];
    }
}

# 0����(n - 1)�����
sub random {
    return int(rand(1) * $_[0]);
}

#----------------------------------------------------------------------
# ��ɽ��
#----------------------------------------------------------------------
# �ե������ֹ����ǥ�ɽ��
sub logFilePrint {
    my($fileNumber, $id, $mode) = @_;
    open(LIN, "${HdirName}/hakojima.log$_[0]");
    my($line, $m, $turn, $id1, $id2, $message);
    while($line = <LIN>) {
	$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),(.*)$/;
	($m, $turn, $id1, $id2, $message) = ($1, $2, $3, $4, $5);

	# ��̩�ط�
	if($m == 1) {
	    if(($mode == 0) || ($id1 != $id)) {
		# ��̩ɽ�������ʤ�
		next;
	    }
	    $m = '<B>(��̩)</B>';
	} else {
	    $m = '';
	}

	# ɽ��Ū�Τ�
	if($id != 0) {
	    if(($id != $id1) &&
	       ($id != $id2)) {
		next;
	    }
	}

	# ɽ��
	out("<NOBR>${HtagNumber_}������$turn$m${H_tagNumber}��$message</NOBR><BR>\n");
    }
    close(LIN);
}

#----------------------------------------------------------------------
# �ƥ�ץ졼��
#----------------------------------------------------------------------
# �����
sub tempInitialize {
    # �祻�쥯��(�ǥե���ȼ�ʬ)
    $HislandList = getIslandList($defaultID);
    $HtargetList = getIslandList($defaultTarget);
}

# ��ǡ����Υץ�������˥塼��
sub getIslandList {
    my($select) = @_;
    my($list, $name, $id, $s, $i);

    #��ꥹ�ȤΥ�˥塼
    $list = '';
    for($i = 0; $i < $HislandNumber; $i++) {
	$name = $Hislands[$i]->{'name'};
	$id = $Hislands[$i]->{'id'};
	if($id eq $select) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}
	$list .=
	    "<OPTION VALUE=\"$id\" $s>${name}��\n";
    }
    return $list;
}


# �إå�
sub tempHeader {
if($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/ and $ENV{HTTP_USER_AGENT}=~/Windows/){
print qq{Content-type: text/html; charset=Shift_JIS\n};
print qq{Content-encoding: gzip\n\n};
# gzip�Υѥ����ѹ���ɬ�פǤ���
open(STDOUT,"| /bin/gzip -1 -c");
print " " x 2048 if($ENV{HTTP_USER_AGENT}=~/MSIE/);
print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
}else{
print qq{Content-type: text/html; charset=Shift_JIS\n\n};
print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
}
out(<<END);

<HTML>
<HEAD>
<TITLE>
$Htitle
</TITLE>
<BASE HREF="$imageDir/">
</HEAD>
<BODY $htmlBody>
<HR>
END
}
sub tempHeaderB {
if($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/ and $ENV{HTTP_USER_AGENT}=~/Windows/){
print qq{Content-type: text/html; charset=Shift_JIS\n};
print qq{Content-encoding: gzip\n\n};
# gzip�Υѥ����ѹ���ɬ�פǤ���
open(STDOUT,"| /bin/gzip -1 -c");
print " " x 2048 if($ENV{HTTP_USER_AGENT}=~/MSIE/);
print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
}else{
print qq{Content-type: text/html; charset=Shift_JIS\n\n};
print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
}
out(<<END);
<META http-equiv=Content-Script-Type content=text/javascript>
<HTML>
<HEAD>
<TITLE>
$Htitle
</TITLE>
<BASE HREF="$imageDir/">
</HEAD>
<BODY $htmlBody onload=init();>
<HR>
END
}
# �եå�
sub tempFooter {
    out(<<END);
<HR>
<P align=center>
<A HREF="$mentehtml">���ƥʥ󥹥⡼��</A><br>
������:$adminName(<A HREF="mailto:$email">$email</A>)<BR>
<A HREF="http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html">Ȣ����祹����ץ����۸�</A><br>
Ȣ�����Υڡ���(<A HREF="http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html">http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html</A>)<BR>
LitsȢ���Ѳ�¤��MT<BR>
</BODY>
</BODY>
</HTML>
END
}

# ��å�����
sub tempLockFail {
    # �����ȥ�
    out(<<END);
${HtagBig_}Ʊ�������������顼�Ǥ���<BR>
�֥饦���Ρ����ץܥ���򲡤���<BR>
���Ф餯�ԤäƤ�����٤����������${H_tagBig}$HtempBack
END
}

# �������
sub tempUnlock {
    # �����ȥ�
    out(<<END);
${HtagBig_}����Υ����������۾ｪλ���ä��褦�Ǥ���<BR>
��å�����������ޤ�����${H_tagBig}$HtempBack
END
}

# hakojima.dat���ʤ�
sub tempNoDataFile {
    out(<<END);
${HtagBig_}�ǡ����ե����뤬�����ޤ���${H_tagBig}$HtempBack
END
}

# �ѥ���ɴְ㤤
sub tempWrongPassword {
    out(<<END);
${HtagBig_}�ѥ���ɤ��㤤�ޤ���${H_tagBig}$HtempBack
END
}

# ��������ȯ��
sub tempProblem {
    out(<<END);
${HtagBig_}����ȯ�����Ȥꤢ������äƤ���������${H_tagBig}$HtempBack
END
}
