'''
Author: Nya-WSL
Copyright © 2023-2024 by Nya-WSL All Rights Reserved. 
Date: 2023-12-31 16:43:50
LastEditors: 狐日泽
LastEditTime: 2024-01-16 15:03:56
'''

import function
import confess_page
import update_page
from nicegui import ui, app
from typing import Optional
from fastapi.responses import RedirectResponse

# messages: List[Tuple[str, str, str, str]] = []
version = "1.2.6"
app.add_static_files('/static', 'static')

@ui.page('/login', title="桥洞教堂忏悔室登记处")
def page() -> Optional[RedirectResponse]:
    if app.storage.user.get('authenticated'):
        return RedirectResponse('/messages')
    else:
        confess_page.login()

@ui.page('/messages', title="桥洞教堂忏悔录")
def page():
    if not app.storage.user.get('authenticated'):
        return RedirectResponse('/login')
    else:
        confess_page.messages()

@ui.page('/update', title="桥洞教堂忏悔室装修日志")
def page():
    update_page.page()

@ui.page('/')
# @ui.page('/{_:path}')
def page():
    confess_page.main()

if __name__ == '__mp_main__':
    function.init()

ui.run(title="桥洞教堂忏悔室", favicon="static/icon.ico", host="0.0.0.0", port=11452, language="zh-CN", show=False, storage_secret='c2b95787b44c084fc7c7d2c8422917913e0b1a673892f7d1f644bcf73c133410')