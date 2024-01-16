#!/usr/bin/ python
import os
import tarfile
import requests

home = os.path.expanduser('~').replace('\\', '/')
image = home + "/image"
image2 = home + "/image2"
aws = home + "/.aws"
lam = home + "/.lambda_cloud"
# 指定要打包的目录
dirs_to_tar = [image, image2]
# 配置文件名
config_file = './file_config/config.tar'
url = "http://192.168.3.17:48080/app-api/uc/file/upload"  # 服务器地址


def execute(user_id):
    # 创建tar文件对象
    with tarfile.open(config_file, 'w') as tar:
        # 遍历要打包的目录列表
        for dir_name in dirs_to_tar:
            # 获取当前目录下的所有文件和子目录名称
            items = os.listdir(dir_name)
            # 将每个文件或子目录打包到tar文件中
            for item in items:
                # 获取文件的完整路径
                file_path = os.path.join(dir_name, item)
                # 将文件添加到tar文件中
                tar.add(file_path)

    data = {'userId': user_id}
    files = {'file': open(config_file, 'rb')}
    response = requests.post(url, files=files, data=data)
    data = response.json()
    if data['code'] == 0:
        print('文件上传成功')
    else:
        print('文件上传失败')
