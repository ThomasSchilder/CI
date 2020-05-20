import json_load

def average(companieslist):
    business = json_load.convert(rootdir, 'business.json')
    stars = [business['stars']) for companies in business if business['name'] in companieslist]
    return sum(stars)/len(stars)

def coverage
