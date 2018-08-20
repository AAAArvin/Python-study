# -*- coding: utf-8 -*-
"""
@author: mrsong
"""
import scrapy
from JourneytoWest.items import JourneytowestItem
import os


class XyjSpider(scrapy.Spider):
    name = 'xyj'
    allowed_domains = ['shicimingju.com']
    start_urls = ['http://www.shicimingju.com/book/xiyouji/1.html']

    def parse(self, response):
        item = JourneytowestItem()
        item['chapter'] = response.css('div.www-main-container').xpath('./h1/text()').extract()[0]
        item['content'] = ""
        contentlist = response.css('div.www-main-container').xpath('./div/p/text()').extract()
        for content in contentlist:
            item['content'] += "".join(content.split())
        path = r'C:\Users\mrsong\PycharmProjects\JourneytoWest\novel\\'+item['chapter']+'.txt'
        f = os.open(path, os.O_RDWR|os.O_CREAT)
        os.write(f, item['content'].encode())
        os.close(f)
        if response.css('div.www-shadow-card').xpath('./a[last()]/span/text()').extract()[0] == '下一章':
            nexturl = response.urljoin(response.css('div.www-shadow-card').xpath('./a[last()]/@href').extract()[0])
            yield scrapy.Request(nexturl, callback=self.parse, dont_filter=True)
        yield item