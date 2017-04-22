# encoding: utf-8

"""
Craw in music info page based on album ids obtained in CrawAlbum.py
Obtain all music ids, names, lyrics, comment numbers in this page
"""

import requests
from bs4 import BeautifulSoup
import time
from sql import sql
from Utilization import encrypt_func as ec
import re
import numpy as np
import json


class Music(object):
    def __init__(self):
        self.sql_obj = sql.SQL()
        # self.base_url_api = 'http://music.163.com/api/song/lyric?os=osx&id={}&lv=-1&kv=-1&tv=-1'.format(music_id)
        self.base_url_api = 'http://music.163.com/album/'
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

    def craw(self, album_id):
        params = {'id': album_id, 'limit': '200'}
        r= requests.get(self.base_url_api, headers=self.headers, params=params)

        # Parse content
        soup = BeautifulSoup(r.content, 'html.parser')
        body = soup.body

        # Obtain music number for each album
        music_number_info = body.find_all('span', attrs={'class': 'sub s-fc3'})
        # Update the number of TABLE album
        try:
            music_number_str = music_number_info[0]
            music_number_short_str = re.findall(r'sub s-fc3.+>(.+?)</span>',str(music_number_str))[0]
            print music_number_short_str, type(music_number_short_str)
            music_number = int(music_number_short_str.replace(str('首歌'), ''))
            self.sql_obj.update_album(album_id, music_number)
        except Exception as e:
            print e, 'Update album info failed!\n'

        musics = body.find_all('ul', attrs={'class': 'f-hide'})
        # Store info into TABLE music
        for music in musics:
            print music, type(music)
            try:
                # music id
                print str(music)
                music_id_short_str = music.find_all('a')[0]['href']
                music_id_final_str = music_id_short_str.replace('/song?id=', '')
                music_id = int(music_id_final_str)
                # music lyrics
                lyrics = self.get_lyric(music_id)
                # music name
                music_name = re.findall(r'/song.+>(.+?)</a>', str(music))
                music_name = music_name[0]
                self.sql_obj.insert_music(music_id, music_name, album_id, lyrics)
            except Exception as e:
                print e, "Error getting music_id | music_name | lyrics \n"

    def get_lyric(self, music_id):
        """
        Input music id, return lyrics of such a music
        """
        lyric_url = 'http://music.163.com/api/song/lyric?os=osx&id={}&lv=-1&kv=-1&tv=-1'.format(music_id)
        headers = {'Cookie': 'appver=1.5.0.75771;', 'Referer': 'http://music.163.com/song?id={}'.format(music_id)}
        # text = json.dumps(ec.TEXT)
        # sec_key = ec.create_secret_key(16)
        # enc_text = ec.aes_encrypt(ec.aes_encrypt(text, ec.NONCE), sec_key)
        # enc_sec_key = ec.rsa_encrypt(sec_key, ec.PUBKEY, ec.MODULUS)
        # data = {'params': enc_text, 'encSecKey': enc_sec_key}
        req = requests.post(lyric_url, headers=headers)
        return str(req.content)

if __name__ == '__main__':
    music_obj = Music()
    albums = music_obj.sql_obj.get_all_albums()
    sleep_flag = 0
    for album_id in albums:
        album_id = int(album_id[0])
        print 'Crawing comment info for music with id %d' % album_id
        music_obj.craw(album_id)
        # When every 100 albums' music information is crawed, sleep for random seconds in (0, 10)
        sleep_flag += 1
        if sleep_flag % 100 == 0:
            print 'Sleep random seconds before next 100 albums music information crawing\n'
            time.sleep(np.random.randint(5, 10))
    music_obj.sql_obj.close()