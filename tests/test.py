"""
To run test functions just call it from its parent directory it means if you see OK all functions work properly.
"""
#!pip install rssarchive
import unittest
import string
import random
#import rssarchive as ra
import importlib.machinery # to import files as module
ora = importlib.machinery.SourceFileLoader('rssarchive','rssarchive/__init__.py').load_module()

ra = ora.RssArchive(CONFIG_TEST_VAR= "suat",
                    CONFIG_EASY_DEBUG = False,
                    CONFIG_TEST_MODE=True,
                    CONFIG_FULL_TEXT_MODE = False)
ra.CONFIG_TEST_VAR

def get_random_string(length):
    """For inserting operations during tests"""
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return(result_str)

class TestRssArchive(unittest.TestCase):

    def test_create_rss_list_if_doest_not_exist(self):
        self.assertEqual(ra.create_rss_list_if_doest_not_exist(), True, "Result should be True")

    def test_scrape_full_text_from_url(self):
        result = ra.scrape_full_text_from_url("https://www.sqlitetutorial.net/sqlite-between/")
        is_more_than_zero = len(result) >0
        self.assertEqual(is_more_than_zero,True,"Return should be satisfy is_the_more_than_zero rule")

    def test_count_fethed_news_in_datetime(self):
        result = ra.count_fethed_news_in_datetime(the_date = "2090-01-01")
        self.assertEqual(result,0,"Return should be zero'")

    def test_private_generate_table_if_dont_exists(self):
        self.assertEqual(ra._private_generate_table_if_dont_exists(), True, "Result should be True")

    def test_save_news_item_to_sqlite(self):
        random_source = "random_string_"+get_random_string(10)
        headline,fulltext,date,source,source_name = "headline","fulltext","date",random_source,"source_name"
        sonuc = ra.save_news_item_to_sqlite(headline,fulltext,date,source,source_name)
        self.assertEqual(sonuc,True,"Return should be True'")

    def test_save_news_item_to_sqlite_2(self):
        """It is first trial to testing saving CONSTANT_STRING
        Return should be True and item should be saved
        Sometimes you may run twice or more at that time test can give error to solve this
        the row string will be deleted after test
        """
        standard_source = "CONSTANT_STRING"
        headline,fulltext,date,source,source_name = "headline","fulltext","date",standard_source,"source_name"
        if ra.check_whether_headline_exist_in_archive(standard_source):
            #delete old one
            ra.delete_news_item_in_sqlite(standard_source)
        else:
            pass
        sonuc = ra.save_news_item_to_sqlite(headline,fulltext,date,source,source_name)
        self.assertEqual(sonuc,True,"Return should be True'")

    def test_save_news_item_to_sqlite_3(self):
        """It is second trial to testing saving CONSTANT_STRING Return should be False and item should not be saved agian """
        standard_source = "CONSTANT_STRING"
        headline,fulltext,date,source,source_name = "headline","fulltext","date",standard_source,"source_name"
        sonuc = ra.save_news_item_to_sqlite(headline,fulltext,date,source,source_name)
        self.assertEqual(sonuc,False,"Return should be False because CONSTANT_STRING already exists'")

    def test_save_rss(self):
        self.assertEqual(ra.save_rss(), True, "Result should be True, save_rss should get news or pass if exist any news")

    def test__whoami(self):
        self.assertEqual(ra._private_whoami(), "suat", "Result should be suat")

if __name__ == '__main__':
    unittest.main()
