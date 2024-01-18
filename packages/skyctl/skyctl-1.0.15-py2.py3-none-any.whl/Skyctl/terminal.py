#!/usr/bin/env python3
import requests
import configparser
import file_config.upload as upload
import os


url_config = configparser.ConfigParser()
# 脚本当前的绝对路径
current_path = os.path.abspath(os.path.dirname(__file__))
url_config.read(current_path + '/server_config.ini')
login_url = url_config['server']['login_url']
upload_url = url_config['server']['upload_url']


def ctl():
    while True:
        username = input("请输入用户名(exit-退出):").strip()
        if username == 'exit':
            return
        password = input("请输入密码(exit-退出):").strip()
        if password == 'exit':
            return
        data = {'username': username, 'password': password}
        response = requests.post(login_url, data=data)
        data = response.json()

        if data['code'] == 0:
            user_id = data['data']['id']
            print("用户：" + username + "登录成功")
            while True:
                option_other = input("请输入你的选择(create, upload, list, exit): ").strip()
                if option_other == "create":
                    print("创建")
                elif option_other == "upload":
                    print("开始上传配置文件.....")
                    name_space = input("请输入Namespace:").strip()
                    upload.execute(user_id, name_space, upload_url)
                elif option_other == "list":
                    print("列表")
                elif option_other == "exit":
                    print("退出Skyctl终端")
                    return
        else:
            print('用户名或密码错误,请重新登录')


ctl()
