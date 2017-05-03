# encoding: utf-8


def get_search_info():
    raw_search_words = raw_input("Please input any keywords you want to search: ")

    if type(raw_search_words) != type("hello"):
        print "Error!Please input your keywords again!\n"
        raw_search_words = get_search_info()
    return raw_search_words




