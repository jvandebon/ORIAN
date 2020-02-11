import orian, time, json,sys

configured = orian.configure("http://cccad2.doc.ic.ac.uk:8087/jvandebon/rm_prototype/2.0")

if not configured: 
	print("Invalid URL")
	exit(0)

volume = 50000

orian.execute("nbody",
                [{"param":"volume", "value": volume}],
                volume,
                [{'config': {'n': 1, 'name':'1DFE'},
                 'impl': {'taskName': 'nbody', 'implName': 'dfe_compute', 
				'implRM': 'cluster0.hnode1.dfe0'}
		}])


## should realized dfe is busy and pick cpu

orian.execute("nbody", [{"param":"volume", "value": volume}], volume)

