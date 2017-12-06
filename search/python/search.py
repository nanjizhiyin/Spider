#encoding=utf-8
import sys
stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
reload(sys)
sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde
sys.setdefaultencoding('utf8')

import MySQLdb
import web
import jieba
import itertools
import re

# 创建数据库
connect = None
cursor = None
app = None

# 定义相应类
class search:
    def GET(self):
        parameter = web.input()
        # 搜索关键字
        word = parameter.wd

        keys = []
        seg_list = jieba.cut_for_search(word)  # 搜索引擎模式
        for key in seg_list:
            keys.append(key)
        searchWord = " ".join(seg_list)
        print('searchWord='+searchWord)

        mHtml = '<html><meta charset="UTF-8">'
        mHtml += '<title>搜索结果</title >'
        mHtml += '<style> .url{color: blue} .em{color: red} .content{} </style>'
        mHtml += '<body>'

        # 读取数据
        sql = "SELECT url,content,MATCH(content) AGAINST('%s') AS score FROM spider_content ORDER BY score desc" % (
            searchWord)
        sql += ' LIMIT 10'

        count = cursor.execute(sql)
        print '总共有 %i 条记录', count
        print "获取所有结果:"
        #重置游标位置，0,为偏移量，mode＝absolute | relative,默认为relative,
        cursor.scroll(0, mode='absolute')
        #获取所有结果
        results = cursor.fetchall()
        for row in results:
            url = row[0]
            content = row[1]
            print content
            for key in keys:
                rpStr = '<em class="em">' + key + '</em>'
                reg = re.compile(re.escape(key), re.IGNORECASE)
                content = reg.sub(rpStr, content)
                
            mHtml += '<div>'
            mHtml += '<a class="url" href="' + url + '">' + url + '</a>'
            mHtml += '<div class="content">' + content + '</div>'
            mHtml += '</div><br />'

        mHtml += "</body></html>"
        return mHtml

if __name__ == "__main__":

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

    # 指定任何url都指向content类
    urls = ("/s", "search")
    app = web.application(urls, globals())  # 绑定url
    web.httpserver.runsimple(app.wsgifunc(), ('127.0.0.1', 8889))
    app.run()
    # python search.py
    # 域名地址: http://127.0.0.1:8889/
    # 搜索: http://127.0.0.1:8889/s?wd=声明
