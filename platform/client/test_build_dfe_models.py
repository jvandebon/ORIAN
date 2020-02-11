import requests, json, time, sys

rm_url = "http://maxnode2.doc.ic.ac.uk:8083/jvandebon/rm_prototype/2.0"

data = {}
data['taskName'] = "adp"
data['implName'] = "dfe_compute"
data['configuration'] = {}


result = requests.post(rm_url + "/models/build", json=data)
print(result)
'''
time.sleep(1)

data = {}
data['taskName'] = "align"
data['implName'] = "dfe_compute"
data['configuration'] = {}

result = requests.post(rm_url + "/models/build", json=data)
print(result)

time.sleep(1)

data = {}
data['taskName'] = "nbody"
data['implName'] = "dfe_compute"
data['configuration'] = {}

result = requests.post(rm_url + "/models/build", json=data)
print(result)
'''
