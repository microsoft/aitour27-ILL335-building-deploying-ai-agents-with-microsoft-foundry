@lab.Title

## Welcome to ILL335

This AI Tour lab is **Building & Deploying AI Agents with Microsoft Foundry**.

To begin, log in to the virtual machine with: +++@lab.VirtualMachine(Win11-Pro-Base).Password+++

# Part 1: Discover Foundry-hosted models

> **Duration:** ~10 minutes

## Scenario

You are an AI developer on Caldova's commercial digital and customer engagement team.Caldova's B2C channels receive thousands of pieces of consumer feedback daily about its products and support services. Your task is to build a **consumer sentiment analysis tool** that classifies feedback sentiment and independently routes regulated signals -- such as potential adverse events, product quality complaints, and medical inquiries -- to the right human reviewers.

In this lab, you will explore the Microsoft Foundry model catalog -- directly inside Visual Studio Code using the **Foundry Toolkit** extension -- to find a model that can power Caldova's consumer sentiment analysis pipeline.

## Objective
Explore the Foundry Toolkit model catalog in Visual Studio Code to discover available hosted models, understand model capabilities, and identify a model suitable for inference-based tasks like product review moderation.

## Step 1: Open the project in VS Code

1. Open Visual Studio Code by launching it from the Start menu or desktop.
2. In VS Code, select **File → Open Folder**.
3. Navigate to the `Desktop` folder, select `AI-Tour-ILL335-main`, and click **Select folder**.
4. When prompted with "Do you trust the authors of the files in this folder?", select **Yes, I trust the authors**.

    !IMAGE[trust.png](instructions343795/trust.png)
5. You should see the project files in the sidebar.

## Step 2: Open the Foundry Toolkit in Visual Studio Code

The [**Foundry Toolkit** extension](https://aka.ms/ftk_install) is already installed on the lab virtual machine, so you can explore models without leaving your editor -- no web browser required.

1. In the **Activity Bar** on the left, click the **Foundry Toolkit** icon to open the toolkit panel.

    !IMAGE[Foundry Toolkit Icon](instructions343795/ftk_icon.png)
2. Click **Set Foundry Project → Switch Project → Sign in to Azure**.
3. When prompted to sign in to Azure to access your Foundry resources, use the following Azure credentials:

    Username: +++@lab.CloudPortalCredential(User1).Username+++

    If prompted for a Temporary Access Pass (TAP): +++@lab.CloudPortalCredential(User1).AccessToken+++

    If prompted for a Password: +++@lab.CloudPortalCredential(User1).Password+++
4. After signing in, select the Foundry project that shows up in the list. This is the project pre-provisioned for you in the lab environment, and it contains the model deployments you will use for Caldova's consumer sentiment analysis system.

The toolkit panel is your central hub for browsing models, testing them in a playground, and working with agents -- all from within VS Code.

## Step 3: Explore the model catalog

1. In the Foundry Toolkit panel, under **Developer Tools**, select **Model Catalog** to open the model catalog view. These are production-ready, hosted models you can use without fine-tuning.

    !IMAGE[Model Catalog](instructions343795/model_catalog.png)
2. Browse the available models. Use the filters at the top of the catalog to narrow the list -- for example, by Publisher (Azure OpenAI, Microsoft, Meta, Mistral, etc.), by where the model is **hosted by** (such as Microsoft Foundry), or by task (Responses, Image Analysis, etc.).

Select a model to view its model card. Take note of the following properties.

| Property | Common values |
|----------|---------------|
| Model provider | Azure OpenAI, Microsoft AI, Meta, Mistral, etc. |
| Task type | Responses, embeddings, text to image |
| Input type | text, image |
| Output type | text, image |
| Context window | Varies by model (see model card) |
| Token limits | Varies by model (see model card) |

## Step 4: Identify a model for this lab

For this workshop, you need a model that supports the **Responses API** -- the ability to accept instructions and input and return structured response text.

Recommended models for this lab:

| Model | Publisher | Why |
|-------|-----------|-----|
| gpt-5.4-mini | OpenAI | Fast, cost-efficient, excellent for sentiment classification |
| gpt-5.4 | OpenAI | Higher quality, good for complex or ambiguous feedback |
| Phi-4 | Microsoft | Strong reasoning, open-weight |

> **Tip:** gpt-5.4-mini is the best choice for this lab -- it is fast, inexpensive, and well-suited for sentiment analysis and classification tasks.

## Step 5: Check model details

The **gpt-5.4-mini** model from Azure OpenAI is high quality, fast, and cost-efficient, which makes it ideal for Caldova's consumer sentiment analysis pipeline.

Find **gpt-5.4-mini** in the catalog and open its detail page. Explore the tabs at the top:

1. **Details** -- Model description and capabilities
2. **Benchmarks** -- Scores and performance metrics
3. **Responsible AI** -- Guardrails imposed on the model from Azure AI Content Safety
4. **License** -- Links to applicable licensing terms

> **Note:** The model card is opened in a web browser page. Make sure to return to VS Code after reviewing it to continue with the lab.

## Step 6: Explore the playground (Optional)

1. Back in VS Code, under **Developer Tools → Build** in the toolkit panel, open the **Model Playground**.
2. Select **gpt-5.4-mini** from the model dropdown.
3. In the **System prompt** (instructions) field, enter:

    ```text
    You are a consumer engagement insight analyst for Caldova, a global pharmaceutical company. Classify the sentiment of the following consumer feedback as POSITIVE, NEUTRAL, NEGATIVE, or MIXED. Respond with only the sentiment label.
    ```
4. In the chat box, enter:

    ```text
    I felt dizzy after taking the Caldova allergy relief tablets.
    ```
5. Send the message and observe the response. This is a preview of the inference pattern you will implement in code during Labs 3 and 4 to analyze sentiment in Caldova consumer feedback.

## What you learned

- ✅ How to navigate the Foundry Toolkit in Visual Studio Code
- ✅ How to browse the model catalog from within VS Code
- ✅ How a model responds to a Caldova consumer sentiment prompt

## Key takeaway

> Microsoft Foundry provides access to production-ready hosted models from multiple publishers. You do not need to train, fine-tune, or host these models yourself -- you simply connect to them via API and start building. For Caldova, this means a working consumer sentiment analysis prototype in hours, not weeks.

======

# Part 2: Verify your project

> **Duration:** ~5 minutes

## Objective

Validate that your lab project environment is configured correctly -- ensuring the `.env` file, dependencies, and CLI tools are all in place before you start writing code.

## Step 1: Validate the .env is correct

In VS Code, ensure that the `.env` file has been created in the root of your project.

1. Open the `.env` file from the root of the project folder.
2. Confirm the following variables exist:

    ```text
    PROJECT_ENDPOINT
    MODEL_DEPLOYMENT_NAME
    ```

    You may also see `MODEL_DEPLOYMENT_NAME_2` and `AZURE_CONTAINER_REGISTRY_NAME`, which are optional variables for later sections -- they are not required.
3. (Optional) Confirm the values are correct according to your Foundry project. `PROJECT_ENDPOINT` should match the project endpoint listed at https://ai.azure.com, and `MODEL_DEPLOYMENT_NAME` should match the name of the model deployment.

## Step 2: Validate your setup

Run the included validation script to confirm that all files, dependencies, CLI tools, and configuration are correct:

1. Open a terminal in VS Code by selecting **Terminal → New Terminal**.
2. Run this command:

    ```powershell
    python -X utf8 src/tests/validate_lab.py
    ```

3. You should see output ending with:

    ```text
    VALIDATION SUMMARY
    Total checks: 100
    ✅ Passed:  99
    ❌ Failed:  0
    ⏭️ Skipped: 1

    Result: PASS -- lab is ready!
    ```

If any checks fail, the output tells you exactly what to fix. Common issues:

| Failure | Fix |
|---------|-----|
| Missing file | Re-check your azd provision output for errors |
| CLI not found | Install the missing tool (see SETUP.md) |
| Package not installed | Run `pip install -r requirements.txt` inside your `.venv` |
| .env not configured | Copy `.env.sample` to `.env` and fill in your endpoint |

> **Tip:** Re-run validation after any fix to confirm it resolves the issue.

## What you learned

- ✅ How to validate your setup with the automated validation script
- ✅ How to load the workshop solution in VS Code

## Key takeaway

> A Foundry project is your workspace for organizing AI resources. The project endpoint is the single connection point your application code needs to access any model deployed within it.

======

# Part 3: Connect and send your first inference

> **Duration:** ~15 minutes

## Objective

Connect securely to your Microsoft Foundry project and send a model request with the OpenAI Responses API. You will also inspect response status and token usage, then try multi-turn continuity.

## Concepts

| Concept | Description |
|---------|-------------|
| **AIProjectClient** | Connects your application to a Foundry project |
| **DefaultAzureCredential** | Uses your signed-in Azure identity without hardcoded keys |
| **Responses API** | Accepts instructions and input, then returns response output and metadata |
| **previous_response_id** | Continues a conversation without rebuilding a message array |

See the official [OpenAI Responses API guide](https://learn.microsoft.com/azure/foundry/openai/how-to/responses) for more examples.

## Step 1: Review the code

Open `src/01_first_inference.py`. The script first loads configuration and creates a project client with your signed-in Azure identity:

```python
load_dotenv()

endpoint = os.environ.get("PROJECT_ENDPOINT")
model = os.environ.get("MODEL_DEPLOYMENT_NAME")

project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)
```

- **Loads** the project endpoint and model deployment from `.env`.
- **Authenticates** with your Azure identity instead of an API key.
- **Establishes** a reusable client for your Foundry project.
- **Provides** an OpenAI-compatible inference client:

```python
inference_client = project_client.get_openai_client()
```


The implemented request separates durable behavior - instructions - from the current input and provides access to the Responses API through the configured project.


```python
response = inference_client.responses.create(
    model=model,
    instructions="You are a helpful assistant for Caldova, Microsoft's fictional global pharmaceutical company. Respond concisely and do not provide medical advice.",
    input="How could Caldova use Microsoft Foundry to understand consumer sentiment about its products? Answer in one sentence.",
)
```

Finally, the script reads the convenient text property and useful metadata:

```python
print(response.output_text)
print(f"Status: {response.status}")
print(
    f"Tokens used: {response.usage.total_tokens} "
    f"(input: {response.usage.input_tokens}, "
    f"output: {response.usage.output_tokens})"
)
```

- **Returns** generated text through `response.output_text`.
- **Reports** completion state through `response.status`.
- **Exposes** input, output, and total token counts for monitoring and cost analysis.

## Step 2: Run the code

From the repository root, run:

```powershell
python src/01_first_inference.py
```

The wording can vary, but the output should include response text, model name, status, and usage:

```text
Connecting to Foundry project...
Sending inference request to model: gpt-5.4-mini
---
Response:
Caldova could use Microsoft Foundry to analyze consumer feedback...
---
Model: gpt-5.4-mini
Status: completed
Tokens used: 52 (input: 30, output: 22)
```

If the script fails, check these common causes:

| Error | Likely cause | Fix |
|-------|--------------|-----|
| Missing `PROJECT_ENDPOINT` | `.env` is missing or incomplete | Restore the value produced in Lab 2 |
| `DefaultAzureCredential` failed | Azure sign-in expired | Run `az login` |
| Resource not found | Deployment name does not match | Verify `MODEL_DEPLOYMENT_NAME` |
| Request remains incomplete | Service or safety condition interrupted generation | Inspect `response.status` and the full response |

## Step 3: Experiment with instructions and input

Now that your code is working, this step is about **actively testing changes and observing how the model behaves**.
Change one value at a time, rerun the script, and compare the output. Start by changing the instructions:

```python
instructions="You are a Caldova consumer engagement assistant. Use plain language. Responses must be concise, max 2 sentences. Do not provide medical advice."
```

Then try a different input:

```python
input="Summarize two ways consumer feedback analysis could help Caldova."
```
Observe whether the response follows both the durable instructions and the current input.

## Step 4: Try multi-turn continuity

The Responses API can continue from an earlier response by passing its ID. In a temporary experiment, add a follow-up after the first request:

```python
follow_up = inference_client.responses.create(
    model=model,
    previous_response_id=response.id,
    input="Which of those uses would be safest to prototype first, and why?",
)

print(follow_up.output_text)
print(f"Status: {follow_up.status}")
```

- **Continues** from the prior response without manually copying earlier turns.
- **Keeps** the follow-up focused through `previous_response_id`.

Do not include sensitive personal or medical data in prompts. For production workloads, follow your organization's data-handling and retention requirements.

## What you learned

- ✅ How to authenticate with `DefaultAzureCredential`
- ✅ How to obtain an OpenAI-compatible client from `AIProjectClient`
- ✅ How to call `responses.create()` with `instructions` and `input`
- ✅ How to read `output_text`, response status, and token usage
- ✅ How to continue a conversation with `previous_response_id`

## Key takeaway

> The Responses API provides one beginner-friendly pattern for model interaction: send instructions and input with `responses.create()`, then inspect output text, status, and usage.

======

# Part 4: Build Caldova's consumer sentiment analysis application

> **Duration:** ~20 minutes

## Objective

Build a working consumer sentiment analysis pipeline for Caldova's B2C engagement channels. The system accepts customer-submitted product reviews, classifies them using a Foundry-hosted model, applies moderation logic, and outputs structured results — ensuring that reviews from customers are safe and helpful before going live on the site.

## The problem

Caldova's B2C channels receive thousands of pieces of consumer feedback daily about products such as allergy relief tablets and topical relief gel, plus support interactions. Manual review does not scale. You need an automated system that can:

1. Accept consumer feedback as input.
2. Classify its sentiment (positive, neutral, negative, or mixed) and topics.
3. Independently identify regulated signals that require human review.
4. Return a structured decision with an evidence-based summary.
5. Handle edge cases gracefully.

Sentiment classification and regulated routing are **independent** of each other -- a POSITIVE piece of feedback can still contain a potential adverse event, and a NEGATIVE piece of feedback might simply reflect a delivery delay with no regulated content at all.

## Architecture

!IMAGE[architecture_lab520.png](instructions343795/architecture_lab520.png)

This pipeline uses **prompt-based JSON**: the system prompt instructs the model to respond only with valid JSON. For even stricter guarantees, OpenAI models support [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs), a `response_format` parameter that constrains the model to conform to a JSON schema. This lab uses the prompt-based approach for simplicity and portability across model providers.

## Step 1: Review the system prompt

The key to reliable sentiment analysis is a well-structured system prompt. Open `src/02_sentiment_analysis.py` and examine the `SYSTEM_PROMPT`:

```python
SYSTEM_PROMPT = """You are a consumer engagement insight analyst for Caldova, Microsoft's fictional global pharmaceutical company. Analyze feedback about Caldova products and support services.

Respond ONLY with valid JSON in this exact format:
{
    "sentiment": "<POSITIVE|NEUTRAL|NEGATIVE|MIXED>",
    "confidence": <0.0-1.0>,
    "topics": ["<PRODUCT_EXPERIENCE|PACKAGING|AVAILABILITY|SUPPORT|VALUE|OTHER>"],
    "review_category": "<NONE|POTENTIAL_ADVERSE_EVENT|PRODUCT_QUALITY_COMPLAINT|MEDICAL_INQUIRY|CONTENT_SAFETY>",
    "summary": "<brief evidence-based summary>"
}

Rules:
- Classify sentiment from the consumer's overall tone. MIXED means clearly positive and negative views are both present.
- POTENTIAL_ADVERSE_EVENT: an unwanted health effect or symptom is associated with use of a Caldova product.
- PRODUCT_QUALITY_COMPLAINT: a possible defect involving packaging, labeling, contamination, appearance, damage, or a delivery device.
- MEDICAL_INQUIRY: the consumer asks for diagnosis, dosing, interaction, treatment, or other personalized medical guidance.
- CONTENT_SAFETY: threats, hate, harassment, explicit content, or dangerous instructions.
- Use NONE when no review category applies.
- Do not determine causality, assess seriousness, or provide medical advice.
- When uncertain, lower confidence rather than inventing facts.

Do not include any text outside the JSON object."""
```

This prompt:

- **Constrains the output format** -- JSON only, predictable structure.
- **Separates two independent signals** -- sentiment (how the consumer feels) and review_category (whether the content needs regulated handling).
- **Provides classification rules** -- reduces ambiguity.
- **Explicitly limits the model's role** -- it must not determine causality, assess seriousness, or give medical advice; that stays with trained human reviewers.
- **Eliminates free-text noise** -- "Do not include any text outside the JSON object".

## Step 2: Understand the sentiment analysis pipeline

The application follows this flow:

### 2a. Send feedback for analysis

```python
def analyze_feedback(client, model: str, feedback: str) -> dict:
    """Send consumer feedback to the model and return structured insight."""
    try:
        response = client.responses.create(
            model=model,
            instructions=SYSTEM_PROMPT,
            input=feedback,
        )
    except Exception as exc:
        if "content_filter" in str(exc) or "content management policy" in str(exc):
            return {
                "sentiment": "MIXED",
                "confidence": 0.0,
                "topics": ["OTHER"],
                "review_category": "CONTENT_SAFETY",
                "summary": "Blocked by Azure content safety filtering.",
            }
        raise

    raw = response.output_text.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "sentiment": "MIXED",
            "confidence": 0.0,
            "topics": ["OTHER"],
            "review_category": "CONTENT_SAFETY",
            "summary": f"Model returned non-JSON output: {raw[:100]}",
        }
```

Key design decisions:

| Decision | Rationale |
|----------|-----------|
| Separate instructions and input | Keeps classification rules distinct from consumer feedback |
| JSON output format | Machine-parseable, no regex needed |
| Structured system prompt | Reliable, consistent categorization |
| try/except around inference | Catches Azure content safety filter blocks gracefully |
| try/except around json.loads() | Falls back to a conservative CONTENT_SAFETY result if the model returns malformed output |

### 2b. Apply governed routing logic

```python
def route_feedback(result: dict) -> str:
    """Route insights to analytics or an appropriate human review queue."""
    review_category = result.get("review_category", "CONTENT_SAFETY")
    confidence = result.get("confidence", 0.0)

    if review_category != "NONE":
        return "ESCALATE_FOR_REVIEW"
    if confidence < 0.8:
        return "REVIEW_LOW_CONFIDENCE"
    return "ADD_TO_SENTIMENT_DASHBOARD"
```

This adds a **business logic layer** on top of the model's analysis:

- Any regulated `review_category` (not `NONE`) → escalate for human review, regardless of sentiment or confidence.
- High-confidence, non-regulated feedback → add to the sentiment dashboard for trend reporting.
- Low-confidence, non-regulated feedback → route to a human for a second look.

Routing is driven entirely by `review_category` and `confidence` -- **never** by `sentiment`. A POSITIVE review can still be escalated (for example, positive feedback that also mentions a symptom).

### 2c. Process results

```python
def process_feedback(client, model: str, feedback: str) -> dict:
    """Analyze feedback, apply routing logic, and return the complete result."""
    analysis = analyze_feedback(client, model, feedback)
    return {
        "feedback": feedback,
        "sentiment": analysis.get("sentiment", "MIXED"),
        "confidence": analysis.get("confidence", 0.0),
        "topics": analysis.get("topics", ["OTHER"]),
        "review_category": analysis.get("review_category", "CONTENT_SAFETY"),
        "summary": analysis.get("summary", ""),
        "action": route_feedback(analysis),
    }
```

## Step 3: Run the application

Run the following command from the terminal:

```powershell
python src/02_sentiment_analysis.py
```

You should see output similar to the sample below. Since LLMs are non-deterministic, the output will not match 100%.

```text
========================================
  Caldova Consumer Sentiment Analysis
  Model: gpt-5.4-mini
========================================

Processing 5 sample feedback items...

--- Feedback 1/5 ---
Feedback: "The Caldova allergy relief tablets fit easily into my morning routine and the packaging is clear."
Sentiment: POSITIVE (confidence: 0.95)
Topics: PRODUCT_EXPERIENCE, PACKAGING
Review category: NONE
Summary: Consumer describes an easy, positive routine and clear packaging.
Action: 📊 ADD_TO_SENTIMENT_DASHBOARD

--- Feedback 4/5 ---
Feedback: "I felt dizzy after taking the Caldova allergy relief tablets."
Sentiment: NEGATIVE (confidence: 0.9)
Topics: PRODUCT_EXPERIENCE
Review category: POTENTIAL_ADVERSE_EVENT
Summary: Consumer reports dizziness after use; no causality determined.
Action: ⚠️ ESCALATE_FOR_REVIEW

========================================
  Engagement Insight Summary
========================================
Total feedback: 5
  POSITIVE:    1
  NEUTRAL:     0
  NEGATIVE:    2
  MIXED:       2
  ESCALATED:   2
```

> **Note:** Some feedback containing threats or explicit content may be blocked by Azure's built-in content safety filter *before* reaching the model. When this happens, the application handles it gracefully and labels the result with review_category CONTENT_SAFETY. This is expected behavior -- the content filter is an additional layer of protection in production deployments.

## Step 4: Test with custom feedback

The application also accepts interactive input. Run it with the `--interactive` flag:

```powershell
python src/02_sentiment_analysis.py --interactive
```

Type feedback to analyze it in real time:

```text
Enter feedback: What dose should I give my child?
Sentiment: NEUTRAL (confidence: 0.85)
Topics: PRODUCT_EXPERIENCE
Review category: MEDICAL_INQUIRY
Summary: Consumer asks for personalized dosing guidance.
Action: ⚠️ ESCALATE_FOR_REVIEW
```

Confirm that the application routes the medical inquiry for human review and does not provide medical advice. Type **quit** to exit.

## Step 5: Test with the sample dataset

The `src/sample_feedback.json` file contains a broader set of test feedback spanning positive, neutral, negative, mixed, adverse-event, product-quality, and medical-inquiry cases. Run the batch test:

```powershell
python src/02_sentiment_analysis.py --file src/sample_feedback.json
```

## Step 6: Customize the routing logic

Try adjusting the confidence threshold in the `route_feedback` function:

| Threshold change | Effect |
|-----------------|--------|
| Lower the confidence threshold (0.8 → 0.6) | More feedback goes straight to the dashboard |
| Raise the confidence threshold (0.8 → 0.9) | More feedback routed for a low-confidence human check |
| Add a new topic-based routing rule | Custom handling for a specific topic, such as VALUE |

After each change, re-run the sentiment analysis script to see the effect on the same 5 sample feedback items.

## What you learned

- ✅ How to design a system prompt for structured output (JSON)
- ✅ How to keep sentiment classification independent from regulated signal routing
- ✅ How to build an analysis pipeline using model inference
- ✅ How to apply business logic on top of model responses
- ✅ How to process batches of content programmatically
- ✅ How to handle interactive input for real-time sentiment analysis

## Key takeaway

> A model provides the intelligence -- your application provides the governance. By combining structured instructions with programmatic decision-making, you can build a production-quality consumer sentiment analysis system for Caldova that keeps regulated signal routing independent of sentiment, without any fine-tuning.

======

# Part 5: Compare model outputs (Optional)

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

!IMAGE[Foundry Toolkit Deployment Complete](instructions343795/ftk_deployment_success.png)

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

======

# Part 6: Deploy a hosted agent

> **Duration:** ~20 minutes

## Objective

Deploy Caldova's consumer sentiment agent directly from Python source to Microsoft Foundry Agent Service. You will inspect the Agent Framework code, verify the direct-code service configuration in `azure.yaml`, test the agent locally with the Agent Inspector, deploy it to the cloud, and validate the hosted agent.

This lab is organized into two sections. **Part A (recommended)** drives the whole lifecycle -- test, deploy, interact, and monitor -- from the Foundry Toolkit UI. **Part B (optional)** shows how to do the same thing from the `azd` command line. You only need to complete one of them.

## What is a hosted agent?

A hosted agent is your agent application running on Foundry-managed infrastructure. Unlike the scripts in Labs 3-5 that run locally, a hosted agent is a persistent, cloud-hosted service that exposes the OpenAI Responses protocol. Foundry handles the heavy lifting:

- **VM-isolated sandboxes** -- each session runs in its own isolated sandbox with a persistent filesystem.
- **REST API** -- a protocol library exposes your agent as an OpenAI Responses API endpoint, callable by the Foundry Playground, other agents, or any application.
- **Per-session scaling** -- the platform creates a sandbox on demand and tears it down when idle.
- **Dedicated agent identity** -- each agent authenticates to Foundry models and Azure services with its own Azure identity (no keys to manage).
- **Managed conversation history** -- the platform maintains continuity between turns, so your `Agent` does not need a local message list.

## Architecture

The Foundry Toolkit and `azd` build your agent code into the hosted service and deploy it to Foundry Agent Service. At runtime, the platform provisions a sandbox and exposes a dedicated endpoint that your agent uses to call Foundry models.

!IMAGE[Hosted agent architecture](../images/mermaid_diagram2.png)

| Property | This lab |
|----------|----------|
| Source | `src/agent/app.py` and `src/agent/requirements.txt` |
| Runtime | Python 3.13 |
| Host adapter | `ResponsesHostServer` |
| Protocol | Responses 2.0.0 |
| Deployment | Direct code through `azure.yaml` and `azd deploy` |
| History | Managed by the Foundry platform |
| Identity | Azure identity; no credentials stored in source |

## Prerequisites

- The Foundry Toolkit extension installed and signed in to Azure (from Lab 1).
- `.env` with `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` set.

Install the agent dependencies (separate from the main lab requirements):

```powershell
pip install -r src/agent/requirements.txt
```

> **Note:** The Foundry Toolkit uses the Azure Developer CLI (`azd`) and its `azure.ai.agents` extension under the hood to build and deploy hosted agents. Both are already installed and configured in the lab environment.

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

### The container definition: src/agent/Dockerfile

This file builds a container with a Python 3.12 installation and packages installed from **requirements.txt**.

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8088
CMD ["python", "-u", "app.py"]
```

### The agent manifest: src/agent/agent.yaml

The manifest tells Foundry how to configure the review moderation agent — which protocols it supports (Responses API) and what environment variables to inject.

```yaml
kind: hosted
name: caldova-review-moderation-agent
description: Feedback review moderation agent for Caldova that classifies customer reviews as SAFE, NEEDS_REVIEW, or UNSAFE and route it accordingly
protocols:
    - protocol: responses
      version: "1.0.0"
environment_variables:
    - name: AZURE_AI_PROJECT_ENDPOINT
      value: ${AZURE_AI_PROJECT_ENDPOINT}
    - name: AZURE_AI_MODEL_DEPLOYMENT_NAME
      value: ${MODEL_DEPLOYMENT_NAME}
```
---

## Install agent dependencies

> This step is shared by both Part A and Part B — do it once before you start.

The agent uses packages that are separate from the main lab requirements, and both deployment paths need them. Install them first:

```powershell
pip install -r src/agent/requirements.txt
```

This includes **agent-dev-cli** and **debugpy**, which power the Agent Inspector and local debugging.

======

# Part A — Deploy with the Foundry Toolkit (Recommended)

In this section you drive the entire agent lifecycle from the Foundry Toolkit UI inside VS Code: test locally with the Agent Inspector, deploy, chat with the deployed agent, watch its logs, and clean up.

## A1: Sign in to azd

The Foundry Toolkit uses `azd` under the hood, so make sure it is authenticated before you start. Open a terminal and run:

```powershell
azd auth login
```

A browser window opens for you to sign in. Use the same account you used for the Foundry Toolkit. Once you see `Logged in to Azure`, you are ready.

> **Tip:** You only need to do this once per environment. If you are already signed in, `azd auth login` will confirm your existing session.


## A2: Test the agent locally with the Agent Inspector

Before deploying, validate that the agent runs correctly on your machine. The Foundry Toolkit ships an **Agent Inspector** -- an interactive test harness that runs your agent as a local HTTP server and lets you send messages and inspect every request, response, and trace, all inside VS Code.

1. In VS Code, open `src/agent/app.py`.
2. Press **F5** (or select **Run → Start Debugging**) and, if prompted, choose **Debug Agent with Agent Inspector**.
3. If you see a dialog about allowing network access, select **Allow**.
4. VS Code starts the agent server and opens the Agent Inspector webview. You should see the server start in the terminal:

    ```text
    Starting caldova-consumer-sentiment-agent...
      Endpoint: https://<your-resource>.services.ai.azure.com/api/projects/<your-project>
      Model:    gpt-5.4-mini
    Application startup complete.
    ```

    > **Tip:** If the Inspector does not open automatically, click the Foundry Toolkit icon in the Activity Bar → **Agent (local) → Open Agent Inspector**.

5. In the Agent Inspector chat box, send a review and inspect the JSON response and trace. Try these prompts to validate each category:

    | Feedback | Expected review category |
    |----------|--------------------------|
    | The Caldova topical relief gel is convenient, but the cap is difficult to open. | NONE |
    | I felt dizzy after taking the Caldova allergy relief tablets. | POTENTIAL_ADVERSE_EVENT |
    | The safety seal on the bottle was already broken when it arrived. | PRODUCT_QUALITY_COMPLAINT |
    | What dose should I give my child? | MEDICAL_INQUIRY |

    Each response is a structured JSON object with sentiment, confidence, topics, review_category, and summary. Confirm the agent does not provide medical advice.

6. Click the **Events** tab to see the raw stream of server-sent events. Because the agent speaks the OpenAI Responses API, the JSON is streamed token-by-token. A `response.completed` event means the agent returned a well-formed response.

When you are done testing, press the **Stop** button in the debug toolbar (or **Ctrl+C** in the terminal) to shut the agent down.

> If Agent Inspector is unavailable in your installed Toolkit version, run `python src/agent/app.py` and use the local Responses endpoint shown by the server.

## A3: Deploy the agent with the Deploy button

Once you tested your agent locally, you can deploy the hosted agent **from inside VS Code** using the **Deploy** button in the Foundry Toolkit Agent Inspector UI. The toolkit handles the entire workflow — provisioning, building, and deploying — with no manual `azd up` required.

In the deployment configuration dialog, you can optionally change the agent name, deployment method, CPU and memory quotas. For the sake of this lab, leave the defaults and click **Deploy**.

When the deployment finishes, you should see a success notification from the Foundry Toolkit and the **Hosted Agent Playground** will be loaded to let you interact with your deployed agent.

### What the toolkit does under the hood

When you deploy, the Foundry Toolkit runs the same multi-step `azd` workflow you would otherwise run manually:

1. **Provisions** — Creates/updates infrastructure (ACR, capability host, RBAC)
2. **Builds** — Sends src/agent/ to ACR for a remote Docker build
3. **Deploys** — Registers a hosted agent version on Foundry Agent Service
4. **Starts** — Launches the container and waits for it to be ready

Since this lab environment has already provisioned the resources, the toolkit skips the provisioning step and only registers the new agent version.

> The first deployment takes 3-5 minutes. Subsequent deployments are faster.
>
> **Note:** You may briefly see a **404 error** while the agent registers. This is a known post-deploy timing issue, not a failure — as long as the toolkit reports the container built and the agent deployed, you can safely ignore it.


## A4: Interact with the hosted agent playground

1. In VS Code, click the Foundry Toolkit icon to open the toolkit panel.
2. Expand **My resources** and click **Agents**. Hosted agents are listed under the **Hosted** tab.
3. Find `caldova-review-moderation-agent` in the list. Its status should show **Success**.
4. Select the agent and open it in the **Playground**.

Send a few reviews to confirm it works in the cloud:

```text
The tablets work well, but delivery was late.
```

Confirm the agent returns valid governed JSON and that sentiment and review routing remain independent.

> **Tip:** If the agent does not appear yet, refresh the Agents view -- it can take a minute after deployment for the agent to register.

## A5: Monitor the agent logs

1. In the Foundry Toolkit panel, expand **My resources → Agents** and select `caldova-consumer-sentiment-agent` (under the **Hosted** tab).
2. Open the **Logs** view for the agent.
3. Click **Start** to begin streaming logs. As you send messages from the playground, the corresponding request and container activity appear in real time.
4. When finished, click **Stop**.

Never send secrets, credentials, or unnecessary personal or health information to logs.

## A6: Clean up

When you are done with the UI workflow, remove the hosted agent so it does not keep consuming resources:

1. In the Foundry Toolkit panel, expand **My resources → Agents** (the **Hosted** tab).
2. Right-click `caldova-consumer-sentiment-agent` (or use the **...** menu) and select **Delete**.
3. Confirm the deletion.

> **Note:** Deleting the agent removes the hosted deployment. If you also want to tear down the underlying infrastructure, use `azd down` as shown in Part B.

======

# Part B (Optional) — Deploy with the command line

Prefer the terminal, or want to automate the workflow in CI/CD? This section walks through the same lifecycle using the `azd` CLI. You only need to do either Part A or Part B.

## B1: Sign in to azd

```powershell
azd auth login
```

Use the same account you used for the Foundry Toolkit. Once you see `Logged in to Azure`, continue.

> **Tip:** If you already ran `azd auth login` in Part A, you are still signed in and can skip this step.

## B2: Test the agent locally

Run the agent directly and send it a request over HTTP. Start the agent from `src/agent`:

```powershell
python src/agent/app.py
```

From a second terminal, send a request:

```powershell
Invoke-RestMethod -Uri "http://localhost:8088/responses" `
    -Method POST -ContentType "application/json" `
    -Body '{"input": "The safety seal on the bottle was already broken when it arrived."}' | ConvertTo-Json -Depth 10
```

The response is an OpenAI Responses API object; the classification JSON is in the `text` field inside `output[].content[]`. When you are done, press **Ctrl+C** in the agent terminal to stop the local server.

## B3: Deploy with azd deploy

The lab environment has already provisioned the infrastructure, so deploy the service code from the repository root:

```powershell
azd deploy
```

This uploads the Python service defined in `agent.yaml`, builds it with the managed Python 3.12 runtime, and registers the new hosted-agent version.

## B4: Invoke the agent

Verify the agent is running:

```powershell
azd ai agent show --output table
```

Send messages to your hosted agent directly from the CLI:

```powershell
azd ai agent invoke "The tablets work well, but delivery was late."
azd ai agent invoke "I felt dizzy after taking the Caldova allergy relief tablets."
```

By default, `azd ai agent invoke` reuses the same conversation session. To start fresh, add `--new-session`.

## B5: Monitor logs

Stream the agent's container logs:

```powershell
azd ai agent monitor
```

Open a second terminal for log monitoring while you invoke the agent in the first.

## B6: Clean up

When you are done, clean up all Azure resources provisioned by azd:

```powershell
azd down
```

This removes the hosted agent deployment and any infrastructure provisioned by azd.

## CLI command reference

| Command | Purpose |
|---------|---------|
| `azd deploy` | Rebuild and redeploy the hosted-agent code (skip provisioning) |
| `azd ai agent show` | Check agent status |
| `azd ai agent invoke "msg"` | Send a message to the agent |
| `azd ai agent monitor` | Stream container logs |
| `azd down` | Delete all resources |

## Stretch goal: add a topic or review category

Want to extend the agent before wrapping up? Add `COMPETITOR_MENTION` to the agent instructions in `src/agent/app.py`, decide how the routing layer should handle it, then redeploy:

```powershell
azd deploy
```

Test the new value in the hosted-agent playground. This reinforces the direct edit → deploy → validate cycle.

## What you learned

- ✅ How hosted agents run your code as a managed service on Foundry
- ✅ How `ResponsesHostServer` exposes the current Responses protocol
- ✅ Why platform-managed history pairs with `store: False`
- ✅ How to test a hosted agent locally with the Agent Inspector (F5) before deploying
- ✅ How to deploy with `azure.yaml` and `azd deploy`, and validate in Foundry Toolkit
- ✅ How to invoke, monitor, and manage hosted agents

## Key takeaway

> A Foundry hosted agent can be deployed directly from Python source. The repository defines behavior in `app.py`, hosting in `azure.yaml`, and deployment through `azd deploy` -- and the entire workflow happens inside VS Code with the Foundry Toolkit.

======

# Part 7: Workshop summary and learning outcomes

> **Duration:** ~10 minutes

## Objective

Review the complete journey from discovering a model in the Foundry catalog to deploying a production-ready hosted agent for Caldova's B2C consumer sentiment analysis. This lab consolidates what you built, the skills you acquired, and where to go next.

## What you built

Across the labs, you -- as an AI developer on Caldova's commercial digital and customer engagement team -- constructed a **consumer sentiment analysis pipeline** end-to-end, from a blank terminal to a cloud-hosted agent accessible via REST API.

!IMAGE[mermaid_diagram3.png](instructions343795/mermaid_diagram3.png)

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

## Skills acquired

**Azure & infrastructure**
- Navigating the Foundry Toolkit for VS Code and the model catalog
- Managing Azure resources (AI Services, RBAC, monitoring)
- Understanding Foundry project architecture (accounts, projects, deployments, capability hosts)

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
| `src/agent/agent.yaml` | Hosted agent manifest |
| `src/agent/Dockerfile` | Container definition for the hosted agent |
| `.env` | Local environment configuration |
| `azure.yaml` | azd project configuration |

## Key patterns and takeaways

1. **Prompt engineering drives behavior.** A well-structured system prompt turns a general-purpose model into a specialized analyst.
2. **Business logic wraps model output.** Models provide probabilistic output; your code makes deterministic routing decisions.
3. **Start cheap, escalate smart.** Use a fast, cheap model for most requests and route only low-confidence cases to a more capable model.
4. **Validate before deployment.** Test with the Agent Inspector, then validate again in the hosted-agent playground after `azd deploy`.
5. **Keep regulated routing independent.** Sentiment and regulated review categories are separate signals -- never route on sentiment alone.

## Next steps

- **Add more topics or review categories** -- for example, route competitor mentions to a competitive-intelligence queue.
- **Add tools to the agent** -- look up a consumer's case history or notify Caldova's pharmacovigilance team via a webhook when a POTENTIAL_ADVERSE_EVENT is detected.
- **Build a multi-agent workflow** -- chain the sentiment agent with a response-drafting agent.
- **Connect to a frontend** -- the hosted agent exposes an OpenAI-compatible REST API at `/responses`.
- **Set up CI/CD** -- use GitHub Actions with `azd` to redeploy on every push that changes `src/agent/**`.

## Thank you

You started with a model in a catalog and finished with a production-ready hosted agent on Microsoft Foundry. The patterns you learned -- prompt engineering, structured output, confidence-based routing, and direct-code deployment -- apply to any AI application, not just consumer sentiment analysis.

If you encountered any issues during this lab or would like to try it self-paced, see the repository issues page.

!IMAGE[Report issues](../images/issues.png)

Happy building!
| `azure.yaml` | Direct-code hosted-agent configuration |

## Continue learning

- [Microsoft Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [OpenAI Responses API](https://learn.microsoft.com/azure/foundry/openai/how-to/responses)
- [Microsoft Foundry hosted agents](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents)

If you encountered an issue, use the repository support guidance after the lab.

**Happy building!**
