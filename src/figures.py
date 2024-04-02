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
    This functions selects a handful of popular Genres and performs
    statistical analyses and visualizations of ratings
    '''

    avg_ratings = merged_data_bygenre.groupby('Genre').agg({'Google Play Rating': 'mean', 'App Store Rating': 'mean'}).reset_index()
    avg_ratings['Google Play Rating'] = avg_ratings['Google Play Rating'].round(2)
    avg_ratings['App Store Rating'] = avg_ratings['App Store Rating'].round(2)
    print(avg_ratings)
