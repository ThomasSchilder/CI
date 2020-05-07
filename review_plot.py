import numpy as np
import matplotlib.pyplot as plt
import json
import os
rootdir ='./data'

json_data = []
review = {}
reviews = 0
 #get all data
for r,d,f in os.walk(rootdir):
	for name in f:
		if(name == 'review.json'):
			json_file = r + '/'+name
			file = open(json_file)
			for line in file:
				reviews += 1
				json_line = json.loads(line)
				json_data.append(json_line)

for x in json_data:
	print(review)
	key = round(x["stars"],1)
	if(key in review.keys()):
		review[key] += 1
	else:
		review[key] = 1

lists = sorted(review.items()) # sorted by key, return a list of tuples

x, y = zip(*lists) # unpack a list of pairs into two tuples
print(reviews)
plt.plot(x,y)
plt.title('Ten cities\nFirst '+ str(reviews) +' reviews')
plt.xlabel('Number of reviews')
plt.ylabel('Score')
plt.show()
