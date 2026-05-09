#!/usr/bin/env bash
# PostToolUse Hook Template
#
# This template is used to generate PostToolUse hooks that monitor specific
# tool usage and provide contextual feedback after tool execution.
#
# Template Variables:
# - {{AGENT_NAME}}: Name of the agent this hook supports
# - {{HOOK_DESCRIPTION}}: Brief description of what the hook does
# - {{TARGET_TOOL}}: Tool name to monitor (e.g., "Bash", "Write", "Edit")
# - {{PATTERN_MATCHING}}: Bash code to check if tool usage matches patterns
# - {{CONTEXT_MESSAGE}}: Message to display when pattern matches
#
# PostToolUse hooks are perfect for:
# - Monitoring specific tool usage patterns
# - Providing tips after tool execution
# - Suggesting agent alternatives to manual operations
# - Examples: git command monitoring, file operation tracking

set -euo pipefail

# ============================================================================
# HOOK METADATA
# ============================================================================
# Hook Type: PostToolUse
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
# For Bash tool: get the command that was executed
if [ "$tool_name" = "Bash" ]; then
  tool_input=$(echo "$input" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tool_input', {}).get('command', ''))" 2>/dev/null || echo "")
fi

# For Write/Edit tools: get the file path
if [ "$tool_name" = "Write" ] || [ "$tool_name" = "Edit" ]; then
  tool_input=$(echo "$input" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tool_input', {}).get('file_path', ''))" 2>/dev/null || echo "")
fi

# ============================================================================
# PATTERN MATCHING
# ============================================================================

{{PATTERN_MATCHING}}

# ============================================================================
# CONTEXTUAL OUTPUT
# ============================================================================

# If pattern matched, provide context
if [ "$pattern_matched" = "true" ]; then
  echo ""
  echo "{{CONTEXT_MESSAGE}}"
  echo ""
fi

# Exit successfully
exit 0

# ============================================================================
# TEMPLATE USAGE EXAMPLES
# ============================================================================
#
# Example 1: Git Command Monitoring
# ----------------------------------
# AGENT_NAME: github-helper
# HOOK_DESCRIPTION: Monitor git commands and suggest agent alternatives
# TARGET_TOOL: Bash
# PATTERN_MATCHING:
#   pattern_matched="false"
#   if echo "$tool_input" | grep -qE "^git (commit|add|push|pull)"; then
#     pattern_matched="true"
#   fi
# CONTEXT_MESSAGE:
#   💡 Tip: The @github-helper agent can help with git operations!
#   Try: /git-commit, /git-sync, or /git-push for assisted workflows.
#
# Example 2: Large File Write Monitoring
# ---------------------------------------
# AGENT_NAME: file-helper
# HOOK_DESCRIPTION: Warn about large file writes
# TARGET_TOOL: Write
# PATTERN_MATCHING:
#   pattern_matched="false"
#   if [ -n "$tool_input" ] && [ -f "$tool_input" ]; then
#     file_size=$(stat -f%z "$tool_input" 2>/dev/null || stat -c%s "$tool_input" 2>/dev/null || echo "0")
#     if [ "$file_size" -gt 1000000 ]; then  # > 1MB
#       pattern_matched="true"
#     fi
#   fi
# CONTEXT_MESSAGE:
#   ⚠️  Large file detected (>1MB). Consider:
#   - Breaking into smaller files
#   - Using streaming for large datasets
#   - Checking if this should be gitignored
#
# Example 3: Test File Edit Monitoring
# -------------------------------------
# AGENT_NAME: test-helper
# HOOK_DESCRIPTION: Suggest running tests after test file edits
# TARGET_TOOL: Edit
# PATTERN_MATCHING:
#   pattern_matched="false"
#   if echo "$tool_input" | grep -qE "\.(test|spec)\.(js|ts|py)$"; then
#     pattern_matched="true"
#   fi
# CONTEXT_MESSAGE:
#   🧪 Test file modified! Consider running tests:
#   - npm test (for JS/TS)
#   - pytest (for Python)
#   - Or use @test-helper for guided test execution
#
# ============================================================================
# SAFETY GUIDELINES
# ============================================================================
#
# PostToolUse hooks MUST:
# ✓ Be fast (< 1 second execution time)
# ✓ Be read-only (no file modifications)
# ✓ Handle parsing errors gracefully
# ✓ Exit with code 0 always (never block execution)
# ✓ Provide helpful, actionable suggestions
#
# PostToolUse hooks MUST NOT:
# ✗ Modify files or system state
# ✗ Make network requests
# ✗ Execute commands from user input unsafely
# ✗ Block or delay tool execution
# ✗ Produce excessive output (keep it concise)
#
# ============================================================================
