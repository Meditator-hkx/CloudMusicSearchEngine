# coding:utf-8

# Use sqlite3 package to store the data in test.db

import sqlite3


class SQL(object):
    def __init__(self):
        self.connection = sqlite3.connect('cloudmusic.db')
        self.cursor = self.connection.cursor()
        self.connection.text_factory = str

    def insert_artist(self, artist_id, artist_name, artist_info=" "):
        sql_command = "INSERT INTO artists VALUES (?, ?, ?)"
        self.cursor.execute(sql_command, (artist_id, artist_name, artist_info))
        self.connection.commit()

    def insert_music(self, music_id, music_name, album_id, music_lyric = 'None', comment_number = 0):
        sql_command = "INSERT INTO musics VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(sql_command, (music_id, music_name, album_id, music_lyric, comment_number))
        self.connection.commit()

    def insert_album(self, album_id, album_name, artist_id, music_number=10):
        sql_command = "INSERT INTO albums VALUES (?, ?, ?, ?)"
        self.cursor.execute(sql_command, (album_id, album_name, artist_id, music_number))
        self.connection.commit()

    def insert_comments(self, music_id, comment_content, details):
        sql_command = "INSERT INTO comments VALUES (?, ?, ?)"
        self.cursor.execute(sql_command, (music_id, comment_content, details))
        self.connection.commit()

    def get_all_artists(self):
        sql_command = "SELECT ID FROM artists ORDER BY ID"
        self.cursor.execute(sql_command,())
        return self.cursor.fetchall()

    def get_all_musics(self):
        sql_command = "SELECT MUSIC_ID FROM musics ORDER BY MUSIC_ID"
        self.cursor.execute(sql_command)
        return self.cursor.fetchall()

    def get_all_albums(self):
        sql_command = "SELECT ALBUM_ID FROM albums ORDER BY ALBUM_ID"
        self.cursor.execute(sql_command,())
        return self.cursor.fetchall()

    def update_album(self, album_id, music_number):
        sql_command = "UPDATE albums SET MUSIC_NUMBER = ? WHERE ALBUM_ID = ?"
        self.cursor.execute(sql_command, (music_number, album_id))
        self.connection.commit()

    def close(self):
        self.connection.close()

# connection = sqlite3.connect('test.db')
# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='1234',
#                              db='test',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)


# # Save comments
# def insert_comments(music_id, comments, detail, con):
#     with con.cursor() as cursor:
#         sql = "INSERT INTO comments (MUSIC_ID, COMMENTS, DETAILS) VALUES (%s, %s, %s)"
#         cursor.execute(sql, (music_id, comments, detail))
#     con.commit()
#
#
# # 保存音乐
# def insert_music(music_id, music_name, album_id):
#     with connection.cursor() as cursor:
#         sql = "INSERT INTO musics (MUSIC_ID, MUSIC_NAME, ALBUM_ID) VALUES (%s, %s, %s)"
#         cursor.execute(sql, (music_id, music_name, album_id))
#     connection.commit()
#
#
# # 保存专辑
# def insert_album(album_id, artist_id):
#     with connection.cursor() as cursor:
#         sql = "INSERT INTO albums (ALBUM_ID, ARTIST_ID) VALUES (%s, %s)"
#         cursor.execute(sql, (album_id, artist_id))
#     connection.commit()
#
#
# # 保存歌手
# def insert_artist(artist_id, artist_name):
#     with connection.cursor() as cursor:
#         sql = "INSERT INTO artists (ARTIST_ID, ARTIST_NAME) VALUES (%s, %s)"
#         cursor.execute(sql, (artist_id, artist_name))
#     connection.commit()
#
#
# # 获取所有歌手的 ID
# def get_all_artist():
#     with connection.cursor() as cursor:
#         sql = "SELECT `ARTIST_ID` FROM `artists` ORDER BY ARTIST_ID"
#         cursor.execute(sql, ())
#         return cursor.fetchall()
#
#
# # 获取所有专辑的 ID
# def get_all_album():
#     with connection.cursor() as cursor:
#         sql = "SELECT `ALBUM_ID` FROM `albums` ORDER BY ALBUM_ID"
#         cursor.execute(sql, ())
#         return cursor.fetchall()
#
#
# # 获取所有音乐的 ID
# def get_all_music():
#     with connection.cursor() as cursor:
#         sql = "SELECT `MUSIC_ID` FROM `musics` ORDER BY MUSIC_ID"
#         cursor.execute(sql, ())
#         return cursor.fetchall()
#
#
# # 获取前一半音乐的 ID
# def get_before_music():
#     with connection.cursor() as cursor:
#         sql = "SELECT `MUSIC_ID` FROM `musics` ORDER BY MUSIC_ID LIMIT 0, 800000"
#         cursor.execute(sql, ())
#         return cursor.fetchall()
#
#
# # 获取后一半音乐的 ID
# def get_after_music():
#     with connection.cursor() as cursor:
#         sql = "SELECT `MUSIC_ID` FROM `musics` ORDER BY MUSIC_ID LIMIT 800000, 1197429"
#         cursor.execute(sql, ())
#         return cursor.fetchall()
#
#
# def dis_connect():
#     connection.close()
