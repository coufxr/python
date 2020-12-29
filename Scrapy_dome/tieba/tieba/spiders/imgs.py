# -*- coding: utf-8 -*-
import scrapy
import re
from tieba.tieba.items import TiebaItem


class ImgsSpider(scrapy.Spider):
    name = 'imgs'
    allowed_domains = ['tieba.baidu.com']  # 限定域名
    start_urls = ["https://tieba.baidu.com/p/3430697608/pn=1"]


    def parse(self, response):
        #获取全部图片链接
        srcs = response.xpath('.//img[@class="BDE_Image"]/@src').getall()
        # for src in srcs:
        #     print(src)
        itmes = TiebaItem(image_urls=srcs)
        yield itmes
        #下一页
        url = response.xpath('//li[@class="l_pager pager_theme_4 pb_list_pager"]/a/@href')[-2].extract()
        # print(url)
        if url:
            next_page = 'https://tieba.baidu.com' + url  # 拼接url
            # print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

