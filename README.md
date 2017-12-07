# Spider
使用python写的爬虫和网站
使用流程:
1.下载源码.安装mysql
2.手动创建数据库spider
3.进入spiders文件夹,执行python spider_init.py来创建数据表
4.执行python spider_domain.py先搜索几个根域名,用于后面的抓取数据
5.执行python spider_url.py 正式开始抓取全球的数据了.
6.执行spider_url一会后可以同时执行python spider_html.py用于抓取所有网页的内容并去掉所有的html标签


#搜索功能
1.cd search/python
2.python search.py
3.打开浏览器输入http://127.0.0.1:8889/s?wd=声明.就是在搜索'声明'两个字的所有网页
4.此代码是自己连接数据库,没有使用API

#查看数据库
1.cd search/python
2.python search_source.py
3.打开浏览器输入http://127.0.0.1:8888/html?contentID=1 查看第一条去掉标签的源码记录
3.打开浏览器输入http://127.0.0.1:8888/html?htmlID=1 查看第一条网页源码记录


#API给外部提供搜索接口,并返回json数据
1.cd api
2.python api.py
3.打开浏览器输入http://127.0.0.1:8890/s?wd=声明.返回所有相关的json内容

#前端和后端分离结构
#后端使用python的api提供数据,前端使用vue和react框架实现

#vue实现,代码在search/vue下面,执行下面的命令,启动项目
$ cd search/vue
$ npm run dev

