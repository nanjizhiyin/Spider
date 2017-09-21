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
import jieba
from urlparse import urlparse


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

# 获取网页的编码
def getCharset():
    html = '<meta http - equiv = "Content-Type" content = "text/html; charset=utf-8" /> < meta name = "publishid" content = "1167041.0.1002.0" / >'
    html = '<meta charset=utf-8><title>百度数据开放平台</title><script type=text/javascript> < meta name = "publishid" content = "1167041.0.1002.0" / >'
    # html = '<meta charset = "utf-8"/>adfasdfasdf'
    # html = '<meta charset = "utf-8" ><meta http - equiv = "X-UA-Compatible" content = "IE=edge,chrome=1" >'
    # html = "<meta charset = 'utf-8' ><meta sss='32323'>"

    # html= removeLabel(html)
    # print(html)

    hrefs = re.findall(
        r'<meta.*charset[\s]*=[\s]*["\']?([^"\'/>]*)', html, re.I | re.M)  # 去掉HTML注释

    for line in hrefs:
        print line
    
# 中文分词
def chineseFen():
    seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
    print("Full Mode: " + "/ ".join(seg_list))  # 全模式

    seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
    print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

    seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
    print(", ".join(seg_list))

    seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
    print(", ".join(seg_list))
    
if __name__ == '__main__':

    key = 'baidu'
    content = "Baidu asdfasfas"
    rpStr = '<em class="em">' + key + '</em>'
    reg = re.compile(re.escape(key), re.IGNORECASE)
    content = reg.sub(rpStr, content)
    print content

    # readTxt()
    # checkCode()
    # getCharset()
    # chineseFen()
  
