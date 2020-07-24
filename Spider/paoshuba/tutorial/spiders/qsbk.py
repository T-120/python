# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TutorialItem
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList


class QsbkSpider(scrapy.Spider):
    name = 'qsbk'
    allowed_domains = ['m.paoshu8.com']
    start_urls = ['http://m.paoshu8.com/sort-1-1/']
    base_domain = "https://m.paoshu8.com"

    def parse(self, response):
        bookdivs = response.xpath("//div[@class='cover']/p")
        for book in bookdivs:
            author = book.xpath("./a[@class='blue']/following-sibling::a[1]/text()").get().strip()
            bookName = book.xpath("./a[@class='blue']/text()").get()
            bookName = "".join(bookName).strip()
            item = TutorialItem(author=author, bookName=bookName)
            yield item
        nextUrl = response.xpath("//div[@class='page']/a[contains(string(), '下页')]/@href").get()
        if not nextUrl:
            return
        else:
            yield scrapy.Request(self.base_domain + nextUrl, callback=self.parse)
