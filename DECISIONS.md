<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Course design decisions

This file records consequential design choices for the 2026 edition of **Practical Numerical Methods**. A decision record explains why a choice was made, what it implies, and what alternatives were considered. Later changes should update a record’s status or add a superseding record rather than silently erase the reasoning.

## PNM-0001: Adopt notebook-first executable exposition with gradual code graduation

- **Status:** Accepted
- **Date:** 2026-08-21
- **Scope:** Course architecture, authoring, and learner workflow

### Context

The course treats a notebook as an executable chapter: learners should be able to follow the mathematical reasoning and the numerical algorithm step by step, run the work, alter it, and inspect its behavior. Moving all numerical logic immediately into imported Python modules would make the notebooks cleaner as software clients but less complete as teaching documents. Keeping every implementation only in notebooks, however, would make reuse, testing, and maintenance increasingly difficult as the course grows.

The 2026 edition must also prepare learners for computational work involving mature scientific libraries and AI agents. That makes transparent specifications, inspection, testing, verification, and engineering judgment more important—not less.

### Decision

Notebooks will be the canonical executable exposition for the course. Numerical methods will first appear in notebooks as readable implementations whose important steps remain visible to the learner.

The course will use three layers of computational material:

1. **Executable notebooks** for derivation, implementation, experimentation, verification, and interpretation.
2. **Small course modules** for stable, tested code that has already been taught transparently and now needs to be reused through a small explicit API.
3. **Scientific libraries** for professional practice after learners understand enough of the method to choose, configure, and validate the library implementation.

Code will graduate from a notebook into `src/practical_numerical_methods/` only when the move improves reuse or testing without introducing an unexplained conceptual gap. The originating notebook will remain understandable, and pedagogically useful reference implementations may remain even when a reusable module version exists.

AI agents may assist at any layer, but their outputs will be treated as proposals. Learners remain responsible for specifying the task and producing evidence that the resulting computation is correct and appropriate.

### Consequences

- Notebooks remain coherent, readable teaching artifacts rather than thin demonstrations of hidden code.
- Learners encounter a deliberate transition from transparent implementations to reusable APIs and professional libraries.
- Some code duplication is accepted when it serves understanding.
- Course modules require focused tests and stable interfaces, adding maintenance work but improving reliability.
- Authors must make code graduation visible in the narrative and avoid unexplained imports.
- The `src/` package will grow slowly; this is intentional.
- Agent-aware outcomes can emphasize specification, inspection, verification, provenance, and judgment.

### Alternatives considered

**Keep all course code in notebooks.** Rejected as the sole model because repeated algorithms would be difficult to test, maintain, and reuse consistently.

**Move numerical implementations into a package from the outset.** Rejected because it would hide important algorithmic work before learners had studied it and would make the notebooks less self-explanatory.

**Teach primarily through scientific-library calls.** Rejected because API familiarity alone does not develop the numerical understanding needed to select methods, diagnose failures, or evaluate agent-produced work.

### Related articulation

See [Notebook-first code architecture](docs/Notebook-First-Code-Architecture.md) for the progression within a topic, criteria for graduating code, and module-design guidance.
