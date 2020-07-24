# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from biquge.items import BiqugeItem


class BqgSpider(CrawlSpider):
    name = 'bqg'
    allowed_domains = ['m.paoshu8.com']
    start_urls = ['http://m.paoshu8.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/sort-\d+-\d+/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # 爬取列表页全部的书名，作者，链接，保存为列表
        booknames = response.xpath("//div[@class='cover']//a[@class='blue']//text()").getall()
        authors = response.xpath(
            "//div[@class='cover']//a[@class='blue']/following-sibling::a[1]//text()").getall()
        book_urls = response.xpath("//div[@class='cover']//a[@class='blue']/@href").getall()

        # 遍历列表中的值，绑定为一个个item对象并返回给pipeline进行数据库操作
        for i in range(len(booknames)):
            bookname = booknames[i]
            author = authors[i]
            book_url = 'http://m.paoshu8.com' + book_urls[i]

            item = BiqugeItem(
                bookname=bookname,
                author=author,
                book_url=book_url
            )
            yield item
