---
name: dayhoff-slurm
description: >-
  Submit R and Python analysis scripts as SLURM jobs on ANU Dayhoff HPC.
  Covers sbatch templates, conda R env selection (r_env vs R-py310), sequeira
  group paths, preflight checks, and job monitoring. Use when expensive compute
  should run on Dayhoff, or the user says /dayhoff-slurm, "sbatch on dayhoff",
  or "run this on the cluster". Connectivity: dahlias-fleet ssh-fleet (not this
  skill).
metadata:
  version: 1.0.1
---

# /dayhoff-slurm — ANU Dayhoff batch jobs

Dayhoff is the ANU RSB SLURM cluster for MegaMove / Sequeira group research.
**SSH/VPN first** — see `dahlias-fleet` → `ssh-fleet.md` (`ssh dayhoff` or
`ssh dayhoff-via-dahlia`). This skill covers **job submission after you are on
the cluster or scripting remote sbatch**.

## Paths

Dayhoff mounts group storage under `/mnt/data/dayhoff/home/...`. In SLURM
scripts, use the full mount path (not `~`):

| What | Path |
|------|------|
| Sequeira group | `/mnt/data/dayhoff/home/groups/sequeira` |
| MegaMove Standards | `.../MegaMove_Standards` |
| MegaMove Threats | `.../MegaMove_Threats` |
| Group conda envs | `.../conda_envs/` |

## Conda R — pick by project

**No `module load` on Dayhoff** — use conda R binaries directly.

| Project | Env | `CONDA_R` path | Notes |
|---------|-----|----------------|-------|
| **MegaMove_Models** | `R-py310` | `/mnt/data/dayhoff/home/u4887749/.conda/envs/R-py310` | All `run_*.sh` / production scripts; set `PROJ_LIB=.../R-py310/share/proj` |
| **MegaMove_Threats** | `R-py310` | same | All `job_*_dayhoff.sh`, end_locations jobs |
| **MegaMove_Standards** | `r_env` | `/mnt/data/dayhoff/home/groups/sequeira/conda_envs/r_env` | Group env with `trip` + spatial stack (Aug 2026); **not yet in repo scripts** — call `r_env/bin/Rscript` explicitly |

`r_env` was bootstrapped for Standards because `trip` would not install in
`R-py310`. Standards R scripts use `#!/usr/bin/env Rscript` with no conda path
baked in — SLURM wrappers must set `CONDA_R` to `r_env` for GAT/L2 work.

For `r_env` jobs, also export PROJ (batch shells do not inherit conda activate
hooks reliably):

```bash
export PROJ_LIB="${CONDA_R}/share/proj"
export PROJ_DATA="${CONDA_R}/share/proj"
```

Override with `CONDA_R_ENV` in the shell script if needed.

**Do not use** the removed `r_mm` env — superseded by `r_env` (Aug 2026). Legacy
`~/.conda/envs/R` is also gone; old Models scripts referencing it need updating.

### Library shadowing (Threats jobs)

User `~/R/` can shadow conda packages (e.g. old `reformulas`). In the `.sh`
wrapper:

```bash
export R_LIBS_USER=""
export R_LIBS="${CONDA_R}/lib/R/library"
```

## SLURM defaults (Sequeira jobs)

| Directive | Typical value |
|-----------|---------------|
| `--partition` | `Standard` |
| `--nodes` | `1` |
| `--ntasks` | `1` |
| `--cpus-per-task` | `1` (raise only if the R script uses parallel) |
| `--mem` | `32G` (profile with `sacct`/`seff` and adjust) |
| `--time` | `04:00:00`–`12:00:00` |
| `--output` / `--error` | Under project `output/.../slurm_%j.out` |

GPU partition exists (`GPU`) — only request when the script actually uses GPU.

## Template — single R script

```bash
#!/bin/bash
#SBATCH --job-name=my_analysis
#SBATCH --partition=Standard
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --output=output/my_workstream/slurm_%j.out
#SBATCH --error=output/my_workstream/slurm_%j.err

set -euo pipefail

PROJECT=/mnt/data/dayhoff/home/groups/sequeira/MegaMove_Threats
cd "${PROJECT}"
mkdir -p output/my_workstream

CONDA_R="${CONDA_R_ENV:-/mnt/data/dayhoff/home/u4887749/.conda/envs/R-py310}"
export R_LIBS_USER=""
export R_LIBS="${CONDA_R}/lib/R/library"
export OMP_NUM_THREADS=1

# Project-specific env vars (read once at top of matching .R script)
export APR2026_TRACKDUR_OUT="${PROJECT}/output/track_duration"

echo "Host=$(hostname) Start=$(date) R=$(${CONDA_R}/bin/Rscript --version)"
"${CONDA_R}/bin/Rscript" code/v2_apr2026/my_script.R
echo "End=$(date)"
```

For **Standards/GAT**, set `CONDA_R` to `.../conda_envs/r_env` instead.

## Template — chained R scripts with preflight

From `MegaMove_Threats/.../job_file2_3_dayhoff.sh` — check upstream outputs
before running downstream:

```bash
n_sp=$(ls -1 "${APR2026_TRACKDUR_OUT}/by_species"/*.csv 2>/dev/null | wc -l)
if [[ "${n_sp}" -lt 100 ]]; then
  echo "ERROR: File 1 incomplete (${n_sp}/111). Wait for file1 job."
  exit 1
fi

"${CONDA_R}/bin/Rscript" code/v2_apr2026/track_duration/02_build_file2_bins.R
"${CONDA_R}/bin/Rscript" code/v2_apr2026/track_duration/03_build_file3_individual.R
```

## Submit and monitor

```bash
# From off-campus (GlobalProtect VPN) or via ProxyJump through campus network
ssh dayhoff 'cd /mnt/data/dayhoff/home/groups/sequeira/MegaMove_Threats && sbatch code/v2_apr2026/track_duration/job_file1_dayhoff.sh'

# On Dayhoff
sbatch path/to/job.sh
squeue -u u4887749
sacct -j JOBID --format=JobID,JobName,State,Elapsed,MaxRSS,ExitCode
scancel JOBID
```

After a run completes, check `seff JOBID` if available — tune `--mem` and
`--time` from observed usage.

## Job arrays (taxon / parameter sweeps)

```bash
#SBATCH --array=1-8%4
TAXA=(dugong turtle shark whale ...)
taxon="${TAXA[$SLURM_ARRAY_TASK_ID]}"
"${CONDA_R}/bin/Rscript" code/run_taxon.R  # taxon from env, not commandArgs — set in shell
```

Pass sweep indices via **exported env vars** read at the top of the R script,
not `commandArgs()` (see `r-human-code`).

## Preflight checklist

Before `sbatch`:

1. Correct `CONDA_R` for workstream (`r_env` vs `R-py310`)
2. `cd` to project root; output dirs exist
3. Input files / upstream job outputs present
4. R script uses plain path variables (no CLI parsing)
5. Log paths writable under group storage
6. VPN up if submitting from off-campus (`ssh dayhoff` probe)

## Known issues

- **`r_env` PROJ warning:** if `sf`/`terra` reprojection fails, set
  `PROJ_LIB` and `PROJ_DATA` to `${CONDA_R}/share/proj` in the SLURM script
  (conda activate alone is not enough in batch). Reinstall spatial stack only
  if that still fails.
- **`glmmTMB` / `TMB` version mismatch** in `R-py310`: reinstall from source
  or align TMB if models fail at load time.

## Companions

| Need | Skill |
|------|--------|
| SSH, VPN, ProxyJump | `dahlias-fleet` → `ssh-fleet.md` |
| R script style | `r-human-code` |
| Local R editor env | `r-editor-setup` |
