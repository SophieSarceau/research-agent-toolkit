# Research Agent Toolkit

Personal Codex instructions and a home for reusable skills for managing research code.

## Using the coding guidelines

[AGENTS.md](AGENTS.md) contains shared defaults for implementation decisions, experimental protocol and reporting, and verification.

To use these defaults across local projects, merge the relevant sections into `~/.codex/AGENTS.md`. To use them in a single repository, merge them into its root `AGENTS.md`. Keep project-specific details there, including training entry points, evaluation commands, and dataset conventions.

## Skills

[Manage a research project](skills/manage-research-project/SKILL.md) gives every file in a research repository one place, so that code, experiments and results stay easy to find. The [Python project template](skills/manage-research-project/assets/project/) includes training, inference and evaluation entry points, Lightning model and data interfaces, and flat Hydra configuration files. The [experiment template](skills/manage-research-project/assets/experiment/) provides an experiment record and a launcher.

## Adding skills

Store each reusable workflow in `skills/<skill-name>/SKILL.md`. Give it a name and a description that says when to use it. To enable a skill in a research project, copy its directory into that project's `.agents/skills/` directory.
