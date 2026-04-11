#!/bin/bash
# Mihomo 卸载脚本
set -e

print_step() {
    echo
    echo "==> $1"
}

if [[ $EUID -ne 0 ]]; then
    echo "错误：请使用 root 运行此脚本。" >&2
    exit 1
fi

print_step "准备卸载 Mihomo"
echo "该操作将删除 Mihomo 程序、Web 管理页面、启动项、运行文件和配置文件。"
read -p "是否继续？(y/N): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "操作已取消。"
    exit 0
fi

print_step "停止 Mihomo 服务"
/etc/init.d/mihomo stop >/dev/null 2>&1 || true

print_step "移除开机自启"
rm -f /etc/rc.d/rc3.d/S99mihomo

print_step "删除程序文件"
rm -f /etc/init.d/mihomo
rm -f /usr/local/bin/mihomo
rm -f /srv/web/ipfire/cgi-bin/mihomo.cgi

print_step "删除运行文件"
rm -rf /var/run/mihomo
rm -f /var/log/mihomo.log

print_step "删除配置文件"
rm -rf /etc/mihomo

print_step "恢复菜单"
cp -a /var/ipfire/menu.d/30-network.menu.bak /var/ipfire/menu.d/30-network.menu 2>/dev/null || true

print_step "重载 Web 服务"
/etc/init.d/apache reload >/dev/null 2>&1 || true

echo
echo "Mihomo 卸载完成！"