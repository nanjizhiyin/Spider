# coding=utf-8
import urllib2
url = "http://www.qq.com/"
headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
req = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(req)
html = response.read()
print html.decode('gbk')
