"""
Lab 5: Model Comparison for Caldova Consumer Sentiment
=======================================================
Compare sentiment, regulated-signal detection, confidence, and latency.

Usage:
    python 03_model_comparison.py
    python 03_model_comparison.py --hybrid
"""

import argparse
import importlib
import os
import sys
import time

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

sentiment_app = importlib.import_module("02_sentiment_analysis")
analyze_feedback = sentiment_app.analyze_feedback

TEST_FEEDBACK = [
    "The Caldova allergy relief tablets fit easily into my morning routine and the packaging is clear.",
    "The Caldova topical relief gel is convenient, but the cap is difficult to open.",
    "The product was fine. Nothing especially good or bad to report.",
    "My order arrived two days late and customer support never replied.",
    "I felt dizzy after taking the Caldova allergy relief tablets.",
    "The safety seal on the bottle was already broken when it arrived.",
    "Can I take this Caldova product with my prescription medicine?",
    "Availability improved, although the online stock information is unreliable.",
]


def compare_models(client, models: list[str], feedback: str) -> list[dict]:
    """Run identical feedback through each model and collect comparable fields."""
    results = []
    for model in models:
        start = time.time()
        result = analyze_feedback(client, model, feedback)
        results.append(
            {
                "model": model,
                "sentiment": result["sentiment"],
                "confidence": result["confidence"],
                "review_category": result["review_category"],
                "latency_ms": round((time.time() - start) * 1000),
            }
        )
    return results


def hybrid_analyze(
    client, primary: str, secondary: str, feedback: str, threshold: float = 0.8
) -> dict:
    """Use the secondary model only when the primary model has low confidence."""
    start = time.time()
    result = analyze_feedback(client, primary, feedback)
    latency_ms = round((time.time() - start) * 1000)
    model_used = primary
    escalated = False

    if result["confidence"] < threshold:
        start = time.time()
        result = analyze_feedback(client, secondary, feedback)
        latency_ms += round((time.time() - start) * 1000)
        model_used = secondary
        escalated = True

    return {
        "feedback": feedback,
        "model_used": model_used,
        "escalated": escalated,
        "sentiment": result["sentiment"],
        "confidence": result["confidence"],
        "review_category": result["review_category"],
        "latency_ms": latency_ms,
    }


def run_comparison(client, models: list[str]):
    """Print side-by-side results and agreement metrics."""
    print("=" * 78)
    print("  Model Comparison: Caldova Consumer Sentiment")
    print("=" * 78)

    all_results = []
    for feedback in TEST_FEEDBACK:
        print(f'\nFeedback: "{feedback}"\n')
        results = compare_models(client, models, feedback)
        all_results.append(results)
        print(
            f"  {'Model':<20s} {'Sentiment':<11s} {'Confidence':<12s} "
            f"{'Review category':<28s} {'Latency':<10s}"
        )
        print(f"  {'-'*18:<20s} {'-'*9:<11s} {'-'*10:<12s} {'-'*26:<28s} {'-'*8:<10s}")
        for result in results:
            print(
                f"  {result['model']:<20s} {result['sentiment']:<11s} "
                f"{result['confidence']:<12.2f} {result['review_category']:<28s} "
                f"{str(result['latency_ms'])+'ms':<10s}"
            )

    agreements = sum(
        1
        for results in all_results
        if len({(item["sentiment"], item["review_category"]) for item in results}) == 1
    )
    total = len(all_results)
    print("\n" + "=" * 78)
    print("  Comparison Summary")
    print("=" * 78)
    print(f"  Sentiment + routing agreement: {agreements}/{total} ({agreements/total*100:.0f}%)")
    for model in models:
        latencies = [
            item["latency_ms"]
            for results in all_results
            for item in results
            if item["model"] == model
        ]
        average = sum(latencies) / len(latencies) if latencies else 0
        print(f"  Avg latency - {model}: {average:.0f}ms")
    print()


def run_hybrid(client, primary: str, secondary: str):
    """Print results from confidence-based model escalation."""
    print("=" * 78)
    print("  Hybrid Sentiment Analysis")
    print(f"  Primary: {primary} | Secondary: {secondary}")
    print("  Model escalation threshold: confidence < 0.8")
    print("=" * 78)

    escalation_count = 0
    for feedback in TEST_FEEDBACK:
        result = hybrid_analyze(client, primary, secondary, feedback)
        marker = "\u2b06\ufe0f " if result["escalated"] else "  "
        print(f'\n{marker}"{feedback}"')
        print(
            f"   Model: {result['model_used']} | {result['sentiment']} "
            f"({result['confidence']:.2f}) | {result['review_category']} | "
            f"{result['latency_ms']}ms"
        )
        escalation_count += int(result["escalated"])

    print(f"\n  Escalated to secondary model: {escalation_count}/{len(TEST_FEEDBACK)}")
    print("  Regulated review categories still require human review.")
    print()


def main():
    endpoint = os.environ.get("PROJECT_ENDPOINT")
    model_1 = os.environ.get("MODEL_DEPLOYMENT_NAME")
    model_2 = os.environ.get("MODEL_DEPLOYMENT_NAME_2")

    if not endpoint or endpoint.startswith("https://<"):
        print("ERROR: Set PROJECT_ENDPOINT in your .env file.")
        sys.exit(1)
    if not model_1:
        print("ERROR: Set MODEL_DEPLOYMENT_NAME in your .env file.")
        sys.exit(1)
    if not model_2:
        print(
            "NOTE: MODEL_DEPLOYMENT_NAME_2 not set. "
            "Using only MODEL_DEPLOYMENT_NAME for comparison.\n"
        )
        model_2 = model_1

    parser = argparse.ArgumentParser(description="Caldova Model Comparison")
    parser.add_argument("--hybrid", action="store_true", help="Hybrid model mode")
    args = parser.parse_args()

    project_client = AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )
    inference_client = project_client.get_openai_client()
    models = [model_1, model_2] if model_1 != model_2 else [model_1]

    if args.hybrid and len(models) == 2:
        run_hybrid(inference_client, models[0], models[1])
    else:
        if args.hybrid:
            print("WARN: Hybrid mode requires two models. Running comparison instead.\n")
        run_comparison(inference_client, models)


if __name__ == "__main__":
    main()
