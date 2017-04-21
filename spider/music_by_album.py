# coding: utf-8


# Obtain all music IDs according the albums


import json
import re
import time

import requests
from bs4 import BeautifulSoup

from sql import sql


class Music(object):
    def __init__(self):
        self.sql_obj = sql.SQL()
        self.BASE_URL = 'http://music.163.com/'
        self.BASE_ALBUM_URL = 'http://music.163.com/#/album?id='
        self.BASE_API_URL = 'http://music.163.com/api/album/'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': '_ntes_nnid=7eced19b27ffae35dad3f8f2bf5885cd,1476521011210; _ntes_nuid=7eced19b27ffae35dad3f8f2bf5885cd; usertrack=c+5+hlgB7TgnsAmACnXtAg==; Province=025; City=025; NTES_PASSPORT=6n9ihXhbWKPi8yAqG.i2kETSCRa.ug06Txh8EMrrRsliVQXFV_orx5HffqhQjuGHkNQrLOIRLLotGohL9s10wcYSPiQfI2wiPacKlJ3nYAXgM; P_INFO=hourui93@163.com|1476523293|1|study|11&12|jis&1476511733&mail163#jis&320100#10#0#0|151889&0|g37_client_check&mailsettings&mail163&study&blog|hourui93@163.com; _ga=GA1.2.1405085820.1476521280; JSESSIONID-WYYY=fb5288e1c5f667324f1636d020704cab2f27ee915622b114f89027cbf60c38be2af6b9cbef2223c1f2581e3502f11b86efd60891d6f61b6f783c0d55114f8269fa801df7352f5cc4c8259876e563a6bd0212b504a8997723a0593b21d5b3d9076d4fa38c098be68e3c5d36d342e4a8e40c1f73378cec0b5851bd8a628886edbdd23a7093%3A1476623819662; _iuqxldmzr_=25; __utma=94650624.1038096298.1476521011.1476610320.1476622020.10; __utmb=94650624.14.10.1476622020; __utmc=94650624; __utmz=94650624.1476521011.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            'DNT': '1',
            'Host': 'music.163.com',
            'Pragma': 'no-cache',
            'Referer': 'http://music.163.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }

    def page_parser(self, album_id, params):
        album_url = self.BASE_API_URL + str(album_id)
        r_ob = requests.get(album_url, headers=self.headers, params=params)
        base_soup = BeautifulSoup(r_ob.content, 'html.parser')
        base_body = base_soup.body
        return base_soup, base_body

    def get_music_name(self, strs):
        pattern = re.compile(r'>(.+)</b>')
        match = re.search(pattern, strs).group()
        return match.replace('<', '').replace('>', '')

    def save_music(self, album_id):
        params = {'id': album_id, 'limit': '200'}
        # Obatin the corresponding pages of albums

        # r = requests.get('http://music.163.com/album', headers=self.headers, params=params)

        # Parse the html page using BeautifulSoup
        # soup = BeautifulSoup(r.content.decode(), 'html.parser')

        soup, body = self.page_parser(album_id, params)
        # debug part
        # for ele in body:
        #     print ele
        # Obatain all musics in an album
        print soup
        # album_info = body.find('a', attrs={'class': 'f-brk'}).findall('')
        # musics = body.find('tr', attrs={'class': 'even'}).find_all('li')
        musics = body.find_all('tr', attrs={'class': 'even'})

        print musics

        for music in musics:
            print music
            music = music.find('a')
            music_id = music['href'].replace('/song?id=', '')
            # music_name = music.getText()
            music_name = self.get_music_name(music)
            # sql.insert_music(music_id, music_name, album_id)

    def get_hot_comments(self, song_id, threshold=100):
        """
        输入歌曲id，返回该歌曲的前threshold个热门评论。

        :param song_id: 歌曲id，string类型和int类型均可，例如35403523
        :param threshold: 前threshold个热门评论
        :return: 返回一个list，每个子元素也是list，其中第一项为评论内容，第二项为点赞数。
        例如： [[u'\u4e24\u5929\u524d \u9648\u5955\u8fc5\u5728\u58a8\u5c14\u672c\u5f00\u6f14\u5531\u4f1a \u5b89\u4e1c\u5c3c\u53d1\u5fae\u535a\u8bf4\u4ed6\u5728\u53f0\u4e0b\u542c\u7684\u611f\u6168\u4e07\u5206 \u5c31\u50cf\u505a\u4e86\u4e00\u573a\u68a6 \u4ed6\u7ec8\u4e8e\u5b8c\u6210\u4e86\u81ea\u5df1\u7684\u68a6 \u81ea\u5df1\u559c\u6b22\u7684\u6b4c\u624b\u4e3a\u4ed6\u7684\u4e66\u5531\u7684\u4e3b\u9898\u66f2 \u4f60\u6709\u68a6\u60f3\u4f60\u5c31\u8981\u634d\u536b\u5b83~', 64520],...]
        """

        ###
        url = self.BASE_URL + 'weapi/v1/resource/comments/R_SO_4_{}?csrf_token='.format(song_id)
        headers = {'Cookie': 'appver=1.5.0.75771;', 'Referer': 'http://music.163.com/song?id={}'.format(song_id)}

        text = json.dumps(TEXT)
        sec_key = create_secret_key(16)
        enc_text = aes_encrypt(aes_encrypt(text, NONCE), sec_key)
        enc_sec_key = rsa_encrypt(sec_key, PUBKEY, MODULUS)
        data = {'params': enc_text, 'encSecKey': enc_sec_key}
        req = requests.post(url, headers=headers, data=data)

        print req.content
        data = json.loads(req.content)['hotComments']

        res = []
        for item in data:
            res.append([item['content'], item['likedCount']])

        return res[:threshold]


if __name__ == '__main__':
    my_music = Music()
    album_ids = my_music.sql_obj.get_all_albums()
    for id_tuple in album_ids:
        print id_tuple
        id_int = int(id_tuple[0])
        if (id_int == 1):
            continue
        try:
            my_music.save_music(id_int)

        except Exception as e:
            # Print logs for debugging
            print(str(id_int) + ': ' + str(e))
            time.sleep(5)
