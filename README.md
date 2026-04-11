## Mihomo for IPFire
在IPFire上运行Mihomo实现透明代理。带Web控制界面，可以进行配置修改、程序控制、日志查看。在IPFire 2.29 (x86_64)上测试通过。

![](images/mihomo.png)

## 集成程序
[Mihomo](https://github.com/IrineSistiana/mosdns) 

## 注意事项
1. 当前仅支持x86_64 平台。
2. 脚本已集成了可用的默认配置，只需替换clash的proxies和rule部分配置即可使用。
3. 为减少长期运行保存的日志数量，在调试完成后，请将所有配置的日志类型修改为error或warn。

## 安装命令
```bash
sh install.sh
```
## 卸载命令
```bash
sh uninstall.sh
```

## 配置过程
1. 安装完成，导航到VPN>Proxy Suite 菜单，修改clash（ proxies和rules部分) 内容并保存。
2. 启动clash服务，转到接口>分配，将tun_3000虚拟网卡添加为接口并启用，无需输入IPv4地址和网关。
3. 为避免端口冲突，将 Unbound DNS 端口修改为5355端口，并作为mosdns的默认上游DNS。
5. 转到防火墙>规则，在tun接口添加一条any to any防火墙规则，允许tun子网访问。
6. 设置完成，客户端访问 ip111.cn，检查分流是否正常。

## 其他事项
1. 默认配置文件开启了clash api功能，访问 http://lan_ip:9090/ui 登录仪表盘查看代理连接信息。
2. 订阅转换可以设置定时任务自动更新。转到系统>设置>任务，添加”Renew Clash Subsribe”任务项即可。
