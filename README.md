The below instructions show examples of how to run the ORIAN platform on Imperial's heterogeneous architecture with access to Maxeler DFE nodes and multi-CPU nodes. 
To run on another platform, change config files as necessary with IP addresses of local machines. 

********************************************************************************
To run prototype platform 1 (one heterogeneous node with CPU and DFE children):
********************************************************************************

1. RUN THE DATABASE:

On cccad2:
cd /platform/Docker
./run-oriain.sh -p 8080
cd platform/database/
rm impl.db task.db 				// clear impls and tasks
python3 db_prototype.y

On cccad2 in another tab:
cd /platform/Docker
./run-orian.sh
cd platform/database/
python3 setup_dbs.py platform1     

2. RUN THE HETEROGENEOUS NODE MANAGER:

On cccad2:
cd /platform/Docker
./run-oriain.sh -p 8081
cd platform/resource_managers
python3 -m swagger_server --rm_type HNodeResourceManager --cfg swagger_server/config_files/hnode_cfg.json -p 8081

3. RUN THE CPU RESOURCE MANAGER:

On maxnode2:
cd /platform/Docker
./run-oriain.sh -p 8082
cd platform/resource_managers
python3 -m swagger_server --rm_type CPUResourceManager --cfg swagger_server/config_files/cpu_cfg.json -p 8082

4.  RUN THE DFE RESOURCE MANAGER:

On maxnode2:
cd /platform/Docker
./run-oriain.sh -p 8083
cd platform/resource_managers
python3 -m swagger_server --rm_type DFEResourceManager --cfg swagger_server/config_files/dfe_cfg.json -p 8083


**********************************************************************
To run prototype platform 2 (cluster with 2 heterogeneous nodes):
**********************************************************************

1. RUN THE DATABASE:

On cccad2:
cd /platform/Docker
./run-oriain.sh -p 8080
cd platform/database/
rm impl.db task.db 				// clear impls and tasks
python3 db_prototype.y

On cccad2:
cd /platform/Docker
./run-orian.sh
cd platform/database/
python3 setup_dbs.py platform2

2. RUN THE CLUSTER MANAGER:

On cccad2:
cd /platform/Docker
./run-oriain.sh -p 8087
cd platform/resource_managers
python3 -m swagger_server --rm_type ClusterResourceManager --cfg swagger_server/config_files/cluster_cfg.json -p 8087

3. RUN BOTH HETEROGENEOUS NODE MANAGERS:

On cccad2:
cd /platform/Docker
./run-oriain.sh -p 8081
cd platform/resource_managers
python3 -m swagger_server --rm_type HNodeResourceManager --cfg swagger_server/config_files/maxnode_hnode_cfg.json -p 8081

On cccad2:
cd /platform/Docker
./run-oriain.sh -p 8084
cd platform/resource_managers
python3 -m swagger_server --rm_type HNodeResourceManager --cfg swagger_server/config_files/maia_hnode_cfg.json -p 8084

4. RUN NODE 1 CPU RESOURCE MANAGER:

On maxnode2:
cd /platform/Docker
./run-oriain.sh -p 8082
cd platform/resource_managers
python3 -m swagger_server --rm_type CPUResourceManager --cfg swagger_server/config_files/maxnode_cpu_cfg.json -p 8082

5. RUN NODE 1 DFE RESOURCE MANAGER:

On maxnode2:
cd /platform/Docker
./run-oriain.sh -p 8083
cd platform/resource_managers
python3 -m swagger_server --rm_type DFEResourceManager --cfg swagger_server/config_files/maxnode_dfe_cfg.json -p 8083

6. RUN NODE 2 CPU RESOURCE MANAGER:

On maia01:
cd /platform/Docker
./run-oriain.sh -p 8085
cd platform/resource_managers
python3 -m swagger_server --rm_type CPUResourceManager --cfg swagger_server/config_files/maia_cpu_cfg.json -p 8085

7. RUN NODE 2 DFE RESOURCE MANAGER:

On maia01:
cd /platform/Docker
./run-oriain.sh -p 8086
cd platform/resource_managers
python3 -m swagger_server --rm_type DFEResourceManager --cfg swagger_server/config_files/maia_dfe_cfg.json -p 8086

