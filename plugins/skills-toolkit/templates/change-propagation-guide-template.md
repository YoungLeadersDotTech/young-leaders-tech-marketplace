# Change Propagation Guide for {{PROJECT_NAME}}

**Version**: {{VERSION}}
**Last Updated**: {{LAST_UPDATED}}
**Project Type**: {{PROJECT_TYPE}}

## Overview

This guide provides standardized command patterns for propagating changes throughout the {{PROJECT_NAME}} system. Use these commands to ensure consistency, quality, and proper documentation when making modifications.

## Core Principles

1. **Always validate before propagating**: Use validation tools before applying changes
2. **Document all changes**: Maintain clear audit trails
3. **Test incrementally**: Validate each step before proceeding
4. **Maintain consistency**: Use standardized command patterns

## Command Patterns by Change Type

### 1. Agent Modifications

#### Single Agent Updates
```bash
# Edit specific agent
"Use agent-editor to modify {{EXAMPLE_AGENT_NAME}} for {{CHANGE_DESCRIPTION}}"

# Validate changes
"Use agent-validator to check {{EXAMPLE_AGENT_NAME}} compliance"

# Update documentation
"Use agent-editor to update {{EXAMPLE_AGENT_NAME}} README with changes"
```

#### Multi-Agent Updates
```bash
# Apply changes across multiple agents
"Use agent-editor to apply {{CHANGE_TYPE}} updates to all {{AGENT_CATEGORY}} agents"

# Bulk validation
"Use agent-validator to check all agents in {{PROJECT_NAME}}"

# Re-package if bundled
"Use agent-packager to create updated {{BUNDLE_NAME}} bundle"
```

### 2. Template Updates

#### Template Modifications
```bash
# Update core template
"Use agent-editor to modify {{TEMPLATE_NAME}} template for {{IMPROVEMENT_DESCRIPTION}}"

# Apply template changes to existing agents
"Use agent-editor to apply updated {{TEMPLATE_NAME}} template to all relevant agents"

# Validate template compliance
"Use agent-validator to verify template compliance across all agents"
```

#### New Template Creation
```bash
# Create new template
"Use agent-builder to create {{NEW_TEMPLATE_NAME}} template for {{PURPOSE}}"

# Apply to existing agents
"Use agent-editor to integrate {{NEW_TEMPLATE_NAME}} template into relevant agents"

# Update documentation
"Use agent-editor to update template documentation and references"
```

### 3. Documentation Updates

#### README Synchronization
```bash
# Update main README
"Use agent-editor to update main README.md with {{NEW_FEATURE_DESCRIPTION}}"

# Sync bundle READMEs
"Use agent-editor to update all bundle README.md files with version {{NEW_VERSION}}"

# Update getting started guides
"Use agent-editor to update GETTING_STARTED.md with new workflow"
```

#### Documentation Generation
```bash
# Generate API documentation
"Use {{DOCUMENTATION_AGENT}} to generate API docs for {{MODULE_NAME}}"

# Create user guides
"Use agent-builder to create user guide for {{FEATURE_NAME}}"

# Update changelog
"Use agent-editor to add version {{VERSION}} changes to CHANGELOG.md"
```

### 4. Quality Assurance

#### Pre-Release Validation
```bash
# Full system validation
"Use agent-validator to perform comprehensive quality check on {{PROJECT_NAME}}"

# Bundle integrity check
"Use agent-packager to verify all bundle manifests and dependencies"

# Installation testing
./install.sh --verify --verbose
```

#### Continuous Quality
```bash
# Daily quality check
"Use agent-validator to run daily quality assessment"

# Template compliance audit
"Use agent-validator to check template compliance across all agents"

# Performance validation
"Use {{PERFORMANCE_AGENT}} to analyze agent performance metrics"
```

### 5. Version Management

#### Version Bumps
```bash
# Minor version update
"Use agent-editor to bump version to {{NEW_VERSION}} across all components"

# Update version dependencies
"Use agent-editor to update version references in all documentation"

# Validate version consistency
"Use agent-validator to verify version consistency across project"
```

#### Release Preparation
```bash
# Prepare release notes
"Use agent-editor to generate release notes for version {{VERSION}}"

# Create release bundle
"Use agent-packager to create release bundle for version {{VERSION}}"

# Final pre-release check
"Use agent-validator to perform final release validation"
```

### 6. Integration Updates

#### External System Integration
```bash
# Update API integrations
"Use agent-editor to update {{API_NAME}} integration in {{AGENT_NAME}}"

# Add new tool integration
"Use agent-editor to add {{TOOL_NAME}} integration to {{AGENT_LIST}}"

# Validate integrations
"Use agent-validator to test all external integrations"
```

#### Cross-Project Dependencies
```bash
# Update shared components
"Use agent-editor to update shared {{COMPONENT_NAME}} across all projects"

# Sync dependency versions
"Use agent-editor to synchronize {{DEPENDENCY_NAME}} versions"

# Test dependency changes
"Use agent-validator to validate dependency compatibility"
```

## Stakeholder Analysis Integration

### Before Major Changes
```bash
# Analyze stakeholder impact
"Use confluence-jira-analysis-agent to assess stakeholder impact of {{PROPOSED_CHANGE}}"

# Review stakeholder feedback
"Use confluence-jira-analysis-agent to extract recent feedback on {{FEATURE_AREA}}"

# Update stakeholder documentation
"Use agent-editor to update stakeholder analysis in docs/stakeholder-analysis/"
```

### During Implementation
```bash
# Track stakeholder requirements
"Use confluence-jira-analysis-agent to monitor requirement changes"

# Validate against stakeholder needs
"Use agent-validator to check implementation against stakeholder requirements"

# Update stakeholder communication
"Use agent-editor to generate stakeholder update for {{CHANGE_SUMMARY}}"
```

## Troubleshooting Commands

### Common Issues
```bash
# Agent not responding correctly
"Use agent-validator to diagnose {{AGENT_NAME}} issues"

# Template conflicts
"Use agent-editor to resolve template conflicts in {{CONFLICTED_AGENTS}}"

# Bundle integrity problems
./install.sh --verify --verbose --debug
```

### Recovery Procedures
```bash
# Rollback changes
"Use agent-editor to rollback {{AGENT_NAME}} to previous version"

# Restore from backup
"Use agent-packager to restore {{COMPONENT_NAME}} from backup bundle"

# Rebuild from source
"Use agent-builder to rebuild {{AGENT_NAME}} from source templates"
```

## Best Practices

### Change Workflow
1. **Plan**: Use stakeholder analysis to understand impact
2. **Implement**: Use agent-editor for modifications
3. **Validate**: Use agent-validator for quality checks
4. **Document**: Update all relevant documentation
5. **Package**: Use agent-packager for distribution
6. **Test**: Verify installation and functionality

### Quality Gates
- All changes must pass agent-validator checks
- Documentation must be updated for user-facing changes
- Version numbers must be consistent across components
- Bundle integrity must be maintained

### Communication
- Use standardized command patterns for consistency
- Document all decisions in change logs
- Update stakeholder analysis when needed
- Maintain clear audit trails

## Emergency Procedures

### Critical Bug Fixes
```bash
# Hotfix workflow
"Use agent-editor to create hotfix for {{CRITICAL_BUG}} in {{AFFECTED_AGENT}}"
"Use agent-validator to verify hotfix doesn't introduce regressions"
"Use agent-packager to create emergency release bundle"
```

### Security Updates
```bash
# Security patch workflow
"Use agent-editor to apply security patch {{PATCH_ID}} to all affected agents"
"Use agent-validator to verify security compliance"
"Use agent-packager to create security release with expedited validation"
```

## Metrics and Monitoring

### Change Impact Assessment
```bash
# Measure change impact
"Use {{METRICS_AGENT}} to analyze impact of {{CHANGE_TYPE}} changes"

# Performance impact
"Use {{PERFORMANCE_AGENT}} to benchmark changes against baseline"

# Quality metrics
"Use agent-validator to generate quality metrics report"
```

### Success Criteria
- All validation checks pass
- Documentation is complete and accurate
- Stakeholder requirements are met
- Performance impact is within acceptable limits
- Security standards are maintained

## Related Documentation

- Main project README: {{MAIN_README_URL}}
- Agent Builder Guide: {{AGENT_BUILDER_GUIDE_URL}}
- Template Documentation: {{TEMPLATE_DOCS_URL}}
- Stakeholder Analysis Guide: {{STAKEHOLDER_GUIDE_URL}}

## Support and Escalation

For issues with change propagation:
1. Use agent-validator to diagnose problems
2. Check this guide for standard solutions
3. Consult project documentation
4. Escalate to {{ESCALATION_CONTACT}} if needed

---

**Note**: This guide is automatically updated when templates or agents change. Always use the latest version from {{GUIDE_LOCATION}}.