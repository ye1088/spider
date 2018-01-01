#!usr/bin/python
# ! _*_coding:utf-8_*_

import os

import sys

from secretThings import cl_src
from spiderUtils import ProxyUtils
from spiderUtils import Utils

'''
    这里处理各种路径
'''
rootPath = os.getcwd()
configDirPath = rootPath + os.sep + "ConfigDir"
runLog = configDirPath + os.sep + "runtime.log"

def clearLog():
    with open(runLog,'w') as logFile:
        logFile.write("")

if __name__=='__main__':
    os.path.abspath(sys.argv[0])
    proxyUtils = ProxyUtils.ProxyUtil()
    caoLiu = cl_src.CaoLiu()
    # utils = Utils.Utils()
    clearLog()
    caoLiu.exc("睡","img")
