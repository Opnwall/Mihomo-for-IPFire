## Mihomo for IPFire
在 IPFire控制Mihomo运行，来实现透明代理。包含配置修改、程序控制、日志查看功能。在IPFire 2.29 (x86_64)上测试通过。

![](image/mihomo.png)

## 集成程序
[Mihomo]([https://github.com/IrineSistiana/mosdns](https://github.com/metacubex/mihomo)) 

## 注意事项
1. 当前仅支持x86_64 平台。
2. 脚本集成了可用的默认设置，只需替换proxies和rule部分配置即可使用。
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
1. 安装完成，导航到网络>Mihomo菜单，修改配置并保存。
2. 点击启动按钮，根据输出的日志内容，排除配置文件错误。
3. 正常启动后，客户端访问 ip111.cn，检查分流是否正常。

## 其他事项
1. 脚本已添加了开机自启功能。
2. 默认配置文件开启了api功能，访问 http://lan_ip:9090/ui 登录Mihomo仪表盘。
