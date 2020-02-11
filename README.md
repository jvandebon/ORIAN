#### Demo  Videos:

1. [Decision Making](https://drive.google.com/file/d/1dVfMgUPPwXdx4Cg_nU587R4FoSyfyzw9/view?usp=sharing)

2. [Profiling](https://drive.google.com/file/d/1s24EzgQSdtmSwIwjk3Yn-JllSydMP4Ds/view?usp=sharing)

The instructions below are how to run the ORIAN platform on Imperial's heterogeneous architecture with access to Maxeler DFE nodes and multi-CPU nodes. To run on another platform, add modified config files to platform/resource_managers/swagger_server/config_files with IP addresses of local machines, and change the paths in the below commands as necessary. 

********************************************************************************
### To run prototype platform 1 (one heterogeneous node with CPU and DFE children):
********************************************************************************

#### 1. Run the database

cd /platform/Docker

./run-oriain.sh -p 8080

cd platform/database/

rm impl.db task.db 				// clear impls and tasks

python3 db_prototype.y

On another tab:

cd /platform/Docker

./run-orian.sh

cd platform/database/

python3 setup_dbs.py platform1     

#### 2. Run the heterogeneous node manager

cd /platform/Docker

./run-oriain.sh -p 8081

cd platform/resource_managers

python3 -m swagger_server --rm_type HNodeResourceManager --cfg swagger_server/config_files/hnode_cfg.json -p 8081

#### 3. Run the CPU manager

cd /platform/Docker

./run-oriain.sh -p 8082

cd platform/resource_managers

python3 -m swagger_server --rm_type CPUResourceManager --cfg swagger_server/config_files/cpu_cfg.json -p 8082

#### 4.  Run the DFE manager

cd /platform/Docker

./run-oriain.sh -p 8083

cd platform/resource_managers

python3 -m swagger_server --rm_type DFEResourceManager --cfg swagger_server/config_files/dfe_cfg.json -p 8083


**********************************************************************
### To run prototype platform 2 (cluster with 2 heterogeneous nodes):
**********************************************************************

#### 1. Run the database

cd /platform/Docker

./run-oriain.sh -p 8080

cd platform/database/

rm impl.db task.db 				// clear impls and tasks

python3 db_prototype.y

On . another tab:

cd /platform/Docker

./run-orian.sh

cd platform/database/

python3 setup_dbs.py platform2

#### 2. Run the cluster manager:

cd /platform/Docker

./run-oriain.sh -p 8087

cd platform/resource_managers

python3 -m swagger_server --rm_type ClusterResourceManager --cfg swagger_server/config_files/cluster_cfg.json -p 8087

#### 3. Run both heterogeneous node managers

cd /platform/Docker

./run-oriain.sh -p 8081

cd platform/resource_managers

python3 -m swagger_server --rm_type HNodeResourceManager --cfg swagger_server/config_files/maxnode_hnode_cfg.json -p 8081

On another tab:

cd /platform/Docker

./run-oriain.sh -p 8084

cd platform/resource_managers

python3 -m swagger_server --rm_type HNodeResourceManager --cfg swagger_server/config_files/maia_hnode_cfg.json -p 8084

#### 4. Run Node 1 CPU manager

cd /platform/Docker

./run-oriain.sh -p 8082

cd platform/resource_managers

python3 -m swagger_server --rm_type CPUResourceManager --cfg swagger_server/config_files/maxnode_cpu_cfg.json -p 8082

#### 5. Run Node 1 DFE manager

cd /platform/Docker

./run-oriain.sh -p 8083

cd platform/resource_managers

python3 -m swagger_server --rm_type DFEResourceManager --cfg swagger_server/config_files/maxnode_dfe_cfg.json -p 8083

#### 6. Run Node 2 CPU manager

cd /platform/Docker

./run-oriain.sh -p 8085

cd platform/resource_managers

python3 -m swagger_server --rm_type CPUResourceManager --cfg swagger_server/config_files/maia_cpu_cfg.json -p 8085

#### 7. Run Node 2 DFE manager

cd /platform/Docker

./run-oriain.sh -p 8086

cd platform/resource_managers

python3 -m swagger_server --rm_type DFEResourceManager --cfg swagger_server/config_files/maia_dfe_cfg.json -p 8086

