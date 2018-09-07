# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mzt.items import MztItem


class MeizituSpider(CrawlSpider):
    name = 'meizitu'
    allowed_domains = ['mzitu.com']
    start_urls = ['http://mzitu.com/']
    img_urls = []
    rules = (Rule(LinkExtractor(allow=('http://www.mzitu.com/\d{1,6}'), deny=('http://www.mzitu.com/\d{1,6}/\d{1,6}')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = MztItem()
        max_num = response.xpath("descendant::div[@class='main']/div[@class='content']/div[@class='pagenavi']/a[last()-1]/span/text()").extract_first(default="N/A")
        item['name'] = response.xpath("./*//div[@class='main']/div[1]/h2/text()").extract_first(default="N/A")
        item['url'] = response.url
        for num in range(1, int(max_num)):
            # page_url 为每张图片所在的页面地址
            page_url = response.url + '/' + str(num)
            yield scrapy.Request(page_url, callback=self.img_url)
        item['image_urls'] = self.img_urls
        yield item


    def img_url(self, response,):
        """取出图片URL 并添加进self.img_urls列表中
        :param response:
        :param img_url 为每张图片的真实地址
        """
        img_urls = response.xpath("descendant::div[@class='main-image']/descendant::img/@src").extract()
        for img_url in img_urls:
            self.img_urls.append(img_url)