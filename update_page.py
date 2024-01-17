'''
Author: Nya-WSL
Copyright © 2024 by Nya-WSL All Rights Reserved. 
Date: 2024-01-16 15:02:50
LastEditors: 狐日泽
LastEditTime: 2024-01-17 17:10:44
'''

from nicegui import ui

def page():
    with ui.row():
        ui.button("返回主页", on_click=lambda: ui.open('/'), color="#E6354F").classes("text-white")
        ui.button("GitHub", on_click=lambda: ui.open('https://github.com/sagesoft-official/confess_room', new_tab=True), color="#E6354F").classes("text-white")
    with ui.timeline(side='right', layout='comfortable', color='red'):
        ui.timeline_entry('Confess Room Decoration Log', heading=True)
        ui.timeline_entry(title='Initial commit', subtitle='2023-12-31', icon='rocket')
        ui.timeline_entry(title='Release of 1.0.0', subtitle='2023-12-31')
        ui.timeline_entry('新增登录页面 | 新增棉花糖读取页面', title='Release of 1.1.0', subtitle='2024-01-01')
        ui.timeline_entry('登录界面新建返回按钮 | 登录界面和忏悔录新增背景 | 优化当棉花糖为空时忏悔录的显示效果', title='Release of 1.1.1', subtitle='2024-01-01')
        ui.timeline_entry('重构棉花糖页面布局 | 棉花糖页面新增返回主页按钮（和退出按钮不同的是返回按钮将会保存登录状态） | 修复当message.json不存在时会报错无法运行的问题', title='Release of 1.1.2', subtitle='2024-01-05')
        ui.timeline_entry('登录密码使用sha256加密，源码仅明文储存sha256值 | storage_secret值改为sha256值（非强制要求）', title='Release of 1.1.3', subtitle='2024-01-05')
        ui.timeline_entry('主页标题新增版本号 | 修改所有按钮的样式 | 部分组件颜色改为#E6354F | 投稿页面新增返回主页按钮 | 现在投稿可以输入自定义昵称，留空默认为投稿时间 | 棉花糖页面新增可切换的紧凑模式，默认为关，该模式可能会缓解当某一条棉花糖有过多换行符时会导致背景Y轴被严重拉伸的问题 | 尝试通过将注意事项部分组件的值改为HTML元素来缓解部分设备的排版问题 | 修复因为显示棉花糖的组件的值是HTML元素导致的棉花糖中的换行符无效的问题 | 修复一个在服务器反代环境下头像文件路径错误的问题', title='Release of 1.2.0', subtitle='2024-01-05')
        ui.timeline_entry('优化发送投稿的函数（可能存在投稿后不会清空输入框内容的bug 但并未复现） | 现在账号登录缓存会在每天0点自动删除', title='Release of 1.2.1', subtitle='2024-01-07')
        ui.timeline_entry('修复定时删除用户缓存在unix系统环境不生效的问题 | 调整注意事项文本', title='fix bug', subtitle='2024-01-08')
        ui.timeline_entry('新增更新日志 | 修复如果没有证书，nginx配置文件可能有错误的问题 | 由于设计缺陷，定时删除用户缓存功能可能不会达成预期的结果', title='Release of 1.2.2', subtitle='2024-01-09')
        ui.timeline_entry('新增字数限制 | 新增字数显示 | 注：标点符号包括在字数限制内 | 新增定时备份，现在将会每小时备份一次投稿数据', title='Release of 1.2.3', subtitle='2024-01-10')
        ui.timeline_entry('采用新的定时方式修复定时备份会导致程序无法进入循环而卡死的问题', title='Release of 1.2.3.1', subtitle='2024-01-10')
        ui.timeline_entry('考虑到目前字数限制功能的局限性，现在超出字数限制仍然可以投稿', title='Release of 1.2.3.2', subtitle='2024-01-10')
        ui.timeline_entry('读取棉花糖新增字数显示 | 修复定时清理用户缓存功能的一个逻辑错误，该错误会导致如果自动新建crontab的日志文件夹，程序就不会将定时任务写入crontab | 尝试优化初始化流程，避免初始化函数被执行两次 | 修复程序无法在Windows运行的问题，现在如果是Windows或macOS系统（不确定），将不会定时备份和清理用户缓存 | 注：这次修复只是为了方便debug，本程序的设计初衷并没有考虑Windows或macOS，目前也没有计划适配上述系统', title='Release of 1.2.4', subtitle='2024-01-11')
        ui.timeline_entry('优化核心代码的可读性，现在所有路径的核心代码和页面布局均在confess_page.py中 | 初始化函数移入function.py | 初始化函数debug优化 | 现在投稿页面点击返回时如果投稿内容为空将无需二次确认', title='Release of 1.2.5', subtitle='2024-01-16')
        ui.timeline_entry(r'用户和投稿数据移入数据库 | 定时备份适配数据库 |  更新日志改为独立模块,不再和子路径为同一个模块 | 优化棉花糖的显示效果,现在"\n"和"\\n"将会被替换为"\n\n" | 注：由于后台不公开，需要手动写入用户数据到数据库', title='Release of 1.2.6', subtitle='2024-01-16')
        ui.timeline_entry('优化数据库模块代码 | 重写备份模块，现在除了本地备份还会将数据库文件上传到七牛云', title='Release of 1.2.7', subtitle='2024-01-17', avatar='static/bg.jpg')