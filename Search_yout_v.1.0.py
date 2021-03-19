import sqlite3
from selenium import webdriver
import time
import random
import unicodedata
import re
import datetime
options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)


driver = webdriver.Chrome('chromedriver.exe', options=options)

conn = sqlite3.connect('bazasearch.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS vidos(
   vidid INT,
   name TEXT,
   name_channel TEXT,
   descr TEXT,
   prosm TEXT,
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
link_list_invest = ['https://www.youtube.com/results?search_query=инвестиции',
                    'https://www.youtube.com/results?search_query=доход',
                    'https://www.youtube.com/results?search_query=заработок',]
link_list_invest2 = ['https://www.youtube.com/results?search_query=источник дохода',
                    'https://www.youtube.com/results?search_query=пассивный доход',
                    'https://www.youtube.com/results?search_query=доходность',]
linnk = ['https://www.youtube.com/channel/UCeYDB1gVQXf4PDfxn5jV9dw/videos', 'https://www.youtube.com/channel/UCQUTeCBc0n3WB_ZPEeA4zTQ/videos']

random.shuffle(link_list)
random.shuffle(link_list)
# Функция добавления вдосов из поиска по списку ключевых слов
def get_vids():
    for link in link_list_invest2:
        driver.get(link)
        time.sleep(1)
        len_scroll = 3000
        for i in range(1, 90):
            driver.execute_script("window.scrollBy(0,{})".format(len_scroll))
            len_scroll += 6000
            time.sleep(1)
            print('прокрутка')
        num = 0

        # print('цикл while')
        for webobj in driver.find_elements_by_tag_name('ytd-video-renderer'):
            if num < 5:
                # Вводим Num+= 0 если нужно снять ограничение
                num += 0
                # print('цикл for')
                # print(num)
                # print(webobj)
                # print(webobj.text)
                # print(str(webobj.get_attribute('href')))
                # print(str(webobj.get_attribute('aria-label')))
                # print(webobj.find_elements_by_id('video-title'))
                name_channel = ''
                link_chan = ''
                for i in webobj.find_elements_by_id('video-title'):
                    # print('ссылка на видео ' + str(i.get_attribute('href')))
                    vid_link = str(i.get_attribute('href'))
                    vid_description = str(i.get_attribute('aria-label'))
                    # print(vid_link + '   ' + vid_description)
                    try:
                        author_date = str(vid_description.split('Автор:', 1)[1]).split(' ', 1)[1].rstrip()
                    except:
                        author_date = "author_date ошибка "
                        # print("author_date ошибка" + str(vid_link))
                    stro = unicodedata.normalize('NFKD', author_date)
                    prosm_text = str(re.findall(r"\w{0}\s{0}\d+\s*\d*\s*\d* просм", stro))
                    prosm_int = re.findall(r'\d+', prosm_text)
                    try:
                        prosm_int = int(''.join(prosm_int))
                    except:
                        prosm_int = 0
                        print('prosm_int исключение' + str(vid_link))
                    prosm_list = str(datetime.date.today()) + ':' + str(prosm_int) + ','
                for b in webobj.find_elements_by_id('channel-name'):
                    for c in b.find_elements_by_tag_name('a'):
                        if c.text != '':
                            # print(c.text)
                            name_channel = c.text
                            # print(c.get_attribute('href'))
                            link_chan = c.get_attribute('href')

                vids = ('1', author_date, name_channel, vid_description, prosm_list, '0', link_chan, vid_link)
                # print(vids)
                try:
                    cur.execute("INSERT INTO vidos VALUES(?, ?, ?, ?, ?, ?, ?, ?);", vids)
                    conn.commit()
                except sqlite3.IntegrityError as err:
                    print(str(err) + 'в ссылке: ' + vid_link)
                    my_result = cur.execute("SELECT * FROM vidos WHERE link=?", (link,))
                    print(str(my_result) + 'это принт')
                    # cur.execute("REPLACE INTO vidos VALUES(?, ?, ?, ?, ?, ?, ?, ?);", vids)
            else:
                break


    driver.close()
# Функция добавления вдосов из поиска по списку ключевых слов
get_vids()

# Функция получения списка каналов из базы
def getChannelSet(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    my_result = cur.execute("""SELECT link_chan, name_channel FROM vidos
    """)
    result_set = set()
    for video in my_result:
        result_set.add(video)
    # conn.close()
    return result_set

# Сканируем каналы из базы
def get_vid3():
    for link in getChannelSet('bazasearch.db'):
        print(link[0]+'/videos') # link
        print(link[1])  # name
        driver.get(link[0]+'/videos')
        time.sleep(1)
        len_scroll = 3000
        for i in range(1, 9):
            driver.execute_script("window.scrollBy(0,{})".format(len_scroll))
            len_scroll += 6000
            time.sleep(1)
            print('прокрутка')
        for i in driver.find_elements_by_id('video-title'):
            # print('ссылка на видео ' + str(i.get_attribute('href')))
            vid_link = str(i.get_attribute('href'))
            vid_description = str(i.get_attribute('aria-label'))
            # print(vid_link + '   ' + vid_description)
            try:
                author_date = str(vid_description.split('Автор:', 1)[1]).split(' ', 1)[1].rstrip()
            except:
                author_date = "author_date ошибка "
                # print("author_date ошибка" + str(vid_link))
            stro = unicodedata.normalize('NFKD', author_date)
            prosm_text = str(re.findall(r"\w{0}\s{0}\d+\s*\d*\s*\d* просм", stro))
            prosm_int = re.findall(r'\d+', prosm_text)
            try:
                prosm_int = int(''.join(prosm_int))
            except:
                prosm_int = 0
                print('prosm_int исключение' + str(vid_link))
            prosm_list = str(datetime.date.today()) + ':' + str(prosm_int) + ','
            name_channel = link[1]
            link_chan = link[0]
            # for b in driver.find_elements_by_id('channel-name'):
            #     for c in b.find_elements_by_tag_name('a'):
            #         if c.text != '':
            #             # print(c.text)
            #             name_channel = c.text
            #             # print(c.get_attribute('href'))
            #             link_chan = c.get_attribute('href')

            # vids = ('1', author_date, name_channel, vid_description, prosm_int, '0', link_chan, vid_link)

            vids = ('1', author_date, name_channel, vid_description, prosm_list, '0', link_chan, vid_link)
            # print(vids)
            try:
                cur.execute("INSERT INTO vidos VALUES(?, ?, ?, ?, ?, ?, ?, ?);", vids)
                conn.commit()
            except sqlite3.IntegrityError as err:
                print(str(err) + 'в ссылке: ' + vid_link)
                my_result = cur.execute("SELECT * FROM vidos WHERE link=?", (vid_link,))
                print(str(my_result) + 'это принт')
                # print(my_result.fetchall())
                # print(my_result.fetchall())
                last_prosm = ''
                for i in my_result:
                    print(i[4])
                    last_prosm += i[4]
                new_prosm = last_prosm + prosm_list
                # print(last_prosm + 'это строка просмторов')
                vids2 = ('1', author_date, name_channel, vid_description, new_prosm, '0', link_chan, vid_link)
                cur.execute("REPLACE INTO vidos VALUES(?, ?, ?, ?, ?, ?, ?, ?);", vids2)
                conn.commit()
# Сканируем каналы из базы
# get_vid3()

# Сканируем каналы из базы
