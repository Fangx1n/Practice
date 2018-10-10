# -*- coding: utf-8 -*-
import csv
import random

import requests
import requests as requests
import time
from bs4 import BeautifulSoup

#获取html文件
def get_html(url):
    response=requests.get(url=url)
    if response.status_code ==200:
        return response.text
    else:
        return None

#获取租房信息
def get_room_info(html):
    soup=BeautifulSoup(html,'lxml')
    titles=soup.select('#house-lst div.info-panel h2 a')
    styles=soup.select('#house-lst div.info-panel div.col-1 span.zone span')
    squares=soup.select('#house-lst div.info-panel div.col-1 span.meters')
    prices=soup.select('#house-lst div.info-panel div.col-3 div.price span')
    # print(titles,styles,squares,prices)
    # for ti, st, sq, pr, in zip(titles, styles, squares, prices):
    #     print(ti,st,sq,pr)
    data=[]
    for ti, st, sq, pr, in zip(titles, styles, squares, prices):
        info = {}
        title = ti.get_text().strip()  # 出租房屋标题
        info['标题'] = title
        style = st.get_text().strip()  # 出租房屋户型
        info['户型'] = style
        square = sq.get_text().strip()[0:-2]  # 出租房屋面积
        info['面积（平方）'] = square
        price = pr.get_text().strip()  # 出租房屋房租
        info['房租（元/月）'] = price
        price_square = round(float(price) / float(square), 3)  # 出租房屋每平米房租
        info['每平方房租（元）'] = price_square
        data.append(info)
    return data

#写入到CSV文件中
def write_to_csv(url,data):
    print(url)
    name=url.split('/')[-3]
    print(name)
    print('正在把数据写入{}文件'.format(name))
    with open('{}.csv'.format(name),'a',encoding='utf-8-sig',newline='') as f:
        fieldnames = ['标题', '户型', '面积（平方）', '房租（元/月）', '每平方房租（元）']  # 控制列的顺序
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        print("写入成功")

#获取数据的页数，一页三十条数据
def get_page_num(url):
    html=get_html(url=url)
    soup=BeautifulSoup(html,'lxml')
    nums=soup.select('div.wrapper div.main-box div.con-box div.list-head.clear h2 span')
    # print(nums)
    for n in nums:
        total=int(n.get_text())
        print(type(total),total)
        if total < 30:
            num = 1
            return num
        else:
            num = total / 30
            if num > 100:
                num = 100
                return num
            else:
                return num

if __name__ == '__main__':
    area_list=['xihu','xiacheng','jianggan','gongshu','shangcheng','binjiang','yuhang','xiaoshan','xiasha']
    for area in area_list:
        base_url='http://hz.lianjia.com/zufang/{}/pg1/'.format(area)
        print("base_url:",base_url)
        num=get_page_num(base_url)
        print('num:',num)
        for page in range(1,int(num)+1):
            url='http://hz.lianjia.com/zufang/{}/pg{}/'.format(area,page)
            html=get_html(url=url)
            data=get_room_info(html)
            write_to_csv(url,data)
            time.sleep(int(format(random.randint(0,5))))