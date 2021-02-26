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

def getChannelList(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    my_result = cur.execute("""SELECT link_chan FROM vidos
    """)
    link_set = set()
    for i in my_result:
        # print(i[0])
        link_set.add(i[0]+'/videos')
    conn.close()
    return link_set

print(getChannelList('bazasearch_invest.db'))

def get_vids():
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
    for link in getChannelList('bazasearch_invest.db'):
        driver.get(link)
        time.sleep(1)
        len_scroll = 300
        num1 = 0
        for i in range(1, 8):
            if num1 < 5:
                print(num1)
                num1+=1
                driver.execute_script("window.scrollBy(0,{})".format(len_scroll))
                len_scroll += 6000
                time.sleep(1)
                print('прокрутка')

                num = 0
                print('цикл while')
                for webobj in driver.find_elements_by_tag_name('ytd-video-renderer'):
                    if num < 5:
                        num += 1
                        print('цикл for')
                        print(num)
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

                        for b in webobj.find_elements_by_id('channel-name'):
                            for c in b.find_elements_by_tag_name('a'):
                                if c.text != '':
                                    # print(c.text)
                                    name_channel = c.text
                                    # print(c.get_attribute('href'))
                                    link_chan = c.get_attribute('href')

                        vids = ('1', author_date, name_channel, vid_description, prosm_int, '0', link_chan, vid_link)

                        vids = ('1', author_date, name_channel, vid_description, prosm_int, '0', link_chan, vid_link)
                        print(vids)
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
            else:
                break

    driver.close()

get_vids()

# "channel-name"

# <a class="yt-simple-endpoint style-scope yt-formatted-string" spellcheck="false" href="/channel/UCSJ9oPTyX_1UqUA-npmJ9eQ" dir="auto">Modern DIY</a>