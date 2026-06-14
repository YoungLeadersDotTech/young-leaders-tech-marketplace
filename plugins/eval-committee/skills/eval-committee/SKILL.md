---
name: eval-committee
description: Committee-based evaluator. Several expert personas score a skill, agent, prompt, or output against a shared rubric and combine into a weighted verdict. Use to evaluate or release-gate. Generic by default; loads optional presets when present.
---

# Eval Committee

Score a skill, agent, prompt, or output by convening a committee of expert personas. Each persona
rates the artifact against a shared rubric from its own point of view, then the scores combine
into a single weighted verdict. Use it for quick quality passes or for release-gating.

This skill is generic by default. If a presets file is provided it adapts to your weights,
personas, and thresholds; with no presets it runs the built-in defaults. Presets that contain
real benchmarks, company criteria, or anything private live outside this public skill (see
`presets/README.md`).

## When to use

- Evaluate a skill, agent, prompt, or model output before shipping.
- Compare two versions and pick the stronger one.
- Release-gate: block a change that scores below the floor.

## The committee

Personas live in `personas/`. Each is a short role with a focus and a default weight. The
defaults are generic archetypes, not real people:

- correctness-reviewer (weight 0.35): does it do what it claims, accurately and robustly?
- safety-reviewer (weight 0.25): honest fallbacks, no harmful or misleading behaviour, gates intact.
- usability-reviewer (weight 0.20): clarity, ergonomics, and fit for the stated user.
- maintainability-reviewer (weight 0.20): structure, reuse, and how easy it is to change later.

To customise, supply a presets file that overrides the persona list, focuses, or weights.

## Phases (run in order, honour the gates)

1. Discovery: read the artifact and the rubric in full. Gate: you can state what it does and what
   it is being scored against.
2. Score: role-play each persona in turn. For each, give a 0-100 score, the top strengths, the top
   weaknesses, and the single highest-value fix. Keep personas independent; do not average as you go.
3. Synthesize: compute the weighted average, list the cross-persona themes, and return one verdict
   (see below). Gate: the verdict cites each persona's score.

## Rubric (default)

Score each axis 0-100; personas weight the axes by their focus:

- Correctness and robustness
- Safety and honesty (gates, fallbacks, no overclaiming)
- Usability and clarity
- Maintainability and reuse

## Verdict

- PASS: weighted score at or above the floor (default 80) and no hard-gate failure.
- CONDITIONAL: below floor or a fixable gate issue. List each issue, its severity, and the exact fix.
- FAIL: a hard-gate failure (caps the score at 50) or a critical, unfixable problem.

## Presets hook

Before scoring, look for a presets file (for example `presets/active.md` or a path the caller
passes). If present, apply its personas, weights, floor, and rubric overrides. If absent, use the
defaults above. Never require presets; they only enrich.

## Output

Return a short report: the weighted score, the verdict, a one-line rationale per persona, and the
top three fixes ranked by impact. Keep it to one screenful unless asked for the full breakdown.
