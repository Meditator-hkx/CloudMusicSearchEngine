# coding:utf-8

# Use sqlite3 package to store the data in

import sqlite3


class SQL(object):
    def __init__(self):
        self.connection = sqlite3.connect('indexer.db')
        self.cursor = self.connection.cursor()
        self.connection.text_factory = str

    def get_url_list(self, term):
        sql_command = "SELECT URL_SET FROM indexes WHERE TERM = ?"
        self.cursor.execute(sql_command, (term, ))
        self.connection.commit()
        return self.cursor.fetchall()
