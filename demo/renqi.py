#!usr/bin/python
# ! _*_coding:utf-8_*_
import requests

from spiderUtils import UserAgent


class renqiSpider():

    def __init__(self):

        self.url = 'https://www.moneydj.com/InfoSvc/apis/vc'
        self.preload = '{"counts":[{"svc":"NV","guid":"85b88e0d-5f79-48ab-bcde-994a60579694"}]}'
        self.header = {
            'User-Agent': UserAgent.getUserAgent(),
            'Content-Type':'application/json'
        }

    def scrapyUrl(self):
        response = requests.post(self.url,data=self.preload,headers=self.header)
        print(response.text)

if __name__=='__main__':
    renqi = renqiSpider()
    renqi.scrapyUrl()