# 微信小程序中的教务网爬虫服务

沈阳师范大学的教务网爬虫，服务部署到内网服务器，包括借鉴的机器学习识别验证码，基于Beautiful Soup，Requests的爬虫，以及flask进行任务调度，返回json格式的数据与公网服务器进行交互。

解决依赖关系：

```
pip3 install -r requirements.txt
```

然后：

```
python3 main.py
```

访问如下的地址：

http://127.0.0.1:8081/schedule/sno/spw	# 返回课程表

http://127.0.0.1:8081/info/sno/spw	# 返回学生信息

http://127.0.0.1:8081/grade/sno/spw	# 返回成绩

http://127.0.0.1:8081/all/sno/spw	# 返回以上的全部内容