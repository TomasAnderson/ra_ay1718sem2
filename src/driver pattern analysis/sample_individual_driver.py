import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def sample_driver():
    input_f = "./data/vehicle_location/dec/vehicle_location_20161201_20161202.csv"
    output_f = "./data/driver_pattern_visualisation/sample.csv"
    with open(input_f) as input:
        with open(output_f, 'w') as output:
            driver_id = input.readline().split(",")[0]
            for line in input.readlines():
                if driver_id == line.split(",")[0]:
                    output.write(line)

    input_f = "./data/driver_pattern_visualisation/sample.csv"
    df = pd.read_csv(input_f, header=None)
    df = df.sort_values(df.columns[2])
    df.to_csv("./data/driver_pattern_visualisation/sample_sorted.csv", index=False, header=None, sep=",")

def parse_line(line):
    driver, car, ts, lat, lon, status = line.split(",")
    ts = datetime.datetime.strptime(ts, "%d/%m/%Y %H:%M:%S")
    return ts, lat, lon, str(status).strip()

def filter_status_change():
    input_f = "./data/driver_pattern_visualisation/sample_sorted.csv"
    output_f = "./data/driver_pattern_visualisation/sample_filtered.csv"
    with open(input_f) as input:
        with open(output_f, 'w') as output:
            prev_line = input.readline()
            output.write(prev_line)
            # curr_ts, curr_lat, curr_lon, curr_status = parse_line(input.readline())
            prev_ts, prev_lat, prev_lon, prev_status = parse_line(prev_line)
            for line in input.readlines():
                ts, lat, lon, status = parse_line(line)
                if status != prev_status:
                    output.write(prev_line)
                    output.write(line)
                prev_line = line
                prev_status = status
            output.write(prev_line)

def select_transanction():
    input_f = "./data/driver_pattern_visualisation/sample_sorted.csv"
    output_f = "./data/driver_pattern_visualisation/sample_transanction.csv"
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
            _,_,_,prev_status = parse_line(line)
            output.write(line)
            for line in input.readlines():
                dt,_,_,status = parse_line(line)
                if status == flip(prev_status):
                    output.write(line)
                    prev_status = status

select_transanction()







def visualise_temporal_behaviour():
    input_f = "./data/driver_pattern_visualisation/sample_filtered.csv"
    status = ['STC', 'FREE', 'BREAK', 'ARRIVED', 'ONCALL', 'OFFLINE', 'POB', 'PAYMENT']
    status_dict = {}
    for s in status:
        status_dict[s] = 0

    with open(input_f) as input:
        lines = input.readlines()
        for i in range(0, len(lines), 2):
            line1, line2 = lines[i], lines[i+1]
            ts1, _, _, status1 = parse_line(line1)
            ts2, _, _, status2 = parse_line(line2)
            span = ts2-ts1
            status_dict[status1] = status_dict[status1]+span.total_seconds()
    min_list, status_list = [], []
    for k in status_dict:
        status_list.append(k)
        min_list.append(status_dict[k] / 60.0)

    plot(min_list, status_list)




def plot(x, labels):
    plt.rcdefaults()
    fig, ax = plt.subplots()

    # Example data
    people = labels
    y_pos = np.arange(len(people))
    performance = x

    ax.barh(y_pos, performance, align='center',
            color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Time(minutes)')
    ax.set_ylabel('Status')
    ax.set_title('How does a driver spent his time')

    plt.show()


def plot_time_span():

    # some labels for each row
    people = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
    r = len(people)

    # how many data points overall (average of 3 per person)
    n = r * 3

    # which person does each segment belong to?
    rows = np.random.randint(0, r, (n,))
    # how wide is the segment?
    widths = np.random.randint(3, 12, n, )
    # what label to put on the segment
    labels = xrange(n)
    colors = 'rgbwmc'

    patch_handles = []

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)

    left = np.zeros(r, )
    row_counts = np.zeros(r, )

    for (r, w, l) in zip(rows, widths, labels):
        print r, w, l
        patch_handles.append(ax.barh(r, w, align='center', left=left[r],
                                     color=colors[int(row_counts[r]) % len(colors)]))
        left[r] += w
        row_counts[r] += 1
        # we know there is only one patch but could enumerate if expanded
        patch = patch_handles[-1][0]
        bl = patch.get_xy()
        x = 0.5 * patch.get_width() + bl[0]
        y = 0.5 * patch.get_height() + bl[1]
        ax.text(x, y, "%d%%" % (l), ha='center', va='center')

    y_pos = np.arange(8)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.set_xlabel('Distance')

    plt.show()
# plot_time_span()

