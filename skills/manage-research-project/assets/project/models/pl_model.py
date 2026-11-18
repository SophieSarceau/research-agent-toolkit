"""Build the model used by the training entry point."""

from omegaconf import DictConfig
from pytorch_lightning import LightningModule


def build_model(cfg: DictConfig) -> LightningModule:
    """Construct the project's LightningModule, including its loss and optimizer."""
    raise NotImplementedError("Implement build_model() with the project's model.")
