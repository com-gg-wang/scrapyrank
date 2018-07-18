import random
import re

import redis
from scrapy import log

from qichacha.agents import AGENTS
from qichacha.proxy import PROXIES
from scrapy.http import HtmlResponse


class CustomUserAgentMiddleware(object):
    rediskey = 'gj_detail_page_key'
    rediscli = None

    def __init__(self):
        self.rediscli = redis.StrictRedis(host='localhost', port=6379, db=2)

    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent
        request.cookies = {
            'Hm_lvt_8dba7bd668299d5dabbd8190f14e4d34': '1525769256',
            'ganji_uuid': '9584171745435987779108',
            'vehicle_list_view_type': '1',
            'ganji_xuuid': '26c0f8cf-9c39-4337-db09-408513abb5ba.1525769263795',
            'xxzl_deviceid': 'xsINkodhXhWOQXTNQFncO4fNQ9GiSxmtYI8KFg0op%2BvR4Z1ymfX4a6j2hxNDDHui',
            'is_fold_show_more': '1',
            '_gl_tracker': '%7B%22ca_source%22%3A%22www.baidu.com%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A52004403010%7D',
            'GANJISESSID': 'n76mutvbtrr1u4kpokt6bir3k8',
            'gj_footprint': '%5B%5B%22%5Cu4e8c%5Cu624b%5Cu623f%5Cu51fa%5Cu552e%22%2C%22http%3A%5C%2F%5C%2Fdl.ganji.com%5C%2Ffang5%5C%2F%22%5D%5D',
            'ganji_login_act': '1528266417208',
        }
        log.logger.info(request.headers['User-Agent'])

        req_url = request.url
        # http://dalian.baixing.com/ershoufang/a1396863116.html?from=regular
        filler = re.search(r'http://dl.ganji.com/\w+/\d+x.htm', req_url)
        if filler:
            statuflag = self.dedupbyredis(req_url)
            if statuflag != 0:
                strr = 'flag = %s, 这条url-%s-是重复数据...' % (statuflag, filler.group(0))
                print(strr)
                content = '<h1>...皮卡丘...</h1>'
                return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
        # http://dl.58.com/ershoufang/34235743315148x.shtml

    def dedupbyredis(self, url):
        # 默认没有值
        statuflag = 0
        filler = re.search(r'http://dl.ganji.com/\w+/\d+x.htm', url)
        if filler:
            print('我要的' + filler.group(0))
            detailpageurl = filler.group(0)
            # 有值返回1，没有返回0
            statuflag = self.rediscli.sismember(self.rediskey, detailpageurl)
            if statuflag == 0:
                self.rediscli.sadd(self.rediskey, detailpageurl)
            return statuflag


class CustomHttpProxyMiddleware(object):

    def process_request(self, request, spider):
        # TODO implement complex proxy providing algorithm
        if self.use_proxy(request):
            p = random.choice(PROXIES)
            try:
                request.meta['proxy'] = "http://%s" % p['ip_port']
            except Exception as  e:
                log.msg("Exception %s" % e, _level=log.CRITICAL)

    def use_proxy(self, request):
        """
        using direct download for depth <= 2
        using proxy with probability 0.3
        """
        if "depth" in request.meta and int(request.meta['depth']) <= 2:
            return False
        i = random.randint(1, 10)
        return i <= 2



