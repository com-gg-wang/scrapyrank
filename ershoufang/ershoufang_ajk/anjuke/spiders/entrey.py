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
    start_urls = ['https://dalian.anjuke.com/sale/']

    rules = (
        Rule(LinkExtractor(allow=r'^[https://].*', restrict_xpaths=r'//div[@class="items"]//span[@class="elems-l"]/a')),
        Rule(LinkExtractor(allow=r'^[https://].*', restrict_xpaths=r'//div[@class="sub-items"]//a')),
        Rule(LinkExtractor(allow=r'^[https://].*', restrict_xpaths=r'//a[@class="aNxt"]'), follow=True),
        Rule(LinkExtractor(allow=r'^[https://].*', restrict_xpaths=r'//div[@class="house-title"]/a'),
             callback='parse_item')

    )

    def parse_item(self, response):



        i = {}
        i['raw'] = response
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        yield i
