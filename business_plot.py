import json
import matplotlib.pyplot as plt
from collections import Counter, OrderedDict
import os
import json_load

rootdir ='./data'
file = 'business.json'
json_data = json_load.convert(rootdir, file)

# Plot categories
#  sort attributes
restaurants = [str(restaurants['categories']).split(', ') for restaurants in json_data]
all_categories = (dict(Counter([categorie for restaurant in restaurants for categorie in restaurant])))
# Plot a histogram that shows how many of each categorie exists in a town
lists = dict(sorted(all_categories.items()))
keys = lists.keys()
values = lists.values()
plt.bar(lists.keys(), lists.values(), width= 1, color='g')
plt.tick_params(axis='x', which='major', labelsize=0.4)
plt.xticks(rotation=90)
plt.show()

# Plot ratings
restaurants_stars = dict(Counter([restaurants['stars'] for restaurants in json_data]))
restaurants_stars = dict(sorted(restaurants_stars.items()))
keys = restaurants_stars.keys()
values = restaurants_stars.values()
plt.bar(restaurants_stars.keys(), restaurants_stars.values(), color='b')
plt.tick_params(axis='x', which='major', labelsize=8)
plt.xticks(rotation=90)
plt.show()
