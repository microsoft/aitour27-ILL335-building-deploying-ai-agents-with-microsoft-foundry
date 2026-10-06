#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

for command_name in git az azd python3; do
    if ! command -v "$command_name" >/dev/null 2>&1; then
        printf 'Missing required command: %s. Rebuild the dev container.\n' "$command_name" >&2
        exit 1
    fi
done

if [[ -e .venv && ! -x .venv/bin/python ]]; then
    printf 'The existing .venv is not a Linux virtual environment. Rename it on the host and rebuild the dev container.\n' >&2
    exit 1
fi

# Install the providers explicitly as well as the bundle, including on reruns.
for extension in microsoft.foundry azure.ai.agents azure.ai.projects; do
    azd ext install "$extension" --no-prompt
done

if [[ ! -x .venv/bin/python ]]; then
    python3 -m venv .venv
fi

.venv/bin/python -c 'import sys; sys.exit("Python 3.13+ is required. Rename .venv and rebuild the dev container.") if sys.version_info < (3, 13) else None'
.venv/bin/python -m pip install --disable-pip-version-check --requirement requirements.txt
.venv/bin/python -m pip check

printf '\nILL335 development environment ready. Activate it with: source .venv/bin/activate\n'
printf 'Next: follow the BYOD instructions in setup/SETUP.md. No Azure login or provisioning has been performed.\n'
