# -*- coding: utf-8 -*-
import codecs
import re

import redis
import scrapy
from scrapy import log
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class EntreySpider(CrawlSpider):
    name = 'entrey'
    # allowed_domains = ['ershoufang_58.com']
    start_urls = ['http://dl.58.com/ershoufang/']

    rules = (
        Rule(LinkExtractor(allow=r'http://dl\.58\.com/\w+/ershoufang/',
                           restrict_xpaths=r'//div[@class="wz-first  on "]/a')),
        Rule(LinkExtractor(allow=r'http://dl.58.com/\w+/ershoufang/',
                           restrict_xpaths=r'//div[@class="wz-second on"]/a')),
        Rule(LinkExtractor(restrict_xpaths=r'//a[@class="next"]'), follow=True),
        Rule(LinkExtractor(allow=r'http://dl.58.com/ershoufang/\w+\.shtml.*',
                           restrict_xpaths=r'//div[@class="list-info"]/h2/a'), callback='parse_item')
    )

    def parse_item(self, response):
        i = {}
        i['raw'] = response
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        yield i


if __name__ == '__main__':
    ma = re.search(r'http://dl.58.com/ershoufang/\w+\.shtml.*',
                   'http://dl.58.com/ershoufang/34203401208754x.shtml?from=2-list-0')
    print(ma.group(0))
