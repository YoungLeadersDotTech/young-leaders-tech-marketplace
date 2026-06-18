# Skills Toolkit for Claude Code

**Version**: 2.0.6
**Author**: Young Leaders Tech
**License**: MIT

## Overview

`skills-toolkit` is the authoring + validation plugin for Claude Code skills and agents in this marketplace. It ships four agents (skill-creator, skill-validator, agent-author, agent-validator), three slash commands, four reusable shared-skill templates, thirteen agent and infrastructure templates, and a marketplace-guidelines reference doc that the validator agents cite when reporting findings.

## What's Included

### 4 Intelligent Agents

#### skill-creator-agent
Interactive guide for creating Claude Code skill files (SKILL.md):
- 5-phase creation workflow
- Description engineering (WHEN + WHEN NOT triggers, <=250-char cap)
- PII validation
- Template-based structure generation
- Task* progress tracking

#### skill-validator-agent
Read-only professional validator for skills:
- YAML frontmatter and markdown structure
- Description quality scoring
- PII detection (emails, phones, secrets)
- Claude Code ecosystem compatibility

#### agent-author (NEW in 2.0.0)
End-to-end agent authoring with three modes selected via AskUserQuestion at session start:
- `create`: build a new subagent from scratch
- `edit`: modify an existing agent file
- `package`: bundle a validated agent with install.sh and MANIFEST.json
Six-phase lifecycle (Analyse, Design, Generate, Bundle, Validate, Document). Replaces the legacy three-agent agent-builder + agent-editor + agent-packager chain.

#### agent-validator (NEW in 2.0.0)
Validates Claude Code subagent files against `references/marketplace-guidelines.md`. Six-phase lifecycle. Reports findings with severity (BLOCKER, WARNING, INFO) and section citation. Auto-detects bundle and plugin context for cross-file consistency checks.

### 3 Slash Commands

#### `/create-skill`
Launch the interactive skill creation workflow:
```
/create-skill stakeholder
/create-skill ground-truth
/create-skill product
/create-skill initiative
```

The skill-creator-agent guides you through requirements gathering, description engineering, structure generation, and validation.

#### `/validate-skill`
Validate existing skills for quality and security:
```
/validate-skill /path/to/SKILL.md
```

Get comprehensive reports with:
- Structure validation (YAML, markdown)
- Content quality scoring
- PII detection results
- Actionable recommendations
- Severity classifications (PASS/NEEDS IMPROVEMENT/FAIL)

#### `/list-skills`
Discover available skills organized by scope:
```
/list-skills
```

Shows personal, project, and shared skills with metadata.

### 4 Shared Skill Templates (`skills/`)

Reusable scaffolds for new skills you author. Each ships description-engineering guidance, placeholder structures, validation checklists, security guidelines, and worked examples.

#### Stakeholder Template
For team/person context on specific projects:
- Roles, goals, pain points
- Communication preferences
- Decision-making patterns

#### Ground Truth Template
For verifiable, canonical reference documentation:
- Canonical definitions
- Verified facts and metrics
- Process flows and state machines
- Validation criteria
- Error codes and messages

#### Product Context Template
For product vision, goals, and constraints:
- Vision and mission
- Target users and personas
- Goals and success metrics
- Features and capabilities
- UX principles

#### Initiative Overview Template
For cross-functional initiative coordination:
- Charter and scope
- Work streams and milestones
- Cross-team coordination
- Dependencies and risks
- Status tracking

### 13 Agent and Infrastructure Templates (`templates/`)

Ready-to-crib templates `agent-author` consumes during create / package modes:

| Template | Purpose |
|---|---|
| `claude-subagent-template.md` | Canonical agent .md frontmatter + body skeleton |
| `portable-agent-template.md` | Standalone agent for use outside a plugin |
| `install-script-template.sh` | Smart install.sh with --global / --project / --sync-back |
| `bundle-readme-template.md` | Auto-generated bundle README |
| `hook-template.sh` | Generic hook skeleton |
| `hook-sessionstart-template.sh` | SessionStart hook |
| `hook-pretooluse-template.sh` | PreToolUse hook |
| `hook-posttooluse-template.sh` | PostToolUse hook |
| `agent-coordination-template.md` | Multi-agent coordination patterns |
| `change-propagation-guide-template.md` | Versioning across cross-agent dependencies |
| `agent-builder-logging-template.md` | Logging skeleton for agent operations |
| `validation-checklist-template.md` | Reusable validation gates |
| `structured-choice-template.md` | AskUserQuestion patterns |

### Reference: `references/marketplace-guidelines.md`

Single ground-truth doc that `agent-validator` and `skill-validator-agent` cite. Codifies:
- 5-file rule (CHANGELOG, VERSION, plugin.json, marketplace.json, README)
- Semver decision table
- Same-commit ordering rule
- Two version fields (top-level + plugin entry)
- CHANGELOG format (Keep a Changelog)
- Frontmatter description cap (<=250 chars)
- Em-dash ban (U+2014)
- Migration pattern (global skill -> plugin skill)
- Claude Code plugin schema reference
- Severity taxonomy (BLOCKER / WARNING / INFO)

### Examples (`examples/`)

- `sample-subagent.md`: a minimal working agent file you can copy and rename.
- `sample-portable-agent/`: a standalone agent bundle (instructions + README).

## Install

In Claude Code, add the marketplace once (SSH form - see [root README](../../README.md#quick-install) for HTTPS and other options):

```text
/plugin marketplace add git@github.com:YoungLeadersDotTech/young-leaders-tech-marketplace.git
```

Then install this plugin:

```text
/plugin install skills-toolkit@young-leaders-tech-marketplace
```

Activate in the current session:

```text
/reload-plugins
```

### Verify install

```text
/list-skills
```

You should see the four shared skill templates plus the plugin's commands and agents available.

## Quick Start

### Create Your First Skill

```
/create-skill stakeholder
```

The skill-creator-agent will guide you through:
1. **Requirements Gathering** - Define skill name, scope, and purpose
2. **Description Engineering** - Craft WHEN/WHEN NOT triggers
3. **Structure Generation** - Generate SKILL.md with proper format
4. **Validation** - Check for PII, quality, and security
5. **Finalization** - Get complete, ready-to-use SKILL.md

### Validate Existing Skills

```
/validate-skill ~/.claude/skills/projects/my-project/SKILL.md
```

Get a comprehensive report:
- Overall status (PASS/NEEDS IMPROVEMENT/FAIL)
- Detailed findings by domain
- Actionable recommendations
- Severity classifications

### Browse Available Skills

```
/list-skills
```

See all your skills organized by:
- Personal skills (`~/.claude/skills/personal/`)
- Project skills (`.claude/skills/projects/`)
- Shared templates (`.claude/skills/`)

## Key Features

### Description Engineering

The toolkit guides you to create high-quality skill descriptions with:

**WHEN Triggers** - Specific terms users will mention:
- Project/product names
- Domain keywords
- Use case terms

**WHEN NOT Exclusions** - Prevent contamination:
- Related but different projects
- General discussions
- Other teams/products

**Example**:
```yaml
description: Stakeholder context for Apollo UX research when discussing user testing, research synthesis, or design validation. Auto-invoke when user mentions Apollo, UX research stakeholders, or design team. Do NOT load for general UX discussions unrelated to Apollo.
```

### PII Protection

Automatic detection of:
- Email addresses
- Phone numbers
- SSN/sensitive identifiers
- Personal names (contextual)

All templates include security checklists to ensure zero PII in skill content.

### Quality Validation

Multi-domain validation:
1. **Structure**: YAML frontmatter, markdown formatting
2. **Content**: Clarity, completeness, professionalism
3. **Technical**: Tool selection, capabilities, error handling
4. **Security**: PII detection, confidential data, allowed-tools

### Hybrid Pattern Architecture

Commands follow the proven hybrid pattern:
- **Agents analyze**: Read files, validate, generate recommendations
- **Main Claude executes**: Write files, display reports, apply fixes
- **Clear separation**: Agent analyzes → Main Claude executes → Changes happen

## Usage Examples

### Example 1: Create Stakeholder Skill

```
User: /create-skill stakeholder

skill-creator-agent: Let's create a stakeholder skill. What project is this for?

User: Apollo UX Research

skill-creator-agent: Great! What specific areas should this skill cover?

User: User testing, research synthesis, design validation

skill-creator-agent: Perfect. What terms should trigger this skill?

User: Apollo, UX research, design team

[Agent guides through description engineering, structure generation, validation]

skill-creator-agent: ✅ Skill creation complete!
File: .claude/skills/projects/apollo/stakeholders/SKILL.md
Validation: PASSED (95/100)

Main Claude: [Writes SKILL.md file to specified location]
```

### Example 2: Validate Before Production

```
User: /validate-skill .claude/skills/projects/apollo/stakeholders/SKILL.md

skill-validator-agent:
================================================================================
SKILL VALIDATION REPORT
================================================================================

Overall Status: ✓ PASS

Structure: ✓ PASS
Content Quality: ✓ PASS (92/100)
Security: ✓ PASS (Zero PII detected)
Integration: ✓ PASS

Recommendation: Production-ready. Optional improvements available.
================================================================================
```

### Example 3: Browse All Skills

```
User: /list-skills

Output:
Personal Skills (2):
└── user-manual/ - Work preferences and communication style
└── learning-goals/ - Current learning objectives

Project Skills (3):
└── apollo/stakeholders/ - Apollo UX research team context
└── checkout/ground-truth/ - Payment processing error codes
└── pricing/initiative/ - Pricing innovation initiative overview

Shared Templates (4):
└── stakeholder-templates/ - Template for stakeholder skills
└── ground-truth-template/ - Template for ground truth skills
└── product-context-template/ - Template for product context skills
└── initiative-overview-template/ - Template for initiative skills
```

## Best Practices

### When to Use Each Template

**Stakeholder Template**: Use when you need context about specific teams, roles, or people on a project
- Team objectives and decision patterns
- Communication preferences
- Pain points and success metrics

**Ground Truth Template**: Use for verifiable facts and canonical reference data
- Error codes and definitions
- Process flows and state machines
- Validation criteria and business rules
- Metrics and verified facts

**Product Context Template**: Use for product vision and strategic context
- Product goals and constraints
- Target users and personas
- Feature capabilities
- UX principles

**Initiative Template**: Use for cross-functional coordination
- Initiative charters and scope
- Work streams and milestones
- Dependencies and risks
- Status tracking

### Description Quality Tips

**DO**:
- ✅ Include specific trigger terms
- ✅ Add explicit WHEN NOT boundaries
- ✅ Use possessive pronouns for personal skills
- ✅ Quantify metrics (">95% accuracy" not "high accuracy")

**DON'T**:
- ❌ Use generic descriptions ("Provides information about...")
- ❌ Skip WHEN NOT exclusions
- ❌ Include PII (names, emails, phones)
- ❌ Mix scopes (keep personal/project/shared separate)

### Security Guidelines

**Always**:
- Use roles instead of names ("Product Owner" not "Jane Smith")
- Use placeholders for sensitive data (`[STAKEHOLDER_NAME]`)
- Set `allowed-tools: []` for reference skills
- Review skills for business-confidential information

**Never**:
- Include emails, phone numbers, or SSN
- Include specific revenue/budget numbers
- Include unreleased features or roadmaps
- Mix personal information with team context

## Troubleshooting

### Agent Not Responding

**Problem**: Agent doesn't respond to tag
**Solution**:
```bash
# Verify installation
ls ~/.claude/agents/skill-creator-agent.md
ls ~/.claude/agents/skill-validator-agent.md

# Restart Claude Code if needed
```

### Command Not Found

**Problem**: Slash command not recognized
**Solution**:
```bash
# Verify command installation
ls ~/.claude/commands/create-skill.md
ls ~/.claude/commands/validate-skill.md
ls ~/.claude/commands/list-skills.md

# Restart Claude Code to reload commands
```

### Template Not Loading

**Problem**: Template referenced but not found
**Solution**:
```bash
# Verify templates installed
ls ~/.claude/skills/

# Should show:
# - stakeholder-templates/
# - ground-truth-template/
# - product-context-template/
# - initiative-overview-template/
```

### Validation Errors

**Problem**: Skill validation reports errors
**Solution**: Review the validation report for specific issues:
- **PII detected**: Remove emails, phones, names
- **Description quality low**: Add WHEN/WHEN NOT patterns
- **Structure issues**: Check YAML frontmatter syntax
- **Security concerns**: Review allowed-tools and confidential data

## Integration with Other Tools

### Works With

- **Claude Code**: All versions with skill support
- **Git**: Version control for skill files
- **Markdown editors**: Edit skills with any markdown editor
- **CI/CD**: Integrate `/validate-skill` in pipelines

### Future Integrations

- Marketplace publishing (when available)
- Team collaboration features
- Automated freshness checking
- Usage analytics

## Technical Details

### Dependencies

**Required**:
- Claude Code with skills support
- Read, Grep, Glob, TaskCreate, TaskUpdate, TaskGet, TaskList tools

**Optional**:
- Git (for version control)
- jq (for JSON processing)

### Compatibility

- **Platform**: macOS, Linux, Windows (WSL)
- **Claude Code Version**: All versions with skill support
- **Shell**: bash, zsh

### Performance

- **Skill Creation**: ~2-5 minutes with interactive guidance
- **Validation**: ~5-30 seconds per skill
- **Template Loading**: Instant

## Support & Contributing

### Getting Help

1. Review this README and troubleshooting section
2. Check validation reports for specific guidance
3. Review template examples and usage patterns
4. Open an issue on GitHub (if applicable)

### Reporting Issues

When reporting issues, include:
- Claude Code version
- Operating system
- Complete error message or validation report
- Steps to reproduce
- Expected vs actual behavior

### Contributing

Contributions welcome! Consider:
- New skill templates
- Validation improvements
- Documentation enhancements
- Bug fixes and optimizations

## Version History

Current: **v2.0.4** (2026-05-09).

For full release notes across all versions see [CHANGELOG.md](./CHANGELOG.md).
Highlights:

- **v2.0.4** - flat plugin source layout (`skills/<name>/`, no more `skills/shared/` wrapper)
- **v2.0.3** - alphabetised `plugin.json` arrays; `disable-model-invocation: true` on all four templates; cited Anthropic 250-char source in `marketplace-guidelines.md`
- **v2.0.2** - canonical tools registry alignment in `agent-validator`; added missing `AskUserQuestion` to `skill-creator-agent`
- **v2.0.1** - reverted (over-permissioning antipattern, see CHANGELOG)
- **v2.0.0** - merged former agent-builder/editor/packager into `agent-author`, added `agent-validator`, `references/marketplace-guidelines.md`, 13 templates, `examples/`
- **v1.0.0** - initial release

## License

MIT License - See LICENSE file for details

## Credits

**Created by**: Young Leaders Tech
**Powered by**: Claude Code

---

**Ready to create professional, production-ready Claude Code skills with automated validation and quality assurance.**
