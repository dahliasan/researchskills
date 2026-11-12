---
name: dayhoff-remote-edits
description: >-
  Rules for changing files on the ANU Dayhoff cluster (host dayhoff). Use this
  whenever the working directory, a file path, or the task involves Dayhoff:
  any path under /Users/dahlia/mnt/dayhoff-sequeira or /home/groups/sequeira,
  the MegaMove_Models repo, or the MegaMove production checkout. Also use it
  before any create, edit, move, delete, chmod, mkdir, git commit, git checkout
  or git switch that touches Dayhoff files, and when the user says "on Dayhoff",
  "the mount", "sshfs", "write via ssh", or "the live checkout". Writes go over
  ssh, never through the sshfs mount, which hangs. Reads and scans also go over
  ssh. Load this before the first write, not after.
metadata:
  version: 1.0.0
---

# Dayhoff remote edits

The local folder `/Users/dahlia/mnt/dayhoff-sequeira/...` is an sshfs (macFUSE)
mount of the live Dayhoff checkout. It is unstable. It hangs, and it can break
the shell's working directory. Writing through it has also left partial edits.

**The rule: every change to a Dayhoff file runs on Dayhoff over ssh.** Never use
Write, Edit, `cp`, `mv`, `rm`, `sed -i`, `python` file writes, `git` write
commands, or redirects (`>`, `>>`) against a path under the mount.

## Session setup

- Always use the Dayhoff repo path in remote commands: `/home/groups/sequeira/MegaMove_Models`.
- Use ssh with timeouts: `ssh -o ConnectTimeout=20 -o ServerAliveInterval=10 dayhoff '<command>'`.
- Keep the local shell in the scratchpad, not in the mount. If the shell reports
  "working directory no longer leads where it did", the mount has dropped. Stop
  and tell the user. Do not work around it by writing through the mount.
- Local drafts (scripts, files to upload) go in the session scratchpad. Use
  `/private/tmp/claude-501/<project>/<session>/scratchpad/`. Never use `/tmp` on
  Dayhoff unless the user asks.

## How to make a change

1. **Write the change as a local file** in the scratchpad when it is more than one line.
2. **Send it to Dayhoff over stdin**, then run it there:

   ```bash
   ssh -o ConnectTimeout=20 dayhoff 'cat > /home/groups/sequeira/MegaMove_Models/path/file.md' < "$SCRATCH/file.md"
   ssh -o ConnectTimeout=20 dayhoff 'bash -s' < "$SCRATCH/edit.sh"        # multi-step edits
   ssh -o ConnectTimeout=20 dayhoff 'python3 -' < "$SCRATCH/edit.py"      # text edits with exact-match asserts
   ```

   Use `python3 -` and `bash -s` for anything with quotes, loops or regex. Nested
   quoting inside one ssh command fails in confusing ways.
3. **Check the result on Dayhoff**, not on the mount:
   `ssh dayhoff 'sha256sum <file>'` and compare with the local hash of the source.
   For edits, grep or sed-print the changed lines on Dayhoff.
4. **Report** what changed, with paths, and the verification result.

## Other rules

- **Do not pipe into `cat > /dev/null` or any command that reads stdin.** An
  ssh call without a file on stdin will wait forever. This has hung the shell before.
- **Reads and scans** also use ssh. Bound them: named paths, `-maxdepth`, `head`.
  Never run `find /`, or a repo-wide grep on the mount.
- **Deletes and moves** on Dayhoff: list the targets first, check references
  (`grep -rn` over the repo, excluding `output/training`, `data`, `production`),
  then act. For data copies, copy, verify hashes or sizes, and only then remove
  the source.
- **Git:** run git on Dayhoff (`ssh dayhoff 'git -C /home/groups/sequeira/MegaMove_Models ...'`).
  Do not switch branches or commit unless the user asks. If on the default branch,
  create a branch first, as the project's commit rules say.
- **Frozen production files:** before editing any file in
  `scripts/production/frozen-production-code-*.json`, or any file it lists, stop and
  get the user's decision. Changing them changes the next cron job. Check the
  manifest hashes after any change to them.
- **Live job:** the monthly cron job runs from this checkout. Do not start
  `sbatch` or `scancel` as part of an edit. Use `dayhoff-slurm` for job submission.
- **Large data:** `data/`, `production/`, `output/training/`, `output/qc/` and
  `_targets*` are large and not in git. Do not copy, move or delete them without an
  explicit decision on destination and verification.

## Off-repo archive

Cluster-side archive target: decide with the user first. The owner has used a
SanDisk drive on the Mac (`/Volumes/SanDisk Extreme Pro/`). Stream data from
Dayhoff to the Mac with a pipe, not through the mount:

```bash
ssh -o ConnectTimeout=20 dayhoff 'cd /home/groups/sequeira/MegaMove_Models && tar -cf - <paths>' | tar -xf - -C "<destination>"
```

Then compare file counts and hashes before removing anything on Dayhoff.

## Companions

| Need | Skill |
|------|--------|
| SLURM job templates, conda env choice, job monitoring | `dayhoff-slurm` |
| SSH hosts, VPN, ProxyJump | `dahlias-fleet` → `ssh-fleet.md` |
| R code style | `r-human-code` |
