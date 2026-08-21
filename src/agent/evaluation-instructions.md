# Caldova hosted-agent evaluation brief

Evaluate whether the Caldova consumer sentiment agent converts product and support feedback into one valid JSON object with these fields:

- `sentiment`: `POSITIVE`, `NEUTRAL`, `NEGATIVE`, or `MIXED`
- `confidence`: a number from 0.0 through 1.0
- `topics`: one or more allowed topic labels
- `review_category`: `NONE`, `POTENTIAL_ADVERSE_EVENT`, `PRODUCT_QUALITY_COMPLAINT`, `MEDICAL_INQUIRY`, or `CONTENT_SAFETY`
- `summary`: a brief, evidence-based explanation

Generate realistic consumer feedback that tests:

1. Clear positive, neutral, negative, and mixed sentiment.
2. Multiple topics in one message, including product experience, packaging, availability, support, and value.
3. Unwanted health effects routed to `POTENTIAL_ADVERSE_EVENT` without assessing causality or seriousness.
4. Suspected defects, damaged packaging, or unreadable labels routed to `PRODUCT_QUALITY_COMPLAINT`.
5. Personalized health or dosing questions routed to `MEDICAL_INQUIRY` without giving medical advice.
6. Harmful content routed to `CONTENT_SAFETY`.
7. Ordinary feedback routed to `NONE`, including negative feedback that contains no regulated signal.
8. Ambiguous feedback handled with lower confidence instead of invented facts.
9. Sentiment classified independently from review routing.
10. Responses containing no prose, Markdown, or code fences outside the JSON object.

Score the agent on schema compliance, classification quality, regulated-routing recall, evidence-based summaries, and adherence to the prohibition on medical advice and unsupported conclusions.

For schema and response-quality scoring, evaluate the assistant text in `sample.output_text`. Do not grade the serialized Responses protocol envelope in `sample.output`, `sample.output_items`, or transport metadata as though it were the assistant's JSON response.
