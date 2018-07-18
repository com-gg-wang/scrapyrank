# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import re

import redis
from bs4 import BeautifulSoup


class qichachaPipeline(object):
    def process_item(self, item, spider):
        reponse = item.get('raw')
        html = reponse.text
        url = reponse.url
        soup = BeautifulSoup(html)
        print(soup.find('h1'))
        print(soup.find('p', {'class': "card-title"}))
        souce_code = re.findall(r'/\d+x', url)[0]
        with open('/home/wang/gj_ershoufang/%s.html' % souce_code, 'w+') as ff:
            ff.write(html)

        return item


# 此处的主方法用取读取，本地文件，拼接url添加进redis
if __name__ == '__main__':
    source_dir = '/home/wang/gj_ershoufang'
    cli = redis.StrictRedis(host='localhost', port=6379, db=2)

    for root, sub_dirs, files in os.walk(source_dir):
        for special_file in files:

            try:
                spcial_file_dir = os.path.join(root, special_file)
                tt = 'http://dl.ganji.com/fang5/%s' % special_file
                print(tt)
                url = re.search(r'http://dl.ganji.com/\w+/\d+x.htm', tt).group(0)
                # 打开文件的两种方式
                # 1.文件以绝对路径方式
                cli.sadd('gj_detail_page_key', url)
            except:
                continue

    pass
