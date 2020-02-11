import orian,requests,json,time
from subprocess import call

db_url = "http://cccad2.doc.ic.ac.uk:8080"
configured = orian.configure("http://cccad2.doc.ic.ac.uk:8081/jvandebon/rm_prototype/2.0")

if not configured:
        print("Invalid URL")
        exit(0)

def orian_execute(task_name, params, volume, n, config_ext, impl_name, impl_rm, profile=False):
        orian.execute(task_name, params, volume,
                [{'config': {'n': n, 'name': str(n) + config_ext},
                'impl': {'taskName': task_name,
                'implName': impl_name,
                'implRM': impl_rm}, 'problem_size': volume}],
                profile=profile)

task_name = input("task name: ")
params = json.loads(input("params: "))
allowed_vols = [int(x) for x in input("Volumes: ").split()]
device = input("Worker type (dfe/cpu): ")
N = int(input("Worker config (1-8 for dfe, 1-12 for cpu): "))
rm_id = input("Worker number: (starts at 0) ")

impl_rm = "hnode0."+device+rm_id
impl_name = device+"_compute"

print(impl_rm)
for volume in allowed_vols:

	print(volume)
	vol_param = [p for p in params if p["param"] == "volume"]
	if len(vol_param) > 0:
		vol_param = vol_param[0]
		vol_param["value"] = volume 

	# execute REPEATS times and collect profiles
	orian_execute(task_name, params, volume, N, device.upper(), impl_name, impl_rm, profile=True)
