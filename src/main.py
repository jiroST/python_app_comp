import pandas as pd
import numpy as np
from utils import *
from figures import *

play_store_data = pd.read_csv("../data/googleplaystore.csv")
app_store_data = pd.read_csv("../data/AppleStore.csv")
category_mapping = {
    'Games': ['Puzzle', 'Board', 'Adventure', 'Action', 'Action & Adventure', 'Games', 'Game', 'Racing', 'Strategy', 'Trivia', 'Word', 'Role Playing', 'Pretend Play', 'Casual', 'Card', 'Casino', 'Brain Games', 'Casual', 'Arcade'],
    'Health & Fitness': ['Health & Fitness', 'Medical'],
    'Social': ['Social', 'Social Networking', 'House & Home', 'Food & Drink', 'Lifestyle', 'News & Magazines', 'Productivity', 'Utilities', 'Reference', 'Parenting', 'News', 'Dating', 'Catalogs', 'Communication'],
    'Shopping': ['Shopping', 'Books & Reference', 'Beauty', 'Auto & Vehicles', 'Book'],
    'Education': ['Education', 'Photo & Video', 'Photography', 'Personalization', 'Video Players & Editors', 'Educational'],
    'Business': ['Business', 'Tools', 'Events', 'Finance'],
    'Food & Drink': ['Food & Drink'], 
    'Music': ['Music', 'Music & Audio', 'Music & Video'],
    'Travel': ['Travel', 'Travel & Local', 'Maps & Navigation', 'Weather', 'Navigation'],
    'Entertainment': ['Entertainment', 'Simulation', 'Sports', 'Libraries & Demo', 'Creativity', 'Comics', 'Art & Design']
}

if __name__ == "__main__":

    merged_data_bygenre = merge_data_genre(play_store_data, app_store_data, category_mapping)
    merged_data = merge_data(play_store_data, app_store_data)    

    print(merged_data[merged_data['Google Play Reviews'] == 0])

    ratings_visualization(merged_data_bygenre)
    merge_data_genre(play_store_data, app_store_data, category_mapping)
    compare_price_std_avg_visualized(merged_data, category_mapping)
    price_rating_correlation(merged_data)