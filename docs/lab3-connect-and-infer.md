# Lab 3: Connect and send your first inference

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

---

**Next:** [Lab 4 - Build Caldova's consumer sentiment analysis application](./lab4-sentiment-analysis.md)

