# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 12:23:42 2017

@author: 88947
"""

import os
import pandas as pd
import numpy as np
import re
from math import isnan

##input your own directory
path = 'E:\\Comfort\\street_hail_trips'


os.chdir(path)
##if it's first time to process the data
#os.mkdir(os.path.join(path,'processed_data'))
##if it's not first time to process the data
#

##integrate all the data need to be processed
files=os.listdir()
all_data=[]
for i in files:
    if re.match('street_hail_trips_201.*',i) is not None:
        all_data.append(i)
    
##load zoning data    
df = pd.read_csv('E:\\Comfort\\post_code_to_zones.csv',index_col='post_code')
title = ['order_id','vehicle_id','driver_id','origin_code','destination_code','trip_fare','distance','start_time','end_time']

##can start loop from here
for data in all_data[0:2]: ##can choose how many csv files to process by setting[]
    file = pd.read_csv(data,names=title)
    origin = pd.to_numeric(file['origin_code'],errors='coerce')
    dest = pd.to_numeric(file['destination_code'],errors='coerce')
    
    origzone=[]
    for i in origin:
        if (not isnan(i))&(i in df.index):
            origzone.append(df.loc[i,'PLN_AREA_N'])
        else:
            origzone.append('NaN')
            
    destzone=[]
    for j in dest:
        if (not isnan(j))&(j in df.index):
            destzone.append(df.loc[j,'PLN_AREA_N'])
        else:
            destzone.append('NaN')
            
    file.loc[:,'origin_zone']=origzone
    file.loc[:,'destination_zone']=destzone        
    file.to_csv(os.path.join(path,'processed_data',data),index=False,header=True,mode='a+')       

