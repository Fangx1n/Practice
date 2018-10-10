# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
from pyecharts import Line, Bar
from pyecharts.engine import create_default_environment

'''评论数变化情况'''

df=pd.read_csv('Sina_Finance_Comments_All_20180811_Cleaned.csv',encoding='utf-8')
print(df.head())
# plt.plot(df.stamp,df.cmntcount)
# plt.show()

print('===================================================')
df_ymdcount=df.groupby('time_ymd')['cmntcount'].count()
print(df_ymdcount)
line1=Line('每日评论数变化情况')
line1.add('日期',df_ymdcount.index,df_ymdcount.values,is_label_show=True,line_type='dotted')
env=create_default_environment('html')
env.render_chart_to_file(line1, path='line1.html')

print('===================================================')
df_mdhcount=df.groupby('time_mdh')['cmntcount'].count()
print(df_mdhcount)
#折线图
line2=Line('每小时评论数')
line2.add('小时',df_mdhcount.index,df_mdhcount.values,is_label_show=True,line_type='dotted')
env.render_chart_to_file(line2,path='line2.html')
#柱状图
bar=Bar('每小时评论数')
bar.add('小时',df_mdhcount.index,df_mdhcount.values,is_label_show=True,line_type='dotted')
env.render_chart_to_file(bar,path='bar.html')