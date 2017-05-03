# coding:utf-8

"""
Craw all comments info based on the music id obtained in CrawMusic.py
Update informantion for TABLE musics with 
"""

import time
import numpy as np
import requests

from sql import sql_craw
import json
from Utilization import encrypt_func as enf

BASE_URL = 'http://music.163.com/'
COMMENT_THRESHOLD = 10
_session = requests.Session()


class Comment(object):
    def __init__(self):
        self.headers = {
            'Host': 'music.163.com',
            'Connection': 'keep-alive',
            'Content-Length': '484',
            'Cache-Control': 'max-age=0',
            'Origin': 'http://music.163.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'DNT': '1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'Cookie': 'JSESSIONID-WYYY=b66d89ed74ae9e94ead89b16e475556e763dd34f95e6ca357d06830a210abc7b685e82318b9d1d5b52ac4f4b9a55024c7a34024fddaee852404ed410933db994dcc0e398f61e670bfeea81105cbe098294e39ac566e1d5aa7232df741870ba1fe96e5cede8372ca587275d35c1a5d1b23a11e274a4c249afba03e20fa2dafb7a16eebdf6%3A1476373826753; _iuqxldmzr_=25; _ntes_nnid=7fa73e96706f26f3ada99abba6c4a6b2,1476372027128; _ntes_nuid=7fa73e96706f26f3ada99abba6c4a6b2; __utma=94650624.748605760.1476372027.1476372027.1476372027.1; __utmb=94650624.4.10.1476372027; __utmc=94650624; __utmz=94650624.1476372027.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        }
        self.params = {
            'csrf_token': ''
        }
        self.data = {
            'params': 'Ak2s0LoP1GRJYqE3XxJUZVYK9uPEXSTttmAS+8uVLnYRoUt/Xgqdrt/13nr6OYhi75QSTlQ9FcZaWElIwE+oz9qXAu87t2DHj6Auu+2yBJDr+arG+irBbjIvKJGfjgBac+kSm2ePwf4rfuHSKVgQu1cYMdqFVnB+ojBsWopHcexbvLylDIMPulPljAWK6MR8',
            'encSecKey': '8c85d1b6f53bfebaf5258d171f3526c06980cbcaf490d759eac82145ee27198297c152dd95e7ea0f08cfb7281588cdab305946e01b9d84f0b49700f9c2eb6eeced8624b16ce378bccd24341b1b5ad3d84ebd707dbbd18a4f01c2a007cd47de32f28ca395c9715afa134ed9ee321caa7f28ec82b94307d75144f6b5b134a9ce1a'
        }
        self.sql_obj = sql_craw.SQL()

        # self.proxies = {'http': 'http://127.0.0.1:10800'}

    def craw(self, music_id):
        hot_comments = self.get_hot_comments(music_id) # Return only comment number now ...
        print hot_comments, music_id
        comment_number = hot_comments
        try:
            comment_number = int(comment_number)
            self.sql_obj.update_music(music_id, comment_number)
        except Exception as e:
            print e
            self.sql_obj.update_music(music_id, 0)
            pass
        # for item in hot_comments:
        #     try:
        #         comment = item[0]
        #         support = item[1]
        #         comment_obj.sql_obj.insert_comments(music_id, comment, support)
        #     except Exception as e:
        #         print e, "Error when inserting data to database"
            # print comment, support

    def get_hot_comments(self, music_id, threshold=COMMENT_THRESHOLD):
        """
        输入歌曲id，返回该歌曲的前threshold个热门评论。

        :param song_id: 歌曲id，string类型和int类型均可，例如35403523
        :param threshold: 前threshold个热门评论
        :return: 返回一个list，每个子元素也是list，其中第一项为评论内容，第二项为点赞数。
        例如： [[u'\u4e24\u5929\u524d \u9648\u5955\u8fc5\u5728\u58a8\u5c14\u672c\u5f00\u6f14\u5531\u4f1a \u5b89\u4e1c\u5c3c\u53d1\u5fae\u535a\u8bf4\u4ed6\u5728\u53f0\u4e0b\u542c\u7684\u611f\u6168\u4e07\u5206 \u5c31\u50cf\u505a\u4e86\u4e00\u573a\u68a6 \u4ed6\u7ec8\u4e8e\u5b8c\u6210\u4e86\u81ea\u5df1\u7684\u68a6 \u81ea\u5df1\u559c\u6b22\u7684\u6b4c\u624b\u4e3a\u4ed6\u7684\u4e66\u5531\u7684\u4e3b\u9898\u66f2 \u4f60\u6709\u68a6\u60f3\u4f60\u5c31\u8981\u634d\u536b\u5b83~', 64520],...]
        """
        url = BASE_URL + 'weapi/v1/resource/comments/R_SO_4_{}?csrf_token='.format(music_id)
        headers = {'Cookie': 'appver=1.5.0.75771;', 'Referer': 'http://music.163.com/song?id={}'.format(music_id)}

        text = json.dumps(enf.TEXT)
        sec_key = enf.create_secret_key(16)
        enc_text = enf.aes_encrypt(enf.aes_encrypt(text, enf.NONCE), sec_key)
        enc_sec_key = enf.rsa_encrypt(sec_key, enf.PUBKEY, enf.MODULUS)
        data = {'params': enc_text, 'encSecKey': enc_sec_key}
        req = requests.post(url, headers=headers, data=data)
        try:
            comment_number = json.loads(req.content)['total']
            # data = json.loads(req.content)['hotComments']
            # res = []
            # for item in data:
            #     res.append([item['content'], item['likedCount']])
            # print len(res)
            return comment_number      #, res[:threshold] # return total comment number and hot comments (limited by THRESHOLD)
        except Exception as e:
            print e
            return []

if __name__ == '__main__':
    comment_obj = Comment()
    musics = comment_obj.sql_obj.get_all_musics()
    sleep_flag = 0
    for music_id in musics:
        music_id = int(music_id[0])
        if music_id < 164840: # Stopped at music id 1868421
            continue
        print 'Crawing comment info for music with id %d' % music_id
        comment_obj.craw(music_id)
        # When every 100 musics' information is crawed, sleep for random seconds in (0, 10)
        sleep_flag += 1
        if sleep_flag % 100 == 0:
            print 'Sleep random seconds before next 100 music comments crawing\n'
            time.sleep(np.random.randint(0, 10))
    comment_obj.sql_obj.close()