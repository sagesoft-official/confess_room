'''
Author: Nya-WSL
Copyright © 2023 by Nya-WSL All Rights Reserved. 
Date: 2023-12-31 16:43:50
LastEditors: 狐日泽
LastEditTime: 2023-12-31 21:44:18
'''

import json
from nicegui import ui
from uuid import uuid4
from router import Router
from datetime import datetime
from typing import List, Tuple

# messages: List[Tuple[str, str, str, str]] = []

@ui.page('/')  # normal index page (e.g. the entry point of the app)
@ui.page('/{_:path}')  # all other pages will be handled by the router but must be registered to also show the SPA index page
def main():
    router = Router()
    page_id = str(uuid4())

    @router.add('/')
    def init():
        ui.badge('赎罪券投放处', outline=True).classes('text-2xl')

    @router.add(f'/{page_id}')
    def index():
        button.set_visibility(False)
        async def send():
            if text.value == '':
                ui.notify('虚假的赎罪是会被修女诅咒的！', type="positive")
                return
            with open('message.json', 'r', encoding="utf-8") as f:
                message_json = json.load(f)
            message_json[f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"] = text.value
            with open('message.json', 'w+', encoding="utf-8") as f:
                json.dump(message_json, f, indent=4, ensure_ascii=False)
            text.set_value('')
            ui.notify('修女会保佑你的...')

        # user_id = str(uuid4())
        # avatar = f'https://robohash.org/{user_id}?bgset=bg2'

        with ui.row().classes('w-full no-wrap items-center'):
            # with ui.avatar().on('click', lambda: ui.open(main)):
            #     ui.image(avatar)
            text = ui.textarea(placeholder='按回车投放赎罪券').on('keydown.enter', send).props('rounded outlined input-class=mx-3').classes('flex-grow')
        ui.markdown('桑尾草原赎罪券投放处').classes('text-xs self-end mr-8 text-primary')

        # with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        #     chat_messages(user_id)

    with ui.row():
        button = ui.button('初始化', on_click=lambda: router.open(index)).classes('w-32')

    # this places the content which should be displayed
    router.frame().classes('w-full p-4 bg-gray-100')

ui.run(title="桥洞教堂忏悔室", favicon="./icon.ico", host="0.0.0.0", port=11452, language="zh-CN", show=False)