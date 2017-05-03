# encoding: utf-8

from userapi import UserSearch as us
from Utilization.splitter_utilizer import split
from indexer.IndexExtractor import get_url_lists as glst
# get user search words
search_words = us.get_search_info()
# split words of search words
terms = split(search_words)

# for each term, find where the corresponding page urls resides
total_list = []
for term in terms:
    # Call function in index database
    return_list = glst(term)
    if not return_list:
        continue
    total_list.append(return_list)
    pass

# Record the url weight based on access times
weight_list = dict()
for lst in total_list:
    for ele in lst:
        if weight_list.has_key(ele):
            weight_list[ele] += 1
        else:
            weight_list[ele] = 1

# Sort the urls based on the url weights
sorted_list = [v[0] for v in sorted(weight_list.items(), key = lambda(k,v):(v,k), reverse=True)]
# print returned results
for ele in sorted_list:
    print ele
