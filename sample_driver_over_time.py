import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os import makedirs
from os import path
from os import listdir
from random import randrange


def sample_driver_id():
    input_f = path.join(DIR, "vehicle_location_20161201_20161202.csv")
    driver_id_list = []
    car_id_list = []
    with open(input_f) as input:
        for i in range(10000):
            car_id = input.readline().split(",")[0]
            if car_id not in car_id_list:
                car_id_list.append(car_id)
            if len(car_id_list) >= 20:
                break




    with open(input_f) as input:
        input.readline()
        for i in range(15000000):
            car_id, driver_id = input.readline().split(",")[0:2]
            if driver_id == "                              ":
                continue
            if car_id in car_id_list and driver_id not in driver_id_list:
                driver_id_list.append(driver_id)

    with open(path.join(DIR, "driver.txt"), 'w') as out:
        out.write("\n".join(driver_id_list))
    print(len(driver_id_list))
    return driver_id_list


def random_select(l, size=30):
    id = []
    for i in range(size):
        random_index = randrange(0, len(l))
        if random_index not in id:
            id.append(random_index)
    return [l[i] for i in id]

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
            curr_id = line.split(",")[1]
            if curr_id in ids:
                id_content[curr_id].append(line)
            count = count + 1

    for id in ids:
        with open(path.join(DIR, "driver_sample", id, output_f + ".csv"), 'w') as output:
            for line in id_content[id]:
                output.write(line)

def sample_driver():
    data_files = get_data_files()
    data_files = data_files[12:]

    for f in data_files:
        date = extract_date(f)
        print("processing date %s" % date)
        sample_driver_activity(ids, f, date)

def load_ids():
    with open(path.join(DIR, "driver.txt")) as input:
        ids = [s.strip() for s in input.readlines()]
        return ids


DIR = "/Volumes/WD/zhouyou/vehicle_location/dec_rda/"
# ids = sample_driver_id()
ids = load_ids()
# create_folder(ids)
sample_driver()
