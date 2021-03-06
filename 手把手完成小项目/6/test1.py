# -*- coding: utf-8 -*-
import pandas as pd
from pyecharts import Bar,Geo
from pyecharts.engine import create_default_environment

'''城市提取与可视化'''
df=pd.read_csv('Sina_Finance_Comments_All_20180811_Cleaned.csv',encoding='utf-8')
# print(df[['area','ip_loc']])

#统计area
area_count=df.groupby('area')['area'].count().sort_values(ascending=False)
area_name=list(area_count.index)
area_values=area_count.values
print(len(area_name),len(area_values))
print(area_count)

#统计area为外国的数据添加到drop列表里
area_len_2 = []
area_len_3 = []
area_len_4 = []
area_len_5 = []
unchina = ['英国','美国','日本','瑞士','法国','瑞典','越南','泰国',
           '意大利','加拿大','菲律宾','新加坡','新西兰','伊拉克','爱尔兰','安哥拉',
           '澳大利亚', '大韩民国', '马来西亚']
droped = []
for area in area_name:
    for unarea in unchina:
        if unarea in area:
            droped.append(area)
    if len(area)==2 and area not in droped: area_len_2.append(area) # 我国共有34个省级行政区域，包括23个省，5个自治区，4个直辖市，2个特别行政区。
    if len(area)==3 and area not in droped: area_len_3.append(area)
    if len(area)==4 and area not in droped: area_len_4.append(area)
    if len(area)>=5 and area not in droped: area_len_5.append(area)
print(len(droped),'\n', droped)
# print(len(area_len_2),'\n', area_len_2)
# print(len(area_len_3),'\n', area_len_3)
# print(len(area_len_4),'\n', area_len_4)
# print(len(area_len_5),'\n', area_len_5)

#省份汇总
prolist = '北京市，天津市，上海市，重庆市，河北省，山西省，辽宁省，吉林省，江苏省，浙江省，安徽省，福建省，\
江西省，山东省，河南省，湖北省，湖南省，广东省，海南省，四川省，贵州省，云南省，陕西省，甘肃省，\
青海省，台湾省，广西，西藏，宁夏，新疆，香港，澳门，内蒙古，黑龙江省'
prolist = prolist.replace('市', '').replace('省', '').split('，')
print(len(prolist), prolist)

#城市提取
# 从 ECharts 官网的effectScatter-bmap示例中提取出城市列表，便于筛选。
# 当然事先并不知道这里的数据和本次评论的数据的匹配度多高，只能“实践出真知”。
geoCoordMap={
    '海门':[121.15,31.89],
    '鄂尔多斯':[109.781327,39.608266],
    '招远':[120.38,37.35],
    '舟山':[122.207216,29.985295],
    '齐齐哈尔':[123.97,47.33],
    '盐城':[120.13,33.38],
    '赤峰':[118.87,42.28],
    '青岛':[120.33,36.07],
    '乳山':[121.52,36.89],
    '金昌':[102.188043,38.520089],
    '泉州':[118.58,24.93],
    '莱西':[120.53,36.86],
    '日照':[119.46,35.42],
    '胶南':[119.97,35.88],
    '南通':[121.05,32.08],
    '拉萨':[91.11,29.97],
    '云浮':[112.02,22.93],
    '梅州':[116.1,24.55],
    '文登':[122.05,37.2],
    '上海':[121.48,31.22],
    '攀枝花':[101.718637,26.582347],
    '威海':[122.1,37.5],
    '承德':[117.93,40.97],
    '厦门':[118.1,24.46],
    '汕尾':[115.375279,22.786211],
    '潮州':[116.63,23.68],
    '丹东':[124.37,40.13],
    '太仓':[121.1,31.45],
    '曲靖':[103.79,25.51],
    '烟台':[121.39,37.52],
    '福州':[119.3,26.08],
    '瓦房店':[121.979603,39.627114],
    '即墨':[120.45,36.38],
    '抚顺':[123.97,41.97],
    '玉溪':[102.52,24.35],
    '张家口':[114.87,40.82],
    '阳泉':[113.57,37.85],
    '莱州':[119.942327,37.177017],
    '湖州':[120.1,30.86],
    '汕头':[116.69,23.39],
    '昆山':[120.95,31.39],
    '宁波':[121.56,29.86],
    '湛江':[110.359377,21.270708],
    '揭阳':[116.35,23.55],
    '荣成':[122.41,37.16],
    '连云港':[119.16,34.59],
    '葫芦岛':[120.836932,40.711052],
    '常熟':[120.74,31.64],
    '东莞':[113.75,23.04],
    '河源':[114.68,23.73],
    '淮安':[119.15,33.5],
    '泰州':[119.9,32.49],
    '南宁':[108.33,22.84],
    '营口':[122.18,40.65],
    '惠州':[114.4,23.09],
    '江阴':[120.26,31.91],
    '蓬莱':[120.75,37.8],
    '韶关':[113.62,24.84],
    '嘉峪关':[98.289152,39.77313],
    '广州':[113.23,23.16],
    '延安':[109.47,36.6],
    '太原':[112.53,37.87],
    '清远':[113.01,23.7],
    '中山':[113.38,22.52],
    '昆明':[102.73,25.04],
    '寿光':[118.73,36.86],
    '盘锦':[122.070714,41.119997],
    '长治':[113.08,36.18],
    '深圳':[114.07,22.62],
    '珠海':[113.52,22.3],
    '宿迁':[118.3,33.96],
    '咸阳':[108.72,34.36],
    '铜川':[109.11,35.09],
    '平度':[119.97,36.77],
    '佛山':[113.11,23.05],
    '海口':[110.35,20.02],
    '江门':[113.06,22.61],
    '章丘':[117.53,36.72],
    '肇庆':[112.44,23.05],
    '大连':[121.62,38.92],
    '临汾':[111.5,36.08],
    '吴江':[120.63,31.16],
    '石嘴山':[106.39,39.04],
    '沈阳':[123.38,41.8],
    '苏州':[120.62,31.32],
    '茂名':[110.88,21.68],
    '嘉兴':[120.76,30.77],
    '长春':[125.35,43.88],
    '胶州':[120.03336,36.264622],
    '银川':[106.27,38.47],
    '张家港':[120.555821,31.875428],
    '三门峡':[111.19,34.76],
    '锦州':[121.15,41.13],
    '南昌':[115.89,28.68],
    '柳州':[109.4,24.33],
    '三亚':[109.511909,18.252847],
    '自贡':[104.778442,29.33903],
    '吉林':[126.57,43.87],
    '阳江':[111.95,21.85],
    '泸州':[105.39,28.91],
    '西宁':[101.74,36.56],
    '宜宾':[104.56,29.77],
    '呼和浩特':[111.65,40.82],
    '成都':[104.06,30.67],
    '大同':[113.3,40.12],
    '镇江':[119.44,32.2],
    '桂林':[110.28,25.29],
    '张家界':[110.479191,29.117096],
    '宜兴':[119.82,31.36],
    '北海':[109.12,21.49],
    '西安':[108.95,34.27],
    '金坛':[119.56,31.74],
    '东营':[118.49,37.46],
    '牡丹江':[129.58,44.6],
    '遵义':[106.9,27.7],
    '绍兴':[120.58,30.01],
    '扬州':[119.42,32.39],
    '常州':[119.95,31.79],
    '潍坊':[119.1,36.62],
    '重庆':[106.54,29.59],
    '台州':[121.420757,28.656386],
    '南京':[118.78,32.04],
    '滨州':[118.03,37.36],
    '贵阳':[106.71,26.57],
    '无锡':[120.29,31.59],
    '本溪':[123.73,41.3],
    '克拉玛依':[84.77,45.59],
    '渭南':[109.5,34.52],
    '马鞍山':[118.48,31.56],
    '宝鸡':[107.15,34.38],
    '焦作':[113.21,35.24],
    '句容':[119.16,31.95],
    '北京':[116.46,39.92],
    '徐州':[117.2,34.26],
    '衡水':[115.72,37.72],
    '包头':[110,40.58],
    '绵阳':[104.73,31.48],
    '乌鲁木齐':[87.68,43.77],
    '枣庄':[117.57,34.86],
    '杭州':[120.19,30.26],
    '淄博':[118.05,36.78],
    '鞍山':[122.85,41.12],
    '溧阳':[119.48,31.43],
    '库尔勒':[86.06,41.68],
    '安阳':[114.35,36.1],
    '开封':[114.35,34.79],
    '济南':[117,36.65],
    '德阳':[104.37,31.13],
    '温州':[120.65,28.01],
    '九江':[115.97,29.71],
    '邯郸':[114.47,36.6],
    '临安':[119.72,30.23],
    '兰州':[103.73,36.03],
    '沧州':[116.83,38.33],
    '临沂':[118.35,35.05],
    '南充':[106.110698,30.837793],
    '天津':[117.2,39.13],
    '富阳':[119.95,30.07],
    '泰安':[117.13,36.18],
    '诸暨':[120.23,29.71],
    '郑州':[113.65,34.76],
    '哈尔滨':[126.63,45.75],
    '聊城':[115.97,36.45],
    '芜湖':[118.38,31.33],
    '唐山':[118.02,39.63],
    '平顶山':[113.29,33.75],
    '邢台':[114.48,37.05],
    '德州':[116.29,37.45],
    '济宁':[116.59,35.38],
    '荆州':[112.239741,30.335165],
    '宜昌':[111.3,30.7],
    '义乌':[120.06,29.32],
    '丽水':[119.92,28.45],
    '洛阳':[112.44,34.7],
    '秦皇岛':[119.57,39.95],
    '株洲':[113.16,27.83],
    '石家庄':[114.48,38.03],
    '莱芜':[117.67,36.19],
    '常德':[111.69,29.05],
    '保定':[115.48,38.85],
    '湘潭':[112.91,27.87],
    '金华':[119.64,29.12],
    '岳阳':[113.09,29.37],
    '长沙':[113,28.21],
    '衢州':[118.88,28.97],
    '廊坊':[116.7,39.53],
    '菏泽':[115.480656,35.23375],
    '合肥':[117.27,31.86],
    '武汉':[114.31,30.52],
    '大庆':[125.03,46.58]
}
citys=list(geoCoordMap.keys())
print(len(citys),'citys:',citys)

'''创建city列'''
prolist_less=[ '河北', '山西', '辽宁', '吉林', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '广西', '西藏', '宁夏', '新疆', '香港', '澳门', '台湾', '内蒙古', '黑龙江']
def get_city(area):
    #此处prolist_less不包括直辖市 ‘北京’，‘上海’，‘天津’，‘重庆’
    unchinas=['英国','美国','日本','瑞士','法国','瑞典','越南','泰国','意大利','加拿大','菲律宾','新加坡','新西兰','伊拉克','爱尔兰','安哥拉','澳大利亚', '大韩民国', '马来西亚']
    for city in citys:
        if city in area:
            return city
    for pro in prolist_less:
        if pro == area:
            return 'pro'
    for unchina in unchinas:
        if unchina in area:
            return 'unchina'
    return 'unknown'
df['city']=df.area.apply(get_city)
print(df[['area','city']])

#查看所有unknown的信息   非海外，也不是省份，而且不包含 ECharts 那些城市
df_unknown=df[['area','city']][df['city']=='unknown']
print(df_unknown.shape)
unknown_city=list(set(df_unknown.area.values.tolist()))
print(len(unknown_city),unknown_city)
#遍历unknown_city,去掉省份前缀，然后加到unknown列表中：
unkwns=[]
others=[]
for unkwn in unknown_city:
    for pro in prolist_less:
       if pro in unkwn: #青海海南藏族自治州
           unkwn=unkwn.replace(pro,'')
           unkwns.append(unkwn)
    if unkwn not in unkwns:
        others.append(unkwn)
print(len(unkwns))
print(unkwns)
# print(len(others))
# print(others)

#汇总所有城市
#将unkwns中含有xxx自治州的去掉后缀
unkwns = ['眉山', '漯河', '滁州', '景德镇', '随州', '遂宁', '三明', '乌兰察布', '吕梁', '莆田', '河池', '定西', '信阳', '阜新', '广元', '汉中', '辽阳', '邵阳', '萍乡', '晋中', '商洛', '乐山', '石河子', '白银', '池州', '内江', '恩施', '益阳', '伊犁', '张掖', '运城', '绥化', '崇左', '南阳', '达州', '海东', '伊春', '黄石', '龙岩', '蚌埠', '上饶', '驻马店', '保山', '呼伦贝尔', '安庆', '淮北', '周口', '孝感', '临沧', '固原', '钦州', '漳州', '巴音郭楞', '宜春', '朝阳', '鹰潭', '娄底', '雅安', '青海', '怀化', '郴州', '许昌', '红河', '赣州', '朔州', '普洱', '吴忠', '新乡', '资阳', '鸡西', '昌吉', '荆门', '六安', '黄山', '商丘', '武威', '抚州', '湘西', '怒江', '铁岭', '百色', '淮南', '广安', '铜陵', '濮阳', '天水', '襄阳', '南平', '阜阳', '鹤壁', '塔城', '宁德', '大理', '梧州', '衡阳', '晋城', '昭通', '黄冈', '永州', '毕节', '通辽', '玉林', '兴安盟', '咸宁']
all_citys=unkwns+citys
print(len(all_citys),'all_citys:',all_citys)

'''更新city列'''
#更新下数据里的city列，含有这些城市的就返回对应城市，否则不论国外还是省份都统一用others表示
def get_city(area):
    for city in all_citys:
        if city in area:
            return city
    return 'other'
df['city']=df.area.apply(get_city)
print(df[['area','city']])

#城市分布
city_count=df.groupby('city')['city'].count().sort_values(ascending=False)
print(city_count)

#柱状图分析
bar = Bar("城市分布")
bar.add("城市",
        city_count.index[:30],  #取前三十个数据
        city_count.values[:30], #取前三十个数据
        is_label_show=True,
        xaxis_interval=0,
        xaxis_rotate=-45)
env=create_default_environment('html')
env.render_chart_to_file(bar,path='bar.html')

# #组合成元祖，方便后续地图可视化传入数据
# city_data=list(zip(city_count.index,city_count.values))
# print(city_data)
#
# #地理坐标系Geo
# geo=Geo('城市分布情况','data from SinaNews',title_color='#fff',title_pos='center',
#         width=800,height=600,background_color='#404a59')
# attr,value=geo.cast(city_data)
# geo.add(
#     '',
#     attr,
#     value,
#     visual_range=[0,360],
#     visual_text_color="#fff",
#     symbol_size=10,     #标记图形大小，默认为12
#     is_visualmap=True,
# )
# env.render_chart_to_file(geo,path='geo.html')
#ValueError: No coordinate is specified for other
#说明pyecharts里没有other的经纬度信息
'''创建nocoor_list列表，用于存储所有报错的城市，反复运行下面两个 cell 的代码，
根据地图报错提醒，不断添加城市到nocoor_list列表中，就能得到全部的无经纬度的城市。
并将剩下没报错的都存储到city_data 列表中。'''
city_data=[]
nocoor_list=[
    'other','青海','达州','崇左','巴音郭楞','普洱','池州','湘西','伊犁','乌兰察布','临沧','海东','眉山',
    '怒江','固原','广安'
]
for item in zip(city_count.index,city_count.values):
    if item[0] in nocoor_list:
        continue    #跳出循环：即遇到不存在经纬度的城市就跳过，不用存储到city_data里面
    city_data.append(item)
print(city_data)
geo=Geo('城市分布情况','data from SinaNews',title_color='#fff',title_pos='center',
        width=800,height=600,background_color='#404a59')
attr,value=geo.cast(city_data)
geo.add(
    '',
    attr,
    value,
    visual_range=[0,360],
    visual_text_color="#fff",
    symbol_size=10,     #标记图形大小，默认为12
    is_visualmap=True,
)
env.render_chart_to_file(geo,path='geo.html')
