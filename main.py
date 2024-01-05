'''
Author: Nya-WSL
Copyright © 2023 by Nya-WSL All Rights Reserved. 
Date: 2023-12-31 16:43:50
LastEditors: 狐日泽
LastEditTime: 2024-01-06 06:19:25
'''

import os
import json
import hashlib
from uuid import uuid4
from router import Router
from typing import Optional
from nicegui import ui, app
# from nicegui import Client
# from fastapi import Request
from datetime import datetime
from fastapi.responses import RedirectResponse
# from starlette.middleware.base import BaseHTTPMiddleware

# messages: List[Tuple[str, str, str, str]] = []
version = "1.2.0"
app.add_static_files('/static', 'static')
passwords = {'Sage': 'b10b88afa32c8c74941f600bb4507e6cbd5fb336bc82390ab0bbe9da07f08e90', 'sage': 'b10b88afa32c8c74941f600bb4507e6cbd5fb336bc82390ab0bbe9da07f08e90', 'sagesoft': '6a2c966fa4655342b1e8e2e2978a666bbb5971722c2f173ac13e848a0728f68f'}

@ui.page('/login', title="桥洞教堂忏悔室登记处")
def login() -> Optional[RedirectResponse]:
    ui.query('body').style('background: url("static/bg.jpg") 0px 0px/cover')
    def try_login() -> None:
        if passwords.get(username.value) == hashlib.sha256(str(password.value).encode('utf-8')).hexdigest():
            app.storage.user.update({'user': username.value, 'authenticated': True})
            ui.open(app.storage.user.get('referrer_path', '/messages'))
        else:
            ui.notify('来访登记簿上没有您的名字哦', color='negative')
    if app.storage.user.get('authenticated'):

        return RedirectResponse('/messages')
    else:
        with ui.card().classes('absolute-center'):
            ui.badge('桥洞教堂忏悔室登记处', outline=True, color='', text_color='#E6354F').classes('text-xl')
            username = ui.input('来访人').on('keydown.enter', try_login)
            password = ui.input('密码', password=True, password_toggle_button=True).on('keydown.enter', try_login)
            with ui.row():
                ui.button('登记', on_click=try_login)
                ui.button('返回', on_click=lambda: ui.open("/"))

@ui.page('/messages', title="桥洞教堂忏悔录")
def page():
    ui.query('body').style('background: url("static/bg.jpg") 0px 0px/cover')
    if not app.storage.user.get('authenticated'):
        return RedirectResponse('/login')
    else:
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

@ui.page('/')
# @ui.page('/{_:path}')
def main():
    router = Router()
    page_id = str(uuid4())

    @router.add('/')
    def init():
        ui.badge(f'桥洞教堂赎罪券投放处v{version}', outline=True, text_color="#E6354F", color="").classes('text-2xl absolute top-1/3 left-1/2 translate-x-[-50%]')

    @router.add('/nicegui/')
    def init():
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
                message_json[f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"] = text.value
            else:
                message_json[f"{author.value} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"] = text.value
            with open('message.json', 'w+', encoding="utf-8") as f:
                json.dump(message_json, f, indent=4, ensure_ascii=False)
            ui.notify('修女会保佑你的...', type="positive", position="top")

        def call():
            send()
            text.set_value('')

        def back():
            with ui.dialog() as dialog, ui.card():
                ui.label('忏悔内容将不会被保存，确定要返回吗？')
                with ui.row().classes('w-full'):
                    ui.button('确定', on_click=lambda: ui.open('/'), color='#E6354F').classes("text-white")
                    ui.button('取消', on_click=dialog.close, color='#E6354F').classes("text-white")
            dialog.open()

        with ui.row().classes('w-full no-wrap'):
            author = ui.input(label="称呼(非必填)").props('input-class=mx-3').classes("absolute-center translate-x-[-50%] translate-y-[-200%]")
            text = ui.textarea(placeholder='忏悔内容').props('rounded outlined input-class=mx-3"').classes('flex-grow')
            # ui.button('忏悔', on_click=lambda: call(), color='#E6354F').classes("absolute top-1/2 left-1/2 translate-x-[-50%] text-white")
            with ui.row().classes("absolute-center text-white"):
                ui.button('忏悔', on_click=lambda: call(), color='#E6354F').classes("text-white")
                ui.button('返回', on_click=lambda: back(), color='#E6354F').classes("text-white")
        ui.markdown('桑尾草原赎罪券投放处').classes('text-xs self-end mr-8 p-2').style('color: rgb(230 53 79)')

    ui.query('body').style('background: url("static/bg.jpg") 0px 0px/cover')
    with ui.row():
        send_button = ui.button('向桥洞修女发起忏悔', on_click=lambda: router.open(index), color="#E6354F").classes("absolute top-1/2 left-1/2 translate-x-[-50%] text-white")
        login_button = ui.button('桥洞教堂忏悔录', on_click=lambda: ui.open('/login'), color="#E6354F").classes("absolute top-1/2 left-1/2 translate-x-[-50%] translate-y-[200%] text-white bg-transparent")
        with ui.badge(outline=True, color="", text_color="#E6354F").classes("absolute top-2/3 left-1/2 translate-x-[-50%]"):
            ui.html('<center>注意事项<br>忏悔页面阅后即焚<br>刷新或关闭后页面将立即销毁<br>如需多次忏悔，可在忏悔后继续忏悔<br>请勿忏悔违法、违规、禁播内容</center>').classes('text-xl')
            # ui.badge("忏悔页面阅后即焚", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[110%]")
            # ui.badge("刷新或关闭后页面将立即销毁", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[220%]")
            # ui.badge("如需多次忏悔，可在忏悔后继续忏悔", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[330%]")
            # ui.badge("请勿忏悔违法、违规、禁播内容", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[440%]")

    # 不可删除
    router.frame().classes('w-full')

ui.run(title="桥洞教堂忏悔室", favicon="static/icon.ico", host="0.0.0.0", port=11452, language="zh-CN", show=False, storage_secret='c2b95787b44c084fc7c7d2c8422917913e0b1a673892f7d1f644bcf73c133410')