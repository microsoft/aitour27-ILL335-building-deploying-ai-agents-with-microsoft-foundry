# Lab 6: Deploy a hosted agent

> **Duration:** ~20 minutes, plus an optional 10-15 minute evaluation extension

## Objective

Deploy Caldova's consumer sentiment agent directly from Python source to Microsoft Foundry Agent Service. You will inspect the Agent Framework code, verify the direct-code service configuration in `azure.yaml`, test the agent locally with the Agent Inspector, deploy it to the cloud, and validate the hosted agent.

This lab has three parts. **Part A** tests the agent locally with the Foundry Toolkit. **Part B** deploys and verifies it with `azd`. **Part C** is an optional self-paced extension that generates and runs a structured evaluation against the deployed agent.

## What is a hosted agent?

A hosted agent is your agent application running on Foundry-managed infrastructure. Unlike the scripts in Labs 3-5 that run locally, a hosted agent is a persistent, cloud-hosted service that exposes the OpenAI Responses protocol. Foundry handles the heavy lifting:

- **VM-isolated sandboxes** -- each session runs in its own isolated sandbox with a persistent filesystem.
- **REST API** -- a protocol library exposes your agent as an OpenAI Responses API endpoint, callable by the Foundry Playground, other agents, or any application.
- **Per-session scaling** -- the platform creates a sandbox on demand and tears it down when idle.
- **Dedicated agent identity** -- each agent authenticates to Foundry models and Azure services with its own Azure identity (no keys to manage).
- **Managed conversation history** -- the platform maintains continuity between turns, so your `Agent` does not need a local message list.

## Architecture

The Foundry Toolkit runs the agent locally for inspection, while `azd` packages and deploys the source to Foundry Agent Service. At runtime, the platform provisions a sandbox and exposes a dedicated endpoint that your agent uses to call Foundry models.

![Direct-code hosted agent architecture](images/mermaid_diagram2.png)

| Property | This lab |
|----------|----------|
| Source | `src/agent/app.py` and `src/agent/requirements.txt` |
| Runtime | Python 3.13 |
| Host adapter | `ResponsesHostServer` |
| Protocol | Responses 2.0.0 |
| Deployment | Direct code through `azure.yaml` and `azd up` |
| History | Managed by the Foundry platform |
| Identity | Azure identity; no credentials stored in source |

## Prerequisites

- Foundry Toolkit 1.6.12 or later installed and signed in to Azure (from Lab 1). After updating the extension, run **Developer: Reload Window** before pressing F5.
- Azure Developer CLI (`azd`) 1.27.1 or later.
- The Microsoft Foundry extension bundle installed with `azd ext install microsoft.foundry`.
- `.env` with `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` set.

Install the agent dependencies (separate from the main lab requirements):

```powershell
pip install -r src/agent/requirements.txt
```

Before Part A, open **Extensions**, find **Foundry Toolkit**, select **Switch to Pre-Release Version** or **Update** if offered, and confirm version 1.6.12 or later. Then run **Developer: Reload Window** from the Command Palette so the updated Agent Inspector is active.

> **Note:** The `microsoft.foundry` meta-extension installs compatible `azure.ai.*` providers, including the project and hosted-agent providers used by this lab.

## Review the agent code

Open `src/agent/app.py`. The hosted agent imports the Foundry client and the Responses host:

```python
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential
```

- **Connects** through `FoundryChatClient` from `agent_framework.foundry`.
- **Hosts** the agent with the Responses adapter, `ResponsesHostServer`.
- **Authenticates** without hardcoded secrets.

The `Agent` uses the Caldova sentiment instructions and disables model-side response storage:

```python
agent = Agent(
    client=FoundryChatClient(
        project_endpoint=PROJECT_ENDPOINT,
        model=MODEL_DEPLOYMENT_NAME,
        credential=DefaultAzureCredential(),
    ),
    name="caldova-consumer-sentiment-agent",
    instructions=SYSTEM_PROMPT,
    default_options={"store": False},
)
```

- **Applies** the Caldova sentiment-analysis instructions.
- **Relies** on platform-managed conversation history.
- **Prevents** duplicate response storage in the model call with `store: False`.

The entry point starts the Responses host:

```python
if __name__ == "__main__":
    ResponsesHostServer(agent).run()
```

- **Exposes** the agent through the Responses protocol expected by Foundry hosting.

### The deployment definition: azure.yaml

The root `azure.yaml` is the source of truth for the Foundry project, model deployment, and hosted agent. The `microsoft.foundry` provider provisions the project without the legacy capability-host infrastructure pattern. The agent uses direct source-code deployment with the managed Python 3.13 runtime:

```yaml
services:
  ai-project:
    host: azure.ai.project
  caldova-consumer-sentiment-agent:
    host: azure.ai.agent
    project: src/agent
    codeConfiguration:
      runtime: python_3_13
      entryPoint: app.py
      dependencyResolution: remote_build
    uses:
      - ai-project
    protocols:
      - protocol: responses
        version: 2.0.0
infra:
  provider: microsoft.foundry
```
---

## Install agent dependencies

> This step is shared by both Part A and Part B — do it once before you start.

Confirm that VS Code is using the workspace virtual environment. The Python interpreter shown in the status bar should be `.venv`.

![VS Code status bar showing the selected virtual environment](images/status_bar.png)

If it is not, run **Python: Select Interpreter** from the Command Palette and choose the Python executable under `.venv`.

The agent uses packages that are separate from the main lab requirements, and both deployment paths need them. Install them first:

```powershell
pip install -r src/agent/requirements.txt
```

This includes the Agent Framework hosting adapter and **debugpy** for local debugging.

---

## Part A: Test locally with the Agent Inspector

You have reviewed the agent and its deployment contract. Before creating a cloud version, run the same Python entry point locally and check its Responses endpoint through the Foundry Toolkit.

1. In VS Code, open **Run and Debug**.
2. Select **Debug Agent with Agent Inspector**.
3. Press **F5**. The configured tasks start `src/agent/app.py`, wait until its server is listening on port `8088`, and open the Foundry Toolkit Agent Inspector inside VS Code.
4. Send this feedback:

   ```text
   The delivery was late, but support kept me informed.
   ```

5. Confirm that the response is one JSON object with sentiment, confidence, topics, review category, and summary fields.

The exact labels can vary, but the agent should identify both the delivery problem and the positive support experience. Stop the debugger when the check is complete.

Inspect the **Overview** tab in the Agent Inspector to see a summary of the agent's status, recent requests, and responses. You will also see:

- A **Tokens** panel showing token usage for each request and response, as well as the total token count for the session.
- An **Events** panel showing the sequence of events for each request and response, including any errors or warnings.
- A **Tools** panel showing details of tool calls made by the agent, including input parameters and results. This agent does not make tool calls, so the panel will be empty.

![Agent Inspector overview showing request and response details](images/inspector_logs.png)

The local entry point reads `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` from the same managed `.env` used in earlier labs. If the Inspector cannot connect, confirm the debug terminal reaches `AgentServerHost started` and update Foundry Toolkit before changing the agent code.

### Local checkpoint

The Agent Inspector receives a valid JSON response and the local server reports no authentication or startup errors.

---

## Part B: Deploy and verify the hosted agent

Local testing proves the code and prompt work together. Deployment now packages the Python source, builds it remotely with the managed Python 3.13 runtime, and creates an immutable hosted-agent version.

> **Cost notice:** The following commands create or use billable Azure resources. In a managed workshop, follow your instructor's directions before running them.

From the repository root, verify the CLI and install the Foundry extension bundle:

```powershell
azd version
azd ext install microsoft.foundry
```

For the first deployment in an environment, provision the project and deploy the agent together:

```powershell
azd up
```

Later code-only changes use `azd deploy caldova-consumer-sentiment-agent` instead. Targeting the agent avoids deploying optional evaluation resources added in Part C. Each successful deployment creates an immutable agent version.

Check that the deployed version is active:

```powershell
azd ai agent show --output json
```

Then send one deployed smoke test:

```powershell
azd ai agent invoke caldova-consumer-sentiment-agent "The delivery was late, but support kept me informed."
```

The response should contain valid governed JSON. The `show` command also returns the Responses endpoint and a Foundry Playground URL for visual testing.

### Cloud checkpoint

The agent status is `active`, and the remote invocation returns a JSON object without storing credentials in source code.

---

## Part C: Generate an evaluation suite (optional preview)

A smoke test checks one response. In this part, you will request 15 test cases, check the generated dataset, run the cases against your deployed agent, and review the scores.

> **Preview and cost notice:** Generation and evaluation make billable model calls and can take several minutes. Skip this section during the core workshop when time is limited.

**Follow Steps 1-10 in order.** Stop if a command reports an error; use the troubleshooting table below before continuing. Each command block is a separate action: paste the whole block, press **Enter**, and wait for it to finish before pasting another.

**Where to paste:** Run only blocks labelled **powershell** in the terminal. Blocks labelled **yaml** or **json** are file content or examples, not terminal commands. Follow the editor instructions beside those blocks.

### Step 1: Open the correct terminal

1. Complete Part B first: the deployed agent must be active and its smoke test must work.
2. In VS Code, select **Terminal > New Terminal** and use **PowerShell**.
3. Make sure the terminal is at the repository root: the folder containing `azure.yaml`, `.env`, and `src`.
4. Keep this terminal open throughout Part C. The endpoint and run ID you set below belong to this terminal session.

**Expected result:** You are ready to use the existing project and agent. You do not need to provision or redeploy them.

### Step 2: Install the evaluations extension

Run:

```powershell
azd extension install azure.ai.evaluations
```

**Expected result:** The extension installs successfully or is already installed. These instructions use `azure.ai.evaluations` `1.0.0-beta.2`, not the retired `azd ai agent eval` commands.

If installation reports a CLI compatibility requirement, update `azd` to a version supported by that extension before continuing. See the Microsoft-owned [evaluations extension guide](https://github.com/Azure/azure-dev/tree/main/cli/azd/extensions/azure.ai.evaluations) for command details.

### Step 3: Set the existing project endpoint

1. In VS Code Explorer, open the repository's existing `.env`.
2. Find `PROJECT_ENDPOINT=` and copy **only the value after `=`**, without surrounding quotes.
3. Run this block. When PowerShell displays the prompt, paste that value and press **Enter**:

```powershell
$env:FOUNDRY_PROJECT_ENDPOINT = Read-Host "Paste the existing PROJECT_ENDPOINT value"
if ([string]::IsNullOrWhiteSpace($env:FOUNDRY_PROJECT_ENDPOINT)) {
  throw "The existing Foundry project endpoint is required before continuing."
}
```

**Expected result:** PowerShell returns to the prompt without an error. The evaluations CLI can now use the same project as your agent. It does not automatically read the Python agent's `PROJECT_ENDPOINT` key from `.env`.

Do not print or share `.env`. Use the same authenticated identity and subscription as Part B. If you open a new terminal later, repeat this step.

### Step 4: Generate the test cases and scoring rubric

Run the following command. It asks for **turn-level** cases: one request and response per row, not multi-turn conversation scenarios.

`--max-samples 15` requests up to 15 cases; it does not guarantee that the preview generator returns exactly 15. Wait for both generation jobs to finish, then check the actual count in Step 5 before initializing or running an evaluation.

```powershell
azd ai eval generate `
  --path evals `
  --target caldova-consumer-sentiment-agent `
  --agent-instruction-file src\agent\evaluation-instructions.md `
  --evaluation-level turn `
  --from prompt `
  --trace-days 0 `
  --generation-model gpt-5.4-mini `
  --max-samples 15 `
  --dataset-name caldova-generated-turn `
  --evaluator-name caldova-quality-turn
```

If prompted:

1. For **What do you want to generate?**, select **Dataset and evaluator**.
2. If asked for the evaluation level, select **Turn**, never **Conversation**.
3. Check the generation plan against this table.
4. Only when the settings match, choose **Generate** and wait for both jobs to finish.

| Setting | Required value |
|---------|----------------|
| Agent | `caldova-consumer-sentiment-agent` |
| Dataset | `caldova-generated-turn` |
| Evaluation level | Turn |
| Number of cases | 15 |
| Dataset source | Prompt |
| Evaluator | `caldova-quality-turn` |
| Traces | Off |

**Expected result:** Both artifacts are downloaded, and `evals/azure.eval.yaml` contains their catalog entries. The files are normally `evals/datasets/caldova-generated-turn.jsonl` and `evals/evaluators/caldova-quality-turn.json`.

If the plan says **Conversation** or **scenarios**, cancel. If these names already exist, do not overwrite them automatically: use the recovery guidance below. Ignore the CLI's suggested next command for now; complete Step 5 first.

### Step 5: Check the generated dataset

**You do not need to run a command for this step.** Inspect the generated file in VS Code:

1. Press **Ctrl+P**, enter `evals\datasets\caldova-generated-turn.jsonl`, and press **Enter**.
2. Count the non-empty lines, with one JSON object per line. The exercise target is **15 non-empty lines**. Use the editor's line numbers; ignore a final blank line. If you see fewer, such as 13, follow the recovery instructions below before proceeding to Step 6.
3. Check every object has a `"query"` field containing feedback text in quotes. The text must not be empty.

   This is a simplified example of the required field, **not content to paste into the file**. Your generated objects may contain other fields too:

```json
{"query": "The delivery was late, but support kept me informed."}
```

4. Read the cases. Look for ordinary sentiment, mixed feedback, regulated review routing, and the prohibition on medical advice.
5. In Explorer, open `evals/evaluators/caldova-quality-turn.json`. Check that its scoring descriptions cover those requirements and valid JSON.

**Expected result:** You have reviewed 15 test cases, each with a non-empty `query`, and their scoring rubric.

**Stop before Step 6** if the file is empty, the number of cases differs from 15, or any object lacks feedback text in `query`. Record the actual number of cases and check the generation output from Step 4. Objects containing only scenario fields such as `simulation_configuration` and `test_case_description` are conversation seeds, not the turn-level cases required here. Do not edit the file to force a pass.

**If fewer than 15 cases were generated:**

1. Confirm that both generation jobs have finished and inspect their output for errors. Do not start another generation while either job is still running.
2. Preserve the existing files and catalog. Do not add dummy rows, duplicate cases, or use `--force` to overwrite them.
3. Retry Step 4 once, changing only `--path evals` to `--path evals-retry-1`, an unused folder. Keep the dataset and evaluator names unchanged. This makes additional billable model calls and may produce different cases.
4. Repeat Step 5 using `evals-retry-1\datasets\caldova-generated-turn.jsonl` and `evals-retry-1/evaluators/caldova-quality-turn.json`. If the retry passes all Step 5 checks, use `--path evals-retry-1` instead of `--path evals` in every remaining evaluation command, and open files under `evals-retry-1/` instead of `evals/`. Do not mix the original dataset or rubric with the retry.
5. If that folder already exists, or the retry still fails the checks, stop and ask for help. You can skip this optional Part C and continue to [Lab 7](./lab7-summary.md) rather than repeatedly generating billable replacements.

**Dataset count is not a pass count.** A 15-row dataset can yield **15 passed, 0 failed** or **13 passed, 2 failed**. Generated cases, agent responses, and preview evaluator judgments can vary between runs. Both totals account for 15 evaluated cases; inspect each failed case in Step 10 rather than regenerating until all cases pass.

### Step 6: Create the local evaluation configuration

Run:

```powershell
azd ai eval init `
  --path evals `
  --name caldova-generated-turn `
  --source dataset `
  --evaluation-level turn `
  --target caldova-consumer-sentiment-agent `
  --dataset caldova-generated-turn `
  --evaluator caldova-quality-turn `
  --judge-model gpt-5.4-mini
```

1. In the preview, confirm the name and dataset are `caldova-generated-turn`, the evaluation level is **turn**, and the evaluator is `caldova-quality-turn`.
2. Confirm the agent is `caldova-consumer-sentiment-agent` and the judge model is `gpt-5.4-mini`.
3. When asked to add the evaluation, choose **Add evaluation**.
4. Open `evals/azure.eval.yaml` and confirm the new evaluation appears under `evals`.

**Expected result:** The CLI updates the local evaluation configuration and reports an evaluation service in the root `azure.yaml`. The service might be named `caldova-consumer-sentiment-agent-evals`; its name is not necessarily `evals`.

The evaluation is configured locally, but it is **not registered in Foundry yet**. The next step does that. Paths in `evals/azure.eval.yaml` are relative to that file; use its `file` and `source` values if artifact paths differ. The evaluation service uses `host: azure.ai.eval`, depends on `ai-project`, and references `./evals/azure.eval.yaml`.

### Step 7: Register the evaluation in Foundry

Run:

```powershell
azd ai eval create caldova-generated-turn --path evals
```

**Expected result:** The named evaluation and its referenced dataset and evaluator are registered, or reported unchanged if already registered. This does not rebuild the agent.

If this command fails, **stop before Step 8**. Do not use `azd up` or guess a service name as a workaround.

**Recover an evaluator version mismatch**

An error such as **version 3 on the project but 2 was recorded at the last deploy** means the published evaluator advanced since this local configuration last reconciled it, and the local definition differs. This is a conflict safeguard, not an agent deployment failure. Regeneration or a standalone `evaluator update` can leave the local and published definitions out of sync. A separate local retry folder does not isolate evaluator names in the same Foundry project.

1. Keep the current dataset, evaluator JSON, `azure.eval.yaml`, and `azure.eval.lock`. Back up the local evaluator JSON in VS Code before making changes. Do not delete the lock file or a published evaluator version, rerun generation, or use a standalone `evaluator update` to bypass the conflict.
2. Download the published version named in the error to a **new file**, not over the local rubric. For the example above, run:

```powershell
azd ai eval evaluator download caldova-quality-turn --version 3 --output-file evals\evaluators\caldova-quality-turn-project-v3.json
```

   Replace **3** and **v3** with the version in your error. If you used the Step 5 retry folder, use `evals-retry-1` instead of `evals` here and below. If the destination already exists, choose another unused filename; do not use `--force`. If your extension does not support `evaluator download`, stop and check the [evaluations extension guide](https://github.com/Azure/azure-dev/tree/main/cli/azd/extensions/azure.ai.evaluations) for compatibility guidance rather than guessing a replacement command.

3. Compare the downloaded rubric with the local backup and confirm that the published dimensions and scoring rules are appropriate. In `evals/azure.eval.yaml`, find the `caldova-quality-turn` evaluator's catalog entry and change only its `source` to `evaluators/caldova-quality-turn-project-v3.json`, relative to that YAML file. Keep the evaluator name and evaluation references unchanged. Save the file. **Do not merge local rubric edits yet**: first reconcile the unchanged published definition.
4. Repeat Step 7:

```powershell
azd ai eval create caldova-generated-turn --path evals
```

   **Expected result:** The published evaluator is reused and the local deployment record is reconciled; the named evaluation registers successfully. Only then proceed to Step 8. If the version advances again, or reconciliation still fails, stop and ask for help; do not repeatedly publish over it.

5. If you still need an intentional local rubric correction, review it against the backup and apply it to the JSON file now named by `source`, only after item 4 succeeds. Repeat Step 7 to publish that intentional change before starting a run. Do not regenerate cases just to obtain failures: all-pass results are valid.

### Step 8: Start one evaluation run

Run this command **once**:

```powershell
azd ai eval run start --path evals --eval caldova-generated-turn --no-wait
```

**Expected result:** The CLI accepts the run and returns a **run ID**. Copy that ID. Do not copy the dataset job ID from Step 4 or the evaluation ID from Step 7.

### Step 9: Wait for that run to finish

1. Copy the **run ID** from the output of Step 8.
2. In the line below, replace `YOUR-RUN-ID-HERE` with that ID. **Keep the double quotes.**
3. Paste your edited line into the same PowerShell terminal and press **Enter**:

```powershell
$runId = "YOUR-RUN-ID-HERE"
```

This saves your ID as `$runId` for the remaining commands. **No output is expected from this line.** Do not run it with the placeholder unchanged.

4. Run this command exactly as shown. PowerShell uses the ID you saved:

```powershell
azd ai eval run show --path evals --eval caldova-generated-turn --run $runId --wait
```

**Expected result:** The run reaches a terminal status and shows its results. A completed run can still contain failed test cases.

If monitoring times out, repeat only the `run show` command above with the same `$runId`. **Do not repeat Step 8** just to resume monitoring: it starts another billable run.

### Step 10: Review the scores and at least one result

1. In the Foundry Toolkit, expand **My Resources > Evaluations**.
2. Select your evaluation and the run you just completed.
3. Review the scores for each criterion, not only the aggregate pass rate.
4. Open a failed or borderline case and read both the assistant response (`sample.output_text`) and the evaluator's explanation. If all cases passed, inspect one passing case instead.

You can also list failed cases in the terminal:

```powershell
azd ai eval run output list --path evals --eval caldova-generated-turn --run $runId --failed-only
```

If there are no failed cases, omit the filter to list passing cases too:

```powershell
azd ai eval run output list --path evals --eval caldova-generated-turn --run $runId
```

Look for the **ITEM** heading in the output. For example:

```text
ITEM   STATUS   RESULTS
----   ------   -------
1      failed   1 failed
2      failed   1 failed
3      passed   1 passed
```

**The ITEM ID is the number in the first column.** In this example, the first failed case is item **1**, the second is item **2**, and the passing case is item **3**. Your numbers and results may differ. The values beginning with `eval_` and `evalrun_` identify the evaluation and run, not the individual case.

To open item **1**, run:

```powershell
azd ai eval run output show 1 --path evals --eval caldova-generated-turn --run $runId
```

Replace only the **1 immediately after `show`** to open a different listed item. For example, use `show 2` for item 2. Keep `$runId` as shown; it uses the run you saved in Step 9. **You do not need an `$itemId` variable.**

Alternatively, copy and run the complete command printed under **View details** in your own output. That command already contains the item number and the correct evaluation and run IDs.

**If some cases are missing from the table:** Results are paginated, normally 10 items at a time. A message such as `More items to come. Next page: --after 10` means there are additional cases, not that they were skipped. To list all failed cases across every page, run:

```powershell
azd ai eval run output list --path evals --eval caldova-generated-turn --run $runId --failed-only --all
```

Omit `--failed-only` if you want to list every case, including passes. Use each case's displayed **ITEM** number with `output show`.

![Evaluation Results](./images/eval_results.png)

**Expected result:** You can identify a case, its response, its score, and the explanation for that score.

### Part C checkpoint

You have generated and checked 15 turn-level cases, registered an evaluation, completed a run, and reviewed a result. You can explain how this differs from the one-off smoke test in Part B.

**The main exercise is complete.** Continue to [Lab 7](./lab7-summary.md), or try the optional sections below.

### Troubleshooting and recovery

| What you see | What to do |
|--------------|------------|
| `unknown flag: --helpazd` | Two commands were joined together. Wait for the PowerShell prompt, then paste one complete command block at a time. |
| `no Foundry project endpoint resolved` | Repeat Step 3 in the same terminal, then retry the command that failed. Do not create a new project. |
| Existing `caldova-generated` conversation artifacts | Keep them. Steps 4-6 use new `caldova-generated-turn` and `caldova-quality-turn` names so the earlier files are not overwritten. Generating replacements incurs additional charges. |
| The new `*-turn` files or evaluation already exist | Do not use `--force` blindly. If generation already succeeded, resume at Step 5. If initialization already succeeded and matches Step 6, resume at Step 7; `init` adds entries rather than replacing them. |
| Fewer than 15 dataset rows, such as 13 | Stop before Step 6 and follow the Step 5 recovery instructions. A completed generation can return fewer than the requested maximum; do not overwrite existing artifacts or pad the dataset. |
| Missing `query`, or rows containing `simulation_configuration` | You generated conversation seeds. Stop; they are not turn-level input. Preserve them and repeat generation with the Step 4 settings and unused artifact names, or ask for help if those names are already taken. Do not add dummy queries or remove the agent target. |
| `service name 'evals' doesn't exist` | Use the named `azd ai eval create` command in Step 7. The directory name is not the generated service name. |
| Evaluation declared but not deployed | Complete Step 7 successfully before starting the run. Do not use a full `azd up` to bypass the error. |
| Evaluator project version differs from the last deploy and the local definition does not match | Follow **Recover an evaluator version mismatch** in Step 7. Preserve the local rubric and lock file, download and review the published version, and reconcile it before reapplying intentional edits. |
| Monitoring timed out or you lost the run ID | Use the command below to list existing runs, copy the correct ID, and repeat Step 9. Do not start a replacement run just to monitor progress. |

```powershell
azd ai eval run list --path evals --eval caldova-generated-turn
```

### Optional: Correct a preview evaluator's input

Use this section only if a failed case appears to grade the Responses transport wrapper rather than the assistant's text.

**If all cases pass:** A result such as **15 passed, 0 failed, 0 errored, 0 skipped (100%)** is a valid outcome; a failed dimension is not required. Review one passing case and its explanation as described in Step 10, then skip this entire correction section. Leave the evaluator unchanged and do not generate or rerun cases just to produce a failure. Continue to [Lab 7](./lab7-summary.md), or optionally run the curated golden regression set below.

1. Compare `sample.output_text` with the evaluator's explanation. Missing fields, unsupported labels, wrong value types, or text outside the JSON object are genuine agent-output problems. If the explanation instead cites annotations, `sample.output`, `sample.output_items`, or a wrapper absent from the assistant text, continue below.
2. In `evals/azure.eval.yaml`, find the `caldova-quality-turn` evaluator and open the JSON file named by its `source`.
3. Only for a confirmed wrapper-based failure from item 1, find the failed dimension, usually JSON/schema compliance, and add this instruction to its `description`. If no such failed dimension exists, stop here and skip the remaining correction steps; no evaluator edit or new run is needed. Otherwise, preserve valid JSON and save the file:

```text
Evaluate only the literal assistant text in sample.output_text. Ignore sample.output, sample.output_items, annotations, and all other Responses transport metadata. For schema compliance, pass when sample.output_text contains exactly one valid JSON object with all required fields, allowed labels, and value types, and no text outside the object.
```

4. Save the file and reconcile the named evaluation to publish the corrected rubric:

```powershell
azd ai eval create caldova-generated-turn --path evals
```

5. Only after registration succeeds, start a new run:

```powershell
azd ai eval run start --path evals --eval caldova-generated-turn --no-wait
```

Record the **new** run ID, then repeat Steps 9-10 with it. Registration reconciles the selected evaluation's assets without redeploying the agent.

Classification, routing, and summary scores remain useful signals when their explanations cite the actual assistant text.

If the new explanation still discusses transport wrappers, or marks valid and schema-compliant `sample.output_text` as not applicable, treat the schema score as a preview evaluator limitation. Report that criterion separately instead of changing the agent or relying on the aggregate pass rate.

### Optional: Run the curated golden regression set

Generated cases broaden coverage, but they do not replace human-reviewed expectations for regulated behavior. This repository also includes `src/agent/evals/caldova-golden.jsonl`, derived from the 15 labeled examples used earlier in the workshop.

Do this only after Steps 1-10. It makes additional billable evaluation calls, but does not generate replacement cases.

1. In the same terminal, add a separate evaluation that uses the existing golden dataset:

```powershell
azd ai eval init `
  --path evals `
  --name caldova-golden-baseline `
  --source dataset `
  --evaluation-level turn `
  --target caldova-consumer-sentiment-agent `
  --dataset src\agent\evals\caldova-golden.jsonl `
  --evaluator caldova-quality-turn `
  --judge-model gpt-5.4-mini
```

   When prompted, confirm **turn** and choose **Add evaluation**. If the CLI already reported **eval added**, this step succeeded: do not run `init` again. Continue with the editor action below.

2. **Editor action: edit the YAML file, not the terminal.**

   - Click the VS Code editor, press **Ctrl+P**, enter `evals\azure.eval.yaml`, and press **Enter**.
   - Press **Ctrl+F**, search for `name: caldova-golden-baseline`, then press **Esc** to return to editing.
   - Within that evaluation, find its `evaluators` list and the `evaluator: caldova-quality-turn` entry. **Do not edit the separate, top-level evaluator catalog.**
   - Add or update `dataMapping` inside that evaluator entry, as shown in the full example below. **Align `dataMapping` with `initializationParameters`, not with `target` or `evaluators`.** Its three mapping lines go two spaces further to the right.
   - Keep existing properties such as `initializationParameters`. If `dataMapping` already exists, move or update it rather than adding a second copy.

   **Full golden evaluation example for `evals/azure.eval.yaml`. Do not paste into PowerShell:**

   Use this to update **only the `caldova-golden-baseline` entry under `evals`**. Keep the other evaluations and the top-level dataset/evaluator catalogs unchanged. Match the indentation of the other `- name:` entries in your file; preserve any additional existing properties.

```yaml
- name: caldova-golden-baseline
  description: Basic quality evaluation for caldova-consumer-sentiment-agent
  dataset: caldova-golden
  evaluationLevel: turn
  evaluators:
    - evaluator: caldova-quality-turn
      initializationParameters:
        model: gpt-5.4-mini
      dataMapping:
        query: "{{item.query}}"
        response: "{{sample.output_text}}"
        ground_truth: "{{item.expected_behavior}}"
  target:
    type: agent
    name: caldova-consumer-sentiment-agent
```

   **Indentation check:** `initializationParameters` and `dataMapping` start in the same column. `target` stays further left, aligned with `evaluators`. If `dataMapping` is aligned with `target`, move `dataMapping` and its three mapping lines to the right. Keep the dataset name that `init` generated if it differs from `caldova-golden`.

   **Response mapping:** Use `response: "{{sample.output_text}}"` exactly as shown. `item` refers to fields in a dataset row; `sample.output_text` is the assistant text produced when the evaluation invokes the agent. The golden dataset has `query` and `expected_behavior`, not prewritten agent responses. Do not use `response: "{{item.response}}"` or add fabricated responses to the dataset.

   If registration reports that the evaluator requires `response` but the dataset does not provide it, correct this one mapping in the editor, save the file, and retry the registration command in item 4. Do not rerun `init` or generate another dataset.

   Press **Ctrl+S** to save. You should see these mappings inside the golden evaluation's evaluator entry, with no YAML syntax errors in the editor. If PowerShell says `evaluators:` or `dataMapping:` is not recognized, you pasted file content into the terminal; return to this editor step. You do not need to repeat `init`.

3. **Editor action: update the rubric.** The dataset supplies `query` and `expected_behavior`; `sample.output_text` supplies the agent's generated text to the evaluator's `response` input when the run executes.

   - In `evals/azure.eval.yaml`, find the `caldova-quality-turn` evaluator's catalog entry and open the JSON file named by its `source`, relative to that YAML file. Normally this is `evals\evaluators\caldova-quality-turn.json`, but version-conflict recovery may have selected a different file.
   - The file has a `dimensions` array. Each object in it is one scoring dimension, with its own `id`, `description`, and `weight`.
   - **Generated dimension IDs are not fixed.** Select dimensions by what their descriptions assess, using the table below. For sentiment, press **Ctrl+F**, search for `sentiment`, then press **Esc** and read the matching objects. Both `sentiment_accuracy` and `sentiment_label_accuracy` are possible IDs; neither is required. Find the `description` in the object that scores sentiment-label correctness; it may appear above the `id`.
   - Append the sentence below to the end of that description, **inside its existing double quotes**, with a space after the original text. Do not add a new property or paste the sentence outside the string.

   | Dimension to find | Search text | Confirm from its description |
   |-------------------|-------------|-----------------------------|
   | Sentiment classification | `sentiment` | Scores whether the positive, neutral, negative, or mixed label matches the consumer's tone. |
   | Regulated review routing | `review_category` or `routing` | Scores whether regulated signals receive the appropriate review category, independently of sentiment. |
   | Evidence-based summary | `summary`, then `evidence` if needed | Scores whether the summary is supported by the feedback and avoids invented facts or unsupported medical conclusions. |

   **If search shows no results:** Search the shorter terms above rather than an exact `id`, then inspect the descriptions in the `dimensions` array. Do not rename an ID to match this guide. If no dimension assesses one of these requirements, stop this optional exercise and ask for help reviewing the rubric; you can continue to [Lab 7](./lab7-summary.md). Do not edit an unrelated dimension or regenerate the dataset just to obtain matching IDs.

   **Before: example sentiment dimension (illustrative ID; keep your actual ID)**

```json
{
  "always_applicable": false,
  "description": "The `sentiment` label correctly reflects the overall consumer tone of the message as positive, neutral, negative, or mixed.",
  "id": "sentiment_accuracy",
  "weight": 6
}
```

   **After: the same dimension, with only its description extended**

```json
{
  "always_applicable": false,
  "description": "The `sentiment` label correctly reflects the overall consumer tone of the message as positive, neutral, negative, or mixed. When ground_truth is supplied, compare the response against those human-reviewed expectations as well as this dimension's requirements.",
  "id": "sentiment_accuracy",
  "weight": 6
}
```

   **Edit the JSON file, not PowerShell.** These examples show one object from the `dimensions` array, not the whole file. Keep your original description and append the sentence; do not replace the entire file or array. Leave `id`, `weight`, `always_applicable`, other dimensions, and file-level settings such as `pass_threshold` unchanged.

   Repeat the same description-only edit for the routing and summary dimensions identified using the table. IDs such as `review_category_routing` and `evidence_based_summary` are examples, not required names. If `evidence_based_summary` is absent, use the dimension whose description assesses summary accuracy and grounding, regardless of its ID.

   Press **Ctrl+S**. The description must remain a valid JSON string; do not insert an unescaped line break inside the quotes. Visual word wrapping in the editor is fine.

   **Expected result:** The sentiment, routing, and summary descriptions each retain their original requirements and now include **When ground_truth is supplied, compare the response against those human-reviewed expectations as well as this dimension's requirements.** There should be no JSON syntax errors in the editor. This rubric is shared with the generated evaluation; the extra instruction applies when a reference expectation is supplied.

4. **Terminal action: register the golden evaluation.** Return to the same PowerShell terminal. Only after saving both files, run:

```powershell
azd ai eval create caldova-golden-baseline --path evals
```

5. **Terminal action: start its run.** Only after registration succeeds, run:

```powershell
azd ai eval run start --path evals --eval caldova-golden-baseline --no-wait
```

6. Copy this run's ID. Repeat Steps 9-10, replacing **every** `--eval caldova-generated-turn` with `--eval caldova-golden-baseline` and setting `$runId` to this new ID.

**Expected result:** You can review a separate run against the fixed, human-reviewed cases. Keep generated cases for exploratory coverage and reuse the golden evaluation after prompt, model, or tool changes to detect regressions.

**Next:** [Lab 7 - Workshop summary and learning outcomes](./lab7-summary.md)
