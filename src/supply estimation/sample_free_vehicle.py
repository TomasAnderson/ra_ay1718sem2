import pandas as pd
from os import listdir
# "","log_dt","veh_x","veh_y","veh_status","driver_cd","vehicle_cd"

def sample_free_veh(filename, start, end):
    print("processing %s..."%filename)
    output_name = filename.split(".")[0]+"_"+start.split(":")[1]+".csv"
    df = pd.read_csv(input_dir+filename,  names = ["vehicle_cd", "driver_cd", "log_dt", "veh_x", "veh_y", "veh_status"])
    # "", "log_dt", "veh_x", "veh_y", "veh_status", "driver_cd", "vehicle_cd"

    df2 = df[(df["veh_status"] == "FREE")]
    veh_ids = set(df2["vehicle_cd"])
    veh_id_dict = dict.fromkeys(veh_ids, 0)

    with open(input_dir+filename) as input_f:
        with open(out_dir+output_name, 'w') as out_f:
            out_f.writelines(input_f.readline())
            for line in input_f.readlines():
                veh_id = line.split(",")[0]
                status = line.split(",")[5]
                dt = line.split(",")[2]
                time = dt.split(" ")[1]

                if time >= start and time <= end:
                    if 'FREE' in status and veh_id in veh_id_dict and veh_id_dict[veh_id] == 0:
                        out_f.write(line)
                        veh_id_dict[veh_id] = 1


def main():
    filenames = []
    for f in listdir(input_dir):
        if ".csv" in f:
            filenames.append(f)
    filenames = [filenames[0]]



    intervals = [("08:05:00", "08:10:00"), ("08:10:00", "08:15:00"),
                 ("08:15:00", "08:20:00"), ("08:20:00", "08:25:00"), ("08:25:00", "08:30:00")]
    # intervals = [("08:00:00", "08:05:00")]
    for interval in intervals:
        start, end = interval
        for f in filenames:
            sample_free_veh(f, start, end)


if __name__ == '__main__':
    input_dir = "/Volumes/WD/zhouyou/comfort_april/"
    out_dir = "/Volumes/WD/zhouyou/comfort_april/free_veh/"
    main()
