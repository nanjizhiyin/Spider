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
1.cd search
2.python search.py
3.打开浏览器输入http://127.0.0.1:8889/s?wd=声明.就是在搜索'声明'两个字的所有网页