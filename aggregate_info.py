from os import path
from os import makedirs, listdir
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import gpxpy.geo
import geopandas as gpd


def load_ids():
    with open(path.join(DIR, "driver.txt")) as input:
        ids = [s.strip() for s in input.readlines()]
        return ids

def sort_by_time(ids):
    for id in ids:
        curr_dir = path.join(DIR, "driver_sample", id)
        raw_files = listdir(curr_dir)
        raw_files = list(filter(lambda s: ".csv" in s, raw_files))

        sorted_dir = path.join(curr_dir, "sorted")
        if not path.exists(sorted_dir):
            makedirs(sorted_dir)

        for f in raw_files:
            try:
                df = pd.read_csv(path.join(curr_dir, f), header=None)
            except:
                continue
            df = df.sort_values(df.columns[2])
            df.to_csv(path.join(sorted_dir, f), index=False, header=None, sep=",")

def filter_by_status_change(ids):
    for id in ids:
        print(id)
        curr_dir = path.join(DIR, "driver_sample", id)
        raw_files = listdir(path.join(curr_dir, "sorted"))
        raw_files = list(filter(lambda s: ".csv" in s, raw_files))

        filtered = path.join(curr_dir, "filtered")
        if not path.exists(filtered):
            makedirs(filtered)

        for f in raw_files:
            with open(path.join(curr_dir, "sorted", f)) as input:
                with open(path.join(curr_dir, "filtered", f), 'w') as output:
                    prev_line = input.readline()
                    dist = 0
                    total_span = 0
                    output.write(prev_line.strip()+",0,0\n")
                    prev_ts, prev_lat, prev_lon, prev_status = parse_line(prev_line)
                    for line in input.readlines():
                        ts, lat, lon, status = parse_line(line)
                        curr_dist = get_distance(prev_lat, prev_lon, lat, lon)
                        dist = dist + curr_dist
                        span = ts - prev_ts
                        total_span = total_span + span.total_seconds()
                        if status != prev_status or span.total_seconds() > 300:
                            output.write(prev_line.strip()+","+str(dist)+","+str(total_span)+"\n")
                            output.write(line.strip()+",0,0\n")
                            dist = 0
                            total_span = 0
                        prev_line, prev_ts, prev_lat, prev_lon, prev_status = line, ts, lat, lon, status
                    output.write(prev_line.strip()+","+str(dist)+","+str(total_span)+"\n")


def aggregate_temporal_distribution():
    for id in ids:
        curr_dir = path.join(DIR, "driver_sample", id)
        input_files = listdir(path.join(curr_dir, "filtered"))

        summary_folder = path.join(curr_dir, "summary")
        if not path.exists(summary_folder):
            makedirs(summary_folder)


        with open(path.join(curr_dir, "summary", "temporal.csv"), 'w') as output:
            header = ",".join(["Date"]+STATUS + ["transanction Count", "Total Time"]) + "\n"
            output.write(header)
            for f in input_files:
                curr_date = f[:8]
                sec_list, payment_count, total_sec = get_temporal_distribution(path.join(curr_dir, "filtered", f))
                min_list = ["%.2f" % (v/3600.0) for v in sec_list]

                line = [curr_date]+min_list+ [payment_count, "%.2f"%(total_sec/3600.0)]
                output.write(",".join([str(v) for v in line])+"\n")


def parse_line(line):
    driver, car, ts, lat, lon, status = line.split(",")
    ts = datetime.strptime(ts, "%d/%m/%Y %H:%M:%S")
    return ts, lat, lon, str(status).strip()

def get_temporal_distribution(input_f):
    status_dict = {}
    for s in STATUS:
        status_dict[s] = 0

    with open(input_f) as input:
        lines = input.readlines()
        payment_count = 0
        for i in range(0, len(lines), 2):
            try:
                line1, line2 = lines[i], lines[i+1]
            except:
                print(input_f)
            ts1, lat1, lon1, status1 = parse_line(line1)
            ts2, lat2, lon2, status2 = parse_line(line2)
            if status1 != status2:
                print(line1, line2)
                exit()
            span = ts2-ts1
            status_dict[status1] = status_dict[status1]+span.total_seconds()

            if status1 == 'PAYMENT':
                payment_count = payment_count + 1
    sec_list, status_list = [], []
    for k in STATUS:
        status_list.append(k)
        sec_list.append(status_dict[k])
    return sec_list, payment_count, sum(sec_list)


def get_distance(lat1, lon1, lat2, lon2):
    dist = gpxpy.geo.distance(float(lat1), float(lon1), None, float(lat2), float(lon2), None)
    return dist

def add_zone_mapping():
    poly = gpd.read_file('/Users/zhouyou/Workspace/RA/code/lib/sub_zone/central_sub_zone.shp')
    poly = poly.loc[:, ['PLN_AREA_N', 'geometry']]
    poly = poly.to_crs(epsg=4326)
    print(poly)

def aggregate_transaction():
    for id in ids:
        curr_dir = path.join(DIR, "driver_sample", id)
        input_files = listdir(path.join(curr_dir, "filtered"))

        summary_folder = path.join(curr_dir, "summary")
        if not path.exists(summary_folder):
            makedirs(summary_folder)


        with open(path.join(curr_dir, "summary", "transanction.csv"), 'w') as output:
            header = ",".join(["transanction index", "Total Time(min)", "Total Distance(km)"]) + "\n"
            output.write(header)
            filtered_lines = []
            for f in input_files:
                with open(path.join(curr_dir, "filtered", f)) as input:
                    for line in input.readlines():
                        cells = line.strip().split(",")
                        status, dist, span = cells[5:]
                        if (status == 'POB' or status == 'FREE') and span != '0':
                            filtered_lines.append(line)


            prev_status, prev_dist, prev_span = filtered_lines[0].split(",")[5:]
            prev_line = filtered_lines[0]
            trans_count = 1
            for line in filtered_lines[1:]:
                cells = line.strip().split(",")
                status, dist, span = cells[5:]
                if prev_status == 'FREE' and status == 'POB':
                    # output.write(prev_line)
                    # output.write(line)
                    finding_time = float(prev_span.strip()) / 60.0
                    finding_dist = float(prev_dist.strip()) /1000.0
                    output_line = ",".join([str(trans_count), "%.2f"%finding_time, "%.2f"%finding_dist])+"\n"
                    output.write(output_line)
                    trans_count = trans_count + 1
                prev_status, prev_dist, prev_span = status, dist, span
                prev_line = line

DIR = "/Volumes/WD/zhouyou/vehicle_location/dec_rda/"
STATUS = ['STC', 'FREE', 'BREAK', 'ARRIVED', 'ONCALL', 'OFFLINE', 'POB', 'PAYMENT', 'NOSHOW', 'BUSY']
ids = load_ids()


# step 1: get temporal distribution
# sort_by_time(ids)
# filter_by_status_change(ids)
# aggregate_temporal_distribution()
aggregate_transaction()

