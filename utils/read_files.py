from os import listdir
from os.path import isfile, join
import sys
import csv
from datetime import datetime, timedelta
from scipy.sparse import csr_matrix
import numpy as np
import matplotlib.pyplot as plt

# ids for file
file2id  = {}
id2file  = {}

# ids for datetime

dates2id = {}
id2dates = {}

def printDictionary(dictionary):
    for key, value in dictionary.items():
        print(key, value)

# plots the data
# params:
#   a matrix with n customers
#   customers -  a list with customers ids to plot, if empty plots all
def simple_plot(mat, customers = []):
    plt.figure()
    if customers:
        for customer in customers:
            plt.plot(mat[customer])
    else:
        for line in mat:
            plt.plot(line)
    plt.ylabel('Consumption')
    plt.xlabel('DATE & HOURS')
    plt.show()


# createIDDate create the two id date dictionaries
# params:
#   startDate - the first date from the dataset (given as string)
#   endDate - the last date from the dataset (given as string)
def createIDDate(startDate, endDate):
    idx_date = 0
    dt = startDate
    while dt <= endDate:
        dates2id[dt] = idx_date
        id2dates[idx_date] = dt
        dt = dt + timedelta(hours=1)
        idx_date += 1

# params:
#   dirpath -  path to csv directory
# returns:
#   Compressed Sparse Row matrix
def readData(dirpath):
    onlyfiles = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
    idx_file = 0
    
    data = []
    row = []
    col = []
    for f in onlyfiles:
        with open(join(dirpath, f), 'r') as fd:
            spamreader = csv.reader(fd, delimiter = ',')
            file2id[str(f)] = idx_file
            id2file[idx_file] = str(f)
            idx_file += 1
            for line in spamreader:
                dt = datetime.strptime(line[0], '%d-%m-%Y')
                idx_hour = 0
                for hour in line[1:]:
                    if dates2id.get(dt + timedelta(hours=idx_hour), None) != None:
                        row.append(file2id[str(f)])
                        col.append(dates2id[dt + timedelta(hours=idx_hour)])
                        data.append(float(hour))
                    idx_hour += 1

    return csr_matrix((data, (row, col)), dtype=np.float64)


# main for test
# receives 3 arguments 
#   argv[1] - the path to the dataset
#   argv[2] - date format
#   argv[3] - start date (minDate = '2014-08-23 0')
#   argv[4] - end date (maxDate = '2014-12-22 0')
# accepts date intervals between minDate & maxDate (minDate < maxDate)
# run on entire dataset e.g. python3.6 read_files.py AMR_DATA/ %Y-%m-%d 2014-08-23 2014-12-22
# run on a subset of the dataset e.g. python3.6 read_files.py AMR_DATA/ "%Y-%m-%d %H" "2014-09-24 3" "2014-09-25 12" # carefull to have data between these dates
if __name__ == "__main__":
    dirpath = sys.argv[1]
    dateFormat = sys.argv[2]
    startDate = datetime.strptime(sys.argv[3], dateFormat)
    endDate = datetime.strptime(sys.argv[4], dateFormat)

    createIDDate(startDate, endDate)
    # if you need the date ids
    printDictionary(id2dates)

    csrmat = readData(dirpath)

    # if you need the file ids
    printDictionary(id2file)

    simple_plot(csrmat.toarray(), [1, 2, 10, 20])