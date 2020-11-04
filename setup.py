from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='rssarchive',
      version='0.5',
      keywords = 'RSS,SQlite, News',
      description='Archive your RSS into SQLite:',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/suatatan/rssarchive',
      author='Suat ATAN',
      author_email='suatatan@gmail.com',
      license='MIT',
      packages=['rssarchive'],
      test_suite='nose.collector',
      scripts=['bin/rssarchive'],
      tests_require=['nose'],
      install_requires = ['newspaper3k','feedparser'],
      zip_safe=False)
