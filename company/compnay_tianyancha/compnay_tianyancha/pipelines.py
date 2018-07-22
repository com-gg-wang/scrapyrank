# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

from bs4 import BeautifulSoup


class CompnayTianyanchaPipeline(object):
    def process_item(self, item, spider):
        get = dict(item).get('raw')
        # print(get)
        re_compile = re.compile(r'https://www\.tianyancha\.com/company/\d+')

        search = re_compile.findall(get)[0]
        search = re.findall(r'\d+',search)[0]
        if search:
            with open('/Users/wang/tianyancha/%s.html'%search,'w',encoding='gb18030') as f :
                f.write(get)
        return item
