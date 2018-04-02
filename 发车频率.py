# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 14:18:05 2018

@author: Liu-pc
"""

import pandas as pd
from scipy.optimize import minimize
import matplotlib as plt
rou = pd.read_csv('C:\Users\Liu-pc\Desktop\simulation\\rou.csv')
speed = pd.read_csv('C:\Users\Liu-pc\Desktop\simulation\\speed.csv')
leave_time = pd.DataFrame({'stiation':range(1,12)})
'''
TS1_1 = 10   #第一班在第一站的停留时间
leave1_1 =0 + TS1_1
TT1_1_2  = 500.0/speed.loc[1,'speed_1'] # 第一班车在第一二站之间的行程时间

leave1_2 = leave1_1 + TT1_1_2 + 10
'''
#####第一班
leave = [0]
for i in range(10):
    n = int(leave[-1]/500) +1
    n = str('speed_%s') %n
    l = 500.0/speed.loc[i,n] + leave[i] +10
    leave.append(l)
    
leave_time['banci1'] = leave
#####第二班
leave = [550]
for i in range(10):
    n = int(leave[-1]/500) +1
    n = str('speed_%s') %n
    print n
    l = 500.0/speed.loc[i,n] + leave[i] + 10
    leave.append(l)
leave_time['banci2'] = leave
#####第三班
'''
leave = [1200]
for i in range(10):
    n = int(leave[-1]/500) +1
    n1 = str('speed_%s') %n
    s = str('time_%s') %n
    print n
    stop_time = (leave_time['banci2'][i] - leave_time['banci2'][i]) * rou[s][n]*2
    l = 500.0/speed.loc[i,n1] + leave[i] + stop_time
    leave.append(l)
leave_time['banci3'] = leave
'''
#####往后多算四班(第3,4,5,6)班，如果要算更多，请保持足够多的rou列【time_n。。。】
def leave_time_function(n_ban,station, leave_time):
    l = range(1100,8000,550)
    people_ = {}
    for i in range(n_ban):
        leave = [l[i]]
        people = 0
        for j in range(station-1):
            n = int(leave[-1]/600) + 1
            n1 = str('speed_%s') %n
            s = str('time_%s') %n
            b = str('banci%s') %(i+2)
            b1 = str('banci%s') %(i+1)
           # print n
            stop_time = (leave_time[b][j +1] - leave_time[b1][j +1 ]) * rou[s][j]*2/60
            people = people +  (leave_time[b][j +1] - leave_time[b1][j +1 ]) * rou[s][j]/60

            t = 500.0/speed.loc[j,n1] + leave[j] + stop_time
            #print t
            leave.append(t)
       # print i
        leave_time['banci%s' %(i+3)] = leave
        people_['banci%s' %(i+3)] = people
    return leave_time,people_

leave_time = leave_time_function(11,11,leave_time)

people = leave_time[1]
leave_time = leave_time[0]
  
plt.plot(leave_time['stiation'], leave_time['banci1'], color='y', linestyle='-', label='y2 data')       
plt.plot(leave_time['stiation'], leave_time['banci2'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci3'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci4'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci5'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci6'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci7'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci8'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci9'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci10'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci11'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci12'], color='y', linestyle='-', label='y2 data')
#plt.plot(leave_time['stiation'], leave_time['banci13'], color='y', linestyle='-', label='y2 data')
plt.xlabel('station')
plt.ylabel('time(s)')
#savefig('C:\Users\Liu-pc\Desktop\simulation\\origin.png', dpi=200)


def head1(data):
    dic = pd.DataFrame()
    h = []
    for j in range(11):
        n = j+1
        b = 'banci%i' %(n)
        b1 = 'banci%i' %(n+1)
        for k in range(11):
            r = data[b1][k] - data[b][k]
            h.append(r)
        dic[b] = h
        h = []
    return dic

first_Sc = head1(leave_time)

import numpy as np

class1 = []
for i in first_Sc.keys():
    class1.extend(list(first_Sc[i]))


class1 = np.array(class1)
np.std(class1)
np.mean(class1)


################################改变发车间隔


leave_time2 = pd.DataFrame({'stiation':range(1,12)})
'''
TS1_1 = 10   #第一班在第一站的停留时间
leave1_1 =0 + TS1_1
TT1_1_2  = 500.0/speed.loc[1,'speed_1'] # 第一班车在第一二站之间的行程时间

leave1_2 = leave1_1 + TT1_1_2 + 10
'''
#####第一班
leave = [0]
for i in range(10):
    n = int(leave[-1]/500) +1
    n = str('speed_%s') %n
    l = 500.0/speed.loc[i,n] + leave[i] +10
    leave.append(l)
    
leave_time2['banci1'] = leave
#####第二班
leave = [250]
for i in range(10):
    n = int(leave[-1]/500) +1
    n = str('speed_%s') %n
    print n
    l = 500.0/speed.loc[i,n] + leave[i] + 10
    leave.append(l)
leave_time2['banci2'] = leave





def leave_time_function(n_ban,station, leave_time):
    l = range(500,8000,250)
    people_ = {}
    for i in range(n_ban):
        leave = [l[i]]
        people = 0
        for j in range(station-1):
            n = int(leave[-1]/600) + 1
            n1 = str('speed_%s') %n
            s = str('time_%s') %n
            b = str('banci%s') %(i+2)
            b1 = str('banci%s') %(i+1)
           # print n
            stop_time = (leave_time[b][j +1] - leave_time[b1][j +1 ]) * rou[s][j]*2/60
            people = people +  (leave_time[b][j +1] - leave_time[b1][j +1 ]) * rou[s][j]/60

            t = 500.0/speed.loc[j,n1] + leave[j] + stop_time
            #print t
            leave.append(t)
       # print i
        leave_time['banci%s' %(i+3)] = leave
        people_['banci%s' %(i+3)] = people
    return leave_time,people_

leave_time2 = leave_time_function(11,11,leave_time2)

people2 = leave_time2[1]
leave_time2 = leave_time2[0]


second_Sc = head1(leave_time2)


class2 = []
for i in first_Sc.keys():
    class2.extend(list(second_Sc[i]))


class2 = np.array(class2)
np.std(class2)
np.mean(class2)


plt.plot(leave_time2['stiation'], leave_time2['banci1'], color='y', linestyle='-', label='y2 data')       
plt.plot(leave_time2['stiation'], leave_time2['banci2'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time2['stiation'], leave_time2['banci3'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time2['stiation'], leave_time2['banci4'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time2['stiation'], leave_time2['banci5'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time2['stiation'], leave_time2['banci6'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time2['stiation'], leave_time2['banci7'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time2['stiation'], leave_time2['banci8'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time2['stiation'], leave_time2['banci9'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time2['stiation'], leave_time2['banci10'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time2['stiation'], leave_time2['banci11'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time2['stiation'], leave_time2['banci12'], color='y', linestyle='-', label='y2 data')
#plt.plot(leave_time['stiation'], leave_time['banci13'], color='y', linestyle='-', label='y2 data')
plt.xlabel('station')
plt.ylabel('time(s)')





def gap_time():
    










################给出期望速度,以及在这个速度下的leave_time
'''
sqr = lambda p:(p-2)**2 
minimize(sqr, 2)


n = int(leave_time['banci2'][0] /600) + 1
t = str('time_%s') %n
n1 = int(leave_time['banci3'][0] /600) + 1
t1 = str('time_%s') %n1
n1 = int(leave_time['banci2'][0] /600) + 1
s = str('speed_%s') %n1

fun =lambda x : ((600 + (500.0/x- 500.0/speed.loc[0, s])- rou.loc[1, t]*2*(leave_time['banci2'][1] -leave_time['banci1'][1])/60.0)/(1- rou.loc[1, t1]*2/60.0) - 600)**2
sp = minimize(fun, 5).x[0]
#把sp带入可以得到2，3车在第2站的head，之后便可以带入下一次循环
head2_23 =  (600 + (500.0/sp- 500.0/speed.loc[0, s])- rou.loc[1, t]*2*(leave_time['banci2'][1] -leave_time['banci1'][1])/60)/(1- rou.loc[1, t1]*2/60)
#如果按照这个速度可以求出在下一站(2站)的leave_time，更新leave_time表
leave_time.loc[1,'banci3'] = leave_time.loc[1,'banci2'] + head2_23
#计算下一个站的期望速度，首先更新，t，t1，s#####################
n = int(leave_time['banci2'][1] /600) + 1
t = str('time_%s') %n
n1 = int(leave_time['banci3'][1] /600) + 1
t1 = str('time_%s') %n1
n1 = int(leave_time['banci2'][1] /600) + 1
s = str('speed_%s') %n1

fun =lambda x : ((head2_23 + (500.0/x- 500.0/speed.loc[0, s])- rou.loc[1, t]*2*(leave_time['banci2'][1] -leave_time['banci1'][1])/60)/(1- rou.loc[1, t1]*2/60) - 600)**2
sp = minimize(fun, 5).x[0]
'''
def updata_leavetime(leave_time,station_number, banci_number,):
    #总共多少站，计算第几班两个参数
    head2_23 = 600
    v = []
    for i in range(station_number):
        n = int(leave_time['banci%s' %(banci_number-1)][i] /600) + 1 
        t = str('time_%s') %n
        n1 = int(leave_time['banci%s' %(banci_number)][i] /600) + 1
        t1 = str('time_%s') %n1
        n1 = int(leave_time['banci%s' %(banci_number-1)][i] /600) + 1 
        s = str('speed_%s') %n1
        fun =lambda x : ((head2_23 + (500.0/x- 500.0/speed.loc[i, s])- rou.loc[i+1, t]*2*(leave_time['banci%s' %(banci_number-1)][i+1] -leave_time['banci%s' %(banci_number-2)][i+1])/60.0)/(1- rou.loc[i+1, t1]*2/60.0) - 600)**2 
        sp = minimize(fun, 5).x[0]
        v.append(sp)   
        head2_23 =  (head2_23 + (500.0/sp- 500.0/speed.loc[i, s])- rou.loc[i+1, t]*2*(leave_time['banci%s' %(banci_number-1)][i+1] -leave_time['banci%s' %(banci_number-2)][i+1])/60.0)/(1- rou.loc[i+1, t1]*2/60.0) 
        leave_time.loc[i + 1,'banci%s' %(banci_number)] = leave_time.loc[i+1,'banci%s' %(banci_number-1)] + head2_23 
        #leave_time.loc[i + 1,'banci%s' %(banci_number)] = leave_time.loc[i,'banci%s' %(banci_number)] + head2_23* rou.loc[i+1,t1]*2/60.0 + 500/sp

    return leave_time,v
    
leave_time_speed = leave_time.copy()
#leave_time_speed为按照期望速度调整好之后的
for i in range(3,13):
    leave_time_speed = updata_leavetime(leave_time_speed, 10, i)[0] 
