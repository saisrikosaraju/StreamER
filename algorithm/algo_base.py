import numpy
import sys
import time
import pandas as pd
import abc

class AlgorithmBase(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def AlgoConfig(self, itemdb, rsize, write_to_file):
        """Event Handler Object"""
        return

    @abc.abstractmethod
    def EventHandler(self, pd):
        """Event Handler Object"""
        return
    
    @abc.abstractmethod
    def RequestRecommendation(self):
        """Recommendation Handler Object"""
        return
    
    @abc.abstractmethod
    def RewardHandler(self, pd):
        """Reward Handler Object"""
        return
