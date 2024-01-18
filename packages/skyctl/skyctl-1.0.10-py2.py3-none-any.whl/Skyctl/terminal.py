#!/usr/bin/env python3
import requests
import configparser
import file_config.upload as upload


url_config = configparser.ConfigParser()
url_config.read('server_config.ini')
login_url = url_config['server']['login_url']


def ctl():
    while True:
        username = input("请输入你的用户名(exit-退出):")
        if username == 'exit':
            return
        password = input("请输入你的密码(exit-退出):")
        if password == 'exit':
            return
        data = {'username': username, 'password': password}
        response = requests.post(login_url, data=data)
        data = response.json()
        print('data', data)
        if data['code'] == 0:
            user_id = data['data']['id']
            print("用户：" + username + "登录成功")
            while True:
                option_other = input("请输入你的选择(create, upload, list, exit): ")
                if option_other == "create":
                    print("创建")
                elif option_other == "upload":
                    print("开始上传配置文件.....")
                    name_space = input("请输入配置文件的命名空间:")
                    upload.execute(user_id, name_space)
                elif option_other == "list":
                    print("列表")
                elif option_other == "exit":
                    print("退出")
                    return
        else:
            print('用户名或密码错误,请重新登录')


ctl()
