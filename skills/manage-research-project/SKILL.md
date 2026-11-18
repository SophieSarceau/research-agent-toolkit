---
name: manage-research-project
description: Set up or maintain research code repositories with training, inference, evaluation, baselines, and reproducible experiments.
---

# Manage a research code project

Start from the [project template](assets/project/) and copy only what the method needs. Follow its [entry points](assets/project/AGENTS.md#entry-points) and [flat config filenames and keys](assets/project/configs/). Preserve existing commands, overrides, and progress records.

## Methods and runs

- Use `train.py` with Hydra and Lightning when the method fits parameters. Keep optimizer and scheduler settings under `train.optimizer` and `train.scheduler`. W&B is optional and disabled by default. Use local credentials when enabled.
- Training-free projects start with `inference.py`, `eval.py`, and `configs/inference.yaml` (`inference.*`). Omit unused training defaults. Record a frozen model's checkpoint or identifier. Omit the checkpoint for methods without weights. Record per-input search budgets, validation-based parameter choices, and any steps that fit parameters across examples.
- Use Hydra's resolved run directory for training checkpoints, config snapshots, and logs, including local W&B files. `configs/config.yaml` sets the default under `outputs/` and controls sweep paths. Keep `hydra.job.chdir: false`.
- Give standalone inference and evaluation their own explicit `--output-dir`. Use the same predictor for single and batch inputs, save stable sample IDs, and score saved predictions. Record the weights, config, split, denominator, and treatment of failed samples.

## Project environment

Set up dependencies only in the target research project when execution or setup requires them. Keep environments and generated lockfiles out of the toolkit and its templates. Follow the project's dependency manager. For new projects, prefer uv, a local `.venv/`, and Python 3.12 if compatible. Commit `pyproject.toml` and `uv.lock`. For Conda, use a local prefix and track its specification. Ignore environment directories. Install only the dependencies used and match PyTorch to the target accelerator and driver.

## Files and experiments

- Use the [project directory layout](assets/project/AGENTS.md#directory-layout) to place each file by purpose. Reserve root-level Python commands for training, inference, and evaluation. Reuse those entry points when only the arguments change.
- Keep each baseline's adapter, config, and upstream revision in `baselines/<baseline_name>/`. Compare through the same evaluator and state each baseline's split and budget.
- Keep each experiment's question, reproduction command, and config overrides in `experiments/<experiment_name>/`. Put a necessary launcher there. Keep shared method code in its owning module and record the Git commit with results.
- Use descriptive `snake_case` names. Never name iterations `v1`, `v2`, or `final_final`. Use Git for revisions, name coexisting variants by mechanism, and retain official external version identifiers.

## Before finishing

- Update `README.md` in place when the project's purpose, status, features, or usage changes. Verify affected examples. Keep release notes, past-version descriptions, and version comparisons out of the README.
- Keep only the current work, latest verified result with evidence, and an open question or agreed next step in the `AGENTS.md` progress section.
- Check the relevant entry points. For training changes, verify configuration composition and the run-directory override. For prediction or scoring changes, pass a small input through inference and evaluation once implemented.
- Run `git status --short --untracked-files=all` and check that each new file belongs in its directory. Remove temporary logs, diagnostics, and caches created by the task. Preserve user files, active runs, and evidence needed to reproduce results.
