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
import json
import os
import re
import sys
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

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
    "The Caldova product was not unlike the one I usually buy, I suppose.",    "The Caldova tablets were... something. I honestly cannot decide how I feel about them.",]


RETAIL_PRICES_URL = "https://prices.azure.com/api/retail/prices"
RETAIL_PRICES_API_VERSION = "2023-01-01-preview"
AZURE_OPENAI_PRICING_URL = (
    "https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/"
)
PUBLISHED_GLOBAL_RATES_USD_PER_1M = {
    "gpt-5.4-mini": {"input": 0.75, "output": 4.50},
    "gpt-5.4": {"input": 2.50, "output": 15.00},
}
INPUT_METER_WORDS = {"input", "inp", "inpt"}
OUTPUT_METER_WORDS = {"output", "out", "outp", "opt"}
EXCLUDED_METER_WORDS = {
    "audio",
    "batch",
    "cached",
    "cchd",
    "codex",
    "dev",
    "fine",
    "ft",
    "grader",
    "grdr",
    "hosting",
    "realtime",
    "training",
}
VALID_MODEL_SUFFIX_WORDS = INPUT_METER_WORDS | OUTPUT_METER_WORDS | {
    "data",
    "dzone",
    "global",
    "glbl",
    "regional",
    "regnl",
}


def _escape_odata(value: str) -> str:
    return value.replace("'", "''")


def _model_aliases(model: str) -> list[str]:
    aliases = {
        model,
        model.upper(),
        model.replace("-", " "),
        model.upper().replace("-", " "),
        re.sub(r"[- ]", "", model).upper(),
    }
    return sorted(aliases)


def fetch_retail_meters(model: str, region: str, currency: str = "USD") -> list[dict]:
    """Fetch model meters from the unauthenticated Azure Retail Prices API."""
    region_value = _escape_odata(region)
    model_filter = " or ".join(
        f"contains(meterName, '{_escape_odata(alias)}')"
        for alias in _model_aliases(model)
    )
    filter_expression = (
        "serviceName eq 'Foundry Models' and "
        f"armRegionName eq '{region_value}' and "
        "priceType eq 'Consumption' and "
        f"({model_filter})"
    )
    query = urlencode(
        {
            "api-version": RETAIL_PRICES_API_VERSION,
            "currencyCode": f"'{currency.upper()}'",
            "$filter": filter_expression,
        }
    )
    next_page = f"{RETAIL_PRICES_URL}?{query}"
    meters = []

    while next_page:
        request = Request(next_page, headers={"User-Agent": "ILL335-model-comparison/1.0"})
        with urlopen(request, timeout=10) as response:
            payload = json.load(response)
        meters.extend(payload.get("Items", []))
        next_page = payload.get("NextPageLink")

    return meters


def _meter_words(meter: dict) -> set[str]:
    text = " ".join(
        str(meter.get(field, ""))
        for field in ("meterName", "skuName", "armSkuName")
    ).lower()
    return set(re.findall(r"[a-z0-9]+", text))


def _matches_exact_model(meter: dict, model: str) -> bool:
    """Reject similarly named variants, such as mini meters for the base model."""
    model_name = re.sub(r"[^a-z0-9]", "", model.lower())
    for field in ("meterName", "skuName", "armSkuName"):
        name = re.sub(r"[^a-z0-9]", "", str(meter.get(field, "")).lower())
        start = name.find(model_name)
        if start == -1:
            continue
        suffix = name[start + len(model_name) :]
        if not suffix:
            return True
        suffix = suffix.lstrip("0123456789")
        if any(suffix.startswith(word) for word in VALID_MODEL_SUFFIX_WORDS):
            return True
    return False


def _tokens_per_unit(unit_of_measure: str) -> int | None:
    match = re.fullmatch(r"(\d+(?:\.\d+)?)\s*([KM]?)", unit_of_measure.upper().strip())
    if not match:
        return None
    multiplier = {"": 1, "K": 1_000, "M": 1_000_000}[match.group(2)]
    return round(float(match.group(1)) * multiplier)


def _select_meter(meters: list[dict], model: str, meter_type: str) -> dict | None:
    required_words = INPUT_METER_WORDS if meter_type == "input" else OUTPUT_METER_WORDS
    candidates = []
    for meter in meters:
        words = _meter_words(meter)
        if (
            not _matches_exact_model(meter, model)
            or words & EXCLUDED_METER_WORDS
            or not words & required_words
            or _tokens_per_unit(str(meter.get("unitOfMeasure", ""))) is None
        ):
            continue
        score = 2 if words & {"global", "glbl"} else 1
        candidates.append((score, str(meter.get("effectiveStartDate", "")), meter))

    return max(candidates, default=(0, "", None), key=lambda item: (item[0], item[1]))[2]


def get_model_pricing(model: str, region: str, currency: str = "USD") -> dict | None:
    """Return standard input and output retail meters for a model when available."""
    meters = fetch_retail_meters(model, region, currency)
    pricing = {}
    for meter_type in ("input", "output"):
        meter = _select_meter(meters, model, meter_type)
        if not meter:
            return None
        pricing[meter_type] = {
            "meter_name": meter["meterName"],
            "retail_price": float(meter["retailPrice"]),
            "unit_of_measure": meter["unitOfMeasure"],
            "tokens_per_unit": _tokens_per_unit(meter["unitOfMeasure"]),
        }
    return pricing


def get_published_global_pricing(model: str, currency: str = "USD") -> dict | None:
    """Return published Global Standard rates when API meters are not yet available."""
    if currency.upper() != "USD":
        return None
    rates = PUBLISHED_GLOBAL_RATES_USD_PER_1M.get(model.lower())
    if not rates:
        return None
    return {
        meter_type: {
            "meter_name": f"{model} {meter_type} Global Standard",
            "retail_price": price,
            "unit_of_measure": "1M tokens",
            "tokens_per_unit": 1_000_000,
        }
        for meter_type, price in rates.items()
    } | {
        "source": "Azure OpenAI pricing page",
        "source_url": AZURE_OPENAI_PRICING_URL,
        "verified_date": "2026-09-11",
    }


def calculate_cost(usage: dict, pricing: dict | None) -> float | None:
    """Calculate one response's retail cost from actual token usage."""
    if not usage or not pricing:
        return None
    input_meter = pricing["input"]
    output_meter = pricing["output"]
    return (
        usage.get("input_tokens", 0)
        / input_meter["tokens_per_unit"]
        * input_meter["retail_price"]
        + usage.get("output_tokens", 0)
        / output_meter["tokens_per_unit"]
        * output_meter["retail_price"]
    )


def calculate_savings(model_costs: dict[str, float]) -> dict | None:
    """Compare observed run costs and return savings against the costliest model."""
    if len(model_costs) < 2:
        return None
    ranked_costs = sorted(model_costs.items(), key=lambda item: item[1])
    cheaper_model, cheaper_cost = ranked_costs[0]
    expensive_model, expensive_cost = ranked_costs[-1]
    difference = expensive_cost - cheaper_cost
    return {
        "cheaper_model": cheaper_model,
        "expensive_model": expensive_model,
        "difference": difference,
        "percent": difference / expensive_cost * 100 if expensive_cost else 0,
    }


def load_model_pricing(
    models: list[str], region: str, currency: str = "USD"
) -> tuple[dict, dict]:
    """Load available prices without allowing pricing failures to block the lab."""
    pricing_by_model = {}
    errors = {}
    for model in models:
        try:
            pricing = get_model_pricing(model, region, currency)
            if pricing:
                pricing["source"] = "Azure Retail Prices API"
                pricing_by_model[model] = pricing
            else:
                pricing = get_published_global_pricing(model, currency)
                if pricing:
                    pricing_by_model[model] = pricing
                else:
                    errors[model] = "no matching standard input/output token meters"
        except (OSError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            pricing = get_published_global_pricing(model, currency)
            if pricing:
                pricing_by_model[model] = pricing
            else:
                errors[model] = str(exc)
    return pricing_by_model, errors


def compare_models(
    client, models: list[str], feedback: str, pricing_by_model: dict | None = None
) -> list[dict]:
    """Run identical feedback through each model and collect comparable fields."""
    results = []
    pricing_by_model = pricing_by_model or {}
    for model in models:
        start = time.time()
        result = analyze_feedback(client, model, feedback)
        usage = result.get("_usage", {})
        results.append(
            {
                "model": model,
                "sentiment": result["sentiment"],
                "confidence": result["confidence"],
                "review_category": result["review_category"],
                "latency_ms": round((time.time() - start) * 1000),
                "usage": usage,
                "estimated_cost": calculate_cost(usage, pricing_by_model.get(model)),
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


def run_comparison(client, models: list[str], region: str, currency: str = "USD"):
    """Print side-by-side results and agreement metrics."""
    pricing_by_model, pricing_errors = load_model_pricing(models, region, currency)
    print("=" * 78)
    print("  Model Comparison: Caldova Consumer Sentiment")
    print("=" * 78)

    all_results = []
    for feedback in TEST_FEEDBACK:
        print(f'\nFeedback: "{feedback}"\n')
        results = compare_models(client, models, feedback, pricing_by_model)
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

    print(f"\n  Pricing estimate: {currency.upper()} (Azure published retail rates)")
    model_costs = {}
    for model in models:
        model_results = [
            item
            for results in all_results
            for item in results
            if item["model"] == model
        ]
        input_tokens = sum(item["usage"].get("input_tokens", 0) for item in model_results)
        output_tokens = sum(item["usage"].get("output_tokens", 0) for item in model_results)
        pricing = pricing_by_model.get(model)
        if not pricing:
            reason = pricing_errors.get(model, "pricing unavailable")
            print(f"  {model}: pricing unavailable ({reason})")
            continue

        cost = sum(item["estimated_cost"] or 0 for item in model_results)
        model_costs[model] = cost
        source = pricing.get("source", "Azure Retail Prices API")
        if pricing.get("verified_date"):
            source += f", verified {pricing['verified_date']}"
        print(f"  {model} pricing source: {source}")
        print(
            f"  {model} rates: input ${pricing['input']['retail_price']:.6f}/"
            f"{pricing['input']['unit_of_measure']}, output "
            f"${pricing['output']['retail_price']:.6f}/"
            f"{pricing['output']['unit_of_measure']}"
        )
        print(
            f"  {model} estimated retail cost: ${cost:.6f} "
            f"({input_tokens:,} input + {output_tokens:,} output tokens)"
        )

    savings = calculate_savings(model_costs)
    if savings:
        print(
            f"  Cost saving: {savings['cheaper_model']} saved {savings['percent']:.1f}% "
            f"(${savings['difference']:.6f}) vs {savings['expensive_model']} for this run"
        )
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
    pricing_region = os.environ.get("AZURE_LOCATION", "northcentralus")
    pricing_currency = os.environ.get("AZURE_PRICING_CURRENCY", "USD")

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
        run_comparison(inference_client, models, pricing_region, pricing_currency)


if __name__ == "__main__":
    main()
