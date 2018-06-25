import numpy
import sys
import time
import pandas as pd

sys.path.insert(0, './algorithm')
sys.path.insert(0, './config_files')
sys.path.insert(0, './data')
sys.path.insert(0, './evaluator')
sys.path.insert(0, './main')
sys.path.insert(0, './metrics')
sys.path.insert(0, './plot')
from parse_config import parse_config
from metric_calculator import *
from algorithm_handler import TriggerCallback
from read_data import getData,initData
from algo_random import *
from algo_popular import *
from metric_ctr import *
from metric_precision import *
from bokeh.plotting import figure, output_file, show
#from popular import *

class Evaluator:
    recset = 0;
    cfg_metrics = 0;
    recsize = 0;
    item_db = 0;
    hitset = 0;
    cfg_algos = 0;
    algorithms = [];
    write_to_file = 0;
    metrics = [];
    reco_db = pd.DataFrame({})

    # Read data from configuration files
    def __init__(self, algos, metrics, FilePath, write_to_file):
        print ("Initializing Evaluator...");

        self.hitset, self.recset, self.cfg_metrics, self.recsize, self.cfg_algos = parse_config(FilePath);

        #convert config into array
        self.hitset =  map(int, self.hitset.rstrip(',').split(','))
        self.recset =  map(int, self.recset.rstrip(',').split(','))
        self.cfg_metrics =  self.cfg_metrics.rstrip(',').split(',')
        self.cfg_algos   =   self.cfg_algos.rstrip(',').split(',')
        self.write_to_file = write_to_file;

        self.algorithms = algos;
        self.metrics    = metrics

        #Init Data
        print ("Initializing Dataset...");
        self.item_db = initData(self.hitset);
        
        #Initialize metric caluclators
        for i in self.metrics:
            i.InitMetric(len(self.algorithms), write_to_file)

        #Call Algorithm Init
        for i in self.algorithms:
            i.AlgoConfig(self.item_db, self.recsize, write_to_file)

        print ("Initialization Complete...")

        
    
    def start_evaluator(self):
        print ("Starting Evaluator...");

        rec_tmp = pd.DataFrame({})
        #Read Data
        gd = getData();
        #Loop until nothing else to read
        while (gd.empty == False):
            count = 0
            #Call Algorithm and get Recommendations
            for i in self.algorithms:
                # Call the algorithm with event handler
                i.EventHandler(gd);

                #Request recommendation
                tmp = i.RequestRecommendation();
                if (len(tmp) > 0):
                    tmp['Algo'] = count;
                    if rec_tmp.empty:
                        rec_tmp = tmp;
                    else:
                        rec_tmp = rec_tmp.append(tmp);
                
                count += 1
       
            self.reco_db = self.reco_db.append(rec_tmp)
            #Read Data Again
            gd = getData();
            count = 0

            #Calculate and plot metrics
            for i in self.metrics:
                i.UpdateMetric(rec_tmp, gd)

            if ((gd['Event'] == 3).any() == True):
                self.Reward_Calculator(gd)

            # Delete the tmp
            rec_tmp = rec_tmp.iloc[0:0]
        print ('Evaluator Run Complete')


    def Reward_Calculator(self,gd):

        count = 0
        for i in self.algorithms:
            # Call the algorithm with event handler
            algo_rec = self.reco_db.loc[self.reco_db['Algo'] == count]
            tmp_db = algo_rec.loc[algo_rec['SessionID'].isin(gd['SessionID'])]

            if (self.write_to_file == 1):
                if not os.path.isfile('eval_reward_100k.csv'):
                    gd.to_csv('eval_reward_100k.csv', header='column_names')
                    algo_rec.to_csv('eval_reward_100k.csv', mode='a')
                    tmp_db.to_csv('eval_reward_100k.csv', mode='a')
                else: # else it exists so append without writing the header
                    algo_rec.to_csv('eval_reward_100k.csv', mode='a')
                    gd.to_csv('eval_reward_100k.csv', mode='a')
                    tmp_db.to_csv('eval_reward_100k.csv', mode='a')

            if(gd['ItemId'].isin(tmp_db['ItemId']).any() == True):
                i.RewardHandler(gd);
            count += 1

    def stop_evaluator(self):
        print ("Stopping Evaluator");

