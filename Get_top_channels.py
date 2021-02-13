import sqlite3
# get top channels
def get_top_channels():
    conn = sqlite3.connect('bazasearch.db')
    cur = conn.cursor()
    my_result = cur.execute("""SELECT * FROM vidos
    ORDER BY prosm DESC
    """)

    for i in my_result:
        print(i[2])
        print(i[1])
        print(i[3])
        print(i[5])

    return my_result

get_top_channels()