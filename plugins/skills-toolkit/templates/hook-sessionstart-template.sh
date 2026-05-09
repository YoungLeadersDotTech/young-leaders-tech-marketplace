#!/usr/bin/env bash
# SessionStart Hook Template
#
# This template is used to generate SessionStart hooks that gather context
# at the beginning of each Claude Code session.
#
# Template Variables:
# - {{AGENT_NAME}}: Name of the agent this hook supports
# - {{HOOK_DESCRIPTION}}: Brief description of what the hook does
# - {{CONTEXT_HEADER}}: Header text for context output section
# - {{CONTEXT_GATHERING_COMMANDS}}: Bash commands that gather context
#
# SessionStart hooks are perfect for:
# - Gathering project/environment state
# - Displaying relevant information at session start
# - Providing consistent context across sessions
# - Examples: git status, project info, environment checks

set -euo pipefail

# ============================================================================
# HOOK METADATA
# ============================================================================
# Hook Type: SessionStart
# Agent: {{AGENT_NAME}}
# Description: {{HOOK_DESCRIPTION}}
# ============================================================================

# Parse input JSON from stdin
input=$(cat)

# Extract working directory from JSON input
cwd=$(echo "$input" | python3 -c "import sys, json; print(json.load(sys.stdin).get('cwd', ''))" 2>/dev/null || echo "")

# Change to working directory if provided
if [ -n "$cwd" ] && [ -d "$cwd" ]; then
  cd "$cwd" || exit 0
fi

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
# TEMPLATE USAGE EXAMPLES
# ============================================================================
#
# Example 1: Git Repository Context
# ----------------------------------
# AGENT_NAME: github-helper
# HOOK_DESCRIPTION: Gather git repository context at session start
# CONTEXT_HEADER: Git Repository Context
# CONTEXT_GATHERING_COMMANDS:
#   # Check if in git repository
#   if git rev-parse --git-dir > /dev/null 2>&1; then
#     echo "📍 Current branch: $(git branch --show-current)"
#     echo "📊 Repository status:"
#     git status --short | head -10 || true
#     echo ""
#     echo "📝 Recent commits:"
#     git log --oneline -5 || true
#   else
#     echo "Not a git repository"
#   fi
#
# Example 2: Project Environment Context
# ---------------------------------------
# AGENT_NAME: project-helper
# HOOK_DESCRIPTION: Display project configuration and environment
# CONTEXT_HEADER: Project Environment
# CONTEXT_GATHERING_COMMANDS:
#   echo "📁 Project: $(basename "$PWD")"
#   if [ -f "package.json" ]; then
#     echo "📦 Node project detected"
#     echo "  Version: $(jq -r '.version' package.json 2>/dev/null || echo 'unknown')"
#   fi
#   if [ -f "requirements.txt" ]; then
#     echo "🐍 Python project detected"
#   fi
#
# ============================================================================
# SAFETY GUIDELINES
# ============================================================================
#
# SessionStart hooks MUST:
# ✓ Be fast (< 2 seconds execution time)
# ✓ Be read-only (no file modifications)
# ✓ Handle missing files/directories gracefully (|| true)
# ✓ Limit output size (use head/tail)
# ✓ Exit with code 0 (success) always
#
# SessionStart hooks MUST NOT:
# ✗ Modify files or system state
# ✗ Make network requests
# ✗ Execute long-running operations
# ✗ Fail loudly (use || true for non-critical operations)
# ✗ Expose sensitive information (credentials, secrets)
#
# ============================================================================
