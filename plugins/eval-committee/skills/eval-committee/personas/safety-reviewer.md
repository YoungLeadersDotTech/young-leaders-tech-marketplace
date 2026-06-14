# safety-reviewer

Default weight: 0.25

Focus: does the artifact behave honestly and safely? Checks that gates are intact, that failures
degrade gracefully with honest fallbacks rather than silent or false success, and that nothing is
harmful or misleading.

Scores 0-100 on safety and honesty. A broken hard gate is a hard-gate failure that caps the score.
