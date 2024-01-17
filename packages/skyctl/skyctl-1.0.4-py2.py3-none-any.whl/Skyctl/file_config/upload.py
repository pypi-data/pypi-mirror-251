#!/usr/bin/env python3
import os
import tarfile
import requests

home = os.path.expanduser('~').replace('\\', '/')
image = home + "/image"
image2 = home + "/image2"
image3 = home + "/image3"
aws = home + "/.aws"
lam = home + "/.lambda_cloud"
azure = home + "/.azure"
# 指定要打包的目录
dirs_to_tar = [image, image2, image3]
# 配置文件名
config_file = './config.tar'
url = "http://192.168.3.17:48080/app-api/uc/file/upload"  # 服务器地址


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
    response = requests.post(url, files=files, data=data)
    data = response.json()
    if data['code'] == 0:
        print('文件上传成功')
    elif data['code'] == 1101000003:
        print('命名空间不存在')
    else:
        print('文件上传失败')
