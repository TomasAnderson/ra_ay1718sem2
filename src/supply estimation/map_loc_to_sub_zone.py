import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import csv
from shapely.geometry import shape
import os



def add_subzone_col(filename):
    print("processing %s..."%filename)
    with open(input_dir+filename) as f:
        with open(out_dir+filename, 'w') as out_f:
            header = f.readline()
            header = header.strip()
            out_f.write(header+",SUBZONE_N\n")

            for row in f.readlines():
                x, y = row.split(",")[3:5]
                point = Point(tuple([float(x), float(y)]))
                mapped = False
                result = ""
                for i, area in enumerate(poly['geometry']):
                    if point.within(area):
                        result = poly.loc[i, 'SUBZONE_N']
                        mapped = True
                if mapped:
                    row = row.strip()
                    out_f.write("%s,%s\n"%(row, result))



def main():
    filenames = []
    for f in os.listdir(input_dir):
        if ".csv" in f:
            filenames.append(f)

    for f in filenames:
        add_subzone_col(f)


if __name__ == '__main__':
    input_dir = "/Volumes/WD/zhouyou/comfort_april/free_veh/"
    out_dir = "/Volumes/WD/zhouyou/comfort_april/free_veh_with_loc/"
    poly = gpd.read_file('/Users/zhouyou/Workspace/RA/code/lib/sub_zone/central_sub_zone.shp')
    poly = poly.loc[:, ['SUBZONE_N', 'geometry']]
    poly = poly.to_crs(epsg=4326)
    main()

