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
AZURE_LOCATION=northcentralus
AZURE_PRICING_CURRENCY=USD
```

Set `AZURE_LOCATION` to the region where your Foundry resource is deployed. The pricing currency defaults to `USD` when `AZURE_PRICING_CURRENCY` is omitted.

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

Open `src/03_model_comparison.py`. The script retrieves current input and output token rates from the unauthenticated [Azure Retail Prices API](https://learn.microsoft.com/rest/api/cost-management/retail-prices/azure-retail-prices), then runs the same feedback through each model:

```python
def compare_models(client, models, feedback, pricing_by_model=None):
    results = []
    pricing_by_model = pricing_by_model or {}
    for model in models:
        start = time.time()
        result = analyze_feedback(client, model, feedback)
        usage = result.get("_usage", {})
        results.append({
            "model": model,
            "sentiment": result["sentiment"],
            "confidence": result["confidence"],
            "review_category": result["review_category"],
            "latency_ms": round((time.time() - start) * 1000),
            "usage": usage,
            "estimated_cost": calculate_cost(
                usage, pricing_by_model.get(model)
            ),
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
  Sentiment + routing agreement: 8/8 (100%)
  Avg latency - gpt-5.4-mini: 311ms
  Avg latency - gpt-5.4:      868ms

  Retail pricing: USD in northcentralus (Azure Retail Prices API)
  gpt-5.4-mini rates: input $<current-rate>/1K, output $<current-rate>/1K
  gpt-5.4-mini estimated retail cost: $<run-cost> (<input> input + <output> output tokens)
  gpt-5.4 rates: input $<current-rate>/1K, output $<current-rate>/1K
  gpt-5.4 estimated retail cost: $<run-cost> (<input> input + <output> output tokens)
  Cost saving: gpt-5.4-mini saved <percent>% ($<amount>) vs gpt-5.4 for this run
```

Pricing and token totals change over time, so your output will contain numbers in place of the placeholders above.

## Step 3: Analyze the results

Look for patterns in the comparison:

- **Agreement** -- Do both models agree on sentiment and review_category? If they disagree on a regulated signal like POTENTIAL_ADVERSE_EVENT, which model would you trust?
- **Confidence** -- Does the more capable model consistently give higher confidence scores? Higher confidence may justify the extra cost for borderline feedback near the escalation threshold.
- **Latency** -- How much slower is the larger model? For real-time intake, latency matters; for nightly batch processing, it may not.
- **Cost** -- The script combines each response's actual input and output token counts with the current retail rate and billing unit returned by the Azure Retail Prices API. It then compares total observed run costs to show both the dollar difference and percentage saved.

The displayed amount is a retail cost estimate, not a billed charge. It does not include negotiated discounts, cached-token pricing, taxes, or other agreement-specific adjustments. See the [Azure OpenAI pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for billing details.

> **Note:** The Retail Prices catalog can lag a newly released model or omit one of its standard token meters. In that case, the script prints `pricing unavailable` and omits the cost comparison instead of substituting stale illustrative prices.

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
- ✅ How to compare sentiment classification quality, confidence, latency, and retail cost
- ✅ How to calculate model cost and percentage savings from actual token usage
- ✅ How to make model selection decisions based on task requirements
- ✅ How to implement a hybrid escalation pattern

## Key takeaway

> Model selection is a product decision, not just a technical one. By programmatically comparing models on your actual Caldova feedback data, you can optimize for the right balance of quality, speed, and cost.

---

**Next:** [Lab 6 - Deploy a hosted agent](./lab6-deploy-agent.md)

