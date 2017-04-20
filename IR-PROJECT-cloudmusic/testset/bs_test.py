# coding: utf-8

import urllib2
from bs4 import BeautifulSoup
import re


# base_url = 'http://club.xywy.com/doc_card/5866660'
# base_url2 = 'http://club.xywy.com/static/20170307/127336866.htm'
# home_url = 'http://www.xywy.com. '

base_url = 'http://music.163.com/artist?id=1876'

response = urllib2.urlopen(base_url)
raw_html = response.read()
# html_gbk = raw_html.decode('gbk')
# print html_gbk
soup = BeautifulSoup(raw_html, 'html')
# match = re.search(r'artist-name(.+)</h2>', str(body))
# name = match.group()

### 放弃所有描述
string = str(soup.head)

result_name = re.findall(r'<title>(.+?) -', string)
rule_decription = '<meta content="(.+?)cloud，netease cloud music'
result_des = re.findall(r'(.+)property="og:abstract"', string)
print result_des[0]
if len(result_des) < 1:
    result_des = re.findall(r'<meta content=".+',string)
    des = result_des[3]
else:
    des = result_des[0]

name = result_name[0]
# des = result_des[3]

# des = des.replace('<meta content="','')

print name, des



#
# doc = ['<html><head><title>Page title</title></head>',
#        '<body><p id="firstpara" align="center">This is paragraph <b>one</b>.',
#        '<p id="secondpara" align="blah">This is paragraph <b>two</b>.',
#        '</html>']
# soup = BeautifulSoup(''.join(doc))
# #
#
# print soup.prettify()
#
# print soup.contents[0].name
# print soup.contents[0].contents[0].name
# head = soup.contents[0].contents[0]
# print head.parent.name
# print head.next
# print head.nextSibling.name
# print head.nextSibling.contents[0]
# print head.nextSibling.contents[0].nextSibling
# print soup.findAll('p', align="center")
# # print soup.findAll('p', attrs={'align':'center'})
# print soup('p', align="center")[0]['id']
# print soup.find('p', align=re.compile('^b.*'))['id']
# print soup.find('p').b.string
# print soup('p')[1].b.string