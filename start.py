import numpy
import sys
import time
import pandas as pd
import importlib

sys.path.insert(0, './evaluator')
sys.path.insert(0, './config_files')
from evaluator import *
from algo_random import *
from algo_popular import *
from metric_ctr import *
from metric_precision import *
FilePath='config_files/session.config'

print 'parsing configuration'

algo_popular = AlgorithmPopular();
algo_random = AlgorithmRandom();

metric_ctr = MetricCTR();
metric_precision = MetricPrecision();

algo_list = [algo_popular, algo_random]
metric_list = [metric_ctr, metric_precision]

write_to_file = 0;
my_evaluator = Evaluator(algo_list, metric_list, FilePath, write_to_file);
my_evaluator.start_evaluator();
my_evaluator.stop_evaluator();

raw_input("Press Enter to continue...")
