import sys
from importlib import import_module
from types import SimpleNamespace

sys.path.insert(0, "src")

mod = import_module("02_sentiment_analysis")
route_feedback = mod.route_feedback
analyze_feedback = mod.analyze_feedback


class FakeResponses:
    def __init__(self, output_text: str, usage=None):
        self.output_text = output_text
        self.usage = usage
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(output_text=self.output_text, usage=self.usage)


class FakeClient:
    def __init__(self, output_text: str, usage=None):
        self.responses = FakeResponses(output_text, usage)


def test_analyze_feedback_uses_responses_api():
    client = FakeClient(
        '{"sentiment":"POSITIVE","confidence":0.9,"topics":["VALUE"],'
        '"review_category":"NONE","summary":"Good value."}'
    )

    result = analyze_feedback(client, "gpt-5.4-mini", "Good value.")

    assert result["sentiment"] == "POSITIVE"
    assert client.responses.kwargs == {
        "model": "gpt-5.4-mini",
        "instructions": mod.SYSTEM_PROMPT,
        "input": "Good value.",
    }


def test_analyze_feedback_handles_non_json_response():
    result = analyze_feedback(FakeClient("not json"), "gpt-5.4-mini", "Feedback")

    assert result["review_category"] == "CONTENT_SAFETY"
    assert result["confidence"] == 0.0


def test_analyze_feedback_preserves_token_usage():
    client = FakeClient(
        '{"sentiment":"POSITIVE","confidence":0.9,"topics":["VALUE"],'
        '"review_category":"NONE","summary":"Good value."}',
        SimpleNamespace(input_tokens=120, output_tokens=30, total_tokens=150),
    )

    result = analyze_feedback(client, "gpt-5.4-mini", "Good value.")

    assert result["_usage"] == {
        "input_tokens": 120,
        "output_tokens": 30,
        "total_tokens": 150,
    }


class TestRouteFeedback:
    """Unit tests for the governed routing layer."""

    def test_high_confidence_sentiment_added_to_dashboard(self):
        result = {"review_category": "NONE", "confidence": 0.95}
        assert route_feedback(result) == "ADD_TO_SENTIMENT_DASHBOARD"

    def test_low_confidence_sentiment_reviewed(self):
        result = {"review_category": "NONE", "confidence": 0.79}
        assert route_feedback(result) == "REVIEW_LOW_CONFIDENCE"

    def test_threshold_sentiment_added_to_dashboard(self):
        result = {"review_category": "NONE", "confidence": 0.8}
        assert route_feedback(result) == "ADD_TO_SENTIMENT_DASHBOARD"

    def test_adverse_event_escalated(self):
        result = {"review_category": "POTENTIAL_ADVERSE_EVENT", "confidence": 0.99}
        assert route_feedback(result) == "ESCALATE_FOR_REVIEW"

    def test_product_quality_complaint_escalated(self):
        result = {"review_category": "PRODUCT_QUALITY_COMPLAINT", "confidence": 0.9}
        assert route_feedback(result) == "ESCALATE_FOR_REVIEW"

    def test_medical_inquiry_escalated(self):
        result = {"review_category": "MEDICAL_INQUIRY", "confidence": 0.85}
        assert route_feedback(result) == "ESCALATE_FOR_REVIEW"

    def test_content_safety_escalated(self):
        result = {"review_category": "CONTENT_SAFETY", "confidence": 1.0}
        assert route_feedback(result) == "ESCALATE_FOR_REVIEW"

    def test_missing_review_category_escalated(self):
        assert route_feedback({"confidence": 0.9}) == "ESCALATE_FOR_REVIEW"

    def test_missing_confidence_reviewed(self):
        assert route_feedback({"review_category": "NONE"}) == "REVIEW_LOW_CONFIDENCE"
