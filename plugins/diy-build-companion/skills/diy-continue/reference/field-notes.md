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

## Clamping when you do not have enough clamps

Almost nobody has enough clamps. These work.

- **Gravity clamping.** Stack heavy things directly over the glue joint. A 40kg railway sleeper or
  a couple of bags of sand is an excellent clamp and costs nothing.
- **Corner bracing.** Wedge the work between two fixed surfaces and let the existing structure be
  the vice.
- **Ratchet straps** are giant clamps, and a rope with a stick twisted through it is a tourniquet
  clamp for awkward shapes.
- **Drill every pilot hole while the pieces are still flat.** Far easier than drilling vertically
  or at an angle later, and it removes most of the need to clamp during assembly.

## Keeping the workspace stable

- Trestles wobble. Clamp a heavy board across them: it makes a stable platform, doubles as the
  cutting surface, and stops the trestles walking mid-cut.
- Stand boards sideways in the trestle notches so they cannot roll. They stay sorted and you can
  pull one out without lifting the stack.
- Set the trestles in a triangle with a wall as the third point, and lean long boards against the
  wall rather than chasing them across the floor.

## Wood filler

- **Push it deep first.** Stab the filler into the hole with the tip of the putty knife rather
  than smearing it across the surface.
- **Overfill by 2-3mm.** It shrinks as it dries, and a flush fill becomes a dent.
- **One swipe to finish**, at about 45 degrees. Do not overwork it, and then walk away and leave
  it alone.
- Too much on the knife? Scrape the excess onto a second knife. One for applying, one for
  collecting, no waste.
- After about five minutes, a damp finger over the top leaves a smooth dome and saves most of the
  sanding later. Works best with water-based fillers.

## Painting and finishing

- **End grain first**, while the brush is still loaded. It drinks far more than the faces, and
  doing it last gives you dry-brush streaks.
- Prime in the morning when humidity is lower, and topcoat in the afternoon while the primer is
  tacky but no longer wet.
- Do not prime late in the day outdoors. Dew lands on a surface that has not cured and ruins it.
- A slightly damp cotton t-shirt beats a tack cloth for dust, catches what the sander missed, and
  can be washed and reused.

## Measuring and marking habits

- **The story stick.** Rather than measuring the same dimension repeatedly, mark every repeated
  measurement once on a single board and transfer the marks to each workpiece. It removes a whole
  class of measurement error, and it is faster.
- Keep the pencil and the tape in the same place every single time - the same pocket, the same
  spot on the belt. Time spent hunting for the pencil is time the cut is not getting made.

## Workshop habits worth having

- **Shadow board.** Trace the tools onto a sheet of pegboard or ply so everything has one home.
  You can see at a glance what is missing, and nothing gets stood on.
- **Sawdust is a slip hazard.** Sweep every half hour. A handful thrown onto a spill makes a
  temporary non-slip surface until you can clean it properly at the break.
- **Number the batteries** and use and charge them in rotation, so you always know which is
  freshest and never get caught with all of them flat.
- **Pre-flight each phase.** Gather every tool, material and piece of hardware, count the fixings,
  and get the safety gear on before starting. It saves the five trips back to the shed.
- **Photograph before you move or cut anything.** If the session gets interrupted, the photo tells
  you exactly where you were far better than memory does.

## Handling material efficiently

- **Flip-stack when sanding.** Sand one face of every piece, stacking each one sanded-side down.
  When the pile is done, every unsanded face is now pointing up.
- **Board butter.** Leftover mixed filler or caulk keeps far longer sandwiched between two boards.
  Pull them apart when you need it again.

## Recovering awkward situations

- **Seized clamps**: soak in penetrating oil overnight, tap with a hammer while working the jaw
  open and closed, then wire-brush the threads. Usually recoverable.
- Wrong material delivered, or stock that turns out warped: stop rather than adapting at the
  bench. A substitution made mid-build has not been through the safety gate.
