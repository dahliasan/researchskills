---
name: dayhoff-slurm
description: >-
  Submit, size and check SLURM jobs on ANU Dayhoff HPC. Use before running
  sbatch, dsub, srun or salloc on Dayhoff; before writing or editing any
  .sh with #SBATCH lines (including changing --mem, --time or --cpus); when
  reading a Slurm log or a low memory utilization email; or when the user
  says /dayhoff-slurm, "run this on the cluster" or "sbatch on dayhoff".
  Covers dsub history-based sizing, conda R env selection (r_env vs
  R-py310), sequeira group paths and preflight checks. Connectivity:
  dahlias-fleet ssh-fleet (not this skill).
metadata:
  version: 1.1.0
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

## Submit with `dsub` (default for every job)

Do not hand-write an sbatch file with a fixed `--mem=20G`. Admins email a
low-utilization warning when a job uses under 70% of the memory it asked for.
Use `~/bin/dsub` on Dayhoff, which sizes the request from the job's own history.
The tools live in this skill's `bin/` (`dsub`, `dsub-size`, `slurm-usage`).
On Dayhoff they are linked from a private clone. To install or update:

```bash
ssh dayhoff 'git -C ~/researchskills pull -q && ~/researchskills/skills/dayhoff-slurm/bin/install-dayhoff'
```


```bash
ssh dayhoff 'cd /home/groups/sequeira/MegaMove_Threats && ~/bin/dsub -J endloc_export -- Rscript scripts/end_locations/05_export_tables.R'
```

- **Sizing:** with no `-m`/`-t`, `dsub` calls `~/bin/dsub-size <name> <dir>`,
  which reads `~/.dsub/history.tsv`. It takes the highest peak of the last 5
  runs with the same job name and folder, adds 30% and rounds up to a whole GB
  (minimum 1G). It sets time to twice the longest run (minimum 30 min). If the
  last run hit its limit, it doubles the request.
- **First run:** a job with no history gets 4G and 2 h, and that run is the
  measurement. Use a **stable `-J` name** per workload so later runs find it.
  If the code can say more (it loads a 15 GB object, say), pass `-m` once.
- **Feedback:** the conda env, `R_LIBS` and `./.env` are loaded for you. The
  log is `slurm_logs/dsub-<name>-<job>.out` in the submit folder. Its last lines
  are a resources table plus any `ADJUST` line. `slurm-usage` also appends the
  run to the history file, so the next run corrects itself.
- **Measure:** peak memory excludes reclaimable page cache, which is the same
  measure the admin emails use.
- **After every job:** read the table, and if it has an `ADJUST` line, say so
  in your reply. Tell the user if a run will be flagged (under 70%).
- **Long jobs (hours) with no history:** run a small slice first (one taxon,
  a few bootstraps) under the same `-J` name, or watch the live peak with
  `slurm-mem-report.sh <JOB_ID>`. `scancel` early if it is far off the request,
  and resubmit. Memory can't change on a running job.
- **Wait:** wait for jobs with a background `until ! squeue -h -j ID | grep -q ID`
  loop, not by polling in chat.

Use a hand-written sbatch script only for arrays or multi-step pipelines. Then
copy the sizing from `dsub-size`, and end the script with
`~/bin/slurm-usage <cpus> <mem> <start epoch>` so the run is recorded.

## SLURM defaults (Sequeira jobs)

| Directive | Typical value |
|-----------|---------------|
| `--partition` | `Standard` |
| `--nodes` | `1` |
| `--ntasks` | `1` |
| `--cpus-per-task` | `1` (raise only if the R script uses parallel) |
| `--mem` | from `dsub-size` (history peak + 30%, min 1G); 4G for a first run. Never a blanket 20G. `sacct` MaxRSS is empty on this cluster |
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
#SBATCH --mem=4G   # replace with `~/bin/dsub-size <job-name>` output
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

if [[ -n "${SLURM_JOB_ID:-}" ]]; then
  trap '/mnt/data/dayhoff/home/shared/software/bin/slurm-mem-report.sh || true' EXIT
fi

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

### Peak RAM report (required)

Dayhoff ships a cgroup peak-RAM reporter. Put it at the **end** of every
`#SBATCH` script (or `trap` on `EXIT`) so stdout shows actual RAM used — better
than `sacct`/`seff` `MaxRSS`, which are often empty on this cluster.

```bash
# End of script — peak RAM for sizing next ask (cluster guide / SBATCH structure)
/mnt/data/dayhoff/home/shared/software/bin/slurm-mem-report.sh || true
```

Preferred in new wrappers:

```bash
set -euo pipefail
if [[ -n "${SLURM_JOB_ID:-}" ]]; then
  trap '/mnt/data/dayhoff/home/shared/software/bin/slurm-mem-report.sh || true' EXIT
fi
```

Manual while job is still in `squeue`:
`/mnt/data/dayhoff/home/shared/software/bin/slurm-mem-report.sh <JOB_ID>`

MegaMove_Models: project skill `.cursor/skills/dayhoff/SKILL.md` § Peak RAM
report; all repo-root `run_*.sh` use the EXIT trap. If `#SBATCH --output=/dev/null`,
tee the report into the script's `LOG_FILE` instead of relying on Slurm stdout.

### After the run

Check the mem-report line in the job stdout log (and `seff JOBID` if available)
— tune `--mem` and `--time` from observed usage.

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
| Editing or moving files on Dayhoff (write over ssh, never through the sshfs mount) | `dayhoff-remote-edits` |
| SSH, VPN, ProxyJump | `dahlias-fleet` → `ssh-fleet.md` |
| R script style | `r-human-code` |
| Local R editor env | `r-editor-setup` |
