# AI Tour Session Outline

**Title of session:** Building & Deploying AI Agents with Microsoft Foundry

**Session ID:** ILL335

**As of:** 04/24/2026

---

## Session Flow: 75 minutes (Lab 5 available as self-paced extension)

**Speaker:** Lee Stott

---

### Act One: Discover and Connect (23 min)

**Introduction — Setting the Scene**
3 min | Lee Stott
Content: SPEAKER-ONLY
Introduce the Caldova scenario: attendees play the role of an AI developer on Caldova's commercial digital and customer engagement team, tasked with building a B2C consumer sentiment analysis tool for Microsoft's fictional global pharmaceutical company. Explain what Microsoft Foundry is and why developers should care — production-ready hosted models, no fine-tuning required.

**Lab 1: Discover Models in Microsoft Foundry**
10 min | Lee Stott
Content: DEMO
Attendees navigate the Foundry portal (ai.azure.com), browse the model catalog, evaluate model capabilities (gpt-5.4-mini, gpt-5.4, Phi-4), check quota and region availability, and optionally test a Caldova consumer feedback sentiment prompt in the Playground.

**Lab 2: Create and Configure a Foundry Project**
10 min | Lee Stott
Content: DEMO
Attendees run the one-command setup script (`setup.ps1` / `setup.sh`) which provisions all Azure infrastructure via azd and Bicep — AI Services account, Foundry project, model deployment (gpt-5.4-mini), monitoring, RBAC, and local `.env` configuration. Covers what azd does and why Infrastructure-as-Code matters.

---

### Act Two: Analyze and Govern (32 min)

**Lab 3: Connect and Send Your First Inference**
12 min | Lee Stott
Content: DEMO
Write Python code using `AIProjectClient` (Azure AI Projects SDK) to authenticate with `DefaultAzureCredential`, obtain an OpenAI-compatible inference client via `get_openai_client()`, and send a first Responses API request. Explore instructions, input, response status, token usage, multi-turn continuity, and error scenarios.

**Lab 4: Build a Consumer Sentiment Analysis Application**
20 min | Lee Stott
Content: DEMO
Build a complete sentiment analysis pipeline for Caldova consumer feedback. Design a structured system prompt that returns JSON with sentiment (POSITIVE / NEUTRAL / NEGATIVE / MIXED), confidence, topics, and an independent review_category (NONE / POTENTIAL_ADVERSE_EVENT / PRODUCT_QUALITY_COMPLAINT / MEDICAL_INQUIRY / CONTENT_SAFETY), add a business logic layer that escalates regulated signals and routes low-confidence results for review. Process sample feedback in batch and interactive modes.

**Lab 5: Compare Model Outputs (Self-Paced Extension — not included in 75-min session)**
15 min | Lee Stott
Content: DEMO
Run identical Caldova consumer feedback through gpt-5.4-mini and gpt-5.4 to compare classification quality, confidence scores, latency, and cost. Demonstrate a hybrid escalation pattern — cheap model first, escalate to premium model when confidence is low. Discuss model selection as a product decision. *Attendees can complete this lab at home using the lab instructions.*

---

### Act Three: Deploy and Wrap Up (20 min)

**Lab 6: Deploy a Hosted Agent**
15 min | Lee Stott
Content: DEMO
Deploy the Caldova consumer sentiment analysis logic as a hosted agent using the Microsoft Agent Framework SDK. Review `app.py` and the direct-code `codeConfiguration` in `azure.yaml`, including Python 3.13 and Responses protocol 2.0.0. Deploy to Foundry Agent Service with `azd deploy`, then test the live agent with the Foundry Toolkit playground.

**Lab 7: Summary, Key Takeaways, Q&A, and Next Steps**
5 min | Lee Stott
Content: SPEAKER-ONLY, GRAPHICS
Recap the full journey: model discovery → project setup → first inference → sentiment analysis pipeline → hosted agent. Point attendees to Lab 5 (model comparison) as a self-paced extension. Share related AI Tour resources and next steps. Take audience questions through chat.

---

## Goals

- **Goal 1:** Attendees can discover, provision, and connect to hosted models in Microsoft Foundry using the Azure AI Projects SDK and OpenAI client — going from zero to a working inference call in minutes.
- **Goal 2:** Attendees can build a production-quality consumer sentiment analysis pipeline that classifies feedback as positive, neutral, negative, or mixed while independently routing regulated signals for human review using structured prompts and business logic — and compare outputs across models to make informed deployment decisions.
- **Goal 3:** Attendees can deploy application logic as a hosted agent on Foundry Agent Service using the Microsoft Agent Framework and `azd deploy` — no container packaging or infrastructure management required.

---

## Nurture (Marketing/Sales Alignment)

This lab targets developers and AI engineers who are evaluating Microsoft Foundry for production AI workloads. The session demonstrates a complete developer workflow — from model discovery through deployment — using a realistic enterprise scenario (Caldova consumer sentiment analysis). Key value propositions reinforced: no fine-tuning needed, OpenAI SDK compatibility, managed infrastructure for agents, and the `azd` developer experience for provisioning and deployment. Attendees leave with working code they can adapt to their own use cases, driving adoption of Microsoft Foundry, Azure AI Services, and the Azure Developer CLI.

---

## Leave Behind Resources

- **Resource 1:** [Microsoft Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/) — Official docs for Foundry projects, models, and agents
- **Resource 2:** [OpenAI Responses API](https://learn.microsoft.com/azure/foundry/openai/how-to/responses) — Reference for the API pattern used in this lab
- **Resource 3:** AI Tour ILL335 lab repository — Complete source code, lab instructions, and infrastructure templates supplied with the session
- **Resource 4:** [Azure Developer CLI documentation](https://learn.microsoft.com/azure/developer/azure-developer-cli/) — Getting started with azd for provisioning and deploying
- **Resource 5:** [Foundry Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio) — Extension for working with Foundry projects in VS Code
- **Resource 6:** [Microsoft AI learning hub](https://learn.microsoft.com/ai/) — Continue the learning journey after AI Tour
