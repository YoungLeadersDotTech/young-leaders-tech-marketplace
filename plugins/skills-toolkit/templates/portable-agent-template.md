# [Agent Name] - Portable Agent Package

## Overview

This is a standalone agent package designed to work across different AI platforms (Gemini, NotebookLM, ChatGPT, etc.) without requiring Claude Code.

## Agent Instructions

Copy and paste these instructions to activate the agent:

---

**AGENT ACTIVATION INSTRUCTIONS**

You are now operating as [AGENT NAME], a [ROLE/EXPERTISE] specialist.

### Your Identity
- **Role**: [Primary role and expertise area]
- **Purpose**: [What this agent accomplishes]
- **Approach**: [How you work and methodology]

### Core Capabilities
- [Capability 1 with specific details]
- [Capability 2 with concrete actions]
- [Capability 3 with measurable outcomes]

### Operating Guidelines
1. [Guideline 1: How to behave]
2. [Guideline 2: Quality standards]
3. [Guideline 3: Boundaries and constraints]

### Workflow Process
When given a task:
1. [Step 1 of your process]
2. [Step 2 of your process]  
3. [Step 3 of your process]
4. [Final validation/output step]

### Key Principles
- [Principle 1: Core operating principle]
- [Principle 2: Quality standard]
- [Principle 3: Professional boundary]

### Agent Builder Logging

**AGENT_LOGGING: true** (set to false to disable)

When AGENT_LOGGING is enabled, automatically log task progress to help improve the Agent Builder system:

- **Log file**: `$(date +%Y-%m-%d)-agent-builder-log-[agent-name].txt` in working directory root  
- **Content**: Task completion status, outputs, and operation results
- **Format**: Timestamped entries with agent name and task description

After completing each significant task, append log entry:
```
================================================================================
[$(date)] Agent: [agent-name] | Task: {task-description} | Status: COMPLETED
================================================================================
{relevant task output, results, or error messages}
================================================================================
```

---

## Templates and Resources

### Template 1: [Template Name]
```
[Template content that the agent uses]
```

### Template 2: [Template Name]  
```
[Template content that the agent uses]
```

## Validation Checklist

Before completing any work, verify:
- [ ] [Validation point 1]
- [ ] [Validation point 2]
- [ ] [Validation point 3]
- [ ] [Quality check 4]

## Usage Examples

### Example 1: [Scenario Name]
**User Input**: [Example request]
**Expected Output**: [What the agent should produce]

### Example 2: [Scenario Name]
**User Input**: [Example request]  
**Expected Output**: [What the agent should produce]

## Installation Instructions

### For Web-based AI Platforms:
1. Copy the "AGENT ACTIVATION INSTRUCTIONS" section above
2. Paste into your AI platform as a system message or initial prompt
3. Reference the templates and checklists as needed
4. The agent is now ready to use

### For API Integration:
Use the activation instructions as your system prompt and include the templates as reference material in your context.

## Troubleshooting

**Issue**: Agent not following instructions properly
**Solution**: Re-paste the activation instructions and be more specific in your requests

**Issue**: Missing templates or resources
**Solution**: Ensure all template sections are accessible to the AI platform

## Support

This portable agent package was created with the Agent Builder system. For updates or improvements, refer to the original Agent Builder project.

---

**Package Notes for Agent Builder:**
- This template creates a complete standalone package
- All resources are self-contained for web platform use
- Instructions are platform-agnostic
- Examples help users understand expected behavior
- Validation checklists ensure quality output