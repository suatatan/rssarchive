from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='rssarchive',
      version='0.2',
      keywords = 'RSS,SQlite, News',
      description='Archive your RSS into SQLite',
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
