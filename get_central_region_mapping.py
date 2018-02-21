import csv

with open("./data/areas_mapping.csv") as input:
    central_region_list = []
    for row in csv.reader(input):
        if "CENTRAL REGION" in row[5]:
            central_region_list.append(row[2])
    print(central_region_list)

