# Lab 2: Verify your project

> **Duration:** ~5 minutes

## Objective

Validate that your lab project environment is configured correctly -- ensuring the `.env` file, dependencies, and CLI tools are all in place before you start writing code.

## Step 1: Validate the .env is correct

In VS Code, ensure that the `.env` file has been created in the root of your project.

1. Open the `.env` file from the root of the project folder.
2. Confirm the following variables exist:

    ```text
    PROJECT_ENDPOINT
    MODEL_DEPLOYMENT_NAME
    ```

    You may also see `MODEL_DEPLOYMENT_NAME_2`, which is optional for the model comparison lab.
3. (Optional) Confirm the values are correct according to your Foundry project. `PROJECT_ENDPOINT` should match the project endpoint listed at https://ai.azure.com, and `MODEL_DEPLOYMENT_NAME` should match the name of the model deployment.

## Step 2: Validate your setup

Run the included validation script to confirm that all files, dependencies, CLI tools, and configuration are correct:

1. Open a terminal in VS Code by selecting **Terminal → New Terminal**.
2. Run this command:

    ```powershell
    python -X utf8 src/tests/validate_lab.py
    ```

3. You should see output ending with:

    ```text
    VALIDATION SUMMARY
    ❌ Failed:  0

    Result: PASS -- lab is ready!
    ```

    The exact check count can change as the workshop evolves. Confirm that the failed count is zero and the final result is `PASS`.

If any checks fail, the output tells you exactly what to fix. Common issues:

| Failure | Fix |
|---------|-----|
| Missing file | Re-check your azd provision output for errors |
| CLI not found | Install the missing tool (see SETUP.md) |
| Package not installed | Run `pip install -r requirements.txt` inside your `.venv` |
| .env not configured | Copy `.env.sample` to `.env` and fill in your endpoint |

> **Tip:** Re-run validation after any fix to confirm it resolves the issue.

## What you learned

- ✅ How to validate your setup with the automated validation script
- ✅ How to load the workshop solution in VS Code

## Key takeaway

> A Foundry project is your workspace for organizing AI resources. The project endpoint is the single connection point your application code needs to access any model deployed within it.

---

**Next:** [Lab 3 - Connect and send your first inference](./lab3-connect-and-infer.md)

