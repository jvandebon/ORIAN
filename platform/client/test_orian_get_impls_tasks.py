import orian, time, json,sys

configured = orian.configure("http://cccad2.doc.ic.ac.uk:8081/jvandebon/rm_prototype/2.0")

if not configured:
	print("Invalid URL")
	exit(0)

print(orian.get_tasks())
print(orian.get_impls())


