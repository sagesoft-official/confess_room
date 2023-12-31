'''
Author: Nya-WSL
Copyright © 2023 by Nya-WSL All Rights Reserved. 
Date: 2023-12-31 16:43:50
LastEditors: 狐日泽
LastEditTime: 2024-01-01 05:26:12
'''

import json
from uuid import uuid4
from router import Router
from nicegui import ui, app
from datetime import datetime
from typing import List, Tuple

# messages: List[Tuple[str, str, str, str]] = []
app.add_static_files('/static', 'static')

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

ui.run(title="桥洞教堂忏悔室", favicon="static/icon.ico", host="0.0.0.0", port=11452, language="zh-CN", show=False)