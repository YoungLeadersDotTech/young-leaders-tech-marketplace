# update-readme

**Version**: 1.0.3
**Author**: Young Leaders Tech
**License**: MIT

## Overview

`update-readme` is a universal README refresher for any repository or sub-object.
It auto-detects the type of the thing it is documenting (Claude Code plugin, plugin
marketplace, generic library, service repository, monorepo, personal repo), confirms
that classification with you, asks how detailed a README you want, and then generates
one using sections appropriate to the type.

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
   plugin gets command and agent tables; a service repo gets operational links when
   they exist; etc.).
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
- Service repository (Java / Kotlin / Dropwizard / Camel)
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

This plugin preserves the same scan, classify, preview, and write discipline you want
from a serious README workflow, but keeps the shipped output generic enough for any repo
you can publish.

## Companion to

- `terminal-setup-macos` - the prompt-as-document-pattern reference example, which
  benefits from a fresh README each time the underlying gotchas change.
- `skills-toolkit` - this plugin was authored using `skills-toolkit:skill-creator-agent`
  and validated against the marketplace-guidelines.md it ships.

## Install

In Claude Code, add the marketplace once (SSH form - see [root README](../../README.md#quick-install) for HTTPS and other options):

```text
/plugin marketplace add git@github.com:YoungLeadersDotTech/young-leaders-tech-marketplace.git
```

Then install this plugin:

```text
/plugin install update-readme@young-leaders-tech-marketplace
```

Activate in the current session:

```text
/reload-plugins
```

Then run the slash command from any directory:

```text
/update-readme
```

## Maintainer

Young Leaders Tech &middot; <https://youngleaders.tech>

## License

MIT
