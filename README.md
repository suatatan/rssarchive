# rssarchive

`rssarchive` is a library for fetching multiple RSS source into SQLite database. It has with functionality of scraping full text via `newspaper3k` library.

## Quick Start

To install `rssarchive` just use with pip:

```bash
pip install -i https://test.pypi.org/simple/ rssarchive
```

To use `rssarchive` you can use over console or calling as library:

Using via console simply call:

```bash
rssarchive
```

Using as library:

```python
#!/usr/bin/env python
import rssarchive as ra
newra  = ra.RssArchive(CONFIG_TEST_MODE=True,CONFIG_FULL_TEXT_MODE = False)
newra.batch_save_rss()
```

When you run the `batch_save_rss()` command the library will create two files in the current directory

- rsslist.cv: This is default file that include some RSS sources
- rssarchive.sqlite: This is SQLite file that fetched news

After code finishes his task you can view/edit the SQLite file with [SQLiteBrowser](https://sqlitebrowser.org/) app.

You can modify the `rsslist.csv`file for your own sources and re-run.

## Parameters in the constuction class

When you run code above you may notice the
```python
newra  = ra.RssArchive(CONFIG_TEST_MODE=True,CONFIG_FULL_TEXT_MODE = False)
```

construction. Here all parameters are defined:

CONFIG_DEFAULT_TABLE_NAME = 'tab_headline'

CONFIG_SQLITEDB_URL = "rssarchive.sqlite",

CONFIG_RSS_LIST = "rss_list.csv",

CONFIG_SINGLE_RSS_SOURCE_URL = "https://www.sabah.com.tr/rss/anasayfa.xml",

CONFIG_EASY_DEBUG = True,

CONFIG_TEST_VAR = "suatatan",

CONFIG_TEST_MODE = False,

CONFIG_FULL_TEXT_MODE = True,

**Amgong these params just two parameters are critical:**

CONFIG_EASY_DEBUG: If True you can show all messages in the code, if false you cannot

CONFIG_FULL_TEXT_MODE: If True library will fetch full text of each URL (it takes time) if False the library will getch RSS only

CONFIG_TEST_MODE: If True the library just fetch two sample resource , if false the code will process all RSS sources in the link (**please keep it True for your real projects **)

## Motivation

This library is open-source library developed within the [turnusol.org](turnusol.org) project. This project is a social enterpreneurship for detecting hate-speech and fake-news in Turkish. If you want to contribute this library or our project please contact us via [turnusol.org](turnusol.org)
