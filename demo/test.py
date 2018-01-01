#!usr/bin/python
# ! _*_coding:utf-8_*_
import spiderUtils.UserAgent as uaUtil
from spiderUtils import Utils


def xPathDemo(url_path):
    import requests
    from lxml import etree

    r = requests.get(url_path)
    xparse = etree.HTML(r.text)
    print(xparse.xpath('//h3/span[@class="comment-info"]/a/@href'))

def zhifuDemo():
    import requests,pandas
    url_path = "https://www.zhihu.com/api/v4/members/timothy-wang-17/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=40&limit=20"
    header = {
        'authorization':'Bearer MS4xVGM0NEJBQUFBQUFYQUFBQVlRSlZUZWVZOTFxOWIybklNd2VkalhUWG9YT2JjSnBrQXNZcnd3PT0=|1510623975|3b616fd23adb09cad90dcc742a4b22353e321efc',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    }
    response = requests.get(url_path, headers=header).json()
    # print(response["data"])
    pd = pandas.DataFrame(response["data"])
    pd.to_excel("11.xlsx")


def mongoDbTest():
    from pymongo import MongoClient
    client = MongoClient()
    db = client.test
    # my_set = db.set
    my_set = db.student
    my_set.insert({"name":"yezi","age":26})

def toutiaoDemo():
    import requests
    from pymongo import MongoClient
    url_path = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0"
    parm_data = {
        'first':'true',
        'pn':'1',
        'kd':'python',
    }

    curHeader = {
        'Referer':'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
        'User-Agent':uaUtil.getUserAgent(),

    }
    response = requests.post(url_path,data=parm_data,headers=curHeader).json()['content']['positionResult']['result']
    # print(response)
    client = MongoClient()
    db = client.test
    job_table = db.job
    job_table.insert(response)

if __name__ == '__main__':
    import time
    url_path = "https://book.douban.com/subject/1084336/comments/"
    # xPathDemo(url_path)
    # zhifuDemo()
    # toutiaoDemo()
    # dict1 ={"1":22}
    # dict2 ={"1":33}
    # mergeDict = dict1.copy()
    # mergeDict.update(dict2)
    # utils = Utils.Utils()
    # utils.testNetOK()

    list1 = ['11','21']
    list2 = ['22','221']
    list1 = list1.extend(list2)
    print(list1)
    pass