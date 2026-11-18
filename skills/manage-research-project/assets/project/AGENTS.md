# 项目协作

## 入口

- 训练使用 Hydra 和 PyTorch Lightning。先接入 `models/pl_model.py` 和 `datasets/pl_data.py`，再运行 `python train.py`。`python train.py --cfg job` 可预览配置。训练目录取自 `configs/config.yaml`，例如 `python train.py hydra.run.dir=/path/to/run`。启用 W&B 时安装 `wandb`。
- 推理使用 OmegaConf 读取 `configs/sampling.yaml`。在 `inference.py` 实现 `predict`，通过 `python inference.py --input INPUT --output-dir PREDICTIONS` 生成预测。
- 评测在 `eval.py` 实现 `evaluate`。通过 `python eval.py --predictions PREDICTIONS --output-dir METRICS` 重算指标。有参考数据时加 `--reference REFERENCE`。

## 当前进度

- 当前工作：
- 最近验证及依据：
- 待解决或已确认的下一步：
