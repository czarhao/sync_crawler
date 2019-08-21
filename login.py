#!/usr/bin/env python3
import json
import os

from captcha.main import get_code
from other import *
import requests
from route import route
from student.models import Student


# 无论执行什么样的操作都要先登录到教务网的

# 创建一个验证码识别的对象

def login(sno, spw, do):  # 实现登录的代码
    try:
        login_session = requests.session()  # 需要一个登录的session，后期的操作都基于这个session
        get_text = login_session.get("http://210.30.208.126/", headers=headers_user_agent())
        now_url = get_text.url[:49]
        get_soup, _ = return_soup(get_text)
        send_data = set_data(sno, spw, get_soup.find('input').get('value'), "学生", now_url, login_session)
        send_header = set_header(now_url)
        login_info = login_session.post(now_url + "default2.aspx", data=send_data, headers=send_header)
        login_soup, login_text = return_soup(login_info)
        login_success, err_info = jud_login(login_text)
        if login_success:  # 当登录成功了进入路由，根据do进行进行下一步操作
            return json.dumps(route(do, Student(sno, spw), login_session, now_url, login_soup, send_header, True, ""),
                              ensure_ascii=False)
        else:  # 若是错误为验证码不对，则重复这个函数，反之返回登录失败的json
            if err_info == "验证码不正确":
                return login(sno, spw, do)
            else:
                return json.dumps(route(do, Student("", ""), "", "", "", "", False, err_info), ensure_ascii=False)
    except Exception as err_info:
        return json.dumps(route(do, Student("", ""), "", "", "", "", False, str(err_info)), ensure_ascii=False)


def read_captcha(this_url):  # 机器学习识别验证码
    return get_code(this_url + "CheckCode.aspx")


def set_header(this_url):  # 设置登录包的头文件
    return {
        "Cache-Control": "max-age = 0",
        "Origin": "http://210.30.208.126",
        "Upgrade-Insecure-Requests": "1",
        "Referer": this_url + "default2.aspx",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3",
        'user-agent': user_agent()
    }


def set_data(user, password, view_state, user_type, this_url, session):  # 设置登录包的数据
    code = read_captcha(this_url)
    return {
        "__VIEWSTATE": view_state,
        "txtUserName": user,
        "TextBox2": password,
        "txtSecretCode": code,
        "RadioButtonList1": user_type.encode('gb2312'),
        "Button1": "",
        "lbLanguage": "",
        "hidPdrs": "",
        "hidsc": ""
    }


def jud_login(body):  # 判断登录是否成功
    # 还有很多别的错误
    if "验证码不正确" in body:
        return False, "验证码不正确"
    if "用户名不存在" in body:
        return False, "用户名不存在或未按照要求参加教学活动"
    if "密码错误" in body:
        return False, "密码错误"
    return True, ""
