# interpretation_note

解读 [宁宁](https://github.com/ConanYu) 的good-guy项目及源码，并注些笔记。

## Makefile

### protobuf

去官网下载protobuf，`make protobuf`构建以下，生成`crawl_service_pb2.py`，`crawl_service_pb2.pyi`，`crawl_service_pb2_grpc.py`三个文件。

## tree

```c++
.../goodguy-crawl$ tree crawl_service
crawl_service
├── __init__.py
├── crawl_service.proto
├── crawl_service_impl.py
├── crawler	// 对不同平台爬数据
│   ├── __init__.py
│   ├── acwing
│   │   └── get_acwing_recent_contest.py
│   ├── atcoder
│   │   ├── __init__.py
│   │   ├── get_atcoder_contest_data.py
│   │   ├── get_atcoder_contest_duration.py
│   │   └── get_atcoder_recent_contest.py
│   ├── codechef
│   │   ├── __init__.py
│   │   └── get_codechef_recent_contest.py
│   ├── codeforces
│   │   ├── __init__.py
│   │   ├── get_codeforces_contest_data.py
│   │   ├── get_codeforces_recent_contest.py
│   │   └── get_codeforces_submit_data.py
│   ├── leetcode
│   │   ├── __init__.py
│   │   ├── get_leetcode_contest_record.py
│   │   ├── get_leetcode_csrf_token.py
│   │   ├── get_leetcode_daily_question.py
│   │   └── get_leetcode_recent_contest.py
│   ├── luogu
│   │   ├── __init__.py
│   │   ├── get_luogu_recent_contest.py
│   │   └── get_luogu_submit_data.py
│   ├── nowcoder
│   │   ├── __init__.py
│   │   ├── get_nowcoder_contest_data.py
│   │   └── get_nowcoder_recent_contest.py
│   ├── request_executor.py
│   ├── uoj
│   │   ├── __init__.py
│   │   ├── login.py
│   │   └── md5.py
│   └── vjudge
│       ├── __init__.py
│       ├── get_vjudge_submit_data.py
│       └── login.py
├── grpc_service.py
├── http_service.py
├── no_service.py
├── service.py
├── tree_crawl_service.txt
└── util	// util库 工具/功能库
    ├── __init__.py
    ├── catcher.py	// 异常捕捉
    ├── config.py	// crawl service的配置
    ├── const.py	// 名词列表 设置一些常量
    ├── go.py	// 多线程创建 http_service调用
    └── new_session.py

11 directories, 44 files
```

## requirements.txt

第三方库

```c++
requests	// 发送http请求 并返回结果
cachetools
readerwriterlock
grpcio		// grpc-io
grpcio-tools // grpc-toos
lxml		// 解析库 支持html和xml
protobuf
PyYAML
js2py
flask
gevent
```

### requests

Python 内置了 requests 模块，该模块主要用来发 送 HTTP 请求，requests 模块比 [urllib](https://www.runoob.com/python3/python-urllib.html) 模块更简洁。

[菜鸟教程-requests](https://www.runoob.com/python3/python-requests.html)

### lxml

lxml是python的一个解析库，支持HTML和XML的解析，支持XPath解析方式。

[lxml](https://www.cnblogs.com/mq0036/p/13161350.html)，[lxml安装与使用](http://c.biancheng.net/python_spider/lxml.html)

### grpc

grpcio和grpcio-tools

[RPC框架：从原理到选型，一文带你搞懂RPC](https://www.51cto.com/article/701423.html)

[gRPC 官方文档中文版 V1.0](https://doc.oschina.net/grpc)

[grpc-python](https://doc.oschina.net/grpc?t=60138)

## crwl_service

### `__init__.py`

关于`__init__.py`可以看[这里](https://zhuanlan.zhihu.com/p/474874811)。

大致来说，就是管理包和模块的。

### service.py

- logging：

一个日志模块

- **serve()**：

去run主体的serve。

`go()(http_service)()`

实际 `go():decorator(http_service):wrapper()`

`grpc_service()`

- main：

logging的基础配置，全局的，先进行init。
然后调用一下server去跑服务。

### crawl_service_impl.py

impl：实现

各种func实现抓取，然后把数据返回了

比如`GetRecentContest()`抓了最近比赛信息，搞一搞格式然后返回

~~具体代码不懂~~

### crawl_service_pb2.py

### crawl_service_pb2.pyi

### crawl_service_pb2_grpc.py

### http_service.py

### grpc_service.py

### no_service.py

### util

此目录放一些工具

#### go.py

三个函数嵌套

[装饰器](https://www.runoob.com/w3cnote/python-func-decorators.html)

- class:_Thread：

线程类

继承 threading.Thread 重写 `__init__() `和 `run()`

- class:_Promise：

[property()函数](https://www.runoob.com/python/python-func-property.html)

#### config.py

配置 yaml文件

在http_service.py的serve()里给ip和端口（post&port）然后配置

==暂时看不懂这堆配置==

#### const.py

名词列表

设置一些常量

#### new_session.py

使用requests发送http请求的session配置，有http报文首部信息

#### catcher.py

异常捕捉

报一下错，`internal error`接不上。

### crawler

