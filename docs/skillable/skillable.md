@lab.Title

## Welcome to ILL335

This Frontier Tour lab is **Building & Deploying AI Agents with Microsoft Foundry**.

To begin, log in to the virtual machine with:
+++@lab.VirtualMachine(ILL335:Win11).Password+++

# Part 1: Discover Foundry-hosted models

> **Duration:** ~10 minutes

## Scenario

You are an AI developer on Caldova's commercial digital and customer engagement team.Caldova's B2C channels receive thousands of pieces of consumer feedback daily about its products and support services. Your task is to build a **consumer sentiment analysis tool** that classifies feedback sentiment and independently routes regulated signals -- such as potential adverse events, product quality complaints, and medical inquiries -- to the right human reviewers.

In this lab, you will explore the Microsoft Foundry model catalog -- directly inside Visual Studio Code using the **Foundry Toolkit** extension -- to find a model that can power Caldova's consumer sentiment analysis pipeline.

## Objective
Explore the Foundry Toolkit model catalog in Visual Studio Code to discover available hosted models, understand model capabilities, and identify a model suitable for inference-based tasks like product review moderation.

## Step 1: Open the project in VS Code

1. Open Visual Studio Code by launching it from the Start menu or desktop.
2. You should see the lab workspace loaded and the project files in the sidebar.


## Step 2: Open the Foundry Toolkit in Visual Studio Code

The [**Foundry Toolkit** extension](https://aka.ms/ftk_install) is already installed on the lab virtual machine, so you can explore models without leaving your editor -- no web browser required.

1. In the **Activity Bar** on the left, click the **Foundry Toolkit** icon to open the toolkit panel.

    !IMAGE[ftk_icon.png](instructions356855/ftk_icon.png)
2. Click **Set Foundry Project → Switch Project → Sign in to Azure**.
3. Confirm you want to sign in, by clicking on **Allow**.

    !IMAGE[confirm_login.png](instructions356855/confirm_login.png)
4. When prompted to sign in to Azure to access your Foundry resources, use the following Azure credentials:

    Username: +++@lab.CloudPortalCredential(User1).Username+++

    If prompted for a Temporary Access Pass (TAP): +++@lab.CloudPortalCredential(User1).AccessToken+++

    If prompted for a Password: +++@lab.CloudPortalCredential(User1).Password+++
5. When asked if you wish to **Sign in to all apps and websites on this device**, select **No, this app only**.
6. After signing in, select the Foundry project that shows up in the list. This is the project pre-provisioned for you in the lab environment, and it contains the model deployments you will use for Caldova's consumer sentiment analysis system.

> **Note:** If no Foundry Projects is retrieved and listed for selection, it probably means that the resources provisioning for the lab hasn't been completed yet. Move to step 3 and continue exploring the model catalog while waiting for the provisioning to complete. then come back to this step in a few minutes and retry. 

!IMAGE[no_matching_resources.png](instructions356855/no_matching_resources.png)

The toolkit panel is your central hub for browsing models, testing them in a playground, and working with agents -- all from within VS Code.

## Step 3: Explore the model catalog

In the Foundry Toolkit panel, under **Developer Tools**, select **Model Catalog** to open the model catalog view. These are production-ready, hosted models you can use without fine-tuning.

!IMAGE[model_catalog.png](instructions356855/model_catalog.png)
    
> **Tip:** You can close the GitHub Copilot Chat window on the right side of the editor for now to have more space to explore the model catalog.

Browse the available models. Use the filters on the left side panel of the catalog UI to narrow the list -- for example, by Publisher (Azure OpenAI, Microsoft, Meta, Mistral, etc.), by where the model is **hosted by** (such as Microsoft Foundry), or by feature (Web Search, Image Attachment, etc.).

> **Note:** If you cannot see the filters on the left side of the catalog, look for **All filters** in the top right corner. 
> !IMAGE[filters.png](instructions356855/filters.png)

Select a model to view its model card. This will open a browser page with model's details. 

> **Note:** This section is meant to make you familiarize with the model catalog and how to explore model details. You don't need to deploy any model, as the model you are going to use later in the lab is already pre-provisioned in the Foundry project you selected as workspace.

The **gpt-5.4-mini** model from Azure OpenAI is high quality, fast, and cost-efficient, which makes it ideal for Caldova's consumer sentiment analysis pipeline. To find the model and view its details follow these steps:

1. Apply the filters **Hosted by** -> **Microsoft Foundry** and **Publisher** -> **OpenAI**.
2. Type **gpt-5.4-mini** in the search bar to locate the model.

    !IMAGE[findmodel.png](instructions356855/findmodel.png)
3. Click on the model name to open the model card and explore its details.

    If the VS Code confirmation dialog **"Do you want Code to open the external website?"** appears, click **Open** to continue. The model card opens in your web browser.

    !IMAGE[model_card_open_confirmation.png](instructions356855/model_card_open_confirmation.png)

    You'll see 4 main tabs:

    - **Details** -- Model description and capabilities
    - **Benchmarks** -- Scores and performance metrics
    - **Responsible AI** -- Guardrails imposed on the model from Azure AI Content Safety
    - **License** -- Links to applicable licensing terms

    More properties are listed in the table on the right side of the model card.

    | Property | Common values |
    |----------|---------------|
    | Type | Chat completion, Responses, etc |
    | Publisher| Anthropic, Cohere, Deepseek, OpenAI, etc |
    | Output type | text, image, code, etc |
    | Context window | Varies by model (see model card) |
    | Token limits | Varies by model (see model card) |

> **Note:** The model card is opened in a web browser page. Make sure to return to VS Code after reviewing it to continue with the lab.

## Step 4: Explore the playground (Optional)

1. Back in VS Code, under **Developer Tools → Build** in the toolkit panel, open the **Model Playground**.
2. Select **gpt-5.4-mini** from the model dropdown.

> **Note:** You see this model listed because it is pre-provisioned in your Foundry project. You do not need to deploy it yourself. If you cannot see it, come back to step 2 and ensure you connected to the provisioned Foundry project correctly.

> **Tip:** If you cannot see the model/system prompt configuration panel, drag the instructions section to the right to extend the playground.

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

Validate that your lab project environment is configured correctly -- ensuring the **.env** file, dependencies, and CLI tools are all in place before you start writing code.

## Step 1: Validate the .env is correct

In VS Code, navigate to the file explorer and ensure that the **.env** file has been created in the root of your project.

1. Open the **.env** file from the root of the project folder.
2. Confirm the following variables exist:

    ```text
    PROJECT_ENDPOINT
    MODEL_DEPLOYMENT_NAME
    MODEL_DEPLOYMENT_NAME_2
    AZURE_LOCATION
    AZURE_PRICING_CURRENCY
    ```

    **MODEL_DEPLOYMENT_NAME_2** is used only by the optional model comparison lab.
3. These values are generated  and pre-filled by an automated script that runs before the lab machine is started. If a value is missing or still contains a placeholder, contact your instructor or proctor instead of replacing the managed **.env** with **.env.sample**.

> **Tip:** To confirm the project endpoint, navigate to https://ai.azure.com, from the VM browser and sign in, with the credentials you used to configure your project in the Foundry Toolkit extension. You'll see the project endpoint on the project home page. 

!IMAGE[foundry_project_home.png](instructions356855/foundry_project_home.png)
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

    The exact check count can change as the workshop evolves. Confirm that the failed count is zero and the final result is **PASS**.

If any checks fail, the output tells you exactly what to fix. Common issues:

| Failure | Fix |
|---------|-----|
| Missing file | Re-check your azd provision output for errors |
| CLI not found | Install the missing tool (see SETUP.md) |
| Package not installed | Run **pip install -r requirements.txt** inside your **.venv** |
| .env not configured | Copy **.env.sample** to **.env** and fill in your endpoint |

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

Open **src/01_first_inference.py**. The script first loads configuration and creates a project client with your signed-in Azure identity:

```python
load_dotenv()

endpoint = os.environ.get("PROJECT_ENDPOINT")
model = os.environ.get("MODEL_DEPLOYMENT_NAME")

project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)
```

- **Loads** the project endpoint and model deployment from **.env**.
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

- **Returns** generated text through **response.output_text**.
- **Reports** completion state through **response.status**.
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
| Missing **PROJECT_ENDPOINT** | **.env** is missing or incomplete | Restore the value produced in Lab 2 |
| **DefaultAzureCredential** failed | Azure sign-in expired | Run **az login** |
| Resource not found | Deployment name does not match | Verify **MODEL_DEPLOYMENT_NAME** |
| Request remains incomplete | Service or safety condition interrupted generation | Inspect **response.status** and the full response |

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

> **Note:** Whenever you edit one file of your project save it ('CTRL+S' or '⌘+S') before running the script again. 

> **Tip** If you get errors when running the new version of the script, double check the indention is correct. 

## Step 4: Try multi-turn continuity

The Responses API can continue from an earlier response by passing its ID. In a temporary experiment, add a follow-up after the first request. Paste the following code at the end of the main() function in your script:

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
- **Keeps** the follow-up focused through **previous_response_id**.

Do not include sensitive personal or medical data in prompts. For production workloads, follow your organization's data-handling and retention requirements.

## What you learned

- ✅ How to authenticate with **DefaultAzureCredential**
- ✅ How to obtain an OpenAI-compatible client from **AIProjectClient**
- ✅ How to call **responses.create()** with **instructions** and **input**
- ✅ How to read **output_text**, response status, and token usage
- ✅ How to continue a conversation with **previous_response_id**

## Key takeaway

> The Responses API provides one beginner-friendly pattern for model interaction: send instructions and input with **responses.create()**, then inspect output text, status, and usage.

======

# Part 4: Build Caldova's consumer sentiment analysis application

> **Duration:** ~20 minutes, plus an optional 10-15 minute evaluation extension

## Objective

Build a working consumer sentiment analysis pipeline for Caldova's B2C engagement channels. The system accepts customer-submitted product reviews, classifies them using a Foundry-hosted model, applies moderation logic, and outputs structured results - ensuring that reviews from customers are safe and helpful before going live on the site.

## The problem

Caldova's B2C channels receive thousands of pieces of consumer feedback daily about products such as allergy relief tablets and topical relief gel, plus support interactions. Manual review does not scale. You need an automated system that can:

1. Accept consumer feedback as input.
2. Classify its sentiment (positive, neutral, negative, or mixed) and topics.
3. Independently identify regulated signals that require human review.
4. Return a structured decision with an evidence-based summary.
5. Handle edge cases gracefully.

Sentiment classification and regulated routing are **independent** of each other -- a POSITIVE piece of feedback can still contain a potential adverse event, and a NEGATIVE piece of feedback might simply reflect a delivery delay with no regulated content at all.

## Architecture

!IMAGE[Caldova sentiment analysis and governed routing architecture](instructions356855/architecture_agent.png)

The model runs in Foundry; JSON parsing and routing run in the local Python application. A content filter block produces **CONTENT_SAFETY** with confidence **0.0** and is escalated. Invalid JSON instead produces **NONE** with confidence **0.0** and is routed to **REVIEW_LOW_CONFIDENCE**. The script returns and prints action labels; it does not implement review queues or a dashboard.

This pipeline uses **prompt-based JSON**: the system prompt instructs the model to respond only with valid JSON. For even stricter guarantees, OpenAI models support [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs), a **response_format** parameter that constrains the model to conform to a JSON schema. This lab uses the prompt-based approach for simplicity and portability across model providers.

## Step 1: Review the system prompt

The key to reliable sentiment analysis is a well-structured system prompt. Open **src/02_sentiment_analysis.py** and examine the **SYSTEM_PROMPT**:

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
**Eliminates free-text noise** -- "Do not include any text outside the JSON object".

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
            "review_category": "NONE",
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
| try/except around json.loads() | Falls back to NONE with confidence 0.0, resulting in REVIEW_LOW_CONFIDENCE, if the model returns malformed output |

### 2b. Apply governed routing logic

```python
def route_feedback(result: dict) -> str:
    """Route insights to analytics or an appropriate human review queue."""
    review_category = result.get("review_category", "NONE")
    confidence = result.get("confidence", 0.0)

    if review_category != "NONE":
        return "ESCALATE_FOR_REVIEW"
    if confidence < 0.8:
        return "REVIEW_LOW_CONFIDENCE"
    return "ADD_TO_SENTIMENT_DASHBOARD"
```

This adds a **business logic layer** on top of the model's analysis:

- Any regulated **review_category** (not **NONE**) → escalate for human review, regardless of sentiment or confidence.
- High-confidence, non-regulated feedback → add to the sentiment dashboard for trend reporting.
- Low-confidence, non-regulated feedback → route to a human for a second look.

Routing is driven entirely by **review_category** and **confidence** -- **never** by **sentiment**. A POSITIVE review can still be escalated (for example, positive feedback that also mentions a symptom).

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
        "review_category": analysis.get("review_category", "NONE"),
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
  ESCALATED:   3
```

> **Note:** Some feedback containing threats or explicit content may be blocked by Azure's built-in content safety filter *before* reaching the model. When this happens, the application handles it gracefully and labels the result with review_category CONTENT_SAFETY. This is expected behavior -- the content filter is an additional layer of protection in production deployments.

## Step 4: Test with custom feedback

The application also accepts interactive input. Run it with the **--interactive** flag:

```powershell
python src/02_sentiment_analysis.py --interactive
```

Type feedback to analyze it in real time

```text
What dose should I give my child?
```

You should get something similar to:

```text
Feedback: "What dose should I give my child?"
Sentiment: NEUTRAL (confidence: 0.98)
Topics: OTHER
Review category: MEDICAL_INQUIRY
Summary: The user is asking for personalized dosing guidance for a child, which is a medical inquiry. No product experience or support issue is described.
Action: ⚠️ ESCALATE_FOR_REVIEW
```

Confirm that the application routes the medical inquiry for human review and does not provide medical advice. Type **quit** to exit.

## Step 5: Test with the sample dataset

The **src/sample_feedback.json** file contains a broader set of test feedback spanning positive, neutral, negative, mixed, adverse-event, product-quality, and medical-inquiry cases. Run the batch test:

```powershell
python src/02_sentiment_analysis.py --file src/sample_feedback.json
```

## Step 6: Customize the routing logic

In this exercise, first try changing the confidence threshold, then add a specific rule for the **SUPPORT** topic. Make these changes in the VS Code editor, not in the terminal.

### 6a. Try a different confidence threshold

1. Open **src/02_sentiment_analysis.py** and find **def route_feedback**.
2. Change **if confidence < 0.8:** to one of the alternatives below, then press **Ctrl+S**.

| Code change | Effect on feedback whose review category is NONE |
|-------------|-------------------------------------------------|
| `if confidence < 0.6:` | Confidence from 0.6 up to, but not including, 0.8 can now reach the dashboard |
| `if confidence < 0.9:` | Confidence from 0.8 up to, but not including, 0.9 now needs a low-confidence human check |

3. From the repository root, rerun the same five built-in samples:

```powershell
python src\02_sentiment_analysis.py
```

**Expected result:** The threshold can change routing for non-regulated feedback. Regulated feedback must still return **ESCALATE_FOR_REVIEW**, regardless of confidence. The model may return different classifications on each run, and the five samples may not include a confidence value in the changed range.

### 6b. Add a SUPPORT topic rule

**Business rule:** When feedback has the **SUPPORT** topic, review category **NONE**, and confidence **at least 0.8**, return **REVIEW_SUPPORT_FEEDBACK** instead of sending it straight to the sentiment dashboard. This represents a customer-support review decision; the lab prints the label but does not create a real support queue or ticket.

1. In **src/02_sentiment_analysis.py**, replace **only** the existing **route_feedback** function with the following code. This restores the confidence threshold to **0.8** and adds the topic check **after** the regulated-category and low-confidence checks:

```python
def route_feedback(result: dict) -> str:
    """Route insights to analytics or an appropriate human review queue."""
    review_category = result.get("review_category", "NONE")
    confidence = result.get("confidence", 0.0)

    if review_category != "NONE":
        return "ESCALATE_FOR_REVIEW"
    if confidence < 0.8:
        return "REVIEW_LOW_CONFIDENCE"
    if "SUPPORT" in result.get("topics", []):
        return "REVIEW_SUPPORT_FEEDBACK"
    return "ADD_TO_SENTIMENT_DASHBOARD"
```

2. Press **Ctrl+S**. Keep the checks in that order:

| Input | Expected action |
|-------|-----------------|
| SUPPORT, NONE, confidence 0.95 | **REVIEW_SUPPORT_FEEDBACK** |
| SUPPORT, NONE, confidence 0.5 | **REVIEW_LOW_CONFIDENCE** |
| SUPPORT with POTENTIAL_ADVERSE_EVENT, confidence 0.95 | **ESCALATE_FOR_REVIEW** |
| VALUE, NONE, confidence 0.95 | **ADD_TO_SENTIMENT_DASHBOARD** |

3. Check these fixed cases without making Azure calls. In VS Code Explorer, right-click **src**, select **New File**, and name it **check_routing.py**. Paste the following **Python file content** into the editor and save it:

```python
from importlib import import_module

route_feedback = import_module("02_sentiment_analysis").route_feedback

checks = [
    ("Support feedback", {"topics": ["SUPPORT"], "review_category": "NONE", "confidence": 0.95}),
    ("Low confidence", {"topics": ["SUPPORT"], "review_category": "NONE", "confidence": 0.5}),
    ("Regulated feedback", {"topics": ["SUPPORT"], "review_category": "POTENTIAL_ADVERSE_EVENT", "confidence": 0.95}),
    ("Other topic", {"topics": ["VALUE"], "review_category": "NONE", "confidence": 0.95}),
]

for name, result in checks:
    print(f"{name}: {route_feedback(result)}")
```

4. Return to the terminal at the repository root and run:

```powershell
python src\check_routing.py
```

**Expected output:**

```text
Support feedback: REVIEW_SUPPORT_FEEDBACK
Low confidence: REVIEW_LOW_CONFIDENCE
Regulated feedback: ESCALATE_FOR_REVIEW
Other topic: ADD_TO_SENTIMENT_DASHBOARD
```

If any label differs, check the function's indentation, condition order, and saved changes before continuing.

5. Rerun **python src\02_sentiment_analysis.py** to see the rule applied to the same five model-analyzed samples. This makes additional model calls. The delivery/customer-support sample can now show **REVIEW_SUPPORT_FEEDBACK** if it is classified as **SUPPORT**, **NONE**, and confidence at least **0.8**. Regulated signals must still take priority. Use the fixed cases above, rather than a guaranteed model label, to verify the rule itself.
6. After the experiment, restore the standard routing for later labs: remove only the **if "SUPPORT" ...** line and its **return "REVIEW_SUPPORT_FEEDBACK"** line, keep the threshold at **0.8**, and save. Delete the temporary **src/check_routing.py** file.

**Checkpoint:** You can explain the routing order: regulated review first, low-confidence review second, the custom topic rule third, and the dashboard otherwise. Sentiment does not determine the routing action.

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
| gpt-5.4-mini | Fast, cost-efficient, good for simple tasks | May miss nuances in complex cases |
| gpt-5.4 | Higher reasoning quality, better at edge cases | Slower, more expensive |
| Phi-4 | Open-weight, strong reasoning, runs on-device | May need different prompt tuning |

Comparing models on your **actual Caldova feedback data** helps you make informed deployment decisions before you go live.

## Prerequisites

Your given workspace already includes a **.env** file with the classroom project endpoint, model names, Azure region, and pricing currency. You can review the managed values with:

```powershell
Get-Content .env
```

The file should include these settings. 

```ini
MODEL_DEPLOYMENT_NAME=gpt-5.4-mini
MODEL_DEPLOYMENT_NAME_2=gpt-5.4
AZURE_LOCATION=<managed-lab-region>
AZURE_PRICING_CURRENCY=USD
```

To complete this lab, you also need the **gpt-5.4** deployment described below.
To compare model pricing, the script first uses the Azure Retail Prices API. This API is public, so it does not require another API key or sign-in. If the newly released GPT-5.4 meters are not yet present, the script uses the published Global Standard USD rates from the Azure OpenAI pricing page and labels that fallback in the output.

### Deploying a new model

If you only have one model deployed, deploy a second one from the Foundry Toolkit Model Catalog:

1. Click the Foundry Toolkit icon in the VS Code Activity Bar to open the extension panel.
2. Navigate to **Developer Tools → Discover → Model Catalog**.
3. Apply the filter **Hosted by → Microsoft Foundry** to see all Foundry-hosted models.
4. In the search bar type **gpt-5.4**.
5. Click **Deploy → Custom Deploy**.
6. Leave parameters as default and confirm by clicking on **Deploy to Microsoft Foundry**.

Wait for the deployment to complete before proceeding. You should see the pop-up below once complete.

!IMAGE[Foundry Toolkit Deployment Complete](instructions356855/ftk_deployment_success.png)

> **Note:** If you are unable to deploy a second model, skip this lab and proceed to Lab 6.

## Step 1: Review the comparison code

Open **src/03_model_comparison.py**. The script retrieves input and output token rates from the unauthenticated [Azure Retail Prices API](https://learn.microsoft.com/rest/api/cost-management/retail-prices/azure-retail-prices), with a dated fallback to the [Azure OpenAI pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for the two Global Standard lab models, then runs the same feedback through each model:

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

    Pricing estimate: USD (Azure published retail rates)
    gpt-5.4-mini pricing source: Azure OpenAI pricing page, verified <date>
    gpt-5.4-mini rates: input $<current-rate>/1M tokens, output $<current-rate>/1M tokens
    gpt-5.4-mini estimated retail cost: $<run-cost> (<input> input + <output> output tokens)
    gpt-5.4 pricing source: Azure OpenAI pricing page, verified <date>
    gpt-5.4 rates: input $<current-rate>/1M tokens, output $<current-rate>/1M tokens
    gpt-5.4 estimated retail cost: $<run-cost> (<input> input + <output> output tokens)
    Cost saving: gpt-5.4-mini saved <percent>% ($<amount>) vs gpt-5.4 for this run
```

Pricing and token totals change over time, so your output will contain numbers in place of the placeholders above.

## Step 3: Analyze the results

Look for patterns in the comparison:

- **Agreement** -- Do both models agree on sentiment and review_category? If they disagree on a regulated signal like POTENTIAL_ADVERSE_EVENT, which model would you trust?
- **Confidence** -- Does the more capable model consistently give higher confidence scores? Higher confidence may justify the extra cost for borderline feedback near the escalation threshold.
- **Latency** -- How much slower is the larger model? For real-time intake, latency matters; for nightly batch processing, it may not.
- **Cost** -- The script combines each response's actual input and output token counts with an Azure-published retail rate and billing unit. It prefers the Retail Prices API and uses the dated pricing-page fallback for these two models when needed. It then compares total observed run costs to show both the dollar difference and percentage saved.

The displayed amount is a retail cost estimate, not a billed charge. It does not include negotiated discounts, cached-token pricing, taxes, or other agreement-specific adjustments. See the [Azure OpenAI pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for billing details.

> **Note:** The fallback is USD-only and specific to the lab's Global Standard **gpt-5.4-mini** and **gpt-5.4** deployments. Other models, currencies, or deployment types still show **pricing unavailable** when the API has no matching meters.

> **Tip:** For this type of classification task, gpt-5.4-mini often matches gpt-5.4 performance at a fraction of the cost.

## Step 4: Try a hybrid approach

A common production pattern is to use the cheaper model first and escalate low-confidence results to the more capable model. The comparison script includes a **--hybrid** mode:

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

======

# Part 6: Deploy a hosted agent

> **Duration:** ~20 minutes, plus an optional 10-15 minute evaluation extension

## Objective

Deploy Caldova's consumer sentiment agent directly from Python source to Microsoft Foundry Agent Service. You will inspect the Agent Framework code, verify the direct-code service configuration in **azure.yaml**, test the agent locally with the Agent Inspector, deploy it to the cloud, and validate the hosted agent.

This lab has three parts. **Part A** tests the agent locally with the Foundry Toolkit. **Part B** deploys and verifies it with **azd**. **Part C** is an optional self-paced extension that generates and runs a structured evaluation against the deployed agent.

## What is a hosted agent?

A hosted agent is your agent application running on Foundry-managed infrastructure. Unlike the scripts in Labs 3-5 that run locally, a hosted agent is a persistent, cloud-hosted service that exposes the OpenAI Responses protocol. Foundry handles the heavy lifting:

- **VM-isolated sandboxes** -- each session runs in its own isolated sandbox with a persistent filesystem.
- **REST API** -- a protocol library exposes your agent as an OpenAI Responses API endpoint, callable by the Foundry Playground, other agents, or any application.
- **Per-session scaling** -- the platform creates a sandbox on demand and tears it down when idle.
- **Dedicated agent identity** -- each agent authenticates to Foundry models and Azure services with its own Azure identity (no keys to manage).
- **Managed conversation history** -- the platform maintains continuity between turns, so your `Agent` does not need a local message list.

## Architecture

The Foundry Toolkit runs the agent locally for inspection, while `azd` packages and deploys the source to Foundry Agent Service. At runtime, the platform provisions a sandbox and exposes a dedicated endpoint that your agent uses to call Foundry models.

!IMAGE[Hosted agent architecture](instructions356855/mermaid_diagram2.png)

| Property | This lab |
|----------|----------|
| Source |**src/agent/app.py** and **src/agent/requirements.txt** |
| Runtime | Python 3.13 |
| Host adapter | **ResponsesHostServer** |
| Protocol | Responses 2.0.0 |
| Deployment | Direct code through **azure.yaml** and **azd up** |
| History | Managed by the Foundry platform |
| Identity | Azure identity; no credentials stored in source |

> **Note:** The **microsoft.foundry** meta-extension installs compatible **azure.ai.** providers, including the project and hosted-agent providers used by this lab.

## Review the agent code

Open **src/agent/app.py**. The hosted agent imports the Foundry client and the Responses host:

```python
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential
```

- **Connects** through **FoundryChatClient** from **agent_framework.foundry**.
- **Hosts** the agent with the Responses adapter, **ResponsesHostServer**.
- **Authenticates** without hardcoded secrets.

The **Agent** uses the Caldova sentiment instructions and disables model-side response storage:

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
- **Prevents** duplicate response storage in the model call with **store: False**.

The entry point starts the Responses host:

```python
if __name__ == "__main__":
    ResponsesHostServer(agent).run()
```

- **Exposes** the agent through the Responses protocol expected by Foundry hosting.

### The deployment definition: azure.yaml

The root **azure.yaml** is the source of truth for the Foundry project, model deployment, and hosted agent. The **microsoft.foundry** provider provisions the project without the legacy capability-host infrastructure pattern. The agent uses direct source-code deployment with the managed Python 3.13 runtime:

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

## Verify agent dependencies

> The managed-lab lifecycle installs these dependencies before the session starts.

Confirm that VS Code is using the workspace virtual environment. The Python interpreter shown in the status bar should be **.venv**. 
!IMAGE[status_bar.png](instructions356855/status_bar.png)

If it is not, run **Python: Select Interpreter** from the Command Palette and choose **.venv\Scripts\python.exe**.

Then verify the environment:

```powershell
python -m pip check
python -c "import debugpy; print(debugpy.__version__)"
```

The agent environment includes the Agent Framework hosting adapter and **debugpy** for local debugging. If either command fails, notify the instructor rather than installing packages into the global Python interpreter.

======

# Part A: Test locally with the Agent Inspector

Before creating a cloud version, run the same Python entry point locally and check its Responses endpoint through the Foundry Toolkit.

1. In VS Code, open **Run and Debug**.
2. Select **Debug Agent with Agent Inspector**.

    !IMAGE[Debug with Agent Inspector](instructions356855/debug_with_agent_inspector.png)
3. Press **F5**. The configured tasks start **src/agent/app.py**, wait until its server is listening on port **8088**, and open the Foundry Toolkit Agent Inspector inside VS Code.
4. Send this feedback:

   ```text
   The delivery was late, but support kept me informed.
   ```

5. Confirm that the response is one JSON object with sentiment, confidence, topics, review category, and summary fields.

The exact labels can vary, but the agent should identify both the delivery problem and the positive support experience. Stop the debugger when the check is complete.

Inspect the **Overview** tab in the Agent Inspector to see a summary of the agent's status, recent requests, and responses. You'll also see:
- A **Tokens** panel showing the token usage for each request and response, as well as the total token count for the session.
- A **Events** panel showing the sequence of events for each request and response, including any errors or warnings.
- A **Tools** panel showing the details of tool calls made by the agent, including input parameters and output results. In this scenario, we do not have any tool calls.

!IMAGE[inspector_logs.png](instructions356855/inspector_logs.png)

The local entry point reads **PROJECT_ENDPOINT** and **MODEL_DEPLOYMENT_NAME** from the managed **.env** used in earlier parts. If the Inspector cannot connect, confirm the debug terminal reaches **AgentServerHost started** and update Foundry Toolkit before changing the agent code.

## Local checkpoint

The Agent Inspector receives a valid JSON response and the local server reports no authentication or startup errors.

======

# Part B: Deploy and verify the hosted agent

Local testing proves the code and prompt work together. Deployment packages the Python source, builds it remotely with the managed Python 3.13 runtime, and creates an immutable hosted-agent version.

The administrator lifecycle has already provisioned the project, installed the Foundry providers, and run the initial deployment. From the repository root, verify the CLI:

```powershell
azd version
```

Follow your instructor's directions to deploy a code update to the existing agent:

```powershell
azd deploy caldova-consumer-sentiment-agent
```

Each successful deployment creates an immutable agent version. Do not run **azd up**, select a different subscription, or reprovision resources in this managed lab.

Check that the deployed version is active:

```powershell
azd ai agent show --output json
```

Send one deployed smoke test:

```powershell
azd ai agent invoke caldova-consumer-sentiment-agent "The delivery was late, but support kept me informed."
```

The response should contain valid governed JSON. The **show** command also returns the Responses endpoint and a Foundry Playground URL for visual testing.

## Cloud checkpoint

The agent status is **active**, and the remote invocation returns a JSON object without storing credentials in source code.

======

# Part C: Generate an evaluation suite (optional preview)

A smoke test checks one response. In this part, you will request 15 test cases, check the generated dataset, run the cases against your deployed agent, and review the scores.

> **Preview and cost notice:** Generation and evaluation make billable model calls and can take several minutes. Skip this section during the core workshop when time is limited.

**Follow Steps 1-10 in order.** Stop if a command reports an error; use the troubleshooting table below before continuing. Each command block is a separate action: paste the whole block, press **Enter**, and wait for it to finish before pasting another.

**Where to paste:** Run only blocks labelled **powershell** in the terminal. Blocks labelled **yaml** or **json** are file content or examples, not terminal commands. Follow the editor instructions beside those blocks.

## Step 1: Open the correct terminal

1. Complete Part B first: the deployed agent must be active and its smoke test must work.
2. In VS Code, select **Terminal > New Terminal** and use **PowerShell**.
3. Make sure the terminal is at the repository root: the folder containing **azure.yaml**, **.env**, and **src**.
4. Keep this terminal open throughout Part C. The endpoint and run ID you set below belong to this terminal session.

## Step 2: Install the evaluations extension

run:

```powershell
azd extension install azure.ai.evaluations
```

**Expected result:** The extension installs successfully or is already installed. These instructions use **azure.ai.evaluations** **1.0.0-beta.2**, not the retired **azd ai agent eval** commands.

If installation fails or requires a newer CLI, See [evaluations extension guide](https://github.com/Azure/azure-dev/tree/main/cli/azd/extensions/azure.ai.evaluations) for command details.

## Step 3: Set the existing project endpoint

1. In VS Code Explorer, open the repository's existing **.env**.
2. Find **PROJECT_ENDPOINT=** and copy **only the value after =**, without surrounding quotes.
3. Run this block. When PowerShell displays the prompt, paste that value and press **Enter**:

```powershell
$env:FOUNDRY_PROJECT_ENDPOINT = Read-Host "Paste the existing PROJECT_ENDPOINT value"
if ([string]::IsNullOrWhiteSpace($env:FOUNDRY_PROJECT_ENDPOINT)) {
    throw "The existing Foundry project endpoint is required before continuing."
}
```

**Expected result:** PowerShell returns to the prompt without an error. The evaluations CLI can now use the same project as your agent. It does not automatically read the Python agent's **PROJECT_ENDPOINT** key from **.env**.

Do not print or share **.env**. Keep the lab's existing authenticated identity and subscription. If you open a new terminal later, repeat this step.

## Step 4: Generate the test cases and scoring rubric

Run the following command. It asks for **turn-level** cases: one request and response per row, not multi-turn conversation scenarios.

**--max-samples 15** requests up to 15 cases; it does not guarantee that the preview generator returns exactly 15. Wait for both generation jobs to finish, then check the actual count in Step 5 before initializing or running an evaluation.

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
| Agent | **caldova-consumer-sentiment-agent** |
| Dataset | **caldova-generated-turn** |
| Evaluation level | Turn |
| Number of cases | 15 |
| Dataset source | Prompt |
| Evaluator | **caldova-quality-turn** |
| Traces | Off |

**Expected result:** Both artifacts are downloaded, and **evals/azure.eval.yaml** contains their catalog entries. The files are normally **evals/datasets/caldova-generated-turn.jsonl** and **evals/evaluators/caldova-quality-turn.json**.

If the plan says **Conversation** or **scenarios**, cancel. If these names already exist, do not overwrite them automatically: use the recovery guidance below. Ignore the CLI's suggested next command for now; complete Step 5 first.

## Step 5: Check the generated dataset

**You do not need to run a command for this step.** Inspect the generated file in VS Code:

1. Press **Ctrl+P**, enter **evals\datasets\caldova-generated-turn.jsonl**, and press **Enter**.
2. Count the non-empty lines, with one JSON object per line. The exercise target is **15 non-empty lines**. Use the editor's line numbers; ignore a final blank line. If you see fewer, such as 13, follow the recovery instructions below before proceeding to Step 6.
3. Check every object has a **"query"** field containing feedback text in quotes. The text must not be empty.

   This is a simplified example of the required field, **not content to paste into the file**. Your generated objects may contain other fields too:

```json
{"query": "The delivery was late, but support kept me informed."}
```

4. Read the cases. Look for ordinary sentiment, mixed feedback, regulated review routing, and the prohibition on medical advice.
5. In Explorer, open **evals/evaluators/caldova-quality-turn.json**. Check that its scoring descriptions cover those requirements and valid JSON.

**Expected result:** You have reviewed 15 test cases, each with a non-empty **query**, and their scoring rubric.

**Stop before Step 6** if the file is empty, the number of cases differs from 15, or any object lacks feedback text in **query**. Record the actual number of cases and ask your instructor to check the generation output from Step 4. Objects containing only scenario fields such as **simulation_configuration** and **test_case_description** are conversation seeds, not the turn-level cases required here. Do not edit the file to force a pass.

**If fewer than 15 cases were generated:**

1. Confirm that both generation jobs have finished and inspect their output for errors. Do not start another generation while either job is still running.
2. Preserve the existing files and catalog. Do not add dummy rows, duplicate cases, or use **--force** to overwrite them.
3. With your instructor's approval, retry Step 4 once, changing only **--path evals** to **--path evals-retry-1**, an unused folder. Keep the dataset and evaluator names unchanged. This makes additional billable model calls and may produce different cases.
4. Repeat Step 5 using **evals-retry-1\datasets\caldova-generated-turn.jsonl** and **evals-retry-1/evaluators/caldova-quality-turn.json**. If the retry passes all Step 5 checks, use **--path evals-retry-1** instead of **--path evals** in every remaining evaluation command, and open files under **evals-retry-1/** instead of **evals/**. Do not mix the original dataset or rubric with the retry.
5. If that folder already exists, or the retry still fails the checks, stop and ask your instructor. You can skip this optional Part C and continue to **Part 7: Workshop summary and learning outcomes** rather than repeatedly generating billable replacements.

**Dataset count is not a pass count.** A 15-row dataset can yield **15 passed, 0 failed** or **13 passed, 2 failed**. Generated cases, agent responses, and preview evaluator judgments can vary between runs. Both totals account for 15 evaluated cases; inspect each failed case in Step 10 rather than regenerating until all cases pass.

## Step 6: Create the local evaluation configuration

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

1. In the preview, confirm the name and dataset are **caldova-generated-turn**, the evaluation level is **turn**, and the evaluator is **caldova-quality-turn**.
2. Confirm the agent is **caldova-consumer-sentiment-agent** and the judge model is **gpt-5.4-mini**.
3. When asked to add the evaluation, choose **Add evaluation**.
4. Open **evals/azure.eval.yaml** and confirm the new evaluation appears under **evals**.

**Expected result:** The CLI updates the local evaluation configuration and reports an evaluation service in the root **azure.yaml**. The service might be named **caldova-consumer-sentiment-agent-evals**; its name is not necessarily **evals**.

The evaluation is configured locally, but it is **not registered in Foundry yet**. The next step does that. Paths in **evals/azure.eval.yaml** are relative to that file; use its **file** and **source** values if artifact paths differ. The evaluation service uses **host: azure.ai.eval**, depends on **ai-project**, and references **./evals/azure.eval.yaml**.

## Step 7: Register the evaluation in Foundry

With your instructor's approval, run:

```powershell
azd ai eval create caldova-generated-turn --path evals
```

**Expected result:** The named evaluation and its referenced dataset and evaluator are registered, or reported unchanged if already registered. This does not rebuild the agent.

If this command fails, **stop before Step 8**. Do not use **azd up** or guess a service name as a workaround.

**Recover an evaluator version mismatch**

An error such as **version 3 on the project but 2 was recorded at the last deploy** means the published evaluator advanced since this local configuration last reconciled it, and the local definition differs. This is a conflict safeguard, not an agent deployment failure. Regeneration or a standalone **evaluator update** can leave the local and published definitions out of sync. A separate local retry folder does not isolate evaluator names in the same Foundry project.

1. Keep the current dataset, evaluator JSON, **azure.eval.yaml**, and **azure.eval.lock**. Back up the local evaluator JSON in VS Code before making changes. Do not delete the lock file or a published evaluator version, rerun generation, or use a standalone **evaluator update** to bypass the conflict.
2. Download the published version named in the error to a **new file**, not over the local rubric. For the example above, run:

```powershell
azd ai eval evaluator download caldova-quality-turn --version 3 --output-file evals\evaluators\caldova-quality-turn-project-v3.json
```

   Replace **3** and **v3** with the version in your error. If you used the Step 5 retry folder, use **evals-retry-1** instead of **evals** here and below. If the destination already exists, choose another unused filename; do not use **--force**. If your extension does not support **evaluator download**, stop and ask your instructor rather than guessing a replacement command.

3. Compare the downloaded rubric with the local backup. With your instructor, confirm that the published dimensions and scoring rules are appropriate. In **evals/azure.eval.yaml**, find the **caldova-quality-turn** evaluator's catalog entry and change only its **source** to **evaluators/caldova-quality-turn-project-v3.json**, relative to that YAML file. Keep the evaluator name and evaluation references unchanged. Save the file. **Do not merge local rubric edits yet**: first reconcile the unchanged published definition.
4. Repeat Step 7:

```powershell
azd ai eval create caldova-generated-turn --path evals
```

   **Expected result:** The published evaluator is reused and the local deployment record is reconciled; the named evaluation registers successfully. Only then proceed to Step 8. If the version advances again, or reconciliation still fails, stop and ask your instructor; do not repeatedly publish over it.

5. If you still need an intentional local rubric correction, review it against the backup and apply it to the JSON file now named by **source**, only after item 4 succeeds. Repeat Step 7 to publish that intentional change before starting a run. Do not regenerate cases just to obtain failures: all-pass results are valid.

## Step 8: Start one evaluation run

Run this command **once**:

```powershell
azd ai eval run start --path evals --eval caldova-generated-turn --no-wait
```

**Expected result:** The CLI accepts the run and returns a **run ID**. Copy that ID. Do not copy the dataset job ID from Step 4 or the evaluation ID from Step 7.

## Step 9: Wait for that run to finish

1. Copy the **run ID** from the output of Step 8.
2. In the line below, replace **YOUR-RUN-ID-HERE** with that ID. **Keep the double quotes.**
3. Paste your edited line into the same PowerShell terminal and press **Enter**:

```powershell
$runId = "YOUR-RUN-ID-HERE"
```

This saves your ID as **$runId** for the remaining commands. **No output is expected from this line.** Do not run it with the placeholder unchanged.

4. Run this command exactly as shown. PowerShell uses the ID you saved:

```powershell
azd ai eval run show --path evals --eval caldova-generated-turn --run $runId --wait
```

**Expected result:** The run reaches a terminal status and shows its results. A completed run can still contain failed test cases.

If monitoring times out, repeat only the **run show** command above with the same **$runId**. **Do not repeat Step 8** just to resume monitoring: it starts another billable run.

## Step 10: Review the scores and at least one result

1. In the Foundry Toolkit, expand **My Resources > Evaluations**.
2. Select **caldova-generated-turn** and the run you just completed. If the view is empty or asks you to sign in, follow the recovery guidance below; you can also complete this step using the CLI.
3. Review the scores for each criterion, not only the aggregate pass rate.
4. Open a failed or borderline case and read both the assistant response (**sample.output_text**) and the evaluator's explanation. If all cases passed, inspect one passing case instead.

**If Evaluations is empty or says you are not signed in**

A successful CLI run does not sign the Foundry Toolkit into Azure. The extension's session or selected project may differ from the CLI's; an empty view alone does not mean the evaluation failed.

1. In Foundry Toolkit, use **Set Foundry Project > Switch Project** to confirm the same pre-provisioned project used in Part B and Step 3. Do not select another subscription or create a project.
2. If the Toolkit reports **You are not signed in to an Azure account**, use its **Sign in to Azure** action and repeat the Part 1 sign-in flow with the managed lab account. If prompted to sign in to all apps and websites, select **No, this app only**. A browser or CLI sign-in alone does not establish the extension's session. If the prompt keeps returning, contact your instructor rather than changing the lab identity.
3. Reselect the existing project, close and reopen the **Evaluations** tab, and use **Refresh** if that action is available. Allow a short time for the view to synchronize, then reopen it. If it remains blank, save your files and run **Developer: Reload Window** from the Command Palette, then reopen Foundry Toolkit and the same project.
4. If the UI still does not list the run, use the existing PowerShell terminal to inspect it without starting another run:

```powershell
azd ai eval run show --path evals --eval caldova-generated-turn --run $runId
```

   Use **--path evals-retry-1** if you followed Step 5 recovery. If you opened a new terminal, repeat Step 3 and restore the **same run ID** as in Step 9. You can open the **Portal** link printed by the CLI and sign in with the same lab account, or review results using the commands below.

5. If the CLI shows the completed run and its results, continue with CLI review; Toolkit visibility is not required for this checkpoint. If the CLI also reports an authentication, permission, or project error, stop and share only the sanitized error with your instructor. Do not regenerate, re-register, redeploy, or start a replacement run just to refresh the UI.

**CLI review (also valid when the Toolkit UI is unavailable):** List failed cases in the terminal:

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

**The ITEM ID is the number in the first column.** In this example, the first failed case is item **1**, the second is item **2**, and the passing case is item **3**. Your numbers and results may differ. The values beginning with **eval_** and **evalrun_** identify the evaluation and run, not the individual case.

To open item **1**, run:

```powershell
azd ai eval run output show 1 --path evals --eval caldova-generated-turn --run $runId
```

Replace only the **1 immediately after show** to open a different listed item. For example, use **show 2** for item 2. Keep **$runId** as shown; it uses the run you saved in Step 9. **You do not need an $itemId variable.**

Alternatively, copy and run the complete command printed under **View details** in your own output. That command already contains the item number and the correct evaluation and run IDs.

**If some cases are missing from the table:** Results are paginated, normally 10 items at a time. A message such as **More items to come. Next page: --after 10** means there are additional cases, not that they were skipped. To list all failed cases across every page, run:

```powershell
azd ai eval run output list --path evals --eval caldova-generated-turn --run $runId --failed-only --all
```

Omit **--failed-only** if you want to list every case, including passes. Use each case's displayed **ITEM** number with **output show**.

!IMAGE[eval_results.png](instructions356855/eval_results.png)

**Expected result:** Using either the Toolkit/portal or the CLI, you can identify a case, its response, its score, and the explanation for that score. An empty Toolkit view does not block completion when the CLI results are available.

## Part C checkpoint

You have generated and checked 15 turn-level cases, registered an evaluation, completed a run, and reviewed a result. You can explain how this differs from the one-off smoke test in Part B.

**The main exercise is complete.** Continue to **Part 7: Workshop summary and learning outcomes**, or try the optional sections below.

## Troubleshooting and recovery

| What you see | What to do |
|--------------|------------|
| **unknown flag: --helpazd** | Two commands were joined together. Wait for the PowerShell prompt, then paste one complete command block at a time. |
| **no Foundry project endpoint resolved** | Repeat Step 3 in the same terminal, then retry the command that failed. Do not create a new project. |
| Existing **caldova-generated** conversation artifacts | Keep them. Steps 4-6 use new **caldova-generated-turn** and **caldova-quality-turn** names so the earlier files are not overwritten. Generating replacements incurs additional charges; follow your instructor's directions. |
| The new **\*-turn** files or evaluation already exist | Do not use **--force** blindly. If generation already succeeded, resume at Step 5. If initialization already succeeded and matches Step 6, resume at Step 7; **init** adds entries rather than replacing them. |
| Fewer than 15 dataset rows, such as 13 | Stop before Step 6 and follow the Step 5 recovery instructions. A completed generation can return fewer than the requested maximum; do not overwrite existing artifacts or pad the dataset. |
| Missing **query**, or rows containing **simulation_configuration** | You generated conversation seeds. Stop; they are not turn-level input. Preserve them and ask your instructor before regenerating with the Step 4 settings and unused artifact names. Do not add dummy queries or remove the agent target. |
| **service name 'evals' doesn't exist** | Use the named **azd ai eval create** command in Step 7. The directory name is not the generated service name. |
| Evaluation declared but not deployed | Complete Step 7 successfully before starting the run. Do not use a full **azd up** to bypass the error. |
| Evaluator project version differs from the last deploy and the local definition does not match | Follow **Recover an evaluator version mismatch** in Step 7. Preserve the local rubric and lock file, download and review the published version, and reconcile it before reapplying intentional edits. |
| **My Resources > Evaluations** is empty or asks for Azure sign-in | Follow Step 10's UI recovery: check the Toolkit's lab account and existing project, refresh/reopen the view, and reload VS Code if needed. Review the existing run through the CLI if the UI remains unavailable; do not start a new run. |
| Monitoring timed out or you lost the run ID | Use the command below to list existing runs, copy the correct ID, and repeat Step 9. Do not start a replacement run just to monitor progress. |

```powershell
azd ai eval run list --path evals --eval caldova-generated-turn
```

## Optional: Correct a preview evaluator's input

Use this section only if a failed case appears to grade the Responses transport wrapper rather than the assistant's text.

**If all cases pass:** A result such as **15 passed, 0 failed, 0 errored, 0 skipped (100%)** is a valid outcome; a failed dimension is not required. Review one passing case and its explanation as described in Step 10, then skip this entire correction section. Leave the evaluator unchanged and do not generate or rerun cases just to produce a failure. Continue to **Part 7: Workshop summary and learning outcomes**, or optionally run the curated golden regression set below.

1. Compare **sample.output_text** with the evaluator's explanation. Missing fields, unsupported labels, wrong value types, or text outside the JSON object are genuine agent-output problems. If the explanation instead cites annotations, **sample.output**, **sample.output_items**, or a wrapper absent from the assistant text, continue below.
2. In **evals/azure.eval.yaml**, find the **caldova-quality-turn** evaluator and open the JSON file named by its **source**.
3. Only for a confirmed wrapper-based failure from item 1, find the failed dimension, usually JSON/schema compliance, and add this instruction to its **description**. If no such failed dimension exists, stop here and skip the remaining correction steps; no evaluator edit or new run is needed. Otherwise, preserve valid JSON and save the file:

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

If the new explanation still discusses transport wrappers, or marks valid and schema-compliant **sample.output_text** as not applicable, treat the schema score as a preview evaluator limitation. Report that criterion separately instead of changing the agent or relying on the aggregate pass rate.

## Optional: Run the curated golden regression set

Generated cases broaden coverage, but they do not replace human-reviewed expectations for regulated behavior. This repository also includes **src/agent/evals/caldova-golden.jsonl**, derived from the 15 labeled examples used earlier in the workshop.

Do this only after Steps 1-10, with your instructor's approval. It makes additional billable evaluation calls, but does not generate replacement cases.

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

   When prompted, confirm **turn** and choose **Add evaluation**. If the CLI already reported **eval added**, this step succeeded: do not run **init** again. Continue with the editor action below.

2. **Editor action: edit the YAML file, not the terminal.**

   - Click the VS Code editor, press **Ctrl+P**, enter **evals\azure.eval.yaml**, and press **Enter**.
   - Press **Ctrl+F**, search for **name: caldova-golden-baseline**, then press **Esc** to return to editing.
   - Within that evaluation, find its **evaluators** list and the **evaluator: caldova-quality-turn** entry. **Do not edit the separate, top-level evaluator catalog.**
   - Add or update **dataMapping** inside that evaluator entry, as shown in the full example below. **Align dataMapping with initializationParameters, not with target or evaluators.** Its three mapping lines go two spaces further to the right.
   - Keep existing properties such as **initializationParameters**. If **dataMapping** already exists, move or update it rather than adding a second copy.

   **Full golden evaluation example for evals/azure.eval.yaml. Do not paste into PowerShell:**

   Use this to update **only the caldova-golden-baseline entry under evals**. Keep the other evaluations and the top-level dataset/evaluator catalogs unchanged. Match the indentation of the other **- name:** entries in your file; preserve any additional existing properties.

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

   **Indentation check:** **initializationParameters** and **dataMapping** start in the same column. **target** stays further left, aligned with **evaluators**. If **dataMapping** is aligned with **target**, move **dataMapping** and its three mapping lines to the right. Keep the dataset name that **init** generated if it differs from **caldova-golden**.

   **Response mapping:** Use **response: "{{sample.output_text}}"** exactly as shown. **item** refers to fields in a dataset row; **sample.output_text** is the assistant text produced when the evaluation invokes the agent. The golden dataset has **query** and **expected_behavior**, not prewritten agent responses. Do not use **response: "{{item.response}}"** or add fabricated responses to the dataset.

   If registration reports that the evaluator requires **response** but the dataset does not provide it, correct this one mapping in the editor, save the file, and retry the registration command in item 4. Do not rerun **init** or generate another dataset.

   Press **Ctrl+S** to save. You should see these mappings inside the golden evaluation's evaluator entry, with no YAML syntax errors in the editor. If PowerShell says **evaluators:** or **dataMapping:** is not recognized, you pasted file content into the terminal; return to this editor step. You do not need to repeat **init**.

3. **Editor action: update the rubric.** The dataset supplies **query** and **expected_behavior**; **sample.output_text** supplies the agent's generated text to the evaluator's **response** input when the run executes.

   - In **evals/azure.eval.yaml**, find the **caldova-quality-turn** evaluator's catalog entry and open the JSON file named by its **source**, relative to that YAML file. Normally this is **evals\evaluators\caldova-quality-turn.json**, but version-conflict recovery may have selected a different file.
   - The file has a **dimensions** array. Each object in it is one scoring dimension, with its own **id**, **description**, and **weight**.
   - **Generated dimension IDs are not fixed.** Select dimensions by what their descriptions assess, using the table below. For sentiment, press **Ctrl+F**, search for **sentiment**, then press **Esc** and read the matching objects. Both **sentiment_accuracy** and **sentiment_label_accuracy** are possible IDs; neither is required. Find the **description** in the object that scores sentiment-label correctness; it may appear above the **id**.
   - Append the sentence below to the end of that description, **inside its existing double quotes**, with a space after the original text. Do not add a new property or paste the sentence outside the string.

   | Dimension to find | Search text | Confirm from its description |
   |-------------------|-------------|-----------------------------|
   | Sentiment classification | **sentiment** | Scores whether the positive, neutral, negative, or mixed label matches the consumer's tone. |
   | Regulated review routing | **review_category** or **routing** | Scores whether regulated signals receive the appropriate review category, independently of sentiment. |
   | Evidence-based summary | **summary**, then **evidence** if needed | Scores whether the summary is supported by the feedback and avoids invented facts or unsupported medical conclusions. |

   **If search shows no results:** Search the shorter terms above rather than an exact **id**, then inspect the descriptions in the **dimensions** array. Do not rename an ID to match this guide. If no dimension assesses one of these requirements, stop this optional exercise and ask your instructor to review the rubric; you can continue to **Part 7: Workshop summary and learning outcomes**. Do not edit an unrelated dimension or regenerate the dataset just to obtain matching IDs.

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

   **Edit the JSON file, not PowerShell.** These examples show one object from the **dimensions** array, not the whole file. Keep your original description and append the sentence; **When ground_truth is supplied, compare the response against those human-reviewed expectations as well as this dimension's requirements.**, do not replace the entire file or array. Leave **id**, **weight**, **always_applicable**, other dimensions, and file-level settings such as **pass_threshold** unchanged.

   Repeat the same description-only edit for the routing and summary dimensions identified using the table. IDs such as **review_category_routing** and **evidence_based_summary** are examples, not required names. If **evidence_based_summary** is absent, use the dimension whose description assesses summary accuracy and grounding, regardless of its ID.

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

6. Copy this run's ID. Repeat Steps 9-10, replacing **every** **--eval caldova-generated-turn** with **--eval caldova-golden-baseline** and setting **$runId** to this new ID.

**Expected result:** You can review a separate run against the fixed, human-reviewed cases. Keep generated cases for exploratory coverage and reuse the golden evaluation after prompt, model, or tool changes to detect regressions.

## CLI command reference

| Command | Purpose |
|---------|---------|
| `azd deploy caldova-consumer-sentiment-agent` | Redeploy code to the agent in the pre-provisioned project |
| `azd ai eval create <name> --path evals` | Register or update one evaluation and its referenced assets without redeploying the agent |
| `azd ai agent show` | Check agent status |
| `azd ai agent invoke "msg"` | Send a message to the agent |
| `azd ai agent monitor` | Stream container logs |
| `azd extension install azure.ai.evaluations` | Add evaluations commands, with instructor approval |
| `azd ai eval generate` | Generate a dataset and rubric from the evaluation brief |
| `azd ai eval init` | Configure an evaluation and its service entry |
| `azd ai eval run start` | Start a new evaluation run |
| `azd ai eval run list` / `azd ai eval run show` | Monitor existing runs without starting another |
| `azd ai eval run output list --failed-only` | List failed cases |
| `azd ai eval run output show <output-item>` | Inspect one case and its evaluator reasons |

## Stretch goal: add a topic or review category

Want to extend the agent before wrapping up? Add **COMPETITOR_MENTION** to the agent instructions in **src/agent/app.py**, decide how the routing layer should handle it, then redeploy:

```powershell
azd deploy caldova-consumer-sentiment-agent
```

Test the new value in the hosted-agent playground. This reinforces the direct edit → deploy → validate cycle.

## What you learned

- ✅ How hosted agents run your code as a managed service on Foundry
- ✅ How **ResponsesHostServer** exposes the current Responses protocol
- ✅ Why platform-managed history pairs with **store: False**
- ✅ How to test a hosted agent locally with the Agent Inspector (F5) before deploying
- ✅ How deployment is defined in **azure.yaml**, and how to update the pre-provisioned agent with **azd deploy** and validate in Foundry Toolkit
- ✅ How to invoke, monitor, and manage hosted agents
- ✅ How generated evaluations complement curated regression cases

## Key takeaway

> A Foundry hosted agent can be deployed directly from Python source. The repository defines behavior in **app.py** and hosting in **azure.yaml**. The administrator lifecycle handles the initial provisioning and deployment; managed-lab learners update the existing agent with **azd deploy** and validate it in VS Code with the Foundry Toolkit.

======

# Part 7: Workshop summary and learning outcomes

> **Duration:** ~10 minutes

## Objective

Review the complete journey from discovering a model in the Foundry Toolkit catalog to deploying a production-ready hosted agent for Caldova's B2C consumer sentiment analysis. This lab consolidates what you built, the skills you acquired, and where to go next.

## What you built

Across the labs, you -- as an AI developer on Caldova's commercial digital and customer engagement team -- constructed a **consumer sentiment analysis pipeline** end-to-end, from a blank terminal to a cloud-hosted agent accessible via REST API.

!IMAGE[Journey from model discovery to a cloud-hosted agent](instructions356855/mermaid_diagram3.png)

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
| **Key skill** | Environment configuration, **.env** validation, and readiness checks |
| **Outcome** | A confirmed Foundry project and a validated local **.env** configuration |

### Lab 3: Connect and send your first inference

| | |
|---|---|
| **What you did** | Reviewed Python code to authenticate with **DefaultAzureCredential** and send a Responses API request |
| **Key skill** | Using the Azure AI Projects SDK for model inference -- instructions, input, status, and token usage |
| **Outcome** | A working script (**src/01_first_inference.py**) that sends prompts and receives model responses |

**Core concept:** Responses API calls separate durable **instructions** from the current **input**, and return convenient output text plus status and usage metadata.

### Lab 4: Build a consumer sentiment analysis application for Caldova

| | |
|---|---|
| **What you did** | Designed a system prompt for structured JSON sentiment analysis, built a governed routing layer with confidence thresholds, processed batches of feedback |
| **Key skill** | Prompt engineering for structured output, building decision logic around model responses |
| **Outcome** | A complete sentiment analysis app (**src/02_sentiment_analysis.py**) that classifies Caldova feedback and independently flags regulated review categories |

**Core concept:** The model provides sentiment and category signals; your code makes the routing decisions -- and never determines causality, seriousness, or medical advice.

### Lab 5: Compare model outputs

| | |
|---|---|
| **What you did** | Ran the same Caldova feedback through gpt-5.4-mini and gpt-5.4, compared quality, latency, and cost |
| **Key skill** | Multi-model evaluation, cost-performance trade-off analysis, hybrid escalation patterns |
| **Outcome** | A comparison script (**src/03_model_comparison.py**) with side-by-side results and an optional hybrid routing mode |

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
- Deploying Python code to Foundry Agent Service with **azure.yaml** and **azd up**
- Invoking and monitoring agents via the **azd ai agent** CLI
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
4. **Validate before deployment.** Test with the Agent Inspector, then validate again in the hosted-agent playground after **azd deploy**.
5. **Keep regulated routing independent.** Sentiment and regulated review categories are separate signals -- never route on sentiment alone.
6. **Use complementary evaluation sets.** Generated suites discover cases; curated golden sets compare agent versions against fixed expectations.

## Next steps

- **Add more topics or review categories** -- for example, route competitor mentions to a competitive-intelligence queue.
- **Add tools to the agent** -- look up a consumer's case history or notify Caldova's pharmacovigilance team via a webhook when a POTENTIAL_ADVERSE_EVENT is detected.
- **Build a multi-agent workflow** -- chain the sentiment agent with a response-drafting agent.
- **Connect to a frontend** -- the hosted agent exposes an OpenAI-compatible REST API at **/responses**.
- **Set up CI/CD** -- use GitHub Actions with **azd** to redeploy on every push that changes **src/agent/**.
- **Add an evaluation quality gate** -- run the curated golden suite before promoting a new agent version.

## Thank you

You started with a model in a catalog and finished with a production-ready hosted agent on Microsoft Foundry. The patterns you learned -- prompt engineering, structured output, confidence-based routing, and direct-code deployment -- apply to any AI application, not just consumer sentiment analysis.

If you encountered any issues during this lab or would like to try it self-paced, see the repository page. Please log any issue experienced on the repo.

!IMAGE[Report Issues](instructions356855/issues.png)


Continue the discussion in the Microsoft Foundry Community 

!IMAGE[foundrydiscord.png](instructions356855/foundrydiscord.png)

Happy building!


## Continue learning

- [Microsoft Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [OpenAI Responses API](https://learn.microsoft.com/azure/foundry/openai/how-to/responses)
- [Microsoft Foundry hosted agents](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents)

If you encountered an issue, use the repository support guidance after the lab.

**Happy building!**