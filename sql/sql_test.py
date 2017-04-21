import sqlite3
import sql

obj = sql.SQL()

obj.insert_artist(2, 'xyz', '')

# con = sqlite3.connect('test.db')
# cursor = con.cursor()
#
# cursor.execute("INSERT INTO artists VALUES ('100', 'JayChou')")
# cursor.execute("INSERT INTO artists VALUES ('101', 'Yixun Chen')")
#
# con.commit()
# con.close()