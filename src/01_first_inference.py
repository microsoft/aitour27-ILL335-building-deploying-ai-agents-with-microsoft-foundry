"""
Lab 3: First Inference with Microsoft Foundry
==============================================
Connect to a Foundry project and send your first inference request to a hosted model.
"""

import os
import sys

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


def main():
    # --- Validate environment ---
    endpoint = os.environ.get("PROJECT_ENDPOINT")
    model = os.environ.get("MODEL_DEPLOYMENT_NAME")

    if not endpoint or endpoint.startswith("https://<"):
        print("ERROR: Set PROJECT_ENDPOINT in your .env file (see Lab 2).")
        sys.exit(1)
    if not model:
        print("ERROR: Set MODEL_DEPLOYMENT_NAME in your .env file.")
        sys.exit(1)

    # --- Connect to Foundry project ---
    print("Connecting to Foundry project...")
    project_client = AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )

    # --- Get inference client ---
    inference_client = project_client.get_openai_client()

    # --- Send inference request ---
    print(f"Sending inference request to model: {model}")
    response = inference_client.responses.create(
        model=model,
        instructions="You are a helpful assistant for Caldova, Microsoft's fictional global pharmaceutical company. Respond concisely and do not provide medical advice.",
        input="How could Caldova use Microsoft Foundry to understand consumer sentiment about its products? Answer in one sentence.",
    )

    # --- Process response ---
    content = response.output_text
    print("---")
    print(f"Response:\n{content}")
    print("---")
    print(f"Model: {response.model}")
    print(f"Status: {response.status}")
    print(
        f"Tokens used: {response.usage.total_tokens} "
        f"(input: {response.usage.input_tokens}, "
        f"output: {response.usage.output_tokens})"
    )


if __name__ == "__main__":
    main()
