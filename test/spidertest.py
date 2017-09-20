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
import chardet


def removeLabel(html):
    #先过滤CDATA

    re_comment = re.compile('<meta[^>]*?charset=(\\w+)[\\W]*?>')  # HTML注释

    html = re_comment.sub('', html)  # 去掉HTML注释



    return html

def checkCode():
    #可根据需要，选择不同的数据 
    html = urllib2.urlopen('http://www.people.com.cn/').read()
    print "编码"
    tmpDic = chardet.detect(html)
    print(tmpDic["encoding"])

# 读取txt
def readTxt():

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
    path = sys.path[0]
    f = open(path+'/test.txt')
    text = f.read()
    # html = text.decode('windows-1254', errors='replace').encode("utf-8")

    # 保存去掉标签的源码
    # tmpStr = '此地址已经存在'
    # 当前时间
    tmpdatetime = datetime.datetime.now()
    sql = "INSERT INTO spider_content(url,content,createDate) VALUES(%s,%s,%s)"
    cursor.execute(sql, ("text.com", text, tmpdatetime))
    connect.commit()
    print '===========>源码已保存'




    f.close()

if __name__ == '__main__':

    # readTxt()
    # checkCode()

    html = '<meta http - equiv = "Content-Type" content = "text/html; charset=utf-8" /> < meta name = "publishid" content = "1167041.0.1002.0" / >'
    # html= removeLabel(html)
    # print(html)

    hrefs = re.findall(r'charset=([^"]*)', html, re.I | re.M)  # 去掉HTML注释
    for line in hrefs:
        print line
    # # 解析器
    # soup = BeautifulSoup(html, "lxml")
    # # 所有的A标签
    # pageurls = soup.find_all("meta")
    # for links in pageurls:
    #     href = links.get("content")
    #     print href
    #     hrefs = re.findall(r'charset=(.*)', href, re.I | re.M)  # 去掉HTML注释
    #     for line in hrefs:
    #         print line  

