# encoding: utf-8

from sql import sql_index

obj = sql_index.SQL()

lst = obj.get_url_list(r'周杰伦')

# deal with returned

lst = list(lst[0])[0]

lst = lst.split(',')

for ele in lst:
    print ele.strip(' ')
