# SketchUp MCP tips

Patterns for any build that models in SketchUp via MCP (`eval_ruby` / `export_scene` against a
live SketchUp document), harvested from real building sessions so the next one doesn't relearn
this the hard way. Read this alongside `field-notes.md` when a project's 3D design work goes
through SketchUp rather than sketches or a CAD file.

## Setup

Community project `github.com/mhyrr/sketchup-mcp` (SketchupMCP) is the one that actually works
from Claude Code - the official Trimble "SketchUp Connector for Claude" is claude.ai-only
(web/desktop), not usable from Claude Code, and generation-only even there.

**Recommended: install the `diy-sketchup-mcp` plugin.** It registers this MCP server for you
(pinned `sketchup-mcp==0.1.17` and `mcp[cli]<2`, registered only while that plugin is enabled).
Its README covers prerequisites, the `.rbz` install, a verify step and the `eval_ruby` trust
guidance. If you previously registered the server by hand, `claude mcp remove sketchup` first.

**Fallback, manual install**: from a clone, `uv tool install --with "mcp[cli]<2" .`, then
register it with `claude mcp add`. Always pin `mcp[cli]<2` - the published PyPI package's
unpinned `mcp[cli]>=1.3.0` dependency resolves to a breaking mcp 2.x by default.

First call of a session can throw one `-32601 Method not found`: the server opens a connection at
session start and sends nothing, SketchUp's main thread blocks waiting on it, and the first tool
call sends a `ping` the Ruby extension doesn't handle. Expect at most one per fresh
session/reconnect; retry once. It also means SketchUp was frozen until that first call, and any
other Claude Code session with the plugin enabled holds SketchUp the same way - model in one
session at a time.

Root cause of the flakiness below, from reading upstream code (`su_mcp/main.rb`,
`sketchup_mcp/server.py` 0.1.17): SketchUp serves one request per connection and then closes it,
while the Python server reuses its socket. A "Connection closed before receiving any data" failure
therefore never reached SketchUp and is safe to retry; a 15-second timeout may have executed, so
check-read before retrying that one.

Managing multiple email addresses for test/trial accounts on any tool (not SketchUp-specific): see
[this post on Gmail plus-addressing](https://www.youngleaders.tech/p/johns-tips-2024w4-use-plus-addressing-to-get-unlimited-email-addresses-a3a90968db2d) -
one mailbox, unlimited addresses.

## Connection flakiness - the actual triage order

**Quantified from one real build's audited session log: 42.2% of all `eval_ruby` calls (156 of
370) failed with "Connection closed before receiving any data."** This is a genuine external
MCP-bridge reliability problem (see the connection-lifetime root cause above), not a usage
mistake - budget for isolated single failures rather than debugging each one, but treat the same
call failing 3+ times in a row as a real signal (see below). Every one of those failures was an isolated
single retry (never two in a row) because a verification read was interleaved before each retry -
that discipline is what keeps a baseline failure rate this high from turning into compounding
confusion about what state the model is actually in.

`Communication error with Sketchup: Connection closed before receiving any data` on one call,
next call succeeding, is routine - retry once without investigating.

If the SAME call keeps failing 3+ times in a row while unrelated reads succeed fine, check these
in order before assuming it's random:

1. **A UI element is physically blocking the click target** - a measurement/dimension line, an
   open dialog (a subscription/license popup is a real recurring one), or another 3D object
   sitting in front of the piece being written to (a large prop, an appliance) can silently block
   writes at that specific spot while everything else works. Confirmed cause more than once. Check
   for anything on-screen at that location before retrying blindly for the 5th time.
2. **Corrupted geometry from an earlier interrupted write** - the tell is a specific object's
   `.bounds` (or any other normally-safe read) reliably failing on every retry while `.bounds`
   works fine on every *other* object, and `.valid?`/`.entities.count` still work on the suspect
   object. This means a transform got interrupted mid-write and left it corrupted. Don't keep
   retrying the same read/transform - erase the object and rebuild it from scratch with
   `entities.add_group` + `add_face` + `pushpull` at the known-good coordinates instead.
3. **Genuinely down** - `'NoneType' object has no attribute 'get'` immediately followed by
   `Could not connect to Sketchup` means the bridge itself is down. Report plainly, don't keep
   retrying.

If none of the above and it's still just failing/succeeding randomly: it's ordinary flakiness.
Standing rule: move or create **one piece per `eval_ruby` call**, even mid-flaky-stretch where
batching several pieces per call is tempting to speed things up. Before every retry, re-read the
target's current state first - if unchanged from before the failure, it's safe to retry the exact
same write; if it already changed in an ambiguous way, resolve that before proceeding rather than
blindly re-running the same call. If a spot keeps failing at 5+ retries even after checking for
obstructions, try a different position on the same piece (e.g. a different x/z offset) rather than
only ever retrying the identical call - a spot-specific obstruction sometimes only affects part of
the piece's face.

## File identity - check every session, and after every export

`export_scene` always writes a NEW temp copy under `/var/folders/.../T/sketchup_exports/`, and -
confirmed root cause, not user error - calling `export_scene` makes SketchUp itself open that
temp copy as the new active document, exactly like "Save As" happened underneath you. Check
`Sketchup.active_model.path` before editing, every session, and immediately after any export.

**Fix, don't just ask the user to reopen**: after export, `cp` the newest file in the temp export
dir back onto the tracked repo path (this actually persists the session's changes - skipping this
step means `Sketchup.open_file` below reopens the OLD file and silently discards everything done
since the last real save), then call `Sketchup.open_file(<tracked path>)` via `eval_ruby` to snap
the active document back. Confirmed working repeatedly. Do this proactively after every export,
not reactively once a drift is noticed.

## Camera / screenshot gotchas

`Sketchup.active_model.active_view.camera` defaults to **parallel/orthographic projection**
(`camera.perspective? == false`) on a fresh model load. In that mode, `camera.fov = N` is a
silent no-op and `camera.set(eye, target, up)` will not honour the eye/target points passed -
SketchUp recalculates an eye position to fit some internal default distance, which looks like the
call was simply ignored (values come back close to but not matching what was set). Fix:
`view.camera.perspective = true` **before** calling `camera.set`/`camera.fov`, every time a
specific framed shot is needed rather than the default overview.

`view.zoom(N)` expects a `Sketchup::Entity` (or array of entities) to zoom to fit, not a numeric
zoom factor - passing a plain number raises `wrong argument type (expected Sketchup::Entity)`.
There's no simple "zoom by factor N" call; frame the shot via `camera.set` + `camera.fov` instead.

`view.zoom_extents` can blow up to a huge, wrong bounding box if any stray far-away geometry
exists in the model (see the garbage-bounds bug below) - fix stray geometry first, or set the
camera manually.

## Text labels on a piece's face (add_3d_text)

Real signature: `add_3d_text(text, alignment, fontname, bold, italic, letterheight, tolerance, z,
filled, extrusion)` - the **2nd argument is text alignment** (e.g. `TextAlignLeft`), NOT the font
name. Passing a font-name string there throws `TypeError: no implicit conversion of String into
Integer`. Needs at least 3 args or raises `ArgumentError: Need at 3 arguments`.

The call returns a **Boolean**, not a Group - the glyphs land as loose `Face`/`Edge` entities
directly in `model.entities`. Capture them immediately with
`model.entities.select { |e| e.is_a?(Sketchup::Face) || e.is_a?(Sketchup::Edge) }` and wrap with
`model.entities.add_group(loose)` to get a real, positionable/nameable group. Any stray loose
geometry already sitting in entities (e.g. from a previous failed attempt) gets swept up by that
same select - clear it first if unsure what's already there.

For unfilled single-stroke/outline lettering (not solid block letters): `filled=false,
extruded=false, extrusion=0.0`, and a bigger `letterheight` (e.g. 22-30mm) reads better at a
glance than the tiny filled-block default.

**Orienting the label to read correctly on a face whose outward normal is +Y** (e.g. a piece's
room-facing front face): center the text at local origin first (translate by
`-(min+size/2)` in x and y), then apply
`Geom::Transformation.rotation(ORIGIN, Geom::Vector3d.new(0,1,1), 180.degrees)`. This one
180-degree rotation about the diagonal axis bisecting +Y and +Z gives normal=+Y, up=+Z, right=+X
all correctly, as a **proper rotation** (no mirroring, no reversed string needed). A naive
-90-degree rotation about the X axis alone gets the face normal right but leaves the text
upside-down and, as a side effect of the wrong 180-degree net rotation, also reading in reverse
order - confirmed by direct visual inspection of a real SketchUp document, not just assumed from
the math.

**Vertical boards** (studs, jack studs) read better with the label rotated another 90 degrees so
the text runs up the board length instead of straight across a narrow face - add
`Geom::Transformation.rotation(ORIGIN, Geom::Vector3d.new(0,1,0), -90.degrees)` applied *after*
the orientation rotation above (i.e. `pos * inplane_rotation * orientation_rotation * pre`).

Full working example (label reads correctly, right-side up, on a +Y-normal face):
```ruby
model.entities.add_3d_text("F-SILL2", TextAlignLeft, "Arial", false, false, 22.mm, 0.0, 0.0, false, 0.0)
loose = model.entities.select { |e| e.is_a?(Sketchup::Face) || e.is_a?(Sketchup::Edge) }
lbl = model.entities.add_group(loose)
b = lbl.bounds
w = b.max.x - b.min.x
h = b.max.y - b.min.y
pre = Geom::Transformation.translation(Geom::Vector3d.new(-(b.min.x + w/2.0), -(b.min.y + h/2.0), 0))
rot = Geom::Transformation.rotation(ORIGIN, Geom::Vector3d.new(0,1,1), 180.degrees)
pos = Geom::Transformation.translation(Geom::Vector3d.new(cx, y_face + 0.5.mm, cz))
lbl.transform!(pos * rot * pre)
```

## Rebuild-in-place helper pattern (rebuild_z)

Define once per session, reuse for the rest of it - erases and recreates a box-shaped piece at a
new z-range rather than transforming it in place. Prefer rebuild-from-scratch over patching in
place for anything more than a trivial move, since a half-applied transform is what causes the
corrupted-geometry failure mode above:
```ruby
def rebuild_z(model, code, z0, z1)
  target = nil
  model.entities.each { |x| target = x if x.is_a?(Sketchup::Group) && x.name.to_s.start_with?("[#{code}]") }
  # capture x/y bounds + material from target before erasing, then add_face + pushpull at z0..z1
end
```

## affine(group, a, b) helper for z-transforms

```ruby
def affine(group, a, b)
  group.transform!(Geom::Transformation.translation([0,0,b.m]) * Geom::Transformation.scaling(ORIGIN,1,1,a))
end
```
Computes `z_new = a*z_old + b`. Anchored-floor compression: `b=0`. Pure shift: `a=1.0`. General
remap: `a=(new_max-new_min)/(old_max-old_min)`, `b=new_min-a*old_min`. Same pattern works for
x-axis scaling.

## Known bugs worth knowing before you hit them

- **`Group#name=` renames the shared ComponentDefinition, not just that instance.** Using
  `entities.add_instance(group.definition, group.transformation)` to "duplicate" a group and then
  renaming one of the two instances renames BOTH (they share one definition) - and further
  transforms compound the confusion into garbage-bounds geometry. Don't duplicate a group intended
  to be transformed independently this way; erase + rebuild both from scratch instead.
- **`make_box`-style pushpull direction bug**: with a face's normal forced to +z via
  `face.reverse! if face.normal.z < 0`, a NEGATIVE pushpull distance extrudes DOWNWARD from z0
  (landing at `[z0-(z1-z0), z0]` instead of `[z0, z1]`), not upward as expected. Fix: use a
  POSITIVE pushpull distance, `face.pushpull((z1-z0).mm)`. A zero-overlap collision check does
  NOT catch this - it only proves nothing collides, not that a piece is at the right height, so
  always verify at least one piece's actual bounds against the intended z0/z1 after any
  pushpull-based creation. The same bug can also manifest as reversed/inward face normals
  (renders as SketchUp's default blue backface colour) rather than wrong-z, depending on what
  else occupied that z-range when the buggy geometry was created - one bug, two different visible
  symptoms.
- **Outliner audits must walk `Sketchup::ComponentInstance` too, not just `Sketchup::Group`** - a
  `grep(Sketchup::Group)`-only leaf collector silently skips stray entourage components (e.g. an
  imported person-figure) that can sit invisibly overlapping real geometry.

## Erase vs hide

`group.visible = false` for real design content being superseded (preserves history) - reserve
`.erase!` for (a) genuinely corrupted/junk stray geometry with no design meaning, and (b) content
the builder explicitly and directly instructs to be permanently removed. Note WHY in a hidden
group's name so a later blanket "enable everything" visibility toggle doesn't resurrect abandoned
geometry unnoticed.

## Collision check pattern

Recursive leaf-collection (only recurse into a `Sketchup::Group` that itself contains child
groups; otherwise it's a leaf) + `combination(2)` pairwise AABB overlap test with a 1mm
tolerance. Re-run after every batch of transforms. Filter to `next unless e.visible?` to reflect
what's actually shown, not superseded/hidden geometry. This genuinely catches real buildability
errors (a stud a few mm from a king stud, redundant framing, wrong AFF heights) that are invisible
in a flat text cut list.

## Purpose-audit pattern

When checking "does every piece still have a purpose" (not just "does the name match the cut
list"), the highest-value finding is usually geometry whose *reason for existing* was removed by a
later redesign but never cleaned up - trace what problem a piece was solving, then check whether a
later change already solved that a different way. This doesn't show up in a naming diff or even a
collision check.

## Piece-code labelling workflow

1. Establish a `[CODE]` naming convention on every outliner group up front, and always reference
   the exact outliner name in conversation and in code, never an informal paraphrase.
2. To label "everything that isn't confirmed/finalised yet": walk the model, skip groups already
   marked confirmed (e.g. by a dedicated material/tag), skip purchased-product groups (appliances,
   fixtures) and already-installed groups, and label the rest one at a time per the standing rule
   above.
3. Define the label helper once, then call it once per piece - keeps each `eval_ruby` call small
   and each failure's blast radius (one piece) trivial to diagnose and retry.
