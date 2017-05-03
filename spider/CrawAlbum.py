# encoding: utf-8

"""
Craw album information based on the artist id obtained in CrawArtist.py
1. For each artist_id, obtain its artist homepage with album info
2. Obtain all the album ids, names in this page and store to sqlite3
"""

import requests
import re
from bs4 import BeautifulSoup
from sql import sql_craw
import time
import numpy as np


class Album(object):
    def __init__(self):
        self.sql_obj = sql_craw.SQL()
        self.base_url = 'http://music.163.com/artist/album'
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

    def craw(self, artist_id):
        params = {'id': artist_id, 'limit': '200'}
        r= requests.get(self.base_url, headers=self.headers, params=params)

        # print r.url

        # Parse content
        soup = BeautifulSoup(r.content, 'html.parser')
        body = soup.body

        albums = body.find_all('a', attrs={'class': 'tit s-fc0'})  # Obtain all albums

        for album in albums:
            album_id = album['href'].replace('/album?id=', '')
            try:
                album_name = re.findall(r'/album.+>(.+?)</a>', str(album))
                album_name = album_name[0]
                self.sql_obj.insert_album(album_id, album_name, artist_id)
            except Exception as e:
                print e


if __name__ == '__main__':
    album_obj = Album()
    artists = album_obj.sql_obj.get_all_artists()
    sleep_flag = 0

    # Stopped at id 2979 on Friday, 2017-4-21
    # Stopped at id 4715 on Friday, 2017-4-21
    # Stopped at id 4837 on Friday, 2017-4-21
    # ---------------------------------------
    # Stopped at id 5198 on Friday, 2017-4-21
    # Stopped at id 6557 on Friday, 2017-4-21
    # Stopped at id 7205 on Friday, 2017-4-21
    # Stopped at id 7298 on Friday, 2017-4-21
    # Stopped at id 7432 on Friday, 2017-4-21
    # Stopped at id 12867 on Friday, 2017-4-21
    # Stopped at id 15877 on Friday, 2017-4-21
    # Stopped at id 16938 on Friday, 2017-4-21
    # Stopped at id 17047 on Friday, 2017-4-21
    # Stopped at id 35343 on Saturday, 2017-4-22
    # try: 40000
    for artist_id in artists:
        artist_id = int(artist_id[0])
        if artist_id < 34517:
            continue
        print 'Crawing album info for artist with id %d' % artist_id
        album_obj.craw(artist_id)
        sleep_flag += 1
        # When every 10 artists' album information is crawed, sleep for random seconds in (0, 10)
        if sleep_flag % 10 == 0:
            print 'Sleep random seconds before next 100 artists album crawing\n'
            time.sleep(np.random.randint(0, 5))
    album_obj.sql_obj.close()