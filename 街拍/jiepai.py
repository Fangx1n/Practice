# _*_ encoding=utf-8 _*_
# version:python 3.6.3
# Tools:Pycharm 2017.3.2
import json
from json import JSONDecodeError
from urllib.parse import urlencode
from requests.exceptions import RequestException
import requests
from bs4 import BeautifulSoup
import re,os
from .config import *
import pymongo
from hashlib import md5
from multiprocessing import Pool

client=pymongo.MongoClient(MONGO_URL,connect=False)
db=client[MONGO_DB]

#请求索引页面获取信息
def get_page_index(offset,keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 1,
        'from':'search_tab'
    }
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response=requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
    except RequestException:
        print('请求索引页失败')
        return None

#请求详情页面获取信息
def get_page_detail(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
    except RequestException:
        print('请求详情页失败',url)
        return None


#解析索引页
def parse_page_index(html):
    try:
        data=json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get("article_url")
    except JSONDecodeError:
        pass

#解析详情页
def parse_page_detail(html,url):
    soup=BeautifulSoup(html,'lxml')
    title=soup.select('title')[0].get_text
    print(title)
    images_pattern=re.compile('var gallery = (.*?);', re.S)
    result=re.search(images_pattern,html)
    if result:
        print(result.group(1))
        data=json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images=data.get('sub_images')
            images=[item.get('url') for item in sub_images]
            for image in images:download_image(image)
            return {
                'title':title,
                'url':url,
                'images':images
            }
#存储到MONGO数据库中
def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到MongoDB成功',result)
        return True
    return False

#下载图片
def download_image(url):
    print('正在下载：',url)
    try:
        response=requests.get(url)
        if response.status_code==200:
            save_image(response.content)
    except RequestException:
        print('请求图片失败',url)
        return None

#保存图片
def save_image(content):
    file_path = '{0}/{1},{2}'.format(os.getcwd(), md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()

def main(offset):
    html=get_page_index(offset,KEYWORD)
    # print(html)
    for url in parse_page_index(html):
        print(url)
        html= get_page_detail(url)
        # print(html)
        if html:
            result=parse_page_detail(html,url)
            # print(result)
            if result:save_to_mongo(result)

if __name__ == '__main__':
    # main()
    groups=[x*20 for x in range(GROUP_START,GROUP_END+1)]
    pool=Pool()
    pool.map(main,groups)
