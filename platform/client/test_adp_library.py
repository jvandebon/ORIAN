import adp

context = adp.cpu_compute_construct(10, 2, "../resource_managers/swagger_server/prior_m", 
					"../resource_managers/swagger_server/prior_v", 
					"../resource_managers/swagger_server/y")
adp.cpu_compute(context)

adp.cpu_compute_destruct(context, "../resource_managers/swagger_server/post_m_cpu", "../resource_managers/swagger_server/post_s_cpu")

print("CPU compute done")

context2 = adp.dfe_compute_construct(10, 2, "../resource_managers/swagger_server/prior_m",
                                        "../resource_managers/swagger_server/prior_v",
                                        "../resource_managers/swagger_server/y")

adp.dfe_compute(context2)
adp.dfe_compute_destruct(context2, "../resource_managers/swagger_server/post_m_dfe", "../resource_managers/swagger_server/post_s_dfe")

print("DFE compute done")
