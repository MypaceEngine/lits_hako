#!/bin/perl

#----------------------------------------------------------------------
# 箱庭諸島 for Java
#
# アプレット通信スクリプト($Revision: 1.7.2.5 $)
# 使用条件、使用方法等は以下の WWWページを参照してください。
#
# 箱庭諸島 for Java 配布ページ:
# SCENERY AND FISH - http://www16.cds.ne.jp/i/ohno/
#
# 箱庭諸島２のスクリプトは以下の WWWページで配布されています。
#
# 箱庭諸島２のページ:
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
# 各種設定値
#  基本的に独自の設定部分はあまりありません。
#  hako-main.cgi と同じ設定にしてください。
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# 以下、必ず設定する部分。
#----------------------------------------------------------------------

# このファイルを置くディレクトリ
#  hako-java.cgi は hako-main.cgi と同じディレクトリに置くことを想定し
#  てつくっています。
#  hako-main.cgi の baseDir の設定と同じにしてください。
#  最後に / は付けません。

# 設置する場所にあわせてURLを変更してください。
$cgiBase  = 'http://hoge.com/cgi-bin/hoge/';


# HakoApp.jar を置くディレクトリ
#  hako-main.cgi と同じサーバー上でなければ動きません。
# 通常 hako-main.cgi $imageDir の設定と同じにして、
# .gif ファイルと同じ場所に HakoApp.jar を設置します。

# 設置する場所にあわせてURLを変更してください
$codeBase = 'http://hoge.com/hoge/hakogif';


# jcode.pl の位置
#  hako-main.cgi と同じ設定にしてください

$jcode = './jcode.pl';


# ディレクトリのパーミッション
# ディレクトリ式ロック使用時のときのみ

$dirMode = 0755;


# データディレクトリの名前
#  hako-main.cgi と同じ設定にしてください

$dirName  = 'storne';


# ロックの方式
#  hako-main.cgi と同じ設定にしてください

$lockMode = 2;

#----------------------------------------------------------------------
# 必ず設定する部分は以上です。
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# 以下は好みで設定する部分ですが、
# hako-main.cgi で以下の項目を調整している場合、同じ設定にしてください
#----------------------------------------------------------------------

# 1ターンが何秒か
# ターン更新判定に使っています。
# hako-main.cgi と同じ値にしてください。

$unitTime      = 21600;


# 異常終了基準時間(ロック後何秒で、強制解除するか)
# 現在 hako-java.cgi では使っていません。
# かならず hako-top.cgi から呼ばれるので必要が殆ど無いからです。

$unlockTime    = 120;


# ログ表示スイッチ
# これが 1 だと 近況が表示されます。
# 0 なら近況表示されません。開発画面の表示が遅いと嫌って人は
# これを 0 にしてください。

$logView = 1;


# ログの表示ターン数
# この数値は hako-main.cgi よりも小さく設定出来ます。
# 数値を小さくすることで、Java開発画面を表示する際の負荷を軽減できます。

$logMax = 4;


# コマンド入力限界数
# hako-main.cgi と同じ値にしてください。

$commandMax    = 50;


# ローカル掲示版(観光者通信)の使用
# 0 にすると ローカル掲示版が使用出来なくります。
# 1 なら使用可能です。

$useLbbs = 1;


# ローカル掲示版の認証モード
# この値を 1 に設定すると、ローカル掲示版の書き込み時にパスワードが
# 確認されるようになり、書き込みの名前の後ろに '＠xxxxx島' が付加されます。

$lbbsAuth = 1;


# ローカル掲示版行数
# hako-main.cgi と同じ値にしてください。

$lbbsMax = 10;


# 島の大きさ
# hako-main.cgi と同じ値にしてください。

$islandSize = 31;


# 他人から資金を見えなくするか
# hako-main.cgi と同じ値にしてください。

$hideMoneyMode = 2;


# パスワードの暗号化
# hako-main.cgi と同じ値にしてください。

$cryptOn       =  1;


# 受け付けるFORMデータの最大長
# 100スケジュールの送信を行なっても 2048バイトはいかないので
# こんなもんでちょうど良いと思います。

$maxContentLength = 2048;


# ローカルBBSで受け付ける名前の最大長

$maxName       = 32;


# ローカルBBSで受け付けるメッセージの最大長

$maxMessage    = 80;


# コメントで受け付けるメッセージの最大長

$maxComment    = 80;


# redirect 設定
# Java開発画面を表示しようとしたときに、ターン更新時間が過ぎていたら、
# ターン更新させるようにします。通常 1 で良いと思います。

$redirectNewTurn = 1;


# 一つの島の行数
# hakojima.dat ファイルの一つの島の情報の行数です。
# 改造等で情報を増やしている場合はこれを調整してください。

$islandLines = 13;

# マップ文字列の桁数
# マップ文字列の桁数を変更している場合に使用してください。
$landDigits = 2;
$landValueDigits = 2;


#----------------------------------------
# 外見関係
#----------------------------------------

# <BODY> タグのオプション

$htmlBody      = 'BGCOLOR="#EEFFFF"';


# ゲームのタイトル文字

$title         = '箱庭諸島 for Java';


# 大きい文字

$tagBig_ = '<FONT SIZE=6>';
$_tagBig = '</FONT>';


# 島の名前など

$tagName_ = '<FONT COLOR="#a06040"><B>';
$_tagName = '</B></FONT>';


# 順位の番号など

$tagNumber_ = '<FONT COLOR="#800000"><B>';
$_tagNumber = '</B></FONT>';

# 島の接尾語

$islandSuffix = '島';

# アプレットの幅

$appletWidth  = '760';


# アプレットの高さ

$appletHeight = '770';


#----------------------------------------------------------------------
# hako-main.cgi と同じ設定にするのはここまでです。
#----------------------------------------------------------------------


#----------------------------------------------------------------------
# 各種定数
#  これ以後の書き換えは Javaアプレットへ影響が出ます。
#  また同種の設定値が hako-main.cgi にもあるものは
#  同じ設定にしてください。
#----------------------------------------------------------------------

# ファイル名
#  .jar .cgiファイルの名前

$archive = "HakoApp.zip";
$cgiJava = "hako-java.cgi";
$cgiMain = "hako-main.cgi";


# アプレット関係

$appletName = "HakoApplet";
$appletClass= "y_ohno.game.hakoniwa.HakoApplet.class";


# Applet との通信時のステータス番号

$CANNOT_LOCK="001";
$MISSING_ID ="002";
$WRONG_PASS ="003";
$FATAL_ERROR="004";
$DISABLED   ="005";


# 地形番号

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
# 島情報ファイルの名前

$dataName     = 'hakojima.dat';


# 島情報ファイル書き込み時のテンポラリファイル

$dataTemp     = 'hakojima.tmp';


# islandファイル書き込み時のテンポラリファイル

$tempName     = 'island.tmp';


#----------------------------------------------------------------------
# main()
#----------------------------------------------------------------------

# ロック済みフラグの初期化

$locked = 0;


# jcode.pl のロード

require($jcode);


# FORM の処理

if (! treatPostedData())
{
    exit 1;
}


# アクションによって分岐

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
# ログ出力
#----------------------------------------------------------------------
# ログファイルにログを書き込みます

#sub logprint
#{
#    open LOGWRITE, ">>${dirName}/log";
#    print LOGWRITE @_;
#    close(LOGWRITE);
#}

#----------------------------------------------------------------------
# ログイン処理
#----------------------------------------------------------------------
# memo:
#  アプレットを表示するHTMLドキュメントを返します。

sub login
{
    my ($id, $password, $reload, $javacgi);

    $id = $FORM{'island'};
    $password = $FORM{'password'};
    $reload = $cgiBase . "/" . $cgiMain;
    $javacgi= $cgiBase . "/" . $cgiJava;

    # 必要なら島の情報の読み込み
    if ($logView || $redirectNewTurn)
    {
	if (! hakolock())
	{
	    printHtmlHeader();
	    printError('ロックの取得に失敗しました');
	    printHtmlFooter();
	    return 0;
	}

	if (! readIslandsFile($id, 0))
	{
	    printHtmlHeader();
	    printError('データファイルの読み込みに失敗しました');
	    printHtmlFooter();
	    return 0;
	}
    }

    # Turn 更新チェック
    if ($redirectNewTurn)
    {
	if ($nextTurn == 0)
	{
	    # window mode なら JavaScript で
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

    # window mode でなければ トップへ戻る を表示
    if ($FORM{'windowmode'} ne 'window')
    {
	printSJIS("<A HREF=\"${reload}\">${tagBig_}トップへ戻る${_tagBig}</A><HR>\n");
    }

    # log 表示時はパスワードチェック
    if ($logView)
    {
	if ($islandPassword ne encrypt($password))
	{
	    hakounlock();
	    printError('パスワードが一致しません');
	    printHtmlFooter();
	    return 0;
	}
    }
    # アプレットの TAGを出力
    if ($FORM{'tag'} eq 'PLUGIN')
    {
	# PLUGINを使う
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
	printSJIS("<NOEMBED></COMMENT>プラグインは使えないみたいです</NOEMBED></EMBED></OBJECT>\n");
    }
    else
    {
	# アプレットタグを使う
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
    # コメント変更 FORMの出力
    print "<SCRIPT language=JavaScript>\n<!--\nfunction commentPost()\n";
    print "{\n  postWindow = window.open(\"\", \"postWindow\", \"menubar=no,toolbar=no,location=no,directories=no,status=no,scrollbars=yes,resizable=yes,width=640,height=80\");\n}\n//-->\n</SCRIPT>\n";
 print "<IMG SRC=\"jyu.cgi?page=${id}&name=${id}\" WIDTH=\"2\" HEIGHT=\"2\">\n";
    printSJIS("${tagBig_}コメントの変更${_tagBig}<BR>\n");
    printSJIS("<FONT SIZE=-1>更新は一度だけ押してください。</FONT><BR>");
    printSJIS("<FORM NAME=\"commentForm\" METHOD=POST ACTION=\"$javacgi\" TARGET=\"postWindow\">\n");
    printSJIS("<INPUT TYPE=hidden NAME=\"action\" VALUE=\"comment\">\n");
    printSJIS("<INPUT TYPE=hidden NAME=\"island\" VALUE=\"${id}\">\n");
    printSJIS("<INPUT TYPE=hidden NAME=\"password\" VALUE=\"${password}\">\n");
    printSJIS("<INPUT TYPE=text NAME=\"comment\" VALUE=\"${islandComment}\" SIZE=80 MAXLENGTH=${maxComment}>\n");
    printSJIS("<INPUT TYPE=submit VALUE=\"更新\" onClick=\"commentPost()\">\n");
    printSJIS("</FORM></CENTER>\n");

    if ($logView)
    {
	print "<HR>";
	printSJIS("${tagBig_}${tagName_}${islandName[$islandIndex]}${islandSuffix}${_tagName}の近況${_tagBig}<BR>\n");
	printAllLog($id);
    }

    printHtmlFooter();

    return 1;
}


#----------------------------------------------------------------------
# コメント更新
#----------------------------------------------------------------------
# memo:
#  コメントを更新します。
#  $FORM{'action'}   = 'comment'
#  $FORM{'comment'}  = 'コメント'
#  $FORM{'island'}   = 島のID
#  $FORM{'password'} = 島のパスワード

sub comment
{
    my ($id, $password, $comment);

    # FORM から取り出す
    $id = $FORM{'island'};
    $password = $FORM{'password'};
    $comment = $FORM{'comment'};

    printHtmlHeader();

    # ファイルのロック
    if (! hakolock())
    {
	printError('ロックに失敗しました');
    }
    else
    {
	# コメントの書き換え
	writeComment($id, $password, $comment);
	hakounlock();
    }

    printSJIS("<BR><CENTER><A HREF=\"javascript:void(0)\" onClick=\"window.close();\">閉じる</A></CENTER>");
    printHtmlFooter();
}


#----------------------------------------------------------------------
# スケジュール設定処理
#----------------------------------------------------------------------
# memo:
#  スケジュールの設定をします。

sub plan
{
    my ($id, $password, @plans);
    my ($i, $line, $length, $readfile, $tempfile);

    # FORMデータの読み込み
    $id = $FORM{'island'};
    $password = encrypt($FORM{'password'});
    @plans = split(/\\/,$FORM{'plan'});

    $length = @plans;
    $readfile = "${dirName}/island.${id}";
    $tempfile = "${dirName}/${tempName}";

    # ロックの取得
    if (! hakolock())
    {
	nack($CANNOT_LOCK);
    }

    # 島データターン等の読み込み
    if (! readIslandsFile($id, 0))
    {
	nack($FATAL_ERROR);
    }

    # パスワードを確認
    if ($islandPassword ne $password)
    {
	nack($WRONG_PASS);
    }

    # スケジュール長を確認
    if ($length != $commandMax)
    {
	nack($FATAL_ERROR);
    }

    # ファイルのオープン
    if (! open(READ, "$readfile"))
    {
	nack($FATAL_ERROR);
    }

    if (! open(WRITE, ">$tempfile"))
    {
	nack($FATAL_ERROR);
    }

    # 島地図データの書きだし
    for ($i = 0; $i < $islandSize; $i++)
    {
	$line = <READ>;
	print WRITE $line;
    }

    # スケジュールの読み飛ばしと書き込み
    for ($i = 0; $i < $commandMax; $i++)
    {
	$line = <READ>;
	print WRITE $plans[$i] . "\n";
    }

    # コメントの書きだし
    print WRITE <READ>;

    # ファイルのクローズ
    close(WRITE);
    close(READ);

    # renameする
    if (! rename("$tempfile", "$readfile"))
    {
	nack($FATAL_ERROR);
    }

    # unlockする
    hakounlock();

    # 完了通知
    ack();
    print "${nextTurn}\n";
}


#----------------------------------------------------------------------
# 通信欄処理
#----------------------------------------------------------------------

sub communication
{
    my ($id, $password, $name, $comment, $auth);
    my ($owner, $readfile, $tempfile, @lbbs);

    # 使用禁止確認
    if ($useLbbs == 0)
    {
	nack($DISABLED);
    }

    # FORMデータの読み込み
    $id = $FORM{'island'};
    $password = $FORM{'password'};
    $name     = $FORM{'name'};
    $comment  = $FORM{'comment'};
    $ownerid  = $FORM{'ownerid'};
    $auth = "";

    $readfile = "${dirName}/island.${id}";
    $tempfile = "${dirName}/${tempName}";

    # データファイルのロック
    if (! hakolock())
    {
	nack($CANNOT_LOCK);
    }

    # 書き込むコメントが存在するか？
    if ($comment ne "")
    {
	# とりあえず、ゲストを仮定
	$owner = 0;

	# パスワードが設定されていたら encryptする
	if ($password ne "")
	{
	    $password = encrypt($password);
	}

	# $name と $comment を 正規化
	$name = cutColumn(jcode::euc($name, 'sjis'), $maxName);
	$comment = cutColumn(jcode::euc($comment, 'sjis'), $maxMessage);

	if ($lbbsAuth)
	{
	    # 認証モード
	    if ($ownerid eq '')
	    {
		nack($FATAL_ERROR);
	    }

	    # 非隠蔽モードで読み込む
	    if (! readIslandsFile($ownerid, 0))
	    {
		nack($FATAL_ERROR);
	    }

	    # パスワードが不一致ならエラー
	    if ($islandPassword ne $password)
	    {
		nack($WRONG_PASS);
	    }

	    # ownerid == id なら ownermode
	    if ($ownerid == $id)
	    {
		$owner = 1;
	    }

	    # 名前の加工
	    $auth = '(' . $islandName[$islandIndex] . $islandSuffix . ')';
	}
	else
	{
	    # 匿名モード
	    # 非隠蔽モードで読み込む
	    if (! readIslandsFile($id, 0))
	    {
		nack($FATAL_ERROR);
	    }

	    # パスワードが一致して、かつ $id == $ownerid なら ownerモード
	    if (($islandPassword eq $password) &&
		($id == $ownerid))
	    {
		$owner = 1;
	    }
	}

	# name と comment の HTML化
	$name = encodeHTML($name);
	$comment = encodeHTML($comment);

	# ファイルのオープン
	if (! open(READ, "$readfile"))
	{
	    nack($FATAL_ERROR);
	}

	if (! open(WRITE, ">$tempfile"))
	{
	    nack($FATAL_ERROR);
	}

	# 島地図データの書きだし
	for ($i = 0; $i < $islandSize; $i++)
	{
	    $line = <READ>;
	    print WRITE $line;
	}

	# スケジュールの読み飛ばしと書き込み
	for ($i = 0; $i < $commandMax; $i++)
	{
	    $line = <READ>;
	    print WRITE $line;
	}

	# 新規コメントの書き込み
	$lbbs[0] = "${owner}>${islandTurn}${auth}：${name}>${comment}\n";
	print WRITE $lbbs[0];

	# 残りのコメントの書きだし
	for ($i = 1; $i < $lbbsMax; $i++)
	{
	    $lbbs[$i] = <READ>;
	    print WRITE $lbbs[$i];
	}

	# ファイルのクローズ
	close(WRITE);
	close(READ);

	# renameする
	if (! rename("$tempfile", "$readfile"))
	{
	    nack($FATAL_ERROR);
	}
    }
    else
    {
	# islandファイルの読み込み
	if (! open(READ, "$readfile"))
	{
	    nack($FATAL_ERROR);
	}

	# コメント以外の読み飛ばし
	for ($i = 0; $i < ($islandSize + $commandMax); $i++)
	{
	    $dummy = <READ>;
	}

	# コメントの読み込みと書きだし
	for ($i = 0; $i < $lbbsMax; $i++)
	{
	    $lbbs[$i] = <READ>;
	}

	# ファイルを閉じる
	close(READ);
    }

    hakounlock();

    # ackの返信
    ack();

    # LocalBBSの最大行数
    print "${lbbsMax}\n";

    # 結果の出力
    for ($i = 0; $i < $lbbsMax; $i++)
    {
$lbbs[$i] =~ /([0-9]*)\>(.*)\>(.*)$/;
if ($1 == '5') {
$gokuhi = "5> >＊＊＊ 極秘 ＊＊＊\n";
print jcode::sjis(${gokuhi}, 'euc');
}else{
print jcode::sjis($lbbs[$i], 'euc');
}
}
}

#----------------------------------------------------------------------
# 全島のデータ＋自島のマップデータの取得
#----------------------------------------------------------------------

sub inspect
{
    my ($id, $password);

    $id = $FORM{'island'};
    $password = encrypt($FORM{'password'});

    # データファイルのロック
    if (! hakolock())
    {
	nack($CANNOT_LOCK);
    }

    # 島データターン等の読み込み
    if (! readIslandsFile($id, 0))
    {
	nack($FATAL_ERROR);
    }

    if (! readMapFile($id, 0))
    {
	nack($FATAL_ERROR);
    }

    hakounlock();

    # パスワードを確認
    if ($islandPassword ne $password)
    {
	nack($WRONG_PASS);
    }

    ack();

    print "${nextTurn}\n";

    # 島の情報を送信
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

    # 島の地形を送信
    for ($i = 0; $i < $islandSize; $i++)
    {
	print $islandMap[$i] . "\n";
    }

    # 島のスケジュールを送信
    print "${commandMax}\n";

    for ($i = 0; $i < $commandMax; $i++)
    {
	print $islandPlan[$i] . "\n";
    }
}


#----------------------------------------------------------------------
# 島のマップの取得
#----------------------------------------------------------------------

sub sightseeing
{
    my ($id);

    $id = $FORM{'island'};

    if (! hakolock())
    {
	nack($CANNOT_LOCK);
    }

    # 島情報の読み込み 隠蔽モード
    if (! readIslandsFile($id, 1))
    {
	nack($FATAL_ERROR);
    }

    # 地図データの読込 隠蔽モード
    if (! readMapFile($id, 1))
    {
	nack($FATAL_ERROR);
    }

    hakounlock();

    ack();

    print "${nextTurn}\n";

    my ($i, $lines);

    # 島の情報を送信

    $lines = 11 + $islandSize;	# 行数の計算

    print "${lines}\n";		# 行数

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

    # 島の地形を送信
    for ($i = 0; $i < $islandSize; $i++)
    {
	print $islandMap[$i] . "\n";
    }
}

#----------------------------------------------------------------------
# サブルーチン郡
#----------------------------------------------------------------------

#----------------------------------------
# SJISによる出力
#----------------------------------------
# argument:
#  $string - 標準出力に出力したいEUC文字列
# memo:
#  EUC文字列を SJIS変換して出力します。

sub printSJIS
{
    print jcode::sjis($_[0], 'euc');
}


#----------------------------------------
# HTML 文章に変換する
#----------------------------------------
# argument:
#  $string - HTMLで表示可能な状態に変換する文章
# memo:
#  HTMLとして表示可能な文章に変換する
#  &   = &amp;
#  "   = &quot;
#  <   = &lt;
#  >   = &gt;
#
#  [\x00-\x1F] は削除
#  SJISでも大丈夫なはずですが、漢字コードは EUCを使用するようにしてください。

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
# 指定の桁数で文字列を切る
#----------------------------------------
# argument:
#  $string    - 切りとる文字列
#  $maxlength - 最大長(バイト数)
# return:
#  切りとった文字列
# memo:
#  漢字コードの上位下位判定をしているため EUCでなければなりません。

sub cutColumn
{
    my ($string, $maxlength) = @_;

    if (length($string) <= $maxlength)
    {
	return $string;
    }

    # $maxlength バイト目が 2byte code の 2byte 目なら
    # $maxlength - 1 までが有効範囲、それ以外は $maxlength まで。
    if (isEUCSecondByte($string, $maxlength))
    {
	$maxlength--;
    }

    return substr($string, 0, $maxlength);
}


#----------------------------------------
# 指定された文字がEUC漢字の2byte目か判定
#----------------------------------------
# argument:
#  $string - 判定する文字列
#  $offset - 判定する文字の位置
# return:
#  0 - $offset 目の文字は EUC漢字コードの１バイト目か半角文字
#  1 - $offset 目の文字は EUC漢字コードの２バイト目

sub isEUCSecondByte
{
    my ($string, $offset) = @_;
    my ($c, $result);

    $result = 0;

    # ↓なんか効率悪い
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
# ポストされたデータの処理
#----------------------------------------
# global reference:
#  $maxContentLength - 受信する最大のフォームデータ
#
# return:
#  FORM - nameをkeyにした連想配列

sub treatPostedData
{
    my ($buffer, @pairs, $name, $value, $length);

    $length = $ENV{'CONTENT_LENGTH'};

    # 異常に長いデータが来たらエラー終了させる
    # 通常、どんなに考えても 2K を越えることは無いはず
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
# ヘッダーを返す
#----------------------------------------
# memo:
#  Java との 通信は基本的に text/plain で行います。

sub printHeader
{
    print "Content-type: text/plain\n\n";
}


#----------------------------------------
# ACKを返す
#----------------------------------------
# memo:
#  Java アプレットに対して要求が受理されたことを通知

sub ack
{
    print "ACK\n";
}


#----------------------------------------
# NACKとエラー番号を返す
#----------------------------------------
# memo:
#  Javaアプレットに対して要求が受理されなかったことを通知

sub nack
{
    hakounlock();
    print "NACK $_[0]\n";
    exit 0;
}


#----------------------------------------
# HTML Header の出力
#----------------------------------------
# memo:
#  HTML Header を出力します

sub printHtmlHeader
{
if($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/ and $ENV{HTTP_USER_AGENT}=~/Windows/){
print qq{Content-type: text/html; charset=Shift_JIS\n};
print qq{Content-encoding: gzip\n\n};

# gzipへのパスの修正が必要です。
open(STDOUT,"| /bin/gzip -1 -c");
print " " x 2048 if($ENV{HTTP_USER_AGENT}=~/MSIE/);
print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
}else{
print qq{Content-type: text/html; charset=Shift_JIS\n\n};
print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
}

    printSJIS("<HTML><HEAD><TITLE>${title}</TITLE></HEAD>\n");
    printSJIS("<BODY ${htmlBody}>");

    # ---v--- 削除禁止です。消さないでねm(_ _)m ---v---
    printSJIS("<A HREF=\"http://t.pos.to/hako/\">箱庭諸島スクリプト配布元</A>　\n");
    # ---^--- 削除禁止です。消さないでねm(_ _)m ---^---

    printSJIS("<A HREF=\"http://www16.cds.ne.jp/~ohno/\">箱庭諸島 for Java 配布元</A><HR>\n");
}


#----------------------------------------
# HTML Footer の出力
#----------------------------------------
# memo:
#  HTML Footer を出力します

sub printHtmlFooter
{
    # 掲示版等へのリンクはここに追加
    printSJIS("<HR></BODY></HTML>\n");
}


#----------------------------------------
# HTMLでのエラー出力
#----------------------------------------
# memo:
#  エラー文章を表示します。
    
sub printError
{
    my($message) = @_;

    printSJIS("${tagBig_}${message}${_tagBig}");
}


#----------------------------------------
# コメントの書き込み
#----------------------------------------
# argument:
#  $id       - コメントを書き込む島の ID
#  $password - コメントを書き込む島の パスワード
#  $comment  - コメント
# memo:
#  $comment == "" なら (未登録) とします。

sub writeComment
{
    my ($id, $password, $comment) = @_;
    my ($i, $l, $n, $found, $readline, $readid, $readfile, $tempfile);

    # $comment を 正規化
    $comment = cutColumn(jcode::euc($comment), $maxComment);
    $comment = encodeHTML($comment);

    if ($comment eq "")
    {
	$comment = "(未登録)";
    }

    $readfile = "${dirName}/${dataName}";
    $tempfile = "${dirName}/${dataTemp}";
    $found = 0;

    # 読み込み側オープン
    if (! open(READ, "$readfile"))
    {
	printError('データファイルを開けません');
	return 0;
    }

    # 書き込み側オープン
    if (! open(WRITE, ">$tempfile"))
    {
	close(READ);
	printError('テンポラリファイルを開けません');
	return 0;
    }

    # ターン情報などの読み込み
    $readline = <READ>;		# ターン数
    print WRITE $readline;
    $readline = <READ>;		# 最終更新時間
    print WRITE $readline;
    $readline = <READ>;		# 島の総数
    print WRITE $readline;
    $n = int($readline);
     $readline = <READ>;		# 次に割り当てるID
    print WRITE $readline;

   # 書き換える島の検索
    SEARCH: for ($i = 0; $i < $n; $i++)
    {
	$l = $islandLines;

	$readline = <READ>; $l--; # 島の名前
	print WRITE $readline;
	$readline = <READ>; $l--; # 島のID
	print WRITE $readline;
	$readid = int($readline);

	# 探している ID か？
	if ($id == $readid)
	{
	    $readline = <READ>; $l--; # 授賞データ
	    print WRITE $readline;
	    $readline = <READ>; $l--; # 連続資金繰り
	    print WRITE $readline;

	    $readline = <READ>; $l--; # 旧コメント
	    $readline = <READ>; $l--; # パスワード
	    chomp($readline);

	    # パスワード確認
	    if ($readline ne encrypt($password))
	    {
		close(READ);
		close(WRITE);
		printError('パスワードが違います');
		return 0;
	    }

	    # コメントとパスワードの出力
	    print WRITE "${comment}\n";
	    print WRITE "${readline}\n";

	    $found = 1;
	    last SEARCH;
	}

	# 残りのデータを書き出す

	while ($l > 0)
	{
	    $readline = <READ>; $l--;
	    print WRITE $readline;
	}
    }

    # コメントが書き換えられていたら
    if ($found)
    {
	# ファイルの残りを全てコピーする
	while (<READ>)
	{
	    print WRITE $_;
	}
    }

    # ファイルのクローズ
    close(WRITE);
    close(READ);

    if ($found)
    {
	# ファイルの置き換え
	if (! rename("$tempfile", "$readfile"))
	{
	    printError('データの置き換えに失敗しました');
	    return 0;
	}
    }
    else
    {
	# 指定のIDが見つからなかった
	printError('書き換えに失敗しました');
	return 0;
    }

    printSJIS("<CENTER>${tagBig_}コメントを書き換えました${_tagBig}</CENTER>");

    return 1;
}


#----------------------------------------
# 島情報の読み込み
#----------------------------------------
# argument:
#   $id      - 島のID番号
#   $conceal - 情報の隠蔽動作
# return:
#   0 - 失敗
#   1 - グローバル変数に以下のデータが設定される。
#   $islandTurn        = このデータのターン
#   $islandNumber      = 島の数
#   $islandNextID      = 新規の島に割り当てるID
#   $islandLastTime    = 最後に更新された時間
#   $nextTurn          = 次のターンまでの時間
#   $islandName[index] = 島の名前
#   $islandID[index]   = 島のID
#
#   以下 $id の 島の情報
#
#   $islandIndex       = 島のIndex
#   $islandPassword    = 暗号化済みパスワード
#   $islandComment     = コメント
#   $islandMoney       = 資金($conceal != 0 のとき $hideMoneyModeにより隠蔽)
#   $islandFood        = 食糧
#   $islandPop         = 人口
#   $islandArea        = 広さ
#   $islandFarm        = 農場規模
#   $islandFactory     = 工場規模
#   $islandMountain    = 採掘場

sub readIslandsFile
{
    my ($id, $conceal) = @_;

    # データファイルを開く
    if (! open(IN, "${dirName}/${dataName}"))
    {
	return 0;
    }

    # ターン数
    $islandTurn = int(<IN>); # ターン数
    if ($islandTurn == 0)
    {
	close(IN);
	return 0;
    }

    # 最終更新時間
    $islandLastTime = int(<IN>);
    if ($islandLastTime == 0)
    {
	close(IN);
	return 0;
    }

    # 島の総数
    $islandNumber   = int(<IN>); # 島の総数
    $islandNextID   = int(<IN>); # 次に割り当てるID

    # ターン処理判定
    $nextTurn = $unitTime - (time - $islandLastTime);
    if ($nextTurn < 0)
    {
	$nextTurn = 0;
    }

    # 島の読みこみ
    my ($i, $l, $skip, $dummy, $found);
    for ($i = 0; $i < $islandNumber; $i++)
    {
	$l = $islandLines;

	# 名前とSCORE の読み込み
	$islandName[$i] = <IN>;
	$l--;
	chomp ($islandName[$i]);

	# 帝国の興亡対応
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

	# $idの読み込み
	$islandID[$i] = int(<IN>);
	$l--;

	# 読み込み対象の島か？
	if ($islandID[$i] == $id)
	{
	    # 対象の島を見つけた
	    $islandIndex = $i;
	    $islandRank = $i + 1;

	    # 授賞データ
	    $dummy = <IN>;
	    $l--;

	    # 連続資金繰り
	    $dummy = <IN>;
	    $l--;

	    # コメント
	    $islandComment = <IN>;
	    $l--;
	    chomp($islandComment);

	    # パスワード
	    $islandPassword = <IN>;
	    $l--;
	    chomp($islandPassword);

	    # 資金
	    if ($conceal)
	    {
		$islandMoney = concealMoney(int(<IN>));
	    }
	    else
	    {
		$islandMoney = int(<IN>);
	    }
	    $l--;

	    # 食糧
	    $islandFood  = int(<IN>);
	    $l--;

	    # 人口
	    $islandPop   = int(<IN>);
	    $l--;

	    # 広さ
	    $islandArea  = int(<IN>);
	    $l--;

	    # 農場
	    $islandFarm  = int(<IN>);
	    $l--;

	    # 工場
	    $islandFactory = int(<IN>);
	    $l--;

	    # 採掘場
	    $islandMountain = int(<IN>);
	    $l--;

	    $found = 1;
	}

	# 次の島まで読み飛ばす
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
# 地図の読み込み
#----------------------------------------
# argument:
#  $id      = 島のID番号
#  $conceal = 情報の隠蔽動作
# return:
#  0 - 失敗
#  1 - グローバル変数に以下のデータが設定される。
#  $islandMap[]       = 地図($conceal != 0 なら隠蔽)
#  $islandPlan[]      = 計画($conceal != 0 なら設定されない)
#  $islandComm[]      = 通信欄

sub readMapFile
{
    my ($id, $conceal) = @_;
    my ($i, $line);

    # ファイルを開く
    if (! open(MAPID, "${dirName}/island.${id}"))
    {
	nack($FATAL_ERROR);
    }

    # 最初の $islandSize 行は MAPデータ
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

    # 次の $commandMax 行は Planデータ
    for ($i = 0; $i < $commandMax; $i++)
    {
	$line = <MAPID>;
	chomp($line);

	if (! $conceal)
	{
	    $islandPlan[$i] = $line;
	}
    }

    # 次の行から $lbbsMax 行が 通信欄
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
# MAP文字列の隠蔽
#----------------------------------------
# argument:
#  $string - 島情報の１行
# memo:
#  自島以外の詳細を隠します。

sub concealMap
{
my ($mapstring) = @_;
my ($x, $result, $land, $landV);
my ($mrexp) = "^(.{${landDigits}})(.{${landValueDigits}})";
my ($mform) = "%0${landDigits}x%0${landValueDigits}x";

    $result = "";


    for ($x = 0; $x < $islandSize; $x++)
    {
        $mapstring =~ s/${mrexp}//;    # この行を変更
        $land  = hex($1);
        $landV = hex($2);

	if ($land == $landForest)
	{
	    # 木の本数を隠す
	    $landV = 0;
	}
	elsif ($land == $landBase)
	{
	    # 木のふり
	    $land = $landForest;
	    $landV= 0;
	}elsif ($land == $landDefence)
	{
if($landV >1){	    # 木のふり
	    $land = $landForest;
	    $landV= 0;
	}
}
	elsif ($land == $landSbase)
	{
	    # 海のふり
	    $land = $landSea;
	    $landV = 0;
	}
	elsif ($land == $landkiken)
	{
	    # 海のふり
	    $land = $landForest;
	    $landV = 0;
	}
elsif ($land == $landKoku)
	{
	    # 海のふり
	    $land = $landForest;
	    $landV = 0;
	}
elsif ($land == $landJira)
	{
	    # 海のふり
	    $land = $landPlains;
	    $landV = 0;
	}
	elsif ($land == $landDummy)
	{
if($landV <1){	    # 防衛基地のふり
	    $land = $landDefence;
} else{
# 木のふり
	    $land = $landForest;
	    $landV= 0;
	}
	}

$result = $result . sprintf($mform, $land, $landV); # この行を変更
    }

    return $result;
}


#----------------------------------------
# 資金の隠蔽
#----------------------------------------
# memo:
# hideMoneyMode = 0 で 資金は見えない
#               = 1 で 資金は見える
#               = 2 で 資金は1000億円単位で四捨五入

sub concealMoney
{
    my ($money) = @_;

    if ($hideMoneyMode == 0)
    {
	# 完全隠蔽
	$money = 0;
    }
    elsif ($hideMoneyMode == 1)
    {
	# 資金公開
	$money = -($money+1);
    }
    else # if ($hideMoneyMode == 2)
    {
	if ($money < 500)
	{
	    # 500億円未満
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
# 全ファイルのログを表示
#----------------------------------------
# argument:
#  $id - ログを表示する島のID
# memo:
#  $id の ログを表示する

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
# １ファイルのログを表示
#----------------------------------------
# argument:
#  $fileNumber - 表示するファイル世代
#  $id - ログを表示する島の id
# memo:
#  指定された世代のログを出力する

sub printLog
{
    my($fileNumber, $id) = @_;
    my($line, $m, $turn, $id1, $id2, $message);

    if (! open(LIN, "${dirName}/hakojima.log${fileNumber}"))
    {
	# ログファイルが存在しない
	return;
    }

    while ($line = <LIN>)
    {
	$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),(.*)$/;
	($m, $turn, $id1, $id2, $message) = ($1, $2, $3, $4, $5);

	# 表示対象の島か？
	if (($id != $id1) &&
	    ($id != $id2))
	{
	    next;
	}

	# 機密関係
	if ($m == 1)
	{
	    if ($id1 != $id)
	    {
		# 機密表示権利なし
		next;
	    }
	    $m = '<B>(機密)</B>';
	}
	else
	{
	    $m = '';
	}

	# 表示の更新
	printSJIS("<NOBR>${tagNumber_}ターン$turn$m${_tagNumber}：$message</NOBR><BR>\n");
    }
    close(LIN);
}


#----------------------------------------
# パスワードの暗号化
#----------------------------------------
# memo:
#  hako-main.cgi と同じ仕様

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
# データファイルのロック＆アンロック
#----------------------------------------
# memo:
#  hako-main.cgi とほぼ同じ仕様

sub hakolock
{
    if (! $locked)
    {
	if ($lockMode == 1)
	{
	    # directory式ロック
	    $locked = hakolock1();
	}
	elsif ($lockMode == 2)
	{
	    # flock式ロック
	    $locked = hakolock2();
	}
	elsif ($lockMode == 3)
	{
	    # symlink式ロック
	    $locked = hakolock3();
	}
	else
	{
	    # 通常ファイル式ロック
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


# directory式ロック

sub hakolock1
{
    # ロックを試す
    if (mkdir('hakojimalock', $dirMode))
    {
	# 成功
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


# flock式ロック

sub hakolock2
{
    open(LOCKID, '>>hakojimalockflock');

    if (flock(LOCKID, 2))
    {
	# 成功
	return 1;
    }
    else
    {
	# 失敗
	return 0;
    }
}

sub hakounlock2
{
    close(LOCKID);
}


# symlink式ロック

sub hakolock3
{
    # ロックを試す
    if (symlink('hakojimalockdummy', 'hakojimalock'))
    {
	# 成功
	return 1;
    }
    else
    {
	# 失敗
	return 0;
    }
}

sub hakounlock3
{
    unlink('hakojimalock');
}


# ファイル式のロック

sub hakolock4
{
    # ロックを試す
    if (unlink('key-free'))
    {
	# 成功
	open(OUT, '>key-locked');
	print OUT time;
	close(OUT);
	return 1;
    }
    else
    {
	# 失敗
	return 0;
    }
}

sub hakounlock4
{
    my($i);
    $i = rename('key-locked', 'key-free');
}
