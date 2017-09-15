#encoding=utf-8

import sys  # 要重新载入sys。因为 Python 初始化后会删除 sys.setdefaultencoding 这个方 法
stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
reload(sys)
sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde
sys.setdefaultencoding('utf8')
from bs4 import BeautifulSoup
import urllib
import MySQLdb
import os
import re

websiteurls={}
# 数据库
cursor = None
connect = None

# 获取网页内容

# recursion 是否递归
def getUrlHtml(url, recursion):
    # 下载源码
    html = urllib.urlopen(url).read()
    # print html
    # 处理源码,去掉特殊符号
    tmpHtml = checkHtml(html)
    content = removeLabel(html)
    # 保存源码
    installHtml(url, tmpHtml, content)
    # 解析器
    soup = BeautifulSoup(html, "lxml")
    # 所有的A标签
    pageurls = []
    pageurls = soup.find_all("a", href=True)
    for links in pageurls:
        href = links.get("href")
        print ("原始地址:"+href)
        # 判断条件,href中好多不是url地址
        if checkUrl(href):
            print '此地址可以使用'
            # getUrlHtml(href, 0)

# 保存html源码
def installHtml(url, html, content):
    # 查询url是否已经存在
    count = countUrl(url)
    if count > 0:
        # 如果已经存在请返回
        print '此地址已经存在'
        return
    # 保存源码
    tmpHtml = html.encode('utf-8')
    sql = "INSERT INTO spider_html(url,html) VALUES(%s,%s)"
    cursor.execute(sql, (url, tmpHtml))
    
    # 保存去掉标签的源码
    tmpStr = '此地址已经存在'  # content.encode('utf - 8')
    # sql = "INSERT INTO spider_content(url,content) VALUES(%s,%s)"
    sql = "INSERT INTO spider_content(url,content) VALUES('" + \
        url + "','" + tmpStr + "')"
    cursor.execute(sql)

    connect.commit()
    print '此地址已保存'

# 查询url是否已经存在
def countUrl(url):
    # 读取数据
    sql = "SELECT urlID FROM spider_html WHERE url = '" + url + "'"
    count = cursor.execute(sql)
    return count

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
            
    




# 处理源码,去掉特殊符号
def checkHtml(html):
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
        '<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile(
        '<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
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

# 初始化数据表
def initTable():
    #创建数据表
    sql = "CREATE TABLE if not exists spider_html(urlID int auto_increment primary key ,url Text COMMENT '网址',html LongText COMMENT 'html源码') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='html源码'"
    cursor.execute(sql)
    sql = "CREATE TABLE if not exists spider_content(urlID int auto_increment primary key ,url Text COMMENT '网址',content LongText COMMENT '删除html标签后的内容') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='去掉html标签后的代码'"
    cursor.execute(sql)
    # 清空数据库
    sql = "DELETE FROM spider_html"
    cursor.execute(sql)
    sql = "DELETE FROM spider_content"
    cursor.execute(sql)
    connect.commit()


if __name__ == '__main__':
  
    # 创建数据库
    connect = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='xpfirst',
        charset='utf8'
    )

    cursor = connect.cursor()
    initTable()

    print ("开始了")
    # 获取网页内容
    url = "https://www.hao123.com/"  # 这里是需要获取的网页
    getUrlHtml(url, 1)
