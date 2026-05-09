#!/bin/bash
# Install Script Template for Agent Bundles
#
# This template provides the standard structure for agent bundle installation scripts.
# The agent-packager should generate install.sh files following this template pattern.
#
# Key Features:
# - Bidirectional sync capabilities (--sync-back, --check-versions)
# - Version conflict detection with timestamp comparison
# - Global/project installation modes
# - Bundle information display from MANIFEST.json
# - Colored output and professional UX
# - Safety checks and confirmation prompts

set -euo pipefail

# ============================================================================
# CONFIGURATION SECTION
# ============================================================================

# Bundle metadata (populate from MANIFEST.json during generation)
BUNDLE_NAME="{{AGENT_NAME}}"
BUNDLE_VERSION="{{VERSION}}"
BUNDLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Components to install (populate from bundle contents)
declare -a AGENTS=(
    "{{AGENT_NAME}}:{{AGENT_DESCRIPTION}}"
    # Add additional agents if bundle contains multiple
)

declare -a TEMPLATES=(
    # List all templates included in bundle
    {{TEMPLATE_LIST}}
)

# ============================================================================
# COLOR CONFIGURATION
# ============================================================================

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    echo -e "${2}${1}${NC}"
}

# ============================================================================
# BUNDLE INFORMATION DISPLAY
# ============================================================================

# Display bundle details from MANIFEST.json
display_bundle_info() {
    echo ""
    print_color "📦 Bundle Information:" "$CYAN"
    if [[ -f "$BUNDLE_DIR/MANIFEST.json" ]]; then
        local version=$(grep -o '"version": "[^"]*"' "$BUNDLE_DIR/MANIFEST.json" | cut -d'"' -f4)
        local agent_count=$(grep -c '"name"' "$BUNDLE_DIR/MANIFEST.json" | head -1)
        local template_count=$(grep -o '"templates": \[.*\]' "$BUNDLE_DIR/MANIFEST.json" | grep -o '"' | wc -l | awk '{print $1/2}')

        # Count commands and hooks from MANIFEST.json
        local command_count=0
        local hook_count=0
        if grep -q '"commands"' "$BUNDLE_DIR/MANIFEST.json"; then
            command_count=$(grep -A 100 '"commands"' "$BUNDLE_DIR/MANIFEST.json" | grep -c '"name"' | head -1)
        fi
        if grep -q '"hooks"' "$BUNDLE_DIR/MANIFEST.json"; then
            hook_count=$(grep -A 50 '"hooks"' "$BUNDLE_DIR/MANIFEST.json" | grep -c '"type"' | head -1)
        fi

        echo "  • Version: $version"
        echo "  • Agents: $agent_count included"
        echo "  • Templates: $template_count"
        [[ $command_count -gt 0 ]] && echo "  • Commands: $command_count"
        [[ $hook_count -gt 0 ]] && echo "  • Hooks: $hook_count"
    else
        echo "  • Version: $BUNDLE_VERSION (MANIFEST.json not found)"
    fi
    echo ""
}

# ============================================================================
# VERSION COMPARISON FUNCTIONS
# ============================================================================

# Get file modification time (cross-platform)
get_file_time() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        echo "0"
        return
    fi

    # Try GNU stat first (Linux), then BSD stat (macOS)
    stat -c "%Y" "$file" 2>/dev/null || stat -f "%m" "$file" 2>/dev/null || echo "0"
}

# Compare versions between bundle and installed
compare_versions() {
    local bundle_file="$1"
    local installed_file="$2"

    if [[ ! -f "$bundle_file" ]]; then
        echo "missing_source"
        return
    fi

    if [[ ! -f "$installed_file" ]]; then
        echo "new"
        return
    fi

    local bundle_time=$(get_file_time "$bundle_file")
    local installed_time=$(get_file_time "$installed_file")

    if [[ $bundle_time -gt $installed_time ]]; then
        echo "newer"
    elif [[ $installed_time -gt $bundle_time ]]; then
        echo "older"
    else
        echo "same"
    fi
}

# ============================================================================
# SYNC-BACK FUNCTIONS
# ============================================================================

# Sync changes from installed location back to bundle
sync_back_to_bundle() {
    print_color "🔄 Syncing changes back to bundle..." "$YELLOW"
    local sync_count=0
    local skip_count=0

    # Sync agents
    for agent_info in "${AGENTS[@]}"; do
        IFS=':' read -r agent_name agent_desc <<< "$agent_info"
        local bundle_agent="$BUNDLE_DIR/agents/${agent_name}.md"
        local installed_agent="$TARGET_DIR/agents/${agent_name}.md"

        if [[ -f "$installed_agent" ]]; then
            local status=$(compare_versions "$bundle_agent" "$installed_agent")

            case "$status" in
                "older")
                    print_color "  ← Syncing $agent_name (installed is newer)" "$GREEN"
                    cp "$installed_agent" "$bundle_agent"
                    ((sync_count++))
                    ;;
                "newer")
                    print_color "  ↷ Skipping $agent_name (bundle is newer)" "$YELLOW"
                    ((skip_count++))
                    ;;
                "same")
                    [[ "$VERBOSE" == true ]] && print_color "  = $agent_name (already in sync)" "$BLUE"
                    ;;
            esac
        else
            print_color "  ✗ $agent_name not found in installation" "$RED"
        fi
    done

    # Sync templates if they exist
    if [[ ${#TEMPLATES[@]} -gt 0 ]]; then
        for template in "${TEMPLATES[@]}"; do
            local bundle_template="$BUNDLE_DIR/templates/$template"
            local installed_template="$TARGET_DIR/templates/$template"

            if [[ -f "$installed_template" ]]; then
                local status=$(compare_versions "$bundle_template" "$installed_template")

                case "$status" in
                    "older")
                        print_color "  ← Syncing template $template" "$GREEN"
                        cp "$installed_template" "$bundle_template"
                        ((sync_count++))
                        ;;
                    "newer")
                        [[ "$VERBOSE" == true ]] && print_color "  ↷ Skipping template $template" "$YELLOW"
                        ((skip_count++))
                        ;;
                esac
            fi
        done
    fi

    echo ""
    print_color "✅ Sync complete: $sync_count files updated, $skip_count skipped" "$GREEN"
}

# ============================================================================
# CHECK VERSIONS MODE
# ============================================================================

# Check and report version status without making changes
check_versions() {
    display_bundle_info

    print_color "📊 Version Status Report" "$CYAN"
    print_color "========================" "$CYAN"
    echo ""

    local newer_count=0
    local older_count=0
    local same_count=0
    local new_count=0

    # Check agents
    for agent_info in "${AGENTS[@]}"; do
        IFS=':' read -r agent_name agent_desc <<< "$agent_info"
        local bundle_agent="$BUNDLE_DIR/agents/${agent_name}.md"
        local installed_agent="$TARGET_DIR/agents/${agent_name}.md"
        local status=$(compare_versions "$bundle_agent" "$installed_agent")

        echo -n "$agent_name: "
        case "$status" in
            "newer")
                print_color "Bundle is NEWER ↑" "$YELLOW"
                ((newer_count++))
                ;;
            "older")
                print_color "Installed is NEWER ⚠️" "$RED"
                ((older_count++))
                ;;
            "same")
                print_color "In sync ✓" "$GREEN"
                ((same_count++))
                ;;
            "new")
                print_color "Not installed +" "$BLUE"
                ((new_count++))
                ;;
        esac
    done

    echo ""
    echo "Summary:"
    [[ $new_count -gt 0 ]] && echo "  • $new_count new files to install"
    [[ $newer_count -gt 0 ]] && echo "  • $newer_count files to update (bundle newer)"
    [[ $older_count -gt 0 ]] && print_color "  • $older_count files where installed is newer" "$YELLOW"
    [[ $same_count -gt 0 ]] && echo "  • $same_count files already in sync"

    if [[ $older_count -gt 0 ]]; then
        echo ""
        print_color "⚠️  Some installed files are newer than bundle" "$YELLOW"
        echo "   Use --sync-back to update bundle with installed changes"
    fi
}

# ============================================================================
# INSTALLATION FUNCTIONS
# ============================================================================

# Install with version checking
install_with_check() {
    local force_install="${1:-false}"

    # Check for version conflicts unless force is enabled
    if [[ "$force_install" != "true" ]]; then
        local conflicts=0

        for agent_info in "${AGENTS[@]}"; do
            IFS=':' read -r agent_name agent_desc <<< "$agent_info"
            local bundle_agent="$BUNDLE_DIR/agents/${agent_name}.md"
            local installed_agent="$TARGET_DIR/agents/${agent_name}.md"
            local status=$(compare_versions "$bundle_agent" "$installed_agent")

            if [[ "$status" == "older" ]]; then
                print_color "⚠️  Warning: $agent_name installed version is newer" "$YELLOW"
                ((conflicts++))
            fi
        done

        if [[ $conflicts -gt 0 ]]; then
            echo ""
            read -p "Overwrite newer installed files? [y/N] " -n 1 -r
            echo ""
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                print_color "Installation cancelled" "$YELLOW"
                exit 0
            fi
        fi
    fi

    # Proceed with installation
    perform_installation
}

# Perform the actual installation
perform_installation() {
    print_color "📦 Installing $BUNDLE_NAME..." "$CYAN"

    # Create directories
    mkdir -p "$TARGET_DIR/agents"
    [[ ${#TEMPLATES[@]} -gt 0 ]] && mkdir -p "$TARGET_DIR/templates"

    # Install agents
    for agent_info in "${AGENTS[@]}"; do
        IFS=':' read -r agent_name agent_desc <<< "$agent_info"
        print_color "  → Installing $agent_name" "$GREEN"
        cp "$BUNDLE_DIR/agents/${agent_name}.md" "$TARGET_DIR/agents/"
    done

    # Install templates
    if [[ ${#TEMPLATES[@]} -gt 0 ]]; then
        for template in "${TEMPLATES[@]}"; do
            print_color "  → Installing template: $template" "$GREEN"
            cp "$BUNDLE_DIR/templates/$template" "$TARGET_DIR/templates/"
        done
    fi

    # Install commands if present
    if [[ -d "$BUNDLE_DIR/.claude/commands" ]] && [[ -n "$(ls -A "$BUNDLE_DIR/.claude/commands" 2>/dev/null)" ]]; then
        print_color "  → Installing slash commands..." "$GREEN"
        mkdir -p "$TARGET_DIR/commands"
        cp -r "$BUNDLE_DIR/.claude/commands/"* "$TARGET_DIR/commands/" 2>/dev/null || true
        local cmd_count=$(ls -1 "$BUNDLE_DIR/.claude/commands" | wc -l | tr -d ' ')
        print_color "    Installed $cmd_count command(s)" "$BLUE"
    fi

    # Install hooks if present
    if [[ -d "$BUNDLE_DIR/.claude/hooks" ]] && [[ -n "$(ls -A "$BUNDLE_DIR/.claude/hooks" 2>/dev/null)" ]]; then
        print_color "  → Installing hooks..." "$GREEN"
        mkdir -p "$TARGET_DIR/hooks"
        cp -r "$BUNDLE_DIR/.claude/hooks/"* "$TARGET_DIR/hooks/" 2>/dev/null || true
        chmod +x "$TARGET_DIR/hooks/"*.sh 2>/dev/null || true
        local hook_count=$(ls -1 "$BUNDLE_DIR/.claude/hooks" | wc -l | tr -d ' ')
        print_color "    Installed $hook_count hook(s)" "$BLUE"
    fi

    print_color "✅ Installation complete!" "$GREEN"
    display_bundle_info
}

# ============================================================================
# MAIN SCRIPT LOGIC
# ============================================================================

# Parse command line arguments
MODE="install"
TARGET_MODE=""
FORCE=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --global|-g)
            TARGET_MODE="global"
            shift
            ;;
        --project|-p)
            TARGET_MODE="project"
            shift
            ;;
        --sync-back)
            MODE="sync"
            shift
            ;;
        --check-versions)
            MODE="check"
            shift
            ;;
        --force|-f)
            FORCE=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            cat << EOF
Usage: $0 [OPTIONS]

Options:
  --global, -g         Install globally to ~/.claude
  --project, -p        Install to current project .claude
  --sync-back          Sync changes from installed back to bundle
  --check-versions     Check version status without changes
  --force, -f          Force operation without confirmations
  --verbose, -v        Show detailed output
  --help, -h           Show this help message

Examples:
  $0 --global              # Install globally
  $0 --check-versions      # Check version status
  $0 --sync-back           # Update bundle from installed
  $0 --global --force      # Force global install
EOF
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Determine target directory if not set
if [[ -z "$TARGET_MODE" ]]; then
    if [[ "$MODE" != "check" ]]; then
        echo "Select installation target:"
        echo "1) Global (~/.claude)"
        echo "2) Project (./.claude)"
        read -p "Choice [1-2]: " choice

        case "$choice" in
            1) TARGET_MODE="global" ;;
            2) TARGET_MODE="project" ;;
            *) echo "Invalid choice"; exit 1 ;;
        esac
    else
        TARGET_MODE="global"  # Default for check mode
    fi
fi

# Set target directory
if [[ "$TARGET_MODE" == "global" ]]; then
    TARGET_DIR="$HOME/.claude"
else
    TARGET_DIR="$(pwd)/.claude"
fi

# Execute based on mode
case "$MODE" in
    "sync")
        sync_back_to_bundle
        ;;
    "check")
        check_versions
        ;;
    "install")
        install_with_check "$FORCE"
        ;;
esac