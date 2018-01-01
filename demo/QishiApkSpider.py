#!usr/bin/python
# ! _*_coding:utf-8_*_
import os

import requests
from lxml import etree
class QishiApkSpider():
    '''
    爬取骑士助手上的破解游戏
    '''

    def __init__(self):
        self.saveApkDir = r'D:\tmp\1223'
        self.start_url = 'http://www.vqs.com/crack/{}-view'
        self.page = 6
        self.gameName = ''
        # 他可能会校验你的来源页面,也就是你访问下一个页面时候的上一个页面的url,所以这里要设置下
        self.prePage = 'http://www.vqs.com/crack/'
        self.headers = {
        # 'authorization':'Bearer MS4xVGM0NEJBQUFBQUFYQUFBQVlRSlZUZWVZOTFxOWIybklNd2VkalhUWG9YT2JjSnBrQXNZcnd3PT0=|1510623975|3b616fd23adb09cad90dcc742a4b22353e321efc',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'Referer':self.prePage,
        }

    def getDownloadPageUrl(self,forwardPageUrl):
        '''
        获取应用详情页的url
        :param forwardPageUrl: 初始页面 url
        :return:
        '''
        response = requests.get(forwardPageUrl,headers=self.headers)
        if response.status_code != 200:
            yield self.getDownloadPageUrl(forwardPageUrl)
        else:
            selector = etree.HTML(response.text)
            gameBlocks = selector.xpath('//*/div[@class="pic_box"]/dl/dd/div')
            for gameBlock in gameBlocks:
                # gameBlock.xpath('./p[1]/text()')[0].split(' | ')[-1].split("M")[0]
                # selector = etree.HTML(gameBlock)
                # gameSize = selector.xpath('./p[1]').split(' | ')[-1].split("M")[0]
                gameSize = gameBlock.xpath('./p[1]/text()')[0].split(' | ')[-1].split("M")[0]
                print("gameSize : " + gameSize)
                self.gameName = gameBlock.xpath('./h3/a/@title')[0]

                print(self.gameName)
                if gameSize=='':
                    yield ""
                    continue
                try :
                    if int(gameSize) > 100:
                        yield ""
                        continue
                except Exception as e :
                    try :
                        if float(gameSize) > 100:
                            yield ""
                            continue
                    except Exception as e:
                        print(e)
                        yield ""
                        continue


                downloadPageUrl = gameBlock.xpath('./p[3]/span/a/@href')[0]

                print("downloadPageUrl : " + downloadPageUrl)
                yield downloadPageUrl

    def checkApkDownSuccess(self,apkPath,apkSize):
        '''
        校验apk是否下载成功
        :param apkPath: apk在本地的路径
        :param apkSize: apk正常大小
        :return:
        '''
        if apkSize/1024/1024 != os.path.getsize(apkPath)/1024/1024:
            return False
        else:
            return True

    def downLoadApk(self,downLoadUrl,retryTime=0):
        '''
        开始下载apk
        :param downLoadUrl: apk的地址
        :return:
        '''
        response = requests.get(downLoadUrl,headers=self.headers)
        apkSize = response.headers.get('Content-Length',0)
        apkPath = self.saveApkDir+os.sep + self.gameName+".apk"
        with open(apkPath,'wb') as f:
            f.write(response.content)
        if not self.checkApkDownSuccess(apkPath,int(apkSize)):
            if retryTime < 3:
                self.downLoadApk(downLoadUrl,retryTime+1)

    def startDownLoadApk(self,downloadPageUrl):
        '''
        获取下载链接并开始下载apk
        :param downloadPageUrl: 游戏详情页 url
        :return:
        '''
        response = requests.get(downloadPageUrl,headers=self.headers)
        if response.status_code != 200:
            self.startDownLoadApk(downloadPageUrl)
            return
        selector = etree.HTML(response.text)
        buttonTxt = selector.xpath('//*/div[@class="txt lft"]/div[@class="down"]/a[1]/text()')[0]
        if buttonTxt != u"高速下载":
            return
        downLoadUrl = selector.xpath('//*/div[@class="txt lft"]/div[@class="down"]/a[1]/@href')[0]
        self.downLoadApk(downLoadUrl)

    def main_exc(self):

        while self.page < 31:
            print("正在爬取第%d页...." %self.page)
            for downloadPageUrl in self.getDownloadPageUrl(self.start_url.format(self.page)):
                self.prePage = self.start_url.format(self.page)
                if downloadPageUrl == "":
                    continue
                else:
                    self.startDownLoadApk(downloadPageUrl)
                pass
            self.page += 1

if __name__ == '__main__':
    spider = QishiApkSpider()
    spider.main_exc()