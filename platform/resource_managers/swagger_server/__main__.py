#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from swagger_server.cpu_resource_manager import CPUResourceManager
from swagger_server.dfe_resource_manager import DFEResourceManager
from swagger_server.hnode_resource_manager import HNodeResourceManager
from swagger_server.cluster_resource_manager import ClusterResourceManager

from optparse import OptionParser

parser = OptionParser()

parser.add_option("-p", "--port", dest="port", type="int")
parser.add_option("--rm_type", dest="rm_type", type="string")
parser.add_option("-c", "--cfg", dest="cfg", type="string")

(options, _) = parser.parse_args()


def main():

	string = options.rm_type + "(\"" + options.cfg + "\")"
	print(string)
	try:
		rm = eval(string)
	except:
		print("Please specify valid class name and cfg file path.")
		exit()	

	if not options.port:
		print("Please specify a port")
		exit()

	app = connexion.App(__name__, specification_dir='./swagger/')
	app.app.json_encoder = encoder.JSONEncoder
	app.add_api('swagger.yaml', arguments={'title': 'RM Prototype'})
	
	app.app.config['rm_object'] = rm
		
	app.run(port=options.port)

if __name__ == '__main__':
	main()
