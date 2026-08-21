---
name: ill335-hosted-agent
description: Supports the ILL335 Microsoft Foundry hosted-agent lab. Use for Lab 6, Agent Framework, FoundryChatClient, ResponsesHostServer, direct code deployment, unified azure.yaml, microsoft.foundry, local readiness checks, azd up, azd deploy, agent invocation, evaluation generation, or deployment troubleshooting.
license: MIT
---

# Support the ILL335 Hosted-Agent Lab

Follow the repository's direct-code deployment path. Use the Microsoft Learn [hosted-agent quickstart](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd), [`azure.yaml` reference](https://learn.microsoft.com/azure/foundry/agents/concepts/azure-yaml-reference), [`azd` development guide](https://learn.microsoft.com/azure/foundry/agents/concepts/cli-agent-development), and current [`microsoft-foundry/foundry-samples`](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents) as the sources of truth.

Do not use older `Azure-Samples/azd-ai-starter-*` repositories as the reference implementation. Do not add deprecated standalone `agent.yaml` or `agent.manifest.yaml` files; the unified root `azure.yaml` replaces them.

This lab uses direct-code remote build through `codeConfiguration`. Do not add a Dockerfile, container registry workflow, or capability-host resources unless the lab deliberately changes to a container deployment or Standard Agent Setup.

## Inspect Before Changing

Read:

- `src/agent/app.py`
- `src/agent/requirements.txt`
- `azure.yaml`
- `docs/lab6-deploy-agent.md`
- `.vscode/tasks.json`

Confirm `azure.yaml` declares:

- `azd` 1.27.1 or later
- `azure.ai.agents` 1.0.0-beta.8 or later and `azure.ai.projects` 1.0.0-beta.4 or later under `requiredVersions`
- an `azure.ai.project` service with the model deployment
- `host: azure.ai.agent`
- `uses` linking the agent to the project service
- Python 3.13 under `codeConfiguration`
- `app.py` as the entry point
- Responses protocol `2.0.0`
- `infra.provider: microsoft.foundry`

## Preserve the Current Agent Pattern

```python
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer

agent = Agent(
    client=FoundryChatClient(...),
    instructions=SYSTEM_PROMPT,
    default_options={"store": False},
)

ResponsesHostServer(agent).run()
```

Foundry manages conversation continuity. Do not add local conversation-history persistence.

## Prepare the Learner Environment

1. Confirm `azd version` is 1.27.1 or later.
2. Run `azd ext install microsoft.foundry`. This meta-extension installs the `azure.ai.*` providers; it does not replace their compatible `requiredVersions` entries in `azure.yaml`.
3. Create and activate `.venv`.
4. Install `src/agent/requirements.txt`.
5. Run `python -m pip check`.
6. Confirm Azure CLI and `azd` use the same tenant and subscription before cloud operations.
7. Never print `.env`, access tokens, or connection strings.

## Validate Locally

Use the Foundry Toolkit F5 task when available. The local server is ready when:

```text
GET http://127.0.0.1:8088/readiness
```

returns HTTP 200 with a healthy status.

## Provision, Deploy, and Invoke

The first cloud operation runs both provider phases: `azd provision` creates the project and model deployment, then `azd deploy` publishes the hosted-agent version:

```powershell
azd up
```

This operation can create billable Azure resources. State that before running it and require the learner's approval.

For later code-only updates to an environment that this project already provisioned:

```powershell
azd deploy
azd ai agent show --output json
azd ai agent invoke "The delivery was late, but support kept me informed."
```

Remote deployment and invocation can incur Azure charges. State that before executing them. Do not run `azd up`, `azd deploy`, or `azd down` merely to test a theory.

## Generate and Run Evaluations

Treat evaluation as an optional post-deployment extension. Generation and evaluation are preview operations that make billable model calls, so state that before running them.

Use `src/agent/evaluation-instructions.md` to generate a domain-specific synthetic suite. Keep `src/agent/evals/caldova-golden.jsonl` as the curated regression set for regulated-routing expectations. Generated data broadens coverage; it does not replace human-reviewed golden cases.

```powershell
azd ai agent eval generate --agent caldova-consumer-sentiment-agent --gen-instruction-file src/agent/evaluation-instructions.md --eval-model gpt-5.4-mini --max-samples 15 --out-file eval.yaml
azd ai agent eval run --config eval.yaml
```

Inspect generated datasets, evaluators, and `eval.yaml` before running them. Do not run optimizer workflows automatically.

When a schema criterion fails, inspect `sample.output_text` before changing the agent. Preview evaluators can mistakenly grade the serialized Responses transport envelope in `sample.output` or `sample.output_items`. If the assistant text is valid but the explanation cites wrapper fields such as annotations or output items, refine the evaluator to grade `sample.output_text`, upload it with `azd ai agent eval update --config eval.yaml --evaluator-only`, and rerun it. Do not present transport-envelope failures as agent regressions.

If wrapper-based failures persist or valid `sample.output_text` is marked not applicable, report the schema criterion separately as a preview evaluator limitation. Do not use the aggregate pass rate alone as the agent quality result.

## Success Criteria

- Agent dependencies resolve without conflicts.
- The local readiness endpoint is healthy.
- `azd up` provisions the project and creates an active hosted-agent version on first use.
- `azd deploy` updates an active hosted-agent version without reprovisioning infrastructure.
- Invocation returns governed JSON through the Responses protocol.
- A learner can distinguish smoke invocation, generated evaluation coverage, and curated regression coverage.
