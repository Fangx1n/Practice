# -*- coding: utf-8 -*-
import random
import time
import requests
import json

'''数据爬取'''
for page in range(1,150):
    start=int(time.time()*1000)#13位开始时间戳
    end_stamp=start+random.randint(100,1000)#构造13位结束时间戳
    end=str(end_stamp)[-8:]#取最后8位
    url='http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=cj&newsid=comos-hhkuskt2879316&group=0&compress=0&ie=gbk&oe=gbk&page={}&page_size=20&jsvar=loader_{}_{}'.format(page,start,end)
    response=requests.get(url).text
    json_dict=json.loads(response[34:])#去除最前面的34个字符‘var loader_1536143157258_43157949=’
    cmntlist=json_dict['result']['cmntlist']
    replylist = json_dict['result']['replydict']
    print(replylist)
    # print(cmntlist)
    # for num,cmnt in enumerate(cmntlist):
    #     print(num,cmnt['nick'],cmnt['area'], cmnt['time'], cmnt['content'])
    break