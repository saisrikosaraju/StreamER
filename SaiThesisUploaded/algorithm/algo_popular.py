import os
import sys
import pandas as pd
import random
from algo_base import AlgorithmBase
import numpy as np

class AlgorithmPopular(AlgorithmBase):
    rec_size = 0;
    write_to_file = 0;
    pd_temp = []
    item_db = []
    buy_db = pd.DataFrame([],columns = ['ItemId', 'Count']);
    reward_db = pd.DataFrame([],columns = ['SessionID', 'Date', 'ItemId', 'Event']);
    rec_db = pd.DataFrame([],columns = ['SessionID', 'Date', 'ItemId', 'Event']);
    reward_cnt = pd.DataFrame(np.zeros((1, 2)),columns = ['RewardLen', 'RLen']);

    def AlgoConfig(self, item_db, rsize, write_to_file):
        self.rec_size = int(rsize);
        self.item_db = item_db
        self.buy_db['ItemId'] = item_db
        self.rec_db['ItemId'] = item_db
        self.buy_db['Count'] = 1
        self.write_to_file = write_to_file;
        if not os.path.isfile('popular_bdb_100k.csv'):
           self.buy_db.to_csv('popular_algo_bdb.csv', header='column_names')
        else: # else it exists so append without writing the header
           self.buy_db.to_csv('popular_algo_bdb.csv', mode='a', header=False)

        self.buy_db = self.buy_db.reset_index(drop=True)
        return
    
    def EventHandler(self, pd):
        """Event Handler Object"""
        self.pd_temp = pd.copy(deep=True)

        #Hardcoded for now
        if (pd['Event'].values == 3):
            if((self.buy_db.shape[0] > 0) and (self.buy_db['ItemId'].isin(self.pd_temp['ItemId']).any() == True)):
                index = self.buy_db[self.buy_db['ItemId'].isin(self.pd_temp['ItemId'])].index
                self.buy_db.loc[index, 'Count'] +=1
            else:
                self.pd_temp['Count'] = 1
                self.buy_db = self.buy_db.append(self.pd_temp.drop(['Date', 'SessionID','Event'], axis=1,inplace=False));
        return 
    
    def RequestRecommendation(self):
        """Recommendation Handler Object"""
        topn = pd.DataFrame([],columns = ['SessionID', 'Date', 'ItemId', 'Event']);
        temp = pd.DataFrame([]);
        bsize = 0

        if (int(self.buy_db.shape[0]) >= self.rec_size):
            bsize = self.rec_size
        elif (self.buy_db.shape[0] > 0):
            bsize = self.buy_db.shape[0]

        temp = self.buy_db.sort_values('Count', ascending=False)[:bsize].sort_index()
        #Get recommendation Items if length is greater than 0
        if (len(temp) > 0):
            topn['ItemId'] = temp['ItemId']

            #Fill in rest of the columns 
            topn = topn.reset_index(drop=True)
            ts = int(self.pd_temp['SessionID'])
            topn['SessionID'] = ts
            ts = int(self.pd_temp['Date'])
            topn['Date'] = ts
            ts = int(self.pd_temp['Event'])
            topn['Event'] = ts 

            #Append the data to the data frame
            self.rec_db.append(topn )
            self.pd_temp = self.pd_temp.iloc[0:0]
            self.reward_cnt.loc[0]['RLen'] +=self.rec_size


        if (self.write_to_file == 1):
            if not os.path.isfile('popular_algo_100k.csv'):
                topn.to_csv('popular_algo_100k.csv', header='column_names')
                temp.to_csv('popular_algo_100k_bdb.csv', header='column_names')
            else: # else it exists so append without writing the header
                topn.to_csv('popular_algo_100k.csv', mode='a', header=False)
                temp.to_csv('popular_algo_100k_bdb.csv', mode='a', header=False)
       
            if not os.path.isfile('popular_algo_rew_100k.csv'):
                self.reward_cnt.to_csv('popular_algo_rew_100k.csv', header='column_names')
                self.reward_cnt.to_csv('popular_algo_rew_backup.csv', header='column_names')
                topn.to_csv('popular_algo_rew_backup.csv', mode='a', header='column_names')
            else: # else it exists so append without writing the header
                self.reward_cnt.to_csv('popular_algo_rew_100k.csv', mode='a', header=False)
                self.reward_cnt.to_csv('popular_algo_rew_backup.csv', mode='a', header='column_names')
                topn.to_csv('popular_algo_rew_backup.csv', mode='a', header='column_names')
        return topn

    def RewardHandler(self, pd):
        """Reward Handler Object"""
        self.reward_db = self.reward_db.append(pd) 
        self.reward_cnt.loc[0]['RewardLen'] +=1

        #Writes to a file
        if (self.write_to_file == 1):
            if not os.path.isfile('popular_algo_reward_100k.csv'):
                self.reward_db.to_csv('popular_algo_reward_100k.csv', header='column_names')
                self.reward_cnt.to_csv('popular_algo_reward_100k.csv', mode='a')
            else: # else it exists so append without writing the header
                self.reward_db.to_csv('popular_algo_reward_100k.csv', mode='a')
                self.reward_cnt.to_csv('popular_algo_reward_100k.csv', mode='a')
        return

