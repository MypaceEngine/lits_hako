#!/bin/perl
# ↑はサーバーに合わせて変更して下さい。
# perl5用です。

#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# メインスクリプト(ver1.00)
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
# 各種設定値
# (これ以降の部分の各設定値を、適切な値に変更してください)
#----------------------------------------------------------------------
#my($ref_url1) = 'http://123.co.jp/game.html';
#my($ref_url2) = 'http://123.co.jp/game.html';
#my($ref_url3) = 'http://123.co.jp/game.html';
#my($ref_url4) = 'http://123.co.jp/game.html';
#my($ref_url5) = 'http://123.co.jp/game.html';
#my($ref_url6) = 'http://123.co.jp/game.html';
#許可するリンク元があれば、4,5…と追加できます
する時は、IF分の中も一緒に増やしてください
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
#<HTML><HEAD><TITLE>箱島アクセス拒否</TITLE></HEAD>
#<BODY><center><H1>箱島アクセス拒否</H1><br>
#Litsの部屋メインページ以外からのアクセスを禁止しています。<br>
#トップページは<a href='http://123.co.jp/'>こちら</a>
#</BODY></HTML>
#EOF
#exit;
#}
# ここまで 
#----------------------------------------------------------------------
# 以下、必ず設定する部分
#----------------------------------------------------------------------

# このファイルを置くディレクトリ
# my($baseDir) = 'http://サーバー/ディレクトリ';
#
# 例)
# http://cgi2.bekkoame.ne.jp/cgi-bin/user/u5534/hakoniwa/hako-main.cgi
# として置く場合、
# my($baseDir) = 'http://cgi2.bekkoame.ne.jp/cgi-bin/user/u5534/hakoniwa';
# とする。最後にスラッシュ(/)は付けない。

my($baseDir) = 'http://www.yahoo.co.jp';

# 画像ファイルを置くディレクトリ
# my($imageDir) = 'http://サーバー/ディレクトリ';
my($imageDir) = 'http://123.co.jp/***';

# jcode.plの位置

# my($jcode) = '/usr/libperl/jcode.pl';  # ベッコアメの場合
# my($jcode) = './jcode.pl';             # 同じディレクトリに置く場合
my($jcode) = './jcode.pl';

# マスターパスワード
# このパスワードは、すべての島のパスワードを代用できます。
# 例えば、「他の島のパスワード変更」等もできます。
my($masterPassword) = '123456';

# 特殊パスワード
# このパスワードで「名前変更」を行うと、その島の資金、食料が最大値になります。
# (実際に名前を変える必要はありません。)
$HspecialPassword = '123456';

# 管理者名
my($adminName) = 'xx';

# 管理者のメールアドレス
my($email) = 'xxx@123.co.jp';

# 掲示板アドレス
my($bbs) = 'http://123.co.jp/xxx.cgi';

# ホームページのアドレス
my($toppage) = 'http://123.co.jp/xxx.htm';
my($mentehtml) = 'http://123.co.jp/hako-mente.cgi';
# ディレクトリのパーミッション
# 通常は0755でよいが、0777、0705、0704等でないとできないサーバーもあるらしい
$HdirMode = 0755;

# データディレクトリの名前
# ここで設定した名前のディレクトリ以下にデータが格納されます。
# デフォルトでは'data'となっていますが、セキュリティのため
# なるべく違う名前に変更してください。
$HdirName = 'xxx';
$HdirName1 = 'xx';
$HdirName2 = 'x';
# データの書き込み方

# ロックの方式
# 1 ディレクトリ
# 2 システムコール(可能ならば最も望ましい)
# 3 シンボリックリンク
# 4 通常ファイル(あまりお勧めでない)
my($lockMode) = 2;

# (注)
# 4を選択する場合には、'key-free'という、パーミション666の空のファイルを、
# このファイルと同位置に置いて下さい。

#----------------------------------------------------------------------
# 必ず設定する部分は以上
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# 以下、好みによって設定する部分
#----------------------------------------------------------------------
#----------------------------------------
# ゲームの進行やファイルなど
#----------------------------------------
# 1ターンが何秒か
$HunitTime = 14400;

# 異常終了基準時間
# (ロック後何秒で、強制解除するか)
my($unlockTime) = 60;

# 島の最大数
$HmaxIsland =99;

# トップページに表示するログのターン数
$HtopLogTurn = 1;

# ログファイル保持ターン数
$HlogMax = 10; 

# バックアップを何ターンおきに取るか
$HbackupTurn = 1;

# バックアップを何回分残すか
$HbackupTimes = 20;

# 発見ログ保持行数
$HhistoryMax = 30;

# 放棄コマンド自動入力ターン数
$HgiveupTurn = 10000;

# コマンド入力限界数
# (ゲームが始まってから変更すると、データファイルの互換性が無くなります。)
$HcommandMax = 50;

# ローカル掲示板行数を使用するかどうか(0:使用しない、1:使用する)
$HuseLbbs = 1;

# ローカル掲示板行数
$HlbbsMax = 20;

# ローカル掲示版のパスワード認証
# 他の島のオーナーが書き込むときにパスワード確認の有無
$HlbbsAuth = 1;

# ローカル掲示版のゲスト使用
# 1 のときは島のオーナーでない人が書き込むことが出来る
$HlbbsGuest = 1;

# 島作成直後のミサイル発射禁止ターン数
# 0 にすれば作成直後でもミサイル発射が可能になります
$HdisableMissileTurn = 0;

# 島作成直後の怪獣派遣禁止ターン数
# 0 にすれば作成直後でも怪獣派遣が可能になります
$HdisableSendMonsterTurn = 0;

# 島作成直後の資金援助禁止ターン数
# 0 にすれば 作成直後でも資金援助が可能になります
$HdisableSupportTurn = 0;

# 島の大きさ
# (変更できないかも)
$HislandSize = 31;

# 他人から資金を見えなくするか
# 0 見えない
# 1 見える
# 2 100の位で四捨五入
$HhideMoneyMode = 2;

# パスワードの暗号化(0だと暗号化しない、1だと暗号化する)
my($cryptOn) = 1;

# デバッグモード(1だと、「ターンを進める」ボタンが使用できる)
$Hdebug = 0;

# write open の retry 回数
$HretryCount = 5;

#----------------------------------------
# 資金、食料などの設定値と単位
#----------------------------------------
# 初期資金
$HinitialMoney = 1000;

# 初期食料
$HinitialFood = 100;

# お金の単位
$HunitMoney = '億円';

# 食料の単位
$HunitFood = '00トン';
$HunitOil = 'トン';

# 人口の単位
$HunitPop = '00人';

# 広さの単位
$HunitArea = '00ヘクタール';

# 木の数の単位
$HunitTree = '00本';

# 木の単位当たりの売値
$HtreeValue = 10;

# 名前変更のコスト
$HcostChangeName = 1;

# 人口1単位あたりの食料消費料
$HeatenFood = 0.05;

#----------------------------------------
# 基地の経験値
#----------------------------------------
# 経験値の最大値
$HmaxExpPoint = 255; # ただし、最大でも255まで

# レベルの最大値
my($maxBaseLevel) = 5;  # ミサイル基地
my($maxSBaseLevel) = 5; # 海底基地

# 経験値がいくつでレベルアップか
my(@baseLevelUp, @sBaseLevelUp);
@baseLevelUp = (20, 60, 120, 200); # ミサイル基地
@sBaseLevelUp = (20, 60, 120, 200);         # 海底基地

#----------------------------------------
# 防衛施設の自爆
#----------------------------------------
# 怪獣に踏まれた時自爆するなら1、しないなら0
$HdBaseAuto = 1;

#----------------------------------------
# 災害
#----------------------------------------
# 通常災害発生率(確率は0.1%単位)
$HdisMaizo      = 1; # 埋蔵金
# 地盤沈下
$HdisFallBorder = 600; # 安全限界の広さ(Hex数)
$HdisFalldown   = 30; # その広さを超えた場合の確率

# 怪獣
$HdisMonsBorder1 = 1001; # 人口基準1(怪獣レベル1)
$HdisMonsBorder2 = 2000; # 人口基準2(怪獣レベル2)
$HdisMonsBorder3 = 3000; # 人口基準3(怪獣レベル3)
$HdisMonsBorder4 = 4000; # 人口基準2(怪獣レベル2)
$HdisMonsBorder5 = 5000; # 人口基準3(怪獣レベル3)
$HdisMonsBorder6 = 6000; # 人口基準3(怪獣レベル3)
$HdisMonsBorder7 = 7000; # 人口基準3(怪獣レベル3)
$HdisMonsBorder8 = 8000; # 人口基準3(怪獣レベル3)
$HdisMonsBorder9 = 9000; # 人口基準3(怪獣レベル3)
# 種類
$HmonsterNumber  = 26; 

# 各基準において出てくる怪獣の番号の最大値
$HmonsterLevel1  = 2; # サンジラまで    
$HmonsterLevel2  = 4; # いのらゴーストまで
$HmonsterLevel3  = 6; # キングいのらまで(全部)
$HmonsterLevel4  = 10; # いのらゴーストまで
$HmonsterLevel5  = 13; # キングいのらまで(全部)
$HmonsterLevel6  = 15; # いのらゴーストまで
$HmonsterLevel7  = 17; # キングいのらまで(全部)
$HmonsterLevel8  = 20; # いのらゴーストまで
$HmonsterLevel9  = 21; # キングいのらまで(全部)
# 名前
@HmonsterName = 
    (
     'メカいのら',     # 0(人造)
     'いのら',         # 1
     'サンジラ',       # 2
     'レッドいのら',   # 3
     'ダークいのら',   # 4
   'いのらエッグ',   # 3
     'いのらベイビー',   # 4
     'いのらゴースト', # 5
     'クジラ',         # 6
     'キングいのら',    # 7
'いのらクイーン',
     '天使いのら',         # 1
     '悪魔いのら',       # 2
     '弱いのら',
     'ラジラ',         # 1
     'カウントダウンいのら',
'ドラゴン',
'火いのら',
'サンドいのら',
'古代シールド兵',
'古代青銅兵',
     'いのら神',
     '鉄鋼兵',
'特攻部隊',
'FX-330',
'FX-330A'
);

# 最低体力、体力の幅、特殊能力、経験値、死体の値段
@HmonsterBHP     = ( 2, 1, 1, 3, 2, 9, 9, 1, 4, 5, 2, 9 ,9, 1,1, 1, 9, 9, 9, 9, 9, 9,4,6,8,5);
@HmonsterDHP     = ( 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 1, 0, 0, 0,8, 8, 0,0, 0, 0, 0, 0, 0, 0, 0, 0);
@HmonsterSpecial = ( 0, 0, 3, 0, 1, 5, 6, 2, 4, 0, 7, 8, 9, 11,12,13,15,16,17,22,18,14,10,19,20,21);
@HmonsterExp     = ( 5, 5, 7,12,15,20,30,10,20,30, 40,50,50,3,20,30,30,40,40,50,100,255,10,20,30,50);
@HmonsterValue   = ( 0, 400, 500, 1000, 800, 1000, 1500, 300, 1500, 2000, 4000, 5000, 5000, 1,2000,1000,2000,3000,3000,5000,10000,999999,10,20,30,50);

# 特殊能力の内容は、
# 0 特になし
# 1 足が速い(最大2歩あるく)
# 2 足がとても速い(最大何歩あるくか不明)
# 3 奇数ターンは硬化
# 4 偶数ターンは硬化

# 画像ファイル
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

# 画像ファイルその2(硬化中)
@HmonsterImage2 =
    ('', '', 'monster4.gif', '', '', '', '', '', 'monster4.gif', '', '', '', '', '', '', 'monster16.gif', '', '', '', '', '', '', '', '', '', '', '');


#----------------------------------------
# 油田
#----------------------------------------
# 油田の収入
$HoilMoney = 2000;

# 油田の枯渇確率
$HoilRatio = 20;

#----------------------------------------
# 記念碑
#----------------------------------------
# 何種類あるか
$HmonumentNumber = 8;

# 名前
@HmonumentName = 
    (
     'モノリス', 
     '戦没者慰霊碑',
     '戦いの碑',
     '女神像(金)',
     '女神像(銀)',
     '女神像(銅)',
'天使像(銀)',
'天使像(金)',
    );

# 画像ファイル
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
# 賞関係
#----------------------------------------
# ターン杯を何ターン毎に出すか
$HturnPrizeUnit = 10;

# 賞の名前
$Hprize[0] = 'ターン杯';
$Hprize[1] = '繁栄賞';
$Hprize[2] = '超繁栄賞';
$Hprize[3] = '超絶繁栄賞';
$Hprize[4] = '平和賞';
$Hprize[5] = '超平和賞';
$Hprize[6] = '超絶平和賞';
$Hprize[7] = '災難賞';
$Hprize[8] = '超災難賞';
$Hprize[9] = '超絶災難賞';
$Hprize[10] = '究極繁栄賞';
$Hprize[11] = '究極平和賞';
$Hprize[12] = '究極災難賞';

#----------------------------------------
# 外見関係
#----------------------------------------
# <BODY>タグのオプション
my($htmlBody) = 'BGCOLOR="#EEFFFF"';

# ゲームのタイトル文字
$Htitle = 'Lits箱庭';

# タグ
# タイトル文字
$HtagTitle_ = '<FONT SIZE=7 COLOR="#8888ff">';
$H_tagTitle = '</FONT>';

# H1タグ用
$HtagHeader_ = '<FONT COLOR="#4444ff">';
$H_tagHeader = '</FONT>';

# 大きい文字
$HtagBig_ = '<FONT SIZE=6>';
$H_tagBig = '</FONT>';

# 島の名前など
$HtagName_ = '<FONT COLOR="#a06040"><B>';
$H_tagName = '</B></FONT>';

# 薄くなった島の名前
$HtagName2_ = '<FONT COLOR="#808080"><B>';
$H_tagName2 = '</B></FONT>';

# 順位の番号など
$HtagNumber_ = '<FONT COLOR="#800000"><B>';
$H_tagNumber = '</B></FONT>';

# 順位表における見だし
$HtagTH_ = '<FONT COLOR="#C00000"><B>';
$H_tagTH = '</B></FONT>';

# 開発計画の名前
$HtagComName_ = '<FONT COLOR="#d08000"><B>';
$H_tagComName = '</B></FONT>';

# 災害
$HtagDisaster_ = '<FONT COLOR="#ff0000"><B>';
$H_tagDisaster = '</B></FONT>';

# ローカル掲示板、観光者の書いた文字
$HtagLbbsSS_ = '<FONT COLOR="#0000ff"><B>';
$H_tagLbbsSS = '</B></FONT>';

# ローカル掲示板、島主の書いた文字
$HtagLbbsOW_ = '<FONT COLOR="#ff0000"><B>';
$H_tagLbbsOW = '</B></FONT>';
$HtagLbbsXX_ = '<FONT COLOR="#888888"><B>';
$H_tagLbbsXX = '</B></FONT>';
# 通常の文字色(これだけでなく、BODYタグのオプションもちゃんと変更すべし
$HnormalColor = '#000000';

# 順位表、セルの属性
$HbgTitleCell   = 'BGCOLOR="#ccffcc"'; # 順位表見出し
$HbgNumberCell  = 'BGCOLOR="#ccffcc"'; # 順位表順位
$HbgNameCell    = 'BGCOLOR="#ccffff"'; # 順位表島の名前
$HbgInfoCell    = 'BGCOLOR="#ccffff"'; # 順位表島の情報
$HbgCommentCell = 'BGCOLOR="#ccffcc"'; # 順位表コメント欄
$HbgInputCell   = 'BGCOLOR="#ccffcc"'; # 開発計画フォーム
$HbgMapCell     = 'BGCOLOR="#ccffcc"'; # 開発計画地図
$HbgCommandCell = 'BGCOLOR="#ccffcc"'; # 開発計画入力済み計画

#----------------------------------------------------------------------
# 好みによって設定する部分は以上
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# これ以降のスクリプトは、変更されることを想定していませんが、
# いじってもかまいません。
# コマンドの名前、値段などは解りやすいと思います。
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# 各種定数
#----------------------------------------------------------------------
# このファイル
$HthisFile = "$baseDir/hako-main.cgi";

# アプレット通信用 CGI
$HjavaFile = "$baseDir/hako-java.cgi";

# 地形番号
$HlandSea      = 0;  # 海
$HlandWaste    = 1;  # 荒地
$HlandPlains   = 2;  # 平地
$HlandTown     = 3;  # 町系
$HlandForest   = 4;  # 森
$HlandFarm     = 5;  # 農場
$HlandFactory  = 6;  # 工場
$HlandBase     = 7;  # ミサイル基地
$HlandDefence  = 8;  # 防衛施設
$HlandMountain = 9;  # 山
$HlandMonster  = 10; # 怪獣
$HlandSbase    = 11; # 海底基地
$HlandOil      = 12; # 海底油田
$HlandMonument = 13; # 記念碑
$HlandHaribote = 14; # ハリボテ
$Hlanddoubutu  = 15; 
$Hlandkiken = 16; # ハリボテ
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
# コマンド

# 計画番号の設定
# 整地系
$HcomPrepare  = 01; # 整地
$HcomPrepare2 = 02; # 地ならし
$HcomReclaim  = 03; # 埋め立て
$HcomDestroy  = 04; # 掘削
$HcomSellTree = 05; # 伐採
$HcomOnse    = 06; # 防衛施設建設
$HcomUmeta   = 07;
$Hcomkaitetu   = 10;

# 作る系
$HcomPlant    = 11; # 植林
$HcomFarm     = 12; # 農場整備
$HcomFactory  = 13; # 工場建設
$HcomMountain = 14; # 採掘場整備
$HcomBase     = 15; # ミサイル基地建設
$HcomDbase    = 16; # 防衛施設建設
$HcomSbase    = 17; # 海底基地建設
$HcomMonument = 18; # 記念碑建造
$HcomHaribote = 19; # ハリボテ設置
$Hcomdoubutu = 20; # 動物園建設　
$HcomOmise = 21; # 動物園建設
$HcomBank = 22;
$HcomTbase    = 23; # 防衛施設建設
$Hcomkiken = 24;
$Hcomkishou    = 25; # 防衛施設建設
$Hcomkukou    = 26; # 防衛施設建設
$Hcomyousho    = 27;
$Hcomhospit    = 28;
$HcomUbase    = 29;
# 発射系
$HcomMissileNC   = 30; # 陸地生成弾
$HcomMissileNM   = 31; # ミサイル発射
$HcomMissilePP   = 32; # PPミサイル発射
$HcomMissileST   = 33; # STミサイル発射
$HcomMissileLD   = 34; # 陸地破壊弾発射
$HcomSendMonster = 35; # 怪獣派遣
$HcomSendMonster2 = 36; # 怪獣派遣
$HcomMissileRE   = 37; # 陸地生成弾
$HcomMissileMK   = 38; # 陸地生成弾
$HcomMissileUC   = 39; # 陸地生成弾
$HcomMissileEM   = 40; # 陸地生成弾
# 運営系
$HcomDoNothing  = 41; # 資金繰り
$HcomSell       = 42; # 食料輸出
$HcomMoney      = 43; # 資金援助
$HcomFood       = 44; # 食料援助
$HcomPropaganda = 45; # 誘致活動
$HcomGiveup     = 46; # 島の放棄
$HcomImport     = 47;
$Hcomteikou     = 48;
$HcomMissileHP   = 51; # 陸地生成弾
$HcomOnpa   = 52;
$HcomInok   = 53;
$HcomGeki   = 54;
$HcomPori   = 55;
$HcomJous   = 56;
$HcomHatu  = 57;
$HcomGomi  = 58;
$HcomBouh  = 59;
$HcomMina  = 60;

# 自動入力系
$HcomAutoPrepare  = 61; # フル整地
$HcomAutoPrepare2 = 62; # フル地ならし
$HcomAutoDelete   = 63; # 全コマンド消去
$HcomReclaim2     = 64;
$HcomReho  = 65;
$HcomGoyu  = 66;
$HcomBoku  = 67;
$HcomTaiy  = 68;
$HcomDenb  = 69;
$HcomJusi  = 70;
$Hcomkouei        = 71; # フル整地
$Hcomkanei        = 72; # フル地ならし
$Hcomkouuti       = 73; # 全コマンド消去
$Hcomkanuti       = 74;
$Hcombouei       = 75; # 全コマンド消去
$Hcombouuti       = 76;
$Hcomreiei       = 77; # 全コマンド消去
$Hcomreiuti       = 78;
$Hcomhatei       = 79; # 全コマンド消去
$Hcomhatuti       = 80;

$Hcomsennyu        = 81; # フル整地
$Hcomheinyu        = 82; # フル地ならし
$Hcominonyu       = 83; # 全コマンド消去
$Hcomsende       = 84;
$Hcomheide        = 85; # フル整地
$Hcominode        = 86; # フル地ならし
$Hcomteiko        = 87; # フル整地
$Hcomkyouko        = 88; # フル地ならし

$Hcomtaifuu      = 91; # フル地ならし
$Hcomtunami       = 92; # 全コマンド消去
$Hcomfunka       = 93;
$Hcominseki        = 94; # フル整地
$Hcomdaiinseki       = 95; # フル地ならし
$Hcomjisin        = 96; # フル整地
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
$HcomStation  = 126; # 駅設置
$HcomRail     = 127; # 線路設置
$HcomMine      = 128; # 地雷設置
$HcomMineSuper = 129; # 高性能地雷設置
$HcomMineWrpe = 130; # 高性能地雷設置
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
# 基礎工事
$HcommandTotala = 10;
@HcomLista = ($HcomPrepare,$HcomPrepare2,$HcomReclaim,$HcomUmeta,$HcomDestroy,$HcomDestroy2,$Hcomjoyo,$Hcomkaitetu,$HcomPlant,$HcomSellTree);
# 建設
$HcommandTotalb = 60;
@HcomListb = ($HcomFarm,$Hcomyousho,$HcomBoku,$HcomFactory,$HcomMountain,$HcomHatu,$HcomFuha,$HcomTaiy,$HcomSuiry,$HcomTinet,$HcomChou,$HcomJusi,$HcomDenb,$HcomJous,$HcomGomi,$HcomGoyu,$HcomPori,$HcomShou,$Hcomhospit,$HcomStation,$HcomRail,$Hcomkukou,$HcomBouh,$HcomMina,$HcomOnse,$Hcomdoubutu,$HcomOmise,$HcomBank,$Hcomkiken,$Hcomkishou,$HcomOnpa,$HcomInok,$HcomEisei,$HcomReho,$HcomMine,$HcomMineSuper,$HcomMineWrpe,$HcomKoku,$HcomBase,$HcomSbase,$HcomDbase,$HcomUbase,$HcomTbase,$HcomHaribote,$HcomKeiba,$HcomFoot,$HcomYakyu,$HcomSki,$HcomSuiz,$HcomHotel,$HcomGolf,$HcomYuu,$HcomTenj,$HcomKaji,$HcomKouen,$HcomShok,$HcomTou,$HcomShiro,$HcomTuri,$HcomMonument);
# 貿易
$HcommandTotalc = 4;
@HcomListc = ($HcomSell,$HcomOilSell,$HcomImport,$HcomOilImport);
# 援助
$HcommandTotald = 7;
@HcomListd = ($HcomMoney,$HcomMoneyH,$HcomFood,$HcomFoodH,$HcomOil,$HcomOilH,$HcomSlag);
# ミサイル
$HcommandTotale = 12;
@HcomListe = ($HcomMissileNM,$HcomMissileEM,$HcomMissileNC,$HcomMissilePP,$HcomMissileST,$HcomMissileLD,$HcomMissileRE,$HcomMissileMK,$HcomMissileUC,$HcomMissileNEB,$HcomMissileHP,$HcomMissileUB);
# 怪獣派遣
$HcommandTotalf = 5;
@HcomListf = ($HcomSendMonster,$HcomSendMonster2,$HcomSendMonster3,$HcomSendMonster4,$HcomSendMonster5);
# 衛星
$HcommandTotalg = 14;
@HcomListg = ($Hcomkouei,$Hcomkanei,$Hcombouei,$Hcomhatei,$Hcomreiei,$HcomPMSei,$Hcomkouuti,$Hcomkanuti,$Hcombouuti,$Hcomhatuti,$Hcomreiuti,$HcomPMSuti,$HcomRazer,$HcomPMS);
# 気象兵器
$HcommandTotalh = 10;
@HcomListh = ($Hcomtaifuu,$Hcomtunami,$Hcomfunka,$Hcominseki,$Hcomdaiinseki,$Hcomjisin,$Hcomkasai,$HcomOoame,$Hcomtimya,$Hcomjibantinka);
# 同盟
$HcommandTotali = 8;
@HcomListi = ($Hcomsennyu,$Hcomheinyu,$Hcominonyu,$Hcomsende,$Hcomheide,$Hcominode,$Hcomteiko,$Hcomkyouko);
# その他
$HcommandTotalj = 10;
@HcomListj = ($HcomDoNothing,$HcomPropaganda,$HcomRob,$HcomRobST,$HcomShakufi,$HcomShakuse,$HcomShakuth,$HcomGeki,$Hcomteikou,$HcomGiveup);
# 自動入力
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
# 計画の名前と値段
$HcomName[$HcomPrepare]      = '整地';
$HcomCost[$HcomPrepare]      = 5;
$HcomName[$HcomPrepare2]     = '地ならし';
$HcomCost[$HcomPrepare2]     = 100;
$HcomName[$Hcomjoyo]      = '地雷撤去';
$HcomCost[$Hcomjoyo]      = 500;
$HcomName[$HcomReclaim]      = '埋め立て';
$HcomCost[$HcomReclaim]      = 150;
$HcomName[$HcomUmeta] = '突貫埋め立て';
$HcomCost[$HcomUmeta] = 300;
$HcomName[$HcomDestroy2]      = '突貫掘削';
$HcomCost[$HcomDestroy2]      = 400;
$HcomName[$HcomDestroy]      = '掘削';
$HcomCost[$HcomDestroy]      = 200;
$HcomName[$HcomOnse] = '温泉採掘';
$HcomCost[$HcomOnse] = 200;
$HcomName[$HcomPlant]        = '植林';
$HcomCost[$HcomPlant]        = 50;
$HcomName[$HcomSellTree]     = '伐採';
$HcomCost[$HcomSellTree]     = 0;
$HcomName[$Hcomyousho]        = '養殖所建設';
$HcomCost[$Hcomyousho]        = 100;
$HcomName[$Hcomkaitetu]     = '海上撤去';
$HcomCost[$Hcomkaitetu]     = 20;
$HcomName[$HcomFarm]         = '農場整備';
$HcomCost[$HcomFarm]         = 20;
$HcomName[$HcomFactory]      = '工場建設';
$HcomCost[$HcomFactory]      = 100;
$HcomName[$HcomMountain]     = '採掘場整備';
$HcomCost[$HcomMountain]     = 300;
$HcomName[$Hcomdoubutu] = '動物園建設';
$HcomCost[$Hcomdoubutu] = 700;
$HcomName[$HcomOmise] = 'デパート建設';
$HcomCost[$HcomOmise] = 1000;
$HcomName[$HcomBank] = '銀行建設';
$HcomCost[$HcomBank] = 1000;
$HcomName[$Hcomkiken] = '気象研究所建設';
$HcomCost[$Hcomkiken] = 5000;
$HcomName[$Hcomkishou] = '気象観測所建設';
$HcomCost[$Hcomkishou] = 2000;
$HcomName[$Hcomkukou] = '空港建設';
$HcomCost[$Hcomkukou] = 4000;
$HcomName[$Hcomhospit] = '病院建設';
$HcomCost[$Hcomhospit] = 300;
$HcomName[$HcomOnpa] = '特殊音波施設建設';
$HcomCost[$HcomOnpa] = 3000;
$HcomName[$HcomInok] = 'いのら研究所建設';
$HcomCost[$HcomInok] = 2000;
$HcomName[$HcomPori] = '警察署建設';
$HcomCost[$HcomPori] = 2000;
$HcomName[$HcomJous] = '浄水所整備';
$HcomCost[$HcomJous] = 100;
$HcomName[$HcomHatu] = '火力発電所整備';
$HcomCost[$HcomHatu] = 100;
$HcomName[$HcomFuha] = '風力発電所整備';
$HcomCost[$HcomFuha] = 10;
$HcomName[$HcomGomi] = 'ごみ処理施設整備';
$HcomCost[$HcomGomi] = 100;
$HcomName[$HcomBouh] = '防波堤整備';
$HcomCost[$HcomBouh] = 160;
$HcomName[$HcomMina] = '港整備';
$HcomCost[$HcomMina] = 30;
$HcomName[$HcomEisei] = '衛星追跡管制施設';
$HcomCost[$HcomEisei] = 10000;
$HcomName[$HcomJusi] = 'マイクロ波受信施設整備';
$HcomCost[$HcomJusi] = 10000;
$HcomName[$HcomDenb] = '電力売買公社建設';
$HcomCost[$HcomDenb] = 5000;
$HcomName[$HcomTaiy] = '太陽光発電所整備';
$HcomCost[$HcomTaiy] = 1000;
$HcomName[$HcomSuiry] = '水力発電所整備';
$HcomCost[$HcomSuiry] = 1500;
$HcomName[$HcomTinet] = '地熱発電所整備';
$HcomCost[$HcomTinet] = 800;
$HcomName[$HcomChou] = '波力発電所整備';
$HcomCost[$HcomChou] = 1000;
$HcomName[$HcomTuri] = '釣り堀整備';
$HcomCost[$HcomTuri] = 100;
$HcomName[$HcomGoyu] = 'ゴミ輸出機構建設';
$HcomCost[$HcomGoyu] = 10000;
$HcomName[$HcomBoku] = '牧場整備';
$HcomCost[$HcomBoku] = 500;
$HcomName[$HcomReho] = '低収束レーザー砲整備';
$HcomCost[$HcomReho] = 1000;
$HcomName[$HcomMine]         = '地雷設置';
$HcomCost[$HcomMine]         = 300;
$HcomName[$HcomMineSuper]    = '高性能地雷設置';
$HcomCost[$HcomMineSuper]    = 600;
$HcomName[$HcomMineWrpe]    = 'ワープ地雷設置';
$HcomCost[$HcomMineWrpe]    = 500;
$HcomName[$HcomKoku] = '軍総司令部建設';
$HcomCost[$HcomKoku] = 100;
$HcomName[$HcomKeiba] = '競馬場建設';
$HcomCost[$HcomKeiba] = 2000;
$HcomName[$HcomFoot] = 'サッカースタジアム建設';
$HcomCost[$HcomFoot] = 2000;
$HcomName[$HcomYakyu] = '野球場建設';
$HcomCost[$HcomYakyu] = 1500;
$HcomName[$HcomSki] = '屋内スキー場建設';
$HcomCost[$HcomSki] = 3000;
$HcomName[$HcomSuiz] = '水族館建設';
$HcomCost[$HcomSuiz] = 1200;
$HcomName[$HcomHotel] = 'リゾートホテル建設';
$HcomCost[$HcomHotel] = 2000;
$HcomName[$HcomGolf] = 'ゴルフ場建設';
$HcomCost[$HcomGolf] = 1300;
$HcomName[$HcomYuu] = '遊園地建設';
$HcomCost[$HcomYuu] = 1500;
$HcomName[$HcomTenj] = '展示場建設';
$HcomCost[$HcomTenj] = 1000;
$HcomName[$HcomKaji] = 'カジノ建設';
$HcomCost[$HcomKaji] = 500;
$HcomName[$HcomKouen] = '公園建設';
$HcomCost[$HcomKouen] = 100;
$HcomName[$HcomShok] = '植物園建設';
$HcomCost[$HcomShok] = 1500;
$HcomName[$HcomTou] = '塔建設';
$HcomCost[$HcomTou] = 1000;
$HcomName[$HcomShiro] = '城建設';
$HcomCost[$HcomShiro] = 3000;
$HcomName[$HcomShou] = '消防署建設';
$HcomCost[$HcomShou] = 3000;
$HcomName[$HcomStation]      = '駅建設';
$HcomCost[$HcomStation]      = 500;
$HcomName[$HcomRail]         = '線路敷設';
$HcomCost[$HcomRail]         = 100;
$HcomName[$HcomBase]         = 'ミサイル基地建設';
$HcomCost[$HcomBase]         = 300;
$HcomName[$HcomSbase]        = '海底基地建設';
$HcomCost[$HcomSbase]        = 8000;
$HcomName[$HcomDbase]        = '防衛施設建設';
$HcomCost[$HcomDbase]        = 800;
$HcomName[$HcomUbase]        = '広域防衛施設建設';
$HcomCost[$HcomUbase]        = 3000;
$HcomName[$Hcomteikou]        = '攻撃停止を要請';
$HcomCost[$Hcomteikou]        = 0;
$HcomName[$HcomTbase] = 'ST防衛施設建設';
$HcomCost[$HcomTbase] = 1500;
$HcomName[$HcomHaribote]     = 'ハリボテ設置';
$HcomCost[$HcomHaribote]     = 1;
$HcomName[$HcomMonument]     = '記念碑建造';
$HcomCost[$HcomMonument]     = 9999;
$HcomName[$HcomMissileNM]    = 'ミサイル発射';
$HcomCost[$HcomMissileNM]    = 20;
$HcomName[$HcomMissilePP]    = 'PPミサイル発射';
$HcomCost[$HcomMissilePP]    = 50;
$HcomName[$HcomMissileST]    = 'STミサイル発射';
$HcomCost[$HcomMissileST]    = 50;
$HcomName[$HcomMissileLD]    = '陸地破壊弾発射';
$HcomCost[$HcomMissileLD]    = 100;
$HcomName[$HcomMissileRE]        = '陸地生成弾発射';
$HcomCost[$HcomMissileRE]        = 150;
$HcomName[$HcomMissileMK]        = '怪獣捕縛弾発射';
$HcomCost[$HcomMissileMK]        = 50;
$HcomName[$HcomMissileUC]        = '核ミサイル発射';
$HcomCost[$HcomMissileUC]        = 5000;
$HcomName[$HcomMissileNEB]        = '中性子ミサイル発射';
$HcomCost[$HcomMissileNEB]        = 4000;
$HcomName[$HcomMissileEM]        = '簡易ミサイル発射';
$HcomCost[$HcomMissileEM]        = 10;
$HcomName[$HcomMissileNC] = '低精度ミサイル発射';
$HcomCost[$HcomMissileNC] = 15;
$HcomName[$HcomMissileHP] = '体力増強ミサイル発射';
$HcomCost[$HcomMissileHP] = 50;
$HcomName[$HcomMissileUB] = 'アンチシールドミサイル発射';
$HcomCost[$HcomMissileUB] = 500;
$HcomName[$HcomSendMonster]  = '怪獣派遣';
$HcomCost[$HcomSendMonster]  = 3000;
$HcomName[$HcomSendMonster2]  = '鉄鋼兵派遣';
$HcomCost[$HcomSendMonster2]  = 2000;
$HcomName[$HcomSendMonster3]  = '特攻部隊派遣';
$HcomCost[$HcomSendMonster3]  = 5000;
$HcomName[$HcomSendMonster4]  = 'FX-330派遣';
$HcomCost[$HcomSendMonster4]  = 7000;
$HcomName[$HcomSendMonster5]  = 'FX-330A派遣';
$HcomCost[$HcomSendMonster5]  = 20000;
$HcomName[$Hcomtaifuu]   = '台風操作';
$HcomCost[$Hcomtaifuu]   = 2500;
$HcomName[$Hcomtunami]  = '津波誘因';
$HcomCost[$Hcomtunami]  = 3000;
$HcomName[$Hcomfunka] = '噴火誘因';
$HcomCost[$Hcomfunka] = 3000;
$HcomName[$Hcominseki]   = '隕石召還';
$HcomCost[$Hcominseki]   = 5000;
$HcomName[$Hcomdaiinseki]   = '大隕石召還';
$HcomCost[$Hcomdaiinseki]   = 9000;
$HcomName[$Hcomjisin]   = '地震誘因';
$HcomCost[$Hcomjisin]   = 6000;
$HcomName[$Hcomkasai]   = '火災誘因';
$HcomCost[$Hcomkasai]   = 3000;
$HcomName[$Hcomtimya]   = '地脈変動誘因';
$HcomCost[$Hcomtimya]   = 7000;
$HcomName[$HcomRazer]   = 'レーザー発射';
$HcomCost[$HcomRazer]   = 1000;
$HcomName[$HcomPMS]   = 'サテライトPMS砲発射';
$HcomCost[$HcomPMS]   = 3000;
$HcomName[$Hcomjibantinka]   = '地盤沈下誘因';
$HcomCost[$Hcomjibantinka]   = 10000;
$HcomName[$HcomOoame]   = '大雨誘因';
$HcomCost[$HcomOoame]   = 500;
$HcomName[$HcomDoNothing]    = '資金繰り';
$HcomCost[$HcomDoNothing]    = 0;
$HcomName[$HcomSell]         = '食料輸出';
$HcomCost[$HcomSell]         = -100;
$HcomName[$HcomOilSell]         = '石油輸出';
$HcomCost[$HcomOilSell]         = 10;
$HcomName[$HcomMoney]        = '資金援助';
$HcomCost[$HcomMoney]        = 100;
$HcomName[$HcomMoneyH]        = 'ST資金援助';
$HcomCost[$HcomMoneyH]        = 100;
$HcomName[$HcomImport]         = '食料輸入';
$HcomCost[$HcomImport]         = 100;
$HcomName[$HcomOilImport]         = '石油輸入';
$HcomCost[$HcomOilImport]         = 10;
$HcomName[$HcomFood]         = '食料援助';
$HcomCost[$HcomFood]         = -100;
$HcomName[$HcomFoodH]         = 'ST食料援助';
$HcomCost[$HcomFoodH]         = -100;
$HcomName[$HcomOil]         = '石油援助';
$HcomCost[$HcomOil]         = 10;
$HcomName[$HcomOilH]         = 'ST石油援助';
$HcomCost[$HcomOilH]         = 10;
$HcomName[$HcomSlag]         = 'ゴミ輸送';
$HcomCost[$HcomSlag]         = -1;
$HcomName[$HcomPropaganda]   = '誘致活動';
$HcomCost[$HcomPropaganda]   = 1000;
$HcomName[$HcomGeki]         = '怪獣撃退';
$HcomCost[$HcomGeki]         = 1000;
$HcomName[$HcomShakufi]         = '資金借り入れ(10回払い)';
$HcomCost[$HcomShakufi]         = 0;
$HcomName[$HcomShakuse]   = '資金借り入れ(50回払い)';
$HcomCost[$HcomShakuse]   = 0;
$HcomName[$HcomShakuth]         = '資金借り入れ(100回払い)';
$HcomCost[$HcomShakuth]         = 0;
$HcomName[$HcomRob]          = '強奪';
$HcomCost[$HcomRob]          = 100;
$HcomName[$HcomRobST]          = 'ST強奪';
$HcomCost[$HcomRobST]          = 200;
$HcomName[$Hcomkouei]  = '攻撃衛星打ち上げ';
$HcomCost[$Hcomkouei]  = 3000;
$HcomName[$Hcomkanei] = '監視衛星打ち上げ';
$HcomCost[$Hcomkanei] = 4000;
$HcomName[$Hcomkouuti]   = '攻撃衛星撃ち落とし';
$HcomCost[$Hcomkouuti]   = 1000;
$HcomName[$Hcomkanuti]   = '監視衛星撃ち落とし';
$HcomCost[$Hcomkanuti]   = 1000;
$HcomName[$Hcombouei] = '防御衛星打ち上げ';
$HcomCost[$Hcombouei] = 10000;
$HcomName[$Hcombouuti]   = '防御衛星撃ち落とし';
$HcomCost[$Hcombouuti]   = 1000;
$HcomName[$Hcomreiei] = 'レーザー衛星打ち上げ';
$HcomCost[$Hcomreiei] = 10000;
$HcomName[$Hcomreiuti]   = 'レーザー衛星撃ち落とし';
$HcomCost[$Hcomreiuti]   = 1000;
$HcomName[$Hcomhatei] = '発電衛星打ち上げ';
$HcomCost[$Hcomhatei] = 10000;
$HcomName[$Hcomhatuti]   = '発電衛星撃ち落とし';
$HcomCost[$Hcomhatuti]   = 1000;
$HcomName[$HcomPMSei] = 'PMS衛星整備';
$HcomCost[$HcomPMSei] = 20000;
$HcomName[$HcomPMSuti]   = 'PMS衛星撃ち落とし';
$HcomCost[$HcomPMSuti]   = 1000;
$HcomName[$Hcomsennyu]   = '戦争愛好同盟に加盟';
$HcomCost[$Hcomsennyu]   = 1;
$HcomName[$Hcomheinyu]   = '平和愛好同盟に加盟';
$HcomCost[$Hcomheinyu]   = 1;
$HcomName[$Hcominonyu]  = '反いのら同盟に加盟';
$HcomCost[$Hcominonyu]  = 1;
$HcomName[$Hcomsende] = '戦争愛好同盟から脱退';
$HcomCost[$Hcomsende] = 1;
$HcomName[$Hcomheide]   = '平和愛好同盟から脱退';
$HcomCost[$Hcomheide]   = 1;
$HcomName[$Hcominode]   = '反いのら同盟から脱退';
$HcomCost[$Hcominode]   = 1;
$HcomName[$Hcomteiko]   = '帝国軍に参加';
$HcomCost[$Hcomteiko]   = 0;
$HcomName[$Hcomkyouko]   = '共和国軍に参加';
$HcomCost[$Hcomkyouko]   = 0;
$HcomName[$HcomGiveup]       = '島の放棄';
$HcomCost[$HcomGiveup]       = 0;
$HcomName[$HcomAutoPrepare]  = '整地自動入力';
$HcomCost[$HcomAutoPrepare]  = 0;
$HcomName[$HcomAutoPrepare2] = '地ならし自動入力';
$HcomCost[$HcomAutoPrepare2] = 0;
$HcomName[$HcomReclaim2]   = '浅瀬埋め立て自動入力';
$HcomCost[$HcomReclaim2]   = 0;
$HcomName[$HcomReclaim3]   = '浅瀬突貫埋め立て自動入力';
$HcomCost[$HcomReclaim3]   = 0;
$HcomName[$HcomAutoDelete]   = '全計画を白紙撤回';
$HcomCost[$HcomAutoDelete]   = 0;

#----------------------------------------------------------------------
# 変数
#----------------------------------------------------------------------

# COOKIE
my($defaultID);       # 島の名前
my($defaultTarget);   # ターゲットの名前


# 島の座標数
$HpointNumber = $HislandSize * $HislandSize;

#----------------------------------------------------------------------
# メイン
#----------------------------------------------------------------------

# jcode.plをrequire
require($jcode);

# 「戻る」リンク
$HtempBack = "<A HREF=\"$HthisFile\">${HtagBig_}トップへ戻る${H_tagBig}</A>";

# ロックをかける
if(!hakolock()) {
    # ロック失敗
    # ヘッダ出力
    tempHeader();

    # ロック失敗メッセージ
    tempLockFail();

    # フッタ出力
    tempFooter();

    # 終了
    exit(0);
}

# 乱数の初期化
srand(time^$$);

# COOKIE読みこみ
cookieInput();

# CGI読みこみ
cgiInput();

# 島データの読みこみ
if(readIslandsFile($HcurrentID) == 0) {
    unlock();
    tempHeader();
    tempNoDataFile();
    tempFooter();
    exit(0);
}

# テンプレートを初期化
tempInitialize();

# COOKIE出力
cookieOutput();

if($HmainMode eq 'owner') {

    # 開発モード
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
# ヘッダ出力
tempHeader();

if($HmainMode eq 'turn') {
    # ターン進行
    require('hako-turn.cgi');
    require('hako-top.cgi');
    turnMain();

} elsif($HmainMode eq 'new') {
    # 島の新規作成
    require('hako-turn.cgi');
    require('hako-map.cgi');
    newIslandMain();

} elsif($HmainMode eq 'print') {
    # 観光モード
    require('hako-map.cgi');
    printIslandMain();


} elsif($HmainMode eq 'command') {
    # コマンド入力モード
    require('hako-map.cgi');
    commandMain();
} elsif($HmainMode eq 'Shuu') {
    # コマンド入力モード
    require('hako-map.cgi');
    ShuuMain();
} elsif($HmainMode eq 'comment') {
    # コメント入力モード
    require('hako-map.cgi');
    commentMain();

} elsif($HmainMode eq 'lbbs') {

    # ローカル掲示板モード
    require('hako-map.cgi');
    localBbsMain();

} elsif($HmainMode eq 'change') {
    # 情報変更モード
    require('hako-turn.cgi');
    require('hako-top.cgi');
    changeMain();

} elsif($HmainMode eq 'chowner') {
  # オーナー名変更モード
  require('hako-turn.cgi');
  require('hako-top.cgi');
  changeOwner();

} elsif($HmainMode eq 'chflag') {
  # オーナー名変更モード
  require('hako-turn.cgi');
  require('hako-top.cgi');
  changeFlag();

} else {
    # その他の場合はトップページモード
    require('hako-top.cgi');
    topPageMain();
}
}
# フッタ出力
tempFooter();

# 終了
exit(0);

# コマンドを前にずらす
sub slideFront {
    my($command, $number) = @_;
    my($i);

    # それぞれずらす
    splice(@$command, $number, 1);

    # 最後に資金繰り
    $command->[$HcommandMax - 1] = {
	'kind' => $HcomDoNothing,
	'target' => 0,
	'x' => 0,
	'y' => 0,
	'arg' => 0
	};
}

# コマンドを後にずらす
sub slideBack {
    my($command, $number) = @_;
    my($i);

    # それぞれずらす
    return if $number == $#$command;
    pop(@$command);
    splice(@$command, $number, 0, $command->[$number]);
}

#----------------------------------------------------------------------
# 島データ入出力
#----------------------------------------------------------------------

# 全島データ読みこみ
sub readIslandsFile {
    my($num) = @_; # 0だと地形読みこまず
                   # -1だと全地形を読む
                   # 番号だとその島の地形だけは読みこむ

    # データファイルを開く
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
    # 各パラメータの読みこみ
    $HislandTurn = int(<IN>); # ターン数
    if($HislandTurn == 0) {
	return 0;
    }
    $HislandLastTime = int(<IN>); # 最終更新時間
    if($HislandLastTime == 0) {
	return 0;
    }
    $HislandNumber   = int(<IN>); 
    $HislandNextID   = int(<IN>); # 次に割り当てるID
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

   # ターン処理判定
    my($now) = time;
    if((($Hdebug == 1) && 
	($HmainMode eq 'Hdebugturn')) ||
       (($now - $HislandLastTime) >= $HunitTime)) {
	$HmainMode = 'turn';
	$num = -1; 
    }

    # 島の読みこみ
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	 $Hislands[$i] = readIsland($num);
	 $HidToNumber{$Hislands[$i]->{'id'}} = $i;
    }

    # ファイルを閉じる
    close(IN);

    return 1;
}

# 島ひとつ読みこみ
sub readIsland {
    my($num) = @_;
    my($name, $id, $prize, $absent, $comment, $password, $money, $food,
       $pop, $area, $farm, $factory, $mountain, $birth, $score, $monsnumber,
       $kouei, $kanei, $sen, $hei, $ino);
    $name = <IN>;		# 島の名前,島が作成されたターン
    chomp($name);
    $name =~ s/,(.*)$//g;	# -島の名前
    $birth = int($1);		# -島が作成されたターン
    $id = int(<IN>);		# ID番号
    $prize = <IN>;		# 受賞
    chomp($prize);
    $absent = int(<IN>);	# 連続資金繰り数
    $comment = <IN>;		# コメント
    chomp($comment);
    $password = <IN>;		# 暗号化パスワード
    chomp($password);
    $money = int(<IN>);		# 資金
    $food = int(<IN>);		# 食料
    $pop = int(<IN>);		# 人口
    $area = int(<IN>);		# 広さ
    $farm = int(<IN>);		# 農場
    $factory = int(<IN>);	# 工場
    $mountain = int(<IN>);	# 採掘場
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
# HidToNameテーブルへ保存
    $HidToName{$id} = $name;	# 

    # 地形
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

	# コマンド
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

	# ローカル掲示板
	for($i = 0; $i < $HlbbsMax; $i++) {
	    $line = <IIN>;
	    chomp($line);
	    $lbbs[$i] = $line;
	}

	close(IIN);
    }

    # 島型にして返す
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
# 全島データ書き込み
sub writeIslandsFile {
    my($num) = @_;

    # ファイルを開く
    my($retry) = $HretryCount;
    while (! open(OUT, ">${HdirName}/hakojima.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 暫定的に終了させます
	    return 1;
	}

	# 0.2 秒 sleep
	select undef, undef, undef, 0.2;
    }
   while (! open(MOUT, ">${HdirName2}/hflag.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 暫定的に終了させます
	    return 1;
	}

	# 0.2 秒 sleep
	select undef, undef, undef, 0.2;
    }
   while (! open(HOUT, ">${HdirName2}/howner.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 暫定的に終了させます
	    return 1;
	}

	# 0.2 秒 sleep
	select undef, undef, undef, 0.2;
    }
   while (! open(GOUT, ">${HdirName2}/haddre.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 暫定的に終了させます
	    return 1;
	}

	# 0.2 秒 sleep
	select undef, undef, undef, 0.2;
    }
   while (! open(SOUT, ">${HdirName2}/hkanko.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 暫定的に終了させます
	    return 1;
	}

	# 0.2 秒 sleep
	select undef, undef, undef, 0.2;
    }

    while (! open(BOUT, ">${HdirName}/hprize.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 暫定的に終了させます
	    return 1;
	}

	# 0.2 秒 sleep
	select undef, undef, undef, 0.2;
    }
    while (! open(COUT, ">${HdirName}/heisei.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 暫定的に終了させます
	    return 1;
	}

	# 0.2 秒 sleep
	select undef, undef, undef, 0.2;
    }
    while (! open(DOUT, ">${HdirName}/hshoyu.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 暫定的に終了させます
	    return 1;
	}

	# 0.2 秒 sleep
	select undef, undef, undef, 0.2;
    }
    while (! open(EOUT, ">${HdirName}/hsonota.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 暫定的に終了させます
	    return 1;
	}

	# 0.2 秒 sleep
	select undef, undef, undef, 0.2;
    }
   while (! open(FOUT, ">${HdirName}/hpara.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 暫定的に終了させます
	    return 1;
	}

	# 0.2 秒 sleep
	select undef, undef, undef, 0.2;
    }
   while (! open(TOUT, ">${HdirName}/hpase.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 暫定的に終了させます
	    return 1;
	}

	# 0.2 秒 sleep
	select undef, undef, undef, 0.2;
    }
    # 各パラメータ書き込み
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
     # 島の書きこみ
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	 writeIsland($Hislands[$i], $num);
    }

    # ファイルを閉じる
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
    # 本来の名前にする
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

    # ファイルを開く
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
    # 各パラメータ書き込み
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
     # 島の書きこみ
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	 writeIslands($Hislands[$i], $num);
    }

    # ファイルを閉じる
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
    # 本来の名前にする
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
# 島ひとつ書き込み
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
# 地形
    if(($num <= -1) || ($num == $island->{'id'})) {
	my ($retry) = $HretryCount;

	while (! open(IOUT, ">${HdirName}/islandtmp.$island->{'id'}"))
	{
	    $retry--;
	    if ($retry <= 0)
	    {
		# 2.02 暫定的に終了させます
		return 1;
	    }

	    # 0.2 秒 sleep
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

	# コマンド
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

	# ローカル掲示板
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

	# コマンド
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

	# ローカル掲示板
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

    # ファイルを開く
    my($retry) = $HretryCount;
    while (! open(OUT, ">${HdirName}/hakojima.tmp"))
    {
	$retry--;
	if ($retry <= 0)
	{
	    # 2.02 暫定的に終了させます
	    return 1;
	}

	# 0.2 秒 sleep
	select undef, undef, undef, 0.2;
    }

    # 各パラメータ書き込み
    print OUT "$HislandTurn\n";
    print OUT "$HislandLastTime\n";
    print OUT "$HislandNumber\n";
    print OUT "$HislandNextID\n";

     # 島の書きこみ
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

    # ファイルを閉じる
    close(OUT);

    # 本来の名前にする
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
		# 2.02 暫定的に終了させます
		return 1;
	    }

	    # 0.2 秒 sleep
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

	# コマンド
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

	# ローカル掲示板
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
# 入出力
#----------------------------------------------------------------------

# 標準出力への出力
sub out {
    print STDOUT jcode::sjis($_[0]);
}

# デバッグログ
sub HdebugOut {
   open(DOUT, ">>debug.log");
   print DOUT ($_[0]);
   close(DOUT);
}

# CGIの読みこみ
sub cgiInput {
    my($line, $getLine);

    # 入力を受け取って日本語コードをEUCに
    $line = <>;
    $line =~ tr/+/ /;
    $line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    $line = jcode::euc($line);
    $line =~ s/[\x00-\x1f\,]//g;

    # GETのやつも受け取る
    $getLine = $ENV{'QUERY_STRING'};

    # 対象の島
    if($line =~ /CommandButton([0-9]+)=/) {
	# コマンド送信ボタンの場合
	$HcurrentID = $1;
	$defaultID = $1;
    }
    if($line =~ /ShuuButton([0-9]+)=/) {
	# コマンド送信ボタンの場合
	$HcurrentID = $1;
	$defaultID = $1;
    }
if($line =~ /ChangeMode([0-9]+)=/) {
	$HcurrentID = $1;
	$defaultID = $1;
}
    if($line =~ /ISLANDNAME=([^\&]*)\&/){
	# 名前指定の場合
	$HcurrentName = cutColumn($1, 32);
    }
if($line =~ /FLAGNAME=([^\&]*)\&/){
  # オーナー名の場合
  $HcurrentFlagName = cutColumn($1, 64);
}
if($line =~ /OWNERNAME=([^\&]*)\&/){
  # オーナー名の場合
  $HcurrentOwnerName = cutColumn($1, 32);
}

    if($line =~ /ISLANDID=([0-9]+)\&/){
	# その他の場合
	$HcurrentID = $1;
	$defaultID = $1;
    }

    # パスワード
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

    # メッセージ
    if($line =~ /MESSAGE=([^\&]*)\&/) {
	$Hmessage = cutColumn($1, 160);
    }

    # ローカル掲示板
    if($line =~ /LBBSNAME=([^\&]*)\&/) {
	$HlbbsName = $1;
	$HdefaultName = $1;
    }
    if($line =~ /LBBSMESSAGE=([^\&]*)\&/) {
	$HlbbsMessage = $1;
    }

    # main modeの取得
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
	    # 観光者
	    $HlbbsMode = 0;
	} elsif($1 eq 'OW') {
	    # 島主
	    $HlbbsMode = 1;
	} elsif($1 eq 'FO') {
	    # 他の島主
$Hsee = 0;
if($line =~ /see=secret\&/){
$Hsee = 1;
}
	    $HlbbsMode = 3;
	    $HforeignerID = $HcurrentID;
	} else {
	    # 削除
	    $HlbbsMode = 2;
	}
	$HcurrentID = $2;

	# 削除かもしれないので、番号を取得
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

	# コマンドモードの場合、コマンドの取得
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

  # 本来の名前にする
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

  # 本来の名前にする
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

  # 本来の名前にする
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

  # 本来の名前にする
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

  # 本来の名前にする
  unlink("${HdirName2}/hkanko.dat");
  rename("${HdirName2}/hkanko.tmp", "${HdirName2}/hkanko.dat");
}
#cookie入力
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

#cookie出力
sub cookieOutput {
    my($cookie, $info);

    # 消える期限の設定
    my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	gmtime(time + 30 * 86400); # 現在 + 30日

    # 2ケタ化
    $year += 1900;
    if ($date < 10) { $date = "0$date"; }
    if ($hour < 10) { $hour = "0$hour"; }
    if ($min < 10) { $min  = "0$min"; }
    if ($sec < 10) { $sec  = "0$sec"; }

    # 曜日を文字に
    $day = ("Sunday", "Monday", "Tuesday", "Wednesday",
	    "Thursday", "Friday", "Saturday")[$day];

    # 月を文字に
    $mon = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
	    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")[$mon];

    # パスと期限のセット
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
	# 自動系以外
	$cookie .= "Set-Cookie: ${HthisFile}KIND=($HcommandKind) $info";
    }

    out($cookie);
}

#------------------
#----------------------------------------------------------------------
# ユーティリティ
#----------------------------------------------------------------------
sub hakolock {
    if($lockMode == 1) {
	# directory式ロック
	return hakolock1();

    } elsif($lockMode == 2) {
	# flock式ロック
	return hakolock2();
    } elsif($lockMode == 3) {
	# symlink式ロック
	return hakolock3();
    } else {
	# 通常ファイル式ロック
	return hakolock4();
    }
}

sub hakolock1 {
    # ロックを試す
    if(mkdir('hakojimalock', $HdirMode)) {
	# 成功
	return 1;
    } else {
	# 失敗
	my($b) = (stat('hakojimalock'))[9];
	if(($b > 0) && ((time() -  $b)> $unlockTime)) {
	    # 強制解除
	    unlock();

	    # ヘッダ出力
	    tempHeader();

	    # 強制解除メッセージ
	    tempUnlock();

	    # フッタ出力
	    tempFooter();

	    # 終了
	    exit(0);
	}
	return 0;
    }
}

sub hakolock2 {
    open(LOCKID, '>>hakojimalockflock');
    if(flock(LOCKID, 2)) {
	# 成功
	return 1;
    } else {
	# 失敗
	return 0;
    }
}

sub hakolock3 {
    # ロックを試す
    if(symlink('hakojimalockdummy', 'hakojimalock')) {
	# 成功
	return 1;
    } else {
	# 失敗
	my($b) = (lstat('hakojimalock'))[9];
	if(($b > 0) && ((time() -  $b)> $unlockTime)) {
	    # 強制解除
	    unlock();

	    # ヘッダ出力
	    tempHeader();

	    # 強制解除メッセージ
	    tempUnlock();

	    # フッタ出力
	    tempFooter();

	    # 終了
	    exit(0);
	}
	return 0;
    }
}

sub hakolock4 {
    # ロックを試す
    if(unlink('key-free')) {
	# 成功
	open(OUT, '>key-locked');
	print OUT time;
	close(OUT);
	return 1;
    } else {
	# ロック時間チェック
	if(!open(IN, 'key-locked')) {
	    return 0;
	}

	my($t);
	$t = <IN>;
	close(IN);
	if(($t != 0) && (($t + $unlockTime) < time)) {
	    # 120秒以上経過してたら、強制的にロックを外す
	    unlock();

	    # ヘッダ出力
	    tempHeader();

	    # 強制解除メッセージ
	    tempUnlock();

	    # フッタ出力
	    tempFooter();

	    # 終了
	    exit(0);
	}
	return 0;
    }
}

# ロックを外す
sub unlock {
    if($lockMode == 1) {
	# directory式ロック
	rmdir('hakojimalock');

    } elsif($lockMode == 2) {
	# flock式ロック
	close(LOCKID);

    } elsif($lockMode == 3) {
	# symlink式ロック
	unlink('hakojimalock');
    } else {
	# 通常ファイル式ロック
	my($i);
	$i = rename('key-locked', 'key-free');
    }
}

# 小さい方を返す
sub min {
    return ($_[0] < $_[1]) ? $_[0] : $_[1];
}

# パスワードエンコード
sub encode {
    if($cryptOn == 1) {
	return crypt($_[0], 'h2');
    } else {
	return $_[0];
    }
}

# パスワードチェック
sub checkPassword {
    my($p1, $p2) = @_;

    # nullチェック
    if($p2 eq '') {
	return 0;
    }

    # マスターパスワードチェック
    if($masterPassword eq $p2) {
	return 1;
    }

    # 本来のチェック
    if($p1 eq encode($p2)) {
	return 1;
    }

    return 0;
}

# 1000億単位丸めルーチン
sub aboutMoney {
    my($m) = @_;
    if($m < 500) {
	return "推定500${HunitMoney}未満";
    } else {
	$m = int(($m + 500) / 1000);
	return "推定${m}000${HunitMoney}";
    }
}

# エスケープ文字の処理
sub htmlEscape {
    my($s) = @_;
    $s =~ s/&/&amp;/g;
    $s =~ s/</&lt;/g;
    $s =~ s/>/&gt;/g;
    $s =~ s/\"/&quot;/g; #"
    return $s;
}

# 80ケタに切り揃え
sub cutColumn {
    my($s, $c) = @_;
    if(length($s) <= $c) {
	return $s;
    } else {
	# 合計80ケタになるまで切り取り
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

# 島の名前から番号を得る(IDじゃなくて番号)
sub nameToNumber {
    my($name) = @_;

    # 全島から探す
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	if($Hislands[$i]->{'name'} eq $name) {
	    return $i;
	}
    }

    # 見つからなかった場合
    return -1;
}

# 怪獣の情報
sub monsterSpec {
    my($lv) = @_;

    # 種類
    my($kind) = int($lv / 10);

    # 名前
    my($name);
    $name = $HmonsterName[$kind];

    # 体力
    my($hp) = $lv - ($kind * 10);
    
    return ($kind, $name, $hp);
}

# 経験地からレベルを算出
sub expToLevel {
    my($kind, $exp) = @_;
    my($i);
    if($kind == $HlandBase) {
	# ミサイル基地
	for($i = $maxBaseLevel; $i > 1; $i--) {
	    if($exp >= $baseLevelUp[$i - 2]) {
		return $i;
	    }
	}
	return 1;
    } else {
	# 海底基地
	for($i = $maxSBaseLevel; $i > 1; $i--) {
	    if($exp >= $sBaseLevelUp[$i - 2]) {
		return $i;
	    }
	}
	return 1;
    }

}

# (0,0)から(size - 1, size - 1)までの数字が一回づつ出てくるように
# (@Hrpx, @Hrpy)を設定
sub makeRandomPointArray {
    # 初期値
    my($y);
    @Hrpx = (0..$HislandSize-1) x $HislandSize;
    for($y = 0; $y < $HislandSize; $y++) {
	push(@Hrpy, ($y) x $HislandSize);
    }

    # シャッフル
    my ($i);
    for ($i = $HpointNumber; --$i; ) {
	my($j) = int(rand($i+1)); 
	if($i == $j) { next; }
	@Hrpx[$i,$j] = @Hrpx[$j,$i];
	@Hrpy[$i,$j] = @Hrpy[$j,$i];
    }
}

# 0から(n - 1)の乱数
sub random {
    return int(rand(1) * $_[0]);
}

#----------------------------------------------------------------------
# ログ表示
#----------------------------------------------------------------------
# ファイル番号指定でログ表示
sub logFilePrint {
    my($fileNumber, $id, $mode) = @_;
    open(LIN, "${HdirName}/hakojima.log$_[0]");
    my($line, $m, $turn, $id1, $id2, $message);
    while($line = <LIN>) {
	$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),(.*)$/;
	($m, $turn, $id1, $id2, $message) = ($1, $2, $3, $4, $5);

	# 機密関係
	if($m == 1) {
	    if(($mode == 0) || ($id1 != $id)) {
		# 機密表示権利なし
		next;
	    }
	    $m = '<B>(機密)</B>';
	} else {
	    $m = '';
	}

	# 表示的確か
	if($id != 0) {
	    if(($id != $id1) &&
	       ($id != $id2)) {
		next;
	    }
	}

	# 表示
	out("<NOBR>${HtagNumber_}ターン$turn$m${H_tagNumber}：$message</NOBR><BR>\n");
    }
    close(LIN);
}

#----------------------------------------------------------------------
# テンプレート
#----------------------------------------------------------------------
# 初期化
sub tempInitialize {
    # 島セレクト(デフォルト自分)
    $HislandList = getIslandList($defaultID);
    $HtargetList = getIslandList($defaultTarget);
}

# 島データのプルダウンメニュー用
sub getIslandList {
    my($select) = @_;
    my($list, $name, $id, $s, $i);

    #島リストのメニュー
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
	    "<OPTION VALUE=\"$id\" $s>${name}島\n";
    }
    return $list;
}


# ヘッダ
sub tempHeader {
if($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/ and $ENV{HTTP_USER_AGENT}=~/Windows/){
print qq{Content-type: text/html; charset=Shift_JIS\n};
print qq{Content-encoding: gzip\n\n};
# gzipのパスの変更が必要です。
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
# gzipのパスの変更が必要です。
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
# フッタ
sub tempFooter {
    out(<<END);
<HR>
<P align=center>
<A HREF="$mentehtml">メンテナンスモード</A><br>
管理者:$adminName(<A HREF="mailto:$email">$email</A>)<BR>
<A HREF="http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html">箱庭諸島スクリプト配布元</A><br>
箱庭諸島のページ(<A HREF="http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html">http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html</A>)<BR>
Lits箱庭用改造：MT<BR>
</BODY>
</BODY>
</HTML>
END
}

# ロック失敗
sub tempLockFail {
    # タイトル
    out(<<END);
${HtagBig_}同時アクセスエラーです。<BR>
ブラウザの「戻る」ボタンを押し、<BR>
しばらく待ってから再度お試し下さい。${H_tagBig}$HtempBack
END
}

# 強制解除
sub tempUnlock {
    # タイトル
    out(<<END);
${HtagBig_}前回のアクセスが異常終了だったようです。<BR>
ロックを強制解除しました。${H_tagBig}$HtempBack
END
}

# hakojima.datがない
sub tempNoDataFile {
    out(<<END);
${HtagBig_}データファイルが開けません。${H_tagBig}$HtempBack
END
}

# パスワード間違い
sub tempWrongPassword {
    out(<<END);
${HtagBig_}パスワードが違います。${H_tagBig}$HtempBack
END
}

# 何か問題発生
sub tempProblem {
    out(<<END);
${HtagBig_}問題発生、とりあえず戻ってください。${H_tagBig}$HtempBack
END
}
