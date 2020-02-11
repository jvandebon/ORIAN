import orian

configured = orian.configure("http://cccad2.doc.ic.ac.uk:8081/jvandebon/rm_prototype/2.0")

if not configured:
        print("Invalid URL")
        exit(0)

result = orian.execute("align",
               [       {"param":"volume", "value": 100000},
                       {"param":"file", "value": "../../apps/exact_align/data/hg38"} ],
                       100000,
                       {'n': 4, 'name':'4T'},
                       {'taskName': 'align', 'implName': 'cpu_compute', 'implRM': 'hnode0.cpu0'},
profile=True)

'''result = orian.execute("align",
               [       {"param":"volume", "value": 1000000},
                       {"param":"file", "value": "../../apps/exact_align/data/hg38"} ],
                       1000000,
                       {'n': 4, 'name':'4DFE'},
                       {'taskName': 'align', 'implName': 'dfe_compute', 'implRM': 'hnode0.dfe0'})'''
