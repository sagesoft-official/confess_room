<!--
 * @Author: Nya-WSL
 * Copyright © 2024 by Nya-WSL All Rights Reserved. 
 * @Date: 2024-01-01 02:52:15
 * @LastEditors: 狐日泽
 * @LastEditTime: 2024-01-09 23:38:24
-->
# Confess Room

桥洞教堂忏悔室（基于NiceGUI的提问箱/棉花糖）

## USAGE

### Server

```
# Port

pip install -r requirements.txt
python main.py

http://127.0.0.1:11452

# Nginx

将nginx_conf所有的domain和第15行的端口替换成你自己的并复制到"/etc/nginx/site-enabled/default"末尾然后重启nginx（systemctl restart nginx）

如需https访问需自行申请证书或通过certbot配置

```

### Local

本程序是基于服务器多用户访问设计的，无法在本地正常运行

本地穿透请参考上方，Windows需自行解决反代配置，宝塔等面板服务器需自行解决nginx配置

## KNOWN ISSUES

- GUI是基于 `24` 寸显示器 + `1920*1080` 分辨率 + `100%` 缩放设计的，在 `1080p+` 和 `100%+` 缩放的设备上可能存在适配问题，移动设备除了平板和折叠屏应该没有这个问题

- 适配问题在 `100%+` 缩放的设备上可能更容易出现

- 如有问题可尝试删除 `ui.textarea` 和 `ui.button` 以外的组件或自行适配

- 移动设备无法拖动文本区，这是组件限制

### URL

- `/` 主页面

- `/nicegui/` server的ws反代

- `/login` 登陆页面

- `/messages` 棉花糖读取页面

- `/{uuid}` 投稿页面

- `/update` 更新日志