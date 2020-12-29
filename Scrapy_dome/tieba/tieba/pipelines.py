# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib import request
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
class TiebaPipeline(object):
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "imgs")
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def process_item(self, item, spider):
        urls=item['image_urls']#需使用item中的值
        for url in urls:
            img_name=url.split("/")[-1]
            request.urlretrieve(url,os.path.join(self.path,img_name))
        return item

