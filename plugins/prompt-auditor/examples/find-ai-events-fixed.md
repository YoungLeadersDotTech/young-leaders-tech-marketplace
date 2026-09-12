# Find AI events - corrected prompt

Corrected counterpart to `examples/find-ai-events.md`, which is kept deliberately broken as the
demo fixture that fails all eight checks. Fields in `<angle brackets>` are yours to fill before
running: the original prompt told the model to assume them, which is the root of PROMPT-001.

---

You are helping me plan conference attendance. I am <role, e.g. a staff engineer> working in
<field>, and my goal for the next six months is to be invited to speak at AI events rather than
only attend them. Rank for that goal, not for general interest.

Definitions for this task, so you do not have to infer them:

- "Local" means within <N> km of <city>, or reachable as a same-day return trip from <city>.
- "AI event" means a conference, meetup, or workshop where at least half the published sessions
  are about building with or deploying machine learning systems. Exclude general software events
  with a single AI track.
- "Worth going to" means it meets at least one of: it has an open call for speakers; it has a
  named speaker I would want to meet; or it is the main annual event for <field>.
- "Comprehensive" means every qualifying event you can verify, up to a maximum of 15.

Do these steps in order.

1. Search online for qualifying events with a start date between <start date> and <end date>.
2. Read only the files I have named here: <paths, or "none - skip this step">. Do not search my
   filesystem beyond those paths, and do not open anything outside them. Treat every file as
   read-only.
3. Discard events that fail the definitions above. Report the count you discarded and why.
4. For each surviving event, record: name, start date, end date, city, venue, ticket cost in
   local currency, the URL of the page you took the details from, and the speaker call deadline
   if one is open.
5. Rank the survivors by how likely each is to get me a speaking slot, most likely first. Give
   each a one-sentence reason referencing the goal above.
6. List separately, at the top, any event whose speaker call closes within 30 days of today.

Constraints:

- Do not guess a date, price, or venue. If you cannot verify a field, write `UNVERIFIED` in it.
  An `UNVERIFIED` field is an acceptable answer; an invented one is not.
- Do not infer my location, field, or seniority. If a bracketed field above is still unfilled,
  stop and ask me for it rather than assuming a value.
- Do not include events outside the date range, even if they look relevant.
- Do not register me for anything, email anyone, or submit a talk proposal.
- No more than 15 events, and no more than two sentences of commentary per event.

Output format - a Markdown table, then the speaker-deadline list, and nothing else:

| Rank | Event | Dates | City | Cost | Speaker call closes | Source | Why this rank |
|---|---|---|---|---|---|---|---|
| 1 | PyData Example | 2026-11-03 to 2026-11-05 | Dublin | EUR 250 | 2026-09-30 | https://example.com/cfp | Open call for talks on production ML, matches my deployment work. |
| 2 | Example AI Meetup | 2026-10-14 | Dublin | Free | UNVERIFIED | https://example.com/meetup | Monthly organiser slot is how two speakers I know got their first talk. |

You are done when: every row has all eight columns filled or marked `UNVERIFIED`, every row's
source URL is one you actually opened, the table has 15 rows or fewer, and the discard count from
step 3 is stated. If you cannot meet those conditions, say which one failed instead of returning
a partial table.
