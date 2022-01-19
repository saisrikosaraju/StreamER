import numpy
import sys
import time
import pandas as pd
import abc

class MetricBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def InitMetric(self, num_algos, write_to_file):
        """Init Metrics"""
        return

    @abc.abstractmethod
    def UpdateMetric(self, rec_tmp, cdata):
        """Update Metrics"""
        return
