# coding:utf-8
import re
import numpy

from spider import album_by_artist

al = album_by_artist.Album()

rd = numpy.random.randint(0,10)

print rd

test_content = '<a class="tit s-fc0" href="/album?id=34555075">The Best of A-Do阿杜‧诚意‧跨厂牌超级精...</a>'
print test_content

# match = al.get_album_name(test_content)
#
# pattern = re.compile(r'>(.+)<')

match = re.search(r'>(.+)<', test_content)
n =  match.group()
n1 = n.replace('>','')
n2 = n1.replace('<','')
print n2

# Only this way can obtain the unicode expression of

