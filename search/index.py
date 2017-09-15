# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb
import web


# 创建数据库
connect = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='root',
    db='xpfirst',
)

cursor = connect.cursor()

urls = ("/.*", "hello")        # 指定任何url都指向hello类
app = web.application(urls, globals())  # 绑定url

# 定义相应类
class hello:
    def GET(self):

        mHtml = '<html><meta charset="UTF - 8">'
        mHtml += '<title>PyWeb</title >'
        mHtml += '<style>div{background-color:darkgrey;}</style>'
        mHtml +'<body>'

        # # 读取数据
        sql = "SELECT content FROM spider_content"
        count = cursor.execute(sql)
        print '总共有 %s 条记录', count
        print "获取所有结果:"
        #重置游标位置，0,为偏移量，mode＝absolute | relative,默认为relative,
        cursor.scroll(0, mode='absolute')
        #获取所有结果
        results = cursor.fetchall()
        for row in results:
            print row
            content = row[0]
            mHtml += '<div>'+content+'</div><br />'

        mHtml += "</body></html>"
        return mHtml

if __name__ == "__main__":
    app.run()
    # 域名地址: http: // 0.0.0.0: 8080/
