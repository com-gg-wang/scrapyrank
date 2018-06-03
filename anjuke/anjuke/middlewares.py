import random
import re

import redis
from scrapy import log

from anjuke.agents import AGENTS_ALL, AGENTS
from anjuke.proxy import PROXIES


class CustomUserAgentMiddleware(object):
    rediscli = None

    def __init__(self):
        self.rediscli = redis.StrictRedis(host='localhost', port=6379, db=0)

    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent
        log.logger.info(request.headers['User-Agent'])
        req_url = request.url
        print(req_url)
        rediskey = re.search(r'', req_url)
        if rediskey:
            pass
            # filepath = re.search(r'', rediskey(0))
            # self.rediscli.smembers(rediskey, filepath)


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
