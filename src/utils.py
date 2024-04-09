import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import os


def merge_data_genre(gp_data, as_data, category_mapping):
    gp_data.rename(columns={'App': 'Name'}, inplace=True)
    gp_data.rename(columns={'Genres': 'Genre'}, inplace=True)
    as_data.rename(columns={'user_rating': 'Rating'}, inplace=True)
    as_data.rename(columns={'track_name': 'Name'}, inplace=True)
    as_data.rename(columns={'prime_genre': 'Genre'}, inplace=True)

    # Condensing App Store Genres
    for index, row in as_data.iterrows():
        # Iterate through the mapping dictionary
        for genre, values in category_mapping.items():
            # Check if the genre in the 'Genre' column is in the values of the mapping dictionary
            if row['Genre'] in values:
                # Replace the genre in the 'Apple Genre' column with the corresponding key from the mapping dictionary
                as_data.at[index, 'Genre'] = genre

    # Split genres separated by ";" into separate values and take the first value
    gp_data['Genre'] = gp_data['Genre'].apply(lambda x: x.split(';')[0] if ';' in x else x)
    gp_data_condensed = gp_data

    # Condensing Play Store Genres
    for index, row in gp_data_condensed.iterrows():
        # Iterate through the mapping dictionary
        for genre, values in category_mapping.items():
            # Check if the genre in the 'Genre' column is in the values of the mapping dictionary
            if row['Genre'] in values:
                # Replace the genre in the 'Apple Genre' column with the corresponding key from the mapping dictionary
                gp_data_condensed.at[index, 'Genre'] = genre

    gp_data_condensed = gp_data_condensed[gp_data_condensed['Genre'] != 'February 11, 2018']

    counter = 0
    for value in gp_data_condensed['Genre']:
        # Check if the genre in the 'Genre' column is in the values of the mapping dictionary
        if value in category_mapping:
            # Replace the genre in the 'Apple Genre' column with the corresponding key from the mapping dictionary
            counter += 1
        else:
            print(f" '{value} is not in category mapping")

    # Order both datasets by genre
    as_sorted = as_data.sort_values(by='Genre')
    gp_sorted = gp_data_condensed.sort_values(by='Genre')

    # Aggregate data by counting occurrences of each genre
    as_sorted_agg = as_sorted.groupby('Genre').size().reset_index(name='Count App Store')
    gp_sorted_agg = gp_sorted.groupby('Genre').size().reset_index(name='Count Google Play Store')

    # Calculate the average rating for each genre in both datasets
    avg_rating_as = as_sorted.groupby('Genre')['Rating'].mean().reset_index(name='App Store Avg Rating')
    avg_rating_gp = gp_sorted.groupby('Genre')['Rating'].mean().reset_index(name='Google Play Avg Rating')

    # Merge aggregated data
    Display_Counts_df = pd.merge(as_sorted_agg, gp_sorted_agg, on='Genre', how='outer')
    merged_data_bygenre = pd.merge(Display_Counts_df, avg_rating_as, on='Genre', how='left')
    merged_data_bygenre = pd.merge(merged_data_bygenre, avg_rating_gp, on='Genre', how='left')

    # Display settings to show all rows and columns of final DataFrame
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    return merged_data_bygenre
def merge_data(gp_data, as_data):

    gp_columns = {
        'App': 'Name', 
        'Price': 'Google Play Price',
        'Rating': 'Google Play Rating',
        'Size': 'Google Play Size',
        'Genres': 'Google Play Genre',
        'Reviews': 'Google Play Reviews'
    }
    gp_data_renamed = gp_data[list(gp_columns.keys())].rename(columns=gp_columns)
    gp_data_renamed = gp_data_renamed.drop_duplicates(subset=['Name'], keep='first')
    

    as_columns = {
        'track_name': 'Name',  
        'price': 'App Store Price',
        'user_rating': 'App Store Rating',
        'size_bytes': 'App Store Size',
        'prime_genre': 'App Store Genre',
        'rating_count_tot': 'App Store Reviews'
    }
    as_data_renamed = as_data[as_columns.keys()].rename(columns=as_columns)
    as_data_renamed = as_data_renamed.drop_duplicates(subset=['Name'], keep='first')

    merged_data = pd.merge(gp_data_renamed, as_data_renamed, on='Name', how='outer')
    merged_data = correct_data_types(merged_data)
    merged_data.to_csv("../data/filtered/merged_data.csv", index=False, na_rep='NaN')
    return merged_data

def compare_price_std_avg_visualized(data, categories):

    gp_std_devs = []
    as_std_devs = []
    gp_avgs = []
    as_avgs = []

    for category in categories:
        google_play_data = data[data['Google Play Genre'].astype(str).isin(categories[category])]
        app_store_data = data[data['App Store Genre'].astype(str).isin(categories[category])]

        gp_std_devs.append(google_play_data['Google Play Price'].std())
        as_std_devs.append(app_store_data['App Store Price'].std())
        gp_avgs.append(google_play_data['Google Play Price'].mean())
        as_avgs.append(app_store_data['App Store Price'].mean())

        # Debug prints
        print(f"Category: {category}")
        print(f"  Google Play Avg. Price: ${gp_avgs[-1]:.2f}")
        print(f"  App Store Avg. Price: ${as_avgs[-1]:.2f}")
        print(f"  Google Play Price Std. Dev.: ${gp_std_devs[-1]:.2f}")
        print(f"  App Store Price Std. Dev.: ${as_std_devs[-1]:.2f}")
        print("")

    x = range(len(categories))  
    width = 0.15
    fig, ax = plt.subplots()

    rects1 = ax.bar(x, gp_avgs, width, label='Google Play Avg Price')
    rects2 = ax.bar([p + width for p in x], gp_std_devs, width, label='Google Play Std Dev')
    rects3 = ax.bar([p + width*2 for p in x], as_avgs, width, label='App Store Avg Price')
    rects4 = ax.bar([p + width*3 for p in x], as_std_devs, width, label='App Store Std Dev')

    ax.set_ylabel('Price ($)')
    ax.set_title('Average Prices and Standard Deviation by Category and Store')
    ax.set_xticks([p + width*1.5 for p in x])
    ax.set_xticklabels(categories, rotation=45)
    ax.legend()
    fig.tight_layout()
    plt.show()

def correct_data_types(merged_data):
    '''
    Makes numbers numbers and removes extra things.
    '''
    merged_data['Google Play Price'] = merged_data['Google Play Price'].astype(str).str.replace('$', '')
    merged_data['Google Play Rating'] = merged_data['Google Play Rating'].map(lambda x: round(x * 2) / 2, 'ignore')
    merged_data['Google Play Price'] = pd.to_numeric(merged_data['Google Play Price'], errors='coerce')
    merged_data.loc[merged_data['Google Play Price'] > 100, 'Google Play Price'] = None
    merged_data.loc[merged_data['App Store Price'] > 100, 'App Store Price'] = None    
    merged_data['App Store Price'] = pd.to_numeric(merged_data['App Store Price'], errors='coerce')
    merged_data['Google Play Rating'] = pd.to_numeric(merged_data['Google Play Rating'], errors='coerce')
    merged_data['App Store Rating'] = pd.to_numeric(merged_data['App Store Rating'], errors='coerce')
    merged_data['App Store Reviews'] = pd.to_numeric(merged_data['App Store Reviews'], errors='coerce')

    return merged_data


