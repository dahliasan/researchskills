# Human-editable run configuration

Read when collaborators need to change recurring analysis settings, or when a batch
runner needs to select an analysis configuration.

## Start with the smallest interface

Start with plain assignments near the top of the script. They are the preferred
interface when collaborators can readily change the settings they need there. Add a
configuration file only when collaborators repeatedly change a coherent set of choices,
such as a species, model form, resampling settings, or thresholds, and those assignments
are no longer a usable interface. A readable YAML file is often a good fit when the
project already uses, or can deliberately add, the `yaml` package.

```yaml
species: turtle
folds: 3
seed: 42
model: dynamic
min_years: 6
```

Load it near the script settings so the selected choices remain easy to inspect:

```r
config <- yaml::read_yaml("config.yml")
```

Use names that describe analysis decisions. Preserve value types, missing-value
semantics, units, and established project paths. Add validation only for constraints
the workflow is designed to enforce or that have caused real failures.

## Connect Bash automation without duplicating settings

For an interactive collaborator workflow, the config file is the run interface: edit it
and source the analysis in RStudio. Use `docopt` only when an established Bash, HPC, or
pipeline caller also needs to select runs. That interface should provide the config path:

```bash
Rscript run.R --config=config.yml
```

Do not add `commandArgs()` to create this interface. Keep an existing `docopt`
interface when its callers require it. For a new configured workflow, do not mirror
every config value as a separate command-line flag unless those values genuinely vary
independently for callers.
