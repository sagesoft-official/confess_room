import os
import hashlib
import confess_db
from uuid import uuid4
from router import Router
from nicegui import ui, app
from datetime import datetime
from main import version

def messages():
    ui.query('body').style('background: url("static/bg.jpg") 0px 0px/cover')
    with ui.row():
        ui.button('Quit', on_click=lambda: (app.storage.user.clear(), ui.navigate.to('/'))).classes('bg-transparent')
        ui.button('Back', on_click=lambda: ui.navigate.to('/')).classes('bg-transparent')
        show_module = ui.switch(text="紧凑模式", value=False, on_change=lambda: ui.navigate.to("/messages")).bind_value(app.storage.user, "show_module")
        show_module.set_visibility(False)
    if not os.path.exists('confess_room.db'):
        confess_db.create()
        message_list = []
    else:
        message_list = confess_db.check_message()

    if message_list == []:
        with ui.card().classes('absolute-center bg-transparent'):
            ui.badge('目前没人前来忏悔...', outline=True, color="", text_color='#E6354F').classes('text-xl')
    else:
        for i in message_list:
            message = str(i["message"]).replace("\n", "\n\n").replace("\\n", "\n\n")
            with ui.expansion(i["user"]).classes('w-full'):
                if show_module.value:
                    ui.textarea(value=message).classes('text-xl w-full').props('outlined readonly bg-color="green-1"')
                else:
                    ui.chat_message(message, avatar='static/bg.jpg').props('bg-color="green-1"').classes('text-h6')
            ui.separator()
    # app.on_disconnect(app.storage.user.clear())

def login():
    def try_login() -> None:
        if confess_db.check_user(username.value)[1] == hashlib.sha256(str(password.value).encode('utf-8')).hexdigest():
            app.storage.user.update({'user': username.value, 'authenticated': True})
            ui.navigate.to(app.storage.user.get('referrer_path', '/messages'))
        else:
            ui.notify('来访登记簿上没有您的名字哦', color='negative')

    ui.query('body').style('background: url("static/bg.jpg") 0px 0px/cover')
    with ui.card().classes('absolute-center'):
        ui.badge('桥洞教堂忏悔室登记处', outline=True, color='', text_color='#E6354F').classes('text-xl')
        username = ui.input('来访人').on('keydown.enter', try_login)
        password = ui.input('密码', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        with ui.row():
            ui.button('登记', on_click=try_login)
            ui.button('返回', on_click=lambda: ui.navigate.to("/"))

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
            if not os.path.exists('confess_room.db'):
                confess_db.create()
            if author.value == "":
                confess_db.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {len(text.value)}字", text.value)
            else:
                confess_db.write(f"{author.value} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {len(text.value)}字", text.value)
            ui.notify('修女会保佑你的...', type="positive", position="top")
            text.set_value('')

        def back():
            with ui.dialog() as dialog, ui.card():
                ui.label('忏悔内容将不会被保存，确定要返回吗？')
                with ui.row().classes('w-full'):
                    ui.button('确定', on_click=lambda: ui.navigate.to('/'), color='#E6354F').classes("text-white")
                    ui.button('取消', on_click=dialog.close, color='#E6354F').classes("text-white")
            if not text.value == "":
                dialog.open()
            else:
                ui.navigate.to('/')

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
        login_button = ui.button('桥洞教堂忏悔录', on_click=lambda: ui.navigate.to('/login'), color="#E6354F").classes("absolute top-1/2 left-1/2 translate-x-[-50%] translate-y-[200%] text-white bg-transparent")
        with ui.badge(outline=True, color="", text_color="#E6354F").classes("absolute top-2/3 left-1/2 translate-x-[-50%]"):
            ui.html('<center>注意事项<br>忏悔页面阅后即焚<br>刷新或关闭后页面将立即销毁<br>如非必要请勿在忏悔界面撰写投稿<br>您应该在撰写完毕后直接复制过来<br>如需多次忏悔，可在忏悔后继续忏悔</center>').classes('text-xl')
            # ui.badge("忏悔页面阅后即焚", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[110%]")
            # ui.badge("刷新或关闭后页面将立即销毁", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[220%]")
            # ui.badge("如需多次忏悔，可在忏悔后继续忏悔", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[330%]")
            # ui.badge("请勿忏悔违法、违规、禁播内容", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[440%]")
        
        ui.button("装修日志", on_click=lambda: ui.navigate.to('/update'), color="#E6354F").classes("text-white bg-transparent")

    # 不可删除
    router.frame().classes('w-full')