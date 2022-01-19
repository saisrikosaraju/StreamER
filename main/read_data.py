import sys
import os
import numpy as np
import pandas as pd
import csv
sys.path.insert(0, './data')
#buy_file = open('./data/merged_data.dat','r')

index = 0;
data_set = pd.DataFrame({})
item_list = []

def initData(hitset):
    global data_set
    data_set = pd.read_csv('./data/data_event_1_100k.csv', dtype={u'SessionId':'int', 'Date':'float', u'ItemId':'int',u'Event':'int'}, encoding='utf-8-sig')
    item_set = pd.read_csv('./data/merged_data_subset.dat', dtype={u'SessionId':'int', 'Date':'float', u'ItemId':'int',u'Event':'int'}, encoding='utf-8-sig')
    #Get all the valid event files
    print('Initializing Dataset ....')

    item_list =  item_set.ItemId.unique();
    uid = data_set.SessionID.unique();
    for iid in uid:
        int_data = data_set.loc[data_set['SessionID'] == iid];
        if (int_data.loc[int_data['Event'] == 3].empty == True):
            data_set.drop(int_data.index, 0, inplace=True)

    print('Dataset init complete....')
    return item_list

def getData():
    global index
    index = index+1;


    return data_set[index-1:index]
