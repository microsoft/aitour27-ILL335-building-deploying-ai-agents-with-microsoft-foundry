# Testing Instructions

Verify your lab work at each phase by running these checks.

---

## Phase 3: First Inference

```bash
python src/01_first_inference.py
```

**Pass criteria:**

- [ ] Script runs without errors
- [ ] Model response is printed to terminal
- [ ] Token usage is displayed
- [ ] Response is relevant to "What is Microsoft Foundry"

**Common issues:**

| Error | Fix |
|-------|-----|
| `PROJECT_ENDPOINT not set` | Edit `.env`  - set your project endpoint from Lab 2 |
| `401 Unauthorized` | Run `az login` and retry |
| `404 Not Found` | Verify `MODEL_DEPLOYMENT_NAME` matches an active deployment |
| `429 Rate Limited` | Wait 30 seconds and retry |

---

## Phase 4: Sentiment Analysis

### Test 1: Sample Feedback

```bash
python src/02_sentiment_analysis.py
```

**Pass criteria:**

- [ ] All 5 sample feedback items are analyzed
- [ ] Each result shows sentiment, confidence, topics, review_category, summary, and action
- [ ] Summary counts are printed
- [ ] Feedback mentioning dizziness after taking Caldova allergy relief tablets is flagged with review_category POTENTIAL_ADVERSE_EVENT
- [ ] Positive feedback (e.g., "The Caldova allergy relief tablets fit easily into my morning routine...") is classified as POSITIVE

### Test 2: File Input

```bash
python src/02_sentiment_analysis.py --file src/sample_feedback.json
```

**Pass criteria:**

- [ ] All 15 feedback items from the JSON file are processed
- [ ] No JSON parsing errors in the output
- [ ] Summary is printed at the end

### Test 3: Interactive Mode

```bash
python src/02_sentiment_analysis.py --interactive
```

**Pass criteria:**

- [ ] Prompt appears: `Enter feedback:`
- [ ] Typing a piece of feedback returns a sentiment analysis result
- [ ] Typing `quit` exits cleanly

### Test 4: Sentiment and Routing Accuracy

Review the output from Test 2 and compare against the `expected_sentiment` and `expected_review_category` labels in `sample_feedback.json`. The model should correctly classify most feedback:

| Expected Accuracy | Status |
|-------------------|--------|
| > 80% agreement | Good |
| 60-80% agreement | Acceptable  - try adjusting the system prompt |
| < 60% | Review your system prompt or try a different model |

---

## Phase 5: Model Comparison (Optional)

### Test 5: Side-by-Side Comparison

```bash
python src/03_model_comparison.py
```

**Pass criteria:**

- [ ] Each feedback item shows results from both models (or one if only one deployed)
- [ ] Latency is measured for each model
- [ ] Agreement rate is displayed in the summary

### Test 6: Hybrid Mode

```bash
python src/03_model_comparison.py --hybrid
```

**Pass criteria:**

- [ ] Low-confidence results are escalated to the secondary model
- [ ] Escalation count is displayed at the end
- [ ] Escalated feedback items show the secondary model name

---

## Quick Validation Script

Run all tests in sequence:

```bash
echo "=== Phase 3: First Inference ===" && \
python src/01_first_inference.py && \
echo "" && \
echo "=== Phase 4: Sentiment Analysis (samples) ===" && \
python src/02_sentiment_analysis.py && \
echo "" && \
echo "=== Phase 4: Sentiment Analysis (file) ===" && \
python src/02_sentiment_analysis.py --file src/sample_feedback.json && \
echo "" && \
echo "=== All tests passed ==="
```

---

## Phase 6: Deploy Agent

### Test 7: Run the Hosted Agent Locally

```bash
python src/agent/app.py
```

**Pass criteria:**

- [ ] The server starts on port 8088
- [ ] The startup output names `caldova-consumer-sentiment-agent`
- [ ] The Agent Inspector can connect to the local server

### Test 8: Invoke Agent

```bash
azd ai agent invoke --local "The product was convenient, but I felt dizzy after using it."
```

**Pass criteria:**

- [ ] Test feedback items are sent to the deployed agent
- [ ] Each response contains sentiment, confidence, topics, review_category, and summary fields
- [ ] Feedback mentioning a symptom is flagged with review_category POTENTIAL_ADVERSE_EVENT
- [ ] Positive feedback is classified with sentiment POSITIVE

### Test 9: Deploy and Invoke the Hosted Agent

```bash
azd deploy
azd ai agent invoke "The safety seal was broken when the bottle arrived."
```

**Pass criteria:**

- [ ] `caldova-consumer-sentiment-agent` deploys successfully
- [ ] The response includes `PRODUCT_QUALITY_COMPLAINT`
- [ ] The feedback is routed for human review

---

## Troubleshooting

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| `ModuleNotFoundError` | Dependencies not installed | `pip install -r requirements.txt` |
| `EnvironmentError` | Missing `.env` values | Copy `.env.sample` to `.env` and fill in values |
| JSON parse errors in sentiment analysis | Model returning free text | Check that `SYSTEM_PROMPT` includes "Respond ONLY with valid JSON" |
| All feedback classified the same | Instructions are too broad or examples are unbalanced | Review `SYSTEM_PROMPT` and test with a varied dataset |
| `HttpResponseError 429` | Rate limiting | Wait 30-60 seconds, reduce request frequency |
| Connection timeout | Network or endpoint issue | Verify endpoint URL, check `az account show` |
