import random
import re

import redis
from scrapy import log

from ershoufang.ershoufang_58.ershoufang_58.agents import AGENTS
from ershoufang.ershoufang_58.ershoufang_58.proxy import PROXIES


class CustomUserAgentMiddleware(object):
    rediskey = '58_detail_page_key'
    rediscli = None

    def __init__(self):
        self.rediscli = redis.StrictRedis(host='localhost', port=6379, db=2)

    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent
        log.logger.info(request.headers['User-Agent'])
        req_url = request.url
        filler = re.search(r'http://dl.58.com/ershoufang/\d+x.*l$', req_url)
        if filler:
            statuflag = self.dedupbyredis(req_url)
            if statuflag != 0:
                strr = 'flag = %s, 这条url-%s-是重复数据...' % (statuflag, filler.group(0))
                print(strr)
                return None
        # http://dl.58.com/ershoufang/34235743315148x.shtml

    def dedupbyredis(self, url):
        # 默认没有值
        statuflag = 0
        filler = re.search(r'http://dl.58.com/ershoufang/\d+x.*l$', url)
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
