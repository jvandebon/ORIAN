import requests, sys, orian, json, time
import numpy as np

def predict_io_time(coefs, volume):
	return coefs[0]*volume + coefs[1]

def predict_compute_time(task, p1, x_):

	if len(p1) == 1:
		return x_ / (1000*p1[0])
	if task == "nbody":
		return x_ / (1000*np.exp(p1[0] + p1[1]*x_ + p1[2]*x_**2 + p1[3]*x_**3 + p1[4]*x_**4))

	elif task == "align" or task == "adp":
		return x_ / (1000*p1[0]* np.log(abs(p1[1] * x_)) + p1[2])


db_url = "http://cccad2.doc.ic.ac.uk:8080"
configured = orian.configure("http://cccad2.doc.ic.ac.uk:8081/jvandebon/rm_prototype/2.0")

if not configured:
        print("Invalid URL")
        exit(0)

REPEATS = 3

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

volumes = []
task_name = input("task name: ")
impl_name = input("impl name: ")
impl_rm = input("impl rm: ")
params = json.loads(input("params: "))
min_vol = int(input("min vol: "))
max_vol = get_range(min_vol, volumes);

another_range = 1
while another_range == 1:
        another_range = int(input("add another range? (1/0): "))
        if another_range == 1:
                max_vol = get_range(max_vol, volumes)

if 'dfe' in impl_name:
	config_ext = 'DFE'
else:
	config_ext = 'T'

# get all models for task and device
model_request = requests.get(db_url + "/models?task_name=" + task_name)
models = json.loads(model_request.text)

if 'dfe' in impl_name:
	models = [m for m in models if 'DFE' in m['config']]
else:
	models = [m for m in models if 'T' in m['config']]

# determine all possible configurations from models
configs = list(set([m['config'] for m in models]))

configs = ['1DFE', '2DFE']
print(configs)

# determine appropriate volume values for each task 
e2e_times = {}


for c in configs:
	print(c)
	e2e_times[c] = {}
	for volume in volumes:
		
		vol_param = [p for p in params if p["param"] == "volume"]
		if len(vol_param) > 0:
			vol_param = vol_param[0]
			vol_param["value"] = volume

		# execute with profile flag 
		e2e_times[c][volume] = []
		for i in range(REPEATS):

			start = time.time()
			orian.execute_sync(task_name, params, volume,
		                [{'config':{'n': int(c[:-len(config_ext)]), 'name': c},
		                 'impl': {'taskName': task_name,
	        	        'implName': impl_name,
	                	'implRM': impl_rm}, 'problem_size': volume}],
	              		 profile=True)
			end = time.time()

			# record end to end time for each execution
			e2e_times[c][volume].append(end-start)

csv_lines = []		
headers = "Config,Volume,ObservedE2E,PredictedE2E,DELTA,DELTA/Observed,ObservedE2E,ProfileE2E,DELTA,DELTA/Observed,PredictedE2E,ProfileE2E,DELTA,Delta/Profile,PredictedIO,ProfileIO,DELTA,Delta/Profile,PredictedCompute,ProfileCompute,DELTA,DELTA/profile\n"
csv_lines.append(headers)
for c in configs:
	for volume in volumes:

		# use model to get predicted IO time
		io_model = [m for m in models if m['type'] == 'io' and m['config'] == c and m['min_size'] < volume and m['max_size'] > volume][0]
		predict_io = predict_io_time(io_model['coefs'], volume)

		# use model to get predicted TP time
		tp_model = [m for m in models if m['type'] == 'tp' and m['config'] == c and m['min_size'] < volume and m['max_size'] >= volume][0]
		predict_compute = predict_compute_time(task_name, tp_model['coefs'], volume)

		predict_e2e = predict_io + predict_compute
		
		# find profiles
		profile_request = requests.get(db_url + "/profiles?task_name=" + task_name
	                                                + "&config=" + c
	                                                + "&problem_size=" + str(volume))
		profiles = json.loads(profile_request.text)
		print("\n", c, volume, len(profiles))
		
		# average profile IO time
		io_times = [p['io_time'] for p in profiles]
		ave_profile_io = np.mean(io_times)
		
		# average profile TP time
		compute_times = [p['time'] for p in profiles]
		tps = [p['problem_size']/p['time']/1000 for p in profiles]
		ave_profile_compute = np.mean(compute_times)

		profile_e2e = ave_profile_io + ave_profile_compute

		# average recorded end to end times
		ave_e2e = np.mean(e2e_times[c][volume])


		csv_line = c+","+str(volume)+","
		csv_line += str(ave_e2e)+","+str(predict_e2e)+","+str(ave_e2e-predict_e2e)+","+str(abs(ave_e2e-predict_e2e)/ave_e2e)
		csv_line += ","+str(ave_e2e)+","+str(profile_e2e)+","+str(ave_e2e-profile_e2e)+","+str(abs(ave_e2e-profile_e2e)/ave_e2e)
		csv_line += ","+str(predict_e2e)+","+str(profile_e2e)+","+str(predict_e2e-profile_e2e)+","+str(abs(predict_e2e-profile_e2e)/profile_e2e)
		csv_line += ","+str(predict_io)+","+str(ave_profile_io)+","+str(predict_io-ave_profile_io)+","+str(abs(predict_io-ave_profile_io)/ave_profile_io)
		csv_line += ","+str(predict_compute)+","+str(ave_profile_compute)+","+str(predict_compute-ave_profile_compute)+","+str(abs(predict_compute-ave_profile_compute)/ave_profile_compute)
		csv_line += "\n"

		csv_lines.append(csv_line)

		continue
		
		# compare model IO and profile IO
		print("MODEL IO v PROFILE IO: ", predict_io, ave_profile_io, predict_io-ave_profile_io)
		# compare model TP and profile TP
		print("MODEL COMPUTE v PROFILE COMPUTE: ", predict_compute, ave_profile_compute, predict_compute - ave_profile_compute)

		# compare model IO + TP and end to end time
		print("MODEL v E2E: ", predict_e2e, ave_e2e, predict_e2e-ave_e2e)
		
		# compare profile IO + TP and end to end time   
		print("PROFILE v E2E: ", profile_e2e, ave_e2e, profile_e2e-ave_e2e)

with open(task_name+"-"+impl_name+"-12DFEevaluation.csv", 'w') as f:
	print("Writing results to " + task_name+"-"+impl_name+"-12DFEevaluation.csv ...")
	for line in csv_lines:
		f.write(line)

