import random
import re

import redis
from scrapy import log

from anjuke.agents import AGENTS_ALL, AGENTS
from anjuke.proxy import PROXIES
from scrapy.http import HtmlResponse


class CustomUserAgentMiddleware(object):
    rediskey = 'anjuke_ershoufang_detailpage'
    rediscli = None

    def __init__(self):
        self.rediscli = redis.StrictRedis(host='localhost', port=6379, db=2)

    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent

        log.logger.info(request.headers['User-Agent'])

        # request.cookies = random.choice(COOKIES)
        req_url = request.url
        # http://dalian.baixing.com/ershoufang/a1396863116.html?from=regular
        filler = re.search(r'^https://dalian.anjuke.com/\w+/view/A\d+', req_url)
        if filler:
            statuflag = self.dedupbyredis(req_url)
            if statuflag != 0:
                strr = 'flag = %s, 这条url-%s-是重复数据...' % (statuflag, filler.group(0))
                print(strr)
                content = '<h1>...打个球吧！...</h1>'
                return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)

    def dedupbyredis(self, url):
        # 默认没有值
        statuflag = 0
        filler = re.search(r'^https://dalian.anjuke.com/\w+/view/A\d+', url)
        if filler:
            detailpageurl = filler.group(0)
            # 有值返回1，没有返回0
            statuflag = self.rediscli.sismember(self.rediskey, detailpageurl)
            if statuflag == 0:
                self.rediscli.sadd(self.rediskey, detailpageurl)
                print('url-%s-进入redis' % detailpageurl)
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
