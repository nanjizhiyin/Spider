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
# forNum 循环次数


def getUrlHtml(forNum):
    print '=========> 正在进行第 %i 轮' % forNum

    # 读取数据
    sql = "SELECT url FROM spider_url WHERE htmlStatus = 0 LIMIT 10 "
    count = cursor.execute(sql)
    print '总共有 %i 条记录'% count
    if count == 0:
        print '没有搜索到结果,说明所有网站都抓取完了'
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
        # 错误代码
        errormsg = ''
        try:
            html = urllib2.urlopen(url, timeout=30).read()
        except Exception as err:
            print("===========>下载失败:%s" % (err))
            continue

        print("===========>下载结束!开始操作SQL")
        htmlLen = len(html)
        if htmlLen > 0:
            print "源码长度:%d" % (htmlLen)
            # 保存源码
            installHtml(url, html)
        else:
            updateUrlErrorMsg(url, errormsg)

    # 下一轮
    print("===========>下一轮")
    getUrlHtml(forNum+1)

# 保存html源码


def installHtml(url, html):

    # 错误代码
    errormsg = ''
    # 当前时间
    tmpdatetime = datetime.datetime.now()
    # 判断编码格式
    print("===========>读取编码格式......")
    encoding = None
    charsets = re.findall(r'charset=([^"]*)', html, re.I | re.M)  # 去掉HTML注释
    if len(charsets) > 0:
        encoding = charsets[0]
        print "===========>编码1:%s" % (encoding)
    else:
        tmpDic = chardet.detect(html)
        encoding = tmpDic["encoding"]
        print "===========>编码2:%s" % (encoding)
    if encoding != None:
        encoding = encoding.lower()
        if encoding != 'utf-8':
            try:
                print("===========>转码....")
                if encoding == 'gb2312':
                    html = html.decode('gb18030').encode("utf-8")
                else:
                    html = html.decode(encoding).encode("utf-8")
            except Exception as err:
                print("===========>解码失败!")
                print(err)
                errormsg = '%s' % (err)
            finally:
                print("===========>解码完成!")

    # html = html.decode('windows-1254', errors='replace')
    # 删除html标签
    content = removeLabel(html)
    # 处理源码,去掉特殊符号
    html = removeHtmlSpe(html)
    errormsg = removeHtmlSpe(errormsg)

    try:
        print("===========>保存源码...")
        # 保存源码
        sql = "INSERT INTO spider_html(url,html,createDate) VALUES(%s,%s,%s)"
        cursor.execute(sql, (url, html, tmpdatetime))
    except Exception as err:
        print("===========>错误:%s" % (err))

    try:
        print("===========>保存去掉标签的源码...")
        # 保存去掉标签的源码
        # tmpStr = '此地址已经存在'
        sql = "INSERT INTO spider_content(url,content,createDate) VALUES(%s,%s,%s)"
        cursor.execute(sql, (url, content, tmpdatetime))
    except Exception as err:
        print("===========>错误:%s" % (err))

    try:
        print("===========>保存成功了,更新状态...")
        # 保存成功了,更新状态
        sql = "UPDATE spider_url SET htmlStatus = 1,encoding='%s',errormsg='%s' WHERE url = '%s' " % (
            encoding, errormsg, url)
        cursor.execute(sql)
    except Exception as err:
        print("===========>错误:%s" % (err))

    connect.commit()
    print '===========>源码已保存'

# 更新url状态

def updateUrlErrorMsg(url,errormsg):
    # 保存成功了,更新状态
    sql = "UPDATE spider_url SET htmlStatus = 2,errormsg='%s' WHERE url = '%s' " % (errormsg, url)
    cursor.execute(sql)
    connect.commit()
    
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
    #先过滤CDATA
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile(
        '<script[^>]*>[\\d\\D]*?</script>', re.I)  # Script
    re_style = re.compile(
        '<style[^>]*>[\\d\\D]*?</style>', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_a = re.compile(
        '<a[^>]*>([\s\S]*?)</a>')  # A标签
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    re_doctype = re.compile('<!DOCTYPE[^>]*>')  # DOCTYPE
    html = re_cdata.sub('', html)  # 去掉CDATA
    html = re_script.sub('', html)  # 去掉SCRIPT
    html = re_style.sub('', html)  # 去掉style
    html = re_br.sub('', html)  # 去掉HR
    html = re_a.sub('', html)  # 去掉A 标签
    html = re_h.sub('', html)  # 去掉HTML 标签
    html = re_comment.sub('', html)  # 去掉HTML注释
    html = re_doctype.sub('', html)  # 去掉DOCTYPE

    html = html.strip()
    html = html.replace("\n", "")
    html = html.replace("\r", "")
    html = html.replace("\t", "")
    html = html.replace("\b", "")
    html = html.replace("&nbsp", "")
    html = html.replace(" ", "")

    return html


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
