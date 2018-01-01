# -*- coding: utf-8 -*-
import scrapy
import sys

import time

from spiderUtils import UserAgent


sys.path.append("..")
# import items.dianYingItem as dianYingItem
import testSpider.items as items
from lxml.html import etree


class DianYingSpider(scrapy.Spider):

    name = 'dianying'
    start_urls = [
        'https://v.qq.com/x/list/movie'
    ]

    def __init__(self):
        self.offset = 0
        self.UA = UserAgent.getUserAgent()
        self.headers = {
            'User-Agent': self.UA
        }






    def parse(self, response):
        suffixUrl = 'https://v.qq.com/x/list/movie?&offset={}'
        # r = scrapy.http(suffixUrl.format(self.offset), headers=self.headers)
        # print(r.body)
        film_lists = response.xpath("//*/div[@class='site_container container_main']/div[@class='container_inner']"
                       "/div[@class='wrapper']/div[@class='mod_figures_wrapper']/div[@class='mod_bd']"
                       "/div[@class='mod_figures mod_figure_v']/ul[@class='figures_list']/li")
        item = items.dianYingItem()
        canReturn = False
        for film_list in film_lists.extract():
            singleFile = etree.HTML(film_list)
            film_names = singleFile.xpath("//div[@class='figure_title_score']/strong/a/text()")
            actor_names = singleFile.xpath("//div[@class='figure_desc']/a/text()")
            playCount = singleFile.xpath("//div[@class='figure_count']/span[@class='num']/text()")
            score_l = singleFile.xpath("//div[@class='figure_title_score']/div[@class='figure_score']"
                                       "/em[@class='score_l']/text()")
            score_s = singleFile.xpath("//div[@class='figure_title_score']/div[@class='figure_score']"
                                       "/em[@class='score_s']/text()")
            # index = 0

            # while index < len(film_names):
            try:

                item['name'] = film_names[0]#[index]
                item['playCount'] = playCount[0]#[index]
                try:
                    item['mainActor'] = actor_names[0]#[index]
                except Exception as e:
                    print(e)
                    item['mainActor'] = "动漫或其他"
                item['score_l'] = score_l[0]
                item['score_s'] = score_s[0]#[index]+score_s[index]
                yield item
            except Exception as e:
                print(e)
                canReturn = True
            if item['name'] == None:
                canReturn = True


        if not canReturn:
            yield self.nextPage(response)



        # item['name']  = film_list.xpath('//a/text()')
        # # item.score = ''
        # # item.playCount = ''
        # # item.mainActor = ''
        # yield item

    def nextPage(self,response):
        time.sleep(4)
        req = []
        suffixUrl = 'https://v.qq.com/x/list/movie?&offset={}'
        self.offset += 30
        r = scrapy.http.Request(suffixUrl.format(self.offset),callback=self.parse)
        # r = response.follow('?&offset={}'.format(self.offset),callback=self.parse)
        # r = scrapy.http(suffixUrl.format(self.offset),callback=self.parse)
        # print(r.body)
        return r


class NewsSpider(scrapy.Spider):
    name = 'news'
    start_urls = [
        'http://rss.qq.com/news.htm'
    ]
    def parse(self, response):
        item = items.newsItem()
        sel = scrapy.Selector(response)
        all_msg = sel.xpath('//*[@id="channel"]/h4')
        index = 0
        for single_msg in all_msg:
            newsType = single_msg.xpath('./span[@id="titile1"]/a/text()').extract()[0]
            newsType_url = single_msg.xpath('./span[@id="xml1"]/a/@href').extract()[0]
            print(newsType)
            print(newsType_url)
            item['newsType'] = newsType
            if index < 3:
                yield item
                time.sleep(4)

                yield scrapy.http.Request(newsType_url,callback=self.newsListParse)

            index +=1

    def newsListParse(self,response):
        print("newsListParse")
        # print(response.url)
        sel = scrapy.Selector(response)
        # print(response.body.decode(response.encoding))
        all_msg = sel.xpath('//*/item')
        newsItem = items.newsItem()
        for msg in all_msg:
            newsItem['newsTitle'] = msg.xpath('./title/text()').extract()[0]
            newsItem['newsUrl'] = msg.xpath('./link/text()').extract()[0]
            newsItem['newsIntroduction'] = msg.xpath('./description/text()').extract()[0]
            newsItem['newsTime'] = msg.xpath('./pubDate/text()').extract()[0]
            # newsItem['newsType'] = None
            # print(newsTitle)
            yield newsItem
        # print(response.body)

