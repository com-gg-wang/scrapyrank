# -*- coding: utf-8 -*-
import codecs
import re

import pymysql
import redis
import scrapy
from scrapy import log
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class EntreySpider(CrawlSpider):
    name = 'entrey'

    # allowed_domains = ['job_51.com']
    # https://www.baidu.com/s?wd=众益天成%23天眼查

    # start_urls = urls

    def start_requests(self):
        db = pymysql.connect(host='192.168.1.214', port=4000, user='dbuser', passwd='dbuserDev123', db='spiderData',
                             use_unicode='true', charset='utf8')
        cursor = db.cursor()
        cursor.execute('select company_name from company_name')
        fetchall = cursor.fetchall()
        print(fetchall)
        urls = []
        for s in fetchall:
            request = scrapy.Request('https://www.baidu.com/s?wd=%s%23天眼查' % s
                                     , callback=self.parse)
            yield request

    rules = (
        Rule(LinkExtractor(allow=r'.*',
                           restrict_xpaths=r'//'), callback='parse_item')
    )

    def parse_item(self, response):
        i = {}
        i['raw'] = response
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        yield i


if __name__ == '__main__':
    ma = re.search('http://dl.ganji.com/\w+/\d+x.htm', 'http://dl.ganji.com/fang5/3293904744x.htm')
    print(ma.group(0))
