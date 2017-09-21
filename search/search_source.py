#encoding=utf-8
import sys
stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
reload(sys)
sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde
sys.setdefaultencoding('utf8')

import MySQLdb
import web

# 创建数据库
connect = None
cursor = None
app = None

# 显示html标签


class html:
    def GET(self):

        parameter = web.input()
        htmlID = parameter.htmlID

        mHtml = '<html><meta charset="UTF-8">'
        mHtml += '<title>HTML内容</title >'
        mHtml += '<style>div{background-color:darkgrey;}</style>'
        mHtml += '<body>'

        # 读取数据
        sql = "SELECT html FROM spider_html"
        if len(htmlID) > 0:
            sql += 'WHERE htmlID = %s' % (htmlID)
        sql += 'LIMIT 10'

        count = cursor.execute(sql)
        print '总共有 %i 条记录' % count
        print "获取所有结果:"
        #重置游标位置，0,为偏移量，mode＝absolute | relative,默认为relative,
        cursor.scroll(0, mode='absolute')
        #获取所有结果
        results = cursor.fetchall()
        for row in results:
            content = row[0]
            print content
            mHtml += '<xmp>' + content + '</xmp><br />'

        mHtml += "</body></html>"
        return mHtml

# 定义相应类


class content:
    def GET(self):
        parameter = web.input()
        contentID = parameter.contentID

        mHtml = '<html><meta charset="UTF-8">'
        mHtml += '<title>content内容</title >'
        mHtml += '<style>div{background-color:darkgrey;}</style>'
        mHtml += '<body>'

        # 读取数据
        sql = "SELECT content FROM spider_content"
        if len(contentID) > 0:
            sql += " WHERE contentID = %s " % (contentID)
        sql += ' LIMIT 10'

        count = cursor.execute(sql)
        print '总共有 %i 条记录', count
        print "获取所有结果:"
        #重置游标位置，0,为偏移量，mode＝absolute | relative,默认为relative,
        cursor.scroll(0, mode='absolute')
        #获取所有结果
        results = cursor.fetchall()
        for row in results:
            content = row[0]
            print content
            mHtml += '<div>' + content + '</div><br />'

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
    urls = ("/html", "html", "/content", "content")
    app = web.application(urls, globals())  # 绑定url
    web.httpserver.runsimple(app.wsgifunc(), ('127.0.0.1', 8889))
    app.run()
    # python index.py
    # 域名地址: http: // 0.0.0.0: 8080/
