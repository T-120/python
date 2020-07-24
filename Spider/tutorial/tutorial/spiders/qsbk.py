# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TutorialItem
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList


class QsbkSpider(scrapy.Spider):
    name = 'qsbk'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']
    base_domain = "https://www.qiushibaike.com"

    def parse(self, response):
        duanzi_divs = response.xpath("//div[@class='col1 old-style-col1']/div")
        for duanzi in duanzi_divs:
            author = duanzi.xpath(".//h2/text()").get().strip()
            content = duanzi.xpath(".//div[@class='content']//text()").getall()
            content = "".join(content).strip()
            item = TutorialItem(author=author, content=content)
            yield item
        nextUrl = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        if not nextUrl:
            return
        else:
            yield scrapy.Request(self.base_domain + nextUrl, callback=self.parse)
