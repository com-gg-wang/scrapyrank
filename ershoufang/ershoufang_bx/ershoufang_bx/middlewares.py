import random
import re

import redis
from scrapy import log

from ershoufang_bx.agents import AGENTS, AGENTS_ALL
from ershoufang_bx.proxy import PROXIES


class CustomUserAgentMiddleware(object):
    rediskey = 'bx_detail_page_key'
    rediscli = None

    def __init__(self):
        self.rediscli = redis.StrictRedis(host='localhost', port=6379, db=2)

    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent
        request.headers['Host'] = 'dalian.baixing.com'

        log.logger.info(request.headers['User-Agent'])
        request.cookies = {
            '__admx_track_id': 'L9jCsT2C85ZwGNtx1eE9IQ',
            '__admx_track_id.sig': 'pvSyLQCDCvnh-Lzcx4LXogrtA7Y',
            '__trackId': '152808293377183',
            '__city': 'dalian',
            '_ga': 'GA1.2.1305236063.1528082935',
            '_gid': 'GA1.2.1824866696.1528082935',
            '__s': '37ph9vf2viivnl8bh87mfj69l0',
            '_auth_redirect': 'http%3A%2F%2Fdalian.baixing.com%2Fershoufang%2F',
            'Hm_lvt_5a727f1b4acc5725516637e03b07d3d2': '1528082935,1528086030,1528095509,1528095911',
            '__sense_session_pv': '12',
            'Hm_lpvt_5a727f1b4acc5725516637e03b07d3d2': '1528097607',
        }
        req_url = request.url
        # http://dalian.baixing.com/ershoufang/a1396863116.html?from=regular
        filler = re.search(r'^http://dalian.baixing.com/ershoufang/\w+.html', req_url)
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
        filler = re.search(r'^http://dalian.baixing.com/ershoufang/\w+.html', url)
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
