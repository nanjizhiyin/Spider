#encoding=utf-8

import sys  # 要重新载入sys。因为 Python 初始化后会删除 sys.setdefaultencoding 这个方 法
stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
reload(sys)
sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde
sys.setdefaultencoding('utf8')
from bs4 import BeautifulSoup
import urllib2
import MySQLdb
import os
import re
import datetime
from urlparse import urlparse

# 数据库
cursor = None
connect = None

# 获取网页内容
# forNum循环的次数
def getUrlHtml(urls, forNum):
    # 循环获取源码
    for url in urls:
        # 可用的URl地址
        newUrl = []
        # 下载源码
        print ("下载地址:" + url)
        try:
            html = urllib2.urlopen(url, timeout=30).read()
        except Exception as err:
            print("===========>下载失败:%s" % (err))
            continue
        # 解析器
        soup = BeautifulSoup(html, "lxml")
        # 所有的A标签
        pageurls = soup.find_all("a", href=True)
        for links in pageurls:
            href = links.get("href")
            # 判断条件,href中好多不是url地址
            if checkUrl(href):
                print '保存href:' + href
                # 保存到数据库
                installUrl(href)
                # 添加到新数组,进入下一个循环
                newUrl.append(href)
        if forNum > 0 and len(newUrl) > 0:
          getUrlHtml(newUrl, forNum - 1)

# 保存html源码


def installUrl(url):
    # 当前时间
    tmpdatetime = datetime.datetime.now()
    # 查询url是否已经存在
    sql = "SELECT urlID FROM spider_url WHERE url = '" + url + "'"
    count = cursor.execute(sql)
    if count > 0:
        # 如果已经存在请返回
        print '=============>已经存在:' + url
        return
    # 保存URL
    print '=============>保存url:' + url
    sql = "INSERT INTO spider_url(url,createDate) VALUES(%s,%s)"
    cursor.execute(sql, (url, tmpdatetime))

    connect.commit()
    print '保存成功:' + url

# 判断是否要下载此地址
def checkUrl(href):
    href = href.strip()
    if len(href) == 0 or href == "javascript:;" or href == "javascript:" or href.find('http://www.baidu.com/s?word') >= 0 or href.find('http') == -1 or href == "#":
        return False
    if href[-1] != '/':
        filename = os.path.basename(href)
        if filename != "html" or filename != "htm":
            return False
    return True


def checkDomain(domainID):
    # 读取数据
    sql = "SELECT domainID,domain FROM spider_domain"
    sql += ' WHERE domainID > %d' % (domainID)
    sql += ' LIMIT 10'

    count = cursor.execute(sql)
    print '总共有 %i 条记录' % (count)
    #获取所有结果
    results = cursor.fetchall()
    if len(results) == 0:
        print "没有更多数据了"
        return
    
    urls=[]
    for row in results:
        domainID = row[0]
        domain = row[1]
        print domainID
        print 'domain=' + domain
        urls.append(domain)
        
    getUrlHtml(urls, 6)
  
    print("===========>更新状态...")
    # 保存成功了,更新状态
    sql = "UPDATE spider_domain SET status = 1 WHERE domainID = %d " % (domainID)
    cursor.execute(sql)
    connect.commit()
    # 递归读取数据
    checkDomain(domainID)

if __name__ == '__main__':

    # 创建数据库
    connect = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='spider',
        charset='utf8mb4'
    )

    cursor = connect.cursor()

    print ("开始了")

    checkDomain(0)

