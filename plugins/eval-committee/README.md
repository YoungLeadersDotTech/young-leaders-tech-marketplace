# eval-committee

Committee-based evaluation for skills, agents, prompts, and outputs. Several expert personas each
score the artifact against a shared rubric, and the scores combine into one weighted verdict.

Generic by default: it runs the built-in personas and rubric, and adapts only if you supply a
presets file. Private benchmarks and company criteria stay in a private repo (see
`skills/eval-committee/presets/README.md`).

## Skills

- **eval-committee** - convene the committee, score against the rubric, return a weighted verdict.

## Install

Published in the young-leaders-tech-marketplace. Add the marketplace and install `eval-committee`.
In Cowork, install from Customize then Plugins.
