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

        # Create a temporary dataframe
        tmp_lst = pd.DataFrame({'Algo':pd.Series([], dtype='str'),
                   'RLen':pd.Series([], dtype='float'),
                   'BLen':pd.Series([], dtype='float'),
                   'ILen':pd.Series([], dtype='float'),
                   'TBLen':pd.Series([], dtype='float')})

        for i in range(1, num_algos+1):
            self.ilen.append([])
            self.ratio.append([])
            self.ratio1.append([])

            # Add element to dataframe
            tmp_lst['Algo'] = pd.Series(i-1) # Algorithm Id
            tmp_lst['RLen'] = 0 #Recommendation length
            tmp_lst['BLen'] = 0 #Number of buys of the recommendations in recommendation length
            tmp_lst['ILen'] = 0  #Item length
            tmp_lst['TBLen'] = 0 #Total buys from all the recommendations by the given algorithm

            # Append temporary dataframe to final dataframe with proper indexing
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
            #Get the recommendations by the given algorithm with length from configuration
            algo_rec = rec_tmp.loc[rec_tmp['Algo'] == algo]
            #If the next event is buy and is recommended by one of the algorithms, then update the metric
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

                #Check if the total list, that contains information on both algorithms is empty. Happens first time.
                #Copy if empty, or append if algorithm is not listed, or update relevant fields if all algorithms are present
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
                ts = pd.Series(algo_rec.shape[0])
                tmp_lst['RLen'] = ts
                # Get the index of algorithm and update the total number of recommendations produced so far
                idx = np.where(self.total_list['Algo'] == algo)
                self.total_list.loc[idx[0], 'RLen'] += tmp_lst.iloc[0]['RLen']

            tmp_lst=tmp_lst.iloc[0:0]

        for count in range(0, self.num_algos):
            #Update total number of items bought even if it is not due to the recommendation from algorithm
            if (cdata['Event'].values == 3):
                self.total_list.loc[count] ['TBLen'] += 1

            #Copy buy length, recommendation length and total buy length for each algorithm
            self.total_list.loc[count] ['ILen'] += 1
            self.total_list = self.total_list.reset_index(drop=True)
            tst1 = deepcopy(self.total_list.iloc[count]['BLen'])
            tst2  = deepcopy(self.total_list.iloc[count]['RLen'])
            tst3  = deepcopy(self.total_list.iloc[count]['TBLen'])

            #Calculate precision, (items_bought/total_recommendations)
            #Only one item will be bought out of provided N recommendations per turn by the algorithm.
            #So the ratio should adjust for that difference
            #Multiply the number of items bought with 3 instead of dividing total recommendations by 3.
            if tst1 == 0:
                tmp_ratio = 0
            else:
                tmp_ratio = 3*tst1/tst2

            #Calculate recall, (items_bought_by_recommendation/total_number_items_bought)
            if tst3 == 0:
                tmp_ratio1 = 0
            else:
                tmp_ratio1 = tst1/tst3

            self.ilen[count].append(deepcopy(self.total_list.iloc[count]['ILen']))
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
