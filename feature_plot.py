import numpy as np
import matplotlib.pyplot as plt
import json
import os
import json_load

rootdir ='./data'
file = 'user.json'

json_data = json_load.convert(rootdir, file)
review = {}

#Create feature plot
for x in json_data:
	key = round(x["review_count"],1)
	if(key in review.keys()):
		review[key].add(x['user_id'])
	else:
		review[key] = set()
		review[key].add(x['user_id'])

lists = sorted(review.items()) # sorted by key, return a list of tuples
(print(lists))

x, y = zip(*lists) # unpack a list of pairs into two tuples
plt.plot(x,y)
plt.title('Ten cities\nreviews per user\ntested on ')
plt.xlabel('Users')
plt.ylabel('Number of reviews')
plt.savefig('./plots/reviews_per_user.png')
plt.show()
