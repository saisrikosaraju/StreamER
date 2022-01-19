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
        self.rec_size = int(rsize); #Number of recommendations to generate per request
        self.item_db = item_db #Item database to send recommendations from
        self.buy_db['ItemId'] = item_db #Buy database to produce recommendations based on popularity
        self.rec_db['ItemId'] = item_db #Recommendataion database

        #Initialize buy count to 1 initially to start generating recommendations
        #Important for popular algorithm as it only sends recommendations from items that are popular
        #Setting buy count to 1 acts as an initalizer. So in theory at the start this is same as random algorithm
        self.buy_db['Count'] = 1
        self.write_to_file = write_to_file;
        self.buy_db = self.buy_db.reset_index(drop=True)
        return
    
    def EventHandler(self, pd):
        """Event Handler Object"""
        self.pd_temp = pd.copy(deep=True)

        #For buy event, update the buy database. Increment count for existing items. Add and increment if new.
        #Hardcoded the event id to 3 for now
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
        #Create a empty topn dataframe
        topn = pd.DataFrame([],columns = ['SessionID', 'Date', 'ItemId', 'Event']);
        temp = pd.DataFrame([]);
        bsize = 0 #Number of Possible recommendations algorithm can produce based on popularity

        #TopN popular algorithm sends top 'N' popular recommendations. Where N is the recommendation size
        #If requested recommendations are more than popular items, then send everything the algorithm has
        if (int(self.buy_db.shape[0]) >= self.rec_size):
            bsize = self.rec_size
        elif (self.buy_db.shape[0] > 0):
            bsize = self.buy_db.shape[0]

        # Sort the database for popularity
        temp = self.buy_db.sort_values('Count', ascending=False)[:bsize].sort_index()

        #Get recommendation Items if possible recommendation length is greater than 0
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

            #Append the current recommendation data to the data frame
            self.rec_db.append(topn )
            #Clear current event data, will be reused by event handler
            self.pd_temp = self.pd_temp.iloc[0:0]
            #Update the recommendation count
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
        #Add reward information to reward database
        self.reward_db = self.reward_db.append(pd)
        #Update reward counters
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

