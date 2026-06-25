import json
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "skills" / "opencode-sync" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import ingest_source  # noqa: E402


class IngestSourceTests(unittest.TestCase):
    def test_filter_units_by_enablement_keeps_plugins_not_explicitly_disabled(self):
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

        self.assertEqual([name for name, _ in filtered], ["alpha", "beta"])

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

    def test_catalogue_style_assets_discovers_skills_agents_commands_and_hooks(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            plugin = root / "plugins" / "alpha"
            (plugin / "skills" / "example").mkdir(parents=True)
            (plugin / "agents").mkdir()
            (plugin / "commands").mkdir()
            (plugin / "hooks").mkdir()

            skill = plugin / "skills" / "example" / "SKILL.md"
            agent = plugin / "agents" / "helper.md"
            command = plugin / "commands" / "run.md"
            hook = plugin / "hooks" / "post-tool.py"
            skill.write_text("---\nname: example\n---\n")
            agent.write_text("---\ndescription: helper\n---\n")
            command.write_text("---\ndescription: run\n---\n")
            hook.write_text("print('ok')\n")

            assets = ingest_source.catalogue_style_assets([plugin])

            self.assertEqual(assets["skills"], [str(skill.resolve())])
            self.assertEqual(assets["agents"], [str(agent.resolve())])
            self.assertEqual(assets["commands"], [str(command.resolve())])
            self.assertEqual(assets["hooks"], [str(hook.resolve())])

    def test_verify_capture_reports_missing_items_and_project_local_mcp(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            plugin = root / "plugins" / "alpha"
            (plugin / "skills" / "example").mkdir(parents=True)
            (plugin / "agents").mkdir()
            (plugin / "commands").mkdir()
            (plugin / "hooks").mkdir()
            (root / ".claude").mkdir()

            skill = plugin / "skills" / "example" / "SKILL.md"
            agent = plugin / "agents" / "helper.md"
            command = plugin / "commands" / "run.md"
            hook = plugin / "hooks" / "post-tool.py"
            skill.write_text("---\nname: example\n---\n")
            agent.write_text("---\ndescription: helper\n---\n")
            command.write_text("---\ndescription: run\n---\n")
            hook.write_text("print('ok')\n")
            (root / ".claude" / "settings.json").write_text(json.dumps({
                "mcpServers": {"project-mcp": {"command": "npx", "args": ["x"]}}
            }))
            (root / ".claude" / "settings.local.json").write_text(json.dumps({
                "mcpServers": {"local-mcp": {"command": "npx", "args": ["y"]}}
            }))

            verification = ingest_source.verify_capture(
                root,
                "marketplace",
                [("alpha", plugin / "skills")],
                {"skills": [str(skill)], "agents": [], "commands": [], "mcp": {}, "hide": []},
            )

            self.assertEqual(verification["missing"]["skills"], [])
            self.assertEqual(verification["missing"]["agents"], [str(agent.resolve())])
            self.assertEqual(verification["missing"]["commands"], [str(command.resolve())])
            self.assertEqual(verification["expected"]["hooks"], [str(hook.resolve())])
            self.assertEqual(sorted(verification["claude_mcp"]["project"].keys()), ["project-mcp"])
            self.assertEqual(sorted(verification["claude_mcp"]["local"].keys()), ["local-mcp"])

    def test_merge_claude_mcp_sources_keeps_user_global_and_repo_local_project(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".claude").mkdir()
            original_home = ingest_source.Path.home
            fake_home = root / "home"
            (fake_home / ".claude").mkdir(parents=True)
            try:
                ingest_source.Path.home = staticmethod(lambda: fake_home)
                (fake_home / ".claude" / "settings.json").write_text(json.dumps({
                    "mcpServers": {"user-mcp": {"command": "npx", "args": ["u"]}}
                }))
                (root / ".claude" / "settings.json").write_text(json.dumps({
                    "mcpServers": {"project-mcp": {"command": "npx", "args": ["p"]}}
                }))
                (root / ".claude" / "settings.local.json").write_text(json.dumps({
                    "mcpServers": {"local-mcp": {"command": "npx", "args": ["l"]}}
                }))

                user_mcp, repo_mcp, sources = ingest_source.merge_claude_mcp_sources(root)

                self.assertEqual(sorted(user_mcp.keys()), ["user-mcp"])
                self.assertEqual(sorted(repo_mcp.keys()), ["local-mcp", "project-mcp"])
                self.assertEqual(sorted(sources["project"].keys()), ["project-mcp"])
                self.assertEqual(sorted(sources["local"].keys()), ["local-mcp"])
            finally:
                ingest_source.Path.home = original_home

    def test_dry_run_routes_repo_scope_mcp_to_project_fragment(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "marketplace"
            plugin = root / "plugins" / "alpha"
            (plugin / "skills" / "example").mkdir(parents=True)
            (root / ".claude-plugin").mkdir()
            (root / ".claude").mkdir()

            (root / ".claude-plugin" / "marketplace.json").write_text(json.dumps({
                "name": "test-marketplace",
                "plugins": [{"name": "alpha", "source": "./plugins/alpha", "version": "1.0.0"}]
            }))
            (plugin / "skills" / "example" / "SKILL.md").write_text("---\nname: example\ndescription: test\n---\n")
            (root / ".claude" / "settings.json").write_text(json.dumps({
                "enabledPlugins": {"alpha@test-marketplace": True},
                "mcpServers": {"project-mcp": {"command": "npx", "args": ["proj"]}}
            }))
            (root / ".claude" / "settings.local.json").write_text(json.dumps({
                "mcpServers": {"local-mcp": {"url": "https://example.test/mcp"}}
            }))

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_DIR / "ingest_source.py"),
                    str(root),
                    "--config-target",
                    "global",
                    "--respect-claude-settings",
                    "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("repo-scope MCP server(s) -> project only (local-mcp, project-mcp)", result.stdout)
            self.assertIn('--- project config ->', result.stdout)
            self.assertIn('"project-mcp"', result.stdout)
            self.assertIn('"local-mcp"', result.stdout)

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
