import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt


def clean_name(name):
    '''
    This function edits the app name to lowercase and removes any special characters or additional spaces etc.
    '''
    name = name.lower()
    name = re.sub(r'[^a-zA-Z0-9]', '', name)
    return name

def merge_data_genre(gp_data, as_data, category_mapping):
    gp_data.rename(columns={'App': 'Name'}, inplace=True)
    gp_data.rename(columns={'Genres': 'Genre'}, inplace=True)
    as_data.rename(columns={'track_name': 'Name'}, inplace=True)
    as_data.rename(columns={'prime_genre': 'Genre'}, inplace=True)

    for index, row in as_data.iterrows():
        # Iterate through the mapping dictionary
        for genre, values in category_mapping.items():
            # Check if the genre in the 'Google Genre' column is in the values of the mapping dictionary
            if row['Genre'] in values:
                # Replace the genre in the 'Apple Genre' column with the corresponding key from the mapping dictionary
                as_data.at[index, 'Genre'] = genre


    print(as_data['Genre'])

    # Split genres separated by ";" into separate values and create multiple rows for each app
    gp_df_split = gp_data.assign(Genre=gp_data['Genre'].str.split(';')).explode('Genre')

    # Apply genre mapping to the split genres
    gp_df_split['Genre'] = gp_df_split['Genre'].apply(
        lambda x: next((key for key, value in category_mapping.items() if x.strip() in value), 'Other') if pd.notna(x) else 'Other')

    # Group by app name and concatenate the condensed genres
    gp_df_condensed = gp_df_split.groupby('Name')['Genre'].apply(
        lambda x: ';'.join(set(x)) if not x.isnull().all() else '').reset_index()

    print(gp_df_condensed['Genre'])

def merge_data(gp_data, as_data):
    gp_columns = {
        'App': 'Name',  
        'Price': 'Google Play Price',
        'Rating': 'Google Play Rating',
        'Size': 'Google Play Size',
        'Genres': 'Google Play Genre',
        'Reviews': 'Google Play Reviews'
    }
    gp_data_renamed = gp_data[gp_columns.keys()].rename(columns=gp_columns)
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
    filtered = data['Google Play Price'].astype(str).str.contains(r'^\$?\d+(\.\d+)?$', na=False)
    data = data[filtered]
    data['Google Play Price'] = data['Google Play Price'].astype(str).str.replace('$', '').astype(float)

    gp_std_devs = []
    as_std_devs = []
    gp_avgs = []
    as_avgs = []

    for category in categories:
        google_play_data = data[data['Google Play Genre'].astype(str).str.contains(category, na=False, case=False)]
        app_store_data = data[data['App Store Genre'].astype(str).str.contains(category, na=False, case=False)]
        
        gp_std_devs.append(google_play_data['Google Play Price'].std())
        as_std_devs.append(app_store_data['App Store Price'].std())
        gp_avgs.append(google_play_data['Google Play Price'].mean())
        as_avgs.append(app_store_data['App Store Price'].mean())
        
        print(f"Category: {category}")
        print(f"  Google Play Avg. Price: ${gp_avgs[-1]:.2f}")
        print(f"  App Store Avg. Price: ${as_avgs[-1]:.2f}")
        print(f"  Google Play Price Std. Dev.: ${gp_std_devs[-1]:.2f}")
        print(f"  App Store Price Std. Dev.: ${as_std_devs[-1]:.2f}")
        print("")

    x = range(len(categories))  
    width = 0.35  

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, gp_std_devs, width, label='Google Play Std Dev')
    rects2 = ax.bar([p + width for p in x], as_std_devs, width, label='App Store Std Dev')
    rects3 = ax.bar(x, gp_avgs, width, bottom=gp_std_devs, label='Google Play Avg Price', alpha=0.5)
    rects4 = ax.bar([p + width for p in x], as_avgs, width, bottom=as_std_devs, label='App Store Avg Price', alpha=0.5)

    ax.set_ylabel('Prices')
    ax.set_title('Average and Standard Deviation of Prices by Category and Store')
    ax.set_xticks([p + width / 2 for p in x])
    ax.set_xticklabels(categories)
    ax.legend()

    fig.tight_layout()
    plt.show()

def filter_no_reviews(merged_data):
    no_reviews = merged_data[merged_data['Google Play Reviews'] == 0 or merge_data['App Store Reviews'] == 0]
    return no_reviews

def correct_data_types(merged_data):
    '''
    Makes numbers numbers and removes extra things.
    '''
    merged_data['Google Play Price'] = merged_data['Google Play Price'].astype(str).str.replace('$', '')
    merged_data['Google Play Price'] = pd.to_numeric(merged_data['Google Play Price'], errors='coerce')
    merged_data['App Store Price'] = pd.to_numeric(merged_data['App Store Price'], errors='coerce')
    merged_data['Google Play Rating'] = pd.to_numeric(merged_data['Google Play Rating'], errors='coerce')
    merged_data['App Store Rating'] = pd.to_numeric(merged_data['App Store Rating'], errors='coerce')
    merged_data['App Store Reviews'] = pd.to_numeric(merged_data['App Store Reviews'], errors='coerce')

    return merged_data


