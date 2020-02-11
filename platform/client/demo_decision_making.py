import orian, time


adp_params = [{"param":"volume", "value": 0}, {"param":"prior_m", "value": "../resource_managers/swagger_server/prior_m"}, {"param":"prior_v", "value": "../resource_managers/swagger_server/prior_v"}, {"param":"y", "value": "../resource_managers/swagger_server/y"}, {"param": "post_m", "value": "../resource_managers/swagger_server/post_m_"}, {"param": "post_s", "value": "../resource_managers/swagger_server/post_s_"}]

align_params = [{"param":"volume", "value": 0}, {"param":"file", "value": "../../apps/exact_align/data/hg38"}]

tasks = ['adp', 'align']
vols = [500, 5000, 50000, 500000, 5000000, 50000000]

for task_name in tasks:

	for problem_size in vols:

		if task_name == 'adp':
			params = adp_params
			name = 'AdPredictor'

		elif task_name == 'align':
			params = align_params
			name = 'Exact Align'

		params[0]["value"] = problem_size

		print("\n\nTask:", name, ", Problem Size:", problem_size, "\n")

		configured = orian.configure("http://cccad2.doc.ic.ac.uk:8087/jvandebon/rm_prototype/2.0")
		print("********** Cluster Scheduling Decision **********")
		orian.execute_sync(task_name, params, problem_size)
		time.sleep(0.5)
		configured = orian.configure("http://cccad2.doc.ic.ac.uk:8084/jvandebon/rm_prototype/2.0")
		print("\n********** Heterogeneous Node Scheduling Decision **********")
		orian.execute_sync(task_name, params, problem_size)
		if task_name =='adp':
			time.sleep(4.5)
		else:
			time.sleep(1.5)

