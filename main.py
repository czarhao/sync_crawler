# !/usr/bin/env python3
from flask import Flask
from login import login

app = Flask(__name__)


# 路由规则，/执行的命令/学号/密码
@app.route('/<do>/<sno>/<spw>')
def get(do, sno, spw):
    info = login(sno, spw, do)
    return info


def main():
    # 设置绑定的端口
    app.run(host='127.0.0.1', port=8081)


if __name__ == '__main__':
    main()
