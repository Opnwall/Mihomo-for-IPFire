#!/usr/bin/perl
use strict;
use utf8;
use Encode qw(decode FB_CROAK);

require '/var/ipfire/general-functions.pl';
require "${General::swroot}/lang.pl";
require "${General::swroot}/header.pl";

my %settings=();
my %checked=();
my %selected=();

# ====== 可调整路径 ======
my $service      = "/etc/init.d/mihomo";
my $mihomo_conf  = "/usr/local/etc/mihomo/config.yaml";
my $mihomo_log   = "/var/log/mihomo.log";
my $sudo_cmd     = "/usr/bin/sudo";
# ========================

&Header::showhttpheaders();

&Header::getcgihash(\%settings);

# AJAX 日志接口
if ($settings{'ajax'} && $settings{'ajax'} eq 'log') {
    print "Content-Type: text/plain; charset=UTF-8\n\n";
    system("tail -n 50 /var/log/mihomo.log");
    exit;
}

my $action = $settings{'ACTION'} || '';
my $cmd_output = '';
my $show_output = 0;

my $save_message = '';

sub decode_post_utf8 {
    my ($value) = @_;
    return '' unless defined $value;
    my $decoded = $value;
    eval {
        $decoded = decode('UTF-8', $value, FB_CROAK);
    };
    return $decoded;
}

sub run_service_command {
    my ($command) = @_;
    return `$sudo_cmd -n $service $command 2>&1`;
}

sub clear_log_file {
    return `$sudo_cmd -n /bin/sh -c ': > $mihomo_log' 2>&1`;
}

# ====== 保存配置 ======
if ($action eq 'saveconf') {
    if (-e $mihomo_conf) {
        system("cp $mihomo_conf ${mihomo_conf}.bak");
    }

    if (defined $settings{'CONF'}) {
        my $conf_text = decode_post_utf8($settings{'CONF'});
        if (open(my $fh, ">:encoding(UTF-8)", $mihomo_conf)) {
            print $fh $conf_text;
            close($fh);
            system("chmod 644 $mihomo_conf");
            $save_message = "配置已保存";
            $cmd_output = $save_message;
            $show_output = 1;
        } else {
            $save_message = "保存失败：无法写入配置文件";
            $cmd_output = $save_message;
            $show_output = 1;
        }
    }
}

# ====== 服务控制 ======
if ($action eq 'start') {
    my $clear_out = clear_log_file();
    my $out = run_service_command('start');
    my $code = $? >> 8;
    $cmd_output = ($clear_out ? $clear_out : '') . $out;
    $show_output = 1;
}
elsif ($action eq 'stop') {
    my $out = run_service_command('stop');
    my $code = $? >> 8;
    $cmd_output = $out;
    $show_output = 1;
}
elsif ($action eq 'restart') {
    my $clear_out = clear_log_file();
    my $out = run_service_command('restart');
    my $code = $? >> 8;
    $cmd_output = ($clear_out ? $clear_out : '') . $out;
    $show_output = 1;
}
elsif ($action eq 'clearlog') {
    my $out = clear_log_file();
    my $code = $? >> 8;
    $cmd_output = ($out ? $out : '') . "日志已清空";
    $show_output = 1;
}

# ====== 状态检测 ======
my $status = run_service_command('status');
chomp $status;

# ====== 页面 ======
&Header::openpage("Mihomo", 1, '');
print "<meta charset='UTF-8'>\n";
print <<'EOF';
<style>
.status-dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 6px;
    vertical-align: middle;
}
.status-dot.running {
    background: #2ecc71;
}
.status-dot.stopped {
    background: #e74c3c;
}
</style>
EOF
&Header::openbigbox('100%', 'left', '', '');

print "<form method='post'>";

# ====== 状态 ======
&Header::openbox('100%', 'left', '服务状态');

print "<b>状态:</b> ";
if ($status =~ /running/i) {
    print "<span class='status-dot running'></span><span style='color:green;'>运行中</span>";
} else {
    print "<span class='status-dot stopped'></span><span style='color:red;'>已停止</span>";
}

print "<br><br>";

print "<button type='submit' name='ACTION' value='start'>启动</button>  ";
print "<button type='submit' name='ACTION' value='stop'>停止</button>  ";
print "<button type='submit' name='ACTION' value='restart'>重启</button>  ";

if ($show_output) {
    print "<br><br><pre style='color:#ff3333;background:#111;padding:5px;box-sizing:border-box;margin:0;white-space:pre-wrap;'>";
    print &Header::escape($cmd_output);
    print "</pre>";
}

&Header::closebox();

# ====== 配置 ======
&Header::openbox('100%', 'left', '配置文件');

print "<div style='margin-bottom:8px;'><button type='submit' name='ACTION' value='saveconf'>保存配置</button></div>";
my $conf_content = '';
if (-e $mihomo_conf) {
    if (open(my $fh, "<:encoding(UTF-8)", $mihomo_conf)) {
        local $/;
        $conf_content = <$fh>;
        close($fh);
    } else {
        open(my $fh, "<", $mihomo_conf);
        local $/;
        $conf_content = <$fh>;
        close($fh);
    }
}

print "<textarea name='CONF' cols='100' rows='15' style='width:100%;box-sizing:border-box;'>";
print &Header::escape($conf_content);
print "</textarea><br>";

&Header::closebox();

# ====== 日志 ======
&Header::openbox('100%', 'left', '实时日志');
print "<div style='margin-bottom:8px;'><button type='submit' name='ACTION' value='clearlog'>清空日志</button></div>";
print "<pre id='logbox' style='background:#000;color:#0f0;height:220px;overflow:auto;width:100%;box-sizing:border-box;margin:0;white-space:pre-wrap;'>";

if (-e $mihomo_log) {
    my @lines = `tail -n 100 $mihomo_log`;
    print @lines;
} else {
    print "暂无日志文件。";
}

print "</pre>";
print <<'EOF';
<script>
(function() {
    var logbox = document.getElementById('logbox');
    if (logbox) {
        logbox.scrollTop = logbox.scrollHeight;
    }
})();
</script>
EOF

&Header::closebox();

print "</form>";

&Header::closebigbox();
&Header::closepage();