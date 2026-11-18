#!/usr/bin/env bash
# Run from the repository root: bash experiments/<category>/<experiment_name>/run.sh [seed]
# Keep only the steps the method needs and add this experiment's overrides to each command.
set -euo pipefail

category="<category>"
name="<experiment_name>"
seed=${1:-0}
run_dir=outputs/${category}/${name}/seed_${seed}

python train.py experiment_name="${name}" train.seed="${seed}" \
  hydra.run.dir="${run_dir}/train"

python inference.py --input "<input>" --output-dir "${run_dir}/predictions" \
  model.checkpoint="${run_dir}/train/checkpoints/last.ckpt" inference.seed="${seed}"

python eval.py --predictions "${run_dir}/predictions" --output-dir "${run_dir}/metrics"
