# standalone-skills

Self-contained skills for Claude Code and Cowork. Each skill in this plugin is a contained
entity: its logic and reference files live inside its own folder, with no dependency on other
skills or plugins. That keeps them portable and Cowork-friendly.

## Skills

- **diy-build-companion** - plan and run DIY builds with energy-aware work blocks and enforced
  breaks, cross-device project state in Google Drive, and an inline child-safety veto gate.

## Install

Published in the young-leaders-tech-marketplace. Add that marketplace and install the
`standalone-skills` plugin (see the marketplace README for the exact add and install commands).
In Cowork, install from Customize then Plugins.

## Design principle

Skills here avoid cross-skill and external plugin dependencies so they run the same way whether
standalone or bundled. Any reference files a skill needs are kept inside that skill's folder.
