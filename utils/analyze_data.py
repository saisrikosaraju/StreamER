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
sys.path.insert(0, './data')

data_ctr = pd.read_csv('./results_final/ctr_100k_1.csv')

calgo0 = data_ctr.loc[data_ctr['Algo'].isin([0])]
calgo1 = data_ctr.loc[data_ctr['Algo'].isin([1])]
plt.figure(1)
plt.ylabel('CTR')
plt.title('CTR for Algorithms')
plt.plot(calgo0['ILen'].values,3*calgo0['CLen'].values/calgo0['RLen'].values, color='red', label = 'popular')
plt.plot(calgo1['ILen'].values,3*calgo1['CLen'].values/calgo1['RLen'].values, color='blue', label = 'random')
plt.legend(loc='upper right')
plt.xlabel('Queries')

data_precision = pd.read_csv('./results_final/prec_100k_1.csv')
palgo0 = data_precision.loc[data_precision['Algo'].isin([0])]
palgo1 = data_precision.loc[data_precision['Algo'].isin([1])]
plt.figure(2)
plt.plot(palgo0['ILen'].values,3*palgo0['BLen'].values/palgo0['RLen'].values, color='red', label = 'popular')
plt.plot(palgo1['ILen'].values,3*palgo1['BLen'].values/palgo1['RLen'].values, color='blue', label = 'random')
plt.ylabel('Precision')
plt.title('Precision for Algorithms')
plt.legend(loc='upper right')
plt.xlabel('Queries')

plt.figure(3)
plt.plot(palgo0['ILen'].values,palgo0['BLen'].values/palgo0['TBLen'].values, color='red', label = 'popular')
plt.plot(palgo1['ILen'].values,palgo1['BLen'].values/palgo1['TBLen'].values, color='blue', label = 'random')
plt.ylabel('Recall')
plt.title('Recall for Algorithms')
plt.legend(loc='upper right')
plt.xlabel('Queries')
plt.show()


