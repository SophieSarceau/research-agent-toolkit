---
name: manage-research-project
description: Keep a research code repository organized so that code, experiments and results stay easy to find. Use when setting up a research project; adding a model, dataset, baseline or experiment; launching runs; or before finishing any task that created files in such a repository.
---

# Manage a research code project

Every file in the project belongs to one row of the table below. Do not create a file that fits no row; ask the user before adding a new kind of file. The project's `AGENTS.md` overrides this skill where they differ.

Start a new project from the [project template](assets/project/) and copy only what the method needs. Training-free methods omit `train.py`, `models/pl_model.py`, `datamodules/pl_data.py`, and `configs/training.yaml` with its defaults entry. In an existing repository, apply the table to new files and keep the current layout, commands and overrides. Reorganize existing files only when the user asks.

| Kind | Location | Git |
| --- | --- | --- |
| Entry points | `train.py`, `inference.py`, `eval.py` at the root | tracked |
| Method code | `models/`, `datamodules/`, `utils/` | tracked |
| Configuration | flat files in `configs/` | tracked |
| Baseline | `baselines/<baseline_name>/`: adapter, config, upstream revision | tracked |
| Experiment | `experiments/<category>/<experiment_name>/`: `README.md`, `run.sh`, analysis code used only by this experiment | tracked |
| Regression test | `tests/` | tracked |
| Documentation | `README.md` and `AGENTS.md` only | tracked |
| Repository metadata | `.gitignore`, `pyproject.toml`, lockfile, license | tracked |
| Environment | `.venv/` or another project-local environment | ignored |
| Data | `data/`, or an external path set in config | ignored |
| Run artifacts | `outputs/` | ignored |
| Scratch | `scratch/` | ignored |

Name experiment categories by the question they answer, such as `training/`, `benchmark/`, `case_study/`, `ablation/` or `sensitivity/`. Small files that define the protocol, such as split lists, may be added to Git with `git add -f`.

## Placing files

- **Outputs mirror experiments.** Start each experiment from the [experiment template](assets/experiment/). Its `run.sh` calls the entry points in order and writes to `outputs/<category>/<experiment_name>/seed_<seed>/`, through `hydra.run.dir` for training and `--output-dir` for inference and evaluation. Runs outside an experiment use Hydra's dated default under `outputs/`. Code writes only to the run directory or the given `--output-dir`, never to paths relative to the working directory.
- **Scratch is disposable.** Run a check as a one-line command when it needs no file. Otherwise put one-off scripts, diagnostics, debug logs and quick plots in `scratch/`. Anything in `scratch/` may be deleted at any time, so no code, experiment or record may depend on it. Move anything worth keeping to its row of the table: a regression check to `tests/`, a shared helper to its module, an analysis to its experiment.
- **One home for each record.** An experiment's question, setup, status, runs and conclusion go in its `README.md`. The entry points save the command, Git commit and uncommitted-change flag to `run.json` in their output directory. The progress section of `AGENTS.md` links to experiments instead of repeating their results. Put task summaries and plans in your reply, not in new files.
- **One evaluator.** Baselines write predictions that `eval.py` can score, and `eval.py` scores saved predictions. Do not add per-baseline evaluation scripts.
- **No environments or secrets in Git.** Create an environment only in the target project, and only when the task needs one. Read W&B and other credentials from the local login or environment variables.

## Naming and iteration

- Use descriptive `snake_case`. Change files in place and let Git hold their history. Never name iterations `v1`, `v2`, `new` or `final_final`. Name variants that must coexist after the mechanism they change. Keep official version identifiers of external models and datasets.
- Do not delete an experiment that failed or was superseded. Record its status and conclusion in its `README.md`.

## Before finishing

- Run `git status --short --untracked-files=all`. Every listed path must belong to a tracked row of the table. Move anything else you created into its place or into `scratch/`.
- Do not delete files you did not create, anything under `outputs/` or `data/`, or files a running job uses. Being ignored by Git does not make a file disposable.
- Update `README.md` in place when the project's purpose, status, features or usage change. Keep release notes and comparisons with earlier versions out of it.
- Update the `AGENTS.md` progress section when the current work, latest verified result or next step changes.
