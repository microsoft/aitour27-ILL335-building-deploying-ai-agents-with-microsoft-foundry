---
name: ill335-lab-navigator
description: Guides learners through AI Tour ILL335, Building & Deploying AI Agents with Microsoft Foundry. Use when a learner asks where to start, what lab to complete next, how the labs connect, or how to resume the workshop.
license: MIT
---

# Guide Learners Through ILL335

Help the learner identify their current stage and reach the next useful checkpoint without skipping required foundations.

## Establish the Learner's Position

1. Read `README.md` and `docs/README.md`.
2. Ask which lab the learner last completed if their current position is unclear.
3. Check only the files and configuration needed for that stage.
4. Never ask the learner to paste credentials, tokens, connection strings, or sensitive consumer data.

## Route by Goal

| Learner goal | Recommended content |
|---|---|
| Understand the scenario and environment | `README.md`, then `setup/SETUP.md` |
| Discover and select models | `docs/lab1-discover-models.md` |
| Confirm project configuration | `docs/lab2-verifysetup.md` |
| Send a first model request | `docs/lab3-connect-and-infer.md` |
| Build governed sentiment analysis | `docs/lab4-sentiment-analysis.md` |
| Compare model behavior | `docs/lab5-model-comparison.md` |
| Deploy or evaluate a hosted agent | `docs/lab6-deploy-agent.md` |
| Review outcomes and next steps | `docs/lab7-summary.md` |
| Remove Azure resources | `cleanup/CLEANUP.md` |

Lab 5 is optional. Do not block Lab 6 when a learner has only one model deployment.

Lab 6 Part C is optional and uses billable preview evaluation features. Do not block the workshop summary when a learner skips it.

Before Lab 6, confirm `azd` 1.27.1 or later, run `azd ext install microsoft.foundry`, and verify Azure CLI and `azd` use the same tenant and subscription. The first deployment uses `azd up`; later code-only updates use `azd deploy`.

## Preserve the Learning Sequence

- Confirm the virtual environment is active before running Python commands.
- Confirm `.env` exists before live inference, but never display its values.
- Explain what a command does before asking a beginner to run it.
- Prefer the smallest checkpoint that proves progress.
- Connect each new task to the result from the previous lab.

## Completion Check

Before moving the learner forward, verify the current lab's checkpoint from its Markdown instructions. If a checkpoint fails, use the `ill335-troubleshooting` skill rather than skipping the failure.
