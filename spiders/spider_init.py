#encoding=utf-8

import MySQLdb
import datetime

# 数据库
cursor = None
connect = None

# 初始化数据表
def initTable():
    #创建数据表
    # 保存url地址
    sql = "CREATE TABLE if not exists spider_url(urlID int auto_increment primary key ,url Text NOT NULL COMMENT '网址',encoding VARCHAR(30),errormsg Text COMMENT '错误日志',htmlStatus INT(1) DEFAULT 0 COMMENT '1:保存到content成功 2:http下载失败',createDate datetime) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='url地址'"
    cursor.execute(sql)
    # 保存网页源码
    sql = "CREATE TABLE if not exists spider_html(htmlID int auto_increment primary key ,url Text NOT NULL COMMENT '网址',html LongText COMMENT 'html源码',createDate datetime) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='html源码'"
    cursor.execute(sql)
    # 保存去掉标签的源码
    sql = "CREATE TABLE if not exists spider_content(contentID int auto_increment primary key ,url Text NOT NULL COMMENT '网址',content LongText COMMENT '删除html标签后的内容',createDate datetime) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='去掉html标签后的代码'"
    cursor.execute(sql)
    print('创建数据库成功')
    # 清空数据库
    
    sql = "UPDATE spider_url SET htmlStatus = 0"
    cursor.execute(sql)
    sql = "DELETE FROM spider_html"
    cursor.execute(sql)
    sql = "DELETE FROM spider_content"
    cursor.execute(sql)
    connect.commit()


if __name__ == '__main__':
    print('开始')
  
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
    initTable()
    print('结束')

