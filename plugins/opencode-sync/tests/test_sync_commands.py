import json
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "skills" / "opencode-sync" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import sync_commands  # noqa: E402


class SyncCommandsTests(unittest.TestCase):
    def test_build_output_drops_argument_hint_and_preserves_supported_fields(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "deploy.md"
            src.write_text(
                "---\n"
                "description: Deploy the target\n"
                "argument-hint: <service>\n"
                "agent: build\n"
                "model: sonnet\n"
                "---\n\n"
                "Deploy $ARGUMENTS\n"
            )
            text = src.read_text()
            fm_lines, body = sync_commands.split_frontmatter(text)
            fm = sync_commands.parse_frontmatter(fm_lines)

            class Args:
                provider = "anthropic"
                model_aliases = dict(sync_commands.MODEL_ALIASES)

            name, output, warnings, _sha = sync_commands.build_output(src, fm, body, Args())
            self.assertEqual(name, "deploy")
            self.assertIn("description: Deploy the target", output)
            self.assertIn("agent: build", output)
            self.assertIn("model: anthropic/claude-sonnet-4-5", output)
            self.assertIn("Deploy $ARGUMENTS", output)
            self.assertIn("argument-hint has no OpenCode equivalent - dropped", warnings)

    def test_cli_generates_command_file_and_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            command_dir = root / "commands"
            out_dir = root / ".opencode" / "command"
            manifest = root / ".opencode-sync" / "manifest.json"
            command_dir.mkdir(parents=True)
            (command_dir / "deploy.md").write_text(
                "---\n"
                "description: Deploy the target\n"
                "---\n\n"
                "Deploy $ARGUMENTS\n"
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_DIR / "sync_commands.py"),
                    str(command_dir),
                    "--out-dir",
                    str(out_dir),
                    "--manifest",
                    str(manifest),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            generated = out_dir / "deploy.md"
            self.assertTrue(generated.exists())
            self.assertIn("Deploy $ARGUMENTS", generated.read_text())
            data = json.loads(manifest.read_text())
            self.assertIn(str(generated), data["generated"])
            self.assertIn("manifest updated", result.stdout)


if __name__ == "__main__":
    unittest.main()
