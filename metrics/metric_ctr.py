from __future__ import division
import os
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
from copy import deepcopy

class MetricCTR(MetricBase):
    total_list = [];
    cnt1 = 0
    cnt2 = 0
    ilen = []
    ratio = []
    p1 = []
    legend = 0
    num_algos = 0
    write_to_file =0 ;
    def InitMetric(self, num_algos, write_to_file):
        global_lists = [];
        self.total_list = pd.DataFrame(global_lists,columns = ['Algo', 'RLen', 'CLen', 'ILen']);
        plt.ion()
        plt.show()
        plt.figure(1)
        self.num_algos = num_algos
        self.cnt1 = 1
        self.cnt2 = 1
        self.legend = plt.legend(title="title", loc=4, fontsize='small', fancybox=True)
        self.write_to_file = write_to_file;

        tmp_lst = pd.DataFrame({'Algo':pd.Series([], dtype='str'),
                   'RLen':pd.Series([], dtype='float'),
                   'CLen':pd.Series([], dtype='float'),
                   'ILen':pd.Series([], dtype='float')})

        for i in range(1, num_algos+1):
            self.ilen.append([])
            self.ratio.append([])
            #Create a dataframe
            ts = pd.Series(i-1)
            tmp_lst['Algo'] = ts
            ts = 0
            tmp_lst['RLen'] = ts
            ts = 0
            tmp_lst['CLen'] = ts
            ts = 0
            tmp_lst['ILen'] = ts 
            self.total_list = self.total_list.append(tmp_lst);
            tmp_lst=tmp_lst.iloc[0:0]
            self.total_list = self.total_list.reset_index(drop=True)

    def UpdateMetric(self, rec_tmp, cdata):
        """Event Handler Object"""

        tmp_lsts = []
        tmp_lst = pd.DataFrame({'Algo':pd.Series([], dtype='str'),
                   'RLen':pd.Series([], dtype='float'),
                   'CLen':pd.Series([], dtype='float'),
                   'ILen':pd.Series([], dtype='float')})
        count = 0
        cdata = cdata

        # Hardcoded event
        if ((cdata['Event'] == 3).any() == True):
            for count in range(0, self.num_algos):
                self.total_list.loc[count]['ILen'] += 1
            if (self.write_to_file == 1):
                if not os.path.isfile('ctr_100k_1.csv'):
                    self.total_list.to_csv('ctr_100k_1.csv', header='column_names', index = False)
                else: # else it exists so append without writing the header
                    self.total_list.to_csv('ctr_100k_1.csv', mode='a', header=False, index=False)
 
            return


        #loop through unique algorithms
        for algo in rec_tmp.Algo.unique():
            algo_rec = rec_tmp.loc[rec_tmp['Algo'] == algo]
            if(cdata['ItemId'].isin(algo_rec['ItemId']).any() == True):
                #Create a dataframe
                ts = pd.Series(algo)
                tmp_lst['Algo'] = ts
                ts = pd.Series(algo_rec.shape[0])
                tmp_lst['RLen'] = ts
                ts = 1
                tmp_lst['CLen'] = ts
                ts = pd.Series(cdata.shape[0])
                tmp_lst['ILen'] = ts

                if (len(self.total_list) == 0):
                    self.total_list =  tmp_lst.copy();
                elif(tmp_lst['Algo'].isin(self.total_list['Algo']).any() == False):
                    self.total_list = self.total_list.append(tmp_lst);
                    self.total_list = self.total_list.reset_index(drop=True)
                else:
                    idx = np.where(self.total_list['Algo'] == algo)
                    self.total_list.loc[idx[0], 'RLen'] += tmp_lst.iloc[0]['RLen']
                    self.total_list.loc[idx[0], 'CLen'] += tmp_lst.iloc[0]['CLen']
            else:
                idx = np.where(self.total_list['Algo'] == algo)
                ts = pd.Series(algo_rec.shape[0])
                tmp_lst['RLen'] = ts
                self.total_list.loc[idx[0], 'RLen'] += tmp_lst.iloc[0]['RLen']

            tmp_lst=tmp_lst.iloc[0:0]

        for count in range(0, self.num_algos):
            self.total_list = self.total_list.reset_index(drop=True)
            tst1 = self.total_list.iloc[count]['CLen'].copy()
            tst2  = self.total_list.iloc[count]['RLen'].copy()
            self.total_list.loc[count]['ILen'] += 1
            if tst1 == 0:
                tmp_ratio = 0
            else:
                tmp_ratio = 3*tst1/tst2
            self.ilen[count].append(self.total_list.iloc[count]['ILen'].copy())
            self.ratio[count].append(tmp_ratio)
            count = count+1

        plt.figure(1)
        tt = plt.plot(self.ilen[0], self.ratio[0], color = 'red')
        tt2 =  plt.plot(self.ilen[1], self.ratio[1], color = 'Blue')
        self.legend = plt.legend(['Popular', 'Random'])

        plt.xlabel('Queries')
        plt.ylabel('Click Through Rate')
        plt.title('Click Through rate for Algorithms')
        plt.draw()
        plt.pause(0.0001)
        plt.show()

        return
