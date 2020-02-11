import requests, json, _thread, time

def http_get(url, data={}):
	result = requests.get(url, json=data)
	return json.loads(result.text)

def http_put(url, data={}):
	result = requests.put(url, json=data)
	return json.loads(result.text)

def http_post(url, data={}):
	result = requests.post(url, json=data)
	return json.loads(result.text)

class ResourceManager:

	def __init__(self, cfg_file):

		# open config file, parse and assign variables
		cfg = self.parse_cfg_file(cfg_file)
		self.name = cfg['name']
		self.url = cfg['url']
		if cfg['parentUrl'] == "":
			self.parent_url = None
		else:
			self.parent_url = cfg['parentUrl']
		self.db_url = cfg['dbUrl']
		self.rm_type = cfg['rmType']
		self.children_count = {}
		self.children = []
		self.rm_id = ""
		self.available = True
		# register with parent and get rm_id
		if self.parent_url is None:
			self.rm_id = self.rm_type + "0"
		else:
			self.rm_id = self.register_with_parent(self.parent_url)
		print("Registered RM as: ", self.rm_id)

	def parse_cfg_file(self, cfg_file):
		with open(cfg_file, 'r') as cfg:
			cfg = json.loads(cfg.read())
		if not 'name' in cfg or not 'url' in cfg or not 'parentUrl'  in cfg or not 'dbUrl'  in cfg or not 'rmType'  in cfg:
			print("Configuration file must contain the following fields: name, url, parentUrl, dbUrl, rmType")
			print(cfg)
			exit()
		return cfg

	def register_with_parent(self, parent_url):
		register_json = http_put(parent_url + "/managers/register", {'url': self.url, 'rmType': self.rm_type})
		return register_json['rm_id']

	def check_availability(self):
		available = []
		if len(self.children) == 0:
			available.append({"rm_id": self.rm_id, "available": self.available})
		else:
			for c in self.children:
				try:
					if self.rm_type == 'cluster':
						to = 4
					else:
						to = 1
					child_avail = requests.get(c['url'] + "/managers/available", timeout=to)
					available += json.loads(child_avail.text)
				except:
					print(c['rm_id'], "timed out")
					available.append({"rm_id": c['rm_id'], "available": False})
		return available

	def _get_tasks(self):
		raise Exception("get tasks not implemented")

	def get_tasks(self):
		# return all tasks in DB 
		try:
			return self._get_tasks()
		except Exception as e:
			print("Exception caught: ", e)
			return e

	def _get_impls(self):
		raise Exception("get impls not implemented")

	def get_impls(self):
		# return metadata of all impls in DB 
		try:
			return self._get_impls()
		except Exception as e:
			print("Exception caught: ", e)
			return e

	def _get_models(self):
		raise Exception("get models not implemented")

	def get_models(self):
		try:
			return self._get_models()
		except Exception as e:
			print("Exception caught: ", e)
			return e

	def _update_tasks(self, tasks):
		raise Exception("update tasks not implemented")

	def update_tasks(self, tasks):
		# update local tasks database with new tasks
		try:
			self._update_tasks(tasks)
		except Exception as e:
			print("Exception caught: ", e)
			return e

	def _update_impls(self, impls):
		raise Exception("update impls not implemented")

	def update_impls(self, impls):
		# update local impls database with new impls
		try:
			self._update_impls(impls)
		except Exception as e:
			print("Exception caught: ", e)
			return e

	def _update_models(self, models):
		raise Exception("execute task not implemented")

	def update_models(self, models):
		try:
			self._update_models(models)
		except Exception as e:
			print("Exception caught: ", e)
			return e

	def generate_child_id(self, child_type):
		return self.rm_id + "." + child_type + str(self.children_count[child_type]-1)

	def add_new_child(self, child):
		# update children counter
		child_type = child['rm_type']
		if child_type in self.children_count:
			self.children_count[child_type] += 1
		else:
			self.children_count[child_type] = 1
		child_id = self.generate_child_id(child_type)
		# add to children list
		child['rm_id'] = child_id
		child['got_data'] = False
		self.children.append(child)
		return child_id

	def remove_child(self, child_url):
		# revert children counter
		child = [c for c in self.children if c['url'] == child_url][0]
		child_type = child['rm_type']
		self.children_count[child_type] -= 1
		# remove from children list
		idx = self.children.index(child)
		del self.children[idx]

	def register_child(self, child):
		# add to children list, update count, create ID
		child_id = self.add_new_child(child)
		_thread.start_new_thread(self._get_child_data, (child['url'],))
		return {'rm_id': child_id}

	def _get_child_data(self, child_url):
		time.sleep(1) # give child a chance to start running
		# try to connect 10 times until connection is established
		attempts = 0
		while attempts < 100:
			try:
				request = requests.get(child_url + "/tasks")
				break
			except:
				attempts += 1
				print('Attempt #' + str(attempts) + ", child not running.")
			time.sleep(5)
			
		if attempts == 100:
			print("Invalid child URL")
			self.remove_child(child_url)
			return
		# update local tasks based on child tasks
		print("Requesting data from " + child_url + "...")
		tasks = http_get(child_url + "/tasks")
		self.update_tasks(tasks)
		# update local impls based on child impls
		impls = http_get(child_url + "/impls")
		self.update_impls(impls)
		# update local models based on child models
		models = http_get(child_url + "/models")
		self.update_models(models)
		print('...done')
		child = [c for c in self.children if c['url']==child_url]
		child[0]['got_data'] = True

	def _execute_task(self, task_name, input_params, config, impl, problem_size, profile=False):
		raise Exception("execute task not implemented")

	def _select_execute_target(self, config, impl):
		raise Exception("select target not implemented")

	def _get_local_impl(self, impl_meta):
		raise Exception("get local impl not implemented")

	def execute_local(self, task_name, input_params, config, impl, problem_size, profile):
		try:
			self._execute_task(task_name, input_params, config, impl, problem_size, profile)
		except Exception as e:
			print("Exception caught: ", e)
			self.available = True
		self.available = True

	def execute(self, task_name, input_params, config, problem_size, sync, profile=False):
		for c in config:
			# select a RM for execution given a config and impl
			impl = self._get_local_impl(c['impl'])
			target = self._select_execute_target(c['config'], impl)
			# if this one is chosen, execute
			if target['rm_id'] == self.rm_id:
				## FOR PARTITIONING
				volume_param = [p for p in input_params if p['param'] == 'volume']
				if len(volume_param) != 0:
					volume_param[0]['value'] = c['problem_size']
				self.available = False
				if sync == True:
					self.execute_local(task_name, input_params, c['config'], impl, c['problem_size'], profile)
					self.available = True
				else:
					# start a new thread for execution 
					_thread.start_new_thread(self.execute_local, (task_name, input_params, c['config'], impl, c['problem_size'], profile,))
				return
				
			# forward to child 
			target_url = target['url']
	
			# forward execution to selected child
			data = {}
			data['taskName'] = task_name
			data['inputParams'] = input_params
			data['config'] = [c]
			data['problemSize'] = c['problem_size']
			data['profile'] = profile
			data['sync'] = sync
			#print("FORWARDING TO", target_url)
			requests.post(target_url + "/tasks/execute", json=data)

	def _get_models(self):
		raise Exception("get models not implemented")

	def get_models(self):
		try:
			return self._get_models()
		except Exception as e:
			print("Exception caught: ", e)
			return e
	
	def _build_model(self, task_name, impl_name):
		raise Exception("build model not implemented")

	def build_model(self, task_name, impl_name):
		return self._build_model(task_name, impl_name)

	def _optimal_config(self, task_name, objectives, problem_size):
		raise Exception("optimal config not implemented")

	def optimal_config(self, task_name, objectives, problem_size):
		return self._optimal_config(task_name, objectives, problem_size)