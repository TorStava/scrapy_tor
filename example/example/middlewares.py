# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from stem import Signal
from stem.control import Controller

class RandomUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, agents=[]):
        super(RandomUserAgentMiddleware, self).__init__()
        if not agents:
            agents = ['Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)']
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        # instance of the current class
        ua_list = []
        with open(crawler.settings.get('USER_AGENT_LIST'), 'r') as f:
            ua_list = [ua.strip() for ua in f.readlines()]

        return cls(ua_list)

    def process_request(self, request, spider):
        ua = random.choice(self.agents)
        request.headers.setdefault('User-Agent', ua)


class ProxyMiddleware(object):
    def __init__(self, http_proxy=None, tor_control_port=None, tor_password=None):
        if not http_proxy:
            raise Exception('http proxy setting should not be empty')
        if not tor_control_port:
            raise Exception('tor control port setting should not be empty')
        if not tor_password:
            raise Exception('tor password setting should not be empty')
        self.http_proxy = http_proxy
        self.tor_control_port = tor_control_port
        self.tor_password = tor_password
        self.count = 1
        self.times = 50

    @classmethod
    def from_crawler(cls, crawler):
        http_proxy = crawler.settings.get('HTTP_PROXY')
        tor_control_port = crawler.settings.get('TOR_CONTROL_PORT')
        tor_password = crawler.settings.get('TOR_PASSWORD')

        return cls(http_proxy, tor_control_port, tor_password)

    def process_request(self, request, spider):
        self.count = (self.count+1) % self.times
        if not self.count:
            # access tor ControlPort to signal tor get a new IP
            with Controller.from_port(port=self.tor_control_port) as controller:
                controller.authenticate(password=self.tor_password)
                controller.signal(Signal.NEWNYM)
        
        # scrapy support http proxy
        request.meta['proxy'] = self.http_proxy