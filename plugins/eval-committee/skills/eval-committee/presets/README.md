# Presets (opt-in)

This skill is generic by default. Presets let you adapt it without forking: override the persona
list, their weights, the rubric, and the score floor.

Keep anything private out of this public folder. Real benchmark datasets, company-specific
criteria, internal names, and credentials belong in a private repo (for example a personal AI-OS
repo), not here. Point the skill at a private presets file at run time.

A preset is a short Markdown file. Minimal example:

    floor: 85
    personas:
      - correctness-reviewer: 0.4
      - safety-reviewer: 0.3
      - usability-reviewer: 0.3
    notes: tighten the floor and drop the maintainability persona for this run.
