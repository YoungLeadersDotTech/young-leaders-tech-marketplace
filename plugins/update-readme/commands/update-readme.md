---
description: Update or rewrite the README for the current repo, plugin, or sub-object. Detects type, asks detail level, then generates.
---

# /update-readme

Invoke the `update-readme` skill from this plugin.

The skill walks through six phases with task tracking and AskUserQuestion gates:

1. **Context review** - parallel-read all canonical files (existing README, manifest, build files, LICENSE, top-level layout)
2. **Type confirmation** - auto-classify the repo or sub-object, then ask user to confirm or override
3. **Detail level** - minimal / standard / comprehensive / custom
4. **Generate** - build the README using type + detail level as a routing key
5. **Preview and confirm** - show the draft, accept write / dry-run / edit / cancel
6. **Write** - write to disk, or print only if dry-run

## Arguments

| Argument | Default | Description |
|---|---|---|
| `--dry-run` | false | Print the generated README to the terminal instead of writing |
| `--target <path>` | cwd | Run against a specific repo or sub-object instead of the working directory |

## Examples

```text
/update-readme
/update-readme --dry-run
/update-readme --target ~/Projects/my-other-project
```
