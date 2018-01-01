# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from testSpider import settings


class TestspiderPipeline(object):
    def __init__(self):
        self.pymongo = pymongo.MongoClient()
        self.db = self.pymongo[settings.DATA_BASE_NAME]
        self.table = self.db[settings.TABLE_NAME]
        self.table.remove()
        if settings.SPIDER_TYPE == 'MOVIE':
            self.table.create_index('name',unique=True)



    def process_item(self, item, spider):
        print('process_item')
        if settings.SPIDER_TYPE == 'NEWS':
            return self.process_news(item ,spider)
        elif settings.SPIDER_TYPE == 'MOVIE':
            return self.process_movies( item, spider)



    def process_news(self,item ,spider):
        ''' 处理新闻信息 '''
        if item['newsType'] != None:
            self.table = self.db[item['newsType']]
        else:
            item['newsType'] = self.table.name
            self.table.insert(dict(item))
        return item


    def process_movies(self, item, spider):
        ''' 处理电影信息 '''
        item['score'] = item['score_l'] + item['score_s']
        if self.table.find_one({'name':item['name']}) == None:
            self.table.insert(dict(item))
        return item