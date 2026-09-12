#!/usr/bin/env node
// audit.mjs - run the static prompt checks against a real directory on disk.
//
// Vendored from github.com/YoungLeadersDotTech/left-the-chat (skills/audit, formerly
// scripts/audit.mjs), where this and the checks it calls originate and stay the source
// of truth. It reuses inspectSetup from lib/checks.js rather than re-implementing the
// checks, so the CLI, the pre-commit hook, and the upstream web page can never drift
// into three different answers for the same input.

import { readdirSync, readFileSync, statSync } from 'node:fs'
import { join, relative } from 'node:path'
import { inspectSetup } from '../lib/checks.js'

// Same file shape the upstream page and hook look for. Kept in sync deliberately - see
// audit-staged.mjs's AGENT_FILE for the sibling definition.
const AGENT_FILE = /(^|\/)(SKILL\.md|AGENTS?\.md|CLAUDE\.md)$|(^|\/)agents\/[^/]+\.md$|(^|\/)skills\/[^/]+\.md$/
const SKIP_DIRS = new Set(['.git', 'node_modules', '.venv', 'venv', 'dist', 'build', '__pycache__'])

function walk(root, dir = root, out = []) {
  for (const entry of readdirSync(dir)) {
    if (SKIP_DIRS.has(entry)) continue
    const full = join(dir, entry)
    const rel = relative(root, full)
    const stats = statSync(full)
    if (stats.isDirectory()) walk(root, full, out)
    else if (AGENT_FILE.test(rel)) out.push({ name: rel, content: readFileSync(full, 'utf8') })
  }
  return out
}

function main(argv) {
  const target = argv[2]
  if (!target) {
    console.error('usage: audit.mjs <directory>')
    process.exit(2)
  }

  const files = walk(target)
  const { findings } = inspectSetup(files)

  if (!files.length) {
    console.log(`prompt-auditor: no SKILL.md, AGENTS.md, CLAUDE.md, agents/*.md, or skills/*.md files found under ${target}`)
    process.exit(0)
  }

  const order = { critical: 0, major: 1, minor: 2 }
  const sorted = [...findings].sort((a, b) => (order[a.severity] ?? 3) - (order[b.severity] ?? 3))

  console.log(`prompt-auditor: audited ${files.length} file(s) under ${target}`)
  console.log('')
  for (const severity of ['critical', 'major', 'minor']) {
    const group = sorted.filter((item) => item.severity === severity)
    if (!group.length) continue
    console.log(`${severity.toUpperCase()} (${group.length})`)
    for (const item of group) console.log(`  ${item.id}  ${item.title}\n      ${item.detail}`)
    console.log('')
  }

  if (!findings.length) console.log('No findings.')
  process.exit(0)
}

if (import.meta.url === `file://${process.argv[1]}`) main(process.argv)

export { walk, AGENT_FILE }
