# AI Agent Guidelines

This file contains instructions and guidelines for AI agents working on this repository.

## 🔒 Security Best Practices

**Never commit sensitive information to this repository:**
- API keys, tokens, or credentials
- Personal access tokens (PATs)
- Database connection strings with passwords
- Environment-specific configuration values

**For MCP configuration files (`mcp.json`):**
- Use placeholder values like `"YOUR_API_KEY_HERE"` or `"${API_KEY}"`
- Reference environment variables for sensitive data
- Include documentation about required environment variables

## 📋 Repository Guidelines

### Purpose
This repository is an AI Tour session content repository and should:
- Provide clear, actionable content for session attendees
- Support self-guided learning for remote/at-home learners
- Keep navigation and delivery guidance aligned with [README.md](README.md) and the [lab guides](docs/README.md).

### What NOT to modify without permission:
- License files (`LICENSE`, `LICENSE-DOCS`, `CODE_OF_CONDUCT.md`)
- Security files (`SECURITY.md`)
- GitHub workflow files in `.github/` directory

### Content Rules
- No large binary files (PowerPoint decks, videos, recordings) in the repo
- Links to slides and recordings are fine — just don't host the actual files
- All README files should be kept up to date
- Unused folders (containing only a placeholder README) should be removed before release

### Delivery Modes

This repository supports two separate delivery scenarios. Identify the target scenario before changing setup, deployment, prerequisites, environment configuration, or learner instructions.

| Scenario | Audience | Setup authority | Learner instructions |
|----------|----------|-----------------|----------------------|
| Managed Skillable lab | Classroom attendees using a provisioned lab VM and subscription | `skillable_lifecycles/deployment.ps1` and `skillable_lifecycles/azddeloy.ps1` | `docs/skillable/skillable.md` |
| Bring your own device (BYOD) | Remote or self-guided learners using their own workstation or Codespaces and Azure subscription | `setup/SETUP.md`, `scripts/setup.ps1`, `scripts/setup.sh`, and the post-provision scripts; `.devcontainer/` prepares only the workspace | Individual guides under `docs/` |

#### Managed Skillable labs

- Treat files under `skillable_lifecycles/` as administrator-run classroom automation, not learner commands.
- Preserve Skillable replacement tokens such as `@lab.CloudSubscription.*`; never replace them with real credentials or copy their values into documentation, logs, tests, or committed files.
- The lifecycle authenticates with the lab service principal, runs the initial `azd up`, grants the classroom user required roles, and renders the local `.env` on the VM.
- Do not instruct managed-lab learners to provision resources, select a subscription, run BYOD setup scripts, or perform administrator lifecycle actions.
- When shared prerequisites, provider versions, model deployments, or `.env.sample` keys change, update `skillable_lifecycles/deployment.ps1`, the installer lifecycle when relevant, and `docs/skillable/skillable.md` in the same change.

#### Bring your own device

- Assume the learner owns authentication, subscription selection, provisioning cost, and cleanup.
- Use `setup/SETUP.md` and `scripts/setup.*` for initial provisioning; use `scripts/postprovision.*` to render local configuration from azd outputs.
- Do not include Skillable template tokens, fixed `LabUser` paths, classroom service-principal flows, or managed-VM assumptions in BYOD instructions.
- When shared prerequisites, provider versions, model deployments, or `.env.sample` keys change, update both PowerShell and Bash setup paths and the affected individual lab guides.

#### BYOD dev containers and Codespaces

- Treat [`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json) and its [workspace hook](.devcontainer/post-create.sh) as optional BYOD workspace preparation, not Azure provisioning or managed Skillable automation.
- Preserve Python 3.13, the stable Azure CLI/azd toolchain, and explicit installation of `microsoft.foundry`, `azure.ai.agents`, and `azure.ai.projects`. Check that referenced image and Feature tags exist; Feature versions and installed CLI versions are separate.
- Keep dependency installation in `updateContentCommand` with `waitFor: updateContentCommand` so Codespaces prebuilds capture it. Do not move it to `postCreateCommand`, `postStartCommand`, or `postAttachCommand`.
- Docker layer caching and GitHub-hosted prebuilds are separate. Hosted prebuilds require repository-administrator configuration; do not claim they are enabled merely because the configuration is committed. Follow the [prebuild setup instructions](setup/SETUP.md#enable-cached-codespaces-prebuilds-repository-administrators); do not add workflows without approval.
- Keep lifecycle hooks non-interactive and credential-free. Do not authenticate, provision/deploy resources, copy host Azure credentials, or create/read `.env` during workspace preparation or prebuilds.
- Install only the root `requirements.txt` in the hook. The [Lab 6 dependencies](src/agent/requirements.txt) have different SDK pins and are installed separately at the [Lab 6 dependency step](docs/lab6-deploy-agent.md#install-agent-dependencies). Rerunning the hook restores the main-lab pins.
- Reuse a compatible `.venv`; report incompatible environments without deleting them. Preserve LF line endings for container shell scripts and propagate installation errors instead of reporting partial setup as success.
- When shared workspace prerequisites change, update the container configuration and [BYOD setup guide](setup/SETUP.md) alongside the affected setup paths. Container-only changes do not require altering Skillable lifecycle scripts.

Core lab code is shared by both scenarios. Keep expected output and learning outcomes aligned between the individual lab guide and the corresponding section of `docs/skillable/skillable.md`, while allowing setup steps to remain scenario-specific.

### Microsoft Foundry Hosted Agents

Use these current Microsoft-owned sources as the deployment authority:

- [Hosted-agent quickstart](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Hosted-agent `azure.yaml` reference](https://learn.microsoft.com/azure/foundry/agents/concepts/azure-yaml-reference)
- [Agent development with `azd`](https://learn.microsoft.com/azure/foundry/agents/concepts/cli-agent-development)
- [`microsoft-foundry/foundry-samples`](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents)

- Require Azure Developer CLI (`azd`) 1.27.1 or later.
- Treat `azure.yaml` `requiredVersions` as the declared compatibility floors, not a guarantee that every newer extension supports the minimum CLI. Respect the selected extension's own azd requirement. Reconcile version guidance across BYOD setup, Skillable automation/instructions, and `azure.yaml` together; do not raise shared floors based only on the version installed during a local test.
- Install the provider bundle with `azd ext install microsoft.foundry`.
- Keep the compatible provider floors in `azure.yaml`: `azure.ai.agents` 1.0.0-beta.8 or later and `azure.ai.projects` 1.0.0-beta.4 or later. The `microsoft.foundry` meta-extension installs these `azure.ai.*` providers; it does not replace their `requiredVersions` entries.
- Use the unified root `azure.yaml` with separate `azure.ai.project` and `azure.ai.agent` services connected through `uses`.
- Use `infra.provider: microsoft.foundry` for Foundry provider-managed provisioning.
- Use Python 3.13 direct-code deployment through `codeConfiguration` and Responses protocol 2.0.0.
- Use `azd up` for the first provision-and-deploy operation. Use `azd deploy` only for later code-only agent updates.
- Do not add deprecated standalone `agent.yaml` or `agent.manifest.yaml` files.
- Hosted-agent deployment uses direct-code remote build, so do not add an agent Dockerfile, Azure Container Registry, or capability-host resources. Those belong only to explicitly selected container deployment or Standard Agent Setup scenarios. The BYOD development container does not change this deployment architecture.
- Treat older `Azure-Samples/azd-ai-starter-*` repositories and capability-host templates as legacy references.
- Confirm Azure CLI and `azd` are authenticated to the same tenant and subscription before cloud operations.
- Never print or commit `.env`, access tokens, credentials, or connection strings.

### Validation

See the [automated testing guide](src/tests/README.md) and [manual lab checkpoints](src/tests/TESTING.md).

- Run `python src/tests/validate_lab.py` for relevant repository/setup changes and the smallest unit-test selection covering the change. Do not use `--live` or `--agent` merely to validate workspace configuration.
- For dev-container changes, run `python -m unittest discover -s src/tests -p test_devcontainer.py -v` and `bash -n .devcontainer/post-create.sh`. On Windows, set `BASH_EXECUTABLE` to Git for Windows Bash if the default Bash points to unavailable WSL.
- When Docker is available, validate the real build, `updateContentCommand`, `python -m pip check`, and offline lab checks inside the container. Verify cached rebuilds and that normal restarts do not reinstall dependencies. Mocked hook tests alone do not establish that a container builds or hosted Codespaces prebuilds work.
- Syntax-check PowerShell and Bash setup scripts when changed. Verify learner commands, expected output, and navigation when documentation changes.
- Distinguish passed checks, expected skips, unavailable validation, and pre-existing failures. Reproduce suspected baseline failures before attributing them to a change; do not fix unrelated lab behavior to make container validation green.
- Do not modify host credentials or environments during container validation. Clean up only the temporary containers and files created for the check; do not prune shared Docker resources.

### Issue Management
When a user reports a problem, asks a question that should be tracked, or wants to file an issue:

1. **Discover available templates** — Check `.github/ISSUE_TEMPLATE/` for any `.yml` or `.md` template files. Read them to understand what fields and labels each template expects.
2. **Match the request to a template** — Based on what the user is describing, pick the best-fit template. If no templates exist, create a plain issue.
3. **Help the user fill in the fields** — Walk through the template's required fields interactively, proposing answers where possible.
4. **Create the issue** — Use `gh issue create --template <template-file>` if a template matches, or `gh issue create` for a plain issue.
5. **Apply labels** — Check `gh label list` to see what labels exist in the repo. Apply relevant labels based on the issue type. Don't try to apply labels that don't exist.

When reviewing open issues at the start of a work phase, summarize relevant issues and propose actions.

### Getting Started
Start with [README.md](README.md), then select the appropriate delivery path: [BYOD setup](setup/SETUP.md) or the [managed Skillable guide](docs/skillable/skillable.md). Keep their workspace preparation and provisioning responsibilities separate.
