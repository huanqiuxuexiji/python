# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class MongoDBPipeline(object):
    def __init__(self):
        connection = MongoClient(
        settings['MONGODB_SERVER'],
        settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collectionE02 = db[settings['MONGODB_COLLECTIONE02']]
        self.collectionE03 = db[settings['MONGODB_COLLECTIONE03']]

    def process_item(self, item, spider):
        vaild = True
        if not item:
            vaild = False
            # raise DropItem('Missing{0}!'.format(item))
        if vaild:
            if spider.name is 'e02':
                self.collectionE02.insert(dict(item))
            if spider.name is 'e03':
                self.collectionE03.insert(dict(item))
            log.msg('News added to MongDB database!', level = log.DEBUG, spider = spider)
        return item