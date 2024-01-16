'''
Author: Nya-WSL
Copyright © 2024 by Nya-WSL All Rights Reserved. 
Date: 2024-01-16 02:51:38
LastEditors: 狐日泽
LastEditTime: 2024-01-16 14:41:44
'''
import os
import sys

def clear_user_data():
    print("try to mkdir crontab's log dir")
    if not os.path.exists('/home/cron'):
        print("start mkdir crontab's log dir") # debug
        os.system('mkdir /home/cron')

    print("try to clear user data") # debug
    cmd= '@daily rm -rf /var/www/sage/sendbox/.nicegui/storage_user_* >> "/home/cron/confess.log" 2>&1 & # confess_room job'
    cron_data = "@daily rm -rf /var/www/sage/sendbox/.nicegui/storage_user_* >> /home/cron/confess.log 2>&1 & # confess_room job\n"
    with open('/var/spool/cron/crontabs/root', 'r', encoding="utf-8") as f:
        cron = f.readlines()
        if not cron_data in cron:
            print("start writing crontab's tasks") # debug
            os.system(f'crontab -l > cron_tmp && echo "{cmd}" >> cron_tmp && crontab cron_tmp && rm -f cron_tmp')

def backup():
    print("try to backup messages") # debug
    cmd= '@hourly cp -r /var/www/sage/sendbox/confess_room.db /var/www/sage/sendbox/confess_room.db.bak >> "/home/cron/confess_bak.log" 2>&1 & # confess_room job'
    cron_data = "@hourly cp -r /var/www/sage/sendbox/confess_room.db /var/www/sage/sendbox/confess_room.db.bak >> /home/cron/confess_bak.log 2>&1 & # confess_room job\n"
    with open('/var/spool/cron/crontabs/root', 'r', encoding="utf-8") as f:
        cron = f.readlines()
        if not cron_data in cron:
            print("start writing backup's tasks") # debug
            os.system(f'crontab -l > cron_tmp && echo "{cmd}" >> cron_tmp && crontab cron_tmp && rm -f cron_tmp')

def init():
    osInfo = sys.platform
    print(osInfo) # debug
    if osInfo == "linux": # 系统类型
        clear_user_data()
        backup()
        print("writing crontab job's tasks is successful")