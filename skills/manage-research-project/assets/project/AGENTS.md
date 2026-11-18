# Working on this project

## Entry points

- **Train.** Implement the model in `models/pl_model.py` and the data module in `datasets/pl_data.py`. Preview the Hydra configuration with `python train.py --cfg job`, then run `python train.py`. Set the training directory in `configs/config.yaml` or override it with `python train.py hydra.run.dir=/path/to/run`. Install `wandb` if tracking is enabled.
- **Infer.** Implement `predict` in `inference.py`. Read settings such as `inference.seed` from `configs/inference.yaml`. Run `python inference.py --input INPUT --output-dir PREDICTIONS`.
- **Evaluate.** Implement `evaluate` in `eval.py`. Run `python eval.py --predictions PREDICTIONS --output-dir METRICS` to score saved predictions. Add `--reference REFERENCE` when the metric needs reference data.

## Current progress

- Current work:
- Latest verified result and evidence:
- Open question or agreed next step:
