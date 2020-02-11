import json, sys, time, uuid
import swagger_server.resource_manager as rm 
import numpy as np
from scipy import optimize

class DFEResourceManager(rm.ResourceManager):

	def __init__(self, cfg_file):
		super(DFEResourceManager, self).__init__(cfg_file)
		# set up functions to build and store performance models for local implementations 
		self.build_functions = {}
		self.build_functions['adp'] = self.build_adp_model
		self.build_functions['nbody'] = self.build_nbody_model
		self.build_functions['align'] = self.build_align_model

	def _get_tasks(self):
		url = self.db_url + "/tasks?rm_id=" + self.rm_id
		tasks = rm.http_get(url)
		return tasks

	def _get_impls(self):
		url = self.db_url + "/impls?rm_id=" + self.rm_id
		impls = rm.http_get(url)
		impls_metadata = [{'impl_name': i['impl_name'], 'task_name': i['task_name'], 'impl_rm': i['impl_rm']} for i in impls]
		return impls_metadata

	def _get_models(self):
		url = self.db_url + "/models?rm_id=" + self.rm_id
		impls = rm.http_get(url)
		return impls

	def write_result_to_file(self, result):
		with open('result', 'w') as f:
			f.write('\n'.join(str(r) for r in result))

	def _execute_task(self, task_name, input_params, config, impl, problem_size, profile=False):

		print("Executing", task_name,  problem_size);
		# find full impl in db to get runtime instructions
		url = self.db_url + "/impls?rm_id=" + self.rm_id + "&task_name=" + task_name + "&impl_name=" + impl['impl_name'] + "&impl_rm=" + impl['impl_rm']
		impls = rm.http_get(url)
		full_impl = impls[0]
		
		# import library using path specified in impl
		path =  full_impl['path']
		print(path)
		sys.path.insert(0, path)
		task_lib = __import__(task_name)

		# get compute, construct, and destruct functions from imported libraries
		func_to_call = getattr(task_lib, impl['impl_name'])
		construct_func = getattr(task_lib, impl['impl_name'] + "_construct")
		destruct_func = getattr(task_lib, impl['impl_name'] + "_destruct")

		# invoke functions 		
		func_time, io_time = self.invoke_function(func_to_call, construct_func, destruct_func,
						input_params, config, json.loads(full_impl['runtime']), profile)

		if profile:
			self.create_profile(task_name, config, full_impl, problem_size, func_time, io_time)

		return {'result': []}

	def get_values_from_file(self, fname, n):
		with open(fname, 'r') as f:
			return [float(next(f)) for x in range(n)]

	def invoke_function(self, func, construct_func, destruct_func, input_params, config, runtime_instr, profile):

		# use runtime instructions to prepare arguments for construct
		construct_args = []
		for i in runtime_instr["construct"]:
			if 'config' in i:
				key = i['config']
				construct_args.append(config[key])
			elif 'param' in i:
				param = i['param']
				in_param_obj = [o for o in input_params if o['param'] == param][0]
				construct_args.append(in_param_obj['value'])

		io_time = 0
		func_time = 0

		if profile:
			start_construct = time.time()

		# call construct func
		context = construct_func(*construct_args)

		if profile:
			end_construct = time.time()
			start_func = time.time()

		# call func
		func(context)

		if profile:
			end_func = time.time()

		# use runtime instructions to prepare arguments for destruct
		destruct_args = [context]
		for i in runtime_instr["destruct"]:
			if 'config' in i:
				key = i['config']
				destruct_args.append(config[key])
			elif 'param' in i:
				param = i['param']
				in_param_obj = [o for o in input_params if o['param'] == param][0]
				destruct_args.append(in_param_obj['value'])

		if profile:
			start_destruct = time.time()

		# call destruct func
		destruct_func(*destruct_args)

		if profile:
			end_destruct = time.time()
			construct_time = end_construct - start_construct
			destruct_time = end_destruct - start_destruct
			io_time = construct_time + destruct_time
			func_time += end_func - start_func

		return func_time, io_time

	def create_profile(self, task_name, config, impl, problem_size, time_taken, io_time):
		profile = {}
		profile['rm_id'] = self.rm_id
		profile['task_name'] = task_name
		profile['impl_name'] = impl['impl_name']
		profile['config'] = config['name']
		profile['problem_size'] = problem_size
		profile['time'] = time_taken
		profile['io_time'] = io_time
		profile['profile_id'] = str(uuid.uuid4())
		self.store_profile(profile)

	def store_profile(self,profile):
		url = self.db_url + "/profiles"
		rm.http_post(url, data=profile)

	def _get_local_impl(self, impl_meta):
		url = self.db_url + "/impls?rm_id=" + impl_meta['implRM'] + "&task_name=" + impl_meta['taskName'] + "&impl_name=" + impl_meta['implName']
		return rm.http_get(url)[0]

	def _select_execute_target(self, config, impl):
		if impl['impl_rm'] == self.rm_id:
			return {'rm_id': self.rm_id}
		return [c for c in self.children if c['rm_id'] == impl['impl_rm']][0]

	def _build_model(self, task_name, impl_name):
		try:
			build_func = self.build_functions[task_name]
			build_func(impl_name) 
		except:
			print("No function to build a model for", task_name)

# below functions are all to build perfrmance models for the tasks and implemented supported by this node

	def get_data_points(self, task):
		 all_profiles = rm.http_get(self.db_url + "/profiles?task_name=" + task)
		 profiles = [p for p in all_profiles if 'DFE' in p['config']]
		 tp_data_points = []
		 io_data_points = []
		 ns = []
		 vols = []
		 for profile in profiles:
			 vol = int(profile['problem_size'])
			 n = int(profile['config'][:-3])
			 tp = float(profile['problem_size'])/float(profile['time'])/1000
			 io_time = float(profile['io_time'])
			 tp_data_points.append({'vol': vol, 'n': n, 'val': tp})
			 io_data_points.append({'vol': vol, 'n': n, 'val': io_time})
			 ns.append(n)
			 vols.append(vol)
		 ns = list(set(ns))
		 ns.sort()
		 vols = list(set(vols))
		 vols.sort()
		 return tp_data_points, io_data_points, ns, vols

	def format_and_average(self, data_points, ns, vols):
		averages = {}
		data = {}
		for n in ns:
			for vol in vols:
				vals = [dp['val'] for dp in data_points if dp['n'] == n and dp['vol'] == vol]
				if len(vals) > 0:
					ave_val = np.mean(vals)
					std_val = np.std(vals)
					if not n in averages:
						averages[n] = {}
					averages[n][vol] = {'ave': ave_val, 'std': std_val}
					if not n in data:
						data[n] = {}
					data[n][vol] = vals
		return data, averages

	def clean_data(self, data, averages, ns, vols):
		for n in ns:
			for vol in vols:
				if n in data and vol in data[n]:
					vals = data[n][vol]
					ave_val = averages[n][vol]['ave']
					std_val = averages[n][vol]['std']
					if std_val > 0.05*ave_val:
						for v in vals:
							if abs(v-ave_val) > std_val:
								vals.remove(v)
						if len(vals) < 2:
							del data[n][vol]
							del averages[n][vol]
						else:
							new_ave = np.mean(vals)
							new_std = np.std(vals)
							if new_std > 0.05*new_ave:
								del data[n][vol]
								del averages[n][vol]
							else:
								averages[n][vol]['ave'] = new_ave
								averages[n][vol]['std'] = new_std

	def construct_model_obj(self, task, impl_name, config, min_size, max_size, coefs, type):
		model = {}
		model['rm_id'] = self.rm_id
		model['task_name'] = task
		model['impl_name'] = impl_name
		model['config'] = config
		model['min_size'] = min_size
		model['max_size'] = max_size
		model['coefs'] = coefs
		model['type'] = type
		return model

	def get_data_to_fit(self, data, averages, ns, vols, max_vals={}):
		vals_to_fit = {}
		vols_to_fit = {}
		for n in ns:
			vols_to_fit_n, vals_to_fit_n = [], []
			prev = False
			for vol in vols:
				if vol in data[n]:
					if n in max_vals and averages[n][vol]['ave'] >= max_vals[n]:
						if prev == True:
							vals_to_fit_n += data[n][vol]
							vols_to_fit_n += [vol] * len(data[n][vol])
							break
						prev = True
					vals_to_fit_n += data[n][vol]
					vols_to_fit_n += [vol] * len(data[n][vol])
			vols_to_fit[n] = np.array(vols_to_fit_n)
			vals_to_fit[n] = np.array(vals_to_fit_n)
		return vols_to_fit, vals_to_fit


	def build_nbody_model(self, impl_name):
		tp_data, io_data, ns, vols = self.get_data_points("nbody")
		tp_models = self.build_decexp_model(tp_data, ns, vols)
		io_models = self.build_linear_model(io_data, ns, vols)
		for n in tp_models:
			for m in tp_models[n]:
				config = str(n) + 'DFE'
				model = self.construct_model_obj("nbody", impl_name, config,
					m['min_size'], m['max_size'], list(m['coefs']), 'tp')
				print(model)
				rm.http_post(self.db_url + "/models", data=model)     

		for n in io_models:
			for m in io_models[n]:
				config = str(n) + 'DFE'
				model = self.construct_model_obj("nbody", impl_name, config,
					m['min_size'], m['max_size'], list(m['coefs']), 'io')
				print(model)
				rm.http_post(self.db_url + "/models", data=model)

	def build_adp_model(self, impl_name):
		tp_data, io_data, ns, vols = self.get_data_points("adp")
		tp_models = self.build_satlog_model(tp_data, ns, vols)
		io_models = self.build_linear_model(io_data, ns, vols)
		for n in tp_models:
			for m in tp_models[n]:
				config = str(n) + 'DFE'

				model = self.construct_model_obj("adp", impl_name, config,
					m['min_size'], m['max_size'], list(m['coefs']), 'tp')
				print(model)
				rm.http_post(self.db_url + "/models", data=model)     
		for n in io_models:
			for m in io_models[n]:
				config = str(n) + 'DFE'
				model = self.construct_model_obj("adp", impl_name, config,
					m['min_size'], m['max_size'], list(m['coefs']), 'io')
				print(model)
				rm.http_post(self.db_url + "/models", data=model)


	def build_align_model(self, impl_name):
		tp_data, io_data, ns, vols = self.get_data_points("align")
		tp_models = self.build_satlog_model(tp_data, ns, vols)
		io_models = self.build_linear_model(io_data, ns, vols)
		for n in tp_models:
			for m in tp_models[n]:
				config = str(n) + 'DFE'
				model = self.construct_model_obj("align", impl_name, config,
					m['min_size'], m['max_size'], list(m['coefs']), 'tp')
				print(model)
				rm.http_post(self.db_url + "/models", data=model)     
		for n in io_models:
			for m in io_models[n]:
				config = str(n) + 'DFE'
				model = self.construct_model_obj("align", impl_name, config,
					m['min_size'], m['max_size'], list(m['coefs']), 'io')
				print(model)
				rm.http_post(self.db_url + "/models", data=model)

	def build_decexp_model(self, data_points, ns, vols):
		# calc averages and format raw data, remove outliers
		data, averages = self.format_and_average(data_points, ns, vols)
		self.clean_data(data, averages, ns, vols)
		# build decaying exponential models
		all_vols_to_fit, all_vals_to_fit = self.get_data_to_fit(data, averages, ns, vols)
		models = {}
		for n in ns:
			vols_to_fit, vals_to_fit = all_vols_to_fit[n], all_vals_to_fit[n]
			fitfunc = lambda p, size: p[0] + p[1]*size + p[2]*size**2 + p[3]*size**3 + p[4]*size**4
			errfunc = lambda p, size, val: fitfunc(p, size) - val
			p0 = [1., -1., 1., 1., 1.]
			p1, success = optimize.leastsq(errfunc, p0[:], args=(vols_to_fit, np.log(vals_to_fit),))
			size = vols_to_fit[-1]
			last_val = np.exp(p1[0] + p1[1]*size + p1[2]*size**2 + p1[3]*size**3 + p1[4]*size**4)
			if not n in models:
				models[n] = []
			models[n].append({'coefs': p1, 'min_size': 0, 'max_size': int(vols_to_fit[-1])})
			models[n].append({'coefs': [last_val], 'min_size': int(vols_to_fit[-1])+1, 'max_size': sys.maxsize})
		return models # coefs for each n with min_size and max_size	

	def build_satlog_model(self, data_points, ns, vols):
		# calc averages and format raw data, remove outliers
		data, averages = self.format_and_average(data_points, ns, vols)
		self.clean_data(data, averages, ns, vols)
		# find saturation values for each n
		sat_vals = {}
		for n in ns:
			to_average = []
			prev_average, average, delta = 0, 0, 0
			for i in range(1, len(vols)+1):
				vol = vols[-i]
				if n in averages and vol in averages[n]:
					if len(to_average) > 1 and abs(averages[n][vol]['ave'] - prev_average) > prev_average*0.025:
						sat_vals[n] = prev_average	
						break
					to_average.append(averages[n][vol]['ave'])
					average = np.mean(to_average)
					delta = average - prev_average
					prev_average = average
		all_vols_to_fit, all_vals_to_fit = self.get_data_to_fit(data, averages, ns, vols, sat_vals)
		models = {}
		# build saturating log models
		for n in ns:
			vols_to_fit, vals_to_fit = all_vols_to_fit[n], all_vals_to_fit[n]
			fitfunc = lambda p, size: p[0] * np.log(abs(p[1] * size)) + p[2]
			errfunc = lambda p, size, val: fitfunc(p, size) - val
			p0 = [1., 1., 1.]
			p1, success = optimize.leastsq(errfunc, p0[:], args=(vols_to_fit, vals_to_fit,))
			# find saturation volume
			x = np.arange(0.1, vols_to_fit[-1], vols_to_fit[-1]/10000)
			y = [ p1[0]* np.log(abs(p1[1] * x_)) + p1[2] for x_ in x ]
			y_ = [ yy for yy in y if yy <= sat_vals[n]]
			x_ = x[:len(y_)]
			if not n in models:
				models[n] = []
			models[n].append({'coefs': p1, 'min_size': 0, 'max_size': x_[-1]})
			models[n].append({'coefs': [sat_vals[n]], 'min_size': x_[-1]+1, 'max_size':sys.maxsize})
		return models # coefs for each n with min_size and max_size

	def build_linear_model(self, data_points, ns, vols):
		# calc averages and format raw data, remove outliers
		data, averages = self.format_and_average(data_points, ns, vols)
		self.clean_data(data, averages, ns, vols)
		all_vols_to_fit, all_vals_to_fit = self.get_data_to_fit(data, averages, ns, vols)
		# build linear models 
		models = {}
		for n in ns:
			vols_to_fit, vals_to_fit = all_vols_to_fit[n], all_vals_to_fit[n]
			fitfunc = lambda p, size: p[0] * size + p[1]
			errfunc = lambda p, size, val: fitfunc(p, size) - val
			p0 = [1., 1.]
			p1, success = optimize.leastsq(errfunc, p0[:], args=(vols_to_fit, vals_to_fit,))
			if not n in models:
				models[n] = []
			models[n].append({'coefs': p1, 'min_size': 0, 'max_size': sys.maxsize})
		return models # coefs for each n with min_size and max_size




