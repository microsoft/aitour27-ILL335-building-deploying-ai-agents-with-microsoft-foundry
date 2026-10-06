---
name: ill335-troubleshooting
description: Diagnoses ILL335 setup, authentication, dependency, Responses API, validation, and hosted-agent failures. Use when a learner reports an error, failed lab checkpoint, broken setup, dev container or Codespaces prebuild failure, deployment problem, rate limit, content filter, or unexpected model output.
license: MIT
---

# Troubleshoot ILL335 Safely

Diagnose the smallest failing layer first. Do not provision, deploy, or delete Azure resources merely to test a theory.

## Start with Reproduction

1. Ask for the command that failed and the error text, with secrets removed.
2. Identify the learner's operating system and lab number.
3. Confirm the virtual environment is active.
4. Run the smallest relevant check.

For Docker workspace startup, Codespaces prebuilds, or container dependency
failures, use [ill335-devcontainer](../ill335-devcontainer/SKILL.md). Establish
BYOD versus managed Skillable first; do not direct managed learners to rebuild
their environment or provision Azure resources.

## Diagnostic Order

### Repository and Python

```powershell
python -m pip check
python -m pytest src\tests\test_sentiment.py -q
python src\tests\validate_lab.py
```

### Configuration

- Confirm `.env` exists without printing its contents.
- Check that `PROJECT_ENDPOINT` is not a placeholder.
- Check that model deployment names match the Foundry project.
- Use `az account show` and `azd auth status` for authentication state.
- Confirm Azure CLI and `azd` are signed into the same tenant and subscription. Reauthenticate the mismatched CLI before retrying.

### Responses API

| Symptom | Likely action |
|---|---|
| Authentication failure | Refresh `az login`; verify project access |
| Resource not found | Verify project endpoint and model deployment name |
| HTTP 429 | Wait for the retry interval; check quota and capacity |
| Content filter response | Explain the safety boundary; do not bypass it |
| Empty or incomplete output | Inspect `response.status` and the full error |
| Invalid JSON | Preserve the conservative fallback and review the instructions |

### Hosted Agent

- Require `azd` 1.27.1 or later and install the provider bundle with `azd ext install microsoft.foundry`.
- Keep `azure.ai.agents` 1.0.0-beta.8 or later and `azure.ai.projects` 1.0.0-beta.4 or later in `azure.yaml` `requiredVersions`; the meta-extension installs these providers but does not replace the compatibility declarations.
- Confirm `azure.yaml` contains separate `azure.ai.project` and `azure.ai.agent` services, an agent `uses` dependency, and `infra.provider: microsoft.foundry`.
- Treat standalone `agent.yaml` and `agent.manifest.yaml` as deprecated. This lab uses direct-code remote build, so Dockerfiles, ACR provisioning, and capability-host resources indicate the wrong deployment path.
- Run `python -m pip install -r src\agent\requirements.txt`, then `python -m pip check`.
- Verify `/readiness`, not `/health`; the current host exposes readiness at port 8088.
- Use `azd up` for the first provision-and-deploy operation and `azd deploy` only for later code updates.
- Use `azd ai agent show --output json` before invoking a deployed agent.
- Review deployment output and hosted logs before changing infrastructure.

## Safety Boundaries

- Never request or reveal credentials, tokens, connection strings, or real patient data.
- Do not disable content safety to make a test pass.
- Do not delete resource groups or agent sessions without explicit learner approval.
- Do not provision resources merely to validate local configuration or dependencies.
- Do not replace current Responses API code with Chat Completions.
- Do not add broad exception handlers that hide the original failure.

## Resolution Check

Repeat the exact failing command after the fix. Then rerun the nearest lab checkpoint and explain what changed in beginner-friendly terms.
