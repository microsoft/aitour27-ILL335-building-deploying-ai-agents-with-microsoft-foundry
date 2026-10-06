# Lab Setup

> **Duration:** ~10 minutes

Complete these steps before starting the lab modules.

> **Fast-track option:** Run `.\scripts\setup.ps1` (Windows) or `./scripts/setup.sh` (Linux/macOS) to automate **all** prerequisite installation, resource provider registration, Azure provisioning, and environment configuration in one command. Then skip to Lab 1.

> **Windows — PowerShell execution policy (self-study only):** If a `.ps1` script (such as `scripts\setup.ps1` or `.venv\Scripts\Activate.ps1`) fails with *"… is not digitally signed"* or *"running scripts is disabled on this system"*, your execution policy is blocking unsigned scripts. Allow them for the current session **before** running `scripts\setup.ps1` or `azd deploy`:
>
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
> ```
>
> This affects only the current terminal session and its child processes (including the azd post-provision hook) — it does not change your machine-wide policy.

---

## Key Terms

New to AI development? Here are the core terms used throughout this workshop:

| Term | Definition |
|------|------------|
| **Inference** | Sending a prompt to a model and getting a response back. |
| **Token** | The unit models use to measure text — roughly ¾ of a word. Pricing is per-token. |
| **System prompt** | Hidden instructions that tell the model how to behave (e.g., classify feedback sentiment and identify review categories). |
| **Endpoint** | The URL your code connects to for accessing a deployed model or project. |
| **Model deployment** | A specific model (like `gpt-5.4-mini`) made available in your project, ready to receive inference requests. |
| **Credential / authentication** | How your code proves it has permission to use Azure resources — typically via `az login` or a managed identity. |
| **Hosted agent** | Your code deployed to Foundry as a managed service, accessible through the Responses API without managing servers. |
| **RBAC** | Role-Based Access Control — Azure's system for granting specific permissions to users and services. |

---

## Option: Use a dev container or GitHub Codespaces (BYOD)

This optional workspace setup is for self-guided learners using their own Azure
subscription. **Managed Skillable learners must use their provisioned VM and
[Skillable instructions](../docs/skillable/skillable.md)** instead; no classroom
lifecycle changes are required.

Choose one:

- **Codespaces:** On GitHub, select **Code > Codespaces > Create codespace** on
  the branch containing this configuration. No local Docker installation is needed.
- **Local VS Code:** Install Docker with Linux containers and the
  **Dev Containers** extension, clone this repository, and run
  **Dev Containers: Reopen in Container**. If the checkout already has a
  Windows/macOS `.venv`, rename it before reopening; the setup will not delete it.

The [configuration](../.devcontainer/devcontainer.json) provides Python 3.13,
Git, the latest stable Azure CLI and `azd`, Python/Pylance, and the Foundry Toolkit
prerelease. The [workspace hook](../.devcontainer/post-create.sh) explicitly
installs `microsoft.foundry`, `azure.ai.agents`, and `azure.ai.projects`, creates
or reuses `.venv`, installs the root requirements, and runs `pip check`.
It does **not** authenticate, register resource providers, provision/deploy
resources, or create/read `.env`. It never copies host Azure credentials.

Wait for **ILL335 development environment ready**, then open a Bash terminal:

```bash
source .venv/bin/activate
python --version
az version
azd version
azd ext list
python -m pip check
python src/tests/validate_lab.py
```

Expect Python 3.13, the Foundry bundle and both providers in the extension list,
`No broken requirements found`, and an offline validation result of `PASS`
(`.env` may be skipped until configured). The container installs only the main
lab requirements: install the separate agent requirements when you reach
[Lab 6](../docs/lab6-deploy-agent.md#install-agent-dependencies). Their SDK pins
differ, so the hook deliberately does not combine the two requirement sets.
Rerunning the hook reapplies the main lab pins; repeat Lab 6's dependency step
after a rebuild if you are resuming that lab.

Workspace preparation is not Azure provisioning. Continue with **Steps 3-5**
below, authenticate `azd` in **Step 6**, and prepare `.env` in **Step 11**.
For browser-based Codespaces, use device-code authentication:

```bash
az login --use-device-code
azd auth login --use-device-code
```

Confirm Azure CLI and `azd` use the same tenant and subscription before cloud
operations. Skip the already-completed tool/dependency installation steps.
Alternatively, after authentication run `bash scripts/setup.sh` for the existing
BYOD provisioning flow. That script creates billable Azure resources; review
the [cleanup instructions](../cleanup/CLEANUP.md) before proceeding.
Codespaces compute/storage can also incur charges independently of Azure.

### Enable cached Codespaces prebuilds (repository administrators)

The expensive workspace hook uses `updateContentCommand`, which runs during
Codespaces prebuilds, rather than `postCreateCommand`, which runs only when a
learner creates a codespace. `waitFor` prevents the workspace being declared ready
before dependency installation finishes. Existing `.venv` packages and pip's
normal download cache are reused on reruns; ordinary starts/attachments do not
run the installation hook.

**Committing this configuration does not enable hosted prebuilds.** After it is
available on the target branch, a repository administrator must:

1. Open **Settings > Codespaces > Prebuild configuration > Set up prebuild**.
2. Select the workshop branch (normally `main`) and
   `.devcontainer/devcontainer.json`.
3. Choose the regions attendees will use and an update trigger, such as
   **Every push** for fresh workshop dependencies. Configure only needed regions
   and retention to limit storage cost.
4. Save the configuration and wait for the GitHub-managed prebuild workflow to
   succeed. GitHub Actions must be enabled and organizational Codespaces billing
   and policies must allow prebuilds.
5. Create a new codespace in a configured region using a machine type marked
   **Prebuild ready**, then run the checks above. If no matching prebuild exists,
   Codespaces performs a normal, slower setup.

Prebuilds consume GitHub Actions minutes and Codespaces storage. Do not add Azure
credentials, project endpoints, `.env` content, or login/provisioning commands to
prebuilds. No custom workflow or container registry is needed. For local dev
containers, Docker reuses downloaded image/Feature layers; hosted Codespaces
snapshots are a separate cache enabled by the administrator.

See GitHub's [prebuild configuration guide](https://docs.github.com/en/codespaces/prebuilding-your-codespaces/configuring-prebuilds)
and [prebuild lifecycle](https://docs.github.com/en/codespaces/prebuilding-your-codespaces/about-github-codespaces-prebuilds).

---

## Step 1: Verify Git

```bash
git --version
```

Expected output: version 2.40 or later. If not installed:

| OS | Install Command |
|----|-----------------|
| Windows | `winget install -e --id Git.Git` |
| macOS | `brew install git` |
| Ubuntu/Debian | `sudo apt-get install git` |

---

## Step 2: Verify Azure CLI

```bash
az version
```

Expected output includes a version number (e.g., `2.67.0` or later). If not installed:

| OS | Install Command |
|----|-----------------|
| Windows | `winget install -e --id Microsoft.AzureCLI` |
| macOS | `brew install azure-cli` |
| Ubuntu/Debian | `curl -sL https://aka.ms/InstallAzureCLIDeb \| sudo bash` |

Or follow the [Azure CLI install guide](https://aka.ms/installazurecli).

---

## Step 3: Log in to Azure

```bash
az login
```

Complete the browser-based authentication flow. Then verify your subscription:

```bash
az account show --query "{Name:name, SubscriptionId:id, State:state}" -o table
```

If you have multiple subscriptions, select the one you want to use:

```bash
az account set --subscription "<your-subscription-id>"
```

---

## Step 4: Verify Role Permissions

Confirm you have sufficient permissions to create Foundry resources:

```bash
az role assignment list \
  --assignee "$(az ad signed-in-user show --query id -o tsv)" \
  --query "[?contains(roleDefinitionName, 'Owner') || contains(roleDefinitionName, 'Contributor') || contains(roleDefinitionName, 'Azure AI')].{Role:roleDefinitionName, Scope:scope}" \
  -o table
```

You need **Owner**, **Contributor**, or **Azure AI Owner** at the subscription or resource group level. If you do not have the required role, contact your Azure administrator before proceeding.

---

## Step 5: Register Azure Resource Providers

The lab requires several resource providers to be registered on your subscription:

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider register --namespace Microsoft.OperationalInsights
az provider register --namespace Microsoft.Insights
az provider register --namespace Microsoft.ContainerRegistry
```

Check registration status:

```bash
az provider show --namespace Microsoft.CognitiveServices --query registrationState -o tsv
```

> All should return `Registered`. Registration may take a few minutes.

---

## Step 6: Verify Azure Developer CLI

```bash
azd version
```

Version 1.28.0 or later is required for the current Foundry hosted-agent extension and direct-code deployment workflow.

If not installed:

| OS | Install Command |
|----|-----------------|
| Windows | `winget install -e --id Microsoft.Azd` |
| macOS/Linux | `curl -fsSL https://aka.ms/install-azd.sh \| bash` |

Or follow the [Azure Developer CLI install guide](https://aka.ms/azure-dev/install).

Log in to azd:

```bash
azd auth login --check-status
```

If not logged in:

```bash
azd auth login
```

Install the Microsoft Foundry extension bundle:

```bash
azd ext install microsoft.foundry
```

Set your tenant ID so azd provisions to the correct tenant:

```bash
azd env set AZURE_TENANT_ID $(az account show --query tenantId -o tsv)
```

> **Skip the azd first-run tools check (self-study only):** The first time you run `azd up`, azd may prompt *"Would you like to check your Azure development tools?"*. This pauses an otherwise unattended run. Disable it once so future `azd` commands run without the prompt:
>
> ```bash
> azd config set tool.firstRunCompleted true
> ```
>
> Alternatively, set the `AZD_SKIP_FIRST_RUN=true` environment variable for a single session (useful in automation/CI). On Windows PowerShell: `$env:AZD_SKIP_FIRST_RUN = "true"`.

---

## Step 7: Verify Python

```bash
python --version
```

Requires **Python 3.10 or later**. If not installed, download from [python.org](https://www.python.org/downloads/).

---

## Step 8: Create a Virtual Environment

Create and activate a Python virtual environment so lab dependencies are isolated from your system Python:

```bash
python -m venv .venv
```

Activate the environment:

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

You should see `(.venv)` in your terminal prompt.

> **Tip:** You will need to activate the virtual environment each time you open a new terminal for this workshop. Visual Studio Code can do this automatically — when prompted to select a Python interpreter, choose the one inside `.venv`.

---

## Step 9: Install Python Dependencies

With the virtual environment active, install requirements:

```bash
pip install -r requirements.txt
```

This installs:

| Package | Purpose |
|---------|---------|
| `azure-ai-projects` | Foundry project client |

| `azure-identity` | Azure authentication (DefaultAzureCredential) |
| `openai` | OpenAI-compatible API client |
| `python-dotenv` | Environment variable management |

---

## Step 10: Install Visual Studio Code Extensions (Recommended)

If you are using Visual Studio Code, install the recommended extensions:

```bash
code --install-extension ms-windows-ai-studio.windows-ai-studio --pre-release --force
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
```

| Extension | Purpose |
|-----------|---------|
| Foundry Toolkit 1.6.12 or later | Foundry project integration and the embedded Agent Inspector |
| Python | Python language support |
| Pylance | IntelliSense for Python |

After Foundry Toolkit installs or updates, run **Developer: Reload Window** from the Command Palette before using the Lab 6 F5 configuration.

---

## Step 11: Prepare Environment File

Copy the sample environment file and fill in your values (you will get these in Lab 2):

```bash
cp .env.sample .env
```

You will populate `.env` with your project endpoint and model deployment name during Lab 2.

---

## Verification Checklist

Before proceeding to Lab 1, confirm:

- [ ] `git --version` returns 2.40+
- [ ] `az version` returns 2.67.0+
- [ ] `az account show` shows an active subscription
- [ ] You have Owner/Contributor/Azure AI Owner role
- [ ] Resource providers registered (`Microsoft.CognitiveServices`, etc.)
- [ ] `azd version` returns 1.28.0+
- [ ] `azd auth login --check-status` shows logged in
- [ ] `python --version` shows 3.10+
- [ ] `.venv` directory exists and is activated (prompt shows `(.venv)`)
- [ ] `pip install -r requirements.txt` completed successfully
- [ ] Visual Studio Code extensions installed (recommended)
- [ ] `.env` file created from `.env.sample`

---

**Next:** [Lab 1 - Discover Models →](../docs/lab1-discover-models.md)
