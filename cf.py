from IPython.display import display
import pandas as pd
#Helper functions are saved in separate file to keep the overview.
import helperfunctions as hf
import json_load

#dataframes: read every json file in the data folder.
df_business = pd.DataFrame(json_load.convert('./data', 'business.json'))[['business_id', 'name','city','state','stars','review_count']]
df_review = pd.DataFrame(json_load.convert('./data', 'review.json'))[['review_id','user_id','business_id','stars','date', 'text']]

#Utility matrixes don't like users that review the same restaurant twice. So I removed duplicates.
df_review.drop_duplicates(subset =["business_id","user_id"], keep = False, inplace = True)

#utility matrix:
utility_review = hf.pivot_ratings(df_review)


display(utility_review.head())
