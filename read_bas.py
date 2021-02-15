import sqlite3

conn = sqlite3.connect('bazasearch_invest.db')
cur = conn.cursor()

my_result = cur.execute("""SELECT * FROM vidos
""")
# get top channels
for i in my_result:
    print(i[2])
    print(i[3])
    print(i[5])