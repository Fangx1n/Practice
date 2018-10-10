# -*- coding: utf-8 -*-
import pandas as pd
from snownlp import SnowNLP
import jieba.analyse
import numpy as np
import matplotlib.pylab as plt
from pyecharts import WordCloud

'''情感分析与词云'''

df=pd.read_csv('Sina_Finance_Comments_All_20180811_Cleaned.csv',encoding='utf-8')

def sentiment(content):
    s=SnowNLP(content)
    return s.sentiments

df['sentiment']=df.content.apply(sentiment)

df_sent=df[['content','sentiment']]
# print(df_sent.sort_values(by=['sentiment'],ascending=False))
# print(df_sent.sort_values(by=['sentiment']))

#基于 TF-IDF 算法的关键词抽取
all_content=df.content.values.tolist()
extract_tags=' '.join(jieba.analyse.extract_tags(
    ' '.join(all_content),topK=200,withWeight=False, allowPOS=('ns', 'n'))
)
print('关键字提取：',extract_tags)

#词云
print(len(all_content),'\n',all_content[-1])

segment=[]
for line in all_content:
    try:
        segs=jieba.lcut(line)
        for seg in segs:
            if len(seg)>1 and seg!='\r\n':
                segment.append(seg)
    except:
        print(line)
        continue
#去停用词
words_df = pd.DataFrame({"segment": segment})

words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数": np.size})
words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)
print(words_stat.head(20))

wordcloud=WordCloud(width=800,height=520)
wordcloud.add('评论词云',
              words_stat['segment'],    #name
              words_stat['计数'],       #value
              word_size_range=[20,100]  #单词字体大小范围，默认为[12,60]
              )
wordcloud.render()
