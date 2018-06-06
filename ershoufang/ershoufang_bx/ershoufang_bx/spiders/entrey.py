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
    # allowed_domains = ['ershoufang_bx.com']
    start_urls = ['http://dalian.baixing.com']

    rules = (
        Rule(LinkExtractor(allow=r'http://dalian.baixing.com/ershoufang/.*', restrict_xpaths='//p[@class="sub-title"]/a')),
        Rule(LinkExtractor(allow=r'http://dalian.baixing.com/ershoufang/.*',
                           restrict_xpaths=r'//div[@class="area links"]/a')),
        Rule(LinkExtractor(allow=r'http://dalian.baixing.com/ershoufang/.*',
                           restrict_xpaths=r'//div[@class="subarea links"]/a')),
        Rule(LinkExtractor(allow=r'.*/?page=(\d+)', restrict_xpaths=r'//a[text()="下一页"]'),
             follow=True),
        Rule(LinkExtractor(allow=r'^http://dalian.baixing.com/ershoufang/\w+.html.*',
                           restrict_xpaths=r'//div[@class="media-body"]//a'), callback='parse_item')
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
