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

    You may also see `MODEL_DEPLOYMENT_NAME_2`, which is optional for the model comparison lab.
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
    ❌ Failed:  0

    Result: PASS -- lab is ready!
    ```

    The exact check count can change as the workshop evolves. Confirm that the failed count is zero and the final result is `PASS`.

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

> **Duration:** ~20 minutes, plus an optional 10-15 minute evaluation extension

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

The Foundry Toolkit and `azd` build your agent code into the hosted service and deploy it to Foundry Agent Service. At runtime, the platform provisions a sandbox and exposes a dedicated endpoint that your agent uses to call Foundry models.

!IMAGE[Hosted agent architecture](../images/mermaid_diagram2.png)

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

- The Foundry Toolkit extension installed and signed in to Azure (from Lab 1).
- Azure Developer CLI (`azd`) 1.27.1 or later.
- The Microsoft Foundry extension bundle installed with `azd ext install microsoft.foundry`.
- `.env` with `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` set.

Install the agent dependencies (separate from the main lab requirements):

```powershell
pip install -r src/agent/requirements.txt
```

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
        deployments:
            - name: gpt-5.4-mini
              model:
                  format: OpenAI
                  name: gpt-5.4-mini
                  version: "2026-03-17"
              sku:
                  name: GlobalStandard
                  capacity: 10
    caldova-consumer-sentiment-agent:
        host: azure.ai.agent
        project: src/agent
        codeConfiguration:
            runtime: python_3_13
            entryPoint: app.py
            dependencyResolution: remote_build
        uses:
            - ai-project
        kind: hosted
        name: caldova-consumer-sentiment-agent
        protocols:
            - protocol: responses
              version: 2.0.0
        environmentVariables:
            - name: AZURE_AI_MODEL_DEPLOYMENT_NAME
              value: gpt-5.4-mini
        container:
            resources:
                cpu: "1.0"
                memory: 2Gi
infra:
    provider: microsoft.foundry
```
---

## Install agent dependencies

> This step is shared by both Part A and Part B — do it once before you start.

The agent uses packages that are separate from the main lab requirements, and both deployment paths need them. Install them first:

```powershell
pip install -r src/agent/requirements.txt
```

This includes the Agent Framework hosting adapter and **debugpy** for local debugging.

======

# Part A: Test locally with the Agent Inspector

Before creating a cloud version, run the same Python entry point locally and check its Responses endpoint through the Foundry Toolkit.

1. In VS Code, open **Run and Debug**.
2. Select **Debug Agent with Agent Inspector**.
3. Press **F5**. The configured tasks start `src/agent/app.py`, wait for port `8088`, and open the Agent Inspector.
4. Send this feedback:

   ```text
   The delivery was late, but support kept me informed.
   ```

5. Confirm that the response is one JSON object with sentiment, confidence, topics, review category, and summary fields.

The exact labels can vary, but the agent should identify both the delivery problem and the positive support experience. Stop the debugger when the check is complete.

## Local checkpoint

The Agent Inspector receives a valid JSON response and the local server reports no authentication or startup errors.

======

# Part B: Deploy and verify the hosted agent

Local testing proves the code and prompt work together. Deployment packages the Python source, builds it remotely with the managed Python 3.13 runtime, and creates an immutable hosted-agent version.

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

Later code-only changes use `azd deploy` instead. Each successful deployment creates an immutable agent version.

Check that the deployed version is active:

```powershell
azd ai agent show --output json
```

Send one deployed smoke test:

```powershell
azd ai agent invoke caldova-consumer-sentiment-agent "The delivery was late, but support kept me informed."
```

The response should contain valid governed JSON. The `show` command also returns the Responses endpoint and a Foundry Playground URL for visual testing.

## Cloud checkpoint

The agent status is `active`, and the remote invocation returns a JSON object without storing credentials in source code.

======

# Part C: Generate an evaluation suite (optional preview)

Evaluation generation creates synthetic cases and evaluators from the Caldova quality and safety brief. It complements the one-off invocation above with repeatable, scored coverage.

> **Preview and cost notice:** Generation and evaluation make billable model calls and can take several minutes. Skip this section during the core workshop when time is limited.

```powershell
azd ai agent eval generate `
    --agent caldova-consumer-sentiment-agent `
    --gen-instruction-file src/agent/evaluation-instructions.md `
    --eval-model gpt-5.4-mini `
    --max-samples 15 `
    --out-file eval.yaml
```

Inspect the generated dataset, evaluator definitions, rubric, and `eval.yaml` before running them. Confirm that the cases cover valid JSON, ordinary and mixed sentiment, regulated routing, and the prohibition on medical advice.

```powershell
azd ai agent eval run --config eval.yaml
```

Before changing the agent because of a low score, open a failed row and compare the rubric explanation with `sample.output_text`. If `sample.output_text` is valid JSON but the explanation describes a list, annotations, or an output-item wrapper, the preview evaluator graded Responses transport metadata instead of the assistant text. Refine the generated rubric to grade `sample.output_text`, upload it with `azd ai agent eval update --config eval.yaml --evaluator-only`, then rerun the evaluation.

If the mismatch persists or valid assistant text is marked not applicable, report the schema criterion separately as a preview evaluator limitation instead of treating the aggregate pass rate as the agent's structured-output quality.

Compare this exploratory suite with `src/agent/evals/caldova-golden.jsonl`. Generated cases broaden coverage; the human-reviewed golden cases protect regulated-routing behavior when the prompt, model, or tools change.

## CLI command reference

| Command | Purpose |
|---------|---------|
| `azd up` | Provision the Foundry project and deploy the hosted agent |
| `azd deploy` | Rebuild and redeploy the hosted-agent code (skip provisioning) |
| `azd ai agent show` | Check agent status |
| `azd ai agent invoke "msg"` | Send a message to the agent |
| `azd ai agent monitor` | Stream container logs |
| `azd ai agent eval generate` | Generate a dataset, evaluators, and evaluation recipe |
| `azd ai agent eval run` | Run a generated evaluation recipe |
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
- ✅ How to provision and deploy with `azure.yaml` and `azd up`, and validate in Foundry Toolkit
- ✅ How to invoke, monitor, and manage hosted agents
- ✅ How generated evaluations complement curated regression cases

## Key takeaway

> A Foundry hosted agent can be deployed directly from Python source. The repository defines behavior in `app.py`, hosting in `azure.yaml`, and the first deployment through `azd up` -- and the entire workflow can also run inside VS Code with the Foundry Toolkit.

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
| **What you did** | Tested Caldova's agent locally, deployed it as a hosted agent, validated it remotely, and optionally generated a structured evaluation suite |
| **Key skill** | Direct-code deployment, the Agent Framework SDK, hosted-agent lifecycle management, and evaluation generation |
| **Outcome** | A live, cloud-hosted **caldova-consumer-sentiment-agent** accessible via the OpenAI Responses API |

**Core concept:** A hosted agent turns local Python code into a managed service while Foundry handles runtime infrastructure and conversation history.

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
- Deploying Python code to Foundry Agent Service with `azure.yaml` and `azd up`
- Invoking and monitoring agents via the `azd ai agent` CLI
- Testing agents in the Foundry Toolkit hosted agents playground
- Generating structured evaluations and comparing synthetic coverage with curated regression cases

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
| `src/agent/evaluation-instructions.md` | Quality and safety criteria for generated evaluations |
| `src/agent/evals/caldova-golden.jsonl` | Curated hosted-agent regression cases |
| `.env` | Local environment configuration |
| `azure.yaml` | Foundry project, model, and direct-code hosted-agent configuration |

## Key patterns and takeaways

1. **Prompt engineering drives behavior.** A well-structured system prompt turns a general-purpose model into a specialized analyst.
2. **Business logic wraps model output.** Models provide probabilistic output; your code makes deterministic routing decisions.
3. **Start cheap, escalate smart.** Use a fast, cheap model for most requests and route only low-confidence cases to a more capable model.
4. **Validate before deployment.** Test with the Agent Inspector, then validate again in the hosted-agent playground after `azd deploy`.
5. **Keep regulated routing independent.** Sentiment and regulated review categories are separate signals -- never route on sentiment alone.
6. **Use complementary evaluation sets.** Generated suites discover cases; curated golden sets compare agent versions against fixed expectations.

## Next steps

- **Add more topics or review categories** -- for example, route competitor mentions to a competitive-intelligence queue.
- **Add tools to the agent** -- look up a consumer's case history or notify Caldova's pharmacovigilance team via a webhook when a POTENTIAL_ADVERSE_EVENT is detected.
- **Build a multi-agent workflow** -- chain the sentiment agent with a response-drafting agent.
- **Connect to a frontend** -- the hosted agent exposes an OpenAI-compatible REST API at `/responses`.
- **Set up CI/CD** -- use GitHub Actions with `azd` to redeploy on every push that changes `src/agent/**`.
- **Add an evaluation quality gate** -- run the curated golden suite before promoting a new agent version.

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
