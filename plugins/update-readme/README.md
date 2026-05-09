# update-readme

**Version**: 1.0.0
**Author**: Young Leaders Tech
**License**: MIT

## Overview

`update-readme` is a universal README refresher for any repository or sub-object.
It auto-detects the type of the thing it is documenting (Claude Code plugin, plugin
marketplace, generic library, Toast service, monorepo, personal repo), confirms that
classification with you, asks how detailed a README you want, and then generates one
using sections appropriate to the type.

It is the inverse of every "README template" repo - rather than handing you a
boilerplate to fill in by hand, it scans what you already have and writes the README
that fits.

## What it does

1. **Scans the target** - parallel reads of canonical sources (existing README,
   plugin manifest, build files, LICENSE, top-level directory listing, marketplace.json
   if present).
2. **Classifies** the repo type from the evidence found, surfacing the signals so the
   classification is auditable.
3. **Confirms with you via AskUserQuestion** - you can accept the auto-detected type
   or override it.
4. **Asks the detail level** - minimal / standard / comprehensive / custom.
5. **Generates the README** using a section catalogue keyed on type + detail level.
   Different types produce different shapes (a marketplace gets a plugins table; a
   plugin gets command and agent tables; a Toast service gets Datadog and IDP links;
   etc.).
6. **Previews and confirms** - shows you the draft, lets you write, dry-run, edit a
   section, or cancel.

## Slash command

```text
/update-readme              # interactive on cwd
/update-readme --dry-run    # print, don't write
/update-readme --target /some/path
```

## Repo types it knows about

- Claude Code plugin marketplace (root README)
- Individual Claude Code plugin
- Toast service repository (Java / Kotlin / Dropwizard / Camel)
- Generic open source library or app (Python / JS / Go / Rust)
- Personal repository (dotfiles, scripts, notes)
- Monorepo (asks which subproject)
- Other (free text)

If your repo is something else, pick "Other" and the skill will fall back to a generic
template using your detail-level preference.

## Detail levels

- **Minimal** - title, install, quick start, license. ~50 lines.
- **Standard** (default) - title, overview, install, usage, configuration, contributing, license. ~150 lines.
- **Comprehensive** - everything plus troubleshooting, FAQ, examples, architecture, contributing guidelines. ~400 lines.
- **Custom** - multi-select from a section list.

## Why this exists

The toast-developer-docs:update-readme skill has a great methodology (parallel scan,
classify, validate links before writing, dry-run support) but its output is hard-wired
to Toast service repos. This plugin keeps the methodology and broadens the output to
cover anything you might ship.

## Companion to

- `terminal-setup-macos` - the prompt-as-document-pattern reference example, which
  benefits from a fresh README each time the underlying gotchas change.
- `skills-toolkit` - this plugin was authored using `skills-toolkit:skill-creator-agent`
  and validated against the marketplace-guidelines.md it ships.

## Install

From the marketplace root:

```bash
./install-plugin.sh install update-readme
```

Or add the marketplace URL once and Claude Code picks up all three plugins:

```text
https://github.com/YoungLeadersDotTech/young-leaders-tech-marketplace/raw/master/.claude-plugin/marketplace.json
```

## Maintainer

Young Leaders Tech &middot; <https://youngleaders.tech>

## License

MIT
