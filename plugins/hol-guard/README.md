# HOL Guard

This marketplace plugin packages the canonical HOL Guard skill for Claude Code and OpenCode users.

After adding the marketplace, install it with:

```text
/plugin install hol-guard@young-leaders-tech-marketplace
```

The skill can install and invoke the HOL Guard runtime for supported local AI harnesses. Typical runtime setup uses:

```bash
pipx install hol-guard
hol-guard detect --json
hol-guard bootstrap
hol-guard install <harness>
hol-guard run <harness> --dry-run
hol-guard run <harness>
hol-guard status
```

Installing this plugin does not by itself make a harness protected. HOL Guard must report the intended harness as installed and active. This integration is for the local agent-harness boundary; it does not claim native interception inside external services or servers.

For package scanning, `plugin-scanner` is a separate distribution:

```bash
pipx install plugin-scanner
plugin-scanner lint .
plugin-scanner verify .
```

Upstream: https://github.com/hashgraph-online/hol-guard

License: Apache-2.0
