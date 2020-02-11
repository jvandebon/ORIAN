import requests, json, time, sys

rm_url = "http://cccad2.doc.ic.ac.uk:8087/jvandebon/rm_prototype/2.0"

result = requests.get(rm_url + "/managers/available")

print(result.text)
