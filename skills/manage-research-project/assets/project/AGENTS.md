# Working on this project

This file holds project-specific instructions. Where it differs from the `manage-research-project` skill, this file takes precedence.

## Files

- Place every new file according to the file table in `.agents/skills/manage-research-project/SKILL.md`. Ask before adding other top-level files or directories.
- Run one-line checks inline. Put other one-off scripts, diagnostics and debug logs in `scratch/`, which may be deleted at any time; nothing may depend on it. Write run artifacts only under `outputs/`.
- Keep `README.md` accurate for the current checkout. Update its description, status, features or usage in place, and keep version history in Git.

## Entry points

- **Train.** Implement the model in `models/pl_model.py` and the data module in `datamodules/pl_data.py`. Preview the Hydra configuration with `python train.py --cfg job`, then run `python train.py`. Override the run directory with `python train.py hydra.run.dir=outputs/<path>`. Install `wandb` if tracking is enabled.
- **Infer.** Implement `predict` in `inference.py`. Settings come from `configs/inference.yaml` and can be overridden as `key=value`: `python inference.py --input INPUT --output-dir outputs/<path> model.checkpoint=CHECKPOINT`.
- **Evaluate.** Implement `evaluate` in `eval.py`. Run `python eval.py --predictions PREDICTIONS --output-dir outputs/<path>` to score saved predictions. Add `--reference REFERENCE` when the metric needs reference data.
- **Experiment.** Run `bash experiments/<category>/<experiment_name>/run.sh [seed]` from the repository root.

## Current progress

- Current work:
- Latest verified result and evidence:
- Open question or agreed next step:
