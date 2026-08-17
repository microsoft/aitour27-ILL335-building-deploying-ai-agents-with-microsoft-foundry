"""
Lab 6: Caldova Consumer Sentiment Agent
========================================
Hosted engagement agent for sentiment analysis and governed signal routing.
"""

import os
import sys

print("Starting caldova-consumer-sentiment-agent...", flush=True)

try:
    from dotenv import load_dotenv

    load_dotenv(override=False)
except ImportError:
    pass

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential

PROJECT_ENDPOINT = os.getenv("FOUNDRY_PROJECT_ENDPOINT") or os.getenv(
    "AZURE_AI_PROJECT_ENDPOINT"
)
MODEL_DEPLOYMENT_NAME = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME") or os.getenv(
    "MODEL_DEPLOYMENT_NAME", "gpt-5.4-mini"
)

if not PROJECT_ENDPOINT:
    print(
        "ERROR: FOUNDRY_PROJECT_ENDPOINT or AZURE_AI_PROJECT_ENDPOINT not set",
        flush=True,
    )
    sys.exit(1)

print(f"  Endpoint: {PROJECT_ENDPOINT}", flush=True)
print(f"  Model:    {MODEL_DEPLOYMENT_NAME}", flush=True)

SYSTEM_PROMPT = """You are a consumer engagement insight analyst for Caldova, Microsoft's fictional global pharmaceutical company. Analyze feedback about Caldova products and support services.

Respond ONLY with valid JSON in this exact format:
{
    "sentiment": "<POSITIVE|NEUTRAL|NEGATIVE|MIXED>",
    "confidence": <0.0-1.0>,
    "topics": ["<PRODUCT_EXPERIENCE|PACKAGING|AVAILABILITY|SUPPORT|VALUE|OTHER>"],
    "review_category": "<NONE|POTENTIAL_ADVERSE_EVENT|PRODUCT_QUALITY_COMPLAINT|MEDICAL_INQUIRY|CONTENT_SAFETY>",
    "summary": "<brief evidence-based summary>"
}

Classify overall sentiment independently from review routing. Escalate unwanted health effects as POTENTIAL_ADVERSE_EVENT, possible defects as PRODUCT_QUALITY_COMPLAINT, personalized health questions as MEDICAL_INQUIRY, and harmful content as CONTENT_SAFETY. Use NONE otherwise. Do not determine causality, assess seriousness, or provide medical advice. When uncertain, lower confidence rather than inventing facts.

Do not include any text outside the JSON object."""

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

if __name__ == "__main__":
    print("Starting hosting adapter on port 8088...", flush=True)
    ResponsesHostServer(agent).run()
