# -*- coding: utf-8 -*-
import scrapy


class SfwSpider(scrapy.Spider):
    name = 'sfw'
    allowed_domains = ['https://www.fang.com/SoufunFamily.htm']
    start_urls = ['https://www.fang.com/SoufunFamily.htm/']

    def parse(self, response):
        tr_list = response.xpath('//div[@id="c02"]//tr')
        province_text = ''
        # 去除国外的城市
        for tr in tr_list[0:55]:
            province = tr.xpath('./td[2]//text()').extract_first().strip('\xa0')
            # 给没有省份的市，添加省份
            if province:
                province_text = province
            else:
                province = province_text
            a_list = tr.xpath('./td[3]/a')

            # city_list = tr.xpath('./td[3]/a/text()').extract()

            # for city in city_list:
            #  print(province, city)
