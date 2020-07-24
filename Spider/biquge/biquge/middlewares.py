# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from selenium import webdriver
import time
from scrapy.http.response.html import HtmlResponse


# 使用selenium+ChromeWebserver模拟浏览器进行爬取数据
class SeleniumDownloadMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r"F:\chromedriver.exe")

    def process_request(self, request, spider):
        self.driver.get(request.url)
        time.sleep(1)
        try:
            while True:
                showMore = self.driver.find_element_by_xpath("//div[@class='page']/a[1]")
                if showMore.text() == '下页':
                    time.sleep(0.3)
                    showMore.click()
        except:
            pass
        source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=source, request=request, encoding='utf-8')
        return response
