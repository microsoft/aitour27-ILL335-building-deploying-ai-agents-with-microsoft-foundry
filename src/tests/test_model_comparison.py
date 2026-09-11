import sys
from importlib import import_module

import pytest

sys.path.insert(0, "src")

mod = import_module("03_model_comparison")


def retail_meter(name: str, price: float) -> dict:
    return {
        "meterName": name,
        "skuName": name,
        "armSkuName": name,
        "retailPrice": price,
        "unitOfMeasure": "1K",
        "effectiveStartDate": "2026-06-01T00:00:00Z",
    }


def test_select_meter_uses_standard_global_rates():
    meters = [
        retail_meter("gpt-5.4-mini-ft input global Tokens", 0.0008),
        retail_meter("gpt-5.4-mini input regional Tokens", 0.0005),
        retail_meter("GPT 5.4 Mini input global Tokens", 0.0004),
    ]

    selected = mod._select_meter(meters, "gpt-5.4-mini", "input")

    assert selected["meterName"] == "GPT 5.4 Mini input global Tokens"


def test_select_meter_accepts_versioned_output_abbreviation():
    meters = [retail_meter("gpt-5.4-mini-20260317-Outp-glbl Tokens", 0.0006)]

    selected = mod._select_meter(meters, "gpt-5.4-mini", "output")

    assert selected["meterName"] == "gpt-5.4-mini-20260317-Outp-glbl Tokens"


def test_select_meter_does_not_mix_model_variants():
    meters = [retail_meter("gpt-5.4-mini input global Tokens", 0.0004)]

    assert mod._select_meter(meters, "gpt-5.4", "input") is None


def test_calculate_cost_uses_api_billing_units():
    pricing = {
        "input": {"retail_price": 0.0004, "tokens_per_unit": 1_000},
        "output": {"retail_price": 0.0016, "tokens_per_unit": 1_000},
    }

    cost = mod.calculate_cost({"input_tokens": 2_000, "output_tokens": 500}, pricing)

    assert cost == pytest.approx(0.0016)


def test_published_global_pricing_uses_current_usd_rates():
    pricing = mod.get_published_global_pricing("gpt-5.4-mini")

    assert pricing["input"]["retail_price"] == 0.75
    assert pricing["output"]["retail_price"] == 4.50
    assert pricing["input"]["tokens_per_unit"] == 1_000_000
    assert pricing["source"] == "Azure OpenAI pricing page"


def test_load_model_pricing_falls_back_when_api_meter_is_missing(monkeypatch):
    monkeypatch.setattr(mod, "get_model_pricing", lambda *args: None)

    pricing_by_model, errors = mod.load_model_pricing(
        ["gpt-5.4-mini", "gpt-5.4"], "eastus2"
    )

    assert set(pricing_by_model) == {"gpt-5.4-mini", "gpt-5.4"}
    assert errors == {}


def test_calculate_savings_uses_observed_run_costs():
    savings = mod.calculate_savings({"gpt-5.4-mini": 0.01, "gpt-5.4": 0.04})

    assert savings == {
        "cheaper_model": "gpt-5.4-mini",
        "expensive_model": "gpt-5.4",
        "difference": pytest.approx(0.03),
        "percent": pytest.approx(75.0),
    }