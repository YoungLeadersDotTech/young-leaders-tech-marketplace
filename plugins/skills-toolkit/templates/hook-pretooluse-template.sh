#!/usr/bin/env bash
# PreToolUse Hook Template
#
# This template is used to generate PreToolUse hooks that validate or prepare
# before tool execution. Use these sparingly as they can interrupt workflow.
#
# Template Variables:
# - {{AGENT_NAME}}: Name of the agent this hook supports
# - {{HOOK_DESCRIPTION}}: Brief description of what the hook does
# - {{TARGET_TOOL}}: Tool name to intercept (e.g., "Bash", "Write", "Edit")
# - {{VALIDATION_LOGIC}}: Bash code to validate tool usage
# - {{BLOCK_MESSAGE}}: Message to display if blocking execution (optional)
#
# PreToolUse hooks are perfect for:
# - Validating prerequisites before execution
# - Warning about potentially destructive operations
# - Checking permissions or file existence
# - Examples: permission checks, destructive operation warnings
#
# ⚠️  WARNING: Use PreToolUse hooks sparingly!
# They can interrupt user workflow and should only be used when absolutely necessary.

set -euo pipefail

# ============================================================================
# HOOK METADATA
# ============================================================================
# Hook Type: PreToolUse
# Agent: {{AGENT_NAME}}
# Description: {{HOOK_DESCRIPTION}}
# Target Tool: {{TARGET_TOOL}}
# ============================================================================

# Parse input JSON from stdin
input=$(cat)

# Extract tool name from JSON input
tool_name=$(echo "$input" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tool_name', ''))" 2>/dev/null || echo "")

# Only process {{TARGET_TOOL}} tool calls
if [ "$tool_name" != "{{TARGET_TOOL}}" ]; then
  exit 0
fi

# ============================================================================
# TOOL INPUT PARSING
# ============================================================================

# Extract tool-specific parameters from input
# For Bash tool: get the command that will be executed
if [ "$tool_name" = "Bash" ]; then
  tool_input=$(echo "$input" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tool_input', {}).get('command', ''))" 2>/dev/null || echo "")
fi

# For Write/Edit tools: get the file path
if [ "$tool_name" = "Write" ] || [ "$tool_name" = "Edit" ]; then
  tool_input=$(echo "$input" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tool_input', {}).get('file_path', ''))" 2>/dev/null || echo "")
fi

# ============================================================================
# VALIDATION LOGIC
# ============================================================================

{{VALIDATION_LOGIC}}

# ============================================================================
# EXIT CODE CONTROL
# ============================================================================

# Exit codes for PreToolUse hooks:
# 0 = Allow tool execution (pass through)
# 2 = Block tool execution and show stderr to Claude
#
# IMPORTANT: Only use exit code 2 when absolutely necessary!
# Blocking execution disrupts user workflow.

# Exit successfully by default (allow execution)
exit 0

# ============================================================================
# TEMPLATE USAGE EXAMPLES
# ============================================================================
#
# Example 1: Warn About Destructive Git Operations
# -------------------------------------------------
# AGENT_NAME: github-helper
# HOOK_DESCRIPTION: Warn before destructive git operations
# TARGET_TOOL: Bash
# VALIDATION_LOGIC:
#   # Check for destructive git operations
#   if echo "$tool_input" | grep -qE "git (reset --hard|clean -fd|push --force)"; then
#     echo "⚠️  WARNING: Potentially destructive git operation detected!" >&2
#     echo "Command: $tool_input" >&2
#     echo "" >&2
#     echo "This operation cannot be undone. Consider using:" >&2
#     echo "- @github-helper for safer git workflows" >&2
#     echo "- /git-sync for complete synchronization" >&2
#     echo "" >&2
#     # Just warn, don't block (exit 0)
#   fi
#
# Example 2: Validate File Permissions Before Write
# --------------------------------------------------
# AGENT_NAME: file-helper
# HOOK_DESCRIPTION: Check file permissions before writing
# TARGET_TOOL: Write
# VALIDATION_LOGIC:
#   if [ -f "$tool_input" ] && [ ! -w "$tool_input" ]; then
#     echo "❌ ERROR: File is not writable: $tool_input" >&2
#     echo "Check file permissions with: ls -la $tool_input" >&2
#     exit 2  # Block execution
#   fi
#
# Example 3: Prevent Accidental System File Modification
# -------------------------------------------------------
# AGENT_NAME: safety-helper
# HOOK_DESCRIPTION: Prevent modification of critical system files
# TARGET_TOOL: Edit
# VALIDATION_LOGIC:
#   # Check if editing critical system files
#   if echo "$tool_input" | grep -qE "^/etc/|^/sys/|^/proc/"; then
#     echo "🛑 BLOCKED: Attempted to edit system file: $tool_input" >&2
#     echo "Editing system files is not allowed for safety." >&2
#     exit 2  # Block execution
#   fi
#
# ============================================================================
# SAFETY GUIDELINES
# ============================================================================
#
# PreToolUse hooks MUST:
# ✓ Be extremely fast (< 500ms execution time)
# ✓ Be read-only (no file modifications)
# ✓ Handle parsing errors gracefully
# ✓ Use exit code 2 ONLY when absolutely necessary
# ✓ Provide clear, actionable error messages
#
# PreToolUse hooks MUST NOT:
# ✗ Block execution except for critical safety issues
# ✗ Modify files or system state
# ✗ Make network requests
# ✗ Execute user input unsafely
# ✗ Be overly restrictive (frustrates users)
#
# WHEN TO USE PreToolUse hooks:
# ✓ Preventing data loss or corruption
# ✓ Checking critical prerequisites
# ✓ Enforcing security policies
#
# WHEN NOT TO USE PreToolUse hooks:
# ✗ Providing tips or suggestions (use PostToolUse instead)
# ✗ Monitoring usage patterns (use PostToolUse instead)
# ✗ Enforcing style preferences (too intrusive)
#
# ============================================================================
