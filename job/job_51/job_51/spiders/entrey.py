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
    start_urls = ['https://jobs.51job.com/all/']

    rules = (

        Rule(LinkExtractor(
            allow=r'https://jobs.51job.com/\w+', restrict_xpaths=r'//div[@class="lkst"]//a'
        )),
        Rule(LinkExtractor(
            allow=r'https://jobs.51job.com/\w+', restrict_xpaths=r'//div[@class="lkst close"]//a'
        )),
        Rule(LinkExtractor(
            allow=r'https://jobs.51job.com/\w+', restrict_xpaths=r'//li[@class="bk"]//a'
        ), follow=True, callback='parse_item')
    )

    def parse_item(self, response):
        # e = job_51Item()
        i = {}
        i['company_name'] = response.xpath(
            r'//div[@class="detlist gbox"]//div[@class="e "]/p[@class="info"]/a/text()').extract()
        # e.company_name = response.xpath(r'//div[@class="detlist gbox"]//div[@class="e "]/p[@class="info"]/a/@title').extract()[0]
        # i['raw'] = response
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        yield i


if __name__ == '__main__':
    ma = re.search('http://dl.ganji.com/\w+/\d+x.htm', 'http://dl.ganji.com/fang5/3293904744x.htm')
    print(ma.group(0))
