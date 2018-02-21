import csv
from random import randrange
import datetime
unit_time = 5 # five minutes
area = ['BISHAN', 'BUKIT MERAH', 'BUKIT TIMAH', 'GEYLANG', 'NOVENA', 'TOA PAYOH', 'DOWNTOWN CORE', 'MARINA EAST', 'NEWTON', 'ORCHARD', 'MARINA SOUTH', 'MUSEUM', 'MARINE PARADE', 'QUEENSTOWN', 'SOUTHERN ISLANDS', 'KALLANG', 'TANGLIN', 'OUTRAM', 'RIVER VALLEY', 'ROCHOR', 'SINGAPORE RIVER', 'STRAITS VIEW']
car_id_index = 0
time_index = 8
location_index = 3
input_dir = "./data/street_hail_trips/"
out_dir = "./data/processed_supply_in_unit/"

def get_next_time(t):
    hour, minute = t.split(":")
    if int(minute) < 55:
        return "%0*s:%0*d"%(2,hour, 2,int(minute)+5)
    elif t == "23:55":
        return "00:00"
    else:
        return "%0*d:00"%(2,int(hour)+1)

def get_index(hour, minute):
    return (int(hour)*60+int(minute)) // unit_time

def get_time(index):
    hour = index*5 // 60
    minute = (index - hour*60//5)*5
    return "%0*d:%0*d"%(2,hour,2,minute)


weekday_dict = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
weekday = 6
with open(out_dir + "supply_in_unit_time_%s.csv" % weekday_dict[weekday], 'w') as out:
    writer = csv.writer(out)
    for day in range(1, 32):
        date = "201612%0*d" % (2, day)
        day_of_week = datetime.datetime(2016, 12, day).weekday()

        if day_of_week != weekday:
            continue

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
                if index < 84 or index > 132:
                    continue
                if index not in supply_dict:
                    supply_dict[index] = []

                if location in area:
                    if car not in supply_dict[index]:
                        supply_dict[index].append([car, location])

            for k in range(84, 133):
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
                            supply = region_dict[r] + randrange(20)
                        else:
                            supply = randrange(0, 3)
                        writer.writerow([date, weekday_dict[day_of_week], get_time(k), r, supply])




