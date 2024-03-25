import pandas as pd
import numpy as np
from utils import *
from figures import *

play_store_data = pd.read_csv('../data/googleplaystore.csv')
app_store_data = pd.read_csv('../data/AppleStore.csv')

if __name__ == "__main__":
    filtered_play_store, filtered_app_store = filter_matching_names(play_store_data, app_store_data)
    #filtered_play_store.to_csv('../data/filtered/filtered_googleplaystore.csv', index=False)
    #filtered_app_store.to_csv('../data/filtered/filteredAppleStore.csv', index=False)
    match_pie_chart(play_store_data, app_store_data)