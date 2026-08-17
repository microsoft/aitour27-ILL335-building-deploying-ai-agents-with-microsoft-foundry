---
name: ill335-responses-api
description: Supports ILL335 model inference and sentiment-analysis labs that use the OpenAI Responses API with Microsoft Foundry. Use for Labs 3-5, responses.create, output_text, previous_response_id, structured JSON, model comparison, or Responses API errors.
license: MIT
---

# Support the ILL335 Responses API Labs

Use the repository's current Responses API implementation as the source of truth. Do not reintroduce Chat Completions examples.

## Read the Relevant Sources

Start with:

- `src/01_first_inference.py` and `docs/lab3-connect-and-infer.md`
- `src/02_sentiment_analysis.py` and `docs/lab4-sentiment-analysis.md`
- `src/03_model_comparison.py` and `docs/lab5-model-comparison.md`
- `requirements.txt`

## Use the Current Request Pattern

```python
response = inference_client.responses.create(
    model=model,
    instructions="Describe the model's role and boundaries.",
    input="Provide the learner's current request.",
)

print(response.output_text)
```

Use these response fields:

- `response.output_text` for generated text
- `response.status` for completion state
- `response.usage.input_tokens`
- `response.usage.output_tokens`
- `response.usage.total_tokens`

Use `previous_response_id=response.id` for a follow-up turn. Do not rebuild a Chat Completions message array.

## Protect the Governed Scenario

For sentiment analysis:

- Keep sentiment classification independent from regulated review routing.
- Escalate potential adverse events, product quality complaints, medical inquiries, and content-safety signals for human review.
- Never determine medical causality, seriousness, diagnosis, or treatment.
- Treat malformed model JSON conservatively and preserve the repository's fallback behavior.

## Validate in a Virtual Environment

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest src\tests\test_sentiment.py -q
python src\tests\validate_lab.py
```

On Linux or macOS, activate with `source .venv/bin/activate`.

Run live tests only when the learner has configured `.env` and explicitly wants to make Azure requests:

```powershell
python src\tests\validate_lab.py --live
```

## Success Criteria

- No deprecated Chat Completions calls are introduced.
- Unit tests pass.
- The offline lab validator reports no failures.
- Live output, when requested, includes text, status, and token usage.
