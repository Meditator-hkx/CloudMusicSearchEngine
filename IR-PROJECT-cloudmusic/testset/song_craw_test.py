import requests
import urllib2

test_url = 'http://music.163.com/#/song?id=418603077'



ret = requests.post(test_url)
