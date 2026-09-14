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

Check the cuts and joins the design needs against the tools actually on hand and the builder's
stated proficiency. If the design needs a tool or technique they have not got or used, flag it and
offer an alternative approach rather than assuming it will be fine.

**If the build repo has a `reference/tool-inventory.md`, read it before asking what tools are on
hand.** A useful inventory records the tool, its condition, and the details that change a cut: the
actual model, blade kerf, battery state. Keep it as a table so a half-filled row still reads
cleanly, and treat an empty condition column as unknown rather than as "does not own it".

Never require the file. With no inventory, ask, and do not create one unprompted - a fabricated
tool list is worse than none, because this domain would then check the design against a fiction.
If the design needs a tool that is not listed, say so and offer the alternative rather than
assuming it will be bought.

This file belongs to the builder's own repo and never to this plugin, so an inventory is never
published with the skill. Whether to commit it is the owner's choice: tracked in a private repo,
ignored in a public one.

### Tool risk tiers

| Tier | Tools | Conditions and protocol |
|---|---|---|
| **Very high** | Chainsaw, angle grinder, concrete saw | Beyond most home builds. Flag explicitly and offer an alternative approach before assuming it goes ahead. |
| **High** | Circular saw, table saw | Stable work surface, two-handed operation, deliberate stance. Material clamped before the cut, no awkward reaches, power disconnected between cuts. |
| **Medium** | Drill/driver, jigsaw, reciprocating saw, belt sander | Proper grip, stable positioning, clear workspace. Depth stops set, guards in place. |
| **Low** | Hand saw, chisel, screwdriver, measuring and marking tools | Keep edges sharp (a blunt chisel slips), standard hand-tool technique, stored safely between uses. |

### Builder capability

Match the tier to stated experience rather than assuming. A beginner is a confident hand-tool and
drill user; intermediate adds a jigsaw and circular saw with guided cuts; advanced covers table
saw, router and freehand circular work. A design needing a tier above the builder's stated level
is a flag, not a fail: offer the alternative (a hand saw and a guide rail instead of a table saw,
pre-cut stock from the merchant instead of ripping sheet goods).

### Required safety equipment

Check these are present before any cutting starts, not once it has:

- Eye protection to **ANSI Z87.1** or equivalent, for every cutting, drilling and sanding operation
- Hearing protection for any tool over **85dB** (most power saws and routers)
- Dust mask or respirator for sanding, and for cutting treated lumber in particular
- Gloves for material handling, **not** for power tools - a glove caught in a rotating blade pulls
  the hand in, which is why this one is stated as a prohibition rather than a recommendation
- Stable work surface or sawhorses, so nothing is cut freehand or against the knee
- First aid kit accessible on site

### Stated physical limitations

Account for any limitation the builder has stated. Do not invent constraints that were not stated,
and do not quietly ignore ones that were. Where a limitation affects the work, accommodate rather
than refuse: raise the work to standing height on sawhorses or a bench instead of kneeling, use a
wheeled cart rather than carrying, split a lift that needs two people, and build a rest into the
work block rather than pushing through.

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

### Practices that prevent the errors

- Measure twice, cut once, and work from a consistent reference point rather than measuring from
  the last cut. Measuring from the previous piece is how tolerance accumulates.
- Verify square with the 3-4-5 method rather than trusting a framing square on a large assembly.
- Account for material thickness explicitly. A worktop height derived from the frame alone is
  wrong by the thickness of the board that goes on top, which is the single most common way a
  child-height dimension drifts out of band.
- Test-fit before final assembly. Dry-fit the whole thing before a single screw goes in.

### Red flags on measurement

- A safety-critical dimension taken once and never checked.
- Imprecision in the stated dimension itself ("about three feet") on anything load-bearing or
  child-height.
- Accumulating error across a multi-step build, where each piece is measured from the last.
- No cut list. If the pieces have not been written down with dimensions before cutting starts,
  the cut list is being held in someone's head and it will drift.

---

## Verdict rules

- **PASS**: every domain clear. Record date and a one-line summary per domain in `safety.md`.
- **CONDITIONAL**: one or more fixable issues. For each: the problem, its severity (CRITICAL /
  HIGH / MEDIUM), and the exact correction. Build stays blocked until fixed and re-gated to PASS.
- **FAIL**: a critical child-safety or structural hazard with no in-place fix (e.g. toxic
  material, load capacity far below the 4x factor, fall height way over the age band). Hard veto:
  record it, block the build, redesign from scratch. The user cannot override this.

## What to keep as a record

`safety.md` holds the gate record itself. Two things are worth keeping alongside it on a build a
child will use:

- **Receipts for structural timber, fixings and finishes.** These are the only durable proof that
  what went into the build is what was approved at the gate. A year on, nobody remembers whether
  the decking screws were the exterior-rated ones.
- **Photographs during assembly**, particularly of connections that end up hidden. When a
  structure is inspected or modified later, buried fixings are otherwise guesswork.
