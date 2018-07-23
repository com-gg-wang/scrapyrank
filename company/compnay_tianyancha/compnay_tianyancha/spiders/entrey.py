# -*- coding: utf-8 -*-
import re

import pymysql
import requests
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import urllib.request


class EntreySpider(CrawlSpider):
    name = 'entrey'
    # https://www.baidu.com/s?tn=baidu&wd=%E5%B9%B3%E5%AE%89%E6%99%AE%E6%83%A0%E6%8A%95%E8%B5%84%E5%92%A8%E8%AF%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E8%8B%8F%E5%B7%9E%E6%96%87%E5%88%9B%E5%A4%A7%E5%8E%A6%E5%88%86%E5%85%AC%E5%8F%B8%E5%A4%A9%E7%9C%BC%E6%9F%A5
    # allowed_domains = ['baidu.com']
    # start_urls = [
    #     'https://www.baidu.com/s?tn=baidu&wd=%E5%B9%B3%E5%AE%89%E6%99%AE%E6%83%A0%E6%8A%95%E8%B5%84%E5%92%A8%E8%AF%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E8%8B%8F%E5%B7%9E%E6%96%87%E5%88%9B%E5%A4%A7%E5%8E%A6%E5%88%86%E5%85%AC%E5%8F%B8%E5%A4%A9%E7%9C%BC%E6%9F%A5']

    def start_requests(self):
        db = pymysql.connect(host='192.168.1.214', port=4000, user='dbuser', passwd='dbuserDev123', db='spiderData',
                              use_unicode='true', charset='utf8')
        #db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Dream96*', db='spider',
                             #use_unicode='true', charset='utf8')
        cursor = db.cursor()

        cursor.execute('select company_name from company_name limit 5 ')
        #cursor.execute('select company_n from company ')
        fetchall = cursor.fetchall()
        print(fetchall)
        urls = []
        for s in fetchall:
            s = re.findall('[\u4e00-\u9fa5]+',str(s))[0]+ '天眼查'
            #quote = urllib.quote(s)
            print(s)
            a = 'https://www.baidu.com/s?tn=baidu&wd=%s' % s

            print(a)

            request = scrapy.Request(a
                                     , callback=self.parse_item)
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
    a = "https://www.baidu.com/s?wd=%E5%B9%B3%E5%AE%89%E6%99%AE%E6%83%A0%E6%8A%95%E8%B5%84%E5%92%A8%E8%AF%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E8%8B%8F%E5%B7%9E%E6%96%87%E5%88%9B%E5%A4%A7%E5%8E%A6%E5%88%86%E5%85%AC%E5%8F%B8%E5%A4%A9%E7%9C%BC%E6%9F%A5"
    header = {
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        # 'Cache-Control': 'max-age=0',
        # 'Connection': 'keep-alive',
        # 'Cookie': 'BIDUPSID=CD1081D7AC10CC90B77EF363C482EEB6; PSTM=1512889754; MCITY=-167%3A; BD_UPN=123253; BAIDUID=98147D945FDC537EF7C0BC161347C9CA:FG=1; pgv_pvi=3370341376; BD_HOME=0; H_PS_PSSID=1433_21081_18560_22157; BD_CK_SAM=1; PSINO=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_645EC=e7f2jnSSzeTWQ0QsqMengQ6eTmjkAxdrHv2LfazwLIC8eDmlUcKbdtDXC3Y; BDSVRTM=0',
        # 'Host': 'www.baidu.com',
        # 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    response = requests.get(a, headers=header)
    print(response.text)
