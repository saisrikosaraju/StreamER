import numpy as np
import matplotlib.pyplot as plt

def plot_data(i,d):
    plt.axis([0, 1000, 0, 10000])
    plt.scatter(i, d)
    plt.pause(0.05)
