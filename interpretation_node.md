# interpretation_note

解读 [宁宁](https://github.com/ConanYu) 的good-guy项目及源码，并注些笔记。

这个仓库是爬信息的东西，就是启动服务器，然后按照写好的方法去爬实时数据过来，然后显示一下。

crwal_service是爬虫的服务端，python写的，使用多线程，gRPC框架

client demo是拿服务器爬下来的信息然后显示到web的客户端

怎么传？用gRPC

怎么拿？py+go-client

## 一些知识

### PyPI

Python的正式第三方库

## Makefile

### protobuf

去官网下载protobuf，`make protobuf`构建一下，生成`crawl_service_pb2.py`，`crawl_service_pb2.pyi`，`crawl_service_pb2_grpc.py`三个文件。

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

https://doc.oschina.net/grpc?t=60138)

### grpcio grpcio-tools

适用python下的gRPC的第三方库

### protobuf

序列化框架，和gRPC一起使用

## crwl_service

### `__init__.py`

关于`__init__.py`可以看[这里](https://zhuanlan.zhihu.com/p/474874811)。

大致来说，就是管理包和模块的。

### crawl_service_impl.py

impl：实现

各种func实现抓取，然后把数据返回了

比如`GetRecentContest()`抓了最近比赛信息，搞一搞格式然后返回

~~具体代码不懂~~

### crawl_service[.proto | _pb2.py | _pb2.pyi | pb2_grpc.py] + grpc

grpcio和grpcio-tools是第三方库

[RPC框架：从原理到选型，一文带你搞懂RPC](https://www.51cto.com/article/701423.html)

[gRPC 官方文档中文版 V1.0](https://doc.oschina.net/grpc)

[python使用protobuf](https://developers.google.com/protocol-buffers/docs/reference/python-generated#invocation)

[Protocol Buffers](https://developers.google.com/protocol-buffers/docs/overview)

[grpc-python](https://doc.oschina.net/grpc?t=60138)

[什么是RPC](https://www.jianshu.com/p/7d6853140e13)

这里是gRPC的服务端部分。

RPC就是远程的两个服务，客户端A要调用服务端B的方法，这个过程。

因为是远程的，所以涉及http远程传输，这里是A把Func参数压成二进制的字节流，然后传给B，B再把字节流搞回成参数，这个过程是**序列化**和**反序列化**。

protobuf，即Google Protocol Buffers，是一套工具库（一个序列化框架）。用来存储数据，用于**服务端与客户端通信**。

特点是**二进制**。

于是就可以利用protobuf来帮助RPC传输序列化的参数过去。

gRPC的话是支持很多语言的RPC框架，这里用它来搞成python文件。

先写.proto协议文件，它里面定义了数据的格式，然后用protobuf的编译器把它编译成python语言，生成_pb2.py文件（就是给服务器的Func）

_pb2是.protobuf的版本2或3的意思，这样和版本1区别开。

xx_pb2.py是**数据格式调用的文件**，就是上面的Func参数，用这段代码来调用B的方法。

xx_pb2_grpc.py是gRPC搞出来的方法调用文件，上面的文件只是一些参数，用了gRPC以后主要调用过程在这里。

xx_pb2.pyi是对应上面那个.py文件的[存根文件](https://blog.csdn.net/weixin_40908748/article/details/106252884)。.pyi文件里有一些类型标注（所以后续敲代码会有提示补全）。

### http_service.py

这个是http的service，就是启动爬虫服务器的

### grpc_service.py

这个是grpc的service，启动的是grpc（远程调用）服务器的

### no_service.py

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

这个是用多线程搞http_server的，相当于整个项目的服务

### util

此目录放一些工具

在这里就是一些功能函数，可以比成c++的utility，拿个目录，然后写一些功能函数，要的时候就拿来用。

#### go.py

搞多线程然后给东西进去跑的。

三个函数嵌套

[装饰器](https://www.runoob.com/w3cnote/python-func-decorators.html)

- class:_Thread：

线程类

继承 threading.Thread 重写 `__init__() `和 `run()`

- class:_Promise：

[property()函数](https://www.runoob.com/python/python-func-property.html)

#### config.py

配置 yaml文件

比如在http_service.py的serve()里给ip和端口（post&port）然后配置

~~看不懂这堆配置~~

#### const.py

名词列表

设置一些常量

#### new_session.py

使用requests发送http请求的session配置，有http报文首部信息

#### catcher.py

异常捕捉

报一下错，`internal error`接不上。

### crawler

针对每个网站写方法，用来登录或者拿数据之类的。

## client demo

上面说过gRPC的服务端部分，这里就有客户端部分。

