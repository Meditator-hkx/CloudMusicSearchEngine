# coding: utf-8
import requests
import re
from bs4 import BeautifulSoup
import time
import os
from sql import sql


class Artist(object):
    def __init__(self):
        self.group_id_set = [1001, 1002, 1003,
                             2001, 2002, 2003,
                             4001, 4002, 4003,
                             6001, 6002, 6003,
                             7001, 7002, 7003]
        self.offset_low = 65
        self.offset_high = 90
        self.headers = {
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
        self.base_url = 'http://music.163.com/discover/artist/cat'
        self.sql_obj = sql.SQL()

    def craw(self, group_id, offset):
        params = {'id': group_id, 'initial': offset}
        r = requests.get(self.base_url, headers=self.headers, params=params)

        # Parse content
        soup = BeautifulSoup(r.content, 'html.parser')
        body = soup.body

        # hot_artists = body.find_all('a', attrs={'class': 'msk'})
        artists = body.find_all('a', attrs={'class': 'nm nm-icn f-thide s-fc0'})
        count = len(artists)
        print 'Crawing %d artists info this time ...\n' % count

        for artist in artists:
            artist_id = artist['href'].replace('/artist?id=', '').strip()
            artist_name = artist['title'].replace(u'的音乐', '')
            try:
                self.sql_obj.insert_artist(artist_id, artist_name)
            except Exception as e:
                # Print error info
                print(e)

if __name__ == '__main__':
    art_obj = Artist()
    for group_id in art_obj.group_id_set:
        offset_set = range(art_obj.offset_low, art_obj.offset_high+1)
        offset_set.append(0)

        for offset in offset_set:
            print 'Crawing in group %d, offset %d' % (group_id, offset)
            art_obj.craw(group_id, offset)
            print 'Sleep 10 seconds before next group crawing\n'

            time.sleep(10)