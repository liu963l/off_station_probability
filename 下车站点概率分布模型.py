# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 15:09:50 2018

@author: Liu-pc
"""



import numpy as np
import pandas as pd
data = np.array([[3,0],
                 [5,2],
                 [4,3],
                 [6,5],
                 [0,8]])
#data为上下车数据


def last(data,station):
    #计算车上剩余多少人
    f= []
    f.append(data[0,0] - data[0,1])
    for i in range(1,station):
        f.append(f[-1] + data[i,0] - data[i,1])
    return f



def leav_num(data,station):
    #计算下车人数,从A站到B站,data为上下车人数原始数据
    leav_people = last(data,station)
    
    m = {}
    for i in range(station):
        if i == 0 :
            l = []
            #l.append(data[1,1]) #第二站的下车人数是从第一站上车的
            for j  in range(i +1 ,station):
                l.append((data[i,0]- float(sum(l)))/leav_people[j-1]* data[j, 1])
        else:
            l = []
            for j  in range(i +1 ,station):
                l.append((data[i,0]- sum(l))/leav_people[j-1]* data[j, 1])
        m[i] = l
    
    return m


def frq(num):
    #计算下车概率
    m = {}
    for i in num.keys():
        l = []
        for j in num[i]:
            l.append(j/sum(num[i]))
            #print '%s >> %s: %s' %(i,j,j/sum(num[i])
        m[i] = l
    return m


D = result[['ON_STATIONID','OFF_STATIONID']][102:153].fillna(0)
D = np.array(D)

d1 = frq(leav_num(D,51))








##上述方法建立在，各个站点之间没有特殊的吸引权重情况下的，单纯数学概率
##是根据车辆上,累计了多少某一站点的人,车上的总人数，以及下车人数共同确定的
##如果考虑到某两个站点的吸引权重，那么将重新考虑下车的概率（关键在于如何确定吸引权重，这个权重的确定是指某一个站点）


'''
可以尝试分析一条线路的上下车



'''


######################已知IC卡数据，求OD矩阵########################################
data = pd.read_csv("H:\\data\\973_data.csv",encoding = 'gbk')
data = data[data['LOC_TREND'] == 1]    

data['ON_STATION_TIME']  = pd.to_datetime(data['ON_STATION_TIME'])

data['on_hour'] = map(lambda x :x.hour, data['ON_STATION_TIME'] )

data.groupby('on_hour')['on_hour'].agg('count').plot()

#step1绘制不同时段的流量图，大概看出高峰、平峰时段,可以综合多天的，出一张图

data_1 = data[(data['on_hour']>=7)&(data['on_hour']<=9)]   #早高峰
data_1['banci_vehic'] = map(lambda x,y: (x,y), data_1['VEHICLE_CODE'],data_1['BANCIID'])
data_1_banci = pd.DataFrame(pd.unique(data_1['banci_vehic']))  #运行班次
data_1_banci['veh'] = map(lambda x: x[0], data_1_banci[0])
data_1_banci['banci'] = map(lambda x: x[1], data_1_banci[0])
data_11 = pd.merge(data, data_1_banci, left_on = ['VEHICLE_CODE','BANCIID'] , right_on = ['veh','banci'],how = 'outer').dropna()
#找到在早高峰期间运行的班次，提取这些班次数据，作为早高峰线路刷卡数据，进行之后的OD分析

data_2 = data[(data['on_hour']>=10)&(data['on_hour']<=17)]  #平峰
data_2['banci_vehic'] = map(lambda x,y: (x,y), data_2['VEHICLE_CODE'],data_2['BANCIID'])
data_2_banci = pd.DataFrame(pd.unique(data_2['banci_vehic']))  #运行班次
data_2_banci['veh'] = map(lambda x: x[0], data_2_banci[0])
data_2_banci['banci'] = map(lambda x: x[1], data_2_banci[0])
data_22 = pd.merge(data, data_2_banci, left_on = ['VEHICLE_CODE','BANCIID'] , right_on = ['veh','banci'],how = 'outer').dropna()


data_3 = data[(data['on_hour']>=18)&(data['on_hour']<=20)]  #小高峰
data_3['banci_vehic'] = map(lambda x,y: (x,y), data_3['VEHICLE_CODE'],data_3['BANCIID'])
data_3_banci = pd.DataFrame(pd.unique(data_3['banci_vehic']))  #运行班次
data_3_banci['veh'] = map(lambda x: x[0], data_3_banci[0])
data_3_banci['banci'] = map(lambda x: x[1], data_3_banci[0])
data_33 = pd.merge(data, data_3_banci, left_on = ['VEHICLE_CODE','BANCIID'] , right_on = ['veh','banci'],how = 'outer').dropna()


#step2 计算od矩阵
def od_matrix(data,station_num = 51):
    #计算出od矩阵
    l = []
    for i in range(station_num):
        l = l + [0]*( i + 1 )
        for j in range(i + 1,station_num):
            l.append(len(data[(data['ON_STATIONID']==i)&(data['OFF_STATIONID']==j)]))
    l = np.array(l).reshape(station_num,station_num)
    return l
    


#a = od_matrix(data, 51)  
'''
#这一步可能需要比较长的时间，因为要分班次，就算每班车od   
data1_od_every = data_11.groupby(['VEHICLE_CODE','BANCIID']).apply(od_matrix)

data1_od_every = dict(data1_od_every)
'''

###step3 高峰时段od矩阵绘图
data1_all = od_matrix(data_11, 51) 


import matplotlib.pyplot as plt 
fig = plt.figure() #调用figure创建一个绘图对象 
ax = fig.add_subplot(111) 
cax = ax.matshow(data1_all, vmin=0, vmax=265) #绘制热力图，从-1到1 
fig.colorbar(cax) #将matshow生成热力图设置为颜色渐变条 
ticks = np.arange(0,51,5)#生成0-9，步长为1 
ax.set_xticks(ticks) #生成刻度 
ax.set_yticks(ticks) 
ax.set_xticklabels(range(1,52,5)) #生成x轴标签
ax.set_yticklabels(range(1,52,5))
plt.show()

#step4 平峰时段矩阵绘图


data2_all = od_matrix(data_22, 51) 


import matplotlib.pyplot as plt 
fig = plt.figure() #调用figure创建一个绘图对象 
ax = fig.add_subplot(111) 
cax = ax.matshow(data2_all, vmin=0, vmax=240) #绘制热力图，从-1到1 
fig.colorbar(cax) #将matshow生成热力图设置为颜色渐变条 
ticks = np.arange(0,51,5)#生成0-9，步长为1 
ax.set_xticks(ticks) #生成刻度 
ax.set_yticks(ticks) 
ax.set_xticklabels(range(1,52,5)) #生成x轴标签
ax.set_yticklabels(range(1,52,5))
plt.show()



data3_all = od_matrix(data_33, 51) 
import matplotlib.pyplot as plt 
fig = plt.figure() #调用figure创建一个绘图对象 
ax = fig.add_subplot(111) 
cax = ax.matshow(data3_all, vmin=0, vmax=40) #绘制热力图，从-1到1 
fig.colorbar(cax) #将matshow生成热力图设置为颜色渐变条 
ticks = np.arange(0,51,5)#生成0-9，步长为1 
ax.set_xticks(ticks) #生成刻度 
ax.set_yticks(ticks) 
ax.set_xticklabels(range(1,52,5)) #生成x轴标签
ax.set_yticklabels(range(1,52,5))
plt.show()



###################数据中的上下车量########################################


###################数据中的上下车量，得到原始数据########################################


data_on_off = data.groupby(['LINE_CODE','BANCIID','ON_STATIONID','VEHICLE_CODE'])['ON_STATIONID'].count()

data_on_off1 = data.groupby(['LINE_CODE','BANCIID','OFF_STATIONID','VEHICLE_CODE'])['OFF_STATIONID'].count()


data_on_off = pd.DataFrame(data_on_off)
data_on_off1 = pd.DataFrame(data_on_off1)

data_on_off['banci'] = map(lambda x:x[1], data_on_off.index)
data_on_off['station'] = map(lambda x:x[2], data_on_off.index)
data_on_off['VEHICLE_CODE'] = map(lambda x:x[3], data_on_off.index)


data_on_off1['banci'] = map(lambda x:x[1], data_on_off1.index)
data_on_off1['station'] = map(lambda x:x[2], data_on_off1.index)
data_on_off1['VEHICLE_CODE'] = map(lambda x:x[3], data_on_off1.index)

d = pd.merge(data_on_off, data_on_off1 , on = ['banci', 'station', 'VEHICLE_CODE'], how = 'outer')

d = d.sort_values(['VEHICLE_CODE','banci', 'station'])
d.index = range(len(d))


def add_station(d,station_num):
    #添加没有上车的为0
    if len(d) == station_num:
        return d
    else:
        l = set(range(station_num )) - set(list(d['station']))
        l = list(l)
        add_data = pd.DataFrame({'ON_STATIONID':0,'banci': d['banci'][0], 'station': l, 'VEHICLE_CODE': d['VEHICLE_CODE'][0], 'OFF_STATIONID':0})
        return  pd.concat([d,add_data]).sort_values('station')
    
d = dict(list(d.groupby(['VEHICLE_CODE','banci'])))
    

result = pd.DataFrame()   #补充站点后的数据
for i in d.keys():
    d[i].index = range(len(d[i]))
    result = pd.concat([result,add_station(d[i],51)])
    

result.index = range(len(result))
#result 为每一班次的od


on_off = pd.DataFrame()
on_off['O'] = result.groupby(['station'])['ON_STATIONID'].sum()
on_off['D'] = result.groupby(['station'])['OFF_STATIONID'].sum()
on_off_num = on_off[0:51]


#on_off_num为上下车人数

############################应用上述函数计算概率#

on_off = np.array(on_off_num)
on_off = frq(leav_num(on_off,51))



on_off_phb = pd.DataFrame()
for i in range(51):
    l = []
    l = [0] *(i+1) + on_off[i]
    on_off_phb[i] = l

on_off_phb = np.array(on_off_phb).T

#on_off_phb为根据均一假设计算的上下车概率


od_num = od_matrix(data, 51)
#od_num 为从原始数据中提出的od矩阵




###将直接计算的概率应用到上下车人数上，得到一个od矩阵跟原始数据的od矩阵对比

od_phb_num = (on_off_phb.T*np.array(on_off_num['O'])).T


'''
od_error = np.empty([51,51])

for i in range(51):
    for j in range(51):
        od_error[i,j] = abs(od_phb_num[i,j] - od_num[i,j])
        #得到误差矩阵



import matplotlib.pyplot as plt 
fig = plt.figure() #调用figure创建一个绘图对象 
ax = fig.add_subplot(111) 
cax = ax.matshow(od_num , vmin=0, vmax=275) #绘制热力图，从-1到1 
fig.colorbar(cax) #将matshow生成热力图设置为颜色渐变条 
ticks = np.arange(0,51,5)#生成0-9，步长为1 
ax.set_xticks(ticks) #生成刻度 
ax.set_yticks(ticks) 
ax.set_xticklabels(range(1,52,5)) #生成x轴标签
ax.set_yticklabels(range(1,52,5))
plt.show()


'''


#####根据沉降量类来修正

















