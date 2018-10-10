# -*- coding: utf-8 -*-
import pandas as pd
from pyecharts import Bar, Map
from pyecharts.engine import create_default_environment

'''省份提取与可视化'''

df = pd.read_csv('Sina_Finance_Comments_All_20180811_Cleaned.csv',encoding='utf-8')
# print(df.head())

# print(df[['area'],['ip_loc']])

#统计area
area_count=df.groupby('area')['area'].count().sort_values(ascending=False)
area_name=list(area_count.index)
area_values=area_count.values
# print(len(area_name),len(area_values))
# print(area_count)
print(len(area_name),area_name)

#去除非国内的数据
area_len_2 = []
area_len_3 = []
area_len_4 = []
area_len_5 = []
unchina = ['英国','美国','日本','瑞士','法国','瑞典','越南','泰国',
           '意大利','加拿大','菲律宾','新加坡','新西兰','伊拉克','爱尔兰','安哥拉',
           '澳大利亚', '大韩民国', '马来西亚']
#去除国外的列表
droped = []
for area in area_name:
    for unarea in unchina:
        if unarea in area:
            droped.append(area) #将国外的地名添加到去除列表中
    #地名为两个字的，不在去除列表中就添加到国内2字地名列表中
    if len(area)==2 and area not in droped: area_len_2.append(area) # 我国共有34个省级行政区域，包括23个省，5个自治区，4个直辖市，2个特别行政区。
    if len(area)==3 and area not in droped: area_len_3.append(area)
    if len(area)==4 and area not in droped: area_len_4.append(area)
    if len(area)>=5 and area not in droped: area_len_5.append(area)
# print(len(droped),'\n', droped)
# print(len(area_len_2),'\n', area_len_2)
# print(len(area_len_3),'\n', area_len_3)
# print(len(area_len_4),'\n', area_len_4)
# print(len(area_len_5),'\n', area_len_5)

#国内所有的省份自治区地名
prolist='北京市，天津市，上海市，重庆市，河北省，山西省，辽宁省，吉林省，江苏省，浙江省，安徽省，福建省，\
江西省，山东省，河南省，湖北省，湖南省，广东省，海南省，四川省，贵州省，云南省，陕西省，甘肃省，\
青海省，台湾省，广西，西藏，宁夏，新疆，香港，澳门，内蒙古，黑龙江省'
prolist=prolist.replace('市','').replace('省','').split('，')  #还是分中英文的，
print(len(prolist),prolist)

#提取省份
def get_pro(area_name):
    for pro in prolist:
        if pro in area_name:
            return pro
    return '海外'
df['pro'] = df.area.apply(get_pro)
print(df[['area','pro']])

#统计数据
pro_count=df.groupby('pro')['pro'].count().sort_values(ascending=False)
print(pro_count)

#绘制图表
#省份分布柱状图
bar=Bar('省份分布')
bar.use_theme("macarons") # 换主题
bar.add('省份',
        pro_count.index,
        pro_count.values,
        is_label_show=True,
        xaxis_interval=0,
        xaxis_rotate=45     #横坐标文字旋转45度
        )
env=create_default_environment('html')
env.render_chart_to_file(bar,path='bar.html')

#省份分布地图
map=Map('省份分布地图',width=1000,height=600)
map.add('',
        pro_count.index,
        pro_count.values,
        maptype='china',
        is_visualmap=True,
        visual_range=[0,400],       #数据范围0-400
        is_map_symbol_show=False,    #是否显示地图标记红点，默认为True。
        visual_text_color='#000',   #地图颜色
        is_label_show=True
        )
env.render_chart_to_file(map,path='map.html')
