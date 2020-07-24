# -*- coding: utf-8 -*-
import scrapy


class QsbkSpider(scrapy.Spider):
    name = 'qsbk'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['http://www.qiushibaike.com/']

    def parse(self, response):
        pass
