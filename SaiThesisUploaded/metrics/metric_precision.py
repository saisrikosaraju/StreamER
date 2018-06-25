from __future__ import division
import numpy as np
import sys
import time
import pandas as pd
import abc
from metric_base import MetricBase
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
import time
import os
from copy import deepcopy

class MetricPrecision(MetricBase):
    total_list = [];
    cnt1 = 0
    cnt2 = 0
    ilen = []
    ratio = []
    ratio1 = []
    p1 = []
    legend = 0
    num_algos = 0
    write_to_file = 0;
    def InitMetric(self, num_algos, write_to_file):
        global_lists = [];
        self.total_list = pd.DataFrame(global_lists,columns = ['Algo', 'RLen', 'BLen', 'ILen', 'TBLen']);
        plt.ion()
        plt.show()
        plt.figure(2)
        self.num_algos = num_algos
        self.cnt1 = 1
        self.cnt2 = 1
        self.write_to_file = write_to_file;
        self.legend = plt.legend(title="title", loc=4, fontsize='small', fancybox=True)

        tmp_lst = pd.DataFrame({'Algo':pd.Series([], dtype='str'),
                   'RLen':pd.Series([], dtype='float'),
                   'BLen':pd.Series([], dtype='float'),
                   'ILen':pd.Series([], dtype='float'),
                   'TBLen':pd.Series([], dtype='float')})

        for i in range(1, num_algos+1):
            self.ilen.append([])
            self.ratio.append([])
            self.ratio1.append([])            
            #Create a dataframe
            ts = pd.Series(i-1)
            tmp_lst['Algo'] = ts
            ts = 0
            tmp_lst['RLen'] = ts
            ts = 0
            tmp_lst['BLen'] = ts
            ts = 0
            tmp_lst['ILen'] = ts 
            ts = 0
            tmp_lst['TBLen'] = ts 
            self.total_list = self.total_list.append(tmp_lst);
            tmp_lst=tmp_lst.iloc[0:0]
            self.total_list = self.total_list.reset_index(drop=True)

    def UpdateMetric(self, rec_tmp, cdata):
        """Event Handler Object"""

        tmp_lsts = []
        tmp_lst = pd.DataFrame({'Algo':pd.Series([], dtype='str'),
                   'RLen':pd.Series([], dtype='float'),
                   'BLen':pd.Series([], dtype='float'),
                   'ILen':pd.Series([], dtype='float')})
        count = 0
        cdata = cdata

        rec_tmp = rec_tmp.reset_index(drop=True)
        #loop through unique algorithms
        uq = rec_tmp.Algo.unique()
        for algo in uq:
            algo_rec = rec_tmp.loc[rec_tmp['Algo'] == algo]
            if((cdata['ItemId'].isin(algo_rec['ItemId']).any() == True) and ((cdata['Event'] == 3).any() == True)):
                #Create a dataframe
                ts = pd.Series(algo)
                tmp_lst['Algo'] = ts
                ts = pd.Series(algo_rec.shape[0])
                tmp_lst['RLen'] = ts
                ts = 1
                tmp_lst['BLen'] = ts
                ts = pd.Series(cdata.shape[0])
                tmp_lst['ILen'] = ts

                if (len(self.total_list) == 0):
                    self.total_list =  tmp_lst.copy();
                elif(tmp_lst['Algo'].isin(self.total_list['Algo']).any() == False):
                    self.total_list = self.total_list.append(tmp_lst);
                    self.total_list = self.total_list.reset_index(drop=True)
                else:
                    self.total_list = self.total_list.reset_index(drop=True)
                    idx = np.where(self.total_list['Algo'] == algo)
                    self.total_list.loc[idx[0], 'RLen'] += tmp_lst.iloc[0]['RLen']
                    self.total_list.loc[idx[0], 'BLen'] += tmp_lst.iloc[0]['BLen']
            else:
                self.total_list = self.total_list.reset_index(drop=True)
                idx = np.where(self.total_list['Algo'] == algo)
                ts = pd.Series(algo_rec.shape[0])
                tmp_lst['RLen'] = ts
                self.total_list.loc[idx[0], 'RLen'] += tmp_lst.iloc[0]['RLen']

            tmp_lst=tmp_lst.iloc[0:0]

        for count in range(0, self.num_algos):
            if (cdata['Event'].values == 3):
                self.total_list.loc[count] ['TBLen'] += 1    
            self.total_list.loc[count] ['ILen'] += 1
            self.total_list = self.total_list.reset_index(drop=True)
            tst1 = self.total_list.iloc[count]['BLen'].copy()
            tst2  = self.total_list.iloc[count]['RLen'].copy()
            tst3  = self.total_list.iloc[count]['TBLen'].copy()
            if tst1 == 0:
                tmp_ratio = 0
            else:
                tmp_ratio = 3*tst1/tst2

            if tst3 == 0:
                tmp_ratio1 = 0
            else:
                tmp_ratio1 = tst1/tst3

            self.ilen[count].append(self.total_list.iloc[count]['ILen'].copy())
            self.ratio[count].append(tmp_ratio)
            self.ratio1[count].append(tmp_ratio1)
            count = count+1

        plt.figure(2)
        tt = plt.plot(self.ilen[0], self.ratio[0], color = 'red')
        tt2 =  plt.plot(self.ilen[1], self.ratio[1], color = 'Blue')
        self.legend = plt.legend(['Popular', 'Random'])
        plt.xlabel('Queries')
        plt.ylabel('Precision')
        plt.title('Precision for Algorithms')
        plt.figure(3)
        tt3 = plt.plot(self.ilen[0], self.ratio1[0], color = 'red')
        tt4 =  plt.plot(self.ilen[1], self.ratio1[1], color = 'Blue')
        self.legend = plt.legend(['Popular', 'Random'])
        plt.xlabel('Queries')
        plt.ylabel('Recall')
        plt.title('Recall for Algorithms')
        plt.draw()
        plt.pause(0.0001)
       
        return
