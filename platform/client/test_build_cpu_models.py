import requests, json, time, sys

rm_url = "http://maxnode2.doc.ic.ac.uk:8082/jvandebon/rm_prototype/2.0"

data = {}
data['taskName'] = "adp"
data['implName'] = "cpu_compute"
data['configuration'] = {}

print(data)

result = requests.post(rm_url + "/models/build", json=data)
'''
time.sleep(1)

data = {}
data['taskName'] = "align"
data['implName'] = "cpu_compute"
data['configuration'] = {}

print(data)

result = requests.post(rm_url + "/models/build", json=data)

time.sleep(1)

data = {}
data['taskName'] = "nbody"
data['implName'] = "cpu_compute"
data['configuration'] = {}

print(data)

result = requests.post(rm_url + "/models/build", json=data)

time.sleep(1)
'''
