import sys
import pandas as pd
from algorithm_handler import RegisterAlgorithm

item_db = 0;
rec_db = pd.DataFrame({})
count = 0

def callback(pd):
    global rec_db
    global count

    pd_temp = []
#    print pd
    if (count%4 == 0):
        pd_temp = pd.copy(deep=True)
        pd_temp =  pd_temp.drop('Date', 1)
        rec_db = rec_db.append(pd_temp)

    count += 1
    return pd_temp

def AlgoInit(itemdb):
    global item_db
    print('Algorithm Initialization')
    item_db = itemdb;
    RegisterAlgorithm(callback)

def algoreward(reward):
    print ('')
#    print reward
