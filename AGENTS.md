# AGENTS.md

## Working with the user

- Use the relevant code, configs, tests, and documentation to resolve routine questions. Follow established project conventions for reversible implementation choices. State assumptions that affect the result.
- Ask when plausible interpretations would materially change the deliverable or the meaning of an experiment. Get explicit approval before changing the method's model architecture (layers, modules, inputs, or outputs) or the code structure (module boundaries, public interfaces, entry-point arguments, or directory layout). Refactoring that leaves these unchanged does not need approval.
- Preserve the agreed experimental protocol. If a proposed fix would change the data split, training objective, evaluation metric, or sample inclusion rules, explain the effect and confirm the intended behavior before proceeding.

## Changing code

- Make the smallest complete change that solves the requested problem. Follow local style, reuse existing logic where it fits, and keep unrelated cleanup out of the change.
- Prefer code that a collaborator can inspect against the method description. Make units, tensor dimensions, masking, and aggregation explicit where they affect correctness.
- Preserve behavior that existing callers and experiments rely on, except where the request calls for a change. Remove anything your own change makes obsolete.

## Research protocol

- Use the same predictor for single and batch inputs and save a stable ID with each prediction. Report each metric with its denominator and how failed samples were counted.
- When comparing with baselines, state the split and budget each method used.
- For training-free methods, treat per-input search, reranking, or iterative optimization as inference and record its budget. Document how any threshold or hyperparameter chosen on a validation split was selected. Give parameters learned across examples, such as a calibrator, a reproducible fitting step.

## Verifying work

- For work spanning several components or involving a consequential tradeoff, give a brief plan and say how you will check the outcome.
- Verify the change through the entry point the project actually uses. For a bug fix, check the original failure case when feasible. For a numerical change, use a case with a known expected result when available.
- Report which checks you ran, what they established, and what remains unverified. Distinguish a successful smoke test from a reproduced experimental result.
