# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TestspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class dianYingItem(scrapy.Item):
    name = scrapy.Field()
    mainActor = scrapy.Field()
    score = scrapy.Field()
    score_l = scrapy.Field()
    score_s = scrapy.Field()
    playCount = scrapy.Field()

class newsItem(scrapy.Item):
    newsType = scrapy.Field()
    newsTitle = scrapy.Field()
    newsIntroduction = scrapy.Field()
    newsTime = scrapy.Field()
    newsUrl = scrapy.Field()

