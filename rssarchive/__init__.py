import pandas as pd
import feedparser
from newspaper import Article
import datetime
import sqlite3
import string
import time
import timeit

class RssArchive:

    def __init__(self,
            CONFIG_DEFAULT_TABLE_NAME = 'tab_headline',
            CONFIG_SQLITEDB_URL = "/home/suat/rssarchive.sqlite",
            CONFIG_RSS_LIST = "/home/suat/rss_list.csv",
            CONFIG_SINGLE_RSS_SOURCE_URL = "https://www.sabah.com.tr/rss/anasayfa.xml",
            CONFIG_EASY_DEBUG = True,
            CONFIG_TEST_VAR = "suatatan",
            CONFIG_TEST_MODE = False,
            CONFIG_FULL_TEXT_MODE = True,
        ):
        self.CONFIG_DEFAULT_TABLE_NAME = CONFIG_DEFAULT_TABLE_NAME
        self.CONFIG_SQLITEDB_URL = CONFIG_SQLITEDB_URL
        self.CONFIG_RSS_LIST = CONFIG_RSS_LIST
        self.CONFIG_SINGLE_RSS_SOURCE_URL = CONFIG_SINGLE_RSS_SOURCE_URL
        self.CONFIG_EASY_DEBUG = CONFIG_EASY_DEBUG # If true all messages will shown
        self.CONFIG_TEST_MODE = CONFIG_TEST_MODE # When it is True some long tasks become shorter to debug
        self.CONFIG_FULL_TEXT_MODE = CONFIG_FULL_TEXT_MODE
        self.CONFIG_TEST_VAR = CONFIG_TEST_VAR
        self.easydebug(f"""CONFIGURATION:
            CONFIG_DEFAULT_TABLE_NAME = {CONFIG_DEFAULT_TABLE_NAME},
            CONFIG_SQLITEDB_URL = {CONFIG_SQLITEDB_URL}
            CONFIG_RSS_LIST = {CONFIG_RSS_LIST}
            CONFIG_SINGLE_RSS_SOURCE_URL = {CONFIG_SINGLE_RSS_SOURCE_URL}
            CONFIG_EASY_DEBUG = {CONFIG_EASY_DEBUG}
            CONFIG_TEST_VAR = {CONFIG_TEST_VAR}
            CONFIG_TEST_MODE = {CONFIG_TEST_MODE}
            CONFIG_FULL_TEXT_MODE = {CONFIG_FULL_TEXT_MODE}
        """)

    def testfun(self):
        return CONFIG_TEST_VAR

    def easydebug(self,msg = None,show = None):
        show = self.CONFIG_EASY_DEBUG if show == None else show
        if show:
            print(msg)
        else:
            pass

    def count_fethed_news_in_datetime(self,the_date = None,sqlite_db_url = None):
        """Count number of news after datetime like YYYY-MM-DD HH:MM:SS if Date is None today date will be calculated"""
        sqlite_db_url = self.CONFIG_SQLITEDB_URL if sqlite_db_url == None else sqlite_db_url
        try:
            if the_date == None:
                nw = datetime.datetime.now()
                today = nw.strftime("%Y-%m-%d")
                the_date = today
            sql = f"select count(*) from tab_headline where datetime(timestamp) > '{the_date}'"
            vt = sqlite3.connect(sqlite_db_url)
            im = vt.cursor()
            res = im.execute(sql)
            val = res.fetchone()
            val = [i for i in val][0] # unzip
            vt.close()
            return val
        except Exception as ex:
            self.easydebug("Error: Officio  "+str(ex))
            return 0

    def batch_save_rss(self,rss_list = None):
        """Takes rss_list and processes each source and saves it into sqlite.
        Parameters
        ----------
        rss_list : list
            The file path of two column rss sources list. First column is name of source second column is URL of rss.
        """
        rss_list = self.CONFIG_RSS_LIST if rss_list == None else rss_list
        allrss = pd.read_csv(rss_list) if self.CONFIG_TEST_MODE != True else pd.read_csv(rss_list).sample(2)

        try:
            start = timeit.default_timer()
            for index,row in allrss.iterrows():
                #row = allrss.iloc[0,]
                this_source_name,this_source = row['name'],row['url']
                self.easydebug(f"RSS source name: {this_source_name}")
                self.save_rss(rss_source_url = this_source, source_name = this_source_name)
            # expost operations (Reporting)
            number_of_fetched_news_today = self.count_fethed_news_in_datetime()
            stop = timeit.default_timer()
            process_duration = stop - start
            print(f"TOTALLY {number_of_fetched_news_today} headlines has been fetched within the {process_duration}!")
        except Exception as ex:
            self.easydebug("Error: Pomodoro  "+str(ex))

    def save_rss(self,rss_source_url = None,
                 sqlite_db_url = None,
                 source_name = "unknown",
                 show_titles = False):
        """Saves news in the RSS url into SQlite file
         Parameters
            ----------
            rss_source_url : str
                The URL of the valid RSS source to feed
            sqlite_db_url : str
                The file path of the SQLite file
            show_titles: bool, optional
                If is True the titles will be self.easydebug
        """
        sqlite_db_url = self.CONFIG_SQLITEDB_URL if sqlite_db_url == None else sqlite_db_url
        rss_source_url = self.CONFIG_SINGLE_RSS_SOURCE_URL if rss_source_url == None else rss_source_url
        try:
            NewsFeed = feedparser.parse(rss_source_url)
            entries = NewsFeed.entries
            df = pd.DataFrame(entries)
            count_of_news = df.count()[0]
            counter = 0
            self.easydebug(f"{count_of_news} news headline will be fetched")
            for index,row in df.iterrows():
                #row = df.iloc[0,]
                if show_titles:
                    print(row['title'])
                scraped_fulltext = None if self.CONFIG_FULL_TEXT_MODE == False else self.scrape_full_text_from_url(row.link)
                headline,fulltext,date,source,in_source_name = row.title,scraped_fulltext,row.published,row.link,source_name
                self.save_news_item_to_sqlite(headline,fulltext,date,source,in_source_name)
                print(row.title)
                self.easydebug(f"{counter} th. headline saved for {in_source_name}  ")
                counter = counter + 1
            return True
        except Exception as ex:
            self.easydebug("Error: Fenestra  "+str(ex))
            return False

    def scrape_full_text_from_url(self,page_url):
        self.easydebug(f"Full text has started for  {page_url}")
        try:
            article = Article(page_url)
            article.download()
            article.parse()
            parsed_text  = article.text
            if len(parsed_text)>100:
                self.easydebug(f"Text is scraped here first words"+ parsed_text[0:20])
                return parsed_text
            else:
                self.easydebug("Text cannot be parsed")
                return None
        except Exception as ex:
            self.easydebug("Error: Fiore "+str(ex))
            return None

    def save_news_item_to_sqlite(self,headline,
                                 fulltext,
                                 date,
                                 source,
                                 source_name,
                                 table_name=None,
                                 sqlite_db_url = None):
        """Save single  headline to table in the database. If there is not any table it will create."""
        sqlite_db_url = self.CONFIG_SQLITEDB_URL if sqlite_db_url == None else sqlite_db_url
        table_name = self.CONFIG_DEFAULT_TABLE_NAME if table_name == None else table_name
        try:
            # for first run
            self._private_generate_table_if_dont_exists()
            is_source_does_not_exists_before = not(self.check_whether_headline_exist_in_archive(source))
            if is_source_does_not_exists_before:
                #item does not exists
                vt = sqlite3.connect(sqlite_db_url)
                im = vt.cursor()
                sql = f"insert into {table_name}(headline,fulltext,date,source,source_name) values(?,?,?,?,?)"
                veri = (headline,fulltext,date,source,source_name)
                x = im.execute(sql,veri)
                vt.commit()
                vt.close()
                self.easydebug(f"Item saved: {source}")
                return True
            else:
                # source is already exists
                self.easydebug(f"Source is already exists, passed: {source}")
                return False
        except Exception as ex:
            self.easydebug(f"""Error: Aeroplane,
                            Hey where is your db and table check it!:
                            sqlite_db_url: {sqlite_db_url} """ + str(ex))
            return False

    def delete_news_item_in_sqlite(self, source,
                        table_name = None,
                        sqlite_db_url = None):
        sqlite_db_url = self.CONFIG_SQLITEDB_URL if sqlite_db_url == None else sqlite_db_url
        table_name = self.CONFIG_DEFAULT_TABLE_NAME if table_name == None else table_name
        try:
            vt = sqlite3.connect(sqlite_db_url)
            sql = f'DELETE FROM {table_name} WHERE source=?'
            im = vt.cursor()
            im.execute(sql, (source,))
            vt.commit()
            vt.close()
        except Exception as ex:
            self.easydebug("Error: Ragazzo "+str(ex))

    def check_whether_headline_exist_in_archive(self, source,
                                                table_name = None,
                                                sqlite_db_url = None):
        """Check whether any headline url is exist in archive, if any result exist it returns True"""
        sqlite_db_url = self.CONFIG_SQLITEDB_URL if sqlite_db_url == None else sqlite_db_url
        table_name = self.CONFIG_DEFAULT_TABLE_NAME if table_name == None else table_name
        self.easydebug("check_whether_headline_exist_in_archive runned")
        vt = sqlite3.connect(sqlite_db_url)
        im = vt.cursor()
        sql = f"select * from {table_name} where source = '{source}'"
        im.execute(sql)
        result = im.fetchone()
        ret = result != None
        vt.close()
        if ret:
            msg = f"item is exists {source}"
        else:
            msg = f"item is not exists {source}"
        self.easydebug(msg)
        return ret

    def _private_generate_table_if_dont_exists(self, table_name = None,
                                               sqlite_db_url = None):
        """Creates tab_headline table if it doesn't exist
        Parameters:
        ------------
        table_name: str,optional
            The table name that will be generate in the database
        sqlite_db_url : str, optional
            The file path of the SQLite file
        """
        sqlite_db_url = self.CONFIG_SQLITEDB_URL if sqlite_db_url == None else sqlite_db_url
        table_name = self.CONFIG_DEFAULT_TABLE_NAME if table_name == None else table_name
        try:
            vt = sqlite3.connect(sqlite_db_url)
            im = vt.cursor()
            sql = f"""CREATE TABLE IF NOT EXISTS  {table_name}(
            headline_id INTEGER PRIMARY KEY AUTOINCREMENT,
            headline TEXT,
            fulltext TEXT,
            date TEXT,
        	source TEXT,
            source_name TEXT,
        	timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);"""
            im.execute(sql)
            vt.commit()
            vt.close()
            return True
        except Exception as ex:
            self.easydebug("Error:  Giardino "+str(ex))
            return False

    def _private_whoami(self):
        return "suat"
