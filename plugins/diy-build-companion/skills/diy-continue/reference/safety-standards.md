# Safety Standards (inline veto gate reference)

This is the reference the safety gate (mode 5) applies. It is self-contained so the gate runs
inline on any device with no separate agent. All figures are non-negotiable minimums; when in
doubt, choose the safer option. A FAIL on child-safety or structural grounds is a hard veto.

**Scope**: this file assumes a domestic build in one household's own garden or home, and Domain 1
is built on EN 71-8, the standard for that case, with every figure cited to its clause. **If the
equipment will ever be used by people outside that household** (a shared amenity, a school, a
community space, anything semi-public), EN 71-8 no longer applies and the far stricter EN 1176/1177
(public playground equipment) governs instead. Stop and say so plainly rather than gating against
the wrong standard.

## The five domains

A gate run checks all five and returns one verdict (PASS / CONDITIONAL / FAIL):

1. Child safety (EN 71-8, domestic use - see the scope note above)
2. Structural integrity (conservative engineering convention, not a cited standard)
3. Tool safety and builder capability
4. Material safety and environmental hazards (BS EN 335 / BS 8417)
5. Measurement accuracy and tolerances

---

## Domain 1: Child safety

**Basis**: EN 71-8 (Safety of toys, Part 8: Activity toys for domestic use). This is the standard
that applies to equipment bought for one household's own garden. It stops applying the moment the
equipment serves people beyond that household (a shared amenity, a school, a public space) - at
that point **EN 1176/1177 (public playground equipment) applies instead**, which is stricter and
outside this file's scope. Every figure below is followed by the clause it comes from. Clauses not
listed here were checked and found not relevant to a typical DIY build; do not extrapolate beyond
what is cited.

**No age banding exists in this standard for height.** Earlier drafts of this file, and the older
suite it replaced, split height limits into four age bands with different figures per band. That
structure does not appear anywhere in EN 71-8: it is a single universal rule.

### Maximum height
- No part of the equipment may let a child climb, sit or stand higher than **2500mm** above the
  ground, for any age (4.1.3).
- Two structure types get their own, lower, universal figures rather than an age-scaled one:
  swings intended for under-36-months use, crossbeam at **1200mm or less** (4.6.1.3); see-saws,
  the sitting/standing point at **1200mm or less** (4.7.2); carousels and rocking toys, free
  height of fall **600mm or less** (4.8 c)).

### Platform barriers and ladders
- A platform **1000mm or more** above the ground needs a barrier, and that barrier is at least
  **600mm** high (4.2.1). Not age-scaled: this is the one figure to apply regardless of who the
  build is for.
- Ladder rungs: cross-section **16mm to 45mm** (4.2.2 e)).
- Tread or rung vertical spacing: no more than **310mm** between the upper surfaces (4.2.2 c)).
- Tread or rung lateral width: **240mm or more** (4.2.2 b)).
- Tread depth on a closed step ladder: **120mm or more** (4.2.2 f)).
- Ladder incline: between **55 and 90 degrees** to the horizontal (4.2.2 g)).
- A ladder reaching 1200mm or more needs a handrail, starting no more than 600mm above the ground
  measured to the top of the platform (4.2.2 h)).

### Slides
- The run-out (exit) section ends **300mm or less** above the ground, inclined between 0 and 10
  degrees to the horizontal (4.5.3 e)).
- Handrail height on the slide's starting section, banded by that section's own height: under
  600mm needs **100mm or more**; 600-999mm needs **150mm or more**; 1000-1799mm needs **350mm or
  more**; 1800mm or above needs **500mm or more** (4.5.3 c)).

### Entrapment
- On any opening whose lower edge is **600mm or more** above the ground: avoid a circular or
  near-circular internal diameter between **130mm and 230mm** (4.3.1 b)), and keep any V-shaped
  opening from narrowing below **60 degrees** (4.3.1 c)). This is the figure that replaces the
  old, uncited 89-229mm rule; below 600mm this specific rule does not apply, but the general
  entrapment principle still does.
- Foot entrapment on any walking surface: no gap greater than **30mm** (4.3.3).
- Finger entrapment: a rigid opening must not admit a **7mm** diameter rod to a depth of 10mm or
  more, unless a **12mm** diameter rod also passes (4.3.4). For equipment intended for under
  36 months - roughly the toddler range - the test tightens to a **5mm** rod under the same
  10mm-depth and 12mm-clearance rule (4.3.4).
- Chain openings (swing chains, cargo nets): **5mm or less** (4.6.7 d)).

### Placement
- Site the equipment at least **2m** from any structure or obstruction (5.2). EN 71-8 does not
  specify a fall-zone radius or an impact-surface depth formula for domestic equipment - that is
  an EN 1176/1177 (public playground) requirement, not a domestic one, and inventing a figure here
  would claim an authority the standard does not have.
- An impact-attenuating surface (rubber mulch, bark, sand, rubber tiles) under anything a child can
  fall from is still good practice, and is recommended for anything above the 600mm stability
  threshold below. Treat it as a sensible precaution, not a cited minimum.

### Stability
- Equipment with a free height of fall of 600mm or less is tested against one tip-over standard;
  above 600mm a different, more demanding stability test applies (4.4.2, 4.4.3). In practice: any
  freestanding structure over about 600mm needs its base, anchoring or footing sized so it cannot
  be tipped or walked over, not just so it can bear a static load.

---

## Domain 2: Structural integrity

**Not covered by EN 71-8.** A toy safety standard regulates the toy's own dimensions and
mechanical hazards, not structural load design for a DIY-built garden structure - there is no
single domestic standard that plays the role EN 71-8 plays for Domain 1. What follows is
conservative engineering convention, stated as such rather than dressed up with a citation it
does not have.

- Apply a **4x safety factor**: a load-bearing element should be sized to hold at least four times
  the maximum realistic load, including dynamic loads (a child jumping, not just standing weight).
  This is standard conservative practice for structures built without individual engineering
  sign-off, not a figure taken from EN 71-8 or any cited regulation. Being a convention rather
  than a citation does not make it optional: apply it as strictly as any of the cited figures
  above.
- **State the calculated factor explicitly before recording a verdict, do not eyeball it.** Show
  the working: maximum realistic dynamic load, the section and material's actual load capacity,
  and the resulting multiple. "Roughly fine" is not a calculation. A design that comes out under
  4x is CONDITIONAL at best - strengthen the element or reduce the span - and a design with no
  credible path to 4x on a genuinely load-bearing, child-relied-upon element is a FAIL, not a
  judgement call to talk around.
- No single point of failure on any element a child relies on to not fall.
- Verify the chosen timber section and fixings actually meet the calculated load, not just nominal
  sizing. Remember nominal vs actual dimensions (a "2x4" is 38x89mm).
- The stability test referenced in Domain 1 (EN 71-8 4.4.2/4.4.3) is the closest this build gets
  to a cited structural requirement, and it covers tip-over resistance, not load capacity.

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

- Eye protection to **EN ISO 16321** (the current EU/Irish eye-protection standard, superseding
  the older EN 166 - check the marking on the glasses themselves, both still appear on the shelf),
  for every cutting, drilling and sanding operation
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

**Basis**: BS EN 335 (use classes, what governs which treatment a piece of timber needs for where
it goes) and BS 8417 (the code of practice that pairs a use class with a treatment and a desired
service life). These are the UK/Irish equivalents of the American treatment codes an earlier
version of this file used, which a merchant here would not recognise.

### Specify by use class, not by product code

Ask for timber treated to the use class the piece actually needs, not by a named chemical:

| Use class | Situation | Typical build application |
|---|---|---|
| UC1 | Internal, no risk of water contact | Not relevant outdoors |
| UC2 | Internal, risk of water contact | Not relevant outdoors |
| UC3.1 | External, above ground, dries quickly | Vertical cladding, rails that shed water |
| UC3.2 | External, above ground, stays wet | Horizontal surfaces, anything water can pool on |
| UC4 | External, in contact with the ground or fresh water | Posts set in or against soil, any below-grade element |
| UC5 | Permanent seawater contact | Not relevant to a garden build |

Any post going into the ground, or any timber touching soil, needs **UC4** at minimum. Above-ground
structural framing that stays dry-ish needs **UC3**, and 3.2 rather than 3.1 if it is horizontal or
otherwise holds water. BS 8417 sets the desired service life against the use class - 15 years is
the common default for a garden structure, 30 for something meant to last longer.

Naturally durable species (cedar, redwood) can substitute for treatment at the equivalent
durability class without chemical preservative, and remain a valid choice regardless of
jurisdiction. Untreated whitewood or SPF is UC1/UC2 material: it needs sealing and is not suitable
as structural timber outdoors regardless of finish.

### Prohibited and restricted

- CCA-treated lumber (chromated copper arsenate): prohibited for anything a child will be near.
  Its residential use is restricted at EU regulatory level, and a merchant here should not be
  selling it for a domestic build in the first place - if it turns up in reclaimed or old stock,
  treat it as a hard no regardless of source.
- Lead-containing finishes: prohibited outright.
- Finishes in reach of children must be non-toxic when cured (child-safe stains and oils, food-safe
  where relevant, e.g. a mud-kitchen worktop).
- A realistic maintenance interval for any outdoor build, and reapply finish before it fails
  rather than after.

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
  material, a load-bearing element with no credible path to the calculated 4x factor, height over
  the 2500mm universal cap, or the build turning out to be for shared/public use, which needs
  EN 1176 rather than this file). Hard veto: record it, block the build, redesign from scratch.
  The user cannot override this.

## What to keep as a record

`safety.md` holds the gate record itself. Two things are worth keeping alongside it on a build a
child will use:

- **Receipts for structural timber, fixings and finishes.** These are the only durable proof that
  what went into the build is what was approved at the gate. A year on, nobody remembers whether
  the decking screws were the exterior-rated ones.
- **Photographs during assembly**, particularly of connections that end up hidden. When a
  structure is inspected or modified later, buried fixings are otherwise guesswork.
