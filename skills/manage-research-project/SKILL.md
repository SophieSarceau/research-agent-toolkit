---
name: manage-research-project
description: Set up or maintain a research code repository with a project-local Python environment and flat configuration files. Use this skill to organize training, inference, evaluation, baselines, experiments, run artifacts, and project progress.
---

# Manage a research code project

For a new project, decide whether the method fits parameters. Copy the relevant version-controlled files from the [project template](assets/project/) and implement the project's data, method, and evaluation protocol. For an existing repository, preserve commands, configuration overrides, and progress records that researchers already use.

```text
AGENTS.md                         Entry points and current progress
configs/
  config.yaml
  training.yaml
  inference.yaml
  wandb.yaml
train.py                          Fit model parameters
inference.py                      Generate predictions or samples for new inputs
eval.py                           Score saved predictions under a specified protocol
models/pl_model.py                Build the LightningModule used for training
datasets/pl_data.py               Build the LightningDataModule for loading and splitting data
utils/                            Utilities shared across modules
baselines/<baseline_name>/        One directory per comparison method
experiments/<experiment_name>/    One directory per experiment on the proposed method
outputs/                          Default training directory, created when training starts
```

## Python environment

Create or update an environment in the target research project's root only when the task calls for setup or execution. When editing this skill, its templates, or documentation, leave the toolkit and template directories free of environments, generated lockfiles, and installed packages.

- Follow the target project's existing dependency manager and lockfile. For a new Python project, prefer uv with a project-local `.venv/`. Python 3.12 is a starting point if the required libraries support it. Track the Python requirement and direct dependencies in `pyproject.toml`, commit `uv.lock`, and ignore `.venv/` in the target project. Recreate a locked environment there with `uv sync --locked`.
- If the project relies on Conda for native libraries, use a project-local Conda prefix such as `./.conda/` and keep the environment specification in Git. Leave the system Python, Conda base, and other projects' environments untouched.
- Install dependencies for the work the project actually performs. Training-free methods need their inference and evaluation libraries. Add Lightning for training and W&B when tracking is used. When PyTorch is required on a GPU server, select its build for that server's accelerator and driver. [PyTorch installation guide](https://pytorch.org/get-started/locally/)

## Entry points and configuration

- Implement the LightningModule in `models/pl_model.py` and the LightningDataModule in `datasets/pl_data.py`. The training entry point composes the Hydra configuration, sets up optional W&B logging, and calls the Lightning Trainer to fit the model and save checkpoints. Validation during training can reuse evaluation logic.
- Use the same prediction logic for single inputs and batches. Write a stable sample ID with each prediction. Give the evaluator the prediction directory, the split to score, and any references the metric needs. Report the metric, its denominator, and how failures were counted. Reuse saved predictions when recomputing metrics.
- Keep [configuration files](assets/project/configs/) in one directory. `config.yaml` composes the files and defines the experiment name and training run directory. In `training.yaml`, use the sections `data`, `model`, `train`, and `sys`. Use `train.optimizer` and `train.scheduler` when needed. Standalone inference reads `inference.*` (for example, `inference.seed`) and the optional `model.checkpoint` from `inference.yaml`. Keep W&B settings under `wandb.wandb_*` in `wandb.yaml`.
- Pass saved predictions to the evaluator with `--predictions` and reference data with `--reference` when needed. Record only the settings each experiment overrides. W&B is disabled by default. When enabled, use credentials from the local login or environment.

### Training-free methods

Start with `inference.py`, `eval.py`, `configs/inference.yaml`, and the directories the method needs. If retaining an existing Hydra entry point, remove unused training entries from its defaults list. For a frozen model, record the checkpoint or a fixed model identifier. For an algorithm without weights, remove the checkpoint field. Add a training entry point, Trainer, and optimizer only when the method fits parameters. W&B can optionally log inference and evaluation.

Treat per-input search, reranking, or iterative optimization as inference and record the budget. If an experiment chooses a threshold or hyperparameter on a validation split, document the selection criterion. If parameters such as a calibrator are learned across examples and reused, provide a reproducible fitting step even when the main model stays frozen.

## Baselines, experiments, and outputs

- Keep each baseline's adapter, required configuration, and upstream revision in `baselines/<baseline_name>/`. Produce predictions that the shared evaluator can read. State the split, budget, and failure-handling rules used in comparisons.
- Give each main experiment, ablation, or sensitivity analysis its own `experiments/<experiment_name>/` directory. Keep its research question, reproduction command, and overrides there. For example, `experiments/without_reranking/` can cover several random seeds. Keep shared implementation in the method's modules.
- Use descriptive `snake_case` for project-owned Python files and directories. Keep filenames stable and record iterations in Git. Never use version suffixes such as `v1`, `v2`, or `final_final` for methods, scripts, configs, or experiments. Name variants that must coexist after the mechanism they change. Preserve official version identifiers for external models and datasets.
- For a single training run, Hydra resolves `hydra.run.dir` from `configs/config.yaml`. The default is `outputs/YYYY-MM-DD/HH-MM-SS-<experiment_name>/`. For a sweep, use `hydra.sweep.dir` and `hydra.sweep.subdir`. Read the final directory from `HydraConfig.get().runtime.output_dir` and place checkpoints, the Hydra configuration snapshot, logs, and local W&B files there. Keep `hydra.job.chdir: false`.
- For standalone inference and evaluation, pass an explicit `--output-dir` to each command. Record the weights and configuration used to predict, the prediction path used for scoring, and the Git commit and overrides needed to reproduce the result.

## Before adding a script

The research repository root must never contain a `scripts/` directory. Place each maintained file with the test, experiment, baseline, or module that owns it. Before adding a script, check whether an existing command already does the job.

| Purpose | Where it belongs |
| --- | --- |
| Run training, inference, or evaluation with different arguments | Reuse the existing entry point. Record the command or config overrides with the experiment. Changing a seed or checkpoint does not need a Python wrapper. |
| Reproduce a specific experiment or run a baseline | Keep a launcher in `experiments/<experiment_name>/` or an adapter in `baselines/<baseline_name>/` only when it performs necessary work beyond passing arguments. |
| Check a lasting behavior | Add a focused test in `tests/` when it can detect a specific regression. A check that only prints a value for inspection can run interactively. |
| Diagnose a failure or perform a one-time check | Use an inline command or a temporary directory outside the repository. Remove any scratch files the task created. |

## Cleanup and handoff

Before finishing, run `test ! -d ./scripts` from the repository root. Check `git status --short --untracked-files=all` and review each new script against the table above. Remove the task's temporary logs, scratch files, and caches. Preserve user files, active runs, paper results, and their reproduction evidence. An ignore rule alone does not establish that a file is safe to delete.

When progress changes, update the existing progress section in the project's [AGENTS.md](assets/project/AGENTS.md). State the current work, latest verified result and its evidence, and an open question or agreed next step. Replace stale entries and link to the relevant commit or artifact. Keep detailed history in Git and per-run metrics in the run directory.

Preview the training configuration with `python train.py --cfg job` and check the arguments of each standalone entry point with `--help`. Once the project implements its method, run a small input through inference and evaluation. For training, verify that a run-directory override puts artifacts in the requested location.
