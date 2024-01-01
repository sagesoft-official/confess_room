'''
Author: Nya-WSL
Copyright © 2023 by Nya-WSL All Rights Reserved. 
Date: 2023-12-31 16:43:50
LastEditors: 狐日泽
LastEditTime: 2024-01-01 23:00:18
'''

import json
import time
from uuid import uuid4
from router import Router
from typing import Optional
from nicegui import ui, app, Client
# from nicegui import Client
# from fastapi import Request
from datetime import datetime
from fastapi.responses import RedirectResponse
# from starlette.middleware.base import BaseHTTPMiddleware

# messages: List[Tuple[str, str, str, str]] = []
app.add_static_files('/static', 'static')
passwords = {'Sage': 'sangyi45sui', 'SageSoft': 'sagesoft'}

@ui.page('/login', title="桥洞教堂忏悔室登记处")
def login() -> Optional[RedirectResponse]:
    def try_login() -> None:
        if passwords.get(username.value) == password.value:
            app.storage.user.update({'user': username.value, 'authenticated': True})
            ui.open(app.storage.user.get('referrer_path', '/messages'))
        else:
            ui.notify('来访登记簿上没有您的名字哦', color='negative')

    if app.storage.user.get('authenticated', True):
        return RedirectResponse('/messages')
    else:
        with ui.card().classes('absolute-center'):
            ui.badge('桥洞教堂忏悔室登记处', outline=True, color='pink').classes('text-xl')
            username = ui.input('来访人').on('keydown.enter', try_login)
            password = ui.input('密码', password=True, password_toggle_button=True).on('keydown.enter', try_login)
            ui.button('登记', on_click=try_login)

@ui.page('/messages', title="桥洞教堂忏悔录")
def page():
    if app.storage.user.get('authenticated', False) or app.storage.user.get('authenticated', ''):
        return RedirectResponse('/login')
    with ui.card().classes('absolute-center'):
        with open('message.json', 'r', encoding="utf-8") as f:
            message_json = json.load(f)
            for key,value in dict(message_json).items():
                ui.button(key, on_click=lambda: ui.open(f'/{str(key)}'))
                @ui.page(f'/{str(key)}')
                def message():
                    ui.textarea(value=value).classes('text-xl w-full')
                    ui.button('Back', on_click=lambda: ui.open('/messages')).classes('absolute-center')

@ui.page('/')
# @ui.page('/{_:path}')
def main():
    router = Router()
    page_id = str(uuid4())

    @router.add('/')
    def init():
        ui.badge('桥洞教堂赎罪券投放处', outline=True).classes('text-2xl absolute top-1/3 left-1/2 translate-x-[-50%]')

    @router.add(f'/{page_id}')
    def index():
        button.set_visibility(False)

        def send():
            if text.value == '':
                ui.notify('虚假的赎罪是会被修女诅咒的！', type="negative", position="top")
                return
            with open('message.json', 'r', encoding="utf-8") as f:
                message_json = json.load(f)
            message_json[f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"] = text.value
            with open('message.json', 'w+', encoding="utf-8") as f:
                json.dump(message_json, f, indent=4, ensure_ascii=False)
            ui.notify('修女会保佑你的...', type="positive", position="top")

        def call():
            send()
            text.set_value('')

        with ui.row().classes('w-full no-wrap items-center'):
            text = ui.textarea(placeholder='忏悔内容').props('rounded outlined input-class=mx-3').classes('flex-grow text-white')
            ui.button('忏悔', on_click=lambda: call()).classes("absolute top-1/2 left-1/2 translate-x-[-50%]")
        ui.markdown('桑尾草原赎罪券投放处').classes('text-xs self-end mr-8 text-pink p-2')

    ui.query('body').style('background: url("static/bg.jpg") 0px 0px/cover')
    with ui.row():
        button = ui.button('向桥洞修女发起忏悔', on_click=lambda: router.open(index), color="pink").classes("absolute top-1/2 left-1/2 translate-x-[-50%]")
        ui.badge("注意事项", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%]")
        ui.badge("忏悔页面阅后即焚", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[110%]")
        ui.badge("刷新或关闭后页面将立即销毁", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[220%]")
        ui.badge("如需多次忏悔，可在忏悔后继续忏悔", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[330%]")
        ui.badge("请勿忏悔违法、违规、禁播内容", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[440%]")

    # 不可删除
    router.frame().classes('w-full')

ui.run(title="桥洞教堂忏悔室", favicon="static/icon.ico", host="0.0.0.0", port=11452, language="zh-CN", show=False, storage_secret='SageSoft')