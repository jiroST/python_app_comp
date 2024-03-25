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

    return merged_data
