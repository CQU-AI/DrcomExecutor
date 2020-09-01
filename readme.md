# Drcom Executor

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/c3b9072a56d745ac868aabd676aa524c)](https://www.codacy.com/gh/CQU-AI/DrcomExecutor?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=CQU-AI/DrcomExecutor&amp;utm_campaign=Badge_Grade)
![Liscence](https://img.shields.io/github/license/CQU-AI/DrcomExecutor)
[![pypi](https://img.shields.io/pypi/v/cqu-de)](https://pypi.org/project/cqu-de/)
![download](https://pepy.tech/badge/cqu-de)

<div align=center> <img src="./doc/logo.png"><img src="./doc/logo.png"></div>

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
3. 在命令行中输入`de`即可开始运行
4. 首次运行，需要输入上网帐号和密码

上网帐号和密码会存储在你的电脑上，如需清除记录，可使用`de -r`

## TODO

- [ ] 日志系统
- [ ] 基于指数退避的自动重连机制
- [ ] 更丰富的配置选项

## 声明

本程序核心代码主要基于 [drcom-generic](https://github.com/drcoms/drcom-generic) 。
