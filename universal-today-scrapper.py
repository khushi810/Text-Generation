import urllib.request
import requests
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import hashlib
import os

site = os.getenv('LINK')
if site is None:
    raise Exception('No link given')

driver = webdriver.Chrome('/usr/bin/chromedriver')
driver.get(site)
file_path = os.getenv('DEST_PATH') or 'scrapped_files/'
titles = []
contents = []
count = int(os.getenv('START') or 1)
checksum_map = dict()
articles_count = int(os.getenv('ARTICLE_COUNT') or 23000)

try:
    while count <= articles_count:
        hash_md5 = hashlib.md5()
        path = file_path + 'article' + str(count) + '.txt'
        fp = open(path, 'w')
        res = driver.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(res, 'lxml')
        article = soup.article
        title = article.header.h1.text
        fp.write(title + '\n')
        content = article.find('div', 'entry-content').text
        checksum = hashlib.md5(content.encode('utf-8'))
        if checksum in checksum_map:
            raise Exception('duplicate file detected for count {count} & cksm {checksum}'.format(count=count, checksum=checksum))

        checksum_map[checksum] = count

        fp.write(content)
        #titles.append(title)
        #contents.append(content)
        prev_link = soup.nav.find('div', 'nav-previous').a.get('href')
        print(str(count) + ". file saved in " + path)
        driver.get(prev_link)
        count = count + 1
        fp.close()
        time.sleep(0.5)
except:
    print('last count', count)
    print('last entry', list(checksum_map.values()).sort[-1])
    raise
