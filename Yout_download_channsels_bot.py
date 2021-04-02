import sqlite3
from selenium import webdriver
import time
import random
import unicodedata
import re
from pytube import YouTube
options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome('chromedriver.exe', options=options)

# создание пустой базы данных
conn = sqlite3.connect('bazasearch_download.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS vidos(
   vidid INT,
   name TEXT,
   descr TEXT,
   prosm INT,
   pub TEXT,
   link TEXT PRIMARY KEY);
""")
conn.commit()

links = ['https://www.youtube.com/c/NickChernobaev/videos',]
def get_links(link_list):
    for link in link_list:
        driver.get(link)
        time.sleep(1)
        len_scroll = 3000
        for i in range(1, 14):
            driver.execute_script("window.scrollBy(0,{})".format(len_scroll))
            len_scroll += 6000
            time.sleep(1)
            print('прокрутка')
        for i in driver.find_elements_by_id('video-title'):
            vid_link = str(i.get_attribute('href'))
            vid_description = str(i.get_attribute('aria-label'))
            print(vid_link + '   ' + vid_description)
            try:
                author_date = str(vid_description.split('Автор:', 1)[1]).split(' ', 1)[1].rstrip()
            except:
                author_date = "author_date ошибка "
                print("author_date ошибка" + str(vid_link))
            stro = unicodedata.normalize('NFKD', author_date)
            prosm_text = str(re.findall(r"\w{0}\s{0}\d+\s*\d*\s*\d* просм", stro))
            prosm_int = re.findall(r'\d+', prosm_text)
            try:
                prosm_int = int(''.join(prosm_int))
            except:
                prosm_int = 0
                print('prosm_int исключение' + str(vid_link))

            vids = ('1', author_date, vid_description, prosm_int, '0', vid_link)
            print(vids)
            try:
                cur.execute("INSERT INTO vidos VALUES(?, ?, ?, ?, ?, ?);", vids)
                conn.commit()
            except sqlite3.IntegrityError as err:
                print(str(err) + 'в ссылке: ' + link)
    driver.close()

# сохраняем ссылки в базу данных
get_links(links)

# Скачивание по ссылкамм из базы, нужно сделать в виде функции и очистка базы в конце.

conn = sqlite3.connect('bazasearch_download.db')
cur = conn.cursor()
cur.execute("""SELECT link FROM vidos""")
vid_links = cur.fetchall()
for i in vid_links:
    yt = YouTube(i[0])
    yt.streams.get_by_itag(18).download()
    print(i[0])