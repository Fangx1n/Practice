# -*- coding: utf-8 -*-
import requests
from lxml import etree

cmntlist={
	'comment_imgs': '',
	'parent_mid': '0',
	'news_mid_source': '0',
	'rank': '0',
	'mid': '5B6B9FA6-777B83B3-68B55EBD-8C5-8E4',
	'video': '',
	'vote': '0',
	'uid': '1756716733',
	'area': '广东深圳',
	'channel_source': '',
	'content': '我手机三年没换 星巴克没去一次 我的房呢？',
	'nick': '潘昱材',
	'hot': '0',
	'status_uid': '1653689003',
	'content_ext': '',
	'ip': '119.123.131.179',
	'media_type': '0',
	'config': 'wb_verified=0&wb_screen_name=潘昱材&wb_cmnt_type=comment_retweeted_status&wb_user_id=1756716733&wb_description=&area=广东深圳&wb_parent=&wb_profile_img=http://tva3.sinaimg.cn/crop.0.0.750.750.50/68b55ebdjw8evkh2jm6goj20ku0kuq3m.jpg&wb_time=2018-08-09 09:57:52&wb_comment_id=4271044707533952',
	'channel': 'cj',
	'comment_mid': '0',
	'status': 'M_PASS',
	'openid': '',
	'newsid_source': '',
	'parent': '',
	'status_cmnt_mid': '4271044707533952',
	'parent_profile_img': '',
	'news_mid': '0',
	'parent_nick': '',
	'newsid': 'comos-hhkuskt2879316',
	'parent_uid': '0',
	'thread_mid': '0',
	'thread': '',
	'level': '0',
	'against': '1533779879',
	'usertype': 'wb',
	'length': '21',
	'profile_img': 'http://tva3.sinaimg.cn/crop.0.0.750.750.50/68b55ebdjw8evkh2jm6goj20ku0kuq3m.jpg',
	'time': '2018-08-09 09:57:59',
	'login_type': '0',
	'audio': '',
	'agree': '0'
}
def ip2loc(ip):
    url = 'https://ip.cn/index.php?ip={}'.format(ip)
    r = requests.get(url).text
    return r
text = ip2loc(cmntlist['ip'])
# print(text)
html=etree.HTML(text)
loc=html.xpath('//*[@id="result"]/div/p[2]/code/text()')[0]
tele=html.xpath('//*[@id="result"]/div/p[4]/text()')[0]
GeoIP=html.xpath('//*[@id="result"]/div/p[3]/text()')[0]
print(loc,'\n',tele,'\n',GeoIP)