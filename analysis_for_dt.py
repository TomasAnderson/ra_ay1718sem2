# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 22:39:07 2018

@author: 88947
"""

import os
import pandas as pd
import numpy as np
import time
import datetime
import csv
import math

path ='E:/Comfort'
os.chdir(path)
files = [x for x in os.listdir(path+'/street_hail_trips') if x.startswith('street')]

ref = pd.read_csv('post_code_to_zones.csv')
downtown = ref.loc[ref['PLN_AREA_N']=='DOWNTOWN CORE','post_code']


##pandas method for daily granularity
title = ['orig','dest','fare','distance','start','end']
origincount = []
destcount = []
withincount = []
for each in files[31:121]:
    df = pd.read_csv('E:/Comfort/street_hail_trips/'+each,header=None,names =title,usecols=[3,4,5,6,7,8])
    df['orig']=pd.to_numeric(df['orig'],errors='corece')
    df['dest']=pd.to_numeric(df['dest'],errors='corece')
    thisdate =datetime.datetime.strptime(each.split('_')[-2],'%Y%m%d')
    ##清理日期&只选定高峰时刻进出dt的
    cleandate=[]
    for i in np.arange(0,len(df),1):
        try:
            recordtime1 = datetime.datetime.strptime(df.loc[i,'start'],'%d/%m/%Y %H:%M:%S')
            recordtime2 = datetime.datetime.strptime(df.loc[i,'end'],'%d/%m/%Y %H:%M:%S')
        except:
            cleandate.append(False)
            continue
        try:
            cleandate.append((-2< (thisdate-recordtime1).days <2) and (-2< (thisdate-recordtime2).days<2)\
                             and 8<=recordtime1.hour<10 and 8<=recordtime2.hour<10)
        except:
            cleandate.append(False) 
    origincount.append(sum(df['orig'].isin(downtown)&cleandate))
    destcount.append(sum(df['dest'].isin(downtown)&cleandate))
    withincount.append(sum(df['orig'].isin(downtown) & cleandate & df['dest'].isin(downtown)))
    print(withincount[-1])
    #df = df.loc[cleandate,:]
    #out = df.loc[df['orig'].isin(downtown),:]
    #enter = df.loc[df['dest'].isin(downtown),:]

result = pd.DataFrame({'o' : origincount,'d' : destcount,'w' : withincount})
result.to_csv('E:/Comfort/street_hail_trips/first_month.csv',index=False)


##15-mins granularity

def q_fold(x):
    fold=round((datetime.datetime.strptime(x,'%d/%m/%Y %H:%M:%S').minute)/15+ ((datetime.datetime.strptime(x,'%d/%m/%Y %H:%M:%S').hour-8)*4))
    return fold



final_result={}
final_result1={}
for each in files[1:30]:
    df = pd.read_csv('E:/Comfort/street_hail_trips/'+each,header=None,names =title,usecols=[3,4,5,6,7,8])
    df['orig']=pd.to_numeric(df['orig'],errors='corece')
    df['dest']=pd.to_numeric(df['dest'],errors='corece')
    thisdate =datetime.datetime.strptime(each.split('_')[-2],'%Y%m%d')
    ##清理日期&只选定高峰时刻进出dt的
    cleandate=[]
    for i in np.arange(0,len(df),1):
        try:
            recordtime1 = datetime.datetime.strptime(df.loc[i,'start'],'%d/%m/%Y %H:%M:%S') #'%d/%m/%Y %H:%M:%S'
            recordtime2 = datetime.datetime.strptime(df.loc[i,'end'],'%d/%m/%Y %H:%M:%S') #'%d/%m/%Y %H:%M:%S'
        except:
            cleandate.append(False)
            continue
        try:
            cleandate.append((-2< (thisdate-recordtime1).days <2) and (-2< (thisdate-recordtime2).days<2)\
                             and 8<=recordtime1.hour<10 and 8<=recordtime2.hour<10)
        except:
            cleandate.append(False) 
    origin = df.loc[df['orig'].isin(downtown)&cleandate, ['orig','dest','start','end'] ]
    origin['15_min']=origin.loc[:,'start'].apply(q_fold)
    q_result = origin.loc[:,['dest','15_min']].groupby('15_min').count()
    final_result[each.split('_')[-2]]=q_result.loc[:,'dest']
    destination = df.loc[df['dest'].isin(downtown)&cleandate, ['orig','dest','start','end'] ]
    destination['15_min']=destination.loc[:,'end'].apply(q_fold)
    q_result1 = destination.loc[:,['dest','15_min']].groupby('15_min').count()
    final_result1[each.split('_')[-2]]=q_result1.loc[:,'dest']
    print(final_result1[each.split('_')[-2]])

##result是orig，result1是dest
with open ('E:/Comfort/street_hail_trips/15min_results1.csv','w') as csv_file:
    writer = csv.writer(csv_file)
    for key,value in final_result1.items():
        list_value = value.tolist()
        writer.writerow(list_value)


##where are the orders coming from
#os.mkdir('E:\Comfort\street_hail_trips\dt_location_results')
        
        
##sub_zone_mapping

ref = pd.read_csv('E:\Comfort\street_hail_trips\dt_result_ge.csv')
subzone = pd.read_csv('E:\Comfort\street_hail_trips\sub_zone_mapping.csv')
re = pd.merge(ref,subzone,how='inner',on='combined').iloc[:,[0,11]]
df = pd.read_csv('E:\Comfort\street_hail_trips\dt_result.csv',names=title)
df['orig']=pd.to_numeric(df['orig'],errors='corece')
df['dest']=pd.to_numeric(df['dest'],errors='corece')
df = pd.merge(df,re,how='inner',left_on='orig',right_on='PICKUP_POS')
df = pd.merge(df,re,how='inner',left_on='dest',right_on='PICKUP_POS')
out = df.loc[df['orig'].isin(downtown)& (~ df['dest'].isin(downtown)),:]
into = df.loc[df['dest'].isin(downtown)& (~ df['orig'].isin(downtown)),:]
within = df.loc[df['orig'].isin(downtown)& ( df['dest'].isin(downtown)),:]
out.to_csv('out.csv',index=False)
into.to_csv('into.csv',index=False)
within.to_csv('within.csv',index=False)



title = ['orig','dest','fare','distance','start','end']
result_in={}
result_out={}
for each in files[1:11]:
    df = pd.read_csv('E:/Comfort/street_hail_trips/'+each,header=None,names =title,usecols=[3,4,5,6,7,8])
    df['orig']=pd.to_numeric(df['orig'],errors='corece')
    df['dest']=pd.to_numeric(df['dest'],errors='corece')
    thisdate =datetime.datetime.strptime(each.split('_')[-2],'%Y%m%d')
    ##清理日期&只选定高峰时刻进出dt的
    cleandate=[]
    for i in np.arange(0,len(df),1):
        try:
            recordtime1 = datetime.datetime.strptime(df.loc[i,'start'],'%d/%m/%Y %H:%M:%S')
            recordtime2 = datetime.datetime.strptime(df.loc[i,'end'],'%d/%m/%Y %H:%M:%S')
        except:
            cleandate.append(False)
            continue
        try:
            cleandate.append((-2< (thisdate-recordtime1).days <2) and (-2< (thisdate-recordtime2).days<2)\
                             and 8<=recordtime1.hour<10 and 8<=recordtime2.hour<10)
        except:
            cleandate.append(False) 
    df = df.loc[cleandate, ['orig','dest'] ] #'start','end'
    coming_in = df.loc[df['dest'].isin(downtown),:].groupby('orig').count().sort_values('dest',ascending=True).tail().index
    going_out = df.loc[df['orig'].isin(downtown),:].groupby('dest').count().sort_values('orig',ascending=True).tail().index
    result_in[each.split('_')[-2]] = coming_in
    result_out[each.split('_')[-2]] = going_out
    print (result_out[each.split('_')[-2]])

with open ('E:/Comfort/street_hail_trips/dt_location_results/result_out.csv','w') as csv_file:
    writer = csv.writer(csv_file)
    for key,value in result_out.items():
        list_value = value.tolist()
        writer.writerow(list_value)


##I/O method
downtown = [str(x) for x in downtown]  
count = 0
for each in files[0:1]:
    with open('E:/Comfort/street_hail_trips/'+each) as table:
        rows = csv.reader(table)
        curdate=datetime.datetime.strptime(each.split('_')[-2],'%Y%m%d')
        for row in rows:
            try:
                start = datetime.datetime.strptime(row[7],'%d/%m/%Y %H:%M')
                end = datetime.datetime.strptime(row[8],'%d/%m/%Y %H:%M')
            except:
                continue
            if ((row[3] in downtown) or (row[4] in downtown))and\
            ((8<=start.hour<=10) or (8<=end.hour<=10)) and\
            ((-2<(curdate - start).days<2) and (-2<(curdate - end).days<2)):
                with open('E:/Comfort/street_hail_trips/dt_result.csv','a+') as result:
                    result.write(row[3]+','+row[4]+','+row[5]+','+row[6]+','+row[7]+','+row[8] +'\n')
                    count += 1
                    
       

