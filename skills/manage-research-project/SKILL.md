---
name: manage-research-project
description: 建立或整理使用扁平配置的科研代码仓库。适用于设计训练、推理与评测入口，组织 baseline 和本方法实验，以及维护运行产物和项目进度。
---

# 管理科研代码项目

新项目从 [项目框架](assets/project/) 复制适用的入口、模块和配置。先确定方法是否需要训练，再接入项目自己的数据、方法和评测协议。已有项目按需合并，保留已有命令、配置调用方式和进度。

```text
AGENTS.md
configs/
  config.yaml
  training.yaml
  inference.yaml
  wandb.yaml
train.py                          训练型方法
inference.py                      对输入生成预测或样本
eval.py                           按指定协议给已有预测打分
models/pl_model.py                构造训练使用的 LightningModule
datasets/pl_data.py               构造数据加载与划分使用的 LightningDataModule
utils/                            多处实际复用的工具
baselines/<baseline_name>/        每个对照方法一个目录
experiments/<experiment_name>/    本方法的每项实验一个目录
outputs/                          默认训练运行根目录，启动训练时按配置生成
```

## 入口与配置

- 在 `models/pl_model.py` 接入 LightningModule，在 `datasets/pl_data.py` 接入 LightningDataModule。`train.py` 组合 Hydra 配置、初始化可选的 W&B 日志，再交给 Lightning Trainer 拟合和保存 checkpoint。训练中的 validation 可复用评测逻辑。
- `inference.py` 读取输入及指定的模型或算法参数，写出可按样本 ID 对齐的预测。单样本和批量使用同一预测逻辑。`eval.py` 读取明确指定的预测目录、数据划分和可用参考值，保存指标、分母及失败样本的处理方式。重算指标时直接使用保存的预测。
- [configs/](assets/project/configs/) 采用扁平结构。`config.yaml` 组合配置，定义实验名和训练运行目录。`training.yaml` 分为 `data`、`model`、`train`、`sys` 四节。需要优化器和调度器时，使用 `train.optimizer`、`train.scheduler`。独立推理从 `inference.yaml` 读取 `sample.*` 和可选的 `model.checkpoint`。`wandb.yaml` 保存 `wandb.wandb_*` 日志设置。
- 独立评测通过 `--predictions` 指定已有预测，需要参考值时传入 `--reference`。实验只声明相对默认值的改动。W&B 默认关闭，启用时从本机登录或环境读取凭据。
- **Training-free** 项目直接从推理开始。在新项目中只取 `inference.py`、`eval.py`、`configs/inference.yaml` 和需要的项目目录。若已有 Hydra 主配置且继续使用它，移除闲置的训练 defaults 项。用冻结模型时保留 `model.checkpoint` 或固定的模型标识；纯算法删除权重字段。只有真实拟合参数时才引入训练入口、Lightning Trainer 和优化器。W&B 可独立记录推理和评测，也可一直关闭。
- 每个输入独立进行的搜索、重排序或迭代优化属于推理，记录搜索预算即可。如果在验证集上选阈值或超参数，在对应实验中记下选择依据。跨训练样本学习并复用的参数（如校准器）应有可复现的拟合步骤，即使主模型始终冻结。

## 基线、实验与运行结果

- 一个 baseline 在 `baselines/<baseline_name>/` 维护适配器、必要的配置或上游版本说明。让它产出同一评测入口可读的预测，比较时明确数据划分、预算和失败样本规则。
- 本方法的一项消融、敏感性分析或主实验在 `experiments/<experiment_name>/` 保留研究问题、复现命令或必要覆盖参数。例如 `experiments/without_reranking/` 表示“去掉重排序”；不同种子是该实验的多次运行。将通用实现放回本方法模块，避免复制整套方法或配置。
- 项目维护的 Python 文件和子目录用有含义的 `snake_case`。禁止用 `v1`、`v2`、`final_final` 等命名方法迭代、脚本、配置或实验目录。迭代沿用原名，由 Git 提交记录；需同时比较的变体按实际机制命名。引用外部模型、数据集版本时保留其正式标识。
- **训练目录由配置决定。** 单次运行使用 `configs/config.yaml` 的 `hydra.run.dir`，默认展开为 `outputs/YYYY-MM-DD/HH-MM-SS-<experiment_name>/`。批量运行使用 `hydra.sweep.dir` 和 `hydra.sweep.subdir`。训练代码从 `HydraConfig.get().runtime.output_dir` 取得最终路径，checkpoint、Hydra 配置快照、日志及启用的 W&B 本地文件都随该路径走。保持 `hydra.job.chdir: false`。
- **预测和指标各自指定去向。** 独立调用 `inference.py`、`eval.py` 时分别传入 `--output-dir`。记录预测所用权重、配置和评测所读的预测路径，保留可复现结果所需的 Git 提交与覆盖参数。

## 收尾与交接

在任务结束前核对 `git status` 和任务产生的文件。临时日志、一次性诊断脚本、临时测试及其缓存用完即清理，适合时直接在临时目录运行。可重复使用的回归测试集中在 `tests/`，能复现实验的脚本归对应实验。保留用户文件、正在使用的运行目录、论文结果及其复现依据。忽略规则只管理 Git 可见性，不能当作删除依据。

有实质进展时，原地更新目标项目 [AGENTS.md](assets/project/AGENTS.md) 的进度区：当前工作、最近一次有依据的结果、待解决的问题或已确认的下一步。覆盖失效条目，引用提交或产物路径；详细历史交给 Git，逐次指标留在运行目录。只有实际完成的验证才能写成已验证。

整理完成后，用 `python train.py --cfg job` 核对训练配置，用两个独立入口的 `--help` 核对参数。接入具体实现后，用小样本检查预测与评测的衔接，并检查训练目录覆盖是否生效。
