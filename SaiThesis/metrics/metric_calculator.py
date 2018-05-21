import numpy
import pandas as pd
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split

total_list = [];
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    global total_list
    xar = []
    yar = []

    for index, row in total_list.iterrows():
        if len(row)>1:
            x = row['ItemId']
            y = row['CLen']/row['RLen']
            xar.append(int(x))
            yar.append(int(y))
    ax1.clear()
    ax1.plot(xar,yar)

def init_metrics():
    global total_list;
    global_lists = [];
    total_list = pd.DataFrame(global_lists,columns = ['SessionID', 'ItemId', 'RLen', 'CLen']);

def calc_metrics(rec_tmp, cdata):
    global total_list

    if (len(total_list) >0):
        if (len(total_list[total_list['SessionID'].isin(cdata['SessionID'])]) > 0):
            index = total_list[total_list['SessionID'].isin(cdata['SessionID'])]['ItemId'].index.tolist()
            for i in index:
                if (total_list.iloc[i]['ItemId'] == cdata.iloc[0]['ItemId']):
                    total_list.loc[i, 'CLen'] += 1

    #If a recommendation is present 
    if (len(rec_tmp) > 0):
        tmp_lsts = [];
        # Append Recommendation data to empty list
        tmp_lst = pd.DataFrame(tmp_lsts,columns = ['SessionID','ItemId','RLen', 'CLen']);
        ts = pd.Series(rec_tmp['SessionID'])
        tmp_lst['SessionID'] = ts.values
        ts = pd.Series(rec_tmp['ItemId'])
        tmp_lst['ItemId'] = ts.values
        ts = pd.Series(1)
        tmp_lst['RLen'] = ts.values
        ts = pd.Series(0)
        tmp_lst['CLen'] = ts.values
        
        # Add Recommendation to the recommendation list
        if (len(total_list) == 0):
            total_list = total_list.append(tmp_lst);
        else:
            if (len(total_list[total_list['SessionID'].isin(tmp_lst['SessionID'])]) > 0):
                index = total_list[total_list['SessionID'].isin(tmp_lst['SessionID'])]['ItemId'].index.tolist()
                for i in index:
                    if (total_list.iloc[i]['ItemId'] == tmp_lst.iloc[0]['ItemId']):
                        total_list.loc[i, 'RLen'] += 1
                    else:
                        total_list = total_list.append(tmp_lst);
            else:
                total_list = total_list.append(tmp_lst);

    
    if (len(total_list) > 0):
        ani = animation.FuncAnimation(fig, animate)
        plt.show()

def get_metrics():
    global total_list
    return total_list;

