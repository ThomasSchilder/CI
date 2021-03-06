import numpy as np
import matplotlib.pyplot as plt
import json
import os
import json_load

rootdir ='./data'
file = 'review.json'

json_data = json_load.convert(rootdir, file)
review = {}

#Create review plot
for x in json_data:
	key = round(x["stars"],1)
	if(key in review.keys()):
		review[key] += 1
	else:
		review[key] = 1

lists = sorted(review.items()) # sorted by key, return a list of tuples
print(lists)
x, y = zip(*lists) # unpack a list of pairs into two tuples
plt.plot(x,y)
plt.title('Ten cities\nFirst '+ str(len(json_data)) +' reviews')
plt.xlabel('Score')
plt.ylabel('Number of reviews')
plt.savefig('./plots/reviews_per_score.png')
plt.show()
