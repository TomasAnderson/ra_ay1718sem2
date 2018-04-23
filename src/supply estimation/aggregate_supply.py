import os
import pandas as pd
from datetime import datetime
import geopandas as gpd
import numpy as np

def aggregate_supply(filename, interval):
    date = datetime.strptime(filename.split("_")[2], "%Y%m%d")
    zone2supply = dict.fromkeys(SUBZONES, 0)


    with open(input_dir+filename) as input_f:
        input_f.readline()
        for line in input_f.readlines():
            zone = line.split(",")[-1]
            zone = zone.strip()
            zone2supply[zone] = zone2supply[zone] + 1

    write_result(zone2supply, date, interval)

def write_header(interval):
    header = "date,%s\n" % ",".join(SUBZONES)
    with open(out_dir+interval+".csv", 'w') as out_f:
        out_f.write(header)

def write_result(zone2supply, date, interval):
    date= date.date()
    supply_list = ",".join([str(zone2supply[z]) for z in SUBZONES])
    with open(out_dir+interval+".csv", 'a') as out_f:
        out_f.write("%s,%s\n"%(date,supply_list))



def calculate_supply(filenames, interval):
    write_header(interval)
    for f in filenames:
        aggregate_supply(f, interval)



def output_summary():
    intervals = ["00", "05", "10", "15", "20", "25"]
    output_df = pd.DataFrame()
    output_df["Subzone"] = SUBZONES

    for interval in intervals:
        df = pd.read_csv(out_dir+interval+".csv")
        weekday_list = filter(lambda x: datetime.strptime(x, "%Y-%m-%d").weekday(), list(df['date']))
        df = df.loc[df['date'].isin(weekday_list)]
        mean_list, std_list = [], []
        for zone in SUBZONES:
            mean_list.append(np.mean(df[zone]))
            std_list.append(np.std(df[zone]))
        output_df["8:"+interval + " mean"] = mean_list
        output_df["8:"+interval + " std"] = std_list

    output_header = "subzone,8:00-8:05 mean,8:00-8:05 std,8:05-8:10 mean,8:05-8:10 std,8:10-8:15 mean,8:10-8:15 std,8:15-8:20 mean,8:15-8:20 std,8:20-8:25 mean,8:20-8:25 std,8:25-8:30 mean,8:25-8:30 std"
    output_df.to_csv(out_dir+"summary.csv", header=output_header, index=False)
def main():
    filenames = []
    for f in os.listdir(input_dir):
        if ".csv" in f:
            filenames.append(f)
    intervals = ["00", "05", "10", "15", "20", "25"]
    for interval in intervals:
        files = filter(lambda x: interval in x.replace(".csv","").split("_")[4], filenames)
        calculate_supply(files, interval)

    output_summary()


if __name__ == '__main__':
    input_dir = "/Volumes/WD/zhouyou/comfort_april/free_veh_with_loc/"
    out_dir = "/Volumes/WD/zhouyou/comfort_april/summary/"


    poly = gpd.read_file('/Users/zhouyou/Workspace/RA/code/lib/sub_zone/central_sub_zone.shp')
    poly = poly.loc[:, ['SUBZONE_N', 'geometry']]
    SUBZONES = [str(s) for s in list(set(poly["SUBZONE_N"]))]

    main()
