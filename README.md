# Drcom Executor

[![cqu-tool-bucket](https://img.shields.io/badge/CQU-%E9%87%8D%E5%BA%86%E5%A4%A7%E5%AD%A6%E5%85%A8%E5%AE%B6%E6%A1%B6%E8%AE%A1%E5%88%92-blue)](https://github.com/topics/cqu-tool-bucket)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/c3b9072a56d745ac868aabd676aa524c)](https://www.codacy.com/gh/CQU-AI/DrcomExecutor?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=CQU-AI/DrcomExecutor&amp;utm_campaign=Badge_Grade)
![Liscence](https://img.shields.io/github/license/CQU-AI/DrcomExecutor)
[![pypi](https://img.shields.io/pypi/v/cqu-de)](https://pypi.org/project/cqu-de/)
![download](https://pepy.tech/badge/cqu-de)
![Upload Python Package](https://github.com/CQU-AI/DrcomExecutor/workflows/Upload%20Python%20Package/badge.svg)

<div align=center> <img src="https://github.com/CQU-AI/DrcomExecutor/raw/master/doc/logo.png"><img src="https://github.com/CQU-AI/DrcomExecutor/raw/master/doc/logo.png"></div>

Drcom Executor 是一个基于 Python3 的第三方重庆大学 Dr.COM 登录器。

这个程序可以用来代替官方版的Drcom登录器来连接重庆大学校园网.

## 特性

使用本登陆器，你可以
 - 稳定开热点
 - 自动查询剩余流量与付费组
 - 开包即用，直接输入用户和密码，无需配置
 - 完美支持Mac和Linux,在Windows上也能稳定运行

## 安装和使用

1. 安装Python
2. 安装DE：`pip install cqu-de`
3. 在命令行中输入`cqu-de`即可开始运行
4. 首次运行，需要输入上网帐号和密码

上网帐号和密码会存储在你的电脑上，如需清除记录，可使用`cqu-de -r`

## TODO

- [x] 日志系统
- [x] 基于指数退避的自动重连机制
- [ ] 更丰富的配置选项

## 声明
1. 本程序核心代码主要基于 [drcom-generic](https://github.com/drcoms/drcom-generic) ,与该项目不同的是，我们主要考虑的是PC端的连接而不是路由器，故进行了一些改进与调整。
1. 本程序开放源代码，可自行检查是否窃取你的信息。
1. 本程序不存储用户的帐号，密码。