# -*- coding: utf-8 -*-

from nowstagram import app
from qiniu import Auth, put_data, put_file
import os

# 需要填写你的 Access Key 和 Secret Key
access_key = app.config['QINIU_ACCESS_KEY']
secret_key = app.config['QINIU_SECRET_KEY']
# 构建鉴权对象，进行初始化对接
q = Auth(access_key, secret_key)
# 要上传的空间
bucket_name = app.config['QINIU_BUCKET_NAME']
sava_dir = app.config['UPLOAD_DIR']  # 保存目录
domain_prefix = app.config['QINIU_DOMAIN']


# 上传文件到七牛云服务器所需函数操作
# source_file为待上传文件，save_file_name为文件名
def qiniu_upload_file(source_file, save_file_name):
    # 1.上传客户端向业务服务器申请一个上传凭证(Upload Token)；业务服务器返回一个上传凭证(token)给上传客户端
    # 传入上传到的空间名以及待上传的文件名。
    token = q.upload_token(bucket_name, save_file_name)
    # 2.上传客户端构建上传请求，上传文件到七牛云存储服务器；七牛云存储服务器返回客户端文件上传的结果。
    # 还有put_file,put_stream等上传函数。
    ret, info = put_data(token, save_file_name, source_file.stream)  # 文件上传到七牛云服务器
    # 3.根据上传状态如何，将文件所在七牛云服务器的URL地址返回，用于存入数据库；
    # print type(info.status_code), info  调试时使用，看上传后的状态信息等
    if info.status_code == 200:
    # 若状态码为200，则上传成功；则将七牛云服务器保存刚上传图片的URL地址返回，用于将该URL地址存入Image表的数据库中；
        return domain_prefix + save_file_name
    return None
