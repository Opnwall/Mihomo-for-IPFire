#!/bin/bash
set -e

print_step() {
    echo
    echo "==> $1"
}

if [[ $EUID -ne 0 ]]; then
    echo "错误：请使用 root 运行此脚本。" >&2
    exit 1
fi

print_step "准备安装 Mihomo"
echo "该操作将安装 Mihomo、Web 管理页面、菜单入口，并重载 Web 服务。"
read -p "是否继续？(y/N): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "操作已取消。"
    exit 0
fi

print_step "检查安装目录"
for dir in ./menu ./cgi-bin ./etc ./bin; do
    if [[ ! -d "$dir" ]]; then
        echo "错误：缺少目录 $dir" >&2
        exit 1
    fi
done

print_step "复制文件"
install -d -m 755 /usr/local/etc/mihomo
cp -a ./menu/* /var/ipfire/menu.d/
cp -a ./cgi-bin/* /srv/web/ipfire/cgi-bin/
cp -a ./etc/init.d/mihomo /etc/init.d/mihomo
cp -a ./etc/mihomo/* /usr/local/etc/mihomo/
cp -a ./bin/* /usr/local/bin/

print_step "设置文件权限"
chmod +x /etc/init.d/mihomo
chmod +x /usr/local/bin/mihomo
chmod +x /srv/web/ipfire/cgi-bin/mihomo.cgi
chmod a+w /usr/local/etc/mihomo/config.yaml

install -d -m 755 /var/run/mihomo
touch /var/log/mihomo.log
chmod 644 /var/log/mihomo.log

print_step "配置开机自启"
ln -sf /etc/init.d/mihomo /etc/rc.d/rc3.d/S99mihomo

print_step "配置sudo权限"
{
    echo "nobody ALL=(ALL) NOPASSWD: /etc/init.d/mihomo"
    echo "nobody ALL=(ALL) NOPASSWD: /usr/local/bin/mihomo"
    echo "nobody ALL=(ALL) NOPASSWD: /bin/sh"
    echo "nobody ALL=(ALL) NOPASSWD: /bin/rm"
} >> /etc/sudoers.d/mihomo
chmod 440 /etc/sudoers.d/mihomo

print_step "重载 Web 服务"
/etc/init.d/apache reload >/dev/null 2>&1

echo
echo "Mihomo 安装完成！请前往 Web 界面进行配置（服务 > Mihomo）。"