# Field Notes (carried-over build lessons)

What actually works, gathered across the slide tower, mud kitchen, and cabinet builds. Read this
before planning any cutting or assembly.

## The assembly-line method (the big one)

Work in phases across the whole build, never piece-by-piece end-to-end:

**mark all -> cut all -> dry-fit all -> assemble all -> finish all**

- Mark every piece and verify it before any cutting starts. Never start cutting until everything
  is marked.
- Label each cut piece immediately (masking tape + marker).
- Lay all pieces out on the floor to verify against the cutting list before assembly.
- Dry-fit the entire structure before a single screw goes in. Measure the outer dimensions at the
  dry-fit stage, before committing.

## Sand before assembly, not after

The mud kitchen lesson, learned the hard way: sanding was done post-assembly, which forced an
extra grit step (80 -> 120 -> 180 instead of 120 -> 180) and made faces hard to reach. Sand
components before they go together: roughly 120 grit on the frame, 180 on surfaces that get
handled. Raise the grain with a damp wipe, let it dry, then a light final pass.

## Energy-to-task mapping

Match the task to the energy level given at the start of a work block:

| Energy level | Suitable tasks |
|---|---|
| High | Cutting, structural assembly |
| Medium | Marking, measuring, drilling |
| Low | Planning, materials check, surface prep |
| Very low | Review plans only, no tools |

Ask again after each break rather than assuming the level held. Energy after an hour of cutting is
not what it was at the start, and the afternoon slump is real. Named low-energy work that still
moves the build forward: sort and count hardware, sand edges, tidy the cut pile, read tomorrow's
step. **Ending the day early is a legitimate outcome**, not a failure, and it is a far better one
than a tired cut on a safety-critical piece.

## Work blocks and breaks

- 45-60 minute work blocks suit physical tasks.
- Warn at **40 minutes**, stop at **45** regardless of where the task has got to. Never run past
  **60 minutes** without an explicit decision to do so.
- The break itself is **15 minutes**. A **5-minute micro-break every 20-30 minutes** within a
  block keeps hands and attention fresh on repetitive cutting.
- The break is mandatory at the block boundary or at the first sign of fatigue. The phrase "just
  one more thing" is the signal that the break is already overdue, not a reason to push on.
- A real break is water, movement, stepping away. Phone-scrolling is not a break.

### Sizing the task to the time

| Task size | Duration |
|---|---|
| Micro | 5-15 min |
| Standard | 15-45 min |
| Extended | 45-60 min, then a mandatory break |

Never schedule more than 90 minutes continuous. Lead with a micro task to build momentum, and try
to **end a session on a completion rather than mid-task** - a finished piece is a far easier thing
to come back to than a half-made cut.

### Before you walk away

Make the workspace safe before the break, not after it:

- Power tools unplugged, not just switched off
- Sharp tools positioned so nothing lands on an edge
- No trip hazards across the route out
- Nothing balanced where it can fall

Then decide per tool whether it stays out for the next block or gets put away. Deciding this
explicitly is what stops the "where did I leave the driver" restart.

## Context recovery across a break or a device switch

- At the start of any session, read `state.md` before touching a tool.
- At the end, update `state.md` with the exact stopping point and the next action, and append to
  `progress-log.md`.
- Take a photo of where you stopped. Worth a thousand words on return, especially when picking the
  build back up on a different day or a different device.

## Cutting: the checklist that prevents the re-cut

Budget roughly **20-25 minutes per large panel** including setup and checking. Rushing this is
what produces the pieces that have to be cut twice.

**Before the cut**
- Measurements marked and checked against the cut list
- Stock flat and clamped, never held by hand or knee
- Blade depth set to material thickness **plus about 3mm** - deeper than that is more exposed
  blade for no benefit
- Eye and ear protection on, area clear, cable routed away from the cut line

**During the cut**
- Let the saw reach full speed before it touches the timber, about **3 seconds**
- Check you are still on the line at the midpoint rather than discovering it at the end
- Saw off and **wait for the blade to stop** before moving the piece or your hands

**After the cut**
- Measure what you actually got against what you wanted
- Label the piece immediately and move it to the done pile
- Inspect the cut edge for splintering before it goes into an assembly

### When a cut comes out wrong

| Error | What to do |
|---|---|
| Under ~3mm | Document it and carry on, if the piece is not structural or child-height |
| ~3mm to ~6mm | Stop and evaluate the safety impact before deciding; a shim or a workaround may be fine |
| Over ~6mm | Re-cut the component |

Two related rules: warped stock gets rejected and replaced rather than forced into the frame, and
if the wrong material was delivered, work stops rather than substituting on the fly. A substitution
made at the bench has not been through the safety gate.

## Timber and sheet goods: nominal versus actual

Nominal sizes are not real sizes. This is the arithmetic behind the mud kitchen height error, and
it bites any time a dimension is derived from the frame rather than measured on the finished
assembly.

| Nominal | Actual |
|---|---|
| 2x4 | 38 x 89mm |
| 2x6 | 38 x 140mm |
| 4x4 | 89 x 89mm |
| 1x6 | 19 x 140mm |

Sheet goods: 1/4in is 6mm, 1/2in is 12mm, 3/4in is 18mm. Always add the board thickness when a
worktop or platform surface sits on top of a frame.

### Plywood grade is a time decision, not just a cost one

Construction-grade ply needs roughly **3 extra hours** of sanding plus edge sealing to be
child-safe. Pre-sanded pine ply needs about **30 minutes**. For anything a child will touch or sit
on, the pre-sanded stock is worth it on splinter risk alone, before the time is even counted.

## Sourcing and tools (practical carry-overs)

Kit worth having before starting, roughly in order of need. Tier 1 is the floor for any build:
tape measure (7m or more), a spirit level (600mm or more), a square, and eye protection. Tier 2
adds a jigsaw, an orbital sander, a decent set of clamps and a stud finder. Tier 3 is table saw,
router and nail gun, none of which a first build needs.

- Structural timber: go to a builders' provider (treated, correct sections). A DIY shed is fine
  for fixings, stain, brushes, consumables, but its CLS is often untreated or the wrong dimension
  for a structural frame.
- Any time a saw blade is changed, check the rotation direction against the guard arrow before the
  first cut.
- Frame width gotcha: decide early whether legs sit inside or outside the cross members; it
  changes the outer dimension and which rails span the full width. Confirm at dry-fit.
