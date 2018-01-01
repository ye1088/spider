#!usr/bin/python
# ! _*_coding:utf-8_*_
import json

import js2xml
import scrapy.selector as Selector
import requests

from spiderUtils import UserAgent

headers = {
    'User-Agent':UserAgent.getUserAgent()

}


def huabanSpider(dstUrl):

    res = requests.get(dstUrl,headers=headers)
    print(res.status_code)
    # print(res.text)
    html_lines = res.text.split('\n')
    for line in html_lines :
        if 'app.page["pins"]' in line :
            print('i am in ')
            xml_js = js2xml.parse(line)
            # print(str(xml_js))
            # print(js2xml.pretty_print(xml_js))
            sel = Selector.Selector(text=js2xml.pretty_print(xml_js))
            print(sel.xpath('//*/property[@name="pin_id"]/number/@value').extract())
            break


if __name__=='__main__':
    url = "http://huaban.com/favorite/beauty/"
    huabanSpider(url)