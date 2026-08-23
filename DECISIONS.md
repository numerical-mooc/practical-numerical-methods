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

## PNM-0002: Adopt a repeated derive–reconstruct–specify–audit–explain lesson cycle

- **Status:** Accepted
- **Date:** 2026-08-22
- **Scope:** Lesson design, learner workflow, and agent-aware pedagogy

### Context

Executable notebooks can encourage passive “Run All” behavior if learners do not first develop an independent understanding of the model and algorithm. At the same time, coding agents make implementation inexpensive without making numerical judgment, verification, or engineering responsibility less important.

The course needs a repeated practice that combines foundational mathematical work, active reconstruction, supervised agent use, and evidence-based conclusions.

### Decision

Every lesson will follow five stages:

1. **Derive — On paper:** complete a short derivation, diagram, dimensional check, calculation, or prediction before computing.
2. **Reconstruct — In your notebook:** use the published lesson as a worked reference while rebuilding its central computation in a learner-owned notebook. Limited copying of mechanical code is acceptable.
3. **Specify — Before using an agent:** define a bounded task through its outcome, context, interface, constraints, permitted access, and acceptance evidence.
4. **Audit — Review and verify:** inspect agent or library output and test it using appropriate mathematical, numerical, and physical evidence.
5. **Explain — Your verdict:** state what is accepted, what evidence supports that decision, and what remains uncertain.

Lessons will expose this rhythm through the signposts **On paper**, **In your notebook**, **With an agent**, and **Your verdict**. Each lesson will include one bounded agentic task emphasizing specification, review, or validation.

Published notebooks remain the canonical executable exposition and must execute reliably, but they are reference artifacts rather than the learner’s primary working notebook.

### Consequences

- Authors must reserve lesson time for reconstruction, verification, and reflection rather than maximizing content coverage.
- Every lesson needs a meaningful paper activity and an agent task grounded in its numerical subject.
- Agent tasks should become less scaffolded as the course progresses.
- Learners produce independent predictions, computational work, review evidence, and a defensible conclusion.
- Course-practice guidance is introduced as core material; appendices provide just-in-time reference patterns.
- Accessible alternatives and a no-paid-agent route must remain available.

### Alternatives considered

**Have learners execute the published notebooks directly.** Rejected as the default because it encourages recognition and execution without requiring reconstruction.

**Teach agent use in a separate module.** Rejected because specification, review, and verification should become habits practiced with every numerical method.

**Allow unstructured agent use.** Rejected because delegation without explicit requirements and acceptance evidence does not develop accountable engineering practice.

### Related articulation

See [Working through a lesson](book/course-practice.md), [Notebook workflow](book/appendices/notebook-workflow.md), [Verification patterns](book/appendices/verification-patterns.md), and [Working with agents](book/appendices/agent-use.md).

## PNM-0003: Assess modules through lesson checkpoints and problem-based capstones

- **Status:** Accepted
- **Date:** 2026-08-23
- **Scope:** Assessment architecture, module design, and instructor workflow

### Context

The legacy course ended each module with a memorable engineering coding assignment, but the surviving assessments primarily asked learners to implement a prescribed method and report expected numerical values or reproduce a target plot. Coding agents can now produce that artifact without demonstrating the numerical judgment the course intends to develop.

Assessment only at the end of a module would also make it difficult to distinguish sustained reconstruction and reasoning from a polished artifact assembled shortly before submission. Conversely, assigning points to every lesson-stage artifact would create unnecessary grading work and shift attention from learning to point accumulation.

### Decision

Assessment will operate at two scales:

1. **Lesson checkpoints** will sample designated handwritten work and learner-owned notebook evidence during a module. They will be marked `Complete` or `Revise` and will not receive separate points.
2. **A problem-based capstone** will conclude each module. It will preserve the module's legacy engineering narrative while requiring a specification, inspectable computational artifact, audit, complementary verification evidence, lightweight provenance, and a defended engineering verdict.

The instructor will review the lesson checkpoints and capstone together in a short individual checkout and assign one module grade on a 1-4 scale. The five module grades will be equally weighted. Revision may replace an earlier module grade within the stated window.

The GW syllabus will remain outside the public Jupyter Book. The fuller capstone architecture will be maintained as instructor-facing documentation in `docs/`; learner-facing assignment briefs and rubrics will be added to their modules as the course is developed.

### Consequences

- Learners receive feedback before the capstone rather than only after completing it.
- The capstone assesses supervision, verification, and defense without abandoning direct implementation where it supports understanding.
- One module grade summarizes the learning process and capstone performance without point totals for every artifact.
- The instructor must keep checkpoints and individual reviews brief and consistent.
- Public design documentation must not contain hidden answers or controlled assessment material.

### Alternatives considered

**Migrate the legacy coding assignments unchanged.** Rejected because expected values and plots do not provide sufficient evidence of specification, review, verification, provenance, or understanding when code generation is inexpensive.

**Assess only the finished capstone.** Rejected because it would not provide timely feedback or establish that the learner reconstructed and understood the central method during the module.

**Grade every lesson artifact separately.** Rejected because it would create excessive bookkeeping and make low-stakes practice feel like a sequence of assignments.

**Replace the module capstones with one large final project.** Rejected because repeated, problem-specific practice is more aligned with the five-module course journey and allows supervisory responsibility to grow gradually.

### Related articulation

See [Assessment and module-capstone design](docs/Assessment-and-Capstone-Design.md) and [Working through a lesson](book/course-practice.md).
