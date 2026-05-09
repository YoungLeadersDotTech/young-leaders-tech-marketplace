---
description: List available skills with organized structure showing personal, project, and shared skills
---

List all available Claude Code skills with clear scope organization.

**Steps:**
1. Check for personal skills in `~/.claude/skills/personal/`
2. Check for project skills in `.claude/skills/projects/`
3. Check for shared skills in `.claude/skills/shared/`
4. Display organized tree structure with skill metadata
5. Show skill name, category, and description for each

**Output Format:**
```
Personal Skills (count):
└── skill-name/ (category) - Brief description

Project Skills (count):
└── project-name/
    └── skill-name/ (category) - Brief description

Shared Skills (count):
└── category/
    └── skill-name/ - Brief description
```

**Note:** This command executes directly without invoking an agent. Use `--all` flag to show all scopes, or specify scope with `--personal`, `--project`, or `--shared`.
