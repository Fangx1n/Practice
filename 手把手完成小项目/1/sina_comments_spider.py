# -*- coding: utf-8 -*-
import requests
import time
import random
import json
import pandas as pd
# %% time # 计算耗时

comments = pd.DataFrame(columns = ['page','jsons','cmntlist','replydict'])
start_page = 0 # 修改起始页数（初始值为 0）和 csv 文件名，方便爬虫中断后，继续爬取，之后再将几个 csv 数据整合到一起即可 # 断点续爬

# http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=cj&newsid=comos-hhkuskt2879316&group=0&compress=0&ie=gbk&oe=gbk&page=3&page_size=20&jsvar=loader_1533711754393_51961031
# jsvar=loader_1533711754393_51961031
try:
    # 手动设置需要爬取的总页数，评论数若有3000条，那每页20条，就设为150，当然一般在爬取时也可能有新增的评论，所以设大些更好。
    for page in range(start_page,200):  # 截止20180808 16点  # 3,037条评论|18,714人参与 # 截止20180810 8点 # 3,723条评论|30,235人参与
        start = int(time.time()*1000)
        end_stamp = start + random.randint(100,1000)
        end = str(end_stamp)[-8:] # # jsvar=loader_1533711754393_51961031
        url = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=cj&newsid=comos-hhkuskt2879316&group=0&compress=0&ie=gbk&oe=gbk&page={}&page_size=20&jsvar=loader_{}_{}'.format(page, start, end)
        content = requests.get(url).text
        jsons = json.loads(content[34:])  # var loader_1533713810791_51961031= { "result":{status: {msg: "", code: 0}, count: {qreply: 8948, total: 17341, show: 2902}, replydict: {,…},…}
        cmntlist = jsons['result']["cmntlist"]
        replydict = jsons['result']["replydict"]
        # jsons 里有几乎所有数据，方便后续爬虫结束也能本地进行提取 # 不过本次主要对 jsons 里的 cmntlist 和 replydict 感兴趣，所以也先提取了
        comments = comments.append({'page':page+1,'jsons':jsons,'cmntlist':cmntlist,'replydict':replydict},ignore_index=True)
        for num,cmnt in  enumerate(cmntlist):
            print(page*20+num+1, page+1, cmnt['nick'], cmnt['time'], cmnt['content'], cmnt['area'])
        if page%5==0:
            time.sleep(random.randint(0,2)) # 每5页随机停0-2秒，作为简单的防反爬的一步
except:
    print("Error")
comments.to_csv('Sina_Comments_20180905.csv',index=False,encoding='utf-8')