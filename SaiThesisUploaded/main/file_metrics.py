import sys
import numpy as np
import pandas as pd
import csv
sys.path.insert(0, './data')
#buy_file = open('./data/merged_data.dat','r')

index = 0;
data_set = pd.DataFrame({})

data_set = pd.read_csv('./data/merged_data_subset.dat', dtype={u'SessionId':'int', 'Date':'float', u'ItemId':'int',u'Event':'int'}, encoding='utf-8-sig')
    #Get all the valid event files
print('Initializing Dataset ....')

data_set = data_set[1:2660]
uid = data_set.ItemId.unique();

for iid in uid:
    print iid
 #       int_data = data_set.loc[data_set['SessionID'] == iid];
  #      if (int_data.loc[int_data['Event'] == 3].empty == True):
   #         data_set.drop(int_data.index, 0, inplace=True)
