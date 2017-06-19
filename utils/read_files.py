from os import listdir
from os.path import isfile, join
import sys
import csv
from datetime import datetime, timedelta
from scipy.sparse import csr_matrix
import numpy as np
import matplotlib.pyplot as plt

def simple_plot(mat):
    plt.figure()
    for line in mat:
        # print(line)
        plt.plot(line)

    plt.ylabel('Consumption')
    plt.xlabel('DATE & HOURS')
    plt.show()



if __name__ == "__main__":
    mypath = sys.argv[1]
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    
    dates2id = {}
    id2dates = {}
    idx_date = 0
    dt = datetime.strptime('2014-08-23', '%Y-%m-%d')
    dates2id[dt] = idx_date
    idx_date += 1
    while dt<datetime.strptime('2014-12-22', '%Y-%m-%d'):
        dt = dt + timedelta(hours=1)
        dates2id[dt] = idx_date
        id2dates[idx_date] = dt
        idx_date += 1

    idx_file = 0

    file2id  = {}
    id2file  = {}
    data = []
    row = []
    col = []
    for f in onlyfiles:
        with open(join(mypath, f), 'r', encoding="utf-8") as fd:
            spamreader = csv.reader(fd, delimiter = ',')
            file2id[str(f)] = idx_file
            id2file[idx_file] = str(f)
            idx_file += 1
            for line in spamreader:
                dt = datetime.strptime(line[0], '%d-%m-%Y')
                idx_hour = 0
                for hour in line[1:]:
                    row.append(file2id[str(f)])
                    col.append(dates2id[dt + timedelta(hours=idx_hour)])
                    idx_hour += 1
                    data.append(float(hour))

    all_data = csr_matrix((data, (row, col)), dtype=np.float64)

    for key, value in id2dates.items():
        print(key, value)
    
    for key, value in id2file.items():
        print(key, value)

    simple_plot(all_data.toarray())