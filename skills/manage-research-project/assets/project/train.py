"""Fit a project model in the run directory selected by Hydra."""

from pathlib import Path

import hydra
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig


@hydra.main(version_base="1.3", config_path="configs", config_name="config")
def main(cfg: DictConfig) -> None:
    from pytorch_lightning import Trainer, seed_everything
    from pytorch_lightning.callbacks import ModelCheckpoint

    from datasets.pl_data import build_datamodule
    from models.pl_model import build_model

    run_dir = Path(HydraConfig.get().runtime.output_dir)
    seed_everything(cfg.train.seed, workers=True)
    model = build_model(cfg)
    data = build_datamodule(cfg)

    tracking = cfg.wandb
    logger = False
    if tracking.wandb_status in ("online", "offline"):
        from pytorch_lightning.loggers import WandbLogger

        logger = WandbLogger(
            project=tracking.wandb_project,
            entity=tracking.wandb_entity,
            name=tracking.wandb_task,
            save_dir=str(run_dir),
            offline=tracking.wandb_status == "offline",
        )
    elif tracking.wandb_status != "disabled":
        raise ValueError("wandb.wandb_status must be disabled, offline or online.")

    trainer = Trainer(
        default_root_dir=str(run_dir),
        callbacks=[ModelCheckpoint(dirpath=run_dir / "checkpoints", save_last=True)],
        logger=logger,
        max_epochs=cfg.train.max_epochs,
        accelerator=cfg.sys.accelerator,
        devices=cfg.sys.devices,
    )
    trainer.fit(model, datamodule=data)


if __name__ == "__main__":
    main()
