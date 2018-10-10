# -*- coding: utf-8 -*-
import pandas as pd
import re
from collections import Counter
from pyecharts import Bar
import jieba
import matplotlib.pylab as plt
import nltk
from nltk.draw.dispersion import dispersion_plot

'''评论emoji提取并绘制图谱'''

df=pd.read_csv('Sina_Finance_Comments_All_20180811_Cleaned.csv',encoding='utf-8')
# print(df.head())
#匹配评论中的emoji信息
def get_emoji(content):
    pattern=re.compile(u"\[[a-zA-Z\u4e00-\u9fa5]+\]")
    result=re.findall(pattern,content)
    return result
df['emojis_list']=df['content'].apply(get_emoji)
# print(df.head(20))
emojis=df['emojis_list'].values.tolist()
# print(emojis)

#去重
emojis_list=sum(emojis,[])
print(emojis_list)
emojis_set=list(set(emojis_list))
num=len(emojis_set)
print(num)
print('去重之后：',emojis_set)

#emoji分组统计
counter=Counter(emojis_list)
print('emoji分组统计:',counter.most_common())

#emoji使用情况,echarts柱状图分析
y_emojis,x_counts=zip(*counter.most_common())
print('y_emojis:',y_emojis)
print('x_counts:',x_counts)
bar =Bar('emoji使用情况')
bar.add(
    'emoji',
    y_emojis[:20],
    x_counts[:20],
    is_label_show=True,
    is_stack=True,
    xaxis_rotate=45,
    xaxis3d_interval=0,
    xaxis3d_margin=8
)
bar.render()

#评论数据
cmnts_list=df['content'].values.tolist()
# print(cmnts_list)
#   合并成一个字符串
cmnts=''.join(cmnts_list)
# print(len(cmnts),cmnts)

#jieba分词
emoji_drop = []
for emojis in y_emojis:
    emoji = emojis[1:-1] # 去掉括号
    jieba.add_word(emoji) # 读者可将上一行注释掉，看看分词结果
    emoji_drop.append(emoji) # 将去掉括号后的emoji单独保存
words = list(jieba.cut(cmnts))
# print(len(words),words)
# print(words)
print(len(emoji_drop),emoji_drop)

#nitk分布图谱
plt.rcParams['font.sans-serif']=['SimHei']
ntext=nltk.Text(words)
ntext.dispersion_plot(emoji_drop[:15])
# ntext.dispersion_plot(emoji_drop)