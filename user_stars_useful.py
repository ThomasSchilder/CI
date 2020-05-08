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
	key = round(data["average_stars"],1)
	review[key] = data['useful']


lists = sorted(review.items()) # sorted by key, return a list of tuples

x, y = zip(*lists) # unpack a list of pairs into two tuples
plt.plot(x,y)
plt.title('Ten cities\nUsefulness based on average stars\ntested on')
plt.xlabel('Average stars')
plt.ylabel('Noted as useful')
plt.savefig('./plots/user_stars_usefull.png')
plt.show()
