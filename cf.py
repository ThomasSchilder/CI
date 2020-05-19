from IPython.display import display
import pandas as pd
#Helper functions are saved in separate file to keep the overview.
import helperfunctions as hf
import json_load
import sys
import numpy as np

skip = False
picklesFound = hf.checkForPickle('./pickles')
if(picklesFound == True):
    answer = input('Already found matrices. Do you want to use these? Type yes/no\n')
    if(answer.lower() == 'yes'):
        skip = True
    else:
        print('No pickle files found that contain matrices. Creating new matrices now..............')
        skip = False

df_training = None
df_test = None
if (skip == False):
    data = pd.DataFrame(json_load.convert('./data', 'review.json'))
    data.drop_duplicates(subset =["business_id","user_id"], keep = False, inplace = True)

    df_training, df_test = hf.split_data(data)
    df_training.to_pickle('./pickles/df_training.pkl')
    df_test.to_pickle('./pickles/df_test.pkl')

    print('trainingset' + str(len(df_training)))
    print('testset' + str(len(df_test)))

    #utility matrix:
    utility_review = hf.pivot_ratings(df_training)
    utility_review.to_pickle('./pickles/utility.pkl')

    #mean center utility matrix
    centered = hf.mean_center_columns(utility_review)

    #cosine similarity matrix:
    similarity = hf.create_similarity_matrix_cosine(centered)
    similarity.to_pickle('./pickles/similarity.pkl')

    business = pd.DataFrame(json_load.convert('./data', 'business.json'))
    business.to_pickle('./pickles/business.pkl')
else:
    #use the dataframes that where already created before.
    df_training = pd.read_pickle("./pickles/df_training.pkl")
    df_test = pd.read_pickle("./pickles/df_test.pkl")
    utility_review = pd.read_pickle("./pickles/utility.pkl")
    similarity = pd.read_pickle("./pickles/similarity.pkl")
    business = pd.read_pickle("./pickles/business.pkl")



TEST = False
userId = "t-nB38eHbeFuabXBdJMwvg"

if TEST:
    # item based
    predicted_item_based = hf.predict_ratings_item_based(similarity, utility_review, df_test[['user_id', 'business_id', 'stars']], TEST)
    # random
    predicted_random = df_test.copy()[['user_id', 'business_id', 'stars']]
    predicted_random["predicted stars"] = np.random.uniform(0.5, 5.0, predicted_random.shape[0])

    # mean
    means = df_test.groupby("business_id").mean()["stars"]
    predicted_item_mean = df_test.join(means, on="business_id", rsuffix="_2").rename(columns={"stars_2": "predicted stars"})

    hf.make_plots(predicted_item_based, predicted_random, predicted_item_mean)
else:
    business["user_id"] = userId
    business = business.reindex(columns=['business_id', 'user_id', 'name'])
    business["stars"] = None

    predicted_item_based = hf.predict_ratings_item_based(similarity, utility_review, business, TEST)
    print(predicted_item_based.nlargest(20, "predicted stars"))

