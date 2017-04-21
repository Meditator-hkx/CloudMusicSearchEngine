# coding: utf-8

import urllib2
from bs4 import BeautifulSoup
import re
import requests


# base_url = 'http://club.xywy.com/doc_card/5866660'
# base_url2 = 'http://club.xywy.com/static/20170307/127336866.htm'
# home_url = 'http://www.xywy.com. '

id = 1875

# base_url = 'http://music.163.com/artist?id='
base_url = 'http://music.163.com/album?'
params = {'id': 34720827, 'limits': 200}
headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': '_ntes_nnid=7eced19b27ffae35dad3f8f2bf5885cd,1476521011210; _ntes_nuid=7eced19b27ffae35dad3f8f2bf5885cd; usertrack=c+5+hlgB7TgnsAmACnXtAg==; Province=025; City=025; _ga=GA1.2.1405085820.1476521280; NTES_PASSPORT=6n9ihXhbWKPi8yAqG.i2kETSCRa.ug06Txh8EMrrRsliVQXFV_orx5HffqhQjuGHkNQrLOIRLLotGohL9s10wcYSPiQfI2wiPacKlJ3nYAXgM; P_INFO=hourui93@163.com|1476523293|1|study|11&12|jis&1476511733&mail163#jis&320100#10#0#0|151889&0|g37_client_check&mailsettings&mail163&study&blog|hourui93@163.com; JSESSIONID-WYYY=189f31767098c3bd9d03d9b968c065daf43cbd4c1596732e4dcb471beafe2bf0605b85e969f92600064a977e0b64a24f0af7894ca898b696bd58ad5f39c8fce821ec2f81f826ea967215de4d10469e9bd672e75d25f116a9d309d360582a79620b250625859bc039161c78ab125a1e9bf5d291f6d4e4da30574ccd6bbab70b710e3f358f%3A1476594130342; _iuqxldmzr_=25; __utma=94650624.1038096298.1476521011.1476588849.1476592408.6; __utmb=94650624.11.10.1476592408; __utmc=94650624; __utmz=94650624.1476521011.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            'DNT': '1',
            'Host': 'music.163.com',
            'Pragma': 'no-cache',
            'Referer': 'http://music.163.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
# proxies = {
#   "http": "http://10.10.1.10:3128",
#   "https": "http://10.10.1.10:1080",
# }

# response_base = requests.get(base_url, headers = headers, params=params)
# print response_base.url
#
# raw_html_base = response_base.content

# response_des = urllib2.urlopen(des_url)
# raw_html_des = response_des.read()

# html_gbk = raw_html.decode('gbk')
# print html_gbk
# soup_base = BeautifulSoup(raw_html_base, 'html')
# body_base = soup_base.body
# # print body_base
#
# name_result = re.findall(r'<h2 class="sname f-thide sname-max".+id="artist-name" title=.+>(.+?)</h2>', str(body_base))

# print name_result[0]

# soup_des = BeautifulSoup(raw_html_des, 'html')
# body_des = soup_des.body
# print body_des

# 在 body 中找到 artist id, name 信息
# art_id = id
# artist_name = re.findall(r'<h2 class="sname f-thide sname-max".+id="artist-name" title=.+>(.+?)</h2>', str(body_base))
# art_name = artist_name[0]

# artist_info = re.findall(r'<div class = "n-artdesc">(.+?)',str(body_des))

# print art_id, art_name


# match = re.search(r'artist-name(.+)</h2>', str(body))
# name = match.group()

### 放弃所有描述
# string = str(soup.head)
#
# result_name = re.findall(r'<title>(.+?) -', string)
# rule_decription = '<meta content="(.+?)cloud，netease cloud music'
# result_des = re.findall(r'(.+)property="og:abstract"', string)
# print result_des[0]
# if len(result_des) < 1:
#     result_des = re.findall(r'<meta content=".+',string)
#     des = result_des[3]
# else:
#     des = result_des[0]
#
# name = result_name[0]
# # des = result_des[3]
#
# # des = des.replace('<meta content="','')
#
# print name, des



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

music_id = 4435
lyric_url = 'http://music.163.com/api/song/lyric?os=osx&id={}&lv=-1&kv=-1&tv=-1'.format(music_id)
req = requests.post(lyric_url, headers=headers)
print req.content