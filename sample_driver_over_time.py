import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os import makedirs
from os import path
from os import listdir
def sample_driver_id():
    input_f = path.join(DIR, "vehicle_location_20161201_20161202.csv")
    driver_id_list = []
    with open(input_f) as input:
        input.readline()
        for i in range(100):
            driver_id = input.readline().split(",")[0]
            if driver_id not in driver_id_list:
                driver_id_list.append(driver_id)
            if len(driver_id_list) >= 20:
               return driver_id_list

def create_folder(ids):
    for id in ids:
        driver_dir = path.join(DIR, "driver_sample", id)
        if not path.exists(driver_dir):
            makedirs(driver_dir)

def get_data_files():
    files = listdir(DIR)
    files = list(filter(lambda s: ".csv" in s, files))
    return files

def extract_date(filename):
    name = filename.split("_")[2]
    return name


def sample_driver_activity(ids, input_f, output_f):
    id_content = {}
    for id in ids:
        id_content[id] = []

    count = 0
    with open(path.join(DIR, input_f)) as input:
        for line in input.readlines():
            curr_id = line.split(",")[0]
            if curr_id in ids:
                id_content[curr_id].append(line)
            count = count + 1

    for id in ids:
        with open(path.join(DIR, "driver_sample", id, output_f + ".csv"), 'w') as output:
            for line in id_content[id]:
                output.write(line)

def sample_driver():
    data_files = get_data_files()
    for f in data_files:
        date = extract_date(f)
        print("processing date %s" % date)
        sample_driver_activity(ids, f, date)



DIR = "/Volumes/WD/zhouyou/vehicle_location/dec_rda/"
ids = sample_driver_id()
# create_folder(ids)
# sample_driver()

