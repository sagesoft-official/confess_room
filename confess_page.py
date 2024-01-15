'''
Author: Nya-WSL
Copyright © 2024 by Nya-WSL All Rights Reserved. 
Date: 2024-01-16 02:40:38
LastEditors: 狐日泽
LastEditTime: 2024-01-16 04:14:00
'''
import os
import json
import hashlib
from uuid import uuid4
from router import Router
from nicegui import ui, app
from datetime import datetime
from main import passwords, version

def update():
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
        ui.timeline_entry('优化核心代码的可读性，现在所有路径的核心代码和页面布局均在confess_page.py中 | 初始化函数移入function.py | 初始化函数debug优化 | 现在投稿页面点击返回时如果投稿内容为空将无需二次确认', title='Release of 1.2.5', subtitle='2024-01-16', avatar='static/bg.jpg')

def messages():
    ui.query('body').style('background: url("static/bg.jpg") 0px 0px/cover')
    with ui.row():
        ui.button('Quit', on_click=lambda: (app.storage.user.clear(), ui.open('/'))).classes('bg-transparent')
        ui.button('Back', on_click=lambda: ui.open('/')).classes('bg-transparent')
        show_module = ui.switch(text="紧凑模式", value=False, on_change=lambda: ui.open("/messages")).bind_value(app.storage.user, "show_module")
    if not os.path.exists('message.json'):
        with open('message.json', 'w', encoding="utf-8") as f:
            f.write(r'{}')
            message_json = {}
    else:
        with open('message.json', 'r', encoding="utf-8") as f:
            message_json = json.load(f)
    
    if message_json == {}:
        with ui.card().classes('absolute-center bg-transparent'):
            ui.badge('目前没人前来忏悔...', outline=True, color="", text_color='#E6354F').classes('text-xl')
    else:
        for key,value in dict(message_json).items():
            with ui.expansion(key).classes('w-full'):
                if show_module.value:
                    ui.textarea(value=value).classes('text-xl w-full').props('outlined readonly bg-color="green-1"')
                else:
                    ui.chat_message(value, avatar='static/bg.jpg').props('bg-color="green-1"').classes('text-h6')
            ui.separator()
    # app.on_disconnect(app.storage.user.clear())

def login():
    def try_login() -> None:
        if passwords.get(username.value) == hashlib.sha256(str(password.value).encode('utf-8')).hexdigest():
            app.storage.user.update({'user': username.value, 'authenticated': True})
            ui.open(app.storage.user.get('referrer_path', '/messages'))
        else:
            ui.notify('来访登记簿上没有您的名字哦', color='negative')

    ui.query('body').style('background: url("static/bg.jpg") 0px 0px/cover')
    with ui.card().classes('absolute-center'):
        ui.badge('桥洞教堂忏悔室登记处', outline=True, color='', text_color='#E6354F').classes('text-xl')
        username = ui.input('来访人').on('keydown.enter', try_login)
        password = ui.input('密码', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        with ui.row():
            ui.button('登记', on_click=try_login)
            ui.button('返回', on_click=lambda: ui.open("/"))

def main():
    router = Router()
    page_id = str(uuid4())

    @router.add('/')
    def page():
        ui.badge(f'桥洞教堂赎罪券投放处v{version}', outline=True, text_color="#E6354F", color="").classes('text-2xl absolute top-1/3 left-1/2 translate-x-[-50%]')

    @router.add('/nicegui/')
    def page():
        ui.badge(f'桥洞教堂赎罪券投放处v{version}', outline=True, text_color="#E6354F", color="").classes('text-2xl absolute top-1/3 left-1/2 translate-x-[-50%]')

    @router.add(f'/{page_id}')
    def index():
        send_button.set_visibility(False)
        login_button.set_visibility(False)

        def send():
            if text.value == '':
                ui.notify('虚假的赎罪是会被修女诅咒的！', type="negative", position="top")
                return
            if not os.path.exists('message.json'):
                with open('message.json', 'w', encoding="utf-8") as f:
                    f.write(r'{}')
                    message_json = {}
            else:
                with open('message.json', 'r', encoding="utf-8") as f:
                    message_json = json.load(f)
            if author.value == "":
                message_json[f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {len(text.value)}字"] = text.value
            else:
                message_json[f"{author.value} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {len(text.value)}字"] = text.value
            with open('message.json', 'w+', encoding="utf-8") as f:
                json.dump(message_json, f, indent=4, ensure_ascii=False)
            ui.notify('修女会保佑你的...', type="positive", position="top")
            text.set_value('')

        def back():
            with ui.dialog() as dialog, ui.card():
                ui.label('忏悔内容将不会被保存，确定要返回吗？')
                with ui.row().classes('w-full'):
                    ui.button('确定', on_click=lambda: ui.open('/'), color='#E6354F').classes("text-white")
                    ui.button('取消', on_click=dialog.close, color='#E6354F').classes("text-white")
            if not text.value == "":
                dialog.open()
            else:
                ui.open('/')

        def check():
            count = 1500
            if len(text.value) > int(count):
                with ui.dialog() as dialog, ui.card():
                    ui.label(f'字数大于{count}字（包括标点符号和换行）！确定要投稿吗？').classes('text-red')
                    with ui.row().classes('w-full'):
                        ui.button('确定', on_click=lambda :send(), color='#E6354F').classes("text-white").on(type='click', handler=dialog.close)
                        ui.button('取消', on_click=dialog.close, color='#E6354F').classes("text-white")
                dialog.open()
            else:
                send()

        def change():
            count.classes('text-white')
            count.set_text(f'{len(text.value)}/1500')
            if len(text.value) > 1500:
                count.classes('text-red')

        with ui.row().classes('w-full no-wrap'):
            author = ui.input(label="称呼(非必填)").props('input-class=mx-3').classes("absolute-center translate-x-[-50%] translate-y-[-200%]")
            text = ui.textarea(placeholder='忏悔内容', on_change=lambda: change()).props('rounded outlined input-class=mx-3"').classes('flex-grow')
            # ui.button('忏悔', on_click=lambda: call(), color='#E6354F').classes("absolute top-1/2 left-1/2 translate-x-[-50%] text-white")
            with ui.row().classes("absolute-center text-white"):
                ui.button('忏悔', on_click=lambda: check(), color='#E6354F').classes("text-white")
                ui.button('返回', on_click=lambda: back(), color='#E6354F').classes("text-white")
        count = ui.label('桑尾草原赎罪券投放处').classes('text-xs self-end mr-8 p-2').style('color: rgb(230 53 79)')

    ui.query('body').style('background: url("static/bg.jpg") 0px 0px/cover')
    with ui.row():
        send_button = ui.button('向桥洞修女发起忏悔', on_click=lambda: router.open(index), color="#E6354F").classes("absolute top-1/2 left-1/2 translate-x-[-50%] text-white")
        login_button = ui.button('桥洞教堂忏悔录', on_click=lambda: ui.open('/login'), color="#E6354F").classes("absolute top-1/2 left-1/2 translate-x-[-50%] translate-y-[200%] text-white bg-transparent")
        with ui.badge(outline=True, color="", text_color="#E6354F").classes("absolute top-2/3 left-1/2 translate-x-[-50%]"):
            ui.html('<center>注意事项<br>忏悔页面阅后即焚<br>刷新或关闭后页面将立即销毁<br>如需多次忏悔，可在忏悔后继续忏悔</center>').classes('text-xl')
            # ui.badge("忏悔页面阅后即焚", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[110%]")
            # ui.badge("刷新或关闭后页面将立即销毁", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[220%]")
            # ui.badge("如需多次忏悔，可在忏悔后继续忏悔", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[330%]")
            # ui.badge("请勿忏悔违法、违规、禁播内容", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[440%]")
        
        ui.button("装修日志", on_click=lambda: ui.open('/update'), color="#E6354F").classes("text-white bg-transparent")

    # 不可删除
    router.frame().classes('w-full')