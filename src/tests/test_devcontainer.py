"""Offline dev-container hook tests; no package installs or Azure operations."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
BASH = os.environ.get("BASH_EXECUTABLE") or shutil.which("bash")


class DevcontainerConfigTests(unittest.TestCase):
    def test_installation_runs_during_prebuild(self):
        config = json.loads((ROOT / ".devcontainer/devcontainer.json").read_text())
        self.assertEqual(
            config["updateContentCommand"], "bash .devcontainer/post-create.sh"
        )
        self.assertEqual(config["waitFor"], "updateContentCommand")
        for hook in ("postCreateCommand", "postStartCommand", "postAttachCommand"):
            self.assertNotIn(hook, config)
        self.assertIn("3.13", config["image"])
        self.assertEqual(config["remoteUser"], "vscode")

    def test_hook_uses_linux_line_endings(self):
        self.assertNotIn(b"\r", (ROOT / ".devcontainer/post-create.sh").read_bytes())


@unittest.skipUnless(BASH, "Bash is required to exercise the Linux container hook")
class DevcontainerHookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / ".devcontainer").mkdir()
        shutil.copyfile(
            ROOT / ".devcontainer/post-create.sh",
            self.root / ".devcontainer/post-create.sh",
        )
        (self.root / "requirements.txt").write_text("# Test fixture\n")
        (self.root / "bin").mkdir()
        self.write_executable("bin/git", "#!/bin/bash\nexit 0\n")
        self.write_executable("bin/az", "#!/bin/bash\necho 'Unexpected Azure operation' >&2\nexit 99\n")
        self.write_executable(
            "bin/azd",
            """#!/bin/bash
printf 'azd %s\\n' "$*" >> calls
[[ "$*" == "ext install "* ]] || exit 99
if [[ "$*" == *"${FAIL_EXTENSION:-never-match}"* ]]; then
    echo "Extension installation failed" >&2
    exit 17
fi
""",
        )
        self.write_executable(
            "bin/python3",
            """#!/bin/bash
printf 'python3 %s\\n' "$*" >> calls
[[ "$*" == "-m venv .venv" ]] || exit 99
mkdir -p .venv/bin
cp bin/venv-python .venv/bin/python
chmod +x .venv/bin/python
""",
        )
        self.write_executable(
            "bin/venv-python",
            """#!/bin/bash
printf 'venv %s\\n' "$*" >> calls
if [[ "$*" == *"${FAIL_PIP:-never-match}"* ]]; then
    echo "Dependency validation failed" >&2
    exit 18
fi
""",
        )

    def write_executable(self, relative_path, content):
        path = self.root / relative_path
        path.write_text(content, encoding="utf-8", newline="\n")
        path.chmod(0o755)

    def run_hook(self, **variables):
        return subprocess.run(
            [BASH, "-c", 'export PATH="$PWD/bin:$PATH"; bash .devcontainer/post-create.sh'],
            cwd=self.root,
            env={**os.environ, **variables},
            capture_output=True,
            text=True,
            timeout=30,
        )

    def test_fresh_setup_and_rerun_reuse_environment(self):
        for _ in range(2):
            result = self.run_hook()
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("development environment ready", result.stdout)
        calls = (self.root / "calls").read_text()
        for extension in ("microsoft.foundry", "azure.ai.agents", "azure.ai.projects"):
            self.assertEqual(calls.count(f"azd ext install {extension} --no-prompt"), 2)
        self.assertEqual(calls.count("python3 -m venv .venv"), 1)
        self.assertEqual(calls.count("--requirement requirements.txt"), 2)
        self.assertEqual(calls.count("venv -m pip check"), 2)
        self.assertNotIn("src/agent/requirements.txt", calls)
        self.assertFalse((self.root / ".env").exists())

    def test_foreign_environment_is_preserved(self):
        (self.root / ".venv").mkdir()
        marker = self.root / ".venv/keep.txt"
        marker.write_text("existing environment")
        result = self.run_hook()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Rename it on the host", result.stderr)
        self.assertEqual(marker.read_text(), "existing environment")
        self.assertFalse((self.root / "calls").exists())

    def test_each_extension_failure_stops_setup(self):
        for extension in ("microsoft.foundry", "azure.ai.agents", "azure.ai.projects"):
            with self.subTest(extension=extension):
                result = self.run_hook(FAIL_EXTENSION=extension)
                self.assertEqual(result.returncode, 17)
                self.assertNotIn("development environment ready", result.stdout)
                self.assertFalse((self.root / ".venv").exists())

    def test_pip_failures_are_not_reported_as_success(self):
        for command in ("pip install", "pip check"):
            with self.subTest(command=command):
                result = self.run_hook(FAIL_PIP=command)
                self.assertEqual(result.returncode, 18)
                self.assertNotIn("development environment ready", result.stdout)


if __name__ == "__main__":
    unittest.main()
