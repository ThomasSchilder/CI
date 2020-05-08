import json
import os

def convert(rootdir, filename):
	json_data = []
	for r,d,f in os.walk(rootdir):
		for name in f:
			if(name == filename):
				json_file = r + '/'+name
				file = open(json_file)
				for line in file:
					json_line = json.loads(line)
					json_data.append(json_line)
	return json_data
