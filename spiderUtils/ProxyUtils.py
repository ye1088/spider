#!usr/bin/python
# ! _*_coding:utf-8_*_
import time
from lxml import etree
import requests

import MainExc
import spiderUtils.UserAgent as UA
import os

class ProxyUtil:

    def __init__(self):

        self.https_proxy_url = 'http://www.xicidaili.com/wn'
        self.http_proxy_url = 'http://www.xicidaili.com/wt'
        # self.configDirPath = os.get
        self.curHeader = {
            'If-None-Match':'W/"9d715b684b39fbcc87a9aad6e82c4ba1"',
            'User-Agent':UA.getUserAgent()
        }

    def mergeIpAndPort(self,ips,ports):
        '''
        将 ip 和 端口port 合并了
        结果类似于这样  ['192.168.1.1:8080']
        :param ips: ip列表
        :param ports: 端口好列表
        :return:
        '''
        if (len(ips) != len(ports)):
            raise '获取的ip和端口port不匹配'
        ipsList = []
        portsIndex = 0
        for ip in ips:
            ipsList.append(ip+':'+ports[portsIndex])
            portsIndex += 1
        return ipsList


    def getHttpProxy(self,maxPage=1):
        '''
       获取 https 的代理ip列表
       样子 大概是这样的 ['192.168.1.1:8080']
       :param maxPage: 要记录的最大页数
       :return:
       '''
        curPage = 1
        proxy_ips = []
        proxy_port = []
        while curPage <= maxPage:
            response = requests.get(self.http_proxy_url+'/%d'%curPage, headers=self.curHeader)
            # print(response.content)
            xparse = etree.HTML(response.text)
            proxy_ips.extend(xparse.xpath('//*[@id="ip_list"]/tr/td[2]/text()'))
            proxy_port.extend(xparse.xpath('//*[@id="ip_list"]/tr/td[3]/text()'))
            # print(proxy_port)
            # print('proxy ip len :%d' %len(proxy_ips) )
            # print('proxy port len :%d' %len(proxy_port) )
            curPage += 1
            time.sleep(1)

        return self.mergeIpAndPort(proxy_ips, proxy_port)



    def getHttpsProxy(self,maxPage=1):
        '''
        获取 https 的代理ip列表
        样子 大概是这样的 ['http://192.168.1.1:8080']
       :param maxPage: 要记录的最大页数
        :return:
        '''
        curPage = 1
        proxy_ips = []
        proxy_port = []
        while curPage <= maxPage:
            response = requests.get(self.https_proxy_url+'/%d'%curPage,headers=self.curHeader)
            # print(response.content)
            xparse = etree.HTML(response.text)

            proxy_ips.extend(xparse.xpath('//*[@id="ip_list"]/tr/td[2]/text()'))
            proxy_port.extend(xparse.xpath('//*[@id="ip_list"]/tr/td[3]/text()'))
            # print(proxy_port)
            # print('proxy ip len :%d' %len(proxy_ips) )
            # print('proxy port len :%d' %len(proxy_port) )
            curPage += 1
            time.sleep(1)
        return self.mergeIpAndPort(proxy_ips,proxy_port)

    def popUnuseIp(self,httpProxyIps,httpsProxyIps,index):
        '''
        pop 掉没有用的代理ip 并返回
        :param httpProxyIps: http 代理ip列表
        :param httpsProxyIps: https 代理ip列表
        :param index: 没有用的ip 的位置
        :return:
        '''
        if len(httpProxyIps) > 0:
            httpProxyIps.pop(index)
            httpsProxyIps.pop(index)
        if len(httpProxyIps) < 50:
            self.updateLocalProxyIps(httpProxyIps,True)
            self.updateLocalProxyIps(httpsProxyIps,False)
            return self.getProxyIpsFromFile(True),self.getProxyIpsFromFile(False)
        else:
            return httpProxyIps,httpsProxyIps


    def updateLocalProxyIps(self,ipList,isHttp=True):
        '''
        本地的代理ip测试完后删掉失效的ip后，保存更新本地的代理文件
        :param ipList:代理列表
        :param isHttp:是否为http代理
        :return:
        '''
        if isHttp:
            with open(MainExc.configDirPath + os.sep + 'http_proxy_ip', 'w') as proxyFile:
                for ip in ipList:
                    proxyFile.write(ip + '\n')
        else:
            with open(MainExc.configDirPath + os.sep + 'https_proxy_ip', 'w') as proxyFile:
                for ip in ipList:
                    proxyFile.write(ip + '\n')


    def updateProxyIps(self, isHttp=True, isGetProxyIpsFromFileCall = False,historyProxy=[]):
        '''
        从网上爬取代理ip更新代理ip文件的ip值
        :param isHttp:是否为http代理
        :param isGetProxyIpsFromFileCall:是否为 getProxyIpsFromFile 方法调用的
        :return:
        '''
        ipList = []
        if not isGetProxyIpsFromFileCall :
            historyProxy = self.getProxyIpsFromFile(isHttp)
        if isHttp:
            ipList = self.getHttpProxy(2)

            ipList += historyProxy
            ipList.pop()
            with open(MainExc.configDirPath+os.sep+'http_proxy_ip','w') as proxyFile:
                for ip in ipList:
                    proxyFile.write(ip+'\n')
        else:
            ipList = self.getHttpsProxy(2)
            ipList += historyProxy
            ipList.pop()
            ipList = list(set(ipList))
            # print(ipList)
            with open(MainExc.configDirPath+os.sep+'https_proxy_ip','w') as proxyFile:
                for ip in ipList:
                    proxyFile.write(ip+'\n')


    def getProxyIpsFromFile(self,isHttp=True):
        '''
        将代理ip的配置文件读取出来，以列表的形式返回
        :param isHttp:是否为http代理
        :return:
        '''
        ipList = []
        if isHttp:
            with open(MainExc.configDirPath + os.sep + 'http_proxy_ip', 'r') as proxyFile:
                ipList = proxyFile.read().split('\n')
        else:
            with open(MainExc.configDirPath + os.sep + 'https_proxy_ip', 'r') as proxyFile:
                ipList = proxyFile.read().split('\n')
        ipList.pop()
        if len(ipList) < 100:
            self.updateProxyIps(isHttp, True,ipList)
            return self.getProxyIpsFromFile(isHttp)
        return ipList







if __name__=='__main__':
    import random

    util = ProxyUtil()
    httpIps = util.getHttpProxy()
    httpsIps = util.getHttpsProxy()
    proxy = {
        'http': httpIps[random.randint(0, len(httpIps) - 1)],
        'https': httpsIps[random.randint(0, len(httpsIps) - 1)],
    }

    proxies = {"http": "114.239.220.206:8118", "https": "113.65.5.35:9000", }
    print(proxy)
    r = requests.get("http://ip.chinaz.com/",headers=util.curHeader,proxies=proxies)
    print(r.content.decode(r.encoding))
