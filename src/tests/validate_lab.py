"""
Lab Validation Test Suite
==========================
Validates that the workshop repo is correctly structured and all components
work end-to-end. Run this before deploying to Skillable or after setup.

Usage:
    python src/tests/validate_lab.py                    # Run offline checks only
    python src/tests/validate_lab.py --live             # Also run live Azure inference tests
    python src/tests/validate_lab.py --live --agent     # Also test agent deployment
"""

import argparse
import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# Resolve repo root (works whether run from repo root or tests/ directory)
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent

passed = 0
failed = 0
skipped = 0
results = []


def record(name: str, status: str, detail: str = ""):
    global passed, failed, skipped
    icon = {"PASS": "\u2705", "FAIL": "\u274c", "SKIP": "\u23ed\ufe0f"}.get(status, "?")
    results.append((name, status, detail))
    if status == "PASS":
        passed += 1
    elif status == "FAIL":
        failed += 1
    else:
        skipped += 1
    line = f"  {icon} {name}"
    if detail:
        line += f" — {detail}"
    print(line)


# =========================================================================
# SECTION 1: File Structure Checks
# =========================================================================
def test_file_structure():
    print("\n" + "=" * 60)
    print("  Section 1: File Structure")
    print("=" * 60)

    required_files = [
        "README.md",
        "azure.yaml",
        "requirements.txt",
        ".env.sample",
        # Learner-support skills
        ".github/skills/ill335-lab-navigator/SKILL.md",
        ".github/skills/ill335-responses-api/SKILL.md",
        ".github/skills/ill335-hosted-agent/SKILL.md",
        ".github/skills/ill335-troubleshooting/SKILL.md",
        # Infra
        "infra/main.bicep",
        "infra/main.parameters.json",
        "infra/abbreviations.json",
        "infra/modules/ai-services.bicep",
        "infra/modules/monitoring.bicep",
        "infra/modules/role-assignments.bicep",
        # Setup & cleanup
        "setup/SETUP.md",
        "cleanup/CLEANUP.md",
        # Scripts
        "scripts/setup.ps1",
        "scripts/setup.sh",
        "scripts/postprovision.ps1",
        "scripts/postprovision.sh",
        # Labs
        "docs/lab1-discover-models.md",
        "docs/lab2-verifysetup.md",
        "docs/lab3-connect-and-infer.md",
        "docs/lab4-sentiment-analysis.md",
        "docs/lab5-model-comparison.md",
        "docs/lab6-deploy-agent.md",
        "docs/lab7-summary.md",
        # Source
        "src/01_first_inference.py",
        "src/02_sentiment_analysis.py",
        "src/03_model_comparison.py",
        "src/sample_feedback.json",
        # Agent (Hosted Agent — direct code deployment)
        "src/agent/app.py",
        "src/agent/requirements.txt",
        # Tests
        "src/tests/TESTING.md",
        "src/tests/test_sentiment.py",
        "src/tests/validate_lab.py",
    ]

    for f in required_files:
        path = REPO_ROOT / f
        if path.exists():
            record(f"File exists: {f}", "PASS")
        else:
            record(f"File exists: {f}", "FAIL", "Missing")


# =========================================================================
# SECTION 2: JSON Validation
# =========================================================================
def test_json_files():
    print("\n" + "=" * 60)
    print("  Section 2: JSON Validity")
    print("=" * 60)

    json_files = [
        "src/sample_feedback.json",
        "infra/main.parameters.json",
        "infra/abbreviations.json",
    ]

    for f in json_files:
        path = REPO_ROOT / f
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            record(f"JSON valid: {f}", "PASS")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            record(f"JSON valid: {f}", "FAIL", str(e))

    # Verify sample_feedback.json structure
    path = REPO_ROOT / "src/sample_feedback.json"
    try:
        with open(path, "r", encoding="utf-8") as fh:
            feedback_items = json.load(fh)
        if isinstance(feedback_items, list) and len(feedback_items) == 15:
            record("sample_feedback.json has 15 entries", "PASS")
        else:
            record(
                "sample_feedback.json has 15 entries",
                "FAIL",
                f"Got {len(feedback_items)}",
            )
        valid_sentiments = {"POSITIVE", "NEUTRAL", "NEGATIVE", "MIXED"}
        valid_review_categories = {
            "NONE",
            "POTENTIAL_ADVERSE_EVENT",
            "PRODUCT_QUALITY_COMPLAINT",
            "MEDICAL_INQUIRY",
            "CONTENT_SAFETY",
        }
        all_valid = all(
            item.get("expected_sentiment") in valid_sentiments
            and item.get("expected_review_category") in valid_review_categories
            for item in feedback_items
        )
        if all_valid:
            record("sample_feedback.json labels valid", "PASS")
        else:
            record(
                "sample_feedback.json labels valid",
                "FAIL",
                "Invalid expected labels",
            )
    except Exception as e:
        record("sample_feedback.json structure", "FAIL", str(e))


# =========================================================================
# SECTION 3: Python Syntax Validation
# =========================================================================
def test_python_syntax():
    print("\n" + "=" * 60)
    print("  Section 3: Python Syntax")
    print("=" * 60)

    py_files = [
        "src/01_first_inference.py",
        "src/02_sentiment_analysis.py",
        "src/03_model_comparison.py",
        "src/agent/app.py",
    ]

    for f in py_files:
        path = REPO_ROOT / f
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(path)],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            record(f"Syntax OK: {f}", "PASS")
        else:
            record(f"Syntax OK: {f}", "FAIL", result.stderr.strip())


# =========================================================================
# SECTION 4: Markdown Navigation Chain
# =========================================================================
def test_markdown_links():
    print("\n" + "=" * 60)
    print("  Section 4: Markdown Navigation Chain")
    print("=" * 60)

    # Expected navigation: Setup → Lab1 → Lab2 → Lab3 → Lab4 → Lab5 → Lab6 → Lab7 → Cleanup
    nav_chain = [
        ("setup/SETUP.md", "docs/lab1-discover-models.md"),
        ("docs/lab1-discover-models.md", "docs/lab2-verifysetup.md"),
        ("docs/lab2-verifysetup.md", "docs/lab3-connect-and-infer.md"),
        ("docs/lab3-connect-and-infer.md", "docs/lab4-sentiment-analysis.md"),
        ("docs/lab4-sentiment-analysis.md", "docs/lab5-model-comparison.md"),
        ("docs/lab5-model-comparison.md", "docs/lab6-deploy-agent.md"),
        ("docs/lab6-deploy-agent.md", "docs/lab7-summary.md"),
        ("docs/lab7-summary.md", "cleanup/CLEANUP.md"),
    ]

    for source, target in nav_chain:
        source_path = REPO_ROOT / source
        # The link in the source file references the target relative to source's directory
        target_filename = Path(target).name
        try:
            content = source_path.read_text(encoding="utf-8")
            if target_filename in content:
                record(f"Nav link: {Path(source).name} → {target_filename}", "PASS")
            else:
                record(f"Nav link: {Path(source).name} → {target_filename}", "FAIL", "Link not found")
        except FileNotFoundError:
            record(f"Nav link: {Path(source).name} → {target_filename}", "FAIL", "Source file missing")


# =========================================================================
# SECTION 5: Model Reference Consistency
# =========================================================================
def test_model_references():
    print("\n" + "=" * 60)
    print("  Section 5: Model Reference Consistency")
    print("=" * 60)

    # Ensure deprecated model names are gone
    deprecated = ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini", "gpt-4.1", "gpt-5.3-chat", "gpt-5-chat"]
    all_files = list(REPO_ROOT.rglob("*"))
    # Exclude this validation script itself — it contains deprecated names as test data
    self_path = Path(__file__).resolve()
    text_files = [
        f for f in all_files
        if f.is_file()
        and f.suffix in (".md", ".py", ".bicep", ".json", ".yaml", ".yml", ".ps1", ".sh", ".sample")
        and ".git" not in str(f)
        and ".venv" not in str(f)
        and f.resolve() != self_path
    ]

    for old_model in deprecated:
        found_in = []
        for f in text_files:
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                if old_model in content:
                    found_in.append(str(f.relative_to(REPO_ROOT)))
            except Exception:
                pass
        if not found_in:
            record(f"No references to deprecated '{old_model}'", "PASS")
        else:
            record(
                f"No references to deprecated '{old_model}'",
                "FAIL",
                f"Found in: {', '.join(found_in[:5])}",
            )

    # Ensure new model names are present where expected
    expected_model_refs = {
        "gpt-5.4-mini": [
            "infra/main.bicep",
            ".env.sample",
            "src/agent/app.py",
        ],
        "gpt-5.4": [
            "infra/main.bicep",
            ".env.sample",
        ],
    }
    for model, files in expected_model_refs.items():
        for f in files:
            path = REPO_ROOT / f
            try:
                content = path.read_text(encoding="utf-8")
                if model in content:
                    record(f"'{model}' referenced in {f}", "PASS")
                else:
                    record(f"'{model}' referenced in {f}", "FAIL", "Not found")
            except FileNotFoundError:
                record(f"'{model}' referenced in {f}", "FAIL", "File missing")


# =========================================================================
# SECTION 6: API and Session Content
# =========================================================================
def test_api_and_session_content():
    print("\n" + "=" * 60)
    print("  Section 6: Responses API and Session Identity")
    print("=" * 60)

    text_files = [
        path
        for path in REPO_ROOT.rglob("*")
        if path.is_file()
        and path.suffix
        in (".md", ".py", ".bicep", ".json", ".yaml", ".yml", ".ps1", ".sh", ".sample")
        and ".git" not in str(path)
        and ".venv" not in str(path)
        and path.resolve() != Path(__file__).resolve()
    ]

    forbidden = {
        "chat.completions": "Chat Completions API call",
        "BRK520": "legacy BRK520 session ID",
        "Microsoft Build 2026": "legacy event name",
        "Build26": "legacy event path",
        "Get Started with Models in Microsoft Foundry": "legacy session title",
    }
    for value, label in forbidden.items():
        found_in = [
            str(path.relative_to(REPO_ROOT))
            for path in text_files
            if value.lower()
            in path.read_text(encoding="utf-8", errors="ignore").lower()
        ]
        if found_in:
            record(f"No {label}", "FAIL", f"Found in: {', '.join(found_in[:5])}")
        else:
            record(f"No {label}", "PASS")

    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    for value, label in {
        "ILL335": "session ID",
        "Building & Deploying AI Agents with Microsoft Foundry": "session title",
        "AI Tour": "event name",
    }.items():
        if value in readme:
            record(f"README contains {label}", "PASS")
        else:
            record(f"README contains {label}", "FAIL", f"Missing: {value}")

    for source in ["src/01_first_inference.py", "src/02_sentiment_analysis.py"]:
        content = (REPO_ROOT / source).read_text(encoding="utf-8")
        if ".responses.create(" in content and ".output_text" in content:
            record(f"{source} uses Responses API", "PASS")
        else:
            record(f"{source} uses Responses API", "FAIL")


# =========================================================================
# SECTION 7: Infrastructure Validation
# =========================================================================
def test_infra():
    print("\n" + "=" * 60)
    print("  Section 7: Infrastructure Files")
    print("=" * 60)

    # Check azure.yaml has correct hooks
    azure_yaml = REPO_ROOT / "azure.yaml"
    try:
        content = azure_yaml.read_text(encoding="utf-8")
        for keyword in ["postprovision", "postprovision.ps1", "postprovision.sh"]:
            if keyword in content:
                record(f"azure.yaml contains '{keyword}'", "PASS")
            else:
                record(f"azure.yaml contains '{keyword}'", "FAIL")
    except FileNotFoundError:
        record("azure.yaml exists", "FAIL")

    # Check main.bicep has required params
    bicep_path = REPO_ROOT / "infra/main.bicep"
    try:
        content = bicep_path.read_text(encoding="utf-8")
        for param in [
            "environmentName",
            "location",
            "modelName",
            "deploySecondModel",
            "enableHostedAgents",
            "principalId",
        ]:
            if param in content:
                record(f"main.bicep param: {param}", "PASS")
            else:
                record(f"main.bicep param: {param}", "FAIL")

        # Check outputs
        for output in [
            "AZURE_RESOURCE_GROUP",
            "AZURE_AI_PROJECT_ENDPOINT",
            "MODEL_DEPLOYMENT_NAME",
            "AZURE_CONTAINER_REGISTRY_NAME",
        ]:
            if output in content:
                record(f"main.bicep output: {output}", "PASS")
            else:
                record(f"main.bicep output: {output}", "FAIL")
    except FileNotFoundError:
        record("main.bicep exists", "FAIL")

    # Check main.parameters.json binds all expected vars
    params_path = REPO_ROOT / "infra/main.parameters.json"
    try:
        content = params_path.read_text(encoding="utf-8")
        for var in [
            "AZURE_ENV_NAME",
            "AZURE_LOCATION",
            "AZURE_PRINCIPAL_ID",
            "DEPLOY_SECOND_MODEL",
            "ENABLE_HOSTED_AGENTS",
        ]:
            if var in content:
                record(f"parameters.json binds {var}", "PASS")
            else:
                record(f"parameters.json binds {var}", "FAIL")
    except FileNotFoundError:
        record("main.parameters.json exists", "FAIL")


# =========================================================================
# SECTION 7: Hosted Agent Files
# =========================================================================
def test_agent_service():
    print("\n" + "=" * 60)
    print("  Section 8: Hosted Agent")
    print("=" * 60)

    # Check app.py uses hosting adapter pattern
    app_path = REPO_ROOT / "src/agent/app.py"
    try:
        content = app_path.read_text(encoding="utf-8")
        if "Agent" in content and "from agent_framework import" in content:
            record("app.py uses Agent", "PASS")
        else:
            record("app.py uses Agent", "FAIL")
        if "ResponsesHostServer" in content:
            record("app.py uses hosting adapter", "PASS")
        else:
            record("app.py uses hosting adapter", "FAIL")
        if "FoundryChatClient" in content:
            record("app.py uses FoundryChatClient", "PASS")
        else:
            record("app.py uses FoundryChatClient", "FAIL")
    except FileNotFoundError:
        record("app.py exists", "FAIL")

    # Check agent requirements have hosting adapter and framework packages
    req_path = REPO_ROOT / "src/agent/requirements.txt"
    try:
        content = req_path.read_text(encoding="utf-8")
        if "agent-framework-foundry-hosting" in content:
            record("requirements.txt includes hosting adapter", "PASS")
        else:
            record("requirements.txt includes hosting adapter", "FAIL")
        if "agent-framework" in content:
            record("requirements.txt includes agent-framework", "PASS")
        else:
            record("requirements.txt includes agent-framework", "FAIL")
    except FileNotFoundError:
        record("Agent requirements.txt exists", "FAIL")

    # Check azure.yaml has agent service config
    azure_yaml = REPO_ROOT / "azure.yaml"
    try:
        content = azure_yaml.read_text(encoding="utf-8")
        if "azure.ai.agent" in content:
            record("azure.yaml host: azure.ai.agent", "PASS")
        else:
            record("azure.yaml host: azure.ai.agent", "FAIL")
        if "codeConfiguration:" in content and "runtime: python_3_13" in content:
            record("azure.yaml direct code deployment", "PASS")
        else:
            record("azure.yaml direct code deployment", "FAIL")
        if "protocol: responses" in content and "version: 2.0.0" in content:
            record("azure.yaml Responses protocol 2.0.0", "PASS")
        else:
            record("azure.yaml Responses protocol 2.0.0", "FAIL")
    except FileNotFoundError:
        record("azure.yaml exists", "FAIL")


# =========================================================================
# SECTION 8: Environment Configuration
# =========================================================================
def test_env_config():
    print("\n" + "=" * 60)
    print("  Section 9: Environment Configuration")
    print("=" * 60)

    # Check .env.sample has required vars
    sample_path = REPO_ROOT / ".env.sample"
    try:
        content = sample_path.read_text(encoding="utf-8")
        for var in ["PROJECT_ENDPOINT", "MODEL_DEPLOYMENT_NAME", "MODEL_DEPLOYMENT_NAME_2"]:
            if var in content:
                record(f".env.sample contains {var}", "PASS")
            else:
                record(f".env.sample contains {var}", "FAIL")
    except FileNotFoundError:
        record(".env.sample exists", "FAIL")

    # Check if .env exists and is configured (for live tests)
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        from dotenv import dotenv_values
        values = dotenv_values(env_path)
        endpoint = values.get("PROJECT_ENDPOINT", "")
        model = values.get("MODEL_DEPLOYMENT_NAME", "")
        if endpoint and not endpoint.startswith("https://<"):
            record(".env PROJECT_ENDPOINT configured", "PASS")
        else:
            record(".env PROJECT_ENDPOINT configured", "FAIL", "Placeholder or missing")
        if model:
            record(".env MODEL_DEPLOYMENT_NAME configured", "PASS")
        else:
            record(".env MODEL_DEPLOYMENT_NAME configured", "FAIL", "Missing")
    else:
        record(".env file exists", "SKIP", "Not yet created — run setup first")


# =========================================================================
# SECTION 9: Dependency Check
# =========================================================================
def test_dependencies():
    print("\n" + "=" * 60)
    print("  Section 10: Python Dependencies")
    print("=" * 60)

    required_packages = [
        ("azure.ai.projects", "azure-ai-projects"),
        ("azure.identity", "azure-identity"),
        ("openai", "openai"),
        ("dotenv", "python-dotenv"),
    ]

    for module_name, pip_name in required_packages:
        try:
            importlib.import_module(module_name)
            record(f"Package installed: {pip_name}", "PASS")
        except ImportError:
            record(f"Package installed: {pip_name}", "FAIL", f"pip install {pip_name}")


# =========================================================================
# SECTION 10: CLI Tool Check
# =========================================================================
def test_cli_tools():
    print("\n" + "=" * 60)
    print("  Section 11: CLI Tools")
    print("=" * 60)

    tools = {
        "az": ["az", "version", "--output", "json"],
        "azd": ["azd", "version"],
        "python": [sys.executable, "--version"],
        "git": ["git", "--version"],
    }

    use_shell = sys.platform == "win32"  # needed to find .cmd wrappers (az.cmd)

    for name, cmd in tools.items():
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15, shell=use_shell)
            if result.returncode == 0:
                version = result.stdout.strip().split("\n")[0][:60]
                record(f"CLI available: {name}", "PASS", version)
            else:
                record(f"CLI available: {name}", "FAIL", result.stderr.strip()[:80])
        except FileNotFoundError:
            record(f"CLI available: {name}", "FAIL", "Not installed")
        except subprocess.TimeoutExpired:
            record(f"CLI available: {name}", "FAIL", "Timed out")



# =========================================================================
# SECTION 11: Live Azure Inference Tests (--live flag)
# =========================================================================
def test_live_inference():
    print("\n" + "=" * 60)
    print("  Section 12: Live Azure Inference")
    print("=" * 60)

    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        record("Live test: .env required", "SKIP", "Run setup first")
        return

    from dotenv import load_dotenv
    load_dotenv(env_path)

    endpoint = os.environ.get("PROJECT_ENDPOINT", "")
    model = os.environ.get("MODEL_DEPLOYMENT_NAME", "")

    if not endpoint or endpoint.startswith("https://<"):
        record("Live test: endpoint configured", "SKIP", "PROJECT_ENDPOINT not set")
        return

    # Test 1: Basic inference (Lab 3)
    try:
        from azure.ai.projects import AIProjectClient
        from azure.identity import DefaultAzureCredential

        client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(),
        )
        inference = client.get_openai_client()
        response = inference.responses.create(
            model=model,
            instructions="Respond with exactly: HELLO",
            input="Say hello",
        )
        content = response.output_text
        if content:
            record("Live: Basic inference", "PASS", f"Response: {content[:50]}")
        else:
            record("Live: Basic inference", "FAIL", "Empty response")
    except Exception as e:
        record("Live: Basic inference", "FAIL", str(e)[:100])

    # Test 2: Caldova sentiment and regulated-signal classification (Lab 4)
    try:
        sentiment_prompt = """You analyze consumer feedback for Caldova, a fictional pharmaceutical company.
Respond ONLY with valid JSON:
{"sentiment": "<POSITIVE|NEUTRAL|NEGATIVE|MIXED>", "confidence": <0.0-1.0>, "review_category": "<NONE|POTENTIAL_ADVERSE_EVENT|PRODUCT_QUALITY_COMPLAINT|MEDICAL_INQUIRY|CONTENT_SAFETY>"}
Use POTENTIAL_ADVERSE_EVENT for an unwanted symptom associated with product use. Do not provide medical advice."""
        test_cases = [
            (
                "The packaging is clear and easy to use.",
                "POSITIVE",
                "NONE",
            ),
            (
                "I felt dizzy after taking the Caldova allergy relief tablets.",
                "NEGATIVE",
                "POTENTIAL_ADVERSE_EVENT",
            ),
        ]

        for feedback, expected_sentiment, expected_review_category in test_cases:
            try:
                response = inference.responses.create(
                    model=model,
                    instructions=sentiment_prompt,
                    input=feedback,
                )
                raw = response.output_text.strip()
                try:
                    result = json.loads(raw)
                    sentiment = result.get("sentiment", "")
                    review_category = result.get("review_category", "")
                    if (
                        sentiment == expected_sentiment
                        and review_category == expected_review_category
                    ):
                        record(
                            f"Live: Analyze '{feedback[:30]}...'",
                            "PASS",
                            f"{sentiment}, {review_category}",
                        )
                    else:
                        record(
                            f"Live: Analyze '{feedback[:30]}...'",
                            "FAIL",
                            "Expected "
                            f"{expected_sentiment}/{expected_review_category}, got "
                            f"{sentiment}/{review_category}",
                        )
                except json.JSONDecodeError:
                    record(
                        f"Live: Analyze '{feedback[:30]}...'",
                        "FAIL",
                        f"Non-JSON: {raw[:50]}",
                    )
            except Exception as inference_error:
                record(
                    f"Live: Analyze '{feedback[:30]}...'",
                    "FAIL",
                    str(inference_error)[:100],
                )
    except Exception as e:
        record("Live: Sentiment classification", "FAIL", str(e)[:100])

    # Test 3: Second model (Lab 5) — optional
    model2 = os.environ.get("MODEL_DEPLOYMENT_NAME_2", "")
    if model2:
        try:
            response = inference.responses.create(
                model=model2,
                instructions="Respond with exactly: OK",
                input="Confirm",
            )
            if response.output_text:
                record("Live: Second model inference", "PASS", f"Model: {model2}")
            else:
                record("Live: Second model inference", "FAIL", "Empty response")
        except Exception as e:
            record("Live: Second model inference", "FAIL", str(e)[:100])
    else:
        record("Live: Second model inference", "SKIP", "MODEL_DEPLOYMENT_NAME_2 not set")


# =========================================================================
# SECTION 12: Agent Deployment Test (--agent flag)
# =========================================================================
def test_agent_deployment():
    print("\n" + "=" * 60)
    print("  Section 13: Agent Deployment (Lab 6)")
    print("=" * 60)

    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        record("Agent test: .env required", "SKIP", "Run setup first")
        return

    from dotenv import load_dotenv
    load_dotenv(env_path)

    endpoint = os.environ.get("PROJECT_ENDPOINT", "")
    if not endpoint or endpoint.startswith("https://<"):
        record("Agent test: project configured", "SKIP", "PROJECT_ENDPOINT not set")
        return

    command_env = os.environ.copy()
    command_env["AZURE_DEV_USER_AGENT"] = "microsoft_foundry_skill"
    try:
        result = subprocess.run(
            ["azd", "ai", "agent", "show", "--output", "json"],
            cwd=REPO_ROOT,
            env=command_env,
            capture_output=True,
            text=True,
            timeout=60,
            shell=sys.platform == "win32",
        )
        if result.returncode == 0 and '"status"' in result.stdout:
            record("Agent deployment is discoverable", "PASS")
        else:
            record("Agent deployment is discoverable", "FAIL", result.stderr.strip()[:100])
    except (FileNotFoundError, subprocess.TimeoutExpired):
        record("Agent deployment is discoverable", "FAIL", "azd unavailable or timed out")


# =========================================================================
# Summary
# =========================================================================
def print_summary():
    print("\n" + "=" * 60)
    print("  VALIDATION SUMMARY")
    print("=" * 60)
    total = passed + failed + skipped
    print(f"  Total checks: {total}")
    print(f"  \u2705 Passed:  {passed}")
    print(f"  \u274c Failed:  {failed}")
    print(f"  \u23ed\ufe0f  Skipped: {skipped}")
    print()

    if failed > 0:
        print("  FAILED CHECKS:")
        for name, status, detail in results:
            if status == "FAIL":
                print(f"    \u274c {name}: {detail}")
        print()
        print("  Result: FAIL — fix the issues above before running the lab.")
        return 1
    else:
        print("  Result: PASS — lab is ready!")
        return 0


# =========================================================================
# Main
# =========================================================================
def main():
    parser = argparse.ArgumentParser(description="Validate workshop lab setup")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Run live Azure inference tests (requires .env with valid credentials)",
    )
    parser.add_argument(
        "--agent",
        action="store_true",
        help="Also verify the hosted-agent deployment with azd",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  Workshop Lab Validation")
    print("  ILL335: Building & Deploying AI Agents with Microsoft Foundry")
    print("=" * 60)

    # Always run offline checks
    test_file_structure()
    test_json_files()
    test_python_syntax()
    test_markdown_links()
    test_model_references()
    test_api_and_session_content()
    test_infra()
    test_agent_service()
    test_env_config()
    test_dependencies()
    test_cli_tools()

    # Optionally run live tests
    if args.live:
        test_live_inference()

    if args.agent:
        test_agent_deployment()

    exit_code = print_summary()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
