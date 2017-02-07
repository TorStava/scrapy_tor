# -*- coding: utf-8 -*-
import scrapy

class ShowIpSpider(scrapy.Spider):
    name = "showip"
    #start_urls = ['http://icanhazip.com']
    url = 'http://icanhazip.com'

    def start_requests(self):
    	for i in range(200):
    		yield scrapy.Request(self.url, callback=self.parse, dont_filter=True)

    def parse(self, response):
    	self.logger.info(response.body)
    	print(response.body)
