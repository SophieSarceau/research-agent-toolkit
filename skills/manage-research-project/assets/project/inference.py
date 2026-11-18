"""Generate predictions for new inputs using the project's inference configuration."""

import argparse
from pathlib import Path

from omegaconf import DictConfig, OmegaConf

from utils.run_record import write_run_record


def predict(inputs: Path, output_dir: Path, config: DictConfig) -> None:
    """Write predictions with stable sample IDs to output_dir."""
    raise NotImplementedError("Implement the project's prediction method in predict().")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Input file or directory")
    parser.add_argument("--output-dir", type=Path, required=True, help="Prediction directory")
    parser.add_argument(
        "--config", type=Path, default=Path(__file__).parent / "configs" / "inference.yaml"
    )
    parser.add_argument("overrides", nargs="*", help="Config overrides such as model.checkpoint=PATH")
    args = parser.parse_args()
    config = OmegaConf.merge(OmegaConf.load(args.config), OmegaConf.from_dotlist(args.overrides))
    write_run_record(args.output_dir)
    OmegaConf.save(config, args.output_dir / "config.yaml")
    predict(args.input, args.output_dir, config)


if __name__ == "__main__":
    main()
