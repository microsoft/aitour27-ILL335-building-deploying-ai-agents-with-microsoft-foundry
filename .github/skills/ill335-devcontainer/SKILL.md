---
name: ill335-devcontainer
description: "Prepares and validates the ILL335 BYOD development container. Use for dev containers, GitHub Codespaces, Docker workspace setup, prebuilds, cached builds, rebuilds, container startup, virtual-environment conflicts, or workspace dependency installation failures."
license: MIT
---

# Prepare and Validate the ILL335 Development Container

Prepare the development workspace without authenticating to Azure or provisioning
cloud resources. The development container does not change the hosted agent's
direct-code deployment architecture.

## Establish Scope

1. Identify the delivery mode before giving setup commands. Managed Skillable
   learners use their provisioned VM and the [Skillable guide](../../../docs/skillable/skillable.md),
   not this BYOD workflow.
2. For BYOD, distinguish local VS Code with Docker from GitHub Codespaces.
   Docker is required locally, not on a learner's device when using Codespaces.
3. Read the [setup guide](../../../setup/SETUP.md),
   [container configuration](../../../.devcontainer/devcontainer.json),
   [workspace hook](../../../.devcontainer/post-create.sh), and
   [test instructions](../../../src/tests/README.md).
4. Inspect only relevant configuration. Never display `.env`, credentials,
   connection strings, or authentication caches.

## Preserve the Workspace Contract

- Use Python 3.13, the configured stable Azure CLI/azd toolchain, and explicit
  installation of `microsoft.foundry`, `azure.ai.agents`, and `azure.ai.projects`.
  Check published image and Feature tags before changing them; a Feature's version
  is not the installed CLI version.
- Respect [azure.yaml](../../../azure.yaml) compatibility floors and the selected
  extensions' own CLI requirements. Do not change shared floors solely to match
  a local test machine.
- Keep installation in `updateContentCommand` and retain
  `waitFor: updateContentCommand`. Codespaces runs that hook during prebuilds;
  `postCreateCommand` is too late to cache its work in the prebuild snapshot.
- Keep hooks non-interactive and fail on installation errors. Do not authenticate,
  provision, deploy, register resource providers, copy host credentials, or
  create/read `.env` in a hook.
- Install only the [root requirements](../../../requirements.txt). Install the
  different [agent requirements](../../../src/agent/requirements.txt) when the
  learner reaches [Lab 6](../../../docs/lab6-deploy-agent.md#install-agent-dependencies).
  Rerunning the workspace hook restores the main-lab pins.
- Reuse compatible virtual environments. If `.venv` comes from Windows/macOS or
  has an incompatible Python version, explain how to rename it before rebuilding;
  never delete it automatically.
- Preserve LF endings for container shell scripts. Do not add an agent Dockerfile,
  container registry, or deployment infrastructure for this workspace feature.

## Validate Locally

Run from the repository root using an available Python interpreter and Bash:

```bash
python -m unittest discover -s src/tests -p test_devcontainer.py -v
bash -n .devcontainer/post-create.sh
```

On Windows, use Git for Windows Bash if WSL is unavailable and set
`BASH_EXECUTABLE` for the hook tests. Use host-appropriate path separators.

For real container validation:

1. Check `docker info` and confirm the engine supports Linux containers. If it is
   unavailable, report build/startup validation as blocked, not passed.
2. Use the Dev Containers extension or its available CLI. For an agent-run test,
   prefer an isolated copy of tracked and relevant non-ignored files, excluding
   `.env`, `.azure`, host credentials, and existing virtual environments.
3. Build and run the actual configuration. With the Dev Containers CLI:

   ```bash
   devcontainer up --workspace-folder "<validation-workspace>" --prebuild
   ```

   This exercises the lifecycle through `updateContentCommand`; it is not a
   GitHub-hosted prebuild.
4. Confirm the container is running and commands execute as the configured
   non-root user. Inside its workspace, activate `.venv` and run:

   ```bash
   source .venv/bin/activate
   python --version
   az version
   azd version
   azd ext list
   python -m pip check
   python src/tests/validate_lab.py
   python -m unittest discover -s src/tests -p test_devcontainer.py -v
   ```

5. Require all three Foundry extensions to be installed, no broken Python
   requirements, and passing offline checks. A missing `.env` is an expected
   skip before Azure setup. Mocked hook tests do not replace this real build.
6. Rebuild the image and inspect actual Docker `CACHED` steps. Rerun the prebuild
   hook to verify environment reuse. Stop and restart only the test container;
   confirm normal startup does not rerun dependency installation.
7. Report exact results and distinguish baseline failures from container
   regressions. Reproduce suspected pre-existing failures outside the container
   before attributing them. Do not make unrelated lab-code changes.
8. Remove only temporary containers/files created for validation. Retain useful
   image caches; never prune shared Docker resources.

## Enable Codespaces Prebuilds

Follow the [administrator instructions](../../../setup/SETUP.md#enable-cached-codespaces-prebuilds-repository-administrators).
Committing the container configuration does not enable hosted prebuilds.
An administrator selects the branch, configuration, regions, and update trigger
under repository **Settings > Codespaces**.

Explain GitHub Actions/storage costs before changing hosted prebuild settings.
Do not add workflows without approval or put Azure credentials into prebuilds.
Verify a successful GitHub-managed prebuild and a new codespace marked
**Prebuild ready** before claiming hosted caching works. Docker cache hits alone
prove only local image caching; local restart timings are not Codespaces startup
benchmarks.

## Diagnose the Smallest Failing Layer

| Failure | Next check |
|---------|------------|
| Image or Feature cannot be resolved | Verify the published tag, registry access, and target architecture. |
| Extension download returns HTTP 5xx | Record the failing public artifact/version, check reachability from inside the container, then retry the exact command once reachability recovers. Persistent failures remain blockers; do not hide them or downgrade arbitrarily. |
| Existing `.venv` is incompatible | Preserve it and explain renaming/rebuilding; do not reuse a host interpreter inside Linux. |
| Dependency resolution fails | Confirm the hook installs only root requirements; use the separate Lab 6 dependency step for agent work. |
| Installation is slow on a Windows bind mount | Check process progress before declaring a hang; distinguish host filesystem overhead from Codespaces performance. |
| No **Prebuild ready** option | Check administrator configuration, branch/configuration, region, and GitHub-managed workflow outcome. |

For Azure authentication, inference, or hosted-agent failures after workspace
preparation, use [ill335-troubleshooting](../ill335-troubleshooting/SKILL.md).
Never provision or make billable model calls merely to test the container.
