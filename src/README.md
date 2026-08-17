# Source Code

Python scripts and agent code for the lab exercises.

| File | Lab | Description |
|------|-----|-------------|
| `01_first_inference.py` | Lab 3 | Connect to a Foundry model and send your first inference request |
| `02_sentiment_analysis.py` | Lab 4 | Consumer sentiment analysis pipeline with structured output and governed routing |
| `03_model_comparison.py` | Lab 5 | Compare outputs across multiple models |
| `sample_feedback.json` | Lab 4-5 | Test data for sentiment analysis and comparison exercises |
| `agent/` | Lab 6 | Hosted agent app entry point and Python dependencies; deployment settings are in `../azure.yaml` |

## How it works

Your Copilot agent scans this folder for context when you run any phase (`Get Started`, `Refine Content`, `Finalize`). It uses what it finds here to propose session titles, descriptions, learning outcomes, and more — but never commits these files to the repo.
