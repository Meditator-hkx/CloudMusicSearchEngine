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