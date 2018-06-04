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
    # allowed_domains = ['ershoufang_gj.com']
    start_urls = ['http://dl.ganji.com/fang5/']

    rules = (
        Rule(LinkExtractor(allow=r'http://dl.ganji.com/fang5/\w+/',
                           restrict_xpaths=r'//ul[@class="f-clear"]//a')),
        Rule(LinkExtractor(allow=r'http://dl.ganji.com/\w+/\w+/',
                           restrict_xpaths=r'//div[@class="fou-list f-clear"]/a')),
        Rule(LinkExtractor(allow=r'.*o\d+/', restrict_xpaths=r'//a[@class="next"]'),
             follow=True),
        Rule(LinkExtractor(allow=r'http://dl.ganji.com/\w+/\d+x.htm',
                           restrict_xpaths=r'//div[@class="f-list-item ershoufang-list"]//dd[@class="dd-item title"]/a'), callback='parse_item')
    )

    def parse_item(self, response):
        i = {}
        i['raw'] = response
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        yield i


if __name__ == '__main__':
    ma = re.search(r'^http://dalian.baixing.com/ershoufang/\w+.html.*',
                   'http://dalian.baixing.com/ershoufang/a1399275053.html?from=regular')
    print(ma.group(0))
