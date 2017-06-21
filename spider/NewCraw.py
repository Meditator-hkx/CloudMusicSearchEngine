# coding: utf-8
import json

import requests
import re
from bs4 import BeautifulSoup
from sql import sql_craw
from Utilization import encrypt_func
import time
import numpy as np

BASE_URL = 'http://music.163.com/'



import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)



class Crawler(object):
    def __init__(self):
        # self.group_id_set = [1001, 1002, 1003,
        #                      2001, 2002, 2003,
        #                      4001, 4002, 4003,
        #                      6001, 6002, 6003,
        #                      7001, 7002, 7003]
        self.group_id_set = [1001, 1002, 1003]
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
        self.album_url = 'http://music.163.com/artist/album'
        self.music_url = 'http://music.163.com/album/'
        self.sql_obj = sql_craw.SQL()
        self.fhand = open('music_download.txt', 'w')
        self.count = 0

    def craw(self, group_id, offset):
        # Step 1: craw artist
        artists = self.craw_artist(group_id, offset)
        for artist in artists[0:11]:
            artist_id = artist['href'].replace('/artist?id=', '').strip()
            artist_name = artist['title'].replace(u'的音乐', '')
            print 'artist info: ', artist_id, artist_name

            # Step 2: craw album
            albums = self.craw_album(artist_id)
            for album in albums[0:11]:
                album_id = album['href'].replace('/album?id=', '')
                album_name = re.findall(r'/album.+>(.+?)</a>', str(album))
                album_name = album_name[0]
                print 'album info: ', album_id, album_name

                # Step3: get musics
                musics = self.craw_music(album_id)
                for music in musics:
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

                    # comment number
                    comment_number = self.get_comment_number(music_id)

                    # mp3 file name
                    mp3_name = artist_name +  u'_' + music_name + u'.mp3'

                    # lyric name
                    lyric_name = artist_name +  u'_' + music_name + u'.lrc'

                    print 'music_info: ', music_id, music_name, mp3_name, comment_number

                    # Write music_url to download to music_download.txt
                    to_write = 'http://music.163.com/song?id=' + str(music_id)
                    self.fhand.write(to_write)
                    self.fhand.write('\n')
                    # Insert into database
                    try:
                        self.sql_obj.insert_music_new(music_id, music_name, album_name, artist_name, lyrics, mp3_name, comment_number, lyric_name)
                    except Exception as e:
                        print e
                    finally:
                        self.count += 1
                        if self.count % 100 == 0:
                            time.sleep(np.random.randint(5, 10))

    def craw_artist(self, group_id, offset):
        params = {'id': group_id, 'initial': offset}
        r = requests.get(self.base_url, headers=self.headers, params=params)

        # Parse content
        soup = BeautifulSoup(r.content, 'html.parser')
        body = soup.body

        # hot_artists = body.find_all('a', attrs={'class': 'msk'})
        artists = body.find_all('a', attrs={'class': 'nm nm-icn f-thide s-fc0'})
        count = len(artists)
        print 'Crawing 10 artists info this time ...\n'
        return artists

    def craw_album(self, artist_id):
        params = {'id': artist_id, 'limit': '200'}
        r = requests.get(self.album_url, headers=self.headers, params=params)
        # Parse content
        soup = BeautifulSoup(r.content, 'html.parser')
        body = soup.body
        albums = body.find_all('a', attrs={'class': 'tit s-fc0'})  # Obtain all albums
        return albums

    def craw_music(self, album_id):
        params = {'id': album_id, 'limit': '200'}
        r = requests.get(self.music_url, headers=self.headers, params=params)

        # Parse content
        soup = BeautifulSoup(r.content, 'html.parser')
        body = soup.body

        # Obtain music number for each album
        musics = body.find_all('ul', attrs={'class': 'f-hide'})
        return musics


    def get_lyric(self, music_id):
        lyric_url = 'http://music.163.com/api/song/lyric?os=osx&id={}&lv=-1&kv=-1&tv=-1'.format(music_id)
        headers = {'Cookie': 'appver=1.5.0.75771;', 'Referer': 'http://music.163.com/song?id={}'.format(music_id)}
        # text = json.dumps(ec.TEXT)
        # sec_key = ec.create_secret_key(16)
        # enc_text = ec.aes_encrypt(ec.aes_encrypt(text, ec.NONCE), sec_key)
        # enc_sec_key = ec.rsa_encrypt(sec_key, ec.PUBKEY, ec.MODULUS)
        # data = {'params': enc_text, 'encSecKey': enc_sec_key}
        req = requests.post(lyric_url, headers=headers)
        return str(req.content)

    def get_comment_number(self, music_id):
        url = BASE_URL + 'weapi/v1/resource/comments/R_SO_4_' + str(music_id) + '/?csrf_token='
        headers = {'Cookie': 'appver=1.5.0.75771;', 'Referer': 'http://music.163.com/'}
        text = {'username': '', 'password': '', 'rememberLogin': 'true'}
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        nonce = '0CoJUm6Qyw8W8jud'
        pubKey = '010001'
        text = json.dumps(text)
        secKey = encrypt_func.create_secret_key(16)
        encText = encrypt_func.aes_encrypt(encrypt_func.aes_encrypt(text, nonce), secKey)
        encSecKey = encrypt_func.rsa_encrypt(secKey, pubKey, modulus)
        data = {'params': encText, 'encSecKey': encSecKey}
        req = requests.post(url, headers=headers, data=data)
        comment_number = req.json()['total']
        return comment_number


if __name__ == '__main__':
    craw_obj = Crawler()
    for group_id in craw_obj.group_id_set:
        offset_set = range(craw_obj.offset_low, craw_obj.offset_high+1)
        offset_set.append(0)

        for offset in offset_set:
            print 'Crawing in group %d, offset %d' % (group_id, offset)
            craw_obj.craw(group_id, offset)

    craw_obj.sql_obj.close()
    craw_obj.fhand.close()