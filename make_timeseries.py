import argparse

def readCSV(filepath, period):
    duration_volumes = {}

    with open(filepath) as fr:
        header = fr.readline()[:-1].split(",")  # strip off \n character and split by comma
        column = header.index(period)
        for line in fr:
            line = line.split(",")
            duration = int(line[0])
            volume = float(line[column])
            duration_volumes[duration] = (volume)

    return duration_volumes

def equalise_interval(duration_volumes, interval):
    duration_volumes = list(duration_volumes.items())
    incremental_durations = [duration_volumes[0][1]]
    for i,(duration,volume) in enumerate(duration_volumes):
        if i == 0:
            continue
        delta_d = duration_volumes[i][0]-duration_volumes[i-1][0]
        delta_v = duration_volumes[i][1]-duration_volumes[i-1][1]
        steps = delta_d // interval
        v_fraction = round(delta_v / steps,3)
        # print(i,(duration,volume),delta_d,delta_v,steps, v_fraction)
        for s in range(steps):
            incremental_durations.append(v_fraction)
    return incremental_durations

def save_csv(filepath, series, returnperiod):
    with open(filepath,"w") as fw:
        fw.write(";;[TIMESERIES]\n")
        fw.write(";;Name YY MM DD HH mm Value\n")
        fw.write(";;---- -- -- -- -- -- -----\n")
        name = "%d-yr" % int(returnperiod[:-1])

        for step,v in enumerate(series):
            step *= 5
            time = "2020 01 %02d %02d %02d" % (step // 1440 + 1, (step % 1440) // 60, step % 60)
            fw.write(name + " " + time + " " + str(v) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("datapath", help="path to storm event data csv")
    parser.add_argument("returnperiod", help="storm event return period. Format: 001A for annual event")
    parser.add_argument("duration", help="storm event duration in minutes",type=int)
    parser.add_argument("--interval", help="desired timeseries interval in minutes, default: 5min", default=5)
    parser.add_argument('--type1', help='use Euler-Type-I style, insted of type-II', action='store_true')
    args = parser.parse_args()

    duration_volumes = readCSV(args.datapath, args.returnperiod)

    incremental_durations = equalise_interval(duration_volumes,args.interval)

    # trim to the desired duration
    steps_needed = args.duration // args.interval
    incremental_durations = incremental_durations[:steps_needed]

    if args.type1:
        # type-I (peak in the beginning)
        result_series = incremental_durations
    else:
        # type-II adjustment (peak at 0.3)
        third_pos = int(len(incremental_durations)*0.3)

        increasing_part = incremental_durations[:third_pos]
        decreasing_part = incremental_durations[third_pos:]

        result_series = increasing_part[::-1] + decreasing_part
    
    save_csv("timeseries.csv",result_series, args.returnperiod)