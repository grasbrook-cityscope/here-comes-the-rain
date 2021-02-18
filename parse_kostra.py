import os
import argparse
import shapefile


def readShape(filepath, index):
    '''read storm volumes from KOSTRA shapefile
    index: INDEX_RC of desired cell
    returns: dict with return periods as keys'''
    # open shapefile
    sf = shapefile.Reader(filepath)
    records = sf.records()

    # extract return periods
    periods = [x[0][3:7] for x in sf.fields[2:]]
    
    # find requested cell by index
    try:
        record = next(filter(lambda x: x[0] == index,records))
    except StopIteration:
        print("index %d not found in shapefile" % index)
        exit()

    ret_dict = dict(zip(periods, record[1:]))
    return ret_dict

def traverse_dir(data_dir, index):
    '''read all KOSTRA data from data_dir and return volume table of cell with given index'''
    data_table = {}
    for d in os.listdir(data_dir):
        subdir = os.path.join(data_dir,d)
        if os.path.isdir(subdir):
            duration = (d.split("_")[-1][-4:])
            subdir = os.path.join(subdir,d)
            for f in os.listdir(subdir):
                if f[-3:] == "shp":
                    filepath = os.path.join(subdir,f)
                    period_volume = readShape(filepath, index)
                    data_table[duration] = period_volume
    return data_table

def save_csv(outpath, data):
    '''save to csv file'''
    with open(outpath,"w") as fw:
        title = "DURATION," + ",".join(list(data.values())[0].keys()) + "\n"
        fw.write(title)
        
        for duration, period_volume in data.items():
            fw.write(duration + "," + ",".join(map(str,period_volume.values())) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("datadir", help="path to KOSTRA DIR")
    parser.add_argument("index", help="desired KOSTRA cell index")
    args = parser.parse_args()
    
    working_directory = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(working_directory,args.datadir) # "KOSTRA2010"

    index = int(args.index) # HH GB: 22035
    data_table = traverse_dir(data_dir, index)

    outpath = "stormevents_%s.csv" % index
    save_csv(outpath,data_table)

