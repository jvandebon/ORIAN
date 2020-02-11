import orian, time

configured = orian.configure("http://cccad2.doc.ic.ac.uk:8081/jvandebon/rm_prototype/2.0")

if not configured:
        print("Invalid URL")
        exit(0)

orian.execute("nbody",
               	[{"param":"volume", "value": 20000}],
                20000,
                [{'config': {'n': 1, 'name':'1T'},
                 'impl': {'taskName': 'nbody', 'implName': 'cpu_compute', 'implRM': 'cluster0.hnode1.cpu0'}}], 
		profile=True)


orian.execute("adp",
                       [       {"param":"volume", "value": 1000},
                               {"param":"prior_m", "value": "../resource_managers/swagger_server/prior_m"},
                               {"param":"prior_v", "value": "../resource_managers/swagger_server/prior_v"},
                               {"param":"y", "value": "../resource_managers/swagger_server/y"},
                               {"param": "post_m", "value": "../resource_managers/swagger_server/post_m_"},
                               {"param": "post_s", "value": "../resource_managers/swagger_server/post_s_"} ],
               1000,
               [{'config': {'n': 12, 'name':'12T'},
                'impl': {'taskName': 'adp', 'implName': 'cpu_compute', 'implRM': 'cluster0.hnode0.cpu0'}}],
		profile=True)

