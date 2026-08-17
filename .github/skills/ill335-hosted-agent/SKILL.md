---
name: ill335-hosted-agent
description: Supports the ILL335 Microsoft Foundry hosted-agent lab. Use for Lab 6, Agent Framework, FoundryChatClient, ResponsesHostServer, direct code deployment, azure.yaml, local readiness checks, azd deploy, agent invocation, or deployment troubleshooting.
license: MIT
---

# Support the ILL335 Hosted-Agent Lab

Follow the repository's direct-code deployment path. Do not add a Dockerfile, `agent.yaml`, container registry workflow, or `azd up` instructions.

## Inspect Before Changing

Read:

- `src/agent/app.py`
- `src/agent/requirements.txt`
- `azure.yaml`
- `docs/lab6-deploy-agent.md`
- `.vscode/tasks.json`

Confirm `azure.yaml` declares:

- `host: azure.ai.agent`
- Python 3.13 under `codeConfiguration`
- `app.py` as the entry point
- Responses protocol `2.0.0`

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

1. Confirm `azd version` is 1.28.0 or later.
2. Create and activate `.venv`.
3. Install `src/agent/requirements.txt`.
4. Run `python -m pip check`.
5. Confirm Azure CLI and azd authentication before cloud operations.
6. Never print `.env`, access tokens, or connection strings.

## Validate Locally

Use the Foundry Toolkit F5 task when available. The local server is ready when:

```text
GET http://127.0.0.1:8088/readiness
```

returns HTTP 200 with a healthy status.

## Deploy and Invoke

Provision only when the learner asks to create or change Azure infrastructure. For an already provisioned lab environment:

```powershell
azd deploy
azd ai agent show --output json
azd ai agent invoke "The delivery was late, but support kept me informed."
```

Remote deployment and invocation can incur Azure charges. State that before executing them.

## Success Criteria

- Agent dependencies resolve without conflicts.
- The local readiness endpoint is healthy.
- `azd deploy` creates an active hosted-agent version.
- Invocation returns governed JSON through the Responses protocol.
