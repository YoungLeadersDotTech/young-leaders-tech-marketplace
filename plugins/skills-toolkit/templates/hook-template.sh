#!/usr/bin/env bash
# Hook Template for Agent Integration
#
# This template is used by the command-builder-agent to generate hook scripts
# that integrate agents with Claude Code's hook system.
#
# Hook Types:
# - SessionStart: Runs at the start of every Claude Code session
# - PostToolUse: Runs after specific tools are used
# - PreToolUse: Runs before specific tools are used (less common)
#
# Template Variables:
# - {{HOOK_TYPE}}: SessionStart, PostToolUse, or PreToolUse
# - {{AGENT_NAME}}: Name of the agent this hook supports
# - {{HOOK_DESCRIPTION}}: Brief description of what the hook does
# - {{HOOK_SPECIFIC_PARSING}}: JSON parsing code specific to hook type
# - {{CONTEXT_HEADER}}: Header text for context output section
# - {{CONTEXT_GATHERING_COMMANDS}}: Bash commands that gather context
#
# IMPORTANT: Hooks must be read-only and safe. Never modify files or state.

set -euo pipefail

# ============================================================================
# HOOK METADATA
# ============================================================================
# Hook Type: {{HOOK_TYPE}}
# Agent: {{AGENT_NAME}}
# Description: {{HOOK_DESCRIPTION}}
# ============================================================================

# Parse input JSON from stdin
input=$(cat)

{{HOOK_SPECIFIC_PARSING}}

# ============================================================================
# CONTEXT GATHERING
# ============================================================================

echo "=== {{CONTEXT_HEADER}} ==="
echo ""

{{CONTEXT_GATHERING_COMMANDS}}

echo ""
echo "=== End {{CONTEXT_HEADER}} ==="

# Exit successfully
exit 0

# ============================================================================
# TEMPLATE USAGE NOTES
# ============================================================================
#
# SessionStart Hook Example:
# - Gathers environment context at session start
# - Useful for providing consistent context
# - Examples: git status, project info, environment variables
#
# PostToolUse Hook Example:
# - Monitors specific tool usage
# - Provides tips or context after tool execution
# - Examples: git command suggestions, file operation feedback
#
# PreToolUse Hook Example:
# - Validates or prepares before tool execution
# - Less common, use with caution
# - Examples: permission checks, prerequisite validation
#
# Safety Guidelines:
# ✓ Only read files and gather information
# ✓ Never modify files or system state
# ✓ Always exit with code 0 (success)
# ✓ Handle errors gracefully (|| true)
# ✓ Limit output size (use head/tail)
# ✓ Be fast (avoid slow operations)
# ✗ Don't run commands that change state
# ✗ Don't execute user input unsafely
# ✗ Don't make network requests (unless read-only)
# ✗ Don't block or hang indefinitely
#
# ============================================================================
