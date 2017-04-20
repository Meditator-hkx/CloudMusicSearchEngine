# Test if the SQL commands in python work well
# INSET test

import sqlite3

con = sqlite3.connect('test.db')
cursor = con.cursor()

cursor.execute("INSERT INTO artists VALUES ('100', 'JayChou', ' ')")
cursor.execute("INSERT INTO artists VALUES ('101', 'Yixun Chen', ' ')")

con.commit()
con.close()