import json
import tempfile
import unittest
from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "skills" / "opencode-sync" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import ingest_source  # noqa: E402


class IngestSourceTests(unittest.TestCase):
    def test_filter_units_by_enablement_keeps_only_enabled_plugins(self):
        units = [
            ("alpha", Path("/tmp/alpha/skills")),
            ("beta", Path("/tmp/beta/skills")),
            ("gamma", Path("/tmp/gamma/skills")),
        ]

        filtered = ingest_source.filter_units_by_enablement(
            units,
            enabled={"alpha", "gamma"},
            disabled={"gamma"},
        )

        self.assertEqual([name for name, _ in filtered], ["alpha"])

    def test_filter_discovery_to_units_keeps_agents_under_plugin_root(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            plugin = root / "plugins" / "alpha"
            skills_dir = plugin / "skills"
            agents_dir = plugin / "agents"
            skills_dir.mkdir(parents=True)
            agents_dir.mkdir(parents=True)

            skill = skills_dir / "example" / "SKILL.md"
            skill.parent.mkdir()
            skill.write_text("---\nname: example\n---\n")

            agent = agents_dir / "helper.md"
            agent.write_text("---\ndescription: helper\n---\n")

            disc = {
                "skills": [str(skill)],
                "hide": [],
                "agents": [str(agent)],
                "commands": [],
                "mcp": {},
            }

            filtered = ingest_source.filter_discovery_to_units(
                root,
                "marketplace",
                disc,
                [("alpha", skills_dir)],
            )

            self.assertEqual(filtered["skills"], [str(skill)])
            self.assertEqual(filtered["agents"], [str(agent)])

    def test_find_mcp_servers_reads_direct_plugin_cache_shape(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".mcp.json").write_text(json.dumps({
                "context7": {
                    "command": "npx",
                    "args": ["-y", "@upstash/context7-mcp"],
                }
            }))

            servers = ingest_source.find_mcp_servers(root)

            self.assertIn("context7", servers)
            self.assertEqual(servers["context7"]["command"], "npx")

    def test_default_agent_out_dir_prefers_global_when_global_target_present(self):
        out_dir = ingest_source.default_agent_out_dir({"global"}, None)
        self.assertEqual(out_dir, str(Path.home() / ".config" / "opencode" / "agent"))

    def test_wire_memory_instructions_include_project_memory_when_present(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "MEMORY.md").write_text("# Test Memory\n")

            instructions = ingest_source.wire_memory_instructions(root)

            self.assertEqual(
                instructions,
                ["MEMORY.md", "AGENTS.md", "~/.claude/memory/memory.md"],
            )

    def test_wire_memory_instructions_fall_back_without_project_memory(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)

            instructions = ingest_source.wire_memory_instructions(root)

            self.assertEqual(
                instructions,
                ["AGENTS.md", "~/.claude/memory/memory.md"],
            )


if __name__ == "__main__":
    unittest.main()
