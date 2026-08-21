# Lab 7: Workshop summary and learning outcomes

> **Duration:** ~10 minutes

## Objective

Review the complete journey from discovering a model in the Foundry catalog to deploying a production-ready hosted agent for Caldova's B2C consumer sentiment analysis. This lab consolidates what you built, the skills you acquired, and where to go next.

## What you built

Across the labs, you -- as an AI developer on Caldova's commercial digital and customer engagement team -- constructed a **consumer sentiment analysis pipeline** end-to-end, from a blank terminal to a cloud-hosted agent accessible via REST API.

![mermaid_diagram3.png](../images/mermaid_diagram3.png)

## Lab-by-lab recap

### Lab 1: Discover models in Microsoft Foundry

| | |
|---|---|
| **What you did** | Browsed the Foundry model catalog in the Foundry Toolkit for VS Code, evaluated model properties, tested Caldova consumer sentiment prompts in the playground |
| **Key skill** | Selecting the right model for a task based on capabilities, pricing, and quotas |
| **Outcome** | Chose **gpt-5.4-mini** as the model for Caldova's consumer sentiment analysis |

### Lab 2: Verify your Foundry project

| | |
|---|---|
| **What you did** | Verified the pre-provisioned Foundry project and validated the local environment with the automated validation script |
| **Key skill** | Environment configuration, `.env` validation, and readiness checks |
| **Outcome** | A confirmed Foundry project and a validated local `.env` configuration |

### Lab 3: Connect and send your first inference

| | |
|---|---|
| **What you did** | Reviewed Python code to authenticate with **DefaultAzureCredential** and send a Responses API request |
| **Key skill** | Using the Azure AI Projects SDK for model inference -- instructions, input, status, and token usage |
| **Outcome** | A working script (`src/01_first_inference.py`) that sends prompts and receives model responses |

**Core concept:** Responses API calls separate durable `instructions` from the current `input`, and return convenient output text plus status and usage metadata.

### Lab 4: Build a consumer sentiment analysis application for Caldova

| | |
|---|---|
| **What you did** | Designed a system prompt for structured JSON sentiment analysis, built a governed routing layer with confidence thresholds, processed batches of feedback |
| **Key skill** | Prompt engineering for structured output, building decision logic around model responses |
| **Outcome** | A complete sentiment analysis app (`src/02_sentiment_analysis.py`) that classifies Caldova feedback and independently flags regulated review categories |

**Core concept:** The model provides sentiment and category signals; your code makes the routing decisions -- and never determines causality, seriousness, or medical advice.

### Lab 5: Compare model outputs

| | |
|---|---|
| **What you did** | Ran the same Caldova feedback through gpt-5.4-mini and gpt-5.4, compared quality, latency, and cost |
| **Key skill** | Multi-model evaluation, cost-performance trade-off analysis, hybrid escalation patterns |
| **Outcome** | A comparison script (`src/03_model_comparison.py`) with side-by-side results and an optional hybrid routing mode |

**Core concept:** Cheaper models often perform well enough for most inputs. Reserve expensive models for low-confidence cases.

### Lab 6: Deploy a hosted agent

| | |
|---|---|
| **What you did** | Tested Caldova's agent locally with the Agent Inspector, deployed it as a hosted-agent, and tested it in the hosted-agent playground |
| **Key skill** | Direct-code deployment, the Agent Framework SDK, and hosted-agent lifecycle management |
| **Outcome** | A live, cloud-hosted **caldova-consumer-sentiment-agent** accessible via the OpenAI Responses API |

**Core concept:** A hosted agent turns local Python code into a managed service while Foundry handles runtime infrastructure and conversation history.

**Optional extension:** Generated a domain-specific dataset and evaluator rubric from the deployed agent, then compared that synthetic coverage with Caldova's curated golden regression set.

## Skills acquired

**Azure & infrastructure**
- Navigating the Foundry Toolkit for VS Code and the model catalog
- Managing Azure resources (AI Services, RBAC, monitoring)
- Understanding Foundry project architecture (accounts, projects, and model deployments)

**Python & AI development**
- Authenticating with **DefaultAzureCredential** (no hardcoded keys)
- Sending Responses API requests via the Azure AI Projects SDK
- Engineering system prompts for structured JSON output
- Building business logic around model responses
- Comparing multiple models on identical tasks

**Agent development & deployment**
- Using the Microsoft Agent Framework (Agent, FoundryChatClient)
- Local testing with the Foundry Toolkit Agent Inspector before cloud deployment
- Deploying Python code to Foundry Agent Service with `azure.yaml` and `azd deploy`
- Invoking and monitoring agents via the `azd ai agent` CLI
- Testing agents in the Foundry Toolkit hosted agents playground
- Generating and running repeatable hosted-agent evaluations with `azd ai agent eval`

## Key files used by the lab

| File | Purpose |
|------|---------|
| `src/01_first_inference.py` | First Responses API request |
| `src/02_sentiment_analysis.py` | Sentiment analysis pipeline and governed routing |
| `src/sample_feedback.json` | Sample Caldova consumer feedback dataset |
| `src/tests/test_sentiment.py` | Unit tests for the governed routing logic |
| `src/03_model_comparison.py` | Side-by-side model evaluation |
| `src/agent/app.py` | Hosted Agent Framework application |
| `src/agent/requirements.txt` | Agent dependencies |
| `src/agent/evaluation-instructions.md` | Caldova quality and safety criteria for generated evaluations |
| `src/agent/evals/caldova-golden.jsonl` | Curated hosted-agent regression cases |
| `.env` | Local environment configuration |
| `azure.yaml` | Foundry project, model, and direct-code hosted-agent configuration |

## Key patterns and takeaways

1. **Prompt engineering drives behavior.** A well-structured system prompt turns a general-purpose model into a specialized analyst.
2. **Business logic wraps model output.** Models provide probabilistic output; your code makes deterministic routing decisions.
3. **Start cheap, escalate smart.** Use a fast, cheap model for most requests and route only low-confidence cases to a more capable model.
4. **Validate before deployment.** Test with the Agent Inspector, then validate again in the hosted-agent playground after `azd deploy`.
5. **Keep regulated routing independent.** Sentiment and regulated review categories are separate signals -- never route on sentiment alone.
6. **Measure changes with fixed evidence.** Generated suites discover new cases; curated golden sets make agent versions comparable.

## Next steps

- **Add more topics or review categories** -- for example, route competitor mentions to a competitive-intelligence queue.
- **Add tools to the agent** -- look up a consumer's case history or notify Caldova's pharmacovigilance team via a webhook when a POTENTIAL_ADVERSE_EVENT is detected.
- **Build a multi-agent workflow** -- chain the sentiment agent with a response-drafting agent.
- **Connect to a frontend** -- the hosted agent exposes an OpenAI-compatible REST API at `/responses`.
- **Set up CI/CD** -- use GitHub Actions with `azd` to redeploy on every push that changes `src/agent/**`.
- **Add an evaluation quality gate** -- run the committed golden evaluation after deployment and fail the pipeline when agreed thresholds regress.

## Thank you

You started with a model in a catalog and finished with a production-ready hosted agent on Microsoft Foundry. The patterns you learned -- prompt engineering, structured output, confidence-based routing, and direct-code deployment -- apply to any AI application, not just consumer sentiment analysis.

If you encountered any issues during this lab or would like to try it self-paced, see the repository issues page.

![Report issues](../images/issues.png)

Happy building!
| `azure.yaml` | Direct-code hosted-agent configuration |

## Continue learning

- [Microsoft Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [OpenAI Responses API](https://learn.microsoft.com/azure/foundry/openai/how-to/responses)
- [Microsoft Foundry hosted agents](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents)

If you encountered an issue, use the repository support guidance after the lab.

**Happy building!**

---

**Next:** [Clean up your Azure resources](../cleanup/CLEANUP.md)

