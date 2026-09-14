# Safety Standards (inline veto gate reference)

This is the reference the safety gate (mode 5) applies. It is self-contained so the gate runs
inline on any device with no separate agent. All figures are non-negotiable minimums; when in
doubt, choose the safer option. A FAIL on child-safety or structural grounds is a hard veto.

## The five domains

A gate run checks all five and returns one verdict (PASS / CONDITIONAL / FAIL):

1. Child safety (age-specific)
2. Structural integrity (4x safety factor)
3. Tool safety and builder capability
4. Material safety and environmental hazards
5. Measurement accuracy and tolerances

---

## Domain 1: Child safety by age band

Pick the band for the youngest intended user. If a build will be used by a wide range, use the
youngest band's height and feature limits.

### Toddlers (2-3)
- Max platform height: 600mm. Max climbing height: 300mm steps.
- Full enclosure on elevated areas; constant direct supervision assumed.
- Prohibited: ropes, ladders, monkey/hanging elements, steps over 150mm rise.

### Preschool (4-5)
- Max platform height: 1200mm. Max climbing height: 1500mm with safety features.
- Guard rails 700-800mm on elevated platforms; closed stair risers; handrails both sides.
- Fall zone: 1.8m minimum radius. Impact-attenuating surface required.
- Prohibited: open-backed stairs, rope ladders, overhead elements over 1500mm.

### Elementary (6-8)
- Max platform height: 2000mm. Max climbing height: 2400mm with proper features.
- Guard rails 900-1000mm; fall zone 2.1m minimum radius; emergency egress from elevated areas.
- Prohibited: overhead elements over 2400mm, crush/pinch moving parts, sharp edges, protruding bolts.

### Pre-teen (9-12)
- Max platform height: 3000mm. Max climbing height: 3600mm with proper anchoring.
- Guard rails 1000-1100mm; multiple egress routes; fall zone 2.4m minimum radius.
- Professional structural review required for zip lines, suspended elements, heights over 3000mm,
  or complex multi-user structures.

### Entrapment limits (all ages)
- Head and limb gaps must be either under 89mm or over 229mm. Nothing in between.
- No finger-trap gaps of 5-12mm.
- No V-shaped gaps that narrow below 89mm (neck/clothing entrapment).

### Fall protection
- Minimum fall-zone radius = 2x platform height (e.g. 1200mm platform -> 2400mm radius).
- Slides: extend the fall zone 1.2m beyond the exit.
- Impact-attenuating surface (rubber mulch, wood chips, pea gravel, foam tiles) under any height
  a child can fall from.

---

## Domain 2: Structural integrity

- Apply a **4x safety factor**: a load-bearing element must be calculated to hold at least four
  times the maximum realistic load (including dynamic loads, e.g. a child jumping, not just static
  weight).
- No single point of failure on any element a child relies on to not fall.
- Verify the chosen timber section and fixings actually meet the calculated load, not just nominal
  sizing. Remember nominal vs actual dimensions (a "2x4" is 38x89mm).

## Domain 3: Tool safety and builder capability

- Check the cuts and joins the design needs against the tools on hand and the builder's stated
  proficiency. If the design needs a tool or technique the builder has not got or used, flag it
  and offer an alternative approach rather than assuming it will be fine.
- Account for any physical limitations the user has stated. Do not invent constraints that were
  not stated; do not ignore ones that were.

## Domain 4: Material safety and environmental hazards

- Prohibited outright for child use: CCA-treated lumber (arsenic), lead-containing finishes.
- Outdoor structural timber must be appropriately treated (ACQ or CA-B) or naturally durable
  (cedar, redwood). Untreated whitewood/SPF needs sealing and is not suitable structurally outdoors.
- Finishes in reach of children must be non-toxic when cured (child-safe stains/oils, food-safe
  where relevant for surfaces like a mud-kitchen worktop).
- Weatherproofing and a realistic maintenance interval for any outdoor build.

## Domain 5: Measurement accuracy and tolerances

- Safety-critical dimensions (platform heights, guard-rail heights, gap sizes): tolerance +/-1.5mm.
- Non-safety-critical dimensions: +/-3mm is fine.
- Double-check every safety-critical dimension against the relevant limit above before approving.

---

## Verdict rules

- **PASS**: every domain clear. Record date and a one-line summary per domain in `safety.md`.
- **CONDITIONAL**: one or more fixable issues. For each: the problem, its severity (CRITICAL /
  HIGH / MEDIUM), and the exact correction. Build stays blocked until fixed and re-gated to PASS.
- **FAIL**: a critical child-safety or structural hazard with no in-place fix (e.g. toxic
  material, load capacity far below the 4x factor, fall height way over the age band). Hard veto:
  record it, block the build, redesign from scratch. The user cannot override this.
