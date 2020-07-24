# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu_spider.items import ArticleItem


class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='_1RuRku']/text()").get()
        avatar = response.xpath("//a[@class='_1OhGeD']/img/@src").get()
        author = response.xpath("//span[@class='FxYr8x']/a/text()").get()
        pub_time = response.xpath("//div[@class='s-dsoj']/time/text()").get()
        url = response.url
        url1 = url.split("?")[0]
        article_id = url1.split('/')[-1]
        content = response.xpath("//article[@class='_2rhmJa']").get()

        word_count = response.xpath("//span[@class='_3tCVn5']/following-sibling::span[1]/text()").get()
        read_count = response.xpath("//span[@class='_3tCVn5']/following-sibling::span[2]/text()").get()
        subjects = ",".join(response.xpath("//div[@class='_2Nttfz']/a/span/text()").getall())

        item = ArticleItem(title=title,
                           avatar=avatar,
                           author=author,
                           pub_time=pub_time,
                           origin_url=response.url,
                           article_id=article_id,
                           content=content,
                           word_count=word_count,
                           read_count=read_count,
                           subjects=subjects
                           )
        yield item
