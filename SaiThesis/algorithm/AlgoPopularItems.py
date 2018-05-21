import numpy as np
import scipy
import pandas as pd
import math
import random
import sklearn
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import svds
import matplotlib.pyplot as plt
from read_data import getData,initData
sys.path.insert(0, './data')
sys.path.inser(0, './main')

product_df = pd.read_csv('../data/merged_data_subset.dat')
product_df = articles_df[articles_df['Event'] == '3']
product_df.head(5)

#Computes the most popular items
item_popularity_df = interactions_full_df.groupby('ItemId')['Event'].sum().sort_values(ascending=False).reset_index()
item_popularity_df.head(10)

class PopularityRecommender:
    MODEL_NAME = 'Popularity'
    
    def __init__(self, popularity_df, items_df=None):
        self.popularity_df = popularity_df
        self.items_df = items_df
        
        
        def get_model_name(self):       
            return self.MODEL_NAME
                        
        def recommend_items(self, user_id, items_to_ignore=[], topn=10, verbose=False):
            # Recommend the more popular items that the user hasn't seen yet.
            recommendations_df = self.popularity_df[~self.popularity_df['ItemId'].isin(items_to_ignore)] \
                    .sort_values('Event', ascending = False) \
                    .head(topn)         
                    
            if verbose:
                if self.items_df is None:
                    raise Exception('"items_df" is required in verbose mode')
                recommendations_df = recommendations_df.merge(self.items_df, how = 'left', 
                        left_on = 'ItemId', 
                        right_on = 'ItemId')[['Event', 'ItemId', 'SessionId', 'date']]
                return recommendations_df
            popularity_model = PopularityRecommender(item_popularity_df, articles_df)

