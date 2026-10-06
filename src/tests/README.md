# Tests

Offline checks and optional live validation for the Caldova consumer sentiment lab.

| File | Purpose |
|------|---------|
| `test_sentiment.py` | Unit tests for confidence-based dashboard routing and regulated-signal escalation |
| `test_devcontainer.py` | Offline prebuild configuration and Bash hook tests with mocked CLIs |
| `validate_lab.py` | Repository structure, JSON, syntax, infrastructure, dependency, and optional live inference checks |
| `TESTING.md` | Manual tests for inference, routing, hosted-agent deployment, and optional evaluation |

## Run the unit tests

```bash
pytest src/tests/test_sentiment.py -v
```

Run the dev-container regression tests without installing dependencies or
contacting Azure:

```bash
python -m unittest discover -s src/tests -p test_devcontainer.py -v
```

Bash is required for the hook tests. On Windows, set `BASH_EXECUTABLE` to the
Git for Windows Bash executable if the default `bash` points to an unconfigured
WSL installation. These tests verify fresh setup, reruns, explicit provider
installation, failure propagation, and preservation of an incompatible `.venv`.
They do not replace a real container build or the Codespaces **Prebuild ready**
check described in [Setup](../../setup/SETUP.md#enable-cached-codespaces-prebuilds-repository-administrators).

## Run offline validation

```bash
python src/tests/validate_lab.py
```

## Run optional live validation

```bash
python src/tests/validate_lab.py --live
```

Live checks require a configured `.env` file and Azure authentication.
