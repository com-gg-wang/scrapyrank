# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re


class ershoufang_58Pipeline(object):
    def process_item(self, item, spider):
        reponse = item.get('raw')
        html = reponse.text
        url = reponse.url
        print(url)
        souce_code = re.findall(r'\d+x', url)[0]
        with open('/home/wang/wubanew/%s.html' % souce_code, 'w+') as ff:
            ff.write(html)

        return item