import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
def parse_line(line):
    driver, car, ts, lat, lon, status = line.split(",")
    ts = datetime.datetime.strptime(ts, "%d/%m/%Y %H:%M:%S")
    return ts, lat, lon, str(status).strip()

def sample_drivers():
    input_f = "./data/vehicle_location/dec/vehicle_location_20161201_20161202.csv"
    driver_list = []
    with open(input_f) as input:
        for i in range(100):
            line = input.readline()
            driver_id = line.split(",")[0]
            if driver_id not in driver_list:
                driver_list.append(driver_id)
            if len(driver_list) >= 20:
                break

    for id in driver_list:
        extract_info_by_driver(id)

def extract_info_by_driver(driverId):
    print("sampleing driver %s..."%driverId)
    input_f = "./data/vehicle_location/dec/vehicle_location_20161201_20161202.csv"
    output_f = "./data/driver_pattern_visualisation/macro_analysis/%s.csv"%driverId
    with open(input_f) as input:
        with open(output_f, 'w') as output:
            for line in input.readlines():
                if driverId == line.split(",")[0]:
                    output.write(line)

def sort_all():
    files = listdir("./data/driver_pattern_visualisation/macro_analysis")
    files.remove(".DS_Store")

    for f in files:
        df = pd.read_csv("./data/driver_pattern_visualisation/macro_analysis/"+f, header=None)
        df = df.sort_values(df.columns[2])
        df.to_csv("./data/driver_pattern_visualisation/sorted/"+f, index=False, header=None, sep=",")




status = ['STC', 'FREE', 'BREAK', 'ARRIVED', 'ONCALL', 'OFFLINE', 'POB', 'PAYMENT', 'NOSHOW', 'BUSY']

def calc_stats(input_f):
    input_f = "./data/driver_pattern_visualisation/macro_analysis/" + input_f
    status_dict = {}
    for s in status:
        status_dict[s] = 0

    with open(input_f) as input:
        lines = input.readlines()
        for i in range(0, len(lines), 2):
            if i+1>=len(lines):
                break
            line1, line2 = lines[i], lines[i + 1]
            ts1, _, _, status1 = parse_line(line1)
            ts2, _, _, status2 = parse_line(line2)
            span = ts2 - ts1
            status_dict[status1] = status_dict[status1] + span.total_seconds()
    min_list, status_list = [], []
    for k in status:
        status_list.append(k)
        min_list.append(status_dict[k] / 60.0)

    return min_list

def select_transanction(id):
    input_f = "./data/driver_pattern_visualisation/macro_analysis/%s.csv"%id
    output_f = "./data/driver_pattern_visualisation/sample_driver/%s_transanction.csv"%id
    def flip(s):
        if 'PAYMENT' in s:
            return 'POB'
        elif 'POB' in s:
            return 'PAYMENT'
        else:
            return "No"

    with open(input_f) as input:
        with open(output_f, 'w') as output:
            line = input.readline()
            # _,_,_,prev_status = parse_line(line)
            prev_status = "PAYMENT"
            output.write(line)
            for line in input.readlines():
                dt,_,_,status = parse_line(line)
                if status == flip(prev_status):
                    output.write(line)
                    prev_status = status


def calc_macro_stats():
    files = listdir("./data/driver_pattern_visualisation/macro_analysis")
    files.remove(".DS_Store")

    macro_stats= np.zeros((20, 10))
    with open("./data/driver_pattern_visualisation/macro_stats.csv", 'w') as output:
        header= ",".join(status)
        output.write("ID,"+"%s\n"%header)

        for i, f in enumerate(files):
            min_list = calc_stats(f)
            macro_stats[i] = min_list
            line = ",".join([str(int(round(v))) for v in min_list])+"\n"
            output.write(f+","+line)
    np.save("macro_stats.npy", macro_stats)
calc_macro_stats()

# select_transanction("51A3F70B9BE7EED66E1307EA8955E0")
select_transanction("78291F86775D6F1893069777549B1C")

