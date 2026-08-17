# Tests

Offline checks and optional live validation for the Caldova consumer sentiment lab.

| File | Purpose |
|------|---------|
| `test_sentiment.py` | Unit tests for confidence-based dashboard routing and regulated-signal escalation |
| `validate_lab.py` | Repository structure, JSON, syntax, infrastructure, dependency, and optional live inference checks |
| `TESTING.md` | Manual test instructions for each lab phase |

## Run the unit tests

```bash
pytest src/tests/test_sentiment.py -v
```

## Run offline validation

```bash
python src/tests/validate_lab.py
```

## Run optional live validation

```bash
python src/tests/validate_lab.py --live
```

Live checks require a configured `.env` file and Azure authentication.
