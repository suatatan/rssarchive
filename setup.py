from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

from setuptools import setup

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='rssarchive',
      version='0.2',
      keywords = 'RSS,SQlite, News',
      description='Archive your RSS into SQLite:',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='',
      author='Suat ATAN',
      author_email='suatatan@gmail.com',
      license='MIT',
      packages=['rssarchive'],
      test_suite='nose.collector',
      scripts=['bin/rssarchive'],
      tests_require=['nose'],
      install_requires = ['newspaper3k','feedparser'],
      zip_safe=False)
