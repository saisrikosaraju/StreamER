import sys
import numpy as np
import csv
import pandas as pd

from copy import deepcopy
sys.path.insert(0, '../data')
outfile = open('merged_data.dat','wb')
clicks_file = open('../data/yoochoose-clicks.dat','r')
buy_file = open('../data/yoochoose-buys.dat','r')

csvbReader = csv.reader(buy_file)
csvcReader = csv.reader(clicks_file)
csvWriter = csv.writer(outfile)

list = [];
lst  = [];

#read each row in the input file
for row in csvcReader:
    row_len = len(row);
    list.append(row[0]);
    row[1] = row[1].replace("T","");
    row[1] = row[1].replace("-","");
    row[1] = row[1].split("Z")[0].replace(":","");
#    row[1] = row[1].replace(".","");
    list.append(row[1]);
    list.append(row[2]);
    list.append(1);
    list.append(row[3]);
    list.append(0);
    list.append(0);
    lst.append(deepcopy(list));
    del list[:];
    
for row in csvbReader:
    row_len = len(row);
    list.append(row[0]);
    row[1] = row[1].replace("T","");
    row[1] = row[1].replace("-","");
    row[1] = row[1].split("Z")[0].replace(":","");
#    row[1] = row[1].replace(".","");
    list.append(row[1]);
    list.append(row[2]);
    list.append(3);
    list.append(0);
    list.append(row[3]);
    list.append(row[4]);
    lst.append(deepcopy(list));
    del list[:];


lst = sorted(lst, key=lambda lst: lst[1]);
list = ['SessionID', 'Date', 'Timestamp', 'ItemId', 'Event', 'Category', 'Price', 'Quantity'];
lst.insert(0,deepcopy(list));
del list[:];
#s = pd.DataFrame(data=lst, columns=['SessionID', 'Date', 'ItemId', 'Event', 'Category', 'Price', 'Quantity'])

#csvWriter.writerow("SessionID, Date, Timestamp, ItemId, Event, Category, Price, Quantity")
for line in lst:
    csvWriter.writerow(line)

outfile.close();
buy_file.close();
clicks_file.close();
