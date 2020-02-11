import orian, time

configured = orian.configure("http://cccad2.doc.ic.ac.uk:8087/jvandebon/rm_prototype/2.0")

if not configured:
        print("Invalid URL")
        exit(0)

orian.execute_sync("nbody",
               	[{"param":"volume", "value": 20000}],
                20000,
                [{'config': {'n': 1, 'name':'1T'},
                 'impl': {'taskName': 'nbody', 'implName': 'cpu_compute', 'implRM': 'cluster0.hnode1.cpu0'}}], 
		profile=True)


orian.execute_sync("nbody",
                [{"param":"volume", "value": 10000}],
               10000,
               [{'config': {'n': 1, 'name':'1DFE'},
                'impl': {'taskName': 'nbody', 'implName': 'dfe_compute', 'implRM': 'cluster0.hnode1.dfe0'}}],
		profile=True)

