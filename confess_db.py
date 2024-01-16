'''
Author: Nya-WSL
Copyright © 2024 by Nya-WSL All Rights Reserved. 
Date: 2024-01-16 12:45:32
LastEditors: 狐日泽
LastEditTime: 2024-01-16 14:55:33
'''

import sqlite3

DatabasePath = "confess_room.db"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create():
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()
    c.execute("CREATE TABLE user(user,passwd)")
    c.execute("CREATE TABLE messages(id,user,message)")
    conn.commit()
    conn.close()

def check_user(user):
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()
    # 获取passwd
    result = c.execute(f"SELECT * FROM user WHERE user = '%s'" % user).fetchone()
    #关闭连接
    conn.close()
    return result

def check_message():
    conn = sqlite3.connect(DatabasePath)
    conn.row_factory = dict_factory
    c = conn.cursor()
    # 获取投稿
    result = c.execute(f"SELECT * FROM messages").fetchall()
    #关闭连接
    conn.close()
    return result

def write(user, message):
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()
    c.execute("INSERT INTO messages (user,message) VALUES (?,?)", (user, message))
    conn.commit()
    conn.close()