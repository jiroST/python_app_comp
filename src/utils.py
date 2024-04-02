import pandas as pd
import numpy as np
import re

def clean_name(name):
    '''
    This function edits the app name to lowercase and removes any special characters or additional spaces etc.
    '''
    name = name.lower()
    name = re.sub(r'[^a-zA-Z0-9]', '', name)
    return name


def filter_matching_names(gp_data, as_data):
    '''
    This function finds the matching apps in both datasets by comparing the name columns. It returns the mathing parts from both datasets.  
    '''
    gp_data['Name'] = gp_data['App'].apply(clean_name)
    as_data['Name'] = as_data['track_name'].apply(clean_name)

    gp_names = set(gp_data['Name'])
    as_names = set(as_data['Name'])

    matched_names = gp_names.intersection(as_names)

    matching_gp = gp_data[gp_data['Name'].isin(matched_names)]
    matching_as = as_data[as_data['Name'].isin(matched_names)]

    return matching_gp, matching_as


def merge_data(gp_data, as_data):
    gp_columns = {
        'App': 'Name',  
        'Price': 'Google Play Price',
        'Rating': 'Google Play Rating',
        'Size': 'Google Play Size',
        'Genres': 'Genre',
        'Reviews': 'Google Play Reviews'
    }
    gp_data_renamed = gp_data[gp_columns.keys()].rename(columns=gp_columns)
    gp_data_renamed = gp_data_renamed.drop_duplicates(subset=['Name'], keep='first')

    as_columns = {
        'track_name': 'Name',  
        'price': 'App Store Price',
        'user_rating': 'App Store Rating',
        'size_bytes': 'App Store Size',
        'prime_genre': 'Genre',
        'rating_count_tot': 'App Store Reviews'
    }
    as_data_renamed = as_data[as_columns.keys()].rename(columns=as_columns)
    as_data_renamed = as_data_renamed.drop_duplicates(subset=['Name'], keep='first')

    merged_data = pd.merge(gp_data_renamed, as_data_renamed, on='Name', how='outer')
    merged_data.to_csv('../data/filtered/merged_data.csv', index=False, na_rep='NaN')

    merged_data_bygenre = pd.merge(gp_data_renamed, as_data_renamed, on='Genre', how='outer') # Merging data by 'Genre'
    merged_data_bygenre['Genre'] = merged_data_bygenre['Genre'].str.split(';')
    merged_data_bygenre = merged_data_bygenre.explode('Genre')
    merged_data_bygenre.groupby('Genre').agg(lambda x: '; '.join(x)).reset_index()
    merged_data_bygenre = merged_data_bygenre[['Genre', 'App Store Rating', 'Google Play Rating']] # Creating a DF with only App Store and Play Store ratings indexed by Genre

    return merged_data, merged_data_bygenre


def price_comparison(gp_data, as_data):
    '''
    This function creates a table that lists app prices from both datasets, excluding free apps.
    It calculates the price difference for mismatched prices, NaN when values match.
    '''
    gp_price_data = gp_data[~gp_data['Price'].isin(['0', 'Free', 'NaN'])]
    as_price_data = as_data[as_data['price'] > 0]

    filtered_gp_price, filtered_as_price = filter_matching_names(gp_price_data, as_price_data)

    filtered_gp_price = filtered_gp_price[['App', 'Price']]
    filtered_as_price = filtered_as_price[['track_name', 'price']]

    filtered_gp_price.rename(columns={'Price': 'Play Store Price'}, inplace=True)
    filtered_as_price.rename(columns={'track_name': 'App', 'price': 'App Store Price'}, inplace=True)

    merged_data = pd.merge(filtered_gp_price, filtered_as_price, on='App', how='outer')

    #TBC!!!

    return
