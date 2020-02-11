import orian,requests,json,time
from subprocess import call

configured = orian.configure("http://cccad2.doc.ic.ac.uk:8081/jvandebon/rm_prototype/2.0")

if not configured:
        print("Invalid URL")
        exit(0)

task_name = input("task name: ")
params = json.loads(input("params: "))
volumes = [int(x) for x in input("volumes: ").split()]
max_time = float(input("max time (0 if none): "))

for volume in volumes:

	print(volume, max_time)

	vol_param = [p for p in params if p["param"] == "volume"]
	if len(vol_param) > 0:
		vol_param = vol_param[0]
		vol_param["value"] = volume 

	if max_time != 0:
		objectives = {'time': {'max': max_time}}
	else:
		objectives = {}

	orian.execute(task_name, params, volume, objectives=objectives, profile=True)
#	time.sleep(1.5)
