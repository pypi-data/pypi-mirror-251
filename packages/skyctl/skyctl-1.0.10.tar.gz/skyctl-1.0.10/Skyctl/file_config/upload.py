#!/usr/bin/env python3
import os
import tarfile
import requests
import configparser

home = os.path.expanduser('~').replace('\\', '/')
upload_config = configparser.ConfigParser()
upload_config.read('server_config.ini')
# image = home + upload_config['file_path']['image']
# image2 = home + "/image2"
# image3 = home + "/image3"
# skypilot配置文件
aws = home + upload_config['file_path']['aws']
lam = home + upload_config['file_path']['lambda']
azure = home + upload_config['file_path']['azure']
# 指定要打包的目录
dirs_to_tar = [aws, lam, azure]
# 配置文件名
config_file = upload_config['file']['file_name']
# 上传路径
upload_url = upload_config['server']['upload_url']


def execute(user_id, name_space):
    # 创建tar文件对象
    with tarfile.open(config_file, 'w') as tar:
        # 遍历要打包的目录列表
        for dir_name in dirs_to_tar:
            # 判断文件夹是否为空
            if os.path.exists(dir_name) and os.path.isdir(dir_name):
                # 获取当前目录下的所有文件和子目录名称
                items = os.listdir(dir_name)
                # 将每个文件或子目录打包到tar文件中
                for item in items:
                    # 获取文件的完整路径
                    file_path = os.path.join(dir_name, item)
                    # 将文件添加到tar文件中
                    tar.add(file_path)

    data = {'userId': user_id, 'nameSpace': name_space}
    files = {'file': open(config_file, 'rb')}
    response = requests.post(upload_url, files=files, data=data)
    data = response.json()
    if data['code'] == 0:
        print('文件上传成功')
    elif data['code'] == 1101000003:
        print('命名空间不存在')
    else:
        print('文件上传失败')
