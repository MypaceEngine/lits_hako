#!/bin/perl
# CGI ���� JAR�ե�������������뤿��Υ����ץ� $Revision: 1.2.2.1 $
#
# CGI Wrapper�ʤɤǡ�HakoApp.jar ��ľ�� CGI�����Ф����ֽ���ʤ�����
# HakoApp.jar �� HakoApp.zip �Ȥ���̾�����ѹ�����
# ���Υե������ HakoApp.jar �Ȥ���̾�����ѹ�����
#  hako-main.cgi �� Ʊ�����˼¹�°����Ĥ���(755)�ˤ������֤��Ƥ���������
# hako-java.cgi �� $archive ����� HakoApp.jar �Τޤޤ� OK�Ǥ���
# ���ξ�� $codeBase ����� $cgiBase��Ʊ���ˤʤ�ޤ���

# ���:�������֤�Ԥʤ���硢HakoApp.jar �� �Ͽ�ɽ���ǻ��Ѥ���
# ����ե��å����᡼���ե����������ʤ���Фʤ�ޤ���

#
# ��������ե�����̾
#
$jarfile = "./HakoApp.zip";

#
# �ե�����Υ����ץ�
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
# �ե�����λ��֤ȥ�������Ĵ�٤�
#
my ($dev, $ino, $mode, $nlink, $uid, $gid, $rdev, $size, $atime, $mtime, $ctime, $blksize, $blocks) = stat(HJARFILE);

#
# ����
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
