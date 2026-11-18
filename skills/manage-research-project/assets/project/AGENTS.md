# Working on this project

Keep `README.md` accurate for the current checkout. Update the project's description, status, features, or usage in place whenever they change. Keep version history and comparisons with earlier versions in Git.

## Directory layout

- The root holds project documentation, repository metadata, and the applicable `train.py`, `inference.py`, and `eval.py` entry points.
- `configs/` holds flat configuration files. `models/` holds model code, `datasets/` holds data loading and split logic, and `utils/` holds helpers shared across modules.
- `baselines/<baseline_name>/` holds one baseline's adapter and configuration. `experiments/<experiment_name>/` holds one experiment's overrides, reproduction command, and any launcher it needs.
- `tests/` holds reusable regression tests. Run one-off checks in a temporary directory outside the repository.
- Training artifacts go to the Hydra run directory, under `outputs/` by default. Standalone inference and evaluation each write to their explicit `--output-dir`.

## Entry points

- **Train.** Implement the model in `models/pl_model.py` and the data module in `datasets/pl_data.py`. Preview the Hydra configuration with `python train.py --cfg job`, then run `python train.py`. Set the training directory in `configs/config.yaml` or override it with `python train.py hydra.run.dir=/path/to/run`. Install `wandb` if tracking is enabled.
- **Infer.** Implement `predict` in `inference.py`. Read settings such as `inference.seed` from `configs/inference.yaml`. Run `python inference.py --input INPUT --output-dir PREDICTIONS`.
- **Evaluate.** Implement `evaluate` in `eval.py`. Run `python eval.py --predictions PREDICTIONS --output-dir METRICS` to score saved predictions. Add `--reference REFERENCE` when the metric needs reference data.

## Current progress

- Current work:
- Latest verified result and evidence:
- Open question or agreed next step:
