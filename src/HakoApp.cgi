#!/bin/perl
# CGI から JARファイルを送信するためのアダプタ $Revision: 1.2.2.1 $
#
# CGI Wrapperなどで、HakoApp.jar を直接 CGIサーバに設置出来ない場合は
# HakoApp.jar を HakoApp.zip という名前に変更し、
# このファイルを HakoApp.jar という名前に変更して
#  hako-main.cgi と 同じ場所に実行属性をつけて(755)にして設置してください。
# hako-java.cgi の $archive 設定は HakoApp.jar のままで OKです。
# この場合 $codeBase 設定は $cgiBaseと同じになります。

# 注意:この設置を行なう場合、HakoApp.jar に 地図表示で使用する
# グラフィックイメージファイルを入れなければなりません。

#
# 送信するファイル名
#
$jarfile = "./HakoApp.zip";

#
# ファイルのオープン
#
$retry = 5;

while (! open(HJARFILE, $jarfile))
{
    $retry--;
    if ($retry <= 0)
    {
        exit 1;
    }

    select undef, undef, undef, 0.2;
}

#
# ファイルの時間とサイズを調べる
#
my ($dev, $ino, $mode, $nlink, $uid, $gid, $rdev, $size, $atime, $mtime, $ctime, $blksize, $blocks) = stat(HJARFILE);

#
# 送信
#
print "Expires: " . makeRFC1123(time + 3600 * 24 * 30) . "\n";
print "Last-Modified: " . makeRFC1123($mtime) . "\n";
print "Content-length: $size\n";
print "Content-type: application/java-archive\n\n";

#
# HEAD Request?
#
$meth = $ENV{'REQUEST_METHOD'};
if ($meth eq 'HEAD')
{
    exit 0;
}


$readbyte = read(HJARFILE, $buffer, $size, 0);
while ($readbyte != 0)
{
    print $buffer;
    $readbyte = read(HJARFILE, $buffer, 65536);
}

close HJARFILE;
exit 0;

sub makeRFC1123
{
    my (@exp) = gmtime($_[0]);

    $exp[6] = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')[$exp[6]];
    $exp[4] = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'O
ct', 'Nov', 'Dec')[$exp[4]];
    $exp[5] += 1900;

    return sprintf("%s, %02d %s %4d %02d:%02d:%02d GMT",
                    $exp[6], $exp[3], $exp[4], $exp[5],
                    $exp[2], $exp[1], $exp[0]);
}
