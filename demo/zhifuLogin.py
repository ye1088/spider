#!usr/bin/python
# ! _*_coding:utf-8_*_

import requests
from lxml import etree

from spiderUtils import UserAgent


class zhihuLogin():

    def __init__(self):

        self.headers = {
            # 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Accept-Encoding':'gzip, deflate, br',
            # 'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            # 'Connection':'keep-alive',
            'User-Agent':UserAgent.getUserAgent(),
            'Upgrade-Insecure-Requests':'1',
            'Cookie':'aliyungf_tc=AQAAAEuJbCwfeQgA3x73drZbNtVsXT9I; q_c1=ee4eb5edc855470fb8cb788ab3e6f0fb|1513518299000|1513518299000; _xsrf=9fc177df23ef4a52053a1dae98ca7e28; d_c0="AHACCspB2QyPTvtNtM76XH9VkGkfjrjHALE=|1513518299"; _zap=cbb783b4-7b6c-435c-ac1e-2e6ddcf69109; r_cap_id="NjkyZTI3Njc1NGM1NDFiOTg1OWY4YTJhNDRkNjVjNmE=|1513519012|b12ce55af951123030c9d47e07ccd1ac627cdca4"; cap_id="YmU5ODRlNTNkNGU1NGM1MDhhYWU4MTU3NzA2ZTVmY2E=|1513519012|b068c5ff59c0cdeb586b40603f6c389296d07c33"; _xsrf=9fc177df23ef4a52053a1dae98ca7e28; __utma=51854390.859663220.1513518299.1513518299.1513518299.1; __utmc=51854390; __utmz=51854390.1513518299.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.000--|3=entry_date=20171217=1'
        }

        self.param = {

            '_xsrf':'9fc177df23ef4a52053a1dae98ca7e28',
            'password':'wzsye1088',
            'Host':'www.zhihu.com',
            # 'captcha_type':'cn',
            'phone_num':'18631616220'
        }


    def getXsrf(self):
        response = self.getResponse("https://www.zhihu.com/#signin")
        sel = etree.HTML(response.content)
        print(response.content.decode(response.encoding))
        _xsrf = sel.xpath('//*/input[@name="_xsrf"]/@value')[0]
        print(_xsrf)
        pass

    def getResponse(self,url):

        return requests.get(url,headers=self.headers)

    def login(self,url,_xsrf,headers):
        self.param['_xsrf'] = _xsrf
        response = requests.post(url,data=self.param,headers = headers )
        print(response.content.decode(response.encoding))
        print(response.status_code)



if __name__ == '__main__':
    zhihu = zhihuLogin()
    _xsrf = zhihu.getXsrf()
    headers = zhihu.headers
    # headers['X-Xsrftoken'] = _xsrf

    zhihu.login('https://www.zhihu.com/login/phone_num',headers,_xsrf)