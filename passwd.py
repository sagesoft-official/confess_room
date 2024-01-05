'''
Author: Nya-WSL
Copyright © 2024 by Nya-WSL All Rights Reserved. 
Date: 2024-01-05 22:38:08
LastEditors: 狐日泽
LastEditTime: 2024-01-05 22:40:47
'''
import hashlib

passwd = input("明文密码：")
print(hashlib.sha256(str(passwd).encode('utf-8')).hexdigest())