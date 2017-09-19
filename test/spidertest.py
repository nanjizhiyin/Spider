#encoding=utf-8
import sys  # 要重新载入sys。因为 Python 初始化后会删除 sys.setdefaultencoding 这个方 法
stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
reload(sys)
sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde
sys.setdefaultencoding('utf8')
import re
import chardet
import urllib2


def removeLabel(html):
    #先过滤CDATA

    re_comment = re.compile('<!--[^>]*-->')  # HTML注释

    html = re_comment.sub('', html)  # 去掉HTML注释



    return html

def checkCode():
    #可根据需要，选择不同的数据 
    html = urllib2.urlopen('http://www.people.com.cn/').read()
    print "编码"
    tmpDic = chardet.detect(html)
    print(tmpDic["encoding"])

if __name__ == '__main__':

    # checkCode()

    html = '<!--[if lt IE 9] >34253453535354<![endif]--> ASDFASDFASDFASDF'
    html= removeLabel(html)
    print(html)
