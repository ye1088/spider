#!usr/bin/python
# ! _*_coding:utf-8_*_


import requests
import time
from lxml import etree
import spiderUtils.UserAgent as ua
from pymongo import MongoClient
import spiderUtils.ProxyUtils as ProxyUtils
import random

from spiderUtils import Utils


class CaoLiu:
    def __init__(self):

        self.main_url = 'http://cl.moqy.pw'
        self.backup_main_url = 'http://www.t66y.com/'# 备用的官方网址

        self.index_url = 'index.php'
        self.ipIndex = 0 # 代理ip列表的索引

        # 获取代理ip列表
        self.proxyUtils = ProxyUtils.ProxyUtil()
        self.httpProxyIps = self.proxyUtils.getProxyIpsFromFile(True)
        self.httpsProxyIps = self.proxyUtils.getProxyIpsFromFile(False)

        self.utils = Utils.Utils()

        self.pageLimit = 20 # 最多爬取几页
        self.curHeader = {
                'User-Agent':ua.getUserAgent(),
            }
        self.client = MongoClient()
        self.caoLiuDB = self.client.cao_liu
        self.caoLiuTable = self.caoLiuDB.caoLiuTable

    def dealExtraInfo1(self,info1,info2):
        '''
        处理多出来的数据信息，将多出来的东西删掉(这里是总的，细节有分支方法处理)
        :param info1: 等待比较的信息1
        :param info2: 等待比较的信息2
        :return:
        '''
        info1_len = len(info1)
        info2_len = len(info2)
        if info1_len == info2:
            return info1,info2
        elif info1_len   > info2_len:
            return self.dealExtraInfo2(info1,info1_len-info2_len),info2
        else:
            return info1,self.dealExtraInfo2(info2, info2_len - info1_len)
    def dealExtraInfo2(self,info,defLen):
        '''
        处理多出来的数据信息，将多出来的东西删掉(这里是处理细节的)
        这里 info1 的长度大于 info2的长度
        :param info: 要处理的信息
        :param defLen: 两个信息相差的长度
        :return:
        '''
        popIndex = 0
        while popIndex < defLen:
            info.pop(0)
            popIndex += 1
        return info


    def getResponse(self,urlPath):
        '''
        获取某网页的response，好处是访问失败后，可以重新再访问
        :param urlPath:
        :return:
        '''

        recordProxy = self.httpProxyIps[self.ipIndex]

        self.utils.printError('proxy ip : '+recordProxy)
        try:
            response = requests.get(urlPath, headers=self.curHeader,
                                    proxies={
                                        'http': recordProxy,
                                        'https': self.httpsProxyIps[self.ipIndex]
                                    },timeout=10)
            self.ipIndexIncrease(len(self.httpProxyIps))
        except Exception as e:
            self.utils.printError(e)
            if self.utils.testNetOK():
                self.httpProxyIps, self.httpsProxyIps = self.proxyUtils.popUnuseIp(self.httpProxyIps,
                                                                                   self.httpsProxyIps, self.ipIndex)
            return self.getResponse(urlPath)
        return response

    def ipIndexIncrease(self,maxIpLen):
        '''
        代理ip的索引+1
        :param maxIpLen: 代理ip池的大小
        :return:
        '''
        self.ipIndex += 1
        if self.ipIndex >= maxIpLen:
            self.ipIndex = 0


    def print_find_src(self,urlPath, keyWord):

        '''
        针对草榴多个模块，多页爬取资源
        :param urlPath:每个模块的网址
        :param keyWord:要爬取资源包含的关键词
        # :param enterType:爬取页面入口的类型（首页的那几个入口，不一样的入口，页面分析的数据也不一样）
            ’‘
        :return:
        '''
        page = 1
        while True:
            if page > self.pageLimit:
                break
            print('正在爬取第%d页\n'%page)

            response = self.getResponse(urlPath + '&page=%d' % page)

            # print(response.content)
            xparse = etree.HTML(response.content)
            #/tbody/tr[@class="tr3 t_one tac"]/td[@class="tal"]/h3/a/@href
            # unUse_url = xparse.xpath('//div[@class="t"]/table[@id="ajaxtable"]/tbody/tr[@class="tr3 t_one tac"]/td[@class="tal"]/h3/a[@id=""]/*/font/text()')
            src_url = xparse.xpath('//*[@id="ajaxtable"]/tbody/tr/td[2]/h3/a/@href')
            src_name = xparse.xpath('//*[@id="ajaxtable"]/tbody/tr/td[2]/h3/a/text()')
            src_url_index = 0
            # print(src_url)
            # print('\n\n\n\n\n')
            # print(src_name)
            # print("unuse url len : "+ str(len(unUse_url)))
            src_url, src_name = self.dealExtraInfo1(src_url,src_name)
            # print(src_url)
            # print('\n\n\n\n\n')
            # print(src_name)
            # print("src url len : "+ str(len(src_url)))
            # print("src name len : "+ str(len(src_name)))
            dict_data = {
                'dataName':[],
                'dataUrl':[],
                'standbyUrl':[],
                'keyWord':keyWord
            }


            for single_title in src_name:
                if keyWord in single_title:
                    # pass
                    dict_data['dataName'].append(single_title)
                    dict_data['dataUrl'].append(self.main_url+'/'+src_url[src_url_index])
                    print('\n'+single_title+"\n"+self.main_url+'/'+src_url[src_url_index]+'\n')
                    # 上面那个有点问题，如果上面提出的网址不对的话就用下面的备用网址
                    if src_url_index-1>=0:
                        dict_data['standbyUrl'].append(self.main_url+'/'+src_url[src_url_index-1])
                        # print('backup url : '+self.main_url+'/'+src_url[src_url_index-1]+'\n')
                    else:
                        dict_data['standbyUrl'].append("")
                        # print('backup url : ')
                src_url_index += 1
            if len(dict_data['dataName']) > 0:
                self.caoLiuTable.insert(dict_data)
            # time.sleep(5)   # 设置延时
            page += 1



    def getKeyWordSrc(self,keyWord,srcType='all'):
        '''
        根据关键词爬取草榴上的资源（文章，图片，视频）
        :param keyWord: 要查找的资源所包含的关键词
        :param srcType:资源类型
            'all'   : 所有的
            'video' : 视频
            'artical'   : 文章
            'img'   : 图片
        :return:
        '''
        authorityEnter = ['亞洲無碼原創區', '亞洲有碼原創區', '歐美原創區', '動漫原創區', '國產原創區', '中字原創區', '轉帖交流區', 'HTTP下載區', '在綫成人影院', '草榴影視庫', '技術討論區', '新時代的我們', '達蓋爾的旗幟', '成人文學交流區', '草榴資訊']
        if srcType == 'video':
            authorityEnter = ['亞洲無碼原創區', '亞洲有碼原創區', '歐美原創區', '動漫原創區', '國產原創區', '中字原創區', '轉帖交流區', 'HTTP下載區', '在綫成人影院']
        elif srcType == 'artical' :
            authorityEnter = ['技術討論區', '成人文學交流區']
        elif srcType == 'img' :
            authorityEnter = ['新時代的我們', '達蓋爾的旗幟']


        response = requests.get(self.main_url+'/'+self.index_url,headers = self.curHeader)

        # print(response.text)

        xparse = etree.HTML(response.content)
        enter_url_suffix = xparse.xpath('//div[@class="t"]/table/tbody/tr[@class="tr3 f_one"]/th/h2/a/@href')
        # print(response.apparent_encoding)
        enter_name = xparse.xpath('//div[@class="t"]/table/tbody/tr[@class="tr3 f_one"]/th/h2/a/text()')
        # print(enter_name)
        index = 0
        # print(response.apparent_encoding)
        # print(response.encoding)
        # print(enter_name)
        for enter_url in enter_url_suffix:
            if enter_name[index] in authorityEnter:
                print('\n'+enter_name[index]+"\n")
                self.print_find_src(self.main_url+'/'+enter_url,keyWord)
            index+=1

    def exc(self,keyWord,srcType):
        '''
        代码执行的main入口
        :param keyWord:
        :param srcType:
        :return:
        '''
        # keyWord = "微信"
        # srcType = 'artical'
        self.getKeyWordSrc(keyWord, srcType)
        self.proxyUtils.updateLocalProxyIps(self.httpsProxyIps,False)
        self.proxyUtils.updateLocalProxyIps(self.httpProxyIps,True)

if __name__=='__main__':
    keyWord = "微信"
    url_path = 'http://cl.moqy.pw/thread0806.php?fid=7'
    # response = requests.get(url_path,headers=curHeader)
    # xparse = etree.HTML(response.content)
    # print(xparse.xpath('//*[@id="ajaxtable"]/tbody/tr/td[2]/h3/a/@href'))
    #
    # print(keyWord.encode().)
    srcType= 'artical'
    cl = CaoLiu()
    cl.getKeyWordSrc(keyWord,srcType)
    # print_find_src(url_path, keyWord)