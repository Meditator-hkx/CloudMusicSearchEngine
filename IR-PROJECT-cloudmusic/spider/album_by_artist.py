# coding:utf-8


# Obtain all the album ids according to the artist ids

import re
import requests
from bs4 import BeautifulSoup
from sql import sql


# class Doctor(object)
# class DiseaseArea(object)
# class


class Album(object):
    def __init__(self):
        self.sql_obj = sql.SQL()
        self.BASE_ARTIST_URL = 'http://music.163.com/artist/album?id='
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

    def page_parser(self, artist_id):
        params = {'id': artist_id, 'limit': '200'}
        album_url = self.BASE_ARTIST_URL + str(artist_id)
        print album_url
        # r_ob = requests.get(album_url, headers=self.headers,params=params)
        r_ob = requests.get(album_url)
        base_soup = BeautifulSoup(r_ob.content, 'html.parser')
        base_body = base_soup.body
        return base_body

    def get_album_name(self, strs):
        pattern = re.compile(r'>(.+)<')
        match = re.search(pattern, strs).group()
        return match.replace('<', '').replace('>','')

    def save_albums(self, artist_id):
        # params = {'id': artist_id, 'limit': '200'}
        # Parse the html page
        # soup = BeautifulSoup(r.content.decode(), 'html.parser')
        # body = soup.body
        body = self.page_parser(artist_id)
        albums = body.find_all('a', attrs={'class': 'tit s-fc0'})  # Obtain all the albums
        print albums

        for album in albums:
            print str(album) # debug
            raw_album_id = album['href'].replace('/album?id=', '')
            album_id = int(raw_album_id)
            album_name = self.get_album_name(str(album))
            try:
                self.sql_obj.insert_album(album_id, album_name, int(artist_id))
            except Exception as e:
                # Print logs
                print(e)
                continue


if __name__ == '__main__':
    # artists = sql.get_all_artist()
    my_album = Album()
    artist_ids = my_album.sql_obj.get_all_artists()

    print artist_ids

    for id_tuple in artist_ids:
        id_int = int(id_tuple[0])
        try:
            my_album.save_albums(id_int)
            # my_album.save_albums(i['ARTIST_ID'])
            # print(i)
        except Exception as e:
            print(str(id_int) + ': ' + str(e))
            # time.sleep(5)
    my_album.sql_obj.close()