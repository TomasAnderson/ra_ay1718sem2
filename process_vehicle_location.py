import csv

location_list = []
hail_dir = "./data/street_hail_trips/"
vehicle_dir = "./data/vehicle_location/"
out_dir = "./data/processed_vehicle_location/"

date1 = "20161201"
date2 = "20160202"

with open(hail_dir+"street_hail_%s.csv"%date1) as f:
    rows = csv.reader(f)
    for row in rows:
        location = row[3]
        location_list.append(location)


with open(hail_dir + "street_hail_20161202.csv") as f:
    rows = csv.reader(f)
    for row in rows:
        location = row[3]
        location_list.append(location)

N = len(location_list)

with open(vehicle_dir+"vehicle_location_%s_%s.csv"%(date1,date2)) as f:
    with open(out_dir+"vehicle_location_2%s_%s.csv"%(date1,date2), 'w') as out:
        writer = csv.writer(out)
        index = 0
        for row in csv.reader(f):
            writer.writerow(row + [location_list[index]])
            index = index + 1
            if index >= N:
                index = 0
