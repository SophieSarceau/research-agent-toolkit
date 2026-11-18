"""Build the data module used by the training entry point."""

from omegaconf import DictConfig
from pytorch_lightning import LightningDataModule


def build_datamodule(cfg: DictConfig) -> LightningDataModule:
    """Construct the data loaders using the project's data and split configuration."""
    raise NotImplementedError("Implement build_datamodule() with the project's dataset.")
