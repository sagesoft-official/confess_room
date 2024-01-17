'''
Author: Nya-WSL
Copyright © 2024 by Nya-WSL All Rights Reserved. 
Date: 2024-01-17 16:28:27
LastEditors: 狐日泽
LastEditTime: 2024-01-17 17:20:49
'''

import os
from qiniu import Auth, put_file, etag

#需要填写你的 Access Key 和 Secret Key
access_key = 'Access_Key'
secret_key = 'Secret_Key'

#构建鉴权对象
q = Auth(access_key, secret_key)

#要上传的空间
bucket_name = 'Your_Bucket_Name'

#上传后保存的文件名
key = 'sagesoft/cfr/confess_room.db'

#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)

#要上传文件的本地路径
localfile = 'confess_room.db'

ret, info = put_file(token, key, localfile, version='v1') 
print(info)
assert ret['key'] == key
assert ret['hash'] == etag(localfile)

os.system('cp -r confess_room.db confess_room.db.bak')