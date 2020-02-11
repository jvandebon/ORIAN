import orian,requests,json,time
from subprocess import call

db_url = "http://cccad2.doc.ic.ac.uk:8080"
configured = orian.configure("http://cccad2.doc.ic.ac.uk:8081/jvandebon/rm_prototype/2.0")

if not configured:
        print("Invalid URL")
        exit(0)

REPEATS = 5


def orian_execute(task_name, params, volume, n, config_ext, impl_name, impl_rm, profile=False):
        orian.execute_sync(task_name, params, volume,
                [{'config': {'n': n, 'name': str(n) + config_ext},
                'impl': {'taskName': task_name,
                'implName': impl_name,
                'implRM': impl_rm}, 'problem_size': volume}],
                profile=profile)

task_name = input("task name: ")
params = json.loads(input("params: "))
allowed_vols = [int(x) for x in input("allowed volumes: ").split()]
device = input("dfe or cpu: ")

print(allowed_vols)

f = open(task_name + "_" + device + "-baseline_e2e.csv", 'w')
f.write("Config,Volume,Trial,E2E Time\n")

if device == "cpu":
	print("Collecting execution time with 1 CPU...")

	impl_rm = "hnode0.cpu0"
	impl_name = "cpu_compute"
	cpu_e2e_times = []
	for volume in allowed_vols:
		print(volume)

		vol_param = [p for p in params if p["param"] == "volume"]
		if len(vol_param) > 0:
			vol_param = vol_param[0]
			vol_param["value"] = volume 

		# execute once to handle any initial overhead
		if task_name == "align":
			orian_execute(task_name, params, volume, 1, 'T', impl_name, impl_rm)

		# execute REPEATS times and collect profiles
		for r in range(REPEATS):
			start = time.time()
			orian_execute(task_name, params, volume, 1, 'T', impl_name, impl_rm, profile=True)
			end = time.time()
			e2e_time = (end-start)
			f.write("1T,"+str(volume)+","+str(r)+","+str(e2e_time)+"\n")


if device == "dfe":
	print("Collecting execution time with 1 DFE...")

	impl_rm = "hnode0.dfe0"
	impl_name = "dfe_compute"
	dfe_e2e_times = []
	for volume in allowed_vols:

		print(volume)

		vol_param = [p for p in params if p["param"] == "volume"]
		if len(vol_param) > 0:
			vol_param = vol_param[0]
			vol_param["value"] = volume 

		# execute once to handle any initial overhead
		if task_name == "align":
			orian_execute(task_name, params, volume, 1, 'DFE', impl_name, impl_rm)

		# execute REPEATS times and collect profiles
		for r in range(REPEATS):
			start = time.time()
			orian_execute(task_name, params, volume, 1, 'DFE', impl_name, impl_rm, profile=True)
			end = time.time()
			e2e_time = (end-start)
			f.write("1DFE,"+str(volume)+","+str(r)+","+str(e2e_time)+"\n")

call(["mv", "../database/profile.db", "../database/profile_"+task_name+"_"+device+"_baseline.db"])



