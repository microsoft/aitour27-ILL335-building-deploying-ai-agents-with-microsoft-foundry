"""
Lab 4: Caldova Consumer Product Sentiment Analysis
===================================================
Analyze B2C feedback about Caldova products and route regulated signals for
human review using Microsoft Foundry-hosted models.

Usage:
    python 02_sentiment_analysis.py
    python 02_sentiment_analysis.py --interactive
    python 02_sentiment_analysis.py --file sample_feedback.json
"""

import argparse
import json
import os
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from azure.ai.projects import AIProjectClient
from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

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

SAMPLE_FEEDBACK = [
    "The Caldova allergy relief tablets fit easily into my morning routine and the packaging is clear.",
    "The Caldova topical relief gel is convenient, but the cap is difficult to open.",
    "My order arrived two days late and customer support kept me updated.",
    "I felt dizzy after taking the Caldova allergy relief tablets.",
    "The safety seal on the bottle was already broken when it arrived.",
]


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


def route_feedback(result: dict) -> str:
    """Route insights to analytics or an appropriate human review queue."""
    review_category = result.get("review_category", "CONTENT_SAFETY")
    confidence = result.get("confidence", 0.0)

    if review_category != "NONE":
        return "ESCALATE_FOR_REVIEW"
    if confidence < 0.8:
        return "REVIEW_LOW_CONFIDENCE"
    return "ADD_TO_SENTIMENT_DASHBOARD"


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


ACTION_ICONS = {
    "ADD_TO_SENTIMENT_DASHBOARD": "\U0001f4ca",
    "REVIEW_LOW_CONFIDENCE": "\U0001f50d",
    "ESCALATE_FOR_REVIEW": "\u26a0\ufe0f",
}


def print_result(result: dict, index: int | None = None, total: int | None = None):
    """Print a consumer feedback insight."""
    header = f"--- Feedback {index}/{total} ---" if index else "---"
    icon = ACTION_ICONS.get(result["action"], "")
    print(header)
    print(f'Feedback: "{result["feedback"]}"')
    print(f"Sentiment: {result['sentiment']} (confidence: {result['confidence']:.2f})")
    print(f"Topics: {', '.join(result['topics'])}")
    print(f"Review category: {result['review_category']}")
    print(f"Summary: {result['summary']}")
    print(f"Action: {icon} {result['action']}")
    print()


def print_summary(results: list[dict]):
    """Print sentiment distribution and routing totals."""
    print("=" * 48)
    print("  Engagement Insight Summary")
    print("=" * 48)
    print(f"Total feedback: {len(results)}")
    for sentiment in ("POSITIVE", "NEUTRAL", "NEGATIVE", "MIXED"):
        count = sum(r["sentiment"] == sentiment for r in results)
        print(f"  {sentiment + ':':12s} {count}")
    escalated = sum(r["action"] == "ESCALATE_FOR_REVIEW" for r in results)
    print(f"  {'ESCALATED:':12s} {escalated}")
    print()


def run_samples(client, model: str):
    """Process the built-in Caldova feedback."""
    print(f"\nProcessing {len(SAMPLE_FEEDBACK)} sample feedback items...\n")
    results = []
    for index, feedback in enumerate(SAMPLE_FEEDBACK, 1):
        result = process_feedback(client, model, feedback)
        print_result(result, index=index, total=len(SAMPLE_FEEDBACK))
        results.append(result)
    print_summary(results)


def run_file(client, model: str, filepath: str):
    """Process feedback from a JSON file."""
    with open(filepath, "r", encoding="utf-8") as file:
        items = json.load(file)

    print(f"\nProcessing {len(items)} feedback items from {filepath}...\n")
    results = []
    for index, item in enumerate(items, 1):
        feedback = item if isinstance(item, str) else item.get("feedback", "")
        result = process_feedback(client, model, feedback)
        print_result(result, index=index, total=len(items))
        results.append(result)
    print_summary(results)


def run_interactive(client, model: str):
    """Analyze consumer feedback entered interactively."""
    print("\nInteractive mode. Enter consumer feedback or type 'quit'.\n")
    while True:
        try:
            feedback = input("Enter feedback: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if feedback.lower() in ("quit", "exit", "q"):
            break
        if not feedback:
            continue
        print_result(process_feedback(client, model, feedback))


def main():
    endpoint = os.environ.get("PROJECT_ENDPOINT")
    model = os.environ.get("MODEL_DEPLOYMENT_NAME")

    if not endpoint or endpoint.startswith("https://<"):
        print("ERROR: Set PROJECT_ENDPOINT in your .env file (see Lab 2).")
        sys.exit(1)
    if not model:
        print("ERROR: Set MODEL_DEPLOYMENT_NAME in your .env file.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Caldova Sentiment Analysis")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--file", type=str, help="Path to a JSON feedback file")
    args = parser.parse_args()

    project_client = AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )
    inference_client = project_client.get_openai_client()

    print("=" * 48)
    print("  Caldova Consumer Sentiment Analysis")
    print(f"  Model: {model}")
    print("=" * 48)

    try:
        if args.interactive:
            run_interactive(inference_client, model)
        elif args.file:
            run_file(inference_client, model, args.file)
        else:
            run_samples(inference_client, model)
    except HttpResponseError as exc:
        if exc.status_code == 429:
            print("ERROR: Rate limited. Wait a moment and try again.")
        elif exc.status_code == 401:
            print("ERROR: Authentication failed. Run 'az login' and try again.")
        else:
            print(f"ERROR: {exc.message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
