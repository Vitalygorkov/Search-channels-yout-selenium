import sqlite3
from selenium import webdriver
import time
import random
import unicodedata
import re
options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)


driver = webdriver.Chrome('chromedriver.exe', options=options)

conn = sqlite3.connect('bazasearch.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS vidos(
   vidid INT,
   name TEXT,
   descr TEXT,
   prosm INT,
   pub TEXT,
   link_chan TEXT,
   link TEXT PRIMARY KEY);
""")
conn.commit()

link_list = ['https://www.youtube.com/results?search_query=handmade',
             'https://www.youtube.com/results?search_query=diy',
             'https://www.youtube.com/results?search_query=ideas',
             'https://www.youtube.com/results?search_query=how+to+make',
             'https://www.youtube.com/results?search_query=как+сделать',
             'https://www.youtube.com/results?search_query=своими+руками']
link_list_test = ['https://www.youtube.com/results?search_query=handmade',]
def get_vids():
    for link in link_list_test:
        driver.get(link)
        time.sleep(1)
        len_scroll = 3000
        # for i in range(1, 80):
        #     driver.execute_script("window.scrollBy(0,{})".format(len_scroll))
        #     len_scroll += 6000
        #     time.sleep(1)
        #     print('прокрутка')
        num = 0

        print('цикл while')
        for i in driver.find_element_by_name("yt-simple-endpoint style-scope yt-formatted-string"):
            if num < 5:
                num += 1
                print(i.text)
                print(i.get_attribute('href'))

                # print('цикл for')
                # print(num)
                # vid_link = str(i.get_attribute('href'))
                # vid_description = str(i.get_attribute('aria-label'))
                # print(vid_link + '   ' + vid_description)
                # try:
                #     author_date = str(vid_description.split('Автор:', 1)[1]).split(' ', 1)[1].rstrip()
                # except:
                #     author_date = "author_date ошибка "
                #     print("author_date ошибка" + str(vid_link))
                # stro = unicodedata.normalize('NFKD', author_date)
                # prosm_text = str(re.findall(r"\w{0}\s{0}\d+\s*\d*\s*\d* просм", stro))
                # prosm_int = re.findall(r'\d+', prosm_text)
                # try:
                #     prosm_int = int(''.join(prosm_int))
                # except:
                #     prosm_int = 0
                #     print('prosm_int исключение' + str(vid_link))
                #
                #
                # link_chan = 'link_chan'
                #
                # vids = ('1', author_date, vid_description, prosm_int, '0', link_chan, vid_link)
                # print(vids)
                # try:
                #     cur.execute("INSERT INTO vidos VALUES(?, ?, ?, ?, ?, ?, ?);", vids)
                #     conn.commit()
                # except sqlite3.IntegrityError as err:
                #     print(str(err) + 'в ссылке: ' + link)

            else:
                break


    driver.close()

get_vids()

# "channel-name"

# <a class="yt-simple-endpoint style-scope yt-formatted-string" spellcheck="false" href="/channel/UCSJ9oPTyX_1UqUA-npmJ9eQ" dir="auto">Modern DIY</a>