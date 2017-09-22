# Spider
使用python写的爬虫和网站
使用流程:
1.下载源码.安装mysql
2.手动创建数据库spider
3.进入spiders文件夹,执行python spider_init.py来创建数据表
4.执行python spider_domain.py先搜索几个根域名,用于后面的抓取数据
5.执行python spider_url.py 正式开始抓取全球的数据了.
6.执行spider_url一会后可以同时执行python spider_html.py用于抓取所有网页的内容并去掉所有的html标签
