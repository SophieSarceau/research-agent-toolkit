# Research Agent Toolkit

Personal Codex instructions and a home for reusable skills for managing research code.

## Using the coding guidelines

[AGENTS.md](AGENTS.md) contains shared defaults for implementation decisions, experimental protocol changes, and verification.

To use these defaults across local projects, merge the relevant sections into `~/.codex/AGENTS.md`. To use them in a single repository, merge them into its root `AGENTS.md`. Keep project-specific details there, including training entry points, evaluation commands, and dataset conventions.

## Adding skills

[Manage a research project](skills/manage-research-project/SKILL.md) covers the repository layout, Hydra configurations, baselines, experiments, and run artifacts for trained and training-free methods. It includes a [code-free project template](skills/manage-research-project/assets/project/).

Store each reusable workflow in `skills/<skill-name>/SKILL.md`. Give it a name and a description that says when to use it. To enable a skill in a research project, copy its directory into that project's `.agents/skills/` directory.
