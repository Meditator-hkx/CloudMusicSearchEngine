# encoding: utf-8
import jieba


def split(sentence):
    split_list = jieba.lcut_for_search(sentence)
    return split_list