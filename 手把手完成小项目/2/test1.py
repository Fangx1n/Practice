# -*- coding: utf-8 -*-
import random

import pandas as pd
import requests
import time
from lxml import etree


df =pd.read_csv('Sina_Finance_Comments_1_20180811.csv',encoding='utf-8')
# print(df.head(10))
# cmntlist=df.cmntlist.values.tolist()
# print(len(cmntlist))
# print(cmntlist[0])
# print(type(cmntlist[0]))

df['jsons'] = df.jsons.apply(lambda x: eval(x))
df['cmntlist'] = df.cmntlist.apply(lambda x: eval(x))
df['replydict'] = df.replydict.apply(lambda x: eval(x))
# print(df['jsons'])
# print(df['cmntlist'])
# print(df['replydict'])
cmntlists=df['cmntlist'].values.tolist()
# print(cmntlists[0])
cmntlist=sum(cmntlists,[])
# print(cmntlist)
# print(len(cmnlist))
# print(cmntlist[0])

#获取ip数据
def ip2loc(ip):
    url = 'https://ip.cn/index.php?ip={}'.format(ip)
    text=requests.get(url).text
    html=etree.HTML(text)
    try:
        loc = html.xpath('//div[@id="result"]/div/p[2]/code/text()')[0]
    except:
        loc = ''
    try:
        geo_ip = html.xpath('//div[@id="result"]/div/p[3]/text()')[0]
    except:
        geo_ip = ''
    try:
        tele = html.xpath('//div[@id="result"]/div/p[4]/text()')[0]
    except:
        tele = ''
    return loc + ' * ' + geo_ip + ' * ' + tele



for num , cmnt in enumerate(cmntlist):
    ip_loc=ip2loc(cmnt['ip'])
    print(num,cmnt['ip'],cmnt['area'],ip_loc)
    if num%5==0:
        time.sleep(random.randint(0,2))
    if num==30:break