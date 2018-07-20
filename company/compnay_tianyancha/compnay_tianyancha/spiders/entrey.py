# -*- coding: utf-8 -*-
import pymysql
import requests
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class EntreySpider(CrawlSpider):
    name = 'entrey'
    allowed_domains = ['baidu.com']
    # start_urls = ['http://baidu.com/']

    def start_requests(self):
        db = pymysql.connect(host='192.168.1.214', port=4000, user='dbuser', passwd='dbuserDev123', db='spiderData',
                             use_unicode='true', charset='utf8')
        cursor = db.cursor()
        cursor.execute('select company_name from company_name limit 3 ')
        fetchall = cursor.fetchall()
        print(fetchall)
        urls = []
        for s in fetchall:
            print(s)
            a = 'https://www.baidu.com/s?wd=%s 天眼查' % s
            print(a)
            request = scrapy.Request(a
                                     , callback=self.parse_item)
            print()
            yield request
    # rules = (
    #     Rule(LinkExtractor(allow=r'.*'), callback='parse_item', follow=True),
    # )

    def parse_item(self, response):
        i = {}
        i['raw'] = response.text
        print(i['raw'])
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        yield i


if __name__ == '__main__':
    a = "https://www.baidu.com/s?wd=%E5%B9%B3%E5%AE%89%E6%99%AE%E6%83%A0%E6%8A%95%E8%B5%84%E5%92%A8%E8%AF%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E8%8B%8F%E5%B7%9E%E6%96%87%E5%88%9B%E5%A4%A7%E5%8E%A6%E5%88%86%E5%85%AC%E5%8F%B83%E5%A4%A9%E7%9C%BC%E6%9F%A5"
    # response = requests.get(a, headers='', cookies=self.cookies, timeout=self.timeout)




