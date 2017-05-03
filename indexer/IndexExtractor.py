# encoding: utf-8

from sql import sql_index


class Extractor(object):
    def __init__(self):
        self.sql_obj = sql_index.SQL()

    def get_url_list(self, term):
        raw_return_info = self.sql_obj.get_url_list(term)
        # deal with raw info and transform it into a regular list
        return raw_return_string


def get_url_lists(term):

    return []
    pass