rm import flask, sqlite3, uuid
from flask import request, Response, json

app = flask.Flask(__name__)

# create tasks db
conn = sqlite3.connect('task.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS task
             (rm_id text, task_name text, input_params text, task_granularity int)''')
conn.commit()
conn.close()

#create impls db
conn = sqlite3.connect('impl.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS impl
             (rm_id text, impl_name text, task_name text, 
             path text, runtime text, impl_rm text)''')
conn.commit()
conn.close()

#create profiles db
conn = sqlite3.connect('profile.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS profile 
			(rm_id text, task_name text, impl_name text, 
			config text, problem_size int, time real, io_time real,
			profile_id text)''')
conn.commit()
conn.close()

#create models db
conn = sqlite3.connect('model.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS model 
			(rm_id text, task_name text, impl_name text, 
			config text, min_size integer, max_size integer, 
			coefs text, type text)''')
conn.commit()
conn.close()

def create_task(task_row):
	task = {}
	task['rm_id'] = task_row[0]
	task['task_name'] = task_row[1]
	task['input_params'] = json.loads(task_row[2])
	task['task_granularity'] = task_row[3]
	return task

@app.route('/tasks', methods=['GET'])
def get_tasks():

	tasks = []
	query_parameters = request.args

	conn = sqlite3.connect('task.db')
	c = conn.cursor()

	task_name = query_parameters.get('task_name')
	rm_id = query_parameters.get('rm_id')

	if task_name:
		c.execute("SELECT * from task where rm_id = '%s' and task_name = '%s'" % (rm_id, task_name))
		res = c.fetchone()
		if res != None:
			tasks.append(create_task(res))
	else:
		c.execute("SELECT * from task where rm_id = '%s'" % (rm_id,))
		res = c.fetchall()
		for r in res:
			tasks.append(create_task(r))

	conn.close()
	return json.dumps(tasks)

@app.route('/tasks', methods=['POST'])
def insert_task():
	task = json.loads(request.data)
	print(task)
	conn = sqlite3.connect('task.db')
	c = conn.cursor()
	c.execute("INSERT INTO task VALUES (\'" + task['rm_id'] + "\', \'" + task['task_name'] +  "\', \'"  + json.dumps(task['input_params']) + "\', \'" + str(task['task_granularity']) + "\')")
	conn.commit()
	conn.close()
	return json.dumps(task)

@app.route('/tasks', methods=['PUT'])
def update_task():
	task = json.loads(request.data)
	conn = sqlite3.connect('task.db')
	c = conn.cursor()
	c.execute("UPDATE task SET input_params = \'" + json.dumps(task['input_params']) + "\', task_granularity=" + str(task['task_granularity']) + " WHERE task_name = \'" + task['task_name'] + "\' and rm_id = \'" + task['rm_id'] + "\'")
	conn.commit()
	conn.close()
	return json.dumps(task)

def create_impl(impl_row):
	impl = {}
	impl['rm_id'] = impl_row[0]
	impl['impl_name'] = impl_row[1]
	impl['task_name'] = impl_row[2]
	impl['path'] = impl_row[3]
	impl['runtime'] = json.loads(impl_row[4])
	impl['impl_rm'] = impl_row[5]
	return impl

@app.route('/impls', methods=['GET'])
def get_impls():

	impls = []
	query_parameters = request.args

	conn = sqlite3.connect('impl.db')
	c = conn.cursor()

	rm_id = query_parameters.get('rm_id')
	impl_rm = query_parameters.get('impl_rm')
	impl_name = query_parameters.get('impl_name')
	
	task_name = query_parameters.get('task_name')

	if impl_rm and impl_name and task_name:
		c.execute("SELECT * from impl where rm_id = '%s' and impl_name = '%s' and impl_rm = '%s' and task_name= '%s'" % (rm_id, impl_name, impl_rm, task_name))
		res = c.fetchone()
		if res != None:
			impls.append(create_impl(res))
	elif impl_rm and impl_name:
		c.execute("SELECT * from impl where rm_id = '%s' and impl_name = '%s' and impl_rm = '%s'" % (rm_id, impl_name, impl_rm))
		res = c.fetchone()
		if res != None:
			impls.append(create_impl(res))
	elif impl_name:
		c.execute("SELECT * from impl where rm_id = '%s' and impl_name = '%s'" % (rm_id, impl_name))
		res = c.fetchone()
		if res != None:
			impls.append(create_impl(res))
	elif task_name:
		c.execute("SELECT * from impl where rm_id = '%s' and task_name = '%s'" % (rm_id, task_name))
		res = c.fetchall()
		for r in res:
			impls.append(create_impl(r))	
	else:
		c.execute("SELECT * from impl where rm_id = '%s'" % (rm_id,))
		res = c.fetchall()
		for r in res:
			impls.append(create_impl(r))

	conn.close()
	return json.dumps(impls)


@app.route('/impls', methods=['POST'])
def insert_impl():
	impl = json.loads(request.data)
	print(impl)
	if 'path' not in impl:
		impl['path'] = ""
	if 'runtime' not in impl:
		impl['runtime'] = ""
	conn = sqlite3.connect('impl.db')
	c = conn.cursor()
	c.execute("INSERT INTO impl VALUES (\'" + impl['rm_id'] + "\', \'" + impl['impl_name'] +  "\', \'"  + impl['task_name'] + "\', \'" + impl['path'] + "\', \'" + json.dumps(impl['runtime']) + "\', \'" + impl['impl_rm'] + "\')")
	conn.commit()
	conn.close()
	return json.dumps(impl)

@app.route('/impls', methods=['PUT'])
def update_impl():
	impl = json.loads(request.data)
	conn = sqlite3.connect('impl.db')
	c = conn.cursor()
	c.execute("UPDATE impl SET task_name = " + json.dumps(impl['task_name']) + ", runtime = " + json.dumps(impl['runtime']) + " WHERE impl_name = " + impl['impl_name'] + " and rm_id = " + impl['rm_id'])
	conn.commit()
	conn.close()
	return json.dumps(impl)

@app.route('/profiles', methods=['POST'])
def insert_profile():
	profile = json.loads(request.data)
	print(profile)
	conn = sqlite3.connect('profile.db')
	c = conn.cursor()
	c.execute("INSERT INTO profile VALUES (\'" + profile['rm_id'] + "\', \'" + profile['task_name'] + "\', \'" + profile['impl_name'] + "\', \'" + profile['config'] + "\', \'" + str(profile['problem_size']) + "\', \'" + str(profile['time']) + "\', \'" + str(profile['io_time']) + "\', \'" + profile['profile_id'] +"\')")
	conn.commit()
	conn.close()
	return json.dumps(profile)

def create_profile(profile_row):
	profile = {}
	profile['rm_id'] = profile_row[0]
	profile['task_name'] = profile_row[1]
	profile['impl_name'] = profile_row[2]
	profile['config'] = profile_row[3]
	profile['problem_size'] = profile_row[4]
	profile['time'] = profile_row[5]
	profile['io_time'] = profile_row[6]
	profile['profile_id'] = profile_row[7]
	return profile

@app.route('/profiles', methods=['GET'])
def get_profiles():
	profiles = []
	query_parameters = request.args

	conn = sqlite3.connect('profile.db')
	c = conn.cursor()

	task_name = query_parameters.get('task_name')
	config = query_parameters.get('config')
	problem_size = query_parameters.get('problem_size')	

	if task_name and config and problem_size:
		c.execute("SELECT * from profile where task_name = '%s' and config = '%s' and problem_size = '%s'" % (task_name, config, problem_size,))
		res = c.fetchall()
		for r in res:
			profiles.append(create_profile(r))

	elif task_name and config:
		c.execute("SELECT * from profile where task_name = '%s' and config = '%s'" % (task_name,config,))
		res = c.fetchall()
		for r in res:
			profiles.append(create_profile(r))
	elif task_name:
		c.execute("SELECT * from profile where task_name = '%s'" % (task_name,))
		res = c.fetchall()
		for r in res:
			profiles.append(create_profile(r))

	conn.close()
	return json.dumps(profiles)

@app.route('/models', methods=['POST'])
def insert_model():
	model = json.loads(request.data)
	print(model)
	conn = sqlite3.connect('model.db')
	c = conn.cursor()
	c.execute("INSERT INTO model VALUES (\'" + model['rm_id'] + "\', \'" + model['task_name'] + "\', \'" + model['impl_name'] + "\', \'" + model['config'] + "\', \'" + str(model['min_size']) + "\', \'" + str(model['max_size']) + "\', \'" + json.dumps(model['coefs']) + "\',\'" + model['type'] + "\')")
	conn.commit()
	conn.close()
	return json.dumps(model)

def create_model(model_row):
	model = {}
	model['rm_id'] = model_row[0]
	model['task_name'] = model_row[1]
	model['impl_name'] = model_row[2]
	model['config'] = model_row[3]
	model['min_size'] = model_row[4]
	model['max_size'] = model_row[5]
	model['coefs'] = json.loads(model_row[6])
	model['type'] = model_row[7]
	return model

@app.route('/models', methods=['GET'])
def get_models():
	models = []
	query_parameters = request.args

	conn = sqlite3.connect('model.db')
	c = conn.cursor()

	rm_id = query_parameters.get('rm_id')
	impl_name = query_parameters.get('impl_name')
	task_name = query_parameters.get('task_name')
	config = query_parameters.get('config')
	type = query_parameters.get('type')

	if task_name and impl_name and config and type:
		c.execute("SELECT * from model where rm_id = '%s' and task_name = '%s' and impl_name = '%s' and config = '%s' and type = '%s'" % (rm_id,task_name, impl_name,config,type,))
		res = c.fetchall()
		for r in res:
			models.append(create_model(r))	
	elif task_name and impl_name:
		c.execute("SELECT * from model where rm_id = '%s' and task_name = '%s' and impl_name = '%s'" % (rm_id,task_name, impl_name,))
		res = c.fetchall()
		for r in res:
			models.append(create_model(r))
	elif task_name:
		c.execute("SELECT * from model where task_name = '%s'" % (task_name,))
		res = c.fetchall()
		for r in res:
			models.append(create_model(r))	
	elif rm_id:
		c.execute("SELECT * from model where rm_id = '%s'" % (rm_id,))
		res = c.fetchall()
		for r in res:
			models.append(create_model(r))

	conn.close()
	return json.dumps(models)

app.run(host='0.0.0.0', port="8080")

