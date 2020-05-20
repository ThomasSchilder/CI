import json
import os

def convert(file):
    for line in file:
        line = line.strip()
        if line == "":
            continue
        json_line = json.loads(line)
        json_data.append(json_line)
    return json_data
