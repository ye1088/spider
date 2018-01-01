#!usr/bin/python
# ! _*_coding:utf-8_*_
import datetime
import os

import requests
import sys

import MainExc
import spiderUtils.UserAgent as UA

class Utils:

    def __init__(self):
        os.path.abspath(sys.argv[0])
        self.headers = {
            'User-Agent': UA.getUserAgent()
        }
        pass


    def printError(self,msg):
        '''
        在控制台上输出错误日志
        :param msg: 日志信息
        :return:
        '''
        with open(MainExc.runLog,'a') as logFile:

            logFile.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S\t')) + str(msg) + '\n')


    def testNetOK(self):
        '''
        测试当前机子不适用代理的网络可用么
        :return:
        '''
        try:
            requests.get("http://www.baidu.com", headers=self.headers)
            return True
        except Exception as e:
            self.printError(e)
            return False

if __name__=='__main__':
    utils = Utils()
    print()
    # utils.testNetOK()