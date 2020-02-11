import json, sys
import swagger_server.resource_manager as rm 
import numpy as np
import time

AUTOSCALING = True

if AUTOSCALING: # (change params for different scenarios)
	## USER PARAMS 
	max_cpus = 3
	max_dfes = 2
	min_cpus = 1
	min_dfes = 0
	inc_t = 0.5
	dec_t = 0.3
	as_window = 5
	## AUTOSCALER SETUP
	worker_types = ['1T', '1DFE']
	worker_pool = {'1T': ['hnode0.cpu1_0', 'hnode0.cpu1_1', 'hnode0.cpu1_2'], '1DFE': ['hnode0.dfe1_0', 'hnode0.dfe1_1']}
	start_group = ['1T', '1DFE']
	used_cpus = 1
	used_dfes = 1
	current_group = ['1DFE', '1T']
	current_workers = ['hnode0.cpu1_0', 'hnode0.dfe1_0']
	scores = {}
	for w in worker_types:
		scores[w] = 0
	job_count = 0 
else:
	current_group = None

class HNodeResourceManager(rm.ResourceManager):

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

	def _get_models(self):
		url = self.db_url + "/models?rm_id=" + self.rm_id
		models = rm.http_get(url)
		return models

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
		models = [m for m in all_models if m['min_size'] <= problem_size and m['max_size'] > problem_size and m['rm_id'] in available_rms and m['type'] == 'tp']
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
				if len(c) > 1:
					tp = c[0] * np.log(abs(c[1]*problem_size)) + c[2]
				else:
					tp = c[0]
			else: # TASK = NBODY
				if len(c) > 1:
					x_ = problem_size
					tp = np.exp(c[0] + c[1]*x_ + c[2]*x_**2 + c[3]*x_**3 + c[4]*x_**4)
				else:
					tp = c[0]
			if tp == 0:
				tp = -1
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
				print(models[i]['config'], times[i])
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

	def cpu_type(self, config):
		return 'T' in config

	def dfe_type(self, config):
		return 'DFE' in config

	def n_cpus_dfes(self, config):
		if self.cpu_type(config):
			return  int(config[:-1])
		elif self.dfe_type(config):
			return int(config[:-3])
	
	def _optimal_config(self, task_name, objectives, problem_size):
		global job_count
		global scores
		global current_group
		global current_workers
		global used_cpus
		global used_dfes
		if AUTOSCALING:
			if job_count == 0:
				print("(AS) START TIME:", time.time())
				print("(AS) CURRENT GROUP:", current_group)
			# every n jobs, adjust group  (change current resource group list)
			elif (job_count % as_window) == 0:
				print("\n(AS) AUTOSCALING EVENT", time.time())
				available = self.check_availability()
				available_rms = [rm['rm_id'] for rm in available if rm['available'] == True]
				start = time.time()
				for worker in scores:
					# make sure worker not busy 
					percentage = scores[worker]/(1.0*as_window)
					if percentage < dec_t and worker in current_group and current_workers[current_group.index(worker)] in available_rms:
				#		print("(AS) Removing from group:", worker)
						del current_workers[current_group.index(worker)]
						current_group.remove(worker)
						if self.cpu_type(worker):
							n_cpus = self.n_cpus_dfes(worker)
							used_cpus -= n_cpus
						elif self.dfe_type(worker):
							n_dfes = self.n_cpus_dfes(worker)
							used_dfes -= n_dfes
				for worker in scores:
					percentage = scores[worker]/(1.0*as_window)
					if percentage > inc_t:
						if self.cpu_type(worker):
							n_cpus = self.n_cpus_dfes(worker)
							if used_cpus + n_cpus > max_cpus:
								scores[worker] =  0
								continue # cant introduce
							used_cpus += n_cpus
						elif self.dfe_type(worker):
							n_dfes = self.n_cpus_dfes(worker)
							if used_dfes + n_dfes > max_dfes:
								scores[worker] = 0
								continue
							used_dfes += n_dfes
						for id in worker_pool[worker]:
							if id not in current_workers:
								print("(AS) Adding to group:", worker)
								current_group.append(worker)
								current_workers.append(id)
								break
					scores[worker] = 0
				if used_cpus < min_cpus:
					for worker in worker_types:
						if self.cpu_type(worker):
				#			print("(AS) Adding", worker, "to meet minimum")
							current_group.append(worker)
							for id in worker_pool[worker]:
								if id not in current_workers:
									current_workers.append(id)
									break
							used_cpus += self.n_cpus_dfes(worker)
							break			
	
				if used_dfes < min_dfes:
					for worker in worker_types:
						if self.dfe_type(worker):
				#			print("(AS) Adding", worker, "to meet minimum")
							current_group.append(worker)
							for id in worker_pool[worker]:
								if id not in current_workers:
									current_workers.append(id)
									break
							used_dfes += self.n_cpus_dfes(worker)
							break
				end = time.time()
				print("(AS) CURRENT GROUP:", current_group, "\n")
				print("(AS) Event Time:", end-start)
			## autoscaler selects model assuming max resource group
			all_workers = [c['rm_id'] for c in self.children]
			print("(AS) ALL WORKERS:", all_workers)
			all_models = self.get_task_models(task_name, problem_size, all_workers)
			models = [m for m in all_models if m['config'] in worker_types]
			best_model = self.select_model(models, objectives, problem_size)
			print("(AS) BEST MODEL: ", best_model['config'])
			# assign score to selected config
			scores[best_model['config']] += 1
			job_count += 1

		## load balancer selects model with current resource group 
		# need a list of current resource group
		resources_available = False
		while not resources_available:
			# check for available resources
			available = self.check_availability()
			available_rms = [rm['rm_id'] for rm in available if rm['available'] == True]
			if not AUTOSCALING:
				print("(LB) AVAILABLE: ", available_rms)
			else:
				av = [w for w in available_rms if w in current_workers]
				if len(av) > 0:
					print("(LB) CURRENT WORKERS: ", current_workers)
					print("(LB) AVAILABLE:", av)
			if len(available_rms) > 0:
				# find models with task_name and limits including problem_size
				models = self.get_task_models(task_name, problem_size, available_rms)
				if current_group != None:
					models = [m for m in models if m['rm_id'] in current_workers]
				if len(models) > 0:
					resources_available = True
			
		# select best based on objectives (if autoscaling, no objectives)
		if AUTOSCALING:
			objectives = {}
		model = self.select_model(models, objectives, problem_size)
		print("(LB) SELECTED MODEL:", model['config'], model['rm_id'])

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
