# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from pyecharts import Bar,Line,Overlap

'''数据异常及清洗'''

df=pd.read_csv('Sina_Finance_Comments_All_20180811.csv',encoding='utf-8')
print(df.shape)
#将用户昵称和评论内容均一致的行删除重复
df.drop_duplicates(subset=['nick','content'],keep='first',inplace=True)
print(df.shape)

#创建时间戳列
#由日期列创建出对应的时间戳列
def time2stamp(cmnttime):
    cmnttime=datetime.strptime(cmnttime,'%Y-%m-%d %H:%M:%S')
    stamp=int(datetime.timestamp(cmnttime))
    return stamp
df['stamp']=df['time'].apply(time2stamp)
df['time_ymd'] = df.time.apply(lambda x:x.split(' ')[0]) # 年月日
df['time_mdh'] = df.time.apply(lambda x:x.split(':')[0][5:]) #月日时 # 方便后续可视化时横坐标展示
df.head()
# print(df.shape)

#按时间排序后重置index索引
df.sort_values(by=["stamp"],ascending=False,inplace=True)
df.reset_index(inplace=True,drop=True)

#创建评论数计数列
df['cmntcount'] =int(df.shape[0])-df.index.to_series()
df['cmntcount'].head()
df.to_csv('Sina_Finance_Comments_All_20180811_Cleaned.csv', encoding='utf-8', line_terminator='\r\n')
print(df.shape)

#用matplotlib画图
# plt.plot(df.stamp,df.cmntcount)
# plt.show()#显示图像

#每小时评论数组合图
df_mdhmax=df.groupby('time_mdh')['cmntcount'].max()
df_mdhcount=df.groupby('time_mdh')['cmntcount'].count()
bar=Bar('每小时评论数')           #图标名称
bar.add("小时",                   #图例名称
        df_mdhcount.index,       #
        df_mdhcount.values,
        is_label_show=True,      #柱状图上显示数据
        xaxis_interval=-90,      #横坐标标度
        xaxis_rotate=-90,        #横坐标标签旋转角度
        yaxis_interval=200,      #纵坐标标度
        yaxis_max=800)           #纵坐标最大值
line = Line("每小时评论数")
line.add("小时",
         df_mdhmax.index,
         df_mdhmax.values,
         line_opacity=1,        #线条不透明度
         line_type='dotted',
         yaxis_interval=1000,
         yaxis_max=4000)

overlap = Overlap()     #结合不同类型图表叠加画在同张图上
overlap.add(bar)
overlap.add(line, is_add_yaxis=True, yaxis_index=1)
overlap.render() # 使用 render() 渲染生成 .html 文件