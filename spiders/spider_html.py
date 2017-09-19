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

# 数据库
cursor = None
connect = None

# 获取网页内容

# recursion 是否递归


def getUrlHtml(urlID):

    # 读取数据
    sql = "SELECT url FROM spider_url WHERE urlID > %i AND htmlStatus = 0 LIMIT 10 " % (
        urlID)
    count = cursor.execute(sql)
    print '总共有 %i 条记录'% count
    if count == 0:
        print '没有搜索到结果'
        return
    #重置游标位置，0,为偏移量，mode＝absolute | relative,默认为relative,
    cursor.scroll(0, mode='absolute')
    #获取所有结果
    results = cursor.fetchall()
    for row in results:
        url = row[0]
        print "读取url:" + url
        # 下载源码
        html = ''
        try:
            html = urllib2.urlopen(url, timeout=30).read()
        except Exception as err:
            print("===========>下载失败!")
            print(err)
        finally:
            print("===========>下载结束!")

        htmlLen = len(html)
        if htmlLen > 0:
            print "源码长度:%d" % (htmlLen)
            # 处理源码,去掉特殊符号
            tmpHtml = removeHtmlSpe(html)
            content = removeLabel(html)
            # 保存源码
            installHtml(url, tmpHtml, content)
   
# 保存html源码
def installHtml(url, html, content):
    # 当前时间
    tmpdatetime = datetime.datetime.now()
    # 判断编码格式
    tmpDic = chardet.detect(html)
    encoding = tmpDic["encoding"]
    print "encoding:" + encoding
    if encoding != 'utf-8':
        try:
            html = html.encode('utf-8')
            content = content.encode('utf-8')
        except Exception as err:
            print("===========>解码失败!")
            print(err)
            html = unicode(html, errors='replace').encode("utf-8")
            content = unicode(content, errors='replace').encode("utf-8")
        finally:
            print("===========>解码完成!")

    # 保存源码
    sql = "INSERT INTO spider_html(url,html,createDate) VALUES(%s,%s,%s)"
    cursor.execute(sql, (url, html, tmpdatetime))

    # 保存去掉标签的源码
    # tmpStr = '此地址已经存在'
    sql = "INSERT INTO spider_content(url,content,createDate) VALUES(%s,%s,%s)"
    cursor.execute(sql, (url, content, tmpdatetime))

    # 保存成功了,更新状态
    sql = "UPDATE spider_url SET htmlStatus = 1,encoding='%s' WHERE url = '%s' " % (encoding,
        url)
    cursor.execute(sql)

    connect.commit()
    print '===========>源码已保存'


# 处理源码,去掉特殊符号
def removeHtmlSpe(html):
    html = html.strip()
    html = html.replace("\n", "")
    html = html.replace("\r", "")
    html = html.replace("\t", "")
    html = html.replace("\b", "")
    html = html.replace("\"", "\\\"")
    html = html.replace("\'", "''")
    return html


# 删除html标签
def removeLabel(html):
    html = html.strip()
    html = html.replace("\n", "")
    html = html.replace("\r", "")
    html = html.replace("\t", "")
    html = html.replace("\b", "")
    #先过滤CDATA
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile(
        '(?i)(<SCRIPT)[\\s\\S]*?((</SCRIPT>)|(/>))', re.I)  # Script
    re_style = re.compile(
        '(?i)(<style)[\\s\\S]*?((</style>)|(/>))', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s = re_cdata.sub('', html)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('\n', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    #去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    return s


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
    getUrlHtml(0)
