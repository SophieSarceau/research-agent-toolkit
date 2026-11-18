"""Evaluate saved predictions under the project's evaluation protocol."""

import argparse
from pathlib import Path
from typing import Optional

from utils.run_record import write_run_record


def evaluate(predictions: Path, reference: Optional[Path], output_dir: Path) -> None:
    """Read predictions and write metrics for the selected samples to output_dir."""
    raise NotImplementedError("Implement the project's scoring protocol in evaluate().")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions", type=Path, required=True, help="Saved predictions")
    parser.add_argument("--reference", type=Path, help="Reference data for supervised metrics")
    parser.add_argument("--output-dir", type=Path, required=True, help="Metric directory")
    args = parser.parse_args()
    write_run_record(args.output_dir)
    evaluate(args.predictions, args.reference, args.output_dir)


if __name__ == "__main__":
    main()
