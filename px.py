# -*-  coding = utf-8 -*-
# @Time : 2023/1/10 14:34
# @Author : Zhuangpx
# @File : px.py.py
# @Software : PyCharm

# 导入 requests 包
import requests

# 发送请求
x = requests.post('https://www.codeforces.com')

# 返回网页内容
f = open("px.html", "w", encoding="UTF-8")
f.write(x.text)
