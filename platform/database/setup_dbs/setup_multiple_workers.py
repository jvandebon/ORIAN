import sqlite3, uuid, requests

def insert_task(rm_id, name, input_params, task_granularity):
	task = {}
	task['rm_id'] = rm_id
	task['task_name'] = name
	task['input_params'] = input_params
	task['task_granularity'] = task_granularity
	res = requests.post(db_url + "/tasks", json=task)
	print(res)

def insert_impl(rm_id, impl_name, task_name, path, runtime, impl_rm):
	impl = {}
	impl['rm_id'] = rm_id
	impl['impl_name'] = impl_name
	impl['task_name'] = task_name
	impl['path'] = path
	impl['runtime'] = runtime
	impl['impl_rm'] = impl_rm
	res = requests.post(db_url + "/impls", json=impl)
	print(res)	


db_url = "http://cccad2.doc.ic.ac.uk:8080"

num_dfes = 4
num_cpus = 6

insert_task("hnode0.dfe2_0", "adp", "[{\"param\": \"volume\", \"type\": \"integer\"}, {\"param\": \"prior_m\", \"type\": \"list\"}, {\"param\": \"prior_v\", \"type\": \"list\"}, {\"param\": \"y\", \"type\": \"list\"}, {\"param\": \"post_s\", \"type\": \"list\"}, {\"param\": \"post_m\", \"type\": \"list\"}]", 10000)


insert_impl("hnode0.dfe2_0", "dfe_compute", "adp", "../library/adp_maia",
                        "{\"construct\": [{\"param\":\"volume\"},{\"config\":\"n\"},"
                                                        + "{\"param\":\"prior_m\"},{\"param\":\"prior_v\"},"
                                                        + "{\"param\":\"y\"}],"
                        + "\"destruct\": [{\"param\":\"post_m\"}, {\"param\":\"post_s\"}]}",
                        "hnode0.dfe2_0")

insert_task("hnode0.dfe2_0", "align", "[{\"param\": \"volume\", \"type\": \"integer\"}, {\"param\": \"file\", \"type\": \"string\"}]", 0)

insert_impl("hnode0.dfe2_0", "dfe_compute", "align", "../library/align",
                        "{\"construct\": [{\"param\":\"volume\"},{\"config\":\"n\"},{\"param\":\"file\"}],"
                        + "\"destruct\": []}",
                        "hnode0.dfe2_0")

insert_task("hnode0.dfe2_0", "adp", "[{\"param\": \"volume\", \"type\": \"integer\"}, {\"param\": \"prior_m\", \"type\": \"list\"}, {\"param\": \"prior_v\", \"type\": \"list\"}, {\"param\": \"y\", \"type\": \"list\"}, {\"param\": \"post_s\", \"type\": \"list\"}, {\"param\": \"post_m\", \"type\": \"list\"}]", 10000)


insert_impl("hnode0.dfe2_0", "dfe_compute", "adp", "../library/adp",
                        "{\"construct\": [{\"param\":\"volume\"},{\"config\":\"n\"},"
                                                        + "{\"param\":\"prior_m\"},{\"param\":\"prior_v\"},"
                                                        + "{\"param\":\"y\"}],"
                        + "\"destruct\": [{\"param\":\"post_m\"}, {\"param\":\"post_s\"}]}",
                        "hnode0.dfe2_0")


insert_task("hnode0.dfe4_0", "adp", "[{\"param\": \"volume\", \"type\": \"integer\"}, {\"param\": \"prior_m\", \"type\": \"list\"}, {\"param\": \"prior_v\", \"type\": \"list\"}, {\"param\": \"y\", \"type\": \"list\"}, {\"param\": \"post_s\", \"type\": \"list\"}, {\"param\": \"post_m\", \"type\": \"list\"}]", 10000)


insert_impl("hnode0.dfe4_0", "dfe_compute", "adp", "../library/adp",
                        "{\"construct\": [{\"param\":\"volume\"},{\"config\":\"n\"},"
                                                        + "{\"param\":\"prior_m\"},{\"param\":\"prior_v\"},"
                                                        + "{\"param\":\"y\"}],"
                        + "\"destruct\": [{\"param\":\"post_m\"}, {\"param\":\"post_s\"}]}",
                        "hnode0.dfe4_0")

insert_task("hnode0.dfe2_0", "align", "[{\"param\": \"volume\", \"type\": \"integer\"}, {\"param\": \"file\", \"type\": \"string\"}]", 0)

insert_impl("hnode0.dfe2_0", "dfe_compute", "align", "../library/align",
                        "{\"construct\": [{\"param\":\"volume\"},{\"config\":\"n\"},{\"param\":\"file\"}],"
                        + "\"destruct\": []}",
                        "hnode0.dfe2_0")



for i in range(num_dfes):
	insert_task("hnode0.dfe1_"+str(i), "adp", "[{\"param\": \"volume\", \"type\": \"integer\"}, {\"param\": \"prior_m\", \"type\": \"list\"}, {\"param\": \"prior_v\", \"type\": \"list\"}, {\"param\": \"y\", \"type\": \"list\"}, {\"param\": \"post_s\", \"type\": \"list\"}, {\"param\": \"post_m\", \"type\": \"list\"}]", 10000)


	insert_impl("hnode0.dfe1_"+str(i), "dfe_compute", "adp", "../library/adp_maia",
                        "{\"construct\": [{\"param\":\"volume\"},{\"config\":\"n\"},"
                                                        + "{\"param\":\"prior_m\"},{\"param\":\"prior_v\"},"
                                                        + "{\"param\":\"y\"}],"
                        + "\"destruct\": [{\"param\":\"post_m\"}, {\"param\":\"post_s\"}]}",
                        "hnode0.dfe1_"+str(i))

	insert_task("hnode0.dfe1_"+str(i), "align", "[{\"param\": \"volume\", \"type\": \"integer\"}, {\"param\": \"file\", \"type\": \"string\"}]", 0)

	insert_impl("hnode0.dfe1_"+str(i), "dfe_compute", "align", "../library/align",
                        "{\"construct\": [{\"param\":\"volume\"},{\"config\":\"n\"},{\"param\":\"file\"}],"
                        + "\"destruct\": []}",
                        "hnode0.dfe1_"+str(i))

	insert_task("hnode0.dfe1_"+str(i), "nbody", "[{\"param\": \"volume\", \"type\": \"integer\"}]", 0)

	insert_impl("hnode0.dfe1_"+str(i), "dfe_compute", "nbody", "../library/nbody",
                        "{\"construct\": [{\"param\":\"volume\"}],"
                        + "\"destruct\": []}",
                        "hnode0.dfe1_"+str(i))

num_maxnode_dfes = 4
for i in range(num_maxnode_dfes):
	insert_task("hnode0.dfe1_"+str(num_dfes+i), "adp", "[{\"param\": \"volume\", \"type\": \"integer\"}, {\"param\": \"prior_m\", \"type\": \"list\"}, {\"param\": \"prior_v\", \"type\": \"list\"}, {\"param\": \"y\", \"type\": \"list\"}, {\"param\": \"post_s\", \"type\": \"list\"}, {\"param\": \"post_m\", \"type\": \"list\"}]", 10000)


	insert_impl("hnode0.dfe1_"+str(num_dfes+i), "dfe_compute", "adp", "../library/adp",
                        "{\"construct\": [{\"param\":\"volume\"},{\"config\":\"n\"},"
                                                        + "{\"param\":\"prior_m\"},{\"param\":\"prior_v\"},"
                                                        + "{\"param\":\"y\"}],"
                        + "\"destruct\": [{\"param\":\"post_m\"}, {\"param\":\"post_s\"}]}",
                        "hnode0.dfe1_"+str(num_dfes+i))

for i in range(num_cpus):
	insert_task("hnode0.cpu1_"+str(i), "adp", "[{\"param\": \"volume\", \"type\": \"integer\"}, {\"param\": \"prior_m\", \"type\": \"list\"}, {\"param\": \"prior_v\", \"type\": \"list\"}, {\"param\": \"y\", \"type\": \"list\"}, {\"param\": \"post_s\", \"type\": \"list\"}, {\"param\": \"post_m\", \"type\": \"list\"}]", 1000)


	insert_impl("hnode0.cpu1_"+str(i), "cpu_compute", "adp", "../library/adp_maia",
                        "{\"construct\": [{\"param\":\"volume\"},{\"config\":\"n\"},"
                                                        + "{\"param\":\"prior_m\"},{\"param\":\"prior_v\"},"
                                                        + "{\"param\":\"y\"}],"
                        + "\"destruct\": [{\"param\":\"post_m\"}, {\"param\":\"post_s\"}]}",
                        "hnode0.cpu1_"+str(i))

	insert_task("hnode0.cpu1_"+str(i), "align", "[{\"param\": \"volume\", \"type\": \"integer\"}, {\"param\": \"file\", \"type\": \"string\"}]", 0)

	insert_impl("hnode0.cpu1_"+str(i), "cpu_compute", "align", "../library/align",
                        "{\"construct\": [{\"param\":\"volume\"},{\"config\":\"n\"},{\"param\":\"file\"}],"
                        + "\"destruct\": []}",
                        "hnode0.cpu1_"+str(i))

	insert_task("hnode0.cpu1_"+str(i), "nbody", "[{\"param\": \"volume\", \"type\": \"integer\"}]", 0)

	insert_impl("hnode0.cpu1_"+str(i), "cpu_compute", "nbody", "../library/nbody",
                        "{\"construct\": [{\"param\":\"volume\"},{\"config\":\"n\"}],"
                        + "\"destruct\": []}",
                        "hnode0.cpu1_"+str(i))
