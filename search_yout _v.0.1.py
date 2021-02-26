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
   name_channel TEXT,
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
link_list_invest = ['https://www.youtube.com/results?search_query=инвестиции',
                    'https://www.youtube.com/results?search_query=доход',
                    'https://www.youtube.com/results?search_query=заработок',]

random.shuffle(link_list)
def get_vids():
    for link in link_list_test:
        driver.get(link)
        time.sleep(1)
        len_scroll = 3000
        # for i in range(1, 90):
        #     driver.execute_script("window.scrollBy(0,{})".format(len_scroll))
        #     len_scroll += 6000
        #     time.sleep(1)
        #     print('прокрутка')
        num = 0

        # print('цикл while')
        for webobj in driver.find_elements_by_tag_name('ytd-video-renderer'):
            if num < 5:
                num += 1
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

                for b in webobj.find_elements_by_id('channel-name'):
                    for c in b.find_elements_by_tag_name('a'):
                        if c.text != '':
                            # print(c.text)
                            name_channel = c.text
                            # print(c.get_attribute('href'))
                            link_chan = c.get_attribute('href')

                vids = ('1', author_date, name_channel, vid_description, prosm_int, '0', link_chan, vid_link)

                vids = ('1', author_date, name_channel, vid_description, prosm_int, '0', link_chan, vid_link)
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

get_vids()

# "channel-name"
# channel-info
# 'video-title

# <ytd-video-renderer class="style-scope ytd-item-section-renderer" lockup="" prominent-thumb-style="DEFAULT" use-prominent-thumbs="" inline-title-icon=""><!--css-build:shady--><div id="dismissable" class="style-scope ytd-video-renderer">
#   <ytd-thumbnail use-hovered-property="" class="style-scope ytd-video-renderer"><!--css-build:shady--><a id="thumbnail" class="yt-simple-endpoint inline-block style-scope ytd-thumbnail" aria-hidden="true" tabindex="-1" rel="null" href="/watch?v=80xrqh3hTUY">
#   <yt-img-shadow ftl-eligible="" class="style-scope ytd-thumbnail no-transition" style="background-color: transparent;" loaded=""><!--css-build:shady--><img id="img" class="style-scope yt-img-shadow" alt="" width="360" src="https://i.ytimg.com/vi/80xrqh3hTUY/hq720.jpg?sqp=-oaymwEcCOgCEMoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&amp;rs=AOn4CLBipNxRDNYABl9IYp45UFD9Tl7kqw"></yt-img-shadow>
#
#   <div id="overlays" class="style-scope ytd-thumbnail"><ytd-thumbnail-overlay-time-status-renderer class="style-scope ytd-thumbnail" overlay-style="DEFAULT"><!--css-build:shady--><yt-icon class="style-scope ytd-thumbnail-overlay-time-status-renderer" disable-upgrade="" hidden=""></yt-icon><span class="style-scope ytd-thumbnail-overlay-time-status-renderer" aria-label="10 минут 11 секунд">
#   10:11
# </span></ytd-thumbnail-overlay-time-status-renderer><ytd-thumbnail-overlay-now-playing-renderer class="style-scope ytd-thumbnail"><!--css-build:shady--><span class="style-scope ytd-thumbnail-overlay-now-playing-renderer">Текущее видео</span>
# <ytd-thumbnail-overlay-equalizer class="style-scope ytd-thumbnail-overlay-now-playing-renderer" hidden=""><!--css-build:shady--><svg xmlns="http://www.w3.org/2000/svg" id="equalizer" viewBox="0 0 55 95" class="style-scope ytd-thumbnail-overlay-equalizer">
#   <g class="style-scope ytd-thumbnail-overlay-equalizer">
#     <rect class="bar style-scope ytd-thumbnail-overlay-equalizer" x="0"></rect>
#     <rect class="bar style-scope ytd-thumbnail-overlay-equalizer" x="20"></rect>
#     <rect class="bar style-scope ytd-thumbnail-overlay-equalizer" x="40"></rect>
#   </g>
# </svg>
# </ytd-thumbnail-overlay-equalizer>
# </ytd-thumbnail-overlay-now-playing-renderer></div>
#   <div id="mouseover-overlay" class="style-scope ytd-thumbnail"></div>
#   <div id="hover-overlays" class="style-scope ytd-thumbnail"></div>
# </a>
# </ytd-thumbnail>
#   <div class="text-wrapper style-scope ytd-video-renderer">
#     <div id="meta" class="style-scope ytd-video-renderer">
#       <div id="title-wrapper" class="style-scope ytd-video-renderer">
#         <h3 class="title-and-badge style-scope ytd-video-renderer">
#           <ytd-badge-supported-renderer class="style-scope ytd-video-renderer" disable-upgrade="" hidden="">
#           </ytd-badge-supported-renderer>
#           <a id="video-title" class="yt-simple-endpoint style-scope ytd-video-renderer" title="КРАШ ТЕСТ Toyota Supra, разбил машину из ПЛАСТИЛИНА" href="/watch?v=80xrqh3hTUY" aria-label="КРАШ ТЕСТ Toyota Supra, разбил машину из ПЛАСТИЛИНА Автор: Handmade 6 месяцев назад 10 минут 11 секунд 414&nbsp;030 просмотров">
#             <yt-icon id="inline-title-icon" class="style-scope ytd-video-renderer" hidden=""><!--css-build:shady--></yt-icon>
#             <yt-formatted-string class="style-scope ytd-video-renderer" aria-label="КРАШ ТЕСТ Toyota Supra, разбил машину из ПЛАСТИЛИНА Автор: Handmade 6 месяцев назад 10 минут 11 секунд 414&nbsp;030 просмотров">КРАШ ТЕСТ Toyota Supra, разбил машину из ПЛАСТИЛИНА</yt-formatted-string>
#           </a>
#         </h3>
#         <div id="menu" class="style-scope ytd-video-renderer"><ytd-menu-renderer class="style-scope ytd-video-renderer"><!--css-build:shady--><div id="top-level-buttons" class="style-scope ytd-menu-renderer"></div>
# <yt-icon-button id="button" class="dropdown-trigger style-scope ytd-menu-renderer"><!--css-build:shady--><button id="button" class="style-scope yt-icon-button" aria-label="Меню действий">
#   <yt-icon class="style-scope ytd-menu-renderer"><svg viewBox="0 0 24 24" preserveAspectRatio="xMidYMid meet" focusable="false" class="style-scope yt-icon" style="pointer-events: none; display: block; width: 100%; height: 100%;"><g class="style-scope yt-icon"><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z" class="style-scope yt-icon"></path></g></svg><!--css-build:shady--></yt-icon>
# </button></yt-icon-button>
# </ytd-menu-renderer></div>
#       </div>
#       <ytd-video-meta-block class="style-scope ytd-video-renderer"><!--css-build:shady-->
# <div id="metadata" class="style-scope ytd-video-meta-block">
#   <div id="byline-container" class="style-scope ytd-video-meta-block" hidden="">
#     <ytd-channel-name id="channel-name" class="style-scope ytd-video-meta-block"><!--css-build:shady--><div id="container" class="style-scope ytd-channel-name">
#   <div id="text-container" class="style-scope ytd-channel-name">
#     <yt-formatted-string id="text" title="" class="style-scope ytd-channel-name complex-string" ellipsis-truncate="" has-link-only_=""><a class="yt-simple-endpoint style-scope yt-formatted-string" spellcheck="false" href="/channel/UCwWp8hvp2szhX53OqAmcy5w" dir="auto">Handmade</a></yt-formatted-string>
#   </div>
#   <paper-tooltip fit-to-visible-bounds="" class="style-scope ytd-channel-name" role="tooltip" tabindex="-1"><!--css-build:shady-->
#
#
#     <div id="tooltip" class="hidden style-scope paper-tooltip">
#
#     Handmade
#
#     </div>
# </paper-tooltip>
# </div>
# <ytd-badge-supported-renderer class="style-scope ytd-channel-name"><!--css-build:shady-->
#   <div class="badge badge-style-type-verified style-scope ytd-badge-supported-renderer">
#     <yt-icon class="style-scope ytd-badge-supported-renderer"><svg viewBox="0 0 24 24" preserveAspectRatio="xMidYMid meet" focusable="false" class="style-scope yt-icon" style="pointer-events: none; display: block; width: 100%; height: 100%;"><g class="style-scope yt-icon"><path fill-rule="evenodd" clip-rule="evenodd" d="M12,2C6.48,2,2,6.48,2,12s4.48,10,10,10s10-4.48,10-10 S17.52,2,12,2z M9.92,17.93l-4.95-4.95l2.05-2.05l2.9,2.9l7.35-7.35l2.05,2.05L9.92,17.93z" class="style-scope yt-icon"></path></g></svg><!--css-build:shady--></yt-icon>
#     <span class="style-scope ytd-badge-supported-renderer"></span>
#   <paper-tooltip position="top" class="style-scope ytd-badge-supported-renderer" role="tooltip" tabindex="-1"><!--css-build:shady-->
#
#
#     <div id="tooltip" class="hidden style-scope paper-tooltip">
#       Подтверждено
#     </div>
# </paper-tooltip></div>
# <dom-repeat id="repeat" as="badge" class="style-scope ytd-badge-supported-renderer"><template is="dom-repeat"></template></dom-repeat>
# </ytd-badge-supported-renderer>
# </ytd-channel-name>
#     <div id="separator" class="style-scope ytd-video-meta-block">•</div>
#   </div>
#   <div id="metadata-line" class="style-scope ytd-video-meta-block">
#
#       <span class="style-scope ytd-video-meta-block">414&nbsp;тыс. просмотров</span>
#
#       <span class="style-scope ytd-video-meta-block">6 месяцев назад</span>
#     <dom-repeat strip-whitespace="" class="style-scope ytd-video-meta-block"><template is="dom-repeat"></template></dom-repeat>
#   </div>
# </div>
# <div id="additional-metadata-line" class="style-scope ytd-video-meta-block">
#   <dom-repeat class="style-scope ytd-video-meta-block"><template is="dom-repeat"></template></dom-repeat>
# </div>
#
# </ytd-video-meta-block>
#     </div>
#     <div id="channel-info" class="style-scope ytd-video-renderer">
#       <a class="style-scope ytd-video-renderer" href="/channel/UCwWp8hvp2szhX53OqAmcy5w" aria-label="Перейти на канал">
#         <yt-img-shadow width="24" class="style-scope ytd-video-renderer no-transition" style="background-color: transparent;" loaded=""><!--css-build:shady--><img id="img" class="style-scope yt-img-shadow" alt="" width="24" src="https://yt3.ggpht.com/ytc/AAUvwni8REGJfjopZ-iKVS6wVsVSmq4C8YvLppdglZuN0l4=s68-c-k-c0x00ffffff-no-rj"></yt-img-shadow>
#       </a>
#       <ytd-channel-name id="channel-name" class="long-byline style-scope ytd-video-renderer" wrap-text="true"><!--css-build:shady--><div id="container" class="style-scope ytd-channel-name">
#   <div id="text-container" class="style-scope ytd-channel-name">
#     <yt-formatted-string id="text" title="" class="style-scope ytd-channel-name" has-link-only_=""><a class="yt-simple-endpoint style-scope yt-formatted-string" spellcheck="false" href="/channel/UCwWp8hvp2szhX53OqAmcy5w" dir="auto">Handmade</a></yt-formatted-string>
#   </div>
#   <paper-tooltip fit-to-visible-bounds="" class="style-scope ytd-channel-name" role="tooltip" tabindex="-1" style="inset: 18.5px auto auto 361px;"><!--css-build:shady-->
#
#
#     <div id="tooltip" class="style-scope paper-tooltip hidden">
#
#     Handmade
#
#     </div>
# </paper-tooltip>
# </div>
# <ytd-badge-supported-renderer class="style-scope ytd-channel-name"><!--css-build:shady-->
#   <div class="badge badge-style-type-verified style-scope ytd-badge-supported-renderer">
#     <yt-icon class="style-scope ytd-badge-supported-renderer"><svg viewBox="0 0 24 24" preserveAspectRatio="xMidYMid meet" focusable="false" class="style-scope yt-icon" style="pointer-events: none; display: block; width: 100%; height: 100%;"><g class="style-scope yt-icon"><path fill-rule="evenodd" clip-rule="evenodd" d="M12,2C6.48,2,2,6.48,2,12s4.48,10,10,10s10-4.48,10-10 S17.52,2,12,2z M9.92,17.93l-4.95-4.95l2.05-2.05l2.9,2.9l7.35-7.35l2.05,2.05L9.92,17.93z" class="style-scope yt-icon"></path></g></svg><!--css-build:shady--></yt-icon>
#     <span class="style-scope ytd-badge-supported-renderer"></span>
#   <paper-tooltip position="top" class="style-scope ytd-badge-supported-renderer" role="tooltip" tabindex="-1"><!--css-build:shady-->
#
#
#     <div id="tooltip" class="hidden style-scope paper-tooltip">
#       Подтверждено
#     </div>
# </paper-tooltip></div>
# <dom-repeat id="repeat" as="badge" class="style-scope ytd-badge-supported-renderer"><template is="dom-repeat"></template></dom-repeat>
# </ytd-badge-supported-renderer>
# </ytd-channel-name>
#     </div>
#     <yt-formatted-string id="description-text" class="style-scope ytd-video-renderer"><span dir="auto" class="style-scope yt-formatted-string">#краш_тест #toyota_supra #crash_test #</span><span dir="auto" class="bold style-scope yt-formatted-string">handmade</span><span dir="auto" class="style-scope yt-formatted-string"> #своими_руками #crashed_car #how_to_make #crafts #clay_sculpting #diy&nbsp;...</span></yt-formatted-string>
#     <dom-repeat class="style-scope ytd-video-renderer" hidden=""><template is="dom-repeat"></template></dom-repeat>
#     <ytd-badge-supported-renderer id="badges" class="style-scope ytd-video-renderer"><!--css-build:shady-->
#   <div class="badge badge-style-type-simple style-scope ytd-badge-supported-renderer">
#     <yt-icon class="style-scope ytd-badge-supported-renderer" disable-upgrade="" hidden="">
#     </yt-icon>
#     <span class="style-scope ytd-badge-supported-renderer">4K</span>
#   </div>
#
#   <div class="badge badge-style-type-simple style-scope ytd-badge-supported-renderer" aria-label="Субтитры">
#     <yt-icon class="style-scope ytd-badge-supported-renderer" disable-upgrade="" hidden="">
#     </yt-icon>
#     <span class="style-scope ytd-badge-supported-renderer">Субтитры</span>
#   </div>
# <dom-repeat id="repeat" as="badge" class="style-scope ytd-badge-supported-renderer"><template is="dom-repeat"></template></dom-repeat>
# </ytd-badge-supported-renderer>
#     <div id="buttons" class="style-scope ytd-video-renderer"></div>
#   </div>
# </div>
# <div id="dismissed" class="style-scope ytd-video-renderer"></div>
# </ytd-video-renderer>