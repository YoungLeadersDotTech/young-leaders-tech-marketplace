---
description: Install a kitted macOS terminal (Ghostty, Oh My Zsh, Powerlevel10k, Glow, optional markdown-preview kit). Idempotent.
---

# /terminal-setup-install

Run the `terminal-setup-install` skill end-to-end: preflight, install the core stack,
ask about optional markdown-preview extras, configure everything, sanity-test.

The skill is idempotent. Tools you already have will be skipped. Your existing
`~/.zshrc` customisations are preserved (backed up to `~/.zshrc.pre-oh-my-zsh`).

Invoke the `terminal-setup-install` skill from this plugin directly.
