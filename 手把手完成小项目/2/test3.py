# -*- coding: utf-8 -*-
import time
import random
from lxml import etree

import pandas as pd
import requests

'''数据提取，IP获取'''
sinanews_comments=pd.DataFrame(columns=['No','page','nick','time','content','area',
                                        'ip','ip_loc','length','against','agree', 'channel',
                                        'hot', 'level', 'login_type', 'media_type', 'mid'])
page=1
df =pd.read_csv('sina_comments_20180905.csv',encoding='utf-8')
df['jsons'] = df.jsons.apply(lambda x: eval(x))
df['cmntlist'] = df.cmntlist.apply(lambda x: eval(x))
df['replydict'] = df.replydict.apply(lambda x: eval(x))
cmntlists=df['cmntlist'].values.tolist()
cmntlist=sum(cmntlists,[])

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


for num,cmnt in enumerate(cmntlist):
    nick = cmnt['nick']
    times = cmnt['time'] #命名成 time 会和下面 time.sleep() 冲突 # 所以命名成 times
    content = cmnt['content']
    area = cmnt['area']
    ip = cmnt['ip']
    ip_loc = ip2loc(cmnt['ip'])
    length = cmnt['length']
    against = cmnt['against']
    agree = cmnt['agree']
    channel = cmnt['channel']
    hot = cmnt['hot']
    level = cmnt['level']
    login_type = cmnt['login_type']
    media_type = cmnt['media_type']
    mid = cmnt['mid']
    print(num+1,page,times,nick,content,area,ip_loc)
    sinanews_comments = sinanews_comments.append({'No':num+1,'page':page,'nick':nick,'time':times,'content':content,'area':area,
                                                  'ip':ip,'ip_loc':ip_loc,'length':length,'against':against,'agree':agree,
                                                  'channel':channel,'hot':hot,'level':level,'login_type':login_type,
                                                  'media_type':media_type,'mid':mid},ignore_index=True)
    if num%30 == 0:
        time.sleep(random.randint(0,1))
    if int((num+1)%20) == 0:
        page += 1
    if page ==11:
        break
sinanews_comments.to_csv('Sina_Comments_All_utf_8_sig.csv', encoding='utf_8_sig', line_terminator='\r\n')