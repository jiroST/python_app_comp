import matplotlib.pyplot as plt
from utils import *
import seaborn as sns


def category_pie_chart(merged_data): 
    
    merged_data['sum'] = merged_data[['Count App Store', 'Count Google Play Store']].sum(axis=1)
    merged_data_sorted = merged_data.sort_values('sum', ascending = False)
    print("The sorted sum of the App Store and Play Store counts:\n", merged_data_sorted)
    merged_data_sorted_top = merged_data_sorted[:7]

    merged_data_sorted_last = pd.DataFrame(data = {'Genre' : ['Other genres'], 'sum' : [merged_data['sum'][7:].sum()]})

    merged_data_sorted_com = pd.concat([merged_data_sorted_top, merged_data_sorted_last])

    plt.figure()
    plt.pie(merged_data_sorted_com['sum'], labels=merged_data_sorted_com['Genre'], autopct='%1.1f%%')
    plt.legend(loc='upper left')
    plt.title('The division of applications among genres')
    plt.show()  

def ratings_visualization(merged_data_bygenre):
    '''
    This functions takes a handful of popular Genres and performs
    statistical analyses and visualizations of ratings
    '''

    # Create lists out of ratings information for each app store for ease of use
    avg_google_play_ratings = merged_data_bygenre['Google Play Avg Rating'].tolist()
    avg_app_store_ratings = merged_data_bygenre['App Store Avg Rating'].tolist()
    genres = merged_data_bygenre['Genre'].tolist()

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

def ave_rating_cost_KDE_plot(merged_data):
    '''
    Function for visualizing whether an application is paid or free affects average rating. 
    Includes both Apple app store and Google play store data.
    '''

    plt.figure(figsize=(10, 6))

    merged_data = merged_data[merged_data['App Store Price'] < 100]
    merged_data = merged_data[merged_data['Google Play Price'] < 100]

    free_apps_app = merged_data[merged_data['App Store Price'] == 0]
    paid_apps_app = merged_data[merged_data['App Store Price'] > 0]
    free_apps_play = merged_data[merged_data['Google Play Price'] == 0]
    paid_apps_play = merged_data[merged_data['Google Play Price'] > 0]

    sns.kdeplot(data=free_apps_app, x='App Store Rating', label='Free Apps (Apple)', fill=True)
    sns.kdeplot(data=paid_apps_app, x='App Store Rating', label='Paid Apps (Apple)', fill=True)
    sns.kdeplot(data=free_apps_play, x='Google Play Rating', label='Free Apps (Google)', fill=True)
    sns.kdeplot(data=paid_apps_play, x='Google Play Rating', label='Paid Apps (Google)', fill=True)

    plt.xlim(1, 5)

    plt.title('Difference in paid and free rating')
    plt.xlabel('Average Rating')
    plt.ylabel('Density')
    plt.legend(loc='upper left')
    plt.grid(True)

    plt.show()
