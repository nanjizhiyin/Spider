# coding=utf-8
from bs4 import BeautifulSoup
import urllib
import MySQLdb
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
    html = checkHtml(html)
    # 保存源码
    installHtml(url, html)
    # 解析器
    soup = BeautifulSoup(html)
    # 所有的A标签
    pageurls = []
    pageurls = soup.find_all("a", href=True)
    for links in pageurls:
        href = links.get("href")
        # 判断条件,href中好多不是url地址
        if recursion == 1 and href != "javascript:;" and href != "javascript:" and href != "#":
            print href
            filename = href.split(".")[-1]
            print filename
            if filename != "apk":
                getUrlHtml(href, 0)


def checkHtml(html):
    html = html.strip()
    html = html.replace("\n", "")
    html = html.replace("\r", "")
    html = html.replace("\t", "")
    html = html.replace("\b", "")
    html = html.replace("\"", "\\\"")
    html = html.replace("\'", "''")
    return html
    
# 保存html源码
def installHtml(url, html):
    #插入一条数据

    # 保存数据
    sql = "INSERT INTO spider_html(url,html) VALUES('" + \
        url + "','" + html + "')"
    result = cursor.execute(sql)
    connect.commit()
  
# 初始化数据表
def initTable():
    #创建数据表
    sql = "CREATE TABLE if not exists spider_html(urlid int auto_increment primary key ,url Text COMMENT '网址',html LongText COMMENT 'html源码') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='URL地址'"
    cursor.execute(sql)
    # 清空数据库
    sql = "DELETE FROM spider_html"
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
  )
  cursor = connect.cursor()
  initTable()

  # 获取网页内容
  url = "https://www.hao123.com/"  # 这里是需要获取的网页
  getUrlContent(url,1)
