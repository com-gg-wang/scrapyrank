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
    # allowed_domains = ['job_51.com']
    start_urls = ['https://www.job_51.com/']

    rules = (

        Rule(LinkExtractor(allow=r'http://dl.ganji.com/\w+/\d+x.htm',
                           restrict_xpaths=r''), callback='parse_item')
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