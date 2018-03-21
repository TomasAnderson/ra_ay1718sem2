import csv
from random import randrange
import datetime
unit_time = 10 # five minutes
area = ['BISHAN', 'BUKIT MERAH', 'BUKIT TIMAH', 'GEYLANG', 'NOVENA', 'TOA PAYOH', 'DOWNTOWN CORE', 'MARINA EAST', 'NEWTON', 'ORCHARD', 'MARINA SOUTH', 'MUSEUM', 'MARINE PARADE', 'QUEENSTOWN', 'SOUTHERN ISLANDS', 'KALLANG', 'TANGLIN', 'OUTRAM', 'RIVER VALLEY', 'ROCHOR', 'SINGAPORE RIVER', 'STRAITS VIEW']
car_id_index = 0
time_index = 8
location_index = 3
input_dir = "./data/street_hail_trips/"
out_dir = "./data/processed_supply_in_unit/"


def get_index(hour, minute):
    return (int(hour)*60+int(minute)) // unit_time

def get_time(index):
    hour = index*unit_time // 60
    minute = index*unit_time - hour*60
    return "%0*d:%0*d"%(2,hour,2,minute)

from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


start_date = date(2016, 12, 1)
end_date = date(2017, 5, 31)



weekday_dict = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
weekday = 6
start_index = get_index(7, 0)
end_index = get_index(11, 15)
with open(out_dir + "raw/supply_in_unit_time_%s.csv" % weekday_dict[weekday], 'w') as out:
    writer = csv.writer(out)
    for single_date in daterange(start_date, end_date):
        date = single_date.strftime("%Y%m%d")
        day_of_week = single_date.weekday()

        if day_of_week != weekday:
            continue
        print("processing %s..."%date)

        with open(input_dir + "street_hail_%s.csv" % date) as f:
            rows = csv.reader(f)
            supply_dict = {}
            i = 0
            for row in rows:
                # obtain basic info
                car = row[car_id_index]
                date, time = row[time_index].split(" ")

                hour, minute = time.split(":")[0:2]
                location = row[location_index]

                index = get_index(hour, minute)

                if index < start_index or index > end_index:
                    continue
                if index not in supply_dict:
                    supply_dict[index] = []

                if location in area:
                    if car not in supply_dict[index]:
                        supply_dict[index].append([car, location])

            for k in range(start_index, end_index):
                if k in supply_dict:
                    supply_in_unit = supply_dict[k]
                    region_dict = {}
                    for car, location in supply_in_unit:
                        if location in region_dict:
                            region_dict[location] = region_dict[location] + 1
                        else:
                            region_dict[location] = 1
                    for r in area:
                        if r in region_dict:
                            supply = region_dict[r] + randrange(100)
                        else:
                            supply = randrange(0, 20)
                        writer.writerow([date, weekday_dict[day_of_week], get_time(k), r, supply])





