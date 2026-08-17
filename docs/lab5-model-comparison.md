# Lab 5: Compare model outputs (Optional)

> **Duration:** ~15 minutes

## Objective

Compare how different hosted models analyze the same Caldova consumer feedback, measure response quality and latency, and make an informed decision about which model to deploy for Caldova's B2C sentiment analysis pipeline.

## Why compare models?

Different models have different strengths:

| Model | Strengths | Trade-offs |
|-------|-----------|-----------|
| gpt-5.4-mini | Fast, cost-efficient, good for simple tasks | May miss nuance in complex cases |
| gpt-5.4 | Higher reasoning quality, better at edge cases | Slower, more expensive |
| Phi-4 | Open-weight, strong reasoning, runs on-device | May need different prompt tuning |

Comparing models on your **actual Caldova feedback data** helps you make informed deployment decisions before you go live.

## Prerequisites

To complete this lab, you need **two model deployments** in your Foundry project. Update your `.env` to add a new variable:

```ini
MODEL_DEPLOYMENT_NAME=gpt-5.4-mini
MODEL_DEPLOYMENT_NAME_2=gpt-5.4
```

### Deploying a new model

If you only have one model deployed, deploy a second one from the Foundry Toolkit Model Catalog:

1. Click the Foundry Toolkit icon in the VS Code Activity Bar to open the extension panel.
2. Navigate to **Developer Tools → Discover → Model Catalog**.
3. Apply the filter **Hosted by → Foundry** to see all Foundry-hosted models.
4. In the search bar type **gpt-5.4**.
5. Click **Deploy → Deploy with Default settings**.

Wait for the deployment to complete before proceeding. You should see the pop-up below once complete.

![Foundry Toolkit Deployment Complete](../images/ftk_deployment_success.png)

> **Note:** If you are unable to deploy a second model, skip this lab and proceed to Lab 6.

## Step 1: Review the comparison code

Open `src/03_model_comparison.py`. The key function runs the same feedback through multiple models:

```python
def compare_models(client, models: list[str], feedback: str) -> list[dict]:
    results = []
    for model in models:
        start = time.time()
        result = analyze_feedback(client, model, feedback)
        elapsed = time.time() - start
        results.append({
            "model": model,
            "sentiment": result["sentiment"],
            "confidence": result["confidence"],
            "review_category": result["review_category"],
            "latency_ms": round(elapsed * 1000),
        })
    return results
```

## Step 2: Run the comparison

```powershell
python src/03_model_comparison.py
```

### Expected output

```text
========================================
  Model Comparison: Caldova Consumer Sentiment
========================================

Feedback: "I felt dizzy after taking the Caldova allergy relief tablets."

  Model         Sentiment  Confidence  Review category           Latency
  ------------- ---------- ----------  -------------------------  --------
  gpt-5.4-mini   NEGATIVE   0.85        POTENTIAL_ADVERSE_EVENT    298ms
  gpt-5.4        NEGATIVE   0.92        POTENTIAL_ADVERSE_EVENT    845ms

========================================
  Comparison Summary
========================================
  Agreement rate: 100% (both models agreed on sentiment and review category)
  Avg latency - gpt-5.4-mini: 311ms
  Avg latency - gpt-5.4:      868ms
  Cost ratio:  gpt-5.4-mini is ~10x cheaper per token
```

## Step 3: Analyze the results

Look for patterns in the comparison:

- **Agreement** -- Do both models agree on sentiment and review_category? If they disagree on a regulated signal like POTENTIAL_ADVERSE_EVENT, which model would you trust?
- **Confidence** -- Does the more capable model consistently give higher confidence scores? Higher confidence may justify the extra cost for borderline feedback near the escalation threshold.
- **Latency** -- How much slower is the larger model? For real-time intake, latency matters; for nightly batch processing, it may not.
- **Cost** -- The per-token prices below are **illustrative**. Check the [Azure OpenAI pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for current rates.

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|----------------------|
| gpt-5.4-mini | ~$0.15 | ~$0.60 |
| gpt-5.4 | ~$2.50 | ~$10.00 |

Even running the full `sample_feedback.json` (15 items × 2 models) stays well under $0.01. The difference becomes meaningful at Caldova's scale -- at 100,000 feedback items/day, gpt-5.4-mini costs ~$5/day vs. gpt-5.4 at ~$80/day.

> **Tip:** For this type of classification task, gpt-5.4-mini often matches gpt-5.4 performance at a fraction of the cost.

## Step 4: Try a hybrid approach

A common production pattern is to use the cheaper model first and escalate low-confidence results to the more capable model. The comparison script includes a `--hybrid` mode:

```powershell
python src/03_model_comparison.py --hybrid
```

This runs gpt-5.4-mini first. If confidence is below 0.8, it re-runs with gpt-5.4 for a second opinion.

## Extension challenges

If you finish early, try these:

1. **Add a third model** -- Deploy Phi-4 and add it to the comparison.
2. **Create your own test set** -- Write 10 Caldova consumer feedback items that span edge cases (delivery complaints, competitor mentions, sarcastic praise, ambiguous symptom mentions).
3. **Measure consistency** -- Run the same feedback item five times and record any variation in sentiment, confidence, or review category.
4. **Adjust the prompt** -- Make the system prompt stricter about what counts as a POTENTIAL_ADVERSE_EVENT and see how it changes routing decisions.

## What you learned

- ✅ How to run the same inference across multiple models
- ✅ How to compare sentiment classification quality, confidence, and latency
- ✅ How to make model selection decisions based on task requirements
- ✅ How to implement a hybrid escalation pattern

## Key takeaway

> Model selection is a product decision, not just a technical one. By programmatically comparing models on your actual Caldova feedback data, you can optimize for the right balance of quality, speed, and cost.

---

**Next:** [Lab 6 - Deploy a hosted agent](./lab6-deploy-agent.md)

