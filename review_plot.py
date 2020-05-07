import numpy as np
import matplotlib.pyplot as plt
import json
import os
rootdir ='./data'

json_data = []
review = {}
reviews = 0
 #Convert all data
for r,d,f in os.walk(rootdir):
	for name in f:
		if(name == 'review.json'):
			json_file = r + '/'+name
			file = open(json_file)
			for line in file:
				reviews += 1
				json_line = json.loads(line)
				json_data.append(json_line)

#Create review plot
for x in json_data:
	key = round(x["stars"],1)
	if(key in review.keys()):
		review[key] += 1
	else:
		review[key] = 1

lists = sorted(review.items()) # sorted by key, return a list of tuples

x, y = zip(*lists) # unpack a list of pairs into two tuples
plt.plot(x,y)
plt.title('Ten cities\nFirst '+ str(reviews) +' reviews')
plt.xlabel('Score')
plt.ylabel('Number of reviews')
plt.savefig('./plots/reviews_per_score.png')
