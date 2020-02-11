import sys,orian,json,requests
import numpy as np

## GET URLS AS INPUTS (?)

db_url = "http://cccad2.doc.ic.ac.uk:8080"
configured = orian.configure("http://cccad2.doc.ic.ac.uk:8081/jvandebon/rm_prototype/2.0")

if not configured:
        print("Invalid URL")
        exit(0)

REPEATS = 1

# input args: task name, impl name, params, min vol, max vol, granularity, allowed configs

#task_name = "nbody"
#impl_name = "cpu_compute"
#impl_rm = "hnode0.cpu0" ## GET THIS DIRECTLY SOMEHOW?
#params = [{"param": "volume", "value": 0}]
#min_vol = 1000
#max_vol = 20000 #65000
#granularity = 1000
#allowed_n = [1,2,4] #[1,2,3,4,5,6,7,8,9,10,11,12]

def get_range(min_vol, allowed_vols):
	max_vol = int(input("min vol = " + str(min_vol) + ", max vol: "))
	granularity = int(input("granularity (enter 0 if specifying allowed volumes): "))
	if granularity == 0:
		allowed_vols += [int(x) for x in input("allowed volumes: ").split()]
	else:
		if len(allowed_vols) != 0:
			min_vol = min_vol + granularity
		allowed_vols += list(range(min_vol, max_vol + 1, granularity))
	return max_vol	

allowed_vols = []
task_name = input("task name: ")
impl_name = input("impl name: ")
impl_rm = input("impl rm: ")
params = json.loads(input("params: "))
min_vol = int(input("min vol: "))
max_vol = get_range(min_vol, allowed_vols);

another_range = 1
while another_range == 1:
	another_range = int(input("add another range? (1/0): "))
	if another_range == 1:
		max_vol	= get_range(max_vol, allowed_vols)

allowed_n = a = [int(x) for x in input("allowed configurations: ").split()]

print(allowed_vols)
print(max_vol)

def orian_execute(task_name, params, volume, n, config_ext, impl_name, impl_rm, profile=False):
	orian.execute_sync(task_name, params, volume, 
		[{'config': {'n': n, 'name': str(n) + config_ext},
		'impl': {'taskName': task_name, 
		'implName': impl_name, 
		'implRM': impl_rm}, 'problem_size': volume}],
		profile=profile)

def get_average(task_name, config_ext, volume, n):
	profile_request = requests.get(db_url + "/profiles?task_name=" + task_name 
						+ "&config=" + str(n) + config_ext 
						+ "&problem_size=" + str(volume))
	profiles = json.loads(profile_request.text)
	return np.mean([float(p['problem_size'])/float(p['time'])/1000 for p in profiles])


print("Profiling:", task_name, impl_name, "\n")

if "cpu" in impl_name:
	config_ext = "T"
else:
	config_ext = "DFE"


for n in allowed_n:

	inc = 1
	volume = min_vol
	gran = 0
	ave_tp = 0
	prev_ave_tp = 0
	ave_del = 0
	prev_ave_del = 0
	ave_del2 = 0.1
	prev_ave_del2 = 0.1

	while volume <= max_vol:
		
		vol_param = [p for p in params if p["param"] == "volume"]
		if len(vol_param) > 0:
			vol_param = vol_param[0]
			vol_param["value"] = volume

		# execute once to handle any initial overhead
		orian_execute(task_name, params, volume, n, config_ext, impl_name, impl_rm)

		# execute REPEATS times and collect profiles
		for r in range(REPEATS):
			orian_execute(task_name, params, volume, n, config_ext, impl_name, impl_rm, profile=True)
			
		# calculate average tp for all collected profiles
		ave_tp = get_average(task_name, config_ext, volume, n)

		if 'nan' in str(ave_tp):
			print("NAN value encountered, something went wrong. Please start again.")
			exit(0)
	
		print(str(n) + " threads", volume, "TP: " + str(ave_tp))

		# compare average to previous average
		if prev_ave_tp != 0:
			ave_del = abs(ave_tp - prev_ave_tp)

		# compare change in averages to previous change in averages
		ave_del2 = ave_del - prev_ave_del

		print(ave_del, ave_del2,"\n")

		## update gran based on del2
		if ave_del2 <= 0 and prev_ave_del2 <= 0:
			print("increasing increment...")
			inc += 1
			ave_del2 = 0.1 # don't want to start negative

		gran += inc
		if gran >= len(allowed_vols):
			break;
		volume = allowed_vols[gran]

		prev_ave_del = ave_del
		prev_ave_tp = ave_tp
		prev_ave_del2 = ave_del2

	print("\n")

