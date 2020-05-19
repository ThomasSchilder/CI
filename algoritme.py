import numpy as np
import json
import os
import json_load
import collections
import pandas as pd
import itertools
import random
import statistics
import helperfunctions as hf

rootdir ='./data'

df_training, df_test = hf.split_data(pd.DataFrame(json_load.convert('./data', 'review.json')))
training_json = df_training.to_json(orient='records')
test_json = df_test.to_json(orient='records')
trainingdata = json.loads(training_json)
testdata = json.loads(test_json)
#print(training_json)

# Returns a list with user id's from the region
def user_list():
    return [user['user_id'] for user in json_load.convert(rootdir, 'user.json')]

# Returns a dict with review scores from the user
def user_reviews(user, data):
    review_list = data;
    business_list = json_load.convert(rootdir, 'business.json')
    business_dict = {}

    for business in business_list:
        business_dict[business["business_id"]] = business["categories"]

    user_reviews = {review['business_id']:(review['stars'], [category.strip() for category in business_dict[review['business_id']].split(',')]) for review in review_list if review['user_id'] == user and review['stars'] >= 3}
    return user_reviews

# Returns a list with all company's in the same categories the user likes
def relevant_companies(user_reviews):
    business_list = json_load.convert(rootdir, 'business.json')
    company_list = []

    category_list = []
    for review in user_reviews:
        category_list.extend(user_reviews[review][1])
    category_set = set(category_list)

    for business in business_list:
        for category in category_set:
            if business["categories"] != None:
                if category in business["categories"]:
                    company_list.append(business["business_id"])

    return company_list

# Returns a list with all attributes that occured in the users ratings with their respective importance for the user
def user_attributes(user_reviews):
    business_list = json_load.convert(rootdir, 'business.json')
    company_list = [key for key in user_reviews]
    attribute_dict = {}

    for business in business_list:
        if business['business_id'] in company_list:
            attributes = business['attributes']
            if attributes != None:
                for attribute in attributes:
                    if attributes[attribute] == 'True':
                        if attribute in attribute_dict:
                            attribute_dict[attribute] += 1
                        else:
                            attribute_dict[attribute] = 1

    for attribute in attribute_dict:
        attribute_dict[attribute] = (attribute_dict[attribute], attribute_dict[attribute] / len(user_reviews))

    return {k: v for k, v in sorted(attribute_dict.items(), reverse=True, key=lambda item: item[1][1])}

# Creates a matrix with all companies and wich attributes apply to them
def attribute_matrix(relevant_companies, user_attributes):
    matrix = pd.DataFrame(index=set(relevant_companies), columns=list(user_attributes))
    business_list = json_load.convert(rootdir, 'business.json')

    for business in business_list:
        if business['business_id'] in matrix.index:
            for attribute in matrix.columns:
                matrix[attribute][business['business_id']] = 0
                if business['attributes'] != None:
                    if attribute in business['attributes']:
                        if business['attributes'][attribute] == 'True':
                            matrix[attribute][business['business_id']] = user_attributes[attribute][1]
    return matrix

# Returns a dict with all companies and their respective summed score of the attributes
def company_dict(matrix):
    sum_dict = {}

    for company in matrix.index:
        sum_dict[company] = sum(matrix.loc[company])
    return {k: v for k, v in sorted(sum_dict.items(), reverse=True, key=lambda item: item[1])}

# recommends the user 20 business with the highest scores
def user_recomendations(company_dict, user_reviews):
    business_list = json_load.convert(rootdir, 'business.json')

    for company in business_list:
        if company['business_id'] in company_dict:
            if len(user_reviews) > 9:
                company_dict[company['business_id']] = (company_dict[company['business_id']] * 0.7) * (company['stars'] * 0.3)
            elif len(user_reviews) > 4:
                company_dict[company['business_id']] = (company_dict[company['business_id']] * 0.5) * (company['stars'] * 0.5)

    return dict(itertools.islice({k: v for k, v in sorted(company_dict.items(), reverse=True, key=lambda item: item[1])}.items(), 20))

# returns the user 20 random recomendations
def random_recomendations(company_dict, user_reviews):
    business_list = json_load.convert(rootdir, 'business.json')

    for company in business_list:
        if company['business_id'] in company_dict:
            if len(user_reviews) > 9:
                company_dict[company['business_id']] = (company_dict[company['business_id']] * 0.7) * (company['stars'] * 0.3)
            elif len(user_reviews) > 4:
                company_dict[company['business_id']] = (company_dict[company['business_id']] * 0.5) * (company['stars'] * 0.5)

    return_dict = {}
    for x in range(20):
        company = random.choice(list(company_dict))
        return_dict[company] = company_dict[company]

    return return_dict

def calculate_deviation(data, businesses):
    totalValue = 0;
    items = 0;
    for key in data.keys():
        value = data[key];
        rating = 0
        for business in businesses:
            for (x, y) in business.items():
                if y == key:
                    rating = business['stars']
        totalValue += abs(rating-value);
        items += 1
    return totalValue/items


    return user_list()

# generate basics
user_list = user_list()
user_reviews = user_reviews("_zPT9ZmR5-nUfsprzIiRew", trainingdata)

user_attributes = user_attributes(user_reviews)
business_list = json_load.convert(rootdir, 'business.json')
recoms = []
# user based
if len(user_reviews) < 5:
    business_dict = {business['business_id']:business['stars'] for business in business_list}
    sorted_dict = {k: v for k, v in sorted(business_dict.items(), reverse=True, key=lambda item: item[1])}

    top_list = []
    i = 0
    for business in business_dict:
        if i == 100:
            break
        top_list.append(business)
        i += 1

    recomendations = [random.choice(top_list) for x in range(20)]
    recoms = recomendations
    '''
    for item in business_list:
        if item['business_id'] in recomendations:
            #print(item['name'])
            print('joe')'''

else:
    relevant_companies = relevant_companies(user_reviews)
    attribute_matrix = attribute_matrix(relevant_companies, user_attributes)
    company_dict = company_dict(attribute_matrix)
    recomendations = user_recomendations(company_dict, user_reviews)
    recoms = recomendations
    value_list = []
    for company in recomendations:
        value_list.append(recomendations[company])
        '''
    for item in business_list:
        if item['business_id'] in recomendations:
            print(item['name'])'''
            #print('joe')
    content_training = (sum(value_list) / len(value_list))

print(recoms)
print(calculate_deviation(recoms, business_list))
# random based
# business_list = json_load.convert(rootdir, 'business.json')
# business_id_list = [business['business_id'] for business in business_list]
# random_matrix = attribute_matrix(business_id_list, user_attributes)
# random_company_dict = company_dict(random_matrix)
# recomendations_random = random_recomendations(random_company_dict, user_reviews)

# value_list = []
# for company in recomendations_random:
#     value_list.append(recomendations_random[company])

# print("random based recomendations:",  (sum(value_list) / len(value_list)))
