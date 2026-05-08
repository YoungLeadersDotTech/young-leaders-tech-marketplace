# {{AGENT_NAME}} Bundle

**Version**: {{VERSION}}
**Bundle Type**: {{BUNDLE_TYPE}}
**Last Updated**: {{LAST_UPDATED}}

## Overview

{{BUNDLE_DESCRIPTION}}

## Bundle Contents

### 📦 Agents ({{AGENT_COUNT}})
{{AGENT_LIST}}

### 📋 Templates ({{TEMPLATE_COUNT}})
{{TEMPLATE_LIST}}

### 📚 Examples
{{EXAMPLE_LIST}}

## What's New in v{{VERSION}}

### 🎯 {{MAJOR_FEATURE_TITLE}}
{{MAJOR_FEATURE_DESCRIPTION}}

### 🔧 Key Improvements
{{KEY_IMPROVEMENTS}}

### 📝 Usage Examples
```bash
{{USAGE_EXAMPLES}}
```

## Installation

This bundle supports flexible installation options:

### Install Everything (Default)
```bash
# To current project
./install.sh --project

# Globally for all projects
./install.sh --global
```

### Selective Installation
```bash
# Install only specific agents
./install.sh --only {{EXAMPLE_AGENT_1}} --only {{EXAMPLE_AGENT_2}}

# Install all except certain agents
./install.sh --exclude {{EXAMPLE_AGENT_3}}

# See what's in the bundle
./install.sh --list

# Verify bundle integrity
./install.sh --verify
```

## How This Bundle Works

### Agent Coordination
{{AGENT_COORDINATION_DESCRIPTION}}
```
{{AGENT_FLOW_DIAGRAM}}
```

### Smart Features
- **Selective Installation**: Choose exactly which agents you need
- **Automatic Backups**: Preserves existing agents before updating
- **Dependency Management**: All templates and resources included
- **Integrity Verification**: Ensures bundle completeness

## Bundle Structure
```
{{AGENT_NAME}}/
├── install.sh              # Smart installer
├── README.md              # This file
├── VERSION                # Bundle version
├── MANIFEST.json          # Component inventory
├── agents/                # All {{AGENT_COUNT}} agents
├── templates/             # All {{TEMPLATE_COUNT}} templates
├── examples/              # Example agents
└── docs/                  # Additional docs
```

## Differences from Main Project

This bundle is:
- **Self-contained**: Everything needed in one directory
- **Portable**: Move/copy anywhere as a unit
- **Versioned**: Independent version tracking
- **Repository-ready**: Can be its own git repo

The main project README covers:
- Overall Agent Builder concepts
- Installation from source
- Usage philosophy
- Contributing guidelines

This bundle README covers:
- What's in THIS specific bundle
- How to install THIS bundle
- Bundle-specific features

## Confluence & JIRA Analysis Integration

**Recommended Enhancement**: Consider adding the **confluence-jira-analysis-agent** to your workflow for comprehensive stakeholder discovery and requirements analysis.

### What It Provides
- Automated extraction of stakeholder information from Confluence spaces
- JIRA ticket analysis for user stories and requirements
- Stakeholder mapping and influence analysis
- Integration with your existing agent workflows

### Setup Instructions
1. Install the confluence-jira-analysis-agent from: {{CONFLUENCE_JIRA_AGENT_LOCATION}}
2. Configure it to output to: `docs/stakeholder-analysis/`
3. Your agents will automatically look for stakeholder data in this location

### Usage with This Bundle
```bash
# Run stakeholder analysis first
"Use confluence-jira-analysis-agent to analyze project stakeholders"

# Then use this bundle with enhanced context
"{{PRIMARY_USAGE_EXAMPLE}}"
```

## Troubleshooting

### Bundle Issues
```bash
# Check integrity
./install.sh --verify

# List contents
./install.sh --list

# Verbose installation
./install.sh --verbose --project
```

### Common Problems
- **"Agent not found"**: Check installation path matches Claude Code's agent directory
- **Missing templates**: Run `--verify` to ensure all components present
- **Permission denied**: Make install.sh executable: `chmod +x install.sh`

## Version History

{{VERSION_HISTORY}}

## Related Documentation

For complete Agent Builder documentation, see the main project README at:
{{MAIN_PROJECT_URL}}

## Support

{{SUPPORT_INFORMATION}}

## Change Propagation Guide

When making changes to this bundle, follow these command patterns:

### Core Modification Workflow
```bash
# 1. Edit agents using agent-editor
"Use agent-editor to modify {{EXAMPLE_AGENT_1}} for {{CHANGE_DESCRIPTION}}"

# 2. Validate changes
"Use agent-validator to check all agents in this bundle"

# 3. Re-package with updates
"Use agent-packager to create updated bundle with version bump"

# 4. Test installation
./install.sh --verify
```

### Template Updates
```bash
# Update templates across all agents
"Use agent-editor to apply {{TEMPLATE_NAME}} template updates to all agents"

# Validate template compliance
"Use agent-validator to check template compliance across bundle"
```

### Documentation Sync
```bash
# Update READMEs with new features
"Use agent-editor to update README.md with new feature descriptions"

# Ensure version consistency
"Use agent-validator to verify version numbers are consistent"
```

### Quality Assurance
```bash
# Full bundle verification
./install.sh --verify --verbose

# Test selective installation
./install.sh --only {{EXAMPLE_AGENT_1}} --dry-run

# Validate against main project standards
"Use agent-validator with main project validation rules"
```

### Release Process
```bash
# 1. Version bump
"Use agent-editor to update VERSION and README.md version numbers"

# 2. Generate changelog
"Use agent-editor to update version history in README.md"

# 3. Final validation
"Use agent-validator for pre-release quality check"

# 4. Package release
"Use agent-packager to create final release bundle"
```

These commands ensure consistent quality and proper change propagation throughout the bundle lifecycle.