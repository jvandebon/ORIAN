import flask, requests, json, zlib, time

# TODO: better way to store this 
rm_url = ""

def configure(_rm_url="127.0.0.1:8081"):
	# connect to top level RM 
	global rm_url
	try:
		request = requests.get(_rm_url + "/tasks")
		if request.status_code != 200:
			return False
	except:
		return False
	rm_url = _rm_url
	return True

def get_tasks():
	res = requests.get(rm_url + "/tasks")
	tasks = json.loads(res.text)
	return_tasks = [{'task_name': t['task_name'],'input_params': t['input_params']} for t in tasks]
	return return_tasks

def get_impls():
	res = requests.get(rm_url + "/impls")
	impls = json.loads(res.text)
	return_impls = [{'task_name': i['task_name'], 'impl_name': i['impl_name'], 'impl_rm': i['impl_rm']} for i in impls]
	return return_impls

def execute(task_name, input_params, problem_size, config=[], objectives={}, profile=False):
	if len(config) == 0: 
		# determine optimal configuration, maybe based on objectives
		print("determining configuration...")
		url = rm_url + "/tasks/config"
		data = {}
		data['taskName'] = task_name
		data['problemSize'] = problem_size
		data['objectives'] = objectives
		result = requests.get(url, json=data)
		config = json.loads(result.text)
		print(config)
	data = {}
	data['taskName'] = task_name
	data['inputParams'] = input_params
	data['config'] = config
	data['problemSize'] = problem_size
	data['profile'] = profile
	data['sync'] = False
	url = rm_url + "/tasks/execute"
	requests.post(url, json=data)
	

def execute_sync(task_name, input_params, problem_size, config=[], objectives={}, profile=False):

	if len(config) == 0: 
		url = rm_url + "/tasks/config"
		data = {}
		data['taskName'] = task_name
		data['problemSize'] = problem_size
		data['objectives'] = objectives
		result = requests.get(url, json=data)
		config = json.loads(result.text)
		for c in config:
			print(c['problem_size'], c['impl']['implRM'], c['config']['name'])
	data = {}
	data['taskName'] = task_name
	data['inputParams'] = input_params
	data['config'] = config
	data['problemSize'] = problem_size
	data['profile'] = profile
	data['sync'] = True
	url = rm_url + "/tasks/execute"
