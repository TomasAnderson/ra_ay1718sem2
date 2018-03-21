import os
import pandas as pd
from datetime import datetime
def aggregate_supply(filename):
    zone2supply_08 = dict.fromkeys(SUBZONE, 0)
    zone2supply_11 = dict.fromkeys(SUBZONE, 0)


    with open(input_dir+filename) as input_f:
        input_f.readline()
        for line in input_f.readlines():
            zone = line.split(",")[-1]
            zone = zone.strip()

            dt = line.split(",")[1]
            dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S") # 2016-12-31 08:02:40
            hour = dt.hour
            if hour == 8:
                zone2supply_08[zone] = zone2supply_08[zone]+1
            else:
                zone2supply_11[zone] = zone2supply_11[zone]+1

    dt = datetime.strptime(filename.replace(".csv", ""), "%Y-%m-%d")

    write_result(zone2supply_08, zone2supply_11, dt)

def write_header():
    header = "date,weekday,time,SUBZONE_N,supply\n"
    with open(out_dir+"dec_08.csv", 'w') as out_f:
        out_f.write(header)
    with open(out_dir+"dec_11.csv", 'w') as out_f:
        out_f.write(header)

def write_result(zone2supply_08, zone2supply_11, dt):
    date, weekday, time1, time2 = dt.date(), dt.weekday(), "8:00-8:05", "10:55-11:00"

    with open(out_dir+"dec_08.csv", 'a') as out_f:
        for area in zone2supply_08:
            out_f.write("%s,%s,%s,%s,%s\n"%(date,weekday,time1,area,zone2supply_08[area]))

    with open(out_dir+"dec_11.csv", 'a') as out_f:
        for area in zone2supply_11:
            out_f.write("%s,%s,%s,%s,%s\n"%(date,weekday,time2,area,zone2supply_11[area]))

def main():
    filenames = []
    for f in os.listdir(input_dir):
        if ".csv" in f:
            filenames.append(f)

    write_header()

    for f in filenames:
        aggregate_supply(f)


if __name__ == '__main__':
    input_dir = "/Volumes/WD/zhouyou/vehicle_location/dec rda/free_veh_with_loc/"
    out_dir = "/Volumes/WD/zhouyou/vehicle_location/dec rda/summary/"

    df = pd.read_csv(input_dir+"2016-12-02.csv")
    SUBZONE = set(df["SUBZONE_N"])

    main()
