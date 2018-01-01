#!usr/bin/python
# ! _*_coding:utf-8_*_
import os

import requests
import time
from lxml import etree


class tieziImg():

    def __init__(self):
        self.saveApkDir = r'D:\tmp\1223'
        self.start_url = 'https://tieba.baidu.com/p/5361645967?pn={}'#https://tieba.baidu.com/p/5356540826??pn={}
        self.page = 1
        self.gameName = ''
        # 他可能会校验你的来源页面,也就是你访问下一个页面时候的上一个页面的url,所以这里要设置下
        self.prePage = 'http://www.vqs.com/crack/'
        self.headers = {
            # 'authorization':'Bearer MS4xVGM0NEJBQUFBQUFYQUFBQVlRSlZUZWVZOTFxOWIybklNd2VkalhUWG9YT2JjSnBrQXNZcnd3PT0=|1510623975|3b616fd23adb09cad90dcc742a4b22353e321efc',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
            # 'Referer': self.prePage,
        }

    def startSpide(self):
        print("zhixingle ")
        while self.page < 2:
            response = requests.get(self.start_url.format(self.page),headers = self.headers)
            # print(response.text)
            selector = etree.HTML(response.text)
            sel = selector.xpath('//*/img/@src')
            for imgUrl in sel:
                try:
                    with open(self.saveApkDir + os.sep + str(imgUrl).split('/')[-1],'wb') as f:

                        response = requests.get(imgUrl,headers= self.headers)
                        f.write(response.content)
                        time.sleep(1)
                except:
                    print(imgUrl)
            self.page += 1
            print("正在爬取第 %d 页" %self.page)

if __name__=='__main__':
    tiezi = tieziImg()

    tiezi.startSpide()
