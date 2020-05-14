import pandas as pd
import numpy as np

def get_rating(ratings, userId, businessId):
    entries = ratings.loc[(ratings['user_id'] == userId) & (ratings['business_id'] == businessId)]
    if(entries['stars'].size == 0):
        return np.nan
    else:
        return entries['stars'].values[0]

def pivot_ratings(ratings):
    result = ratings.pivot(index='business_id', columns='user_id', values='stars')
    return result

'''def pivot_ratings(ratings):
    business = ratings['business_id'].unique()
    users = ratings['user_id'].unique()
    frame = pd.DataFrame(index=business, columns=users)
    for y in frame.index:
        for x in frame.columns:
            frame[x][y] = get_rating(ratings, x, y)
    return frame
'''
