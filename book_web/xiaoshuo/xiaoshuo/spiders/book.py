# -*- coding: utf-8 -*-
import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['qidian.com']
    start_urls = ['https://www.qidian.com/finish?chanId=21']

    def parse(self, response):
        book_box = response.xpath('.//div[@class="book-mid-info"]')
        for list in book_box:
            book_url = list.xpath('h4/a/@herf').extract_first()
            book_name = list.xpath('h4/a/text()').extract_first()
            print(book_name,":",book_url)

        # for i in book_name,book_url:
        # print(book_name,":",book_url)
        pass
