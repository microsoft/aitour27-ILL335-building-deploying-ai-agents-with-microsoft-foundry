# ILL335 — Session Delivery Resources

**Building & Deploying AI Agents with Microsoft Foundry**

This folder contains the presenter and attendee decks plus the guidance needed to run **ILL335** at AI Tour or re-deliver it at user groups, internal enablement sessions, community events, and customer workshops.

The current lab is built for the AI Tour FY27 Skillable environment. Attendee projects and model deployments are pre-provisioned; self-paced presenters can use [`../setup/SETUP.md`](../setup/SETUP.md) to create an equivalent environment.

## Core materials

| Item | Link | Notes |
| --- | --- | --- |
| Delivery deck | [ILL335 Presentation](https://github.com/microsoft/aitour27-ILL335-building-deploying-ai-agents-with-microsoft-foundry/blob/main/delivery-resources/ILL335-Attendee-Walkthrough-FY27.pptx)  | PowerPoint presentation |
| Session recording | [ILL335 Video](https://aka.ms/aitour27/ILL335/youtube) | Video delivery |

---

## 👤 Who this guide is for

- **Lead presenters** delivering the 75-minute lab session on stage or in a hands-on lab room
- **Proctors** supporting attendees on the floor during the lab
- **Community speakers / MVPs** re-delivering this content at user groups, meetups, or internal events
- **Customer-facing engineers** running this as a customer workshop

If you are an **attendee** working through the lab, start at the root [README](../README.md) and [docs/lab1-discover-models.md](../docs/lab1-discover-models.md) instead.

---

## ⏱ Session at a glance

| Block | Duration | Content type | Notes |
|:------|:---------|:-------------|:------|
| Introduction — Caldova scenario, what is Microsoft Foundry | 3 min | Speaker only | Set the story: attendees are an AI developer on Caldova's commercial digital and customer engagement team |
| Lab 1: Discover Models in Microsoft Foundry | 10 min | Guided lab | Foundry Toolkit model catalog and playground in VS Code |
| Lab 2: Verify the Foundry Project | 5 min | Guided lab | Confirm `.env`, dependencies, CLI tools, and the pre-provisioned project |
| Lab 3: Connect and Send Your First Inference | 12 min | Demo | `AIProjectClient` + `get_openai_client()` |
| Lab 4: Build a Consumer Sentiment Analysis Application for Caldova | 20 min | Demo | Structured JSON prompt → governed routing logic → batch run |
| Lab 6: Deploy a Hosted Agent | 20 min | Guided lab | Test with Agent Inspector, then deploy Python source with `azd up` |
| Lab 7: Summary, takeaways, Q&A, next steps | 5 min | Speaker only | Point to Lab 5 as self-paced extension |
| **Total** | **75 min** | | |

**Lab 5 (Model Comparison)** is intentionally **not** in the 75-minute flow. It is a self-paced extension attendees can complete at home — call it out at the end.

Full timing detail is in [`../session-outline.md`](../session-outline.md).

---

## 🎯 Learning outcomes you are delivering

Reinforce these three messages at the start, in the middle, and at the close:

1. Attendees can **discover and connect** to hosted models in Microsoft Foundry — zero to a working inference call in minutes.
2. Attendees can **build a production-quality consumer sentiment analysis pipeline** that returns structured JSON, with governed routing logic on top.
3. Attendees can **deploy a hosted agent directly from Python source** with `azd up` and the `microsoft.foundry` provider.

If an attendee leaves with only one of these, make it #1 (Foundry + OpenAI SDK pattern is the foundation).

---

## ✅ Pre-session checklist (do this 24–48 hours before delivery)

### Trainer environment
- [ ] Complete the Skillable lab end-to-end **at least once** on the exact machine and tenant used for delivery.
- [ ] Confirm the repository opens from `C:\Users\LabUser\Desktop\AI-Tour-ILL335-main` and the Foundry Toolkit is installed and signed in.
- [ ] Run `python -X utf8 src/tests/validate_lab.py` and confirm the result is `PASS` with zero failed checks.
- [ ] Run `src/01_first_inference.py`, `src/02_sentiment_analysis.py`, and the local agent flow to confirm the pre-provisioned endpoint and model work.
- [ ] Verify Azure CLI and `azd` are authenticated to the same tenant and subscription.
- [ ] Confirm `azd` 1.27.1 or later and install the current extension bundle with `azd ext install microsoft.foundry`.
- [ ] Run `azd up` once in a trainer environment so you know the deployment duration and expected output. This creates billable Azure resources.

### Slides, screen, network
- [ ] Confirm the slide deck version matches the lab version (check the title slide against `session-outline.md`).
- [ ] Increase terminal and editor font size — aim for back-of-room readability (16pt+ terminal, 18pt+ editor).
- [ ] Hide secrets: scrub `.env`, browser tabs, and shell history. Use a fresh terminal profile if possible.
- [ ] Have the Foundry portal ([ai.azure.com](https://ai.azure.com)) signed in on a separate tab/window.
- [ ] Test your microphone, screen share, and recording (if applicable).

### Attendee environment (Skillable lab rooms)
- [ ] Confirm each seat can sign in to the VM and that the Azure username, password or Temporary Access Pass, and VM password appear in the Skillable instructions panel.
- [ ] Confirm the repo is already cloned, `.env` is configured, and the Foundry project includes the **gpt-5.4-mini** deployment.
- [ ] Confirm the Foundry Toolkit, Python, Azure CLI, `azd`, Git, and VS Code are available on every VM.
- [ ] Keep the [Skillable guide](../docs/skillable/skillable.md) and [Lab 1](../docs/lab1-discover-models.md) available to proctors.

### Proctors
- [ ] Make sure every proctor has done the lab themselves at least once.
- [ ] Share the [troubleshooting cheat sheet](#-troubleshooting-cheat-sheet-for-proctors) below.
- [ ] Agree on a hand-signal / raised-card system so attendees can flag for help without interrupting the speaker.

---

## 🧭 Delivery flow — what to say and do, lab by lab

### Introduction (3 min) — set the scene

- Introduce **Caldova** (Microsoft's fictional global pharmaceutical company, mid-transformation) and the role attendees play: an **AI developer** on Caldova's commercial digital and customer engagement team.
- Consumer feedback scenario: Caldova's B2C channels receive feedback about products such as allergy relief tablets and topical relief gel, plus support interactions, that needs to be analyzed for sentiment and independently checked for regulated signals before it reaches the dashboard.
- One-line definition of Microsoft Foundry: *production-ready hosted models with managed infrastructure, no fine-tuning required, OpenAI SDK compatible.*
- Show the end state on a slide: a deployed agent answering sentiment analysis requests. "By the end of this lab, you'll build this."

### Lab 1 — Discover Models (10 min)

- Open the **Foundry Toolkit** in VS Code and navigate to **Developer Tools → Model Catalog**.
- Talk through filters: provider, capability (chat, embeddings), modality, deployment options.
- Compare **gpt-5.4-mini**, **gpt-5.4**, and **Phi-4** — frame as "cost, latency, quality" trade-off.
- Open the model card and point out details, benchmarks, Responsible AI, and licensing.
- Optional: paste a piece of Caldova consumer feedback into the Toolkit **Model Playground** and show a sentiment label.

**Common attendee question:** *"How do I know which model to choose?"* — Answer: start with the cheapest model that meets your quality bar, then measure. Lab 5 shows the comparison workflow.

### Lab 2 — Verify the Foundry Project (5 min)

- Explain that Skillable has already provisioned the attendee project and model deployment.
- Confirm `.env` contains `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME`. Do not display their values on a shared screen.
- Run `python -X utf8 src/tests/validate_lab.py`.
- Confirm the output ends with zero failed checks and `Result: PASS -- lab is ready!`.
- If a check fails, use the message from the validator rather than reprovisioning the environment.

### Lab 3 — First Inference (12 min)

- Open [`src/01_first_inference.py`](../src/01_first_inference.py).
- Walk through line by line:
  - `DefaultAzureCredential()` — explain the credential chain
  - `AIProjectClient(...)` — the project endpoint pattern
  - `project_client.get_openai_client()` — returns the OpenAI-compatible client
  - `client.responses.create(...)` — separates `instructions` from `input`
- Run it. Show `response.output_text`, `response.status`, and input/output/total token usage.
- Change one instruction or input, then demonstrate a follow-up with `previous_response_id`.

### Lab 4 — Build the Consumer Sentiment Analysis Application (20 min)

- Open [`src/02_sentiment_analysis.py`](../src/02_sentiment_analysis.py).
- Show the **structured JSON system prompt** — explain why structured output is the difference between a demo and a production app.
- Show the sentiment schema: `POSITIVE` / `NEUTRAL` / `NEGATIVE` / `MIXED` with `confidence`, `topics`, `review_category`, and `summary`.
- Emphasize that **sentiment and regulated routing are independent** — a positive review can still contain a potential adverse event, and vice versa.
- Walk through the **governed routing layer**:
  - Any `review_category` other than `NONE` → escalate for human review
  - High-confidence, non-regulated feedback → add to the sentiment dashboard
  - Low-confidence, non-regulated feedback → route to a human for a second look
- Run against [`src/sample_feedback.json`](../src/sample_feedback.json) in batch mode.
- Run an interactive analysis (let an attendee suggest a piece of feedback if you have time).
- Show [`src/tests/test_sentiment.py`](../src/tests/test_sentiment.py) — reinforce that *real apps have tests*.

**Don't skip:** the confidence threshold conversation and the reminder that the model must never determine causality, assess seriousness, or give medical advice. This is the most-cited takeaway from previous deliveries.

### Lab 6 — Deploy a Hosted Agent (20 min)

- Open `src/agent/app.py` and walk through `FoundryChatClient`, `ResponsesHostServer`, and `default_options={"store": False}`.
- Open `azure.yaml` and highlight direct code deployment, Python 3.13, and Responses protocol 2.0.0.
- Press **F5** with **Debug Agent with Agent Inspector** and verify one local JSON response before cloud deployment.
- Run `azd up` for the first deployment. Explain that the `microsoft.foundry` provider provisions the project and model, then remotely builds and hosts the Python source on managed infrastructure.
- When deployment finishes, check `azd ai agent show --output json`, then invoke the agent with `azd ai agent invoke caldova-consumer-sentiment-agent "The delivery was late, but support kept me informed."`.
- Use `azd deploy` only for later code-only updates to an environment already provisioned by this project.
- Optional: tail logs from the agent to show observability.
- Optional self-paced extension: generate a structured evaluation with `azd ai agent eval generate`, inspect `eval.yaml` and its rubric, then run it with `azd ai agent eval run`.
- Contrast the generated cases with `src/agent/evals/caldova-golden.jsonl`: generated data expands coverage, while curated cases protect regulated-routing behavior across versions.

**If deployment is slow:** keep the narrative going — talk about platform-managed runtime, history, scaling, and identity.

**Cost and timing note:** evaluation generation is a billable preview feature and can take several minutes. Do not include it in the core 75-minute delivery unless the deployment finishes early.

### Lab 7 — Wrap, takeaways, Q&A (5 min live; 10 min self-paced module)

- Recap the journey in one breath: *catalog → project → first call → consumer sentiment analysis pipeline → hosted agent.*
- Call out **Lab 5** as a self-paced extension — attendees compare gpt-5.4-mini vs gpt-5.4 at home, including the hybrid "cheap first, escalate when uncertain" pattern.
- Point to related AI Tour sessions listed in the current event agenda.
- Direct attendees to:
  - The AI Tour ILL335 lab repository supplied with the session
  - [Microsoft Foundry docs](https://learn.microsoft.com/azure/ai-foundry/)
  - [Microsoft AI learning hub](https://learn.microsoft.com/ai/)
- Take questions in chat / Q&A — don't run over.

---

## 🧯 Troubleshooting cheat sheet (for proctors)

The vast majority of attendee issues fall into one of these buckets. Triage in this order:

| Symptom | Most likely cause | Fix |
|:--------|:------------------|:----|
| `az login` / `azd auth login` loops or fails | Wrong tenant or stale token | `az logout` then `az login --tenant <tenant-id>`; same for `azd auth logout` / `login` |
| `setup.ps1` fails on resource provider not registered | Subscription is missing `Microsoft.CognitiveServices` | `az provider register --namespace Microsoft.CognitiveServices` |
| Model deployment fails with quota error | No quota for **gpt-5.4-mini** in chosen region | Switch to a region with quota (see [armsetup.md](../setup/armsetup.md)) or request quota |
| `DefaultAzureCredential` fails in Python | Not signed in, or wrong tenant active | `az login`; verify `az account show` matches the project's subscription |
| `401`/`403` on first inference call | RBAC role assignment hasn't propagated yet | Wait 1–2 minutes; re-run. If still failing, confirm role assignment in the portal |
| `ModuleNotFoundError` | Virtual env not activated or `pip install -r requirements.txt` not run | Activate venv; reinstall |
| `azd up` fails during dependency resolution | Agent package or runtime mismatch | Check `src/agent/requirements.txt` and the Python 3.13 setting in `azure.yaml` |
| `azd up` is slow | Foundry resources and the hosted runtime are being prepared | Expected on a first deployment; keep narrating |
| Agent invoke returns empty / weird response | Wrong deployment name in `.env` | Re-run setup script or manually align `MODEL_DEPLOYMENT_NAME` |
| Attendee can't find the lab | Sent to wrong tab | Direct to [docs/lab1-discover-models.md](../docs/lab1-discover-models.md) |

If you hit something **not** on this list, write it down — we want to add it. File an issue against the repo (see [AGENTS.md](../AGENTS.md) for the issue process).

---

## 🛠 Tips for proctors on the floor

- Stand at the back/side; scan for raised hands or stuck attendees (frozen screens, confused expressions).
- When helping: ask "what error are you seeing?" — read the error, then act. Don't drive their keyboard unless they ask.
- If multiple attendees hit the same problem, flag the lead presenter — they can address it once for the room.
- Don't get stuck on one attendee for more than 5 minutes. Get them past the blocker (even by sharing a working `.env`) so the rest of the room keeps moving.
- For quota / subscription issues that can't be fixed in-room, pair them with a neighbour or point them to the [self-paced setup](../setup/SETUP.md) so they can finish later.

---

## 🔁 Re-delivering this lab (community events, internal training)

You are welcome and encouraged to re-deliver this content. A few asks:

- **Keep the Caldova narrative** — it ties this lab to the broader Microsoft Foundry demo storyline (an AI developer on Caldova's commercial digital and customer engagement team building a B2C consumer sentiment analysis application).
- **Use the latest version** of the repo from GitHub. Lab steps and SDK calls evolve; pin yourself to `main`.
- **Don't commit secrets** to forks. Every demo subscription has its own `.env`. See [AGENTS.md](../AGENTS.md).
- **Cite the source** on your title slide as *Microsoft AI Tour ILL335*.
- **Adapt the timing** as needed:
  - **30-min lightning version:** Intro + Lab 1 + Lab 3 + Lab 7 (skip provisioning, use a pre-built project)
  - **60-min meetup version:** Intro + Labs 1–4 + Lab 7
  - **Full 75-min AI Tour version:** as documented above
  - **Half-day workshop:** all labs including Lab 5 (model comparison), with longer hands-on time per section

---

## 📚 Related resources

- [`ILL335-Train-the-Trainer-FY27.pptx`](ILL335-Train-the-Trainer-FY27.pptx) — presenter readiness, timing, checkpoints, and recovery guidance
- [`ILL335-Attendee-Walkthrough-FY27.pptx`](ILL335-Attendee-Walkthrough-FY27.pptx) — attendee welcome and lab journey deck
- [`../session-outline.md`](../session-outline.md) — official session outline with timing per block
- [`../techspec.md`](../techspec.md) — technical specification for the lab
- [`../setup/SETUP.md`](../setup/SETUP.md) — attendee setup guide
- [`../setup/armsetup.md`](../setup/armsetup.md) — ARM-based setup and region/quota notes
- [`../cleanup/CLEANUP.md`](../cleanup/CLEANUP.md) — resource cleanup instructions
- [`../AGENTS.md`](../AGENTS.md) — repo contribution and issue-filing guidelines

---

## ❓ Questions or feedback on delivery

If you spot a gap in this guide, or you want to share what worked / didn't work when you delivered this lab, please **open an issue** on the repo using the issue templates in [`.github/ISSUE_TEMPLATE/`](../.github/ISSUE_TEMPLATE/). Tag it with the `train-the-trainer` label (or request the label if it doesn't exist yet).

Good luck — and have fun delivering ILL335. 🚀
