#!pip uninstall -y rssarchive
#!pip install /home/suat/Belgeler/github/turnusol_prod/turnusol/factomat/scripts/rssarchive/
import pandas as pd
import feedparser
from newspaper import Article
import datetime
import sqlite3
import string
import time
import timeit
import pathlib
import os
import textwrap
import inspect
import feedparser
from newspaper import Article
import datetime
import sqlite3
import importlib.machinery # to import files as module
ora = importlib.machinery.SourceFileLoader('rssarchive','./rssarchive/__init__.py').load_module()
ra  = ora.RssArchive(CONFIG_TEST_MODE=True,CONFIG_FULL_TEXT_MODE = False)

dir(ra)

ra.create_rss_list_if_doest_not_exist(rss_list = "abrakadabra-2.csv")

ra.create_rss_list_if_doest_not_exist()

ra._private_generate_table_if_dont_exists()

headline,fulltext,date,source,source_name = "headline","fulltext","date","a","source_name"
ra.check_whether_headline_exist_in_archive(source = "sourceX")

ra.save_news_item_to_sqlite(headline,fulltext,date,source,source_name)

ra.delete_news_item_in_sqlite("source")

ra.save_rss(source_name = "Sabah")



ra.batch_save_rss()








rss_list = "rss list.csv"
DEFAULT_RSS_LIST = textwrap.dedent("""
            name,url
            Hürriyet,https://www.hurriyet.com.tr/rss/anasayfa
            Sabah,https://www.sabah.com.tr/rss/anasayfa.xml
            Star,http://www.star.com.tr/rss/rss.asp
            Takvim,https://www.takvim.com.tr/rss/anasayfa.xml
            Türkiye,http://www.turkiyegazetesi.com.tr/rss/rss.xml
            YeniÇağ,https://www.yenicaggazetesi.com.tr/rss
            YeniŞafak,https://www.yenisafak.com/Rss
            CNNTürk,https://www.cnnturk.com/feed/rss/news
            HaberTürk,http://www.haberturk.com/rss
            NTV,https://www.ntv.com.tr/gundem.rss
            GazeteDuvar,http://www.gazeteduvar.com.tr/feed
            Birgün,https://www.birgun.net/feed
            Milliyet,https://www.milliyet.com.tr/rss/rssnew/gundemrss.xml
            Cumhuriyet,http://www.cumhuriyet.com.tr/rss/son_dakika.xml
            Sözcü,https://www.sozcu.com.tr/feed/
            """)
DEFAULT_RSS_LIST = "".join([s for s in DEFAULT_RSS_LIST.strip().splitlines(True) if s.strip()])
path = ""
file = rss_list
p = pathlib.Path(file)
if p.is_file():
    # Creating a file at specified location
    with open(os.path.join(path, file), 'w') as fp:
        fp.write(DEFAULT_RSS_LIST)
        fp.close()
        self.easydebug("RSS file does not exist, it was created")
else:
    self.easydebug("RSS list file already exists")
    pass
return True
