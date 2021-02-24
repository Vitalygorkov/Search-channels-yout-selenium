import sqlite3

conn = sqlite3.connect('bazasearch_invest.db')
cur = conn.cursor()

my_result = cur.execute("""SELECT * FROM vidos
""")
# get top channels
def PrintResults():
    nums = 0
    for i in my_result:
        print(i[2])
        print(i[3])
        print(i[5])
        print(nums)
        nums+=1

PrintResults()

def FindBase(key):
    conn = sqlite3.connect('bazasearch_invest.db')
    cur = conn.cursor()

    my_result = cur.execute("""SELECT * FROM vidos WHERE 
    """)