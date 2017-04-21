# coding: utf-8

import re
from bs4 import BeautifulSoup
import requests
import threading
import encrypt_func
from sql import sql
import time

# Write a single thread crawler at first and output infomartion into a txt file
# Output format: | artist_id | artist_name | artist_info | maybe others ... |


class SpiderArtist(object):
    def __init__(self, thread_number = 10):
        self.base_url = 'http://music.163.com/artist?id='
        # self.low_aid = 1875
        # self.low_aid = 2916
        self.low_aid = 6693
        self.high_aid = 106275
        self.counter_id = self.low_aid
        self.thread_number = thread_number
        # self.file = f
        self.sql_obj = sql.SQL()
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

        # Initiate list with '[]' and set with '{}'
        # start from artists with respect to music favour nature
        # self.start_url = ['http://music.163.com/discover/artist/cat?id=1001', # 华语男歌手
        #                   'http://music.163.com/discover/artist/cat?id=1002', # 华语女歌手
        #                   'http://music.163.com/discover/artist/cat?id=1003', # 华语组合
        #                   'http://music.163.com/discover/artist/cat?id=2001', # 美国男歌手
        #                   'http://music.163.com/discover/artist/cat?id=2002', # 美国女歌手
        #                   'http://music.163.com/discover/artist/cat?id=2003', # 美国组合
        #                   'http://music.163.com/discover/artist/cat?id=6001', # 韩国男歌手
        #                   'http://music.163.com/discover/artist/cat?id=6002', # 韩国女歌手
        #                   'http://music.163.com/discover/artist/cat?id=6003', # 韩国组合
        #                   'http://music.163.com/discover/artist/cat?id=7001', # 日本男歌手
        #                   'http://music.163.com/discover/artist/cat?id=7002', # 日本女歌手
        #                   'http://music.163.com/discover/artist/cat?id=7003', # 日本组合
        #                   'http://music.163.com/discover/artist/cat?id=4001', # 其他男歌手
        #                   'http://music.163.com/discover/artist/cat?id=4002', # 其他女歌手
        #                   'http://music.163.com/discover/artist/cat?id=4003'  # 其他组合
        #                   ]

    def craw_artists(self):
        craw_url = self.base_url + str(self.counter_id)
        params = {'id': 4003, 'initial': 0}
        r = requests.get(self.base_url,params)
        soup = BeautifulSoup(r.content, 'html.parser')
        # raw_artists = base_body.find_all('a', attrs={'class': 'nm nm-icn f-thide s-fc0'}
        body = soup.body
        name_result = re.findall(r'<h2 class="sname f-thide sname-max".+id="artist-name" title=.+>(.+?)</h2>', str(body))
        try:
            name = name_result[0]
            self.save_artists(self.counter_id, str(name))
        except Exception as e:
            print e
        #     # self.counter_id += 1

    def save_artists(self, id, name):
        # Write to txt file
        # self.file.write(str(id) + ', ')
        # self.file.write(name)
        # self.file.write('\n')
        # Write to sqlite db
        self.sql_obj.insert_artist(id, name)



# class MyThread(threading.Thread):
#     def __init__(self, id, artist):
#         threading.Thread.__init__(self)
#         self.thread_id = id
#         self.name = 'thread-' + str(id)
#         self.artist = artist
#         self.counter_id = 0
#         self.return_set = []
#         self.sql_obj = sql.SQL()
#
#     def run(self):
#         print 'Starting: ' + self.name
#
#         while self.artist.counter_id < self.artist.high_aid:
#             # Acquire lock
#             thread_lock.acquire()
#             # Run craw program in artist instance
#             # print_time(self.name, self.counter, self.artist)
#             print 'thread %s running to craw the %d artist page ...\n' % (self.name, self.artist.counter_id)
#             artist_info = self.artist.craw_artists()
#             self.save_artist(artist_info)
#             self.artist.counter_id += 1
#             # Release lock
#             thread_lock.release()
#
#     def save_artist(self, artist_info):
#         if len(artist_info) > 0:
#             self.sql_obj.insert_artist(artist_info[0], artist_info[1])
#         else:
#             pass

if __name__ == '__main__':
    # Craw urls in start_url list in order with a simple implementation
    # Store all artist ids in artist_id.txt file for further crawling their homepage infos
    # f = open('artist_info.txt', 'w+', buffering=100)
    # f.write('**********\n' + 'id, artist_name\n' + '**********\n')
    spider = SpiderArtist()
    while spider.counter_id < spider.high_aid:
        print 'Currently crawing the %d artist pages ...' % spider.counter_id
        spider.craw_artists()
        spider.counter_id += 1
        if spider.counter_id % 100 == 0:
            time.sleep(10)


    # thread_lock = threading.Lock()
    # threads = []
    # # Create 10 theads to craw in parallel except that the counter_id should be accessed with a lock
    # for i in range(spider.thread_number):
    #     # Create new threads
    #     new_thread = MyThread(i, spider)
    #     threads.append(new_thread)
    #
    # # Start run new threads
    # for t in threads:
    #     t.start()
    #
    # # Wait for all threads to finish their jobs
    # for t in threads:
    #     t.join()

    # f.close()
