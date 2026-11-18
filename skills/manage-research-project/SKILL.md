---
name: manage-research-project
description: 按 Apo2Mol 的配置习惯建立或整理科研代码仓库。适用于设计训练、推理与评测入口，组织 baseline 和本方法实验，以及维护运行产物和项目进度。
---

# 管理科研代码项目

新项目从 [项目骨架](assets/project/) 取需要的文件。已有项目先核对公开命令、配置及其调用者，合并适用的约定，保留已有进度。用户只要架构时，交付目录和配置即可。下图中的 Python 文件是实现阶段的入口约定。

```text
AGENTS.md
configs/
  config.yaml
  training.yaml
  sampling.yaml
  wandb.yaml
train.py                          训练型方法
inference.py                      对输入生成预测或样本
eval.py                           按指定协议给已有预测打分
models/                           本方法实现，按需建立
datasets/                         数据读取、变换和划分逻辑
utils/                            多处实际复用的工具
baselines/<baseline_name>/        每个对照方法一个目录
experiments/<experiment_name>/    本方法的每项实验一个目录
outputs/                          首次运行时生成
```

## 入口与配置

- 训练型项目用 `train.py` 负责拟合、验证和保存 checkpoint。PyTorch Lightning 管训练循环，Hydra 组合配置，W&B 按配置记录实验。训练中的 validation 可复用评测逻辑。
- `inference.py` 读取输入及指定的模型或算法参数，写出可按样本 ID 对齐的预测。单样本和批量使用同一预测逻辑。`eval.py` 读取明确指定的预测目录、数据划分和可用参考值，保存指标、分母及失败样本的处理方式。重算指标时直接使用保存的预测。
- 保持 [configs/](assets/project/configs/) 扁平。`config.yaml` 负责 Hydra defaults、`experiment_name` 和运行目录。`training.yaml` 沿用顶层 `data`、`model`、`train`、`sys`，优化器和调度器需要时放在 `train.optimizer`、`train.scheduler`。推理配置沿用 `sampling.yaml`、`sample.*` 和可选的 `model.checkpoint`。`wandb.yaml` 沿用 `wandb.wandb_*` 字段。入口文件名可以是 `inference.py`，配置仍叫 `sampling.yaml`。
- 评测优先复用已有配置和实验协议。需要可配置的独立评测参数时，在 `config.yaml` 加小型 `eval` 节；有现成项目约定时沿用它。实验只声明相对默认值的改动。W&B 默认关闭，启用时从本机登录或环境读取凭据。
- **Training-free** 项目直接从推理开始。在骨架中移除 `training.yaml` 及其 defaults 项，保留有用的 `inference.py`、`eval.py`、Hydra 和实验目录。推理与评测共享的数据路径或划分可移至 `config.yaml` 的 `data` 节。用冻结模型时保留 `model.checkpoint` 或固定的模型标识；纯算法删除权重字段。只有真实拟合参数时才引入训练入口、Lightning Trainer 和优化器。W&B 可独立记录推理和评测，也可一直关闭。
- 每个输入独立进行的搜索、重排序或迭代优化属于推理，记录搜索预算即可。如果在验证集上选阈值或超参数，在对应实验中记下选择依据。跨训练样本学习并复用的参数（如校准器）应有可复现的拟合步骤，即使主模型始终冻结。

## 基线、实验与运行结果

- 一个 baseline 在 `baselines/<baseline_name>/` 维护适配器、必要的配置或上游版本说明。让它产出同一评测入口可读的预测，比较时明确数据划分、预算和失败样本规则。
- 本方法的一项消融、敏感性分析或主实验在 `experiments/<experiment_name>/` 保留研究问题、复现命令或必要覆盖参数。例如 `experiments/without_reranking/` 表示“去掉重排序”；不同种子是该实验的多次运行。将通用实现放回本方法模块，避免复制整套方法或配置。
- 项目维护的 Python 文件和子目录用有含义的 `snake_case`。禁止用 `v1`、`v2`、`final_final` 等命名方法迭代、脚本、配置或实验目录。迭代沿用原名，由 Git 提交记录；需同时比较的变体按实际机制命名。引用外部模型、数据集版本时保留其正式标识。
- 各入口把产物写入 Hydra 分配的本次运行目录，沿用 `outputs/YYYY-MM-DD/HH-MM-SS-<experiment_name>/` 和 `hydra.job.chdir: false`。训练放 checkpoint，推理放预测，评测放指标。日志、W&B 本地文件和可视化也指向本次运行目录。评测记录所读预测路径，各次运行保留配置、覆盖参数和 Git 提交号（含未提交修改状态）。同秒并发时用明确的任务名或调度器作业号避开重名；Hydra sweep 用作业子目录。

## 收尾与交接

在任务结束前核对 `git status` 和任务产生的文件。临时日志、一次性诊断脚本、临时测试及其缓存用完即清理，适合时直接在临时目录运行。可重复使用的回归测试集中在 `tests/`，能复现实验的脚本归对应实验。保留用户文件、正在使用的运行目录、论文结果及其复现依据。忽略规则只管理 Git 可见性，不能当作删除依据。

有实质进展时，原地更新目标项目 [AGENTS.md](assets/project/AGENTS.md) 的进度区：当前工作、最近一次有依据的结果、待解决的问题或已确认的下一步。覆盖失效条目，引用提交或产物路径；详细历史交给 Git，逐次指标留在运行目录。只有实际完成的验证才能写成已验证。

整理完项目后，按所选模式核对入口与 defaults 是否一致、配置能否组合、预测能否被评测消费，以及运行后仓库根目录是否整洁。只有文档与配置时，验证到配置组合为止。

架构取自 [Apo2Mol 的目录与入口](https://github.com/AIDD-LiLab/Apo2Mol/tree/549be4f0273179ebfe9d8a12b60ab02bd2c85b9c)。原项目训练写入 `outputs/`，采样与评测另用 `sampled_results/`、`eval_results/`。这里将三者统一到同一产物根目录。
