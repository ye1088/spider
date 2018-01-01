#!usr/bin/python
# ! _*_coding:utf-8_*_
import json
import os

import requests
from lxml import etree
class Zidonghuifu():
    '''
        公众号后台自动回复包含某些关键词的评论

        配置文件 GongZhongHaoHuiFu.cfg 说明:
            Artical_index = 要回复第几篇文章中的评论
            Comment_key = 用户评论中包含哪些关键词(建议4个字以上),多个关键词用 '|' 分割
            Cookie  = 我们登录公众号之后的 cookie
    '''
    def __init__(self):

        self.config_dict = {}
        self.initConfig()
        self.start_url = 'https://mp.weixin.qq.com/misc/appmsgcomment?action=list_comment&begin={}&count=10&' \
                         'comment_id={}&filtertype=0&day=0&type=2&token=1581168041&lang=zh_CN&f=json&ajax=1'  # https://tieba.baidu.com/p/5356540826??pn={}
        self.comment_url = self.start_url   # 用户评论的内容
        self.reply_data = { # 回复的数据
            'comment_id':'884411644',
            'content_id':'15806176224255934470',
            'content':'谢谢~~也祝你新年快乐~~',
            'token':'1581168041',
            'lang':'zh_CN',
            'f':'json',
            'ajax':'1'
        }

        # 这里换页 是 begin 10 的倍数换页
        # index_page 公众号后台最开始的页面
        self.index_page = 'https://mp.weixin.qq.com/misc/appmsgcomment?action=get_unread_appmsg_comment&begin=0&count=10&token=1581168041&lang=zh_CN&f=json&ajax=1'
        self.reply_url = 'https://mp.weixin.qq.com/misc/appmsgcomment?action=reply_comment'
        self.page = 10
        self.artical_index = int(self.config_dict['Artical_index']) # 要回复的第几个文章的回复
        self.reply_msg = self.config_dict['Reply_msg']
        self.key_msg = self.config_dict['Comment_key']  # 用户评论所包含的key

        self.headers = {
            # 'authorization':'Bearer MS4xVGM0NEJBQUFBQUFYQUFBQVlRSlZUZWVZOTFxOWIybklNd2VkalhUWG9YT2JjSnBrQXNZcnd3PT0=|1510623975|3b616fd23adb09cad90dcc742a4b22353e321efc',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
            'Cookie':self.config_dict['Cookie']
            # 'Referer': self.prePage,
        }
        self.artical_id = self.getArticalId(self.artical_index)  # 要回复的文章的id

    def initConfig(self):
        '''
        读取配置文件初始化各种配置
        :return:
        '''
        with open(os.getcwd() + os.sep + 'config' + os.sep +'GongZhongHaoHuiFu.cfg','r',encoding='utf8') as f:
            # while True:
            #     line = f.readline()
            #     if not line :
            #         break
            #     self.config_dict[line.split('===')[0]] = line.split('===')[1]
            for line  in f:
                self.config_dict[line.split('===')[0]] = line.split('===')[1].split('\n')[0]

    def getArticalId(self,artical_index = 0):
        '''
        获取第 artical_index 篇文章的id
        :param artical_index:
        :return:
        '''
        response = requests.get(self.index_page,headers=self.headers)
        index_page_msg = json.loads(response.content)
        print("artical id : "+index_page_msg['item'][artical_index]['comment_id'])
        return index_page_msg['item'][artical_index]['comment_id']


    def isContainKeyMsg(self,comment):
        '''
        判断用户评论是否包含某些关键词
        :param comment: 用户的评论
        :return:
        '''

        # if u"新年快乐" in comment:
        #     print(comment)
        for key_msg in self.key_msg.split('|'):
            if key_msg in comment:
                return True
        return False

    def getUserComment(self):
        '''
        遍历用户的评论,包含某些关键词就自动回复
        :return:
        '''
        for page in range(0,100):

            print("这是第%d页" %page)
            response = requests.get(self.start_url.format(self.page * page,self.artical_id),headers= self.headers)
            all_json = json.loads(response.content)
            comment_json = json.loads(all_json['comment_list'])['comment']
            for i in range(0,9):
                # print(comment_json[i]['content'])
                if self.isContainKeyMsg(comment_json[i]['content']):
                    self.reply_comment(comment_json[i], self.reply_msg)

    def reply_comment(self,reply_com,reply_msg = None):
        '''
        自动回复评论
        :param reply_com: 要回复的评论
        :param reply_msg: 要回复的内容
        :return:
        '''
        self.reply_data['comment_id'] = reply_com['comment_id']
        self.reply_data['content_id'] = reply_com['content_id']
        self.reply_data['content'] = reply_msg
        self.headers['Referer'] = self.start_url
        response = requests.post(self.reply_url,data=self.reply_data,headers=self.headers)
        print(response.content)



if __name__ == '__main__':
    huifu = Zidonghuifu()
    huifu.getUserComment()

    # huifu.getArticalId()
    # print(huifu.key_msg)
    # print(huifu.artical_index)
    # print(huifu.reply_msg)
    # print(huifu.config_dict['Cookie'])
