from IPython.display import display
import pandas as pd
#Helper functions are saved in separate file to keep the overview.
import helperfunctions as hf
import json_load
import sys

skip = False
picklesFound = hf.checkForPickle('./pickles');
if(picklesFound == True):
    answer = input('Already found matrices. Do you want to use these? Type yes/no\n')
    if(answer.lower() == 'yes'):
        skip = True
    else:
        print('No pickle files found that contain matrices. Creating new matrices now..............');
        skip = False

if (skip == False):
    df_training, df_test = hf.split_data(pd.DataFrame(json_load.convert('./data', 'review.json')))
    print('trainingset' + str(len(df_training)))
    print('testset' + str(len(df_test)));

    #dataframes: read every json file in the data folder.
    df_business = pd.DataFrame(json_load.convert('./data', 'business.json'))[['business_id', 'name','city','state','stars','review_count']]
    df_review = pd.DataFrame(json_load.convert('./data', 'review.json'))[['review_id','user_id','business_id','stars','date', 'text']]
    df_review.to_pickle("./pickles/df_review.pkl")
    df_business.to_pickle("./pickles/df_business.pkl");

    #Utility matrixes don't like users that review the same restaurant twice. So I removed duplicates.
    df_review.drop_duplicates(subset =["business_id","user_id"], keep = False, inplace = True)

    #utility matrix:
    utility_review = hf.pivot_ratings(df_review)
    utility_review.to_pickle('./pickles/utility.pkl')

    #mean center utility matrix
    centered = hf.mean_center_columns(utility_review)

    #cosine similarity matrix:
    similarity = hf.create_similarity_matrix_cosine(centered)
    similarity.to_pickle('./pickles/similarity.pkl')
else:
    #use the dataframes that where already created before.
    utility_review = pd.read_pickle("./pickles/utility.pkl")
    similarity = pd.read_pickle("./pickles/similarity.pkl")
    df_review = pd.read_pickle("./pickles/df_review.pkl");

userId = "upGYcgeV-g_qcfIOdL87Lg"
recommend = hf.select_neighborhood(userId, similarity, utility_review, df_review, 10)

display(recommend)
