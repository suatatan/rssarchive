#!pip uninstall -y rssarchive
#!pip install /home/suat/Belgeler/github/turnusol_prod/turnusol/factomat/scripts/rssarchive/
import pandas as pd
import feedparser
from newspaper import Article
import datetime
import sqlite3
import importlib.machinery # to import files as module
ra = importlib.machinery.SourceFileLoader('rssarchive','/home/suat/Belgeler/github/turnusol_prod/turnusol/factomat/scripts/rssarchive/rssarchive/__init__.py').load_module()

dir(ra)

ra._private_generate_table_if_dont_exists()

headline,fulltext,date,source,source_name = "headline","fulltext","date","a","source_name"
ra.check_whether_headline_exist_in_archive(source = "sourceX")

ra.save_news_item_to_sqlite(headline,fulltext,date,source,source_name)

ra.delete_news_item_in_sqlite("source")

ra.save_rss(source_name = "Sabah")



ra.batch_save_rss()
