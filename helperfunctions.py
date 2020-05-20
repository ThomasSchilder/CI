import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from IPython.display import display

def split_data(data,d=0.75):
	""" split data in a training and test set
	   `d` is the fraction of data in the training set"""
	np.random.seed(seed=5)
	mask_test = np.random.rand(data.shape[0]) < d
	return data[mask_test], data[~mask_test]

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

def select_neighborhood(similarities, ratings, k, test):
    neighborhood = similarities[similarities > 0].nlargest(n=k)
    if test:
        neighborhood = neighborhood[ratings > 0]
    
    return neighborhood

def weighted_mean(neighborhood, ratings):  
    similarities = neighborhood * ratings
    similarities = similarities.dropna()
        
    top = similarities.sum()
    bottom = neighborhood.sum()
    
    if bottom == 0:
        return np.nan
        
    return top / bottom
	

def predict_ratings_item_based(similarity, utility, user_item_pairs, test):
    ratings_test_c = user_item_pairs.copy()
    
    for index, row in ratings_test_c.iterrows():
        if row["user_id"] not in utility or row["business_id"] not in similarity:
            ratings_test_c.loc[index, "predicted stars"] = None
            continue

        neighborhood = select_neighborhood(similarity[row["business_id"]], utility[row["user_id"]], 100, test)
        prediction = weighted_mean(neighborhood, utility[row["user_id"]])
        ratings_test_c.loc[index, "predicted stars"] = prediction
        
    return ratings_test_c[ratings_test_c["predicted stars"] > 0]

def mse(predicted_ratings):
    difference = predicted_ratings["stars"] - predicted_ratings["predicted stars"]
    squared = np.square(difference)
    return squared.sum() / len(predicted_ratings)

def make_plots(predicted_item_based, predicted_random, predicted_item_mean):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(ncols=2, nrows=2)
    fig.tight_layout(pad=3.0)

    axes = [ax1, ax2, ax3, ax4]
    data = [predicted_item_based['stars'],
            predicted_item_based['predicted stars'],
            predicted_random['predicted stars'], 
            predicted_item_mean['predicted stars']]
    titles = ["actual ratings", "predicted item based", "predicted random", "predicted mean"]

    for ax, d, title in zip(axes, data, titles):
        ax.hist(list(d), bins=list(np.arange(0,5.5,0.25)))
        ax.set_xlabel("stars")
        ax.set_ylabel("amount")
        ax.set_title(title)

    print('     | actual | item | random | mean')
    print('-----+--------+------+------+-----')
    print(f'mean |   {data[0].mean():.2f} | {data[1].mean():.2f} | {data[2].mean():.2f} | {data[3].mean():.2f}')
    print(f'std  |   {data[0].std():.2f} | {data[1].std():.2f} | {data[2].std():.2f} | {data[3].std():.2f}')
    print(f'mse  |   {0:.2f} | {mse(predicted_item_based):.2f} | {mse(predicted_random):.2f} | {mse(predicted_item_mean):.2f}')
    
    plt.show()




tresholds = [2.5, 3.0, 3.5, 4.0, 4.5]
treshold_used = 4

def recommended(predictions, treshold):
    return predictions[predictions["predicted stars"] >= treshold]
    

def hidden(predictions, treshold):
    return predictions[predictions["predicted stars"] < treshold]

def used(predictions, treshold):
    return predictions[predictions["stars"] >= treshold]
    

def unused(predictions, treshold):
    return predictions[predictions["stars"] < treshold]

def confusion(recommended, hidden, used, unused):
    tp = len(pd.merge(recommended, used, how='inner'))
    fp = len(pd.merge(recommended, unused, how='inner'))
    tn = len(pd.merge(hidden, unused, how='inner'))
    fn = len(pd.merge(hidden, used, how='inner'))
    
    data = [[tp, fp], [fn, tn]]
    
    return pd.DataFrame(data, columns=['used', 'unused'], index=['recommended', 'hidden'])

def precision(confusion_matrix):
    tp = confusion_matrix.loc["recommended", "used"]
    fp = confusion_matrix.loc["recommended", "unused"]
    return tp / (tp + fp)

def recall(confusion_matrix):
    tp = confusion_matrix.loc["recommended", "used"]
    fn = confusion_matrix.loc["hidden", "used"]
    return tp / (tp + fn)

def precision_recall(predicted_ratings, treshold_recommended, treshold_used):
    recommended_items = recommended(predicted_ratings, treshold_recommended)
    hidden_items = hidden(predicted_ratings, treshold_recommended)
    used_items = used(predicted_ratings, treshold_used)
    unused_items = unused(predicted_ratings, treshold_used)
    
    confusion_matrix = confusion(recommended_items, hidden_items, used_items, unused_items)
    
    return precision(confusion_matrix), recall(confusion_matrix)

def plot_precision_recall(predicted_ratings):
    precisions = []
    recalls = []
    for treshold_recommended in tresholds:
        precision_value, recall_value = precision_recall(predicted_ratings, treshold_recommended, treshold_used)
        precisions.append(precision_value)
        recalls.append(recall_value)
        
    plt.plot(recalls, precisions)
    for r, p, t in zip(recalls, precisions, tresholds):
        plt.text(r, p, t)

def make_plots2(item_based, random, mean):
    plot_precision_recall(item_based)
    plot_precision_recall(random)
    plot_precision_recall(mean)

    plt.title("Precision/recall curve voor verschillende thresholds. Threshold used=4")
    plt.xlim(0.0, 1.0)
    plt.ylim(0.3, 1.0)
    plt.xlabel('recall')
    plt.ylabel('precision')

    plt.legend(['Item based collaborative filtering', 'Predictions with random', 'Predictions with mean'], loc = 'lower left')
    plt.show()

