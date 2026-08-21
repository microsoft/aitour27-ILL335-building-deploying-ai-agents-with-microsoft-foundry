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
- Follow the structure established by GUIDANCE.md

### What NOT to modify without permission:
- License files (`LICENSE`, `LICENSE-DOCS`, `CODE_OF_CONDUCT.md`)
- Security files (`SECURITY.md`)
- GitHub workflow files in `.github/` directory

### Content Rules
- No large binary files (PowerPoint decks, videos, recordings) in the repo
- Links to slides and recordings are fine — just don't host the actual files
- All README files should be kept up to date
- Unused folders (containing only a placeholder README) should be removed before release

### Microsoft Foundry Hosted Agents

Use these current Microsoft-owned sources as the deployment authority:

- [Hosted-agent quickstart](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Hosted-agent `azure.yaml` reference](https://learn.microsoft.com/azure/foundry/agents/concepts/azure-yaml-reference)
- [Agent development with `azd`](https://learn.microsoft.com/azure/foundry/agents/concepts/cli-agent-development)
- [`microsoft-foundry/foundry-samples`](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents)

- Require Azure Developer CLI (`azd`) 1.27.1 or later.
- Install the provider bundle with `azd ext install microsoft.foundry`.
- Keep the compatible provider floors in `azure.yaml`: `azure.ai.agents` 1.0.0-beta.8 or later and `azure.ai.projects` 1.0.0-beta.4 or later. The `microsoft.foundry` meta-extension installs these `azure.ai.*` providers; it does not replace their `requiredVersions` entries.
- Use the unified root `azure.yaml` with separate `azure.ai.project` and `azure.ai.agent` services connected through `uses`.
- Use `infra.provider: microsoft.foundry` for Foundry provider-managed provisioning.
- Use Python 3.13 direct-code deployment through `codeConfiguration` and Responses protocol 2.0.0.
- Use `azd up` for the first provision-and-deploy operation. Use `azd deploy` only for later code-only agent updates.
- Do not add deprecated standalone `agent.yaml` or `agent.manifest.yaml` files.
- This lab uses direct-code remote build, so do not add a Dockerfile, Azure Container Registry, or capability-host resources. Those belong only to explicitly selected container or Standard Agent Setup scenarios.
- Treat older `Azure-Samples/azd-ai-starter-*` repositories and capability-host templates as legacy references.
- Confirm Azure CLI and `azd` are authenticated to the same tenant and subscription before cloud operations.
- Never print or commit `.env`, access tokens, credentials, or connection strings.

### Issue Management
When a user reports a problem, asks a question that should be tracked, or wants to file an issue:

1. **Discover available templates** — Check `.github/ISSUE_TEMPLATE/` for any `.yml` or `.md` template files. Read them to understand what fields and labels each template expects.
2. **Match the request to a template** — Based on what the user is describing, pick the best-fit template. If no templates exist, create a plain issue.
3. **Help the user fill in the fields** — Walk through the template's required fields interactively, proposing answers where possible.
4. **Create the issue** — Use `gh issue create --template <template-file>` if a template matches, or `gh issue create` for a plain issue.
5. **Apply labels** — Check `gh label list` to see what labels exist in the repo. Apply relevant labels based on the issue type. Don't try to apply labels that don't exist.

When reviewing open issues at the start of each phase, summarize them and propose actions — this behavior already exists in the Issue Tracking and Commits section of GUIDANCE.md.

### Getting Started
If this repo still has a `GUIDANCE.md` file, that means setup isn't complete yet. Read it and follow the instructions to prepare the repo for publication.
