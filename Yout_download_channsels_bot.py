import sqlite3
from selenium import webdriver
import time
import random
import unicodedata
import re
from pytube import YouTube


#Модуль бота
import telebot
from config import api_key


bot = telebot.TeleBot(api_key)

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('баланс', 'банк')
print('start')
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text.lower() == 'Go':
        bot.send_message(message.from_user.id, 'начинаем эффективную работу', reply_markup=keyboard1)
        print('Баланс')
    elif message.text.lower().split()[0].isdigit() == True:
        bot.send_message(message.from_user.id, 'задание '+ message.text, reply_markup=keyboard1)
        print('задание')

    else:
        print(message.text)
        bot.send_message(message.from_user.id, 'Минуты пробел задача', reply_markup=keyboard1)

bot.polling(none_stop=True, interval=0)


#МОдуль Скачивания
def channel_download_module(chan_for_download, number_of_downloads):
    # создание пустой базы данных
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome('chromedriver.exe', options=options)

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

    # links = ['https://www.youtube.com/c/NickChernobaev/videos',]

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
    get_links(chan_for_download)

    # Скачивание по ссылкамм из базы, нужно сделать в виде функции и очистка базы в конце.

    conn = sqlite3.connect('bazasearch_download.db')
    cur = conn.cursor()
    cur.execute("""SELECT link FROM vidos""")
    vid_links = cur.fetchall()
    for i in vid_links:
        yt = YouTube(i[0])
        yt.streams.get_by_itag(18).download()
        print(i[0])
    # нужно добавить очистку базы данных
    return 'просто текст результат функциии channel_download_module'