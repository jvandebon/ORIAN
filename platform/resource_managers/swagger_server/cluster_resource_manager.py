import json, sys
import swagger_server.resource_manager as rm 
import numpy as np

DEMO=False
AUTOSCALING = True

# change params for different scenarios and the target system
max_resource_group = {'DFE8': ['cluster0.hnode1.dfe0'], 
			'CPU': ['cluster0.hnode0.cpu0', 'cluster0.hnode1.cpu0'], 
			'DFE4': ['cluster0.hnode0.dfe0']} # max group
start_resource_group = ['cluster0.hnode0.cpu0']
max_resource_list = []
for type in max_resource_group:
	for resource in max_resource_group[type]:
		max_resource_list.append(resource)

if AUTOSCALING: # (change params for different scenarios)
	global_job_count = 0
	autoscaling_inc = 5
	scores = {}
	max_group_size = 0
	for type in max_resource_group:
		scores[type] = 0
		max_group_size += len(max_resource_group[type])
	current_resource_group = start_resource_group
	increase_threshold = 1.0/max_group_size
	decrease_threshold = 1.0/max_group_size
else:
	current_resource_group = max_resource_list

class ClusterResourceManager(rm.ResourceManager):

	def add_new_task(self, task):
		print("Adding new task:", task)
		task['rm_id'] = self.rm_id
		rm.http_post(self.db_url + "/tasks", data=task)

	def update_task(self, task):
		print("Updating task:", task)
		rm.http_put(self.db_url + "/tasks", data=task)

	def _get_tasks(self):
		url = self.db_url + "/tasks?rm_id=" + self.rm_id
		tasks = rm.http_get(url)
		return tasks

	def _update_tasks(self, tasks):
		# task : (rm_id text, name text, input_params text)
		for task in tasks:
			# check if task already in local db
			url = self.db_url + "/tasks?rm_id=" + self.rm_id + "&name=" + task['task_name']
			exists = rm.http_get(url)
			if len(exists) == 0:
				# if not already in db, add
				self.add_new_task(task)
			else:
				# check if need to update impl id list or resource types 
				existing_task = exists[0]
				need_to_update = False
				# check if input params have changed
				if existing_task['input_params'] != task['input_params']:
					need_to_update = True

				if need_to_update:
					self.update_task(task)

	def _get_impls(self):
		url = self.db_url + "/impls?rm_id=" + self.rm_id
		impls = rm.http_get(url)
		impls_metadata = [{'impl_name': i['impl_name'], 'task_name': i['task_name'], 'impl_rm': i['impl_rm']} for i in impls]
		return impls_metadata

	def add_new_impl(self, impl):
		print("Adding new impl:", impl)
		impl['rm_id'] = self.rm_id
		rm.http_post(self.db_url + "/impls", data=impl)

	def update_impl(self, impl):
		irint("Updating impl:", impl)
		rm.http_put(self.db_url + "/impls", data=impl)

	def _update_impls(self, impls):
		for impl in impls:
			# check if impl_id already in local db
			url = self.db_url + "/impls?rm_id=" + self.rm_id + "&impl_name=" + impl['impl_name'] + "&impl_rm=" + impl['impl_rm'] 
			exists = rm.http_get(url)
			# if not, add
			if len(exists) == 0:
				self.add_new_impl(impl)

	def add_new_model(self, model):
		print("Adding new model:", model)
		rm.http_post(self.db_url + "/models", data=model)

	def _update_models(self, models):
		for model in models:
			url = self.db_url + "/models?rm_id=" + model['rm_id'] + "&impl_name=" + model['impl_name'] + "&task_name=" + model['task_name'] + "&config=" + model['config']
			existing_models = rm.http_get(url)
			exists = []
			for existing_model in existing_models:
				if existing_model['min_size'] == model['min_size'] and existing_model['max_size'] == model['max_size']:
					exists.append(model)
					break
			if len(exists) == 0:
				self.add_new_model(model)

	def _get_local_impl(self, impl_meta):
		url = self.db_url + "/impls?rm_id=" + impl_meta['implRM'] + "&task_name=" + impl_meta['taskName'] + "&impl_name=" + impl_meta['implName']
		return rm.http_get(url)[0] 

	def _select_execute_target(self, config, impl):
		if impl['impl_rm'] == self.rm_id:
			return {'rm_id': self.rm_id}
		
		return [c for c in self.children if c['rm_id'] in impl['impl_rm']][0]

	def get_task_models(self, task_name, problem_size, available_rms):
		url = self.db_url + "/models?task_name=" + task_name
		all_models = rm.http_get(url)
		models = [m for m in all_models if m['min_size'] <= problem_size and m['max_size'] > problem_size and m['rm_id'] in available_rms]
		return models

	def filter_models_based_on_time(self, models, times, time_obj, problem_size):
		models_ = []
		times_ = []
		if 'max' in time_obj:
			max_time = time_obj['max']
		else:
			max_time = sys.maxsize
		for i in range(len(times)):
			if times[i]*1.1 <= max_time: # 10% buffering, can adjust
				times_.append(times[i])
				models_.append(models[i])
		if len(models_) == 0:
			min_time = min(times)
			times_.append(min_time)
			models_.append(models[times.index(min_time)])
		return times_, models_

	def filter_models_based_on_objectives(self, models, times, objectives, problem_size):
		models_ = models
		times_ = times
		if 'time' in objectives:
			times_, models_ = self.filter_models_based_on_time(models, times, objectives['time'], problem_size)
		return times_, models_

	def calculate_time_for_models(self, models, problem_size):
		tp_models = [m for m in models if m['type'] == "tp"]	
		times = []
		for m in tp_models:
			c = m['coefs']
			if m['task_name'] == 'adp' or m['task_name'] == 'align':
				if m['min_size'] == 0:
					tp = c[0] * np.log(abs(c[1]*problem_size)) + c[2]
				else:
					tp = c[0]
			else: # TASK = NBODY
				if len(c) > 1:
					x_ = problem_size
					tp = np.exp(c[0] + c[1]*x_ + c[2]*x_**2 + c[3]*x_**3 + c[4]*x_**4)
				else:
					tp = c[0]
			compute_time = problem_size / (tp * 1000)
			time = compute_time
			if time < 0:
				time = sys.maxsize
			times.append(time)
		return times, tp_models

	def config_cost(self, config):
		cost = 0
		if 'T' in config:
			cost += int(config[:-1])
		elif 'DFE' in config:
			cost += 3 * int(config[:-3])
		return cost

	def pick_model(self, times, models, objectives):
		if objectives != {}:
			# pick cheapest model
			best_i = -1
			min_cost = sys.maxsize
			for i in range(len(models)):
				cost = self.config_cost(models[i]['config'])*times[i]
				if cost < min_cost:
					min_cost = cost
					best_i = i
			model = models[best_i]
		else:
			# pick model with minimum time
			min_time = min(times)
			model = models[times.index(min_time)]
		return model

	def select_model(self, models, objectives, problem_size):
		# calculate expected time for problem size w/ each config
		times, tp_models = self.calculate_time_for_models(models, problem_size)
		# filter out models that don't meet objectives
		times_, tp_models_ = self.filter_models_based_on_objectives(tp_models, times, objectives, problem_size)
		# pick config with minimum time
		model = self.pick_model(times_, tp_models_, objectives)
		return model

	def _optimal_config(self, task_name, objectives, problem_size):

		global global_job_count
		global current_resource_group
		global scores

		if AUTOSCALING:
			# every n jobs, adjust group  (change current resource group list)
			if global_job_count > 0 and (global_job_count%autoscaling_inc) == 0:
				print("(AS) AUTOSCALING EVENT")
				for type in scores:
					percentage = scores[type]/(1.0*autoscaling_inc)
					if percentage > increase_threshold: # and resource not in current_resource_group:
						for resource in max_resource_group[type]:
							if resource not in current_resource_group:
								print("(AS) Adding to group:", resource)
								current_resource_group.append(resource)
								break
					elif percentage < decrease_threshold and len(current_resource_group) > 1:  #and resource in current_resource_group
						for resource in max_resource_group[type]:
							if resource in current_resource_group:
								print("(AS) Removing from group:", resource)
								current_resource_group.remove(resource)
								break
					scores[type] = 0

			## autoscaler selects model assuming max resource group
			all_models = self.get_task_models(task_name, problem_size, max_resource_list)
			best_model = self.select_model(all_models, objectives, problem_size)
			print("(AS) BEST MODEL: ", best_model['config'])
			# assign score to selected config
			for type in max_resource_group:
				if best_model['rm_id'] in max_resource_group[type]:
					scores[type] += 1
	
			global_job_count += 1

			## load balancer selects model with current resource group
			resources_available = False
			while not resources_available:
				# check for available resources
				available = self.check_availability()
				available_rms = [rm['rm_id'] for rm in available if rm['available'] == True and rm['rm_id'] in current_resource_group]
				print("(LB) AVAILABLE: ", available_rms)
				if len(available_rms) > 0:
					# find all models with task_name = task_name and limits including problem_size
					models = self.get_task_models(task_name, problem_size, available_rms)
					if len(models) > 0:
						resources_available = True

			# select best based on objectives (if autoscaling, no objectives)
			if AUTOSCALING:
				objectives = {}
			model = self.select_model(models, objectives, problem_size)
			print("(LB) SELECTED MODEL:", model['config'])

			# get impl and config from model
			impl = {}
			impl['taskName'] = task_name
			impl['implName'] = model['impl_name']
			impl['implRM'] = model['rm_id']
			config = {}
			config['name'] = model['config']
			if 'T' in config['name']:
				config['n'] = int(model['config'][:-1])
			elif 'DFE' in config['name']:
				config['n'] = int(model['config'][:-3])

			return [{'impl': impl, 'config': config, 'problem_size': problem_size}]