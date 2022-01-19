import sys
import os
import pandas as pd
import numpy as np
from algo_base import AlgorithmBase
import random


class AlgorithmRandom(AlgorithmBase):
    rec_size = 0
    pd_temp = []       
    reward_db = pd.DataFrame({})
    item_db = []
    write_to_file = 0;
    reward_db = pd.DataFrame([],columns = ['SessionID', 'Date', 'ItemId', 'Event']);
    rec_db = pd.DataFrame(pd_temp,columns = ['SessionID', 'Date', 'ItemId', 'Event']);
    reward_cnt = pd.DataFrame(np.zeros((1, 2)),columns = ['RewardLen', 'RLen']);

    def AlgoConfig(self, item_db, rsize, write_to_file):
        self.rec_size = int(rsize);
        self.item_db = item_db
        self.write_to_file = write_to_file;

    def EventHandler(self, pd):
        """Event Handler Object"""
        self.pd_temp = pd.copy(deep=True)
        return 
    
    def RequestRecommendation(self):
        """Recommendation Handler Object"""
        # Get rec_size random items from the item database
        if (int(self.item_db.shape[0]) >  self.rec_size) :
            item_locations = random.sample(range(0,self.item_db.shape[0]-1),self.rec_size);

        #Get recommendation Items
        temp_recs = pd.DataFrame([],columns = ['SessionID', 'Date', 'ItemId', 'Event']);
        temp_recs['ItemId'] = self.item_db[item_locations]

    
        #Fill in rest of the columns 
        #Copy session id, date and event to inform the evaluator about the event that caused this recommendation
        temp_recs = temp_recs.reset_index(drop=True)
        ts = int(self.pd_temp['SessionID'])
        temp_recs['SessionID'] = ts
        ts = int(self.pd_temp['Date'])
        temp_recs['Date'] = ts
        ts = int(self.pd_temp['Event'])
        temp_recs['Event'] = ts 

        #Append the current recommendation data to the data frame
        self.rec_db.append(temp_recs)
        #Clear current event data, will be reused by event handler
        self.pd_temp = self.pd_temp.iloc[0:0]
        #Update total recommendation count
        self.reward_cnt.loc[0]['RLen'] +=self.rec_size

        if (self.write_to_file == 1):
            if not os.path.isfile('random_algo_100k.csv'):
                temp_recs.to_csv('random_algo_100k.csv', header='column_names')
            else: # else it exists so append without writing the header
                temp_recs.to_csv('random_algo_100k.csv', mode='a', header=False)


        if (self.write_to_file == 1):
            if not os.path.isfile('random_algo_rew_100k.csv'):
               self.reward_cnt.to_csv('random_algo_rew_100k.csv', header='column_names')
            else: # else it exists so append without writing the header
                self.reward_cnt.to_csv('random_algo_rew_100k.csv', mode='a', header=False)
        return temp_recs;

    def RewardHandler(self, pd):
        """Reward Handler Object"""
        #Add reward information to reward database
        self.reward_db = self.reward_db.append(pd)
        #Update reward counters
        self.reward_cnt.loc[0]['RewardLen'] +=1

        #Write to file
        if (self.write_to_file == 1):
            if not os.path.isfile('random_algo_reward_100k.csv'):
                self.reward_db.to_csv('random_algo_reward_100k.csv', header='column_names')
                self.reward_cnt.to_csv('random_algo_reward_100k.csv', mode='a')
            else: # else it exists so append without writing the header
                self.reward_db.to_csv('random_algo_reward_100k.csv', mode='a')
                self.reward_cnt.to_csv('random_algo_reward_100k.csv', mode='a')

