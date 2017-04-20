# coding: utf-8

import re
from bs4 import BeautifulSoup
import requests
import encrypt_func
from sql import sql

# Write a single thread crawler at first and output infomartion into a txt file
# Output format: | artist_id | artist_name | artist_info | maybe others ... |

class SpiderArtist(object):
    def __init__(self, file):
        self.base_url = 'http://music.163.com/artist?id='
        self.low_aid = 1875
        self.high_aid = 106275
        self.counter_id = self.low_aid
        self.file = file

        # Initiate list with '[]' and set with '{}'
        # start from artists with respect to music favour nature
        self.start_url = ['http://music.163.com/discover/artist/cat?id=1001', # 华语男歌手
                          'http://music.163.com/discover/artist/cat?id=1002', # 华语女歌手
                          'http://music.163.com/discover/artist/cat?id=1003', # 华语组合
                          'http://music.163.com/discover/artist/cat?id=2001', # 美国男歌手
                          'http://music.163.com/discover/artist/cat?id=2002', # 美国女歌手
                          'http://music.163.com/discover/artist/cat?id=2003', # 美国组合
                          'http://music.163.com/discover/artist/cat?id=6001', # 韩国男歌手
                          'http://music.163.com/discover/artist/cat?id=6002', # 韩国女歌手
                          'http://music.163.com/discover/artist/cat?id=6003', # 韩国组合
                          'http://music.163.com/discover/artist/cat?id=7001', # 日本男歌手
                          'http://music.163.com/discover/artist/cat?id=7002', # 日本女歌手
                          'http://music.163.com/discover/artist/cat?id=7003', # 日本组合
                          'http://music.163.com/discover/artist/cat?id=4001', # 其他男歌手
                          'http://music.163.com/discover/artist/cat?id=4002', # 其他女歌手
                          'http://music.163.com/discover/artist/cat?id=4003'  # 其他组合
                          ]

    def craw_artists(self):
        craw_url = self.base_url + str(self.counter_id)
        r = requests.get(craw_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        # raw_artists = base_body.find_all('a', attrs={'class': 'nm nm-icn f-thide s-fc0'})
        return soup

    def craw(self):
        soup = self.craw_artists()
        head = str(soup.head)
        result = re.findall(r'<title>(.+?) -', head)
        if len(result) < 1:
            # No correct info crawed
            print 'Nothing to craw in this page!\n'
            self.counter_id += 1
        else:
            name = result[0]
            self.save_artists(self.counter_id, str(name))

    def save_artists(self, id, name):
        self.file.write(str(id) + ', ')
        self.file.write(name)
        self.file.write('\n')
        self.counter_id += 1





if __name__ == '__main__':
    # Craw urls in start_url list in order with a simple implementation
    # Store all artist ids in artist_id.txt file for further crawling their homepage infos
    f = open('artist_info.txt', 'w+', buffering=100000)
    f.write('**********\n' + 'id, artist_name\n' + '**********\n')
    spider = SpiderArtist(f)

    while (spider.counter_id < spider.high_aid):
        print 'The %d artist id is to be crawed!\n' %(spider.counter_id)
        info = spider.craw()

    f.close()



    # for url in spider.start_url:
    #     url_append = url + '&initial=0'
    #     two_urls = [url, url_append]
        # for url in two_urls:
        #     # craw infos in start_url and record all artist ids
        #     # test_url = 'http://music.163.com/discover/artist/cat'
        #     artists_info = spider.craw_artists(url)
        #     for artist in artists_info:
        #         raw_artist_id = artist['href'].replace('/artist?id=', '').strip()
        #         artist_id = int(raw_artist_id)
        #         artist_name = artist['title'].replace(u'的音乐', '')
        #         count += 1
        #         # print 'all artists id, name: ', artist_id, artist_name
        #         try:
        #             # self.sql_obj.insert_artist(artist_id, artist_name)
        #             # artist is acii code, cannot turn into str form
        #             f.write(str(artist_id) + ', ')
        #             f.write(str(artist_name.encode('utf-8')))
        #             f.write('\n')
        #         except Exception as e:
        #             # Print logs
        #             print(e)
        #             continue
        #     f.write('-----------------------------------------------\n')
        #     print 'One round over with %d artists recorded\n', count
