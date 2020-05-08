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
for data in json_data:
	key = round(data["review_count"],1)
	if(key in review.keys()):
		review[key].add(data['user_id'])
	else:
		review[key] = set()
		review[key].add(data['user_id'])

lists = sorted(review.items()) # sorted by key, return a list of tuples
new_lists = []
total = 0
for entry in lists:
	total += len(entry[1])
	tuple = (entry[0], len(entry[1]))
	new_lists.append(tuple)

x, y = zip(*new_lists) # unpack a list of pairs into two tuples
plt.plot(x,y)
plt.title('Ten cities\nreviews per user\ntested on '+str(total))
plt.xlabel('Reviews')
plt.ylabel('Number of users')
plt.savefig('./plots/reviews_per_user.png')
plt.show()
