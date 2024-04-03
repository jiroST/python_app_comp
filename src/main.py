import pandas as pd
import numpy as np
from utils import *
from figures import *

play_store_data = pd.read_csv("../data/filtered/googleplaystore.csv")
app_store_data = pd.read_csv("../data/filtered/AppleStore.csv")

if __name__ == "__main__":
    filtered_play_store, filtered_app_store = filter_matching_names(play_store_data, app_store_data)
    #filtered_play_store.to_csv('../data/filtered/filtered_googleplaystore.csv', index=False)
    #filtered_app_store.to_csv('../data/filtered/filteredAppleStore.csv', index=False)
    
    merged_data, merged_data_bygenre = merge_data(play_store_data, app_store_data)
    merged_data['Google Play Price'] = pd.to_numeric(merged_data['Google Play Price'], errors='coerce')
    merged_data['App Store Price'] = pd.to_numeric(merged_data['App Store Price'], errors='coerce')

    print(merged_data[merged_data['Google Play Reviews'] == 0])
    print(len(filter_no_reviews))
    ratings_visualization(merged_data_bygenre)

    price_rating_correlation(merged_data)