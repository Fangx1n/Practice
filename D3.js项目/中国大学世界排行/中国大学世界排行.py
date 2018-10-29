# _*_ encoding=utf-8 _*_
#version:python 3.6.3
#Tools:Pycharm 2018.2.1
import re
import time

import requests
from bs4 import BeautifulSoup
from requests import RequestException
import pandas as pd

#程序开始时间
start_time=time.time()
def get_one_page(year):
    try:
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
        }
        url='http://www.zuihaodaxue.com/ARWU{}.html'.format(year)
        response=requests.get(url=url,headers=headers)
        if response.status_code==200:
            return response.content
        return None
    except RequestException:
        print('爬取失败')

#获取国家
def get_country(html):
    soup=BeautifulSoup(html,'lxml')
    counties=soup.select('td > a > img')
    list=[]
    for i in counties:
        src=i['src']
        pattern=re.compile('flag.*\/(.*?).png')
        country=re.findall(pattern,src)[0]
        list.append(country)
    return list

def parse_one_page(html,i):
    tb=pd.read_html(html)[0]
    # print(tb)
    #重命名表格列，不需要的列用数字表示
    tb.columns=['world rank','university',2,3,'score',5,6,7,8,9,10]
    #删除后面不需要的评分列
    tb.drop([2,3,5,6,7,8,9,10],axis=1,inplace=True)

    #rank列100名后是区间，需要唯一化，增加一列index作为排名
    tb['index_rank']=tb.index
    tb['index_rank']=tb['index_rank'].astype(int)+1
    #增加一列年分列
    tb['year']=i
    #获取国家单独爬取
    tb['country']=get_country(html)
    return tb

def save_to_csv(tb):
    tb.to_csv(r'university.csv', mode='a', encoding='utf_8_sig', header=True, index=0)
    endtime=time.time()-start_time
    print('程序运行了%.2f秒' % endtime)

def analysis():
    df=pd.read_csv('university.csv')
    #查询中国的大学（包括港台）
    # df=df.query('(country=="China")|(country=="China-hk")|(country=="China-tw")|(country=="China-HongKong")|(country=="China-Taiwan")')

    #查询中国大陆的大学
    df=df.query('(country=="China")')

    df['index_rank_score']=df['index_rank']
    # 将index_rank列转为整形
    df['index_rank'] = df['index_rank'].astype(int)

    #求topn名
    def topn(df):
        top=df.sort_values(['year','index_rank'],ascending=True)
        return top[:20].reset_index()
    df=df.groupby(by=['year']).apply(topn)
    #更改列顺序
    df = df[['university', 'index_rank_score', 'index_rank', 'year']]
    #重命名列
    df.rename(columns={'university': 'name', 'index_rank_score': 'type', 'index_rank': 'value', 'year': 'date'},inplace=True)
    #输出结果
    df.to_csv('university_ranking.csv',mode ='w',encoding='utf_8_sig', header=True, index=False)


def main(year):
    for i in range(2009,year):
        html=get_one_page(i)
        tb=parse_one_page(html,i)
        save_to_csv(tb)
        print(i,'年排名提取完成')
        analysis()

if __name__ == '__main__':
    main(2019)