# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

import redis
from bs4 import BeautifulSoup


class ershoufang_bxPipeline(object):
    redislci = None

    def __init__(self):
        self.rediscli = redis.StrictRedis(host='localhost', port=6379, db=2)
        pass

    def process_item(self, item, spider):
        reponse = item.get('raw')
        print(reponse)
        html = reponse.text
        url = reponse.url
        soup = BeautifulSoup(html)
        flag = self.rediscli.sismember('bx_detail_page_key', url)
        if flag:
            print('错误')
        print(soup.find('h1'))
        souce_code = re.findall(r'\d+', url)[0]
        with open('/home/wang/bx_ershoufang/%s.html' % souce_code, 'w+') as ff:
            ff.write(html)

        return item
