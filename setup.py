from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='rssarchive',
      version='0.1',
      keywords = 'RSS,SQlite, News',
      description='Archive your RSS into SQLite',
      url='',
      author='Suat ATAN',
      author_email='suatatan@gmail.com',
      license='MIT',
      packages=['rssarchive'],
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires = ['newspaper','feedparser'],
      zip_safe=False)
