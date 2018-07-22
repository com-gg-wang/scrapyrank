# -*- coding: utf-8 -*-
import re

import pymysql
import requests
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import urllib

class EntreySpider(CrawlSpider):
    name = 'entrey'
    # allowed_domains = ['baidu.com']
    # start_urls = [
    #     'https://www.baidu.com/s?tn=baidu&wd=%E4%BC%97%E7%9B%8A%E5%A4%A9%E6%88%90%E5%A4%A9%E7%9C%BC%E6%9F%A5']

    def start_requests(self):
        # db = pymysql.connect(host='192.168.1.214', port=4000, user='dbuser', passwd='dbuserDev123', db='spiderData',
        #                      use_unicode='true', charset='utf8')
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Dream96*', db='spider',
                             use_unicode='true', charset='utf8')
        cursor = db.cursor()

        # cursor.execute('select company_name from company_name limit 3 ')
        cursor.execute('select company_n from company ')
        fetchall = cursor.fetchall()
        print(fetchall)
        urls = []
        for s in fetchall:
            print(s)
            s = str(s)+ '天眼查'
            quote = urllib.quote(s)

            a = 'https://www.baidu.com/s?tn=baidu&wd=%s' % quote
            print(a)
            request = scrapy.Request(a
                                     , callback=self.parse_item)
            print()
            yield request
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[text()="下一页>"]'), follow=True,callback='parse_item'),
        Rule(LinkExtractor(allow=r'.*', restrict_xpaths=r'//a[text()="百度快照"]'), callback='parse_item'),
    )

    def parse_item(self, response):
        i = {}
        i['raw'] = response.text
        # print(i['raw'])

        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        yield i



if __name__ == '__main__':
    a = "https://www.baidu.com/s?ie=utf-8&mod=1&isbd=1&isid=9b5ce9590001e776&ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E4%BC%97%E7%9B%8A%E5%A4%A9%E6%88%90&oq=%25E4%25BC%2597%25E7%259B%258A%25E5%25A4%25A9%25E6%2588%2590&rsv_pq=9b5ce9590001e776&rsv_t=0e523BNDP0TaLVbKRLBML6S0Ch1yeO1HIFqpmB2nF8mXljwTyir8T3CrCCU&rqlang=cn&rsv_enter=0&bs=%E4%BC%97%E7%9B%8A%E5%A4%A9%E6%88%90&rsv_sid=1433_21081_18560_22157&_ss=1&clist=eb7b925aa27799da&hsug=&f4s=1&csor=4&_cr1=30132"
    header = {
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        # 'Cache-Control': 'max-age=0',
        # 'Connection': 'keep-alive',
        # 'Cookie': 'BIDUPSID=CD1081D7AC10CC90B77EF363C482EEB6; PSTM=1512889754; MCITY=-167%3A; BD_UPN=123253; BAIDUID=98147D945FDC537EF7C0BC161347C9CA:FG=1; pgv_pvi=3370341376; BD_HOME=0; H_PS_PSSID=1433_21081_18560_22157; BD_CK_SAM=1; PSINO=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_645EC=e7f2jnSSzeTWQ0QsqMengQ6eTmjkAxdrHv2LfazwLIC8eDmlUcKbdtDXC3Y; BDSVRTM=0',
        # 'Host': 'www.baidu.com',
        # 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    response = requests.get(a, headers=header)
    print(response.text)
