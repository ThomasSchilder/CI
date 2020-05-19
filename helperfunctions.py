import pandas as pd
import numpy as np
import os

from IPython.display import display

def checkForPickle(pickles):
    for r,d,f in os.walk(pickles):
        if(len(f) > 0):
            return True
        else:
            return False

def get_rating(ratings, userId, businessId):
    entries = ratings.loc[(ratings['user_id'] == userId) & (ratings['business_id'] == businessId)]
    if(entries['stars'].size == 0):
        return np.nan
    else:
        return entries['stars'].values[0]

def pivot_ratings(ratings):
    result = ratings.pivot(index='business_id', columns='user_id', values='stars')
    return result

def cosine_similarity(matrix, id1, id2):
    if id1 == id2:
        return 1

    selected_features = matrix.loc[id1].notna() & matrix.loc[id2].notna()

    if not selected_features.any():
        return np.nan

    features1 = matrix.loc[id1][selected_features]
    features2 = matrix.loc[id2][selected_features]

    top = features1 * features2
    top = top.sum()

    bottom_left = np.sqrt(np.square(features1).sum())
    bottom_right = np.sqrt(np.square(features2).sum())

    if bottom_left == 0 or bottom_right == 0:
        return np.nan

    bottom = bottom_left * bottom_right

    similarity_value = top / bottom

    if similarity_value is np.nan:
        return np.nan

    return similarity_value

def create_similarity_matrix_cosine(matrix):
    """creates the similarity matrix based on eucledian distance"""
    data = []
    for id1 in matrix.index:
        row = []
        for id2 in matrix.index:
            row.append(cosine_similarity(matrix, id1, id2))
        data.append(row)

    similarity_matrix = pd.DataFrame(data, index=matrix.index, columns=matrix.index, dtype=float)

    return similarity_matrix

def mean_center_columns(matrix):
    return matrix - matrix.mean()


def select_neighborhood(userId, similarity, utility_review, df_review, amount):
    if len(df_review[df_review["user_id"] == userId]) == 0:
        return "No reviews found, selecting top " + str(amount)

    top_review = df_review[df_review["user_id"] == userId]["stars"].sort_values(ascending=False).index[0]

    top_business = df_review.loc[top_review, "business_id"]

    similarities = similarity[top_business]
    reviews = utility_review[userId]

    similarities = similarities[similarities > 0].nlargest(n=amount)
    neighborhood = similarities[reviews > 0]

    return neighborhood

'''def pivot_ratings(ratings):
    business = ratings['business_id'].unique()
    users = ratings['user_id'].unique()
    frame = pd.DataFrame(index=business, columns=users)
    for y in frame.index:
        for x in frame.columns:
            frame[x][y] = get_rating(ratings, x, y)
    return frame
'''
