import pandas as pd
from os import listdir
# "","log_dt","veh_x","veh_y","veh_status","driver_cd","vehicle_cd"

def sample_free_veh(filename):
    df = pd.read_csv(input_dir+filename)
    df2 = df[(df["veh_status"] == "FREE")]
    veh_ids = set(df2["vehicle_cd"])
    veh_id_dict = dict.fromkeys(veh_ids, 0)

    with open(input_dir+filename) as input_f:
        with open(out_dir+filename, 'w') as out_f:
            out_f.writelines(input_f.readline())
            for line in input_f.readlines():
                veh_id = int(line.split(",")[6])
                status = line.split(",")[4]

                if 'FREE' in status and veh_id in veh_id_dict and veh_id_dict[veh_id] == 0:
                    out_f.write(line)
                    veh_id_dict[veh_id] = 1

def main():
    filenames = []
    for f in listdir(input_dir):
        if ".csv" in f:
            filenames.append(f)
    for f in filenames:
        sample_free_veh(f)


if __name__ == '__main__':
    input_dir = "/Volumes/WD/zhouyou/vehicle_location/march rda/processed/"
    out_dir = "/Volumes/WD/zhouyou/vehicle_location/march rda/free_veh/"
    main()
