#!/usr/bin/ python
import requests
import file_config.upload as upload

url = "http://192.168.3.17:48080/app-api/uc/user/login"  # 服务器地址


def ctl():
    username = input("请输入你的用户名:")
    password = input("请输入你的密码:")
    data = {'username': username, 'password': password}
    response = requests.post(url, data=data)
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
                upload.execute(user_id)
            elif option_other == "list":
                print("列表")
            elif option_other == "exit":
                print("退出")
                return


ctl()
