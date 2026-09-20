# Performance and memory

Read before changing execution for speed, memory pressure, parallelism, or by-reference
mutation.

Profile representative work before optimizing. Reduce repeated computation and reads
before changing packages or adding workers. Compare outputs as well as elapsed time.

Read only needed columns or process in batches when scale warrants it. Do not introduce
databases or disk-backed machinery without a demonstrated requirement.

With `data.table`, `:=` and `set*()` mutate by reference. Use
`data.table::copy(original)` when the original must remain independent; ordinary
assignment does not create an independent deep copy for this purpose.

Parallelize substantial independent work only when measured benefit exceeds overhead.
Respect available CPU/memory, avoid nested worker multiplication, use reproducible RNG
support for stochastic jobs, and compare against serial results where applicable.
