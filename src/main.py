import pandas as pd
import numpy as np
from utils import *
from figures import *

play_store_data = pd.read_csv("../data/googleplaystore.csv")
app_store_data = pd.read_csv("../data/AppleStore.csv")
category_mapping = {
    'Games': ['Games', 'Game'],
    'Health & Fitness': ['Health & Fitness'],
    'Social': ['Social', 'Social Networking'], 
    'Shopping': ['Shopping'],
    'Education': ['Education'], 
    'Business': ['Business'],
    'Food & Drink': ['Food & Drink'], 
    'Music': ['Music'],
    'Travel': ['Travel', 'Travel & Local']
}

if __name__ == "__main__":
    filtered_play_store, filtered_app_store = filter_matching_names(play_store_data, app_store_data)
    
    merged_data_bygenre = merge_data_genre(play_store_data, app_store_data)
    merged_data = merge_data(play_store_data, app_store_data)    

    print(merged_data[merged_data['Google Play Reviews'] == 0])
    ratings_visualization(merged_data_bygenre)
    compare_price_std_avg_visualized(merged_data, category_mapping)
    price_rating_correlation(merged_data)