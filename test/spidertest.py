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

def checkCode():
    #可根据需要，选择不同的数据 
    html = urllib2.urlopen('http://www.people.com.cn/').read()
    print "编码"
    tmpDic = chardet.detect(html)
    print(tmpDic["encoding"])

if __name__ == '__main__':

    checkCode()
