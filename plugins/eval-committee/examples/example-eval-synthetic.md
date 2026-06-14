# Eval run: example-widget-skill (synthetic)

- Date: 2026-01-01
- Artifact: skills/example-widget-skill/SKILL.md (fictional, for illustration)
- Floor: 80

## Persona scores

| Persona | Score | Top strength | Top weakness | Highest-value fix |
|---|---|---|---|---|
| correctness-reviewer | 88 | handles missing input cleanly | one claim not covered by the body | add the missing branch or trim the claim |
| safety-reviewer | 82 | honest manual fallback | no check before claiming a write | confirm the write tool exists first |
| usability-reviewer | 90 | clear trigger description | example is a little long | trim the example to one screen |
| maintainability-reviewer | 79 | generic core | presets mixed into the body | move presets to a separate file |

## Weighted score

85.1 / 100  (0.35 x 88 + 0.25 x 82 + 0.20 x 90 + 0.20 x 79)

## Verdict

PASS (at or above the floor of 80, no hard-gate failure)

## Top fixes (ranked)

1. Confirm the write tool exists before claiming a write (safety).
2. Move presets out of the body into a separate file (maintainability).
3. Align the description claims with what the body does (correctness).
