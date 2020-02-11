import align


print("Testing cpu...")
c = align.cpu_compute_construct(50000, 12, "../../../apps/exact_align/data/hg38")
align.cpu_compute(c)
align.cpu_compute_destruct(c)

print("Testing dfe...")
c = align.dfe_compute_construct(5000000, 2, "../../../apps/exact_align/data/hg38")
align.dfe_compute(c)
align.dfe_compute_destruct(c)


