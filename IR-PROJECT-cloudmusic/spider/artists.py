# coding: utf-8


# Get all the artists info from the base page: (url) http://music.163.com/discover/artist/cat/

import requests
from bs4 import BeautifulSoup
from sql import sql
import re

BASE_URL = 'http://music.163.com/discover/artist/cat'
# params = {'id': 4003, 'initial': 0} # what's the usage of such parameters?


class Artist(object):
    def __init__(self):
        self.sql_obj = sql.SQL()
        self.base_url = BASE_URL

    def page_parser(self):
        r = requests.get(self.base_url)
        base_soup = BeautifulSoup(r.content, 'html.parser')
        base_body = base_soup.body
        return base_body

    def save_artists(self):
        # Parse the html page
        # soup = BeautifulSoup(r.content.decode(), 'html.parser')
        body = self.page_parser()

        # hot_artists = body.find_all('a', attrs={'class': 'msk'})
        artists = body.find_all('a', attrs={'class': 'nm nm-icn f-thide s-fc0'})
        print artists

        # Add hot artists into artist table
        # for artist in hot_artists:
        #     artist_id = artist['href'].replace('/artist?id=', '').strip()
        #     artist_name = artist['title'].replace(u'的音乐', '')
        #     # artist_name = artist['title'].replace('\u7684\u97f3\u4e50', '')
        #     print 'hot_artists id, name: ', artist_id, artist_name  # simply for test correctness
        #     try:
        #         self.sql_obj.insert_artist(artist_id, artist_name)
        #     except Exception as e:
        #         # Print logs
        #         print e
        #         continue
        # Add other artist into artist table
        for artist in artists:
            raw_artist_id = artist['href'].replace('/artist?id=', '').strip()
            artist_id = int(raw_artist_id)
            artist_name = artist['title'].replace(u'的音乐', '')
            # artist_name = artist['title'].replace('?', '')
            print 'all artists id, name: ', artist_id, artist_name
            try:
                self.sql_obj.insert_artist(artist_id, artist_name)
            except Exception as e:
                # Print logs
                print(e)
                continue

if __name__ == '__main__':
    # Need to mdify according to the requirement
    my_artist = Artist()
    my_artist.save_artists()
    my_artist.sql_obj.close()




# SQL Instance
# sql_obj = sql.SQL()

# header not used in this program
# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate, sdch',
#     'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
#     'Cache-Control': 'no-cache',
#     'Connection': 'keep-alive',
#     'Cookie': '_ntes_nnid=7eced19b27ffae35dad3f8f2bf5885cd,1476521011210; _ntes_nuid=7eced19b27ffae35dad3f8f2bf5885cd; usertrack=c+5+hlgB7TgnsAmACnXtAg==; Province=025; City=025; NTES_PASSPORT=6n9ihXhbWKPi8yAqG.i2kETSCRa.ug06Txh8EMrrRsliVQXFV_orx5HffqhQjuGHkNQrLOIRLLotGohL9s10wcYSPiQfI2wiPacKlJ3nYAXgM; P_INFO=hourui93@163.com|1476523293|1|study|11&12|jis&1476511733&mail163#jis&320100#10#0#0|151889&0|g37_client_check&mailsettings&mail163&study&blog|hourui93@163.com; NTES_SESS=Fa2uk.YZsGoj59AgD6tRjTXGaJ8_1_4YvGfXUkS7C1NwtMe.tG1Vzr255TXM6yj2mKqTZzqFtoEKQrgewi9ZK60ylIqq5puaG6QIaNQ7EK5MTcRgHLOhqttDHfaI_vsBzB4bibfamzx1.fhlpqZh_FcnXUYQFw5F5KIBUmGJg7xdasvGf_EgfICWV; S_INFO=1476597594|1|0&80##|hourui93; NETEASE_AUTH_SOURCE=space; NETEASE_AUTH_USERNAME=hourui93; _ga=GA1.2.1405085820.1476521280; JSESSIONID-WYYY=cbd082d2ce2cffbcd5c085d8bf565a95aee3173ddbbb00bfa270950f93f1d8bb4cb55a56a4049fa8c828373f630c78f4a43d6c3d252c4c44f44b098a9434a7d8fc110670a6e1e9af992c78092936b1e19351435ecff76a181993780035547fa5241a5afb96e8c665182d0d5b911663281967d675ff2658015887a94b3ee1575fa1956a5a%3A1476607977016; _iuqxldmzr_=25; __utma=94650624.1038096298.1476521011.1476595468.1476606177.8; __utmb=94650624.20.10.1476606177; __utmc=94650624; __utmz=94650624.1476521011.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
#     'DNT': '1',
#     'Host': 'music.163.com',
#     'Pragma': 'no-cache',
#     'Referer': 'http://music.163.com/',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
# }

# BASE_URL is where we start to crawl the music info

# BASE_URL = 'http://music.163.com/discover/artist/cat'


# def save_artist(group_id, initial):
#     params = {'id': group_id, 'initial': initial}
#     r = requests.get(BASE_URL, params=params)
#
#     # Parse the html page
#     # soup = BeautifulSoup(r.content.decode(), 'html.parser')
#     soup = BeautifulSoup(r.content, 'html.parser')
#     body = soup.body
#
#     hot_artists = body.find_all('a', attrs={'class': 'msk'})
#     artists = body.find_all('a', attrs={'class': 'nm nm-icn f-thide s-fc0'})
#
#     print artists
#
#     for artist in hot_artists:
#         artist_id = artist['href'].replace('/artist?id=', '').strip()
#         artist_name = artist['title'].replace(u'的音乐', '')
#         # artist_name = artist['title'].replace('\u7684\u97f3\u4e50', '')
#
#         print 'hot_artists id, name: ', artist_id, artist_name # simply for test correctness
#
#         try:
#             sql_obj.insert_artist(artist_id, artist_name)
#         except Exception as e:
#             # Print logs
#             print e
#             sql_obj.cursor.execute("DELETE from artists",()) # at last this should be deleted
#             sql_obj.insert_artist(artist_id, artist_name)
#
#     for artist in artists:
#         artist_id = artist['href'].replace('/artist?id=', '').strip()
#         artist_name = artist['title'].replace(u'的音乐', '')
#         # artist_name = artist['title'].replace('?', '')
#
#         print 'all artists id, name: ', artist_id, artist_name
#
#         try:
#             sql_obj.insert_artist(artist_id, artist_name)
#         except Exception as e:
#             # Print logs
#             print(e)
#             continue


# gg = 4003
#
# save_artist(gg, 0)
# for i in range(65, 91):
#     save_artist(gg, i)
