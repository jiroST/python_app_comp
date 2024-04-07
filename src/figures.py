import matplotlib.pyplot as plt
from utils import *


def match_pie_chart(gp_data, as_data):
    '''
    This function visualizes the filtering function, drawing a pie chart to show the percentages of matching and unmatching values. 
    '''
    gp_count = len(gp_data)
    as_count = len(as_data)
    filtered_gp, filtered_as = filter_matching_names(gp_data, as_data)
    filtered_count = len(filtered_gp)
    unmatch_gp = gp_count - filtered_count
    unmatch_as = as_count - filtered_count

    labels = ['Matching', 'Unmatched Google Play Store', 'Unmatched App Store']
    allocation = [filtered_count, unmatch_gp, unmatch_as]
    colors = ['#ff9999','#66b3ff','#99ff99']
    plt.figure(figsize=(10, 10))
    plt.pie(allocation, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.show()

def ratings_visualization(merged_data_bygenre):
    '''
    This functions takes a handful of popular Genres and performs
    statistical analyses and visualizations of ratings
    '''
'''
    avg_app_store_ratings = []
    avg_google_play_ratings = []
    genres = merged_data_bygenre['Condensed_Genre']

    # Iterate through each genre
    for index, row in merged_data_bygenre.iterrows():
        # Calculate average ratings for App Store (excluding NaN values)
        app_store_ratings = [rating for rating in row['App Store Rating'] if not pd.isna(rating)]
        avg_app_store_rating = sum(app_store_ratings) / len(app_store_ratings) if app_store_ratings else None
        avg_app_store_ratings.append(avg_app_store_rating)

        # Calculate average ratings for Google Play (excluding NaN values)
        google_play_ratings = [rating for rating in row['Google Play Rating'] if not pd.isna(rating)]
        print(len(google_play_ratings))
        avg_google_play_rating = sum(google_play_ratings) / len(google_play_ratings) if google_play_ratings else None
        avg_google_play_ratings.append(avg_google_play_rating)

    # Plotting
    plt.figure(figsize=(10, 6))

    # Plot average ratings for App Store and Google Play
    plt.bar(genres, avg_app_store_ratings, color='blue', alpha=0.5, label='App Store')
    plt.bar(genres, avg_google_play_ratings, color='red', alpha=0.5, label='Google Play')

    plt.legend()
    plt.xlabel('Genres')
    plt.ylabel('Average Ratings')
    plt.title('Average App Store and Google Play Ratings by Genre')

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    '''
def price_rating_correlation(merged_data):
    '''
    Function for visualizing the correlation between application price and 
    average rating. Includes both Apple app store and Google play store data.
    Also prints the amount of outliers. 
    '''
    
    merged_data.head()
    merged_data['Google Play Price'] = pd.to_numeric(merged_data['Google Play Price'], errors='coerce')
    merged_data['App Store Price'] = pd.to_numeric(merged_data['App Store Price'], errors='coerce')
    merged_data['Google Play Rating'] = pd.to_numeric(merged_data['Google Play Rating'], errors='coerce')
    merged_data['App Store Rating'] = pd.to_numeric(merged_data['App Store Rating'], errors='coerce')    #Google Play Price,Google Play Rating
    
    merged_data['App Store Rating'].replace(0, np.nan, inplace=True)

    combined_prices = pd.concat([merged_data['Google Play Price'], merged_data['App Store Price']], ignore_index=True)
    combined_ratings = pd.concat([merged_data['Google Play Rating'], merged_data['App Store Rating']], ignore_index=True)
    combined_rewievs = pd.concat([merged_data['Google Play Reviews'], merged_data['App Store Reviews']], ignore_index=True)
    #rslt_df = dataframe[dataframe['Stream'].isin(options)] 
    outliers_google = merged_data[merged_data['Google Play Price'] > 50]
    outliers_apple = merged_data[merged_data['App Store Price'] > 50]
    print(len(outliers_google)+len(outliers_apple))
    #combined_df = pd.DataFrame({'combined_prices': combined_prices, 'combined_ratings': combined_ratings})
    plt.figure(figsize=(10, 6))
    plt.scatter(merged_data['Google Play Rating'], merged_data['Google Play Price'], label='Play Store', alpha=0.5)
    plt.scatter(merged_data['App Store Rating'], merged_data['App Store Price'], label='Apple Store', alpha=0.5)
    #plt.scatter(combined_df['combined_ratings'], combined_df['combined_prices'], alpha=0.5)
    plt.title('Price vs. Average Rating')
    plt.xlabel('Average Rating')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)

    plt.figure(figsize=(10, 6))
    plt.scatter(merged_data['Google Play Rating'], merged_data['Google Play Price'], alpha=0.5)
    plt.title('Price vs. Average Rating (Play Store)')
    plt.xlabel('Average Rating')
    plt.ylabel('Price (USD)')
    plt.grid(True)

    plt.show()


def price_rating_with_ranges(merged_data):
    '''
    To help with visualising, price ranges have been set. Pie chart. 
    The ranges are:
        free, 0-5 USD, 5-20 USD, 20-50 USD and more than 50 USD.
    '''
    pass

def downloads_age_rating():
    '''
    Function for analysing the relationship between amount of downloads 
    and contentrating.
    '''
    pass

def downloads_rating_correlation():
    '''s
    This function visualizes the relationship between the amount of 
    downloads and ratings.
    '''
    pass

def review_count_rating_correlation():
    '''
    This function takes into account the amount of reviews when considering ratings.
    '''
    pass

def review_download_ratio():
    '''
    This function gives the ratio between total amount of downloads and reviews.
    '''
    pass

