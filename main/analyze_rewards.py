from __future__ import division
import os
import numpy as np
import sys
import time
import pandas as pd
import abc
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
import time
from copy import deepcopy


import sys
import os
import numpy as np
import pandas as pd
import csv

algo1 = pd.read_csv('../results_final/random_algo_rew_100k.csv')
algo0 = pd.read_csv('../results_final/popular_algo_rew_100k.csv')


plt.plot(algo0['RLen'].values,algo0['RewardLen'].values/algo0['RLen'].values, color='red', label = 'popular')
plt.plot(algo1['RLen'].values,algo1['RewardLen'].values/algo1['RLen'].values, color='blue', label = 'random')
plt.legend(loc='upper right')
plt.xlabel('Recommendations')
plt.ylabel('Reward Ratio')
plt.title('Reward Ratio for Algorithms')
plt.show()