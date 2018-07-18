# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import os
import re

import pymysql
import redis
from bs4 import BeautifulSoup


class job_51Pipeline(object):

    def __init__(self):
        self.db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='Dream96*', db='spider',
                                  use_unicode='true', charset='utf8')
        pass

    def process_item(self, item, spider):
        cursor = self.db.cursor()

        for a in dict(item).get('company_name'):
            s = "INSERT INTO company (company_n) VALUES ('%s')" % a.strip()
            print(s)
            cursor.execute(s)
            self.db.commit()
        return item

    def close_spider(self, spider):
        self.file.close()


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
