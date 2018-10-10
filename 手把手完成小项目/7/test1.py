# -*- coding: utf-8 -*-
import pandas as pd
import requests,json

'''经纬度获取及BDP可视化'''
df=pd.read_csv('Sina_Finance_Comments_All_20180811_Cleaned.csv',encoding='utf-8')
# print(df.head(2))

#获取经纬度
def area2coor(area):
    ak = 'ZyvfwDxPTS1nBeLq9CeMXMNA3ApOB4MQ' # 应用列表里访问应用（AK）的一串字符
    try:
        # http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding
        address = area
        url = 'http://api.map.baidu.com/geocoder/v2/?address=' + address  + '&output=json&ak=' + ak
        text=requests.get(url = url)
        json_data = text.json()
        coor_loc = json_data['result']['location']
        return coor_loc
    except:
        return "nocoor" # 不换ak多半都是 'nocoor'

# print(df.loc[0,'area'])
# print(area2coor(df.loc[0,'area']))
#创建经纬度列
df['coor_loc']=df.area.apply(area2coor)
print(df.coor_loc)

#拆分经度纬度
df_coor=df[df['coor_loc']!='nocoor']    #选出非‘nocoor’的数据
df_coor['lng']=df_coor['coor_loc'].apply(lambda x:x['lng']) #经度
df_coor['lat']=df_coor['coor_loc'].apply(lambda x:x['lat']) #维度
print(df_coor[['lng','lat']])
df_coor.to_csv('Sina_Finance_Comments_All_20180811_toBDP.csv',encoding='utf-8',line_terminator='\r\n')
