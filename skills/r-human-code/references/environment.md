# Project environment

Read when changing dependencies, credentials, R versions, or environment setup.

Respect existing project activation and `renv.lock`. For maintained shared analyses,
prefer the project's established reproducibility mechanism. Install or restore once
during setup; do not install packages from analysis scripts.

A package lockfile does not install R itself or system libraries. Record environment
requirements where the project already documents them.

Keep secrets out of version control and out of logs. Use actual project requirements,
not hypothetical deployment machinery.
