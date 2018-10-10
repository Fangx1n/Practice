# _*_ encoding=utf-8 _*_
#version:python 3.6.3
#Tools:Pycharm 2017.3.2
__data__ = '2018/7/28 11:17'
__author__ = 'Fangx1n'

import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

#请求网页
def get_one_page(url):
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    try:
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.text
        else:
            return None
    except RequestException:
        return None

#解析网页
def parse_one_page(html):
    pattern=re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>',re.S)
    items=re.findall(pattern,html)
    # print(items)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],     #切掉 【主演：】三个字符
            'time':item[4].strip()[5:],   #同理 切掉【上映时间：】五个字符
            'score':item[5]+item[6]
        }

#写入到文件中
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()


def main(offset):
    url='http://maoyan.com/board/4?offset='+str(offset)
    html=get_one_page(url)
    # print(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(i*10)

    #开启多线程进行抓取，有些数据会抓不到
    # pool=Pool()
    # pool.map(main,[i*10 for i in range(10)])