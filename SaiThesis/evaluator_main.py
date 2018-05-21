import numpy
import sys
import time
import pandas as pd
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
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
from plot_realtime import plot_data
from read_data import getData,initData
from algo import *

# Read data from configuration files
delay = 0;
hitset = 0;
recset = 0;
metrics = 0;
recsize = 0;
item_db = 0;
rec_db1 = pd.DataFrame({})

def init_evaluator():
    print ("Initializing Evaluator...");
    #Read Configuration data
    print ("Parsing Configuration...");
    global delay, hitset, recset, metrics, recsize;
    delay, hitset, recset, metrics, recsize = parse_config();

    #convert config into array
    hitset =  map(int, hitset.rstrip(',').split(','))
    recset =  map(int, recset.rstrip(',').split(','))
    metrics =  map(int, metrics.rstrip(',').split(','))

    #Init Data
    global item_db
    print ("Initializing Dataset...");
    item_db = initData(hitset);
    #Call Algorithm Init
    AlgoInit(item_db);
    init_metrics();
    print ("Initialization Complete...")
    
def start_evaluator():
    print ("Starting Evaluator...");
    #Read Data
    gd = getData();
    rec_tmp = [];

    print ("Got first item");
    #Loop until nothing else to read
    while (gd.empty == False):
        global rec_db1

            #Call Algorithm and get Recommendations
        rec_tmp = callback(gd)
        if (len(rec_tmp) != 0):
            if (delay == True):
                rec_db1 = rec_db1.append(rec_tmp)
            else:
                rec_db1 = rec_tmp
        
        #Read Data Again
        gd = getData();
        
        # If the session and item matches a recommendation
        # then provide a reward            
        if ((len(rec_db1) != 0) and (gd.loc[gd['SessionID'].isin(rec_db1.iloc[:,0])]['Event'].values == 3 )):
            #Generate Reward
            algoreward(gd)
        
        if ((delay == False) and (len(rec_db1) != 0)):
            rec_db1.drop(rec_db1.index[0], inplace=True)

        #Calculate and plot metrics
        calc_metrics(rec_tmp, gd);
         
    print ('Evaluator Run Complete')
#    print rec_db1;
    get_metrics();


def stop_evaluator():
    print ("Stopping Evaluator");

#Start Here
init_evaluator();
start_evaluator();
stop_evaluator();

