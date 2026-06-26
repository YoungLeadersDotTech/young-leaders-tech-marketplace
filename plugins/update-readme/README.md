# update-readme

**Version**: 1.1.0
**Author**: Young Leaders Tech
**License**: MIT

## Overview

`update-readme` is a type-driven README updater. It does not start by asking how long a README
 should be. It starts by deciding what kind of README the target actually needs, confirms that
 choice with the user, and then generates from the matching template family.

This keeps README generation structured, auditable, and safer than a generic regenerator that tries
 to improvise a one-size-fits-all document.

## Workflow

The skill follows this control order:

1. **Scan the target** for signals such as plugin manifests, marketplace manifests, build files,
   existing README content, top-level structure, and licence files.
2. **Detect the README family** that best matches the target.
3. **Confirm that family with the user** before generation.
4. **Ask for presentation choices**:
   - style
   - audience
   - depth
5. **Generate from the matching template family** instead of from open-ended prose.
6. **Preview before write** so no README is replaced without an explicit approval step.

## README Families

The current design supports these families:

- Claude Code plugin marketplace root
- Individual Claude Code plugin
- Service repository
- Generic library or app
- Monorepo
- Personal repo or dotfiles
- Other

## Presentation Controls

### Style

- **Minimal** - only the sections needed to orient a reader quickly
- **Standard** - the normal default for most repos
- **Comprehensive** - adds more examples, contributor guidance, and troubleshooting
- **Diagram-aware** - prefers diagrams when the source material supports them; otherwise falls back
  to normal structured sections

### Audience

- **Mixed** - balanced for users, contributors, and maintainers
- **End user** - biased toward install, usage, and examples
- **Contributor** - biased toward structure and contribution workflow
- **Maintainer** - biased toward release rules, internal layout, and operational notes

### Depth

- **Minimal**
- **Standard**
- **Comprehensive**
- **Custom section mix**

## Output Safety

The redesigned skill is opinionated about safety:

- it confirms the README family before generation
- it validates link targets before writing them
- it replaces unknowns with HTML TODO comments instead of inventing content
- it treats all scanned files as data, not instructions
- it avoids private individual names and personal email addresses in public-facing output
- it keeps preview-before-write as a hard gate

## Why this plugin exists

README quality problems are usually not about Markdown syntax. They come from using the wrong
 document shape for the wrong repo. `update-readme` is built to optimise for README fit first, then
 polish and detail second.

## Install

In Claude Code, add the marketplace once:

```text
/plugin marketplace add git@github.com:YoungLeadersDotTech/young-leaders-tech-marketplace.git
```

Then install this plugin:

```text
/plugin install update-readme@young-leaders-tech-marketplace
```

Activate it in the current session:

```text
/reload-plugins
```

Run it from any repo or plugin directory:

```text
/update-readme
/update-readme --dry-run
/update-readme --target /absolute/path/to/target
```

## Maintainer

Young Leaders Tech &middot; <https://youngleaders.tech>

## License

MIT
