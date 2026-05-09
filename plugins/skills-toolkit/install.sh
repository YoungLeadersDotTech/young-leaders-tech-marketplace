#!/usr/bin/env bash
# Skills Toolkit Plugin Installer
# Version: 1.0.0

set -euo pipefail

VERSION="1.0.0"
PLUGIN_NAME="Skills Toolkit"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $*"
}

# Detect Claude Code configuration directory
detect_claude_dir() {
    local claude_dir=""

    if [[ -d "${HOME}/.claude" ]]; then
        claude_dir="${HOME}/.claude"
    elif [[ -d "${HOME}/.config/claude" ]]; then
        claude_dir="${HOME}/.config/claude"
    else
        log_error "Claude Code configuration directory not found"
        echo "Expected: ~/.claude or ~/.config/claude"
        echo "Please create the directory first or check your Claude Code installation"
        return 1
    fi

    echo "${claude_dir}"
}

# Install agents
install_agents() {
    local claude_dir="$1"
    local agents_dir="${claude_dir}/agents"

    log_step "Installing agents..."

    mkdir -p "${agents_dir}"

    cp agents/skill-creator-agent.md "${agents_dir}/"
    log_info "✓ Installed skill-creator-agent"

    cp agents/skill-validator-agent.md "${agents_dir}/"
    log_info "✓ Installed skill-validator-agent"
}

# Install commands
install_commands() {
    local claude_dir="$1"
    local commands_dir="${claude_dir}/commands"

    log_step "Installing commands..."

    mkdir -p "${commands_dir}"

    cp commands/create-skill.md "${commands_dir}/"
    log_info "✓ Installed /create-skill command"

    cp commands/validate-skill.md "${commands_dir}/"
    log_info "✓ Installed /validate-skill command"

    cp commands/list-skills.md "${commands_dir}/"
    log_info "✓ Installed /list-skills command"
}

# Install skill templates
install_skills() {
    local claude_dir="$1"
    local skills_dir="${claude_dir}/skills/shared"

    log_step "Installing skill templates..."

    mkdir -p "${skills_dir}"

    # Copy all template directories (source path is now skills/<name>/, install destination keeps the shared/ scope)
    for template_dir in skills/*/; do
        template_name=$(basename "${template_dir}")
        mkdir -p "${skills_dir}/${template_name}"
        cp -r "${template_dir}"* "${skills_dir}/${template_name}/"
        log_info "✓ Installed ${template_name}"
    done
}

# Verify installation
verify_installation() {
    local claude_dir="$1"
    local errors=0

    log_step "Verifying installation..."

    # Check agents
    if [[ ! -f "${claude_dir}/agents/skill-creator-agent.md" ]]; then
        log_error "skill-creator-agent.md not found"
        ((errors++))
    fi

    if [[ ! -f "${claude_dir}/agents/skill-validator-agent.md" ]]; then
        log_error "skill-validator-agent.md not found"
        ((errors++))
    fi

    # Check commands
    if [[ ! -f "${claude_dir}/commands/create-skill.md" ]]; then
        log_error "create-skill.md not found"
        ((errors++))
    fi

    if [[ ! -f "${claude_dir}/commands/validate-skill.md" ]]; then
        log_error "validate-skill.md not found"
        ((errors++))
    fi

    if [[ ! -f "${claude_dir}/commands/list-skills.md" ]]; then
        log_error "list-skills.md not found"
        ((errors++))
    fi

    # Check skill templates
    local template_count=$(find "${claude_dir}/skills/shared" -name "SKILL.md" 2>/dev/null | wc -l)
    if [[ ${template_count} -lt 4 ]]; then
        log_warn "Expected 4 skill templates, found ${template_count}"
    fi

    if [[ ${errors} -eq 0 ]]; then
        log_info "✓ Verification complete - all files installed correctly"
        return 0
    else
        log_error "Verification failed with ${errors} errors"
        return 1
    fi
}

# Show success message
show_success() {
    local claude_dir="$1"

    echo ""
    log_info "=========================================="
    log_info "${PLUGIN_NAME} v${VERSION} installed successfully!"
    log_info "=========================================="
    echo ""
    echo "Installed to: ${claude_dir}"
    echo ""
    echo "Components installed:"
    echo "  ✓ 2 agents (skill-creator-agent, skill-validator-agent)"
    echo "  ✓ 3 commands (/create-skill, /validate-skill, /list-skills)"
    echo "  ✓ 4 skill templates (stakeholder, ground-truth, product, initiative)"
    echo ""
    echo "Quick start:"
    echo "  1. Create your first skill:"
    echo "     /create-skill"
    echo ""
    echo "  2. Validate an existing skill:"
    echo "     /validate-skill /path/to/SKILL.md"
    echo ""
    echo "  3. List all available skills:"
    echo "     /list-skills"
    echo ""
    echo "Documentation: README.md"
    echo ""
}

# Uninstall function
uninstall() {
    local claude_dir="$1"

    log_step "Uninstalling ${PLUGIN_NAME}..."

    # Remove agents
    rm -f "${claude_dir}/agents/skill-creator-agent.md"
    rm -f "${claude_dir}/agents/skill-validator-agent.md"
    log_info "✓ Removed agents"

    # Remove commands
    rm -f "${claude_dir}/commands/create-skill.md"
    rm -f "${claude_dir}/commands/validate-skill.md"
    rm -f "${claude_dir}/commands/list-skills.md"
    log_info "✓ Removed commands"

    # Note: We don't remove skill templates as they may be in use
    log_warn "Skill templates NOT removed (may be in use)"
    log_info "To remove templates manually: rm -rf ${claude_dir}/skills/shared/*-template*"

    echo ""
    log_info "${PLUGIN_NAME} uninstalled successfully"
}

# Main installation
main() {
    echo "=========================================="
    echo "${PLUGIN_NAME} Installer v${VERSION}"
    echo "=========================================="
    echo ""

    # Check for uninstall flag
    if [[ "${1:-}" == "uninstall" ]]; then
        local claude_dir=$(detect_claude_dir) || exit 1
        uninstall "${claude_dir}"
        exit 0
    fi

    # Detect Claude directory
    log_step "Detecting Claude Code configuration..."
    local claude_dir=$(detect_claude_dir) || exit 1
    log_info "Found Claude directory: ${claude_dir}"
    echo ""

    # Install components
    install_agents "${claude_dir}"
    echo ""

    install_commands "${claude_dir}"
    echo ""

    install_skills "${claude_dir}"
    echo ""

    # Verify installation
    if verify_installation "${claude_dir}"; then
        show_success "${claude_dir}"
    else
        log_error "Installation verification failed"
        echo "Please check error messages above and try again"
        exit 1
    fi
}

# Show usage if help requested
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo "Usage: $0 [uninstall]"
    echo ""
    echo "Install or uninstall ${PLUGIN_NAME}"
    echo ""
    echo "Commands:"
    echo "  $0            Install the plugin"
    echo "  $0 uninstall  Uninstall the plugin"
    echo "  $0 --help     Show this help message"
    exit 0
fi

main "$@"
