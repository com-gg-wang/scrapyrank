# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

from bs4 import BeautifulSoup


class AnjukePipeline(object):
    def process_item(self, item, spider):
        reponse = item.get('raw')
        html = reponse.text
        url = reponse.url
        print(url)
        soup = BeautifulSoup(html)
        print(soup.find('h1'))
        print(soup.find('h3'))
        souce_code = re.findall(r'A\d+', url)[0]
        with open('/home/wang/anjukeershoufang/%s.html' % souce_code, 'w+') as ff:
            ff.write(html)

        return item
