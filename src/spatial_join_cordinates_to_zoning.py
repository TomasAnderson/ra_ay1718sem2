# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 13:38:27 2017

@author: 88947
"""
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import fiona
from rtree import index
import csv
from shapely.geometry import shape
import os
import re

path = 'E:/Comfort'
os.chdir(path)
#os.mkdir('location_results')
filelist = []
for file in os.listdir(path+'/vehicle_location'):
    if file.startswith('vehicle_location'):
        filelist.append(file)
crs={'init':'epsg:4326'}

poly = gpd.read_file('E:/Comfort/spatial_reference/wgs84_1.shp')
poly = poly.loc[:,['PLN_AREA_N','geometry']]
poly.crs
idx = index.Index()
for pos in np.arange(0,len(poly),1):
    pol = poly.loc[pos,'geometry']
    idx.insert(pos, pol.bounds)

##faster way
for each in filelist:
    with open (path+'/vehicle_location/'+each) as f:

##trial with one single file
result = []
with open (path+'/vehicle_location/'+filelist[0]) as f:
     rows = csv.reader(f)
     for row in rows:
         point = Point(tuple([float(row[3]),float(row[4])]))
         for j in idx.intersection(point.bounds):
             if point.within(poly.loc[j,'geometry']):
                 result.append(poly.loc[j,'PLN_AREA_N'])
df = pd.read_csv(path+'/vehicle_location/'+filelist[0],header = None)
df.loc[:,'region']=result
df.to_csv('123.csv')


with open (path+'/vehicle_location/'+filelist[0]) as f:
     with open(path+'/location_results/result1.csv','w') as new:
         header = 'region\n'
         new.write(header)
         rows = csv.reader(f)
         for row in rows:
             point = Point(tuple([float(row[3]),float(row[4])]))
             for j in idx.intersection(point.bounds):
                 if point.within(poly.loc[j,'geometry']):
                     new.write(poly.loc[j,'PLN_AREA_N'] + '\n')

                     #new.write(row[0] + ',' + row[1] + ',' +row[2] + ',' + row[3] + ',' + row[4] + ',' + row[5] + ',' + poly.loc[j,'PLN_AREA_N'] + '\n')
                        
                      
                        
                

        
    
##geopandas
point = pd.read_csv('E:\\Comfort\\vehicle_location\\'+filelist[1],
                   usecols=[3,4],header = None,names=['lon','lat'],
                   dtype={'lat':np.float64,'lon':np.float64})

geometry = [Point(xy) for xy in zip(point.lon, point.lat)]



#其实可以不用这步
point = gpd.GeoDataFrame(point, crs=crs, geometry=geometry)
point.crs

poly = gpd.read_file('E:/Comfort/spatial_reference/wgs84_1.shp')
poly = poly.iloc[:,['PLN_AREA_N','geometry']]
poly.crs


##Method 1
idx = index.Index()
for pos in np.arange(0,len(poly),1):
    pol = poly.loc[pos,'geometry']
    idx.insert(pos, pol.bounds)

result=[]
for id in np.arange(0,len(point),1):
  poi = point.loc[id,'geometry']
  # iterate through spatial index
  for j in idx.intersection(poi.bounds):
      if poi.within(poly.loc[j,'geometry']):
            result.append(poly.loc[j,'PLN_AREA_N'])


##Method 2
gpd.sjoin(point,poly,how = 'inner',op = 'intersects')



##weather station mapping

path = 'E:/Comfort'
os.chdir(path)

poly = gpd.read_file('E:/Comfort/spatial_reference/wgs84_1.shp')
poly = poly.loc[:,['PLN_AREA_N','geometry']]
poly.crs
idx = index.Index()
for pos in np.arange(0,len(poly),1):
    pol = poly.loc[pos,'geometry']
    idx.insert(pos, pol.bounds)


with open (path+'/weather_station.csv') as f:
    with open (path + '/weather_station_mapping.csv','w',newline='') as output:
         rows = csv.DictReader(f)
         out_row = csv.writer(output)
         title = ['station_id','lat','lon','zone']
         out_row.writerow(title)
         for row in rows:
             point = Point(tuple([float(row['Longitude']),float(row['Latitude'])]))
             for j in idx.intersection(point.bounds):
                 if point.within(poly.loc[j,'geometry']):
                     row['area']=poly.loc[j,'PLN_AREA_N']
                     out_row.writerow(row.values())




