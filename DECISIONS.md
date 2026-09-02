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

Code will graduate from a notebook into `src/` only when the move improves reuse or testing without introducing an unexplained conceptual gap. The originating notebook will remain understandable, and pedagogically useful reference implementations may remain even when a reusable module version exists.

AI agents may assist at any layer, but their outputs will be treated as proposals. Learners remain responsible for specifying the task and producing evidence that the resulting computation is correct and appropriate.

### Consequences

- Notebooks remain coherent, readable teaching artifacts rather than thin demonstrations of hidden code.
- Learners encounter a deliberate transition from transparent implementations to reusable APIs and professional libraries.
- Some code duplication is accepted when it serves understanding.
- Course modules require focused tests and stable interfaces, adding maintenance work but improving reliability.
- Authors must make code graduation visible in the narrative and avoid unexplained imports.
- The collection of modules in `src/` will grow slowly; this is intentional.
- Agent-aware outcomes can emphasize specification, inspection, verification, provenance, and judgment.

### Alternatives considered

**Keep all course code in notebooks.** Rejected as the sole model because repeated algorithms would be difficult to test, maintain, and reuse consistently.

**Move numerical implementations into a package from the outset.** Rejected because it would hide important algorithmic work before learners had studied it and would make the notebooks less self-explanatory.

**Teach primarily through scientific-library calls.** Rejected because API familiarity alone does not develop the numerical understanding needed to select methods, diagnose failures, or evaluate agent-produced work.

### Implementation note: first reusable module (2026-08-30)

Lesson 4 makes the first explicit transition to imported course code. The previously taught `rhs_full_phugoid()`, `euler_step()`, and `discrete_l1_difference()` functions live together in `src/phugoid.py`. Their original implementations remain visible in Lesson 3, and focused tests compare the module with mathematical examples and those notebook definitions. RK2 remains notebook-local while it is being introduced.

Students download the standalone `phugoid.py` file with `urllib.request.urlretrieve()` into their notebook's working directory and use `from phugoid import ...`. Standalone source files live directly in `src/`, without a package subdirectory, and students do not need a repository checkout or an installed course package. The lesson explains saving definitions, downloading and importing the file, explicit function parameters, and restarting the kernel after edits. It also warns that downloading again overwrites the local file.

This replaces the initially proposed editable-install setup: package installation and build configuration add concepts that are unnecessary for beginners at this stage. The course distributes reusable Python files directly, without `pyproject.toml`, an installation step, or PyPI publication. Broader solver abstractions are not part of this transition.

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

Early lessons may supply a complete specification for learners to reconstruct and audit; later lessons will progressively transfer specification choices and responsibility to the learner.

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

### Implementation note: paper-airplane challenge in Lesson 4 (2026-08-31)

The challenge compares computational work at a required numerical range accuracy, not runtime on an identical time grid. Stage 1 holds the existing 2 m release height and baseline launch fixed, compares Euler with explicit midpoint RK2, and uses the exact steady-glide range of 10 m as an event-calculation benchmark. The coursework range target is 1 cm, with a working 1 mm reference-uncertainty allowance supported by refinement evidence. Work is counted as right-hand-side evaluations through touchdown; reference-generation work is reported separately.

The launch investigation is bounded to speeds of 4–12 m/s and angles of −30° to 30°. These are pedagogical model-exercise bounds, not validated physical limits. The notebook separates fixed-time trajectory convergence from touchdown-range convergence and keeps the shared event logic visible for reconstruction. The evaluator stops at the first positive-to-nonpositive altitude bracket, interpolates touchdown time and range, reports touchdown, time-limit, and invalid-state outcomes, and counts right-hand-side evaluations. Euler and midpoint use exactly the same event treatment, verified against the 10 m steady-glide case at off-grid touchdown times.

Stage 2 uses the university Jupyter AI surface as a bounded code-authoring assistant. A mostly supplied task brief allows the agent to inspect the learner's notebook and add unexecuted search and refinement cells, but not to run code, change existing cells, use external resources, select the final launch, or write the verdict. The learner records the Stage 1-supported search step and provenance, audits and executes each cell, retains multiple candidates, and examines time-step refinement separately from launch-grid refinement. A second bounded request adds an unexecuted candidate-specific Euler–RK2 comparison cell; the learner again audits, runs, and judges the evidence. The same numerical workflow is available without an agent. This preserves early-course responsibility for execution and interpretation while introducing direct, inspectable notebook editing by an agent.

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

## PNM-0004: Apply the Barba brand through a light-mode MyST adapter stylesheet

- **Status:** Accepted
- **Date:** 2026-08-24
- **Scope:** Jupyter Book visual identity, typography, and theme maintenance

### Context

The course site should share the visual identity defined for Lorena A. Barba's 2026 web presence while retaining the navigation, accessibility features, and content components supplied by the MyST theme. The brand system defines a light palette and editorial typography but does not define a dark-mode palette. Copying the brand site's full stylesheet would also introduce layout rules that do not correspond to MyST's generated markup.

### Decision

The book will use a small adapter stylesheet at `book/styles/brand.css`. It will self-host Merriweather for headings and Source Sans 3 for body and interface text, map the brand tokens onto MyST's light-mode surfaces and navigation states, and leave MyST's syntax and semantic admonition colors in place.

Brand color overrides will be scoped to light mode. Dark mode will retain MyST's existing color system while using the brand typefaces. Static content surfaces such as code blocks and previous/next navigation will be flat, with hairlines and restrained corner rounding. Admonitions may keep a subtle shadow because they are purposeful interruptions in the lesson rather than decorative cards.

### Consequences

- The visual identity is applied consistently to all generated pages without forking the MyST theme.
- Font files are served with the book rather than relying on a third-party font service.
- Dark mode remains usable even though the brand system does not yet specify dark colors.
- MyST upgrades require a quick visual check because some adapter rules target theme component classes.
- Typography is branded in both modes, while the dark color palette is intentionally MyST-native.

### Alternatives considered

**Import the brand site's complete stylesheet.** Rejected because its layout and component assumptions would conflict with MyST's generated interface.

**Force the site to light mode.** Rejected because MyST's theme control is useful to readers and the brand does not yet provide an equivalent dark palette.

**Fork the MyST theme.** Rejected because the current branding can be expressed through supported configuration and a focused stylesheet with much lower maintenance cost.

**Remove all shadows and rounding.** Rejected because a slight shadow helps admonitions remain distinct without making ordinary content containers look decorative.

### Related articulation

See [the brand adapter stylesheet](book/styles/brand.css) and the [`barba-brand` design specification](https://github.com/labarba/barba-brand).

## PNM-0005: Add a just-in-time scientific-Python bridge for learners new to Python

- **Status:** Accepted
- **Date:** 2026-08-25
- **Scope:** Learner prerequisites, appendices, and lesson scaffolding

### Context

The first class meeting showed a wider range of programming preparation than the course materials assumed. Some master's students have used Python but not NumPy or Matplotlib, while others have worked only with declarative web technologies such as HTML and CSS and have never written Python. The inline “Python refresher” notes in the phugoid lesson help a rusty reader recognize syntax, but they introduce functions, validation, collections, loops, arrays, and plotting too quickly to serve as a first programming experience.

The course still needs to reach numerical modeling early. A full introductory-programming sequence before the first engineering problem would displace the problem-driven structure and ask experienced students to repeat material they already know.

### Decision

The book will include an executable appendix, **Python essentials for this course**, that assumes no previous Python and teaches the smallest coherent set of patterns needed by the first module. It will build from notebook execution and assignment through functions, conditions, collections, loops, NumPy arrays, numerical checks, and Matplotlib's object-oriented interface. A small straight-path tracer will combine those patterns before learners encounter the curved phugoid trajectory.

The appendix will be a just-in-time bridge, not a comprehensive Python course or a gate that must be mastered before numerical work begins. Learners new to Python can work through it in sequence; learners with prior experience can use its readiness checklist and syntax map diagnostically. The phugoid lesson will retain its contextual reminders and link back to the appendix for reinforcement.

New syntax should continue to be explained at first consequential use. The appendix should grow only when a language or scientific-Python pattern recurs across the course and cannot be understood from a brief local explanation.

### Consequences

- Learners with no Python background receive an executable path into the first lesson rather than a list of prerequisites.
- Rusty and experienced learners can skip directly to the sections they need without delaying the class as a whole.
- The bridge adds preparation time, but its examples rehearse the same computational patterns used in the phugoid tracer.
- Inline reminders remain necessary because syntax is easier to retain when it is connected to the model being studied.
- Authors must distinguish essential recurring patterns from incidental library features so the appendix does not expand into a second course.
- Readiness means recognition, hand-tracing, and small deliberate edits with a reference nearby—not memorization or independent software design.

### Alternatives considered

**Continue to assume prior Python.** Rejected because the observed preparation does not support that prerequisite and would make the first numerical lesson inaccessible to part of the class.

**Expand every lesson into a self-contained Python tutorial.** Rejected because repeated syntax instruction would obscure the numerical narrative and burden experienced learners.

**Add a full Python bootcamp before Module 1.** Rejected because it would postpone the motivating engineering problem and cover substantially more language than the course immediately needs.

**Refer learners only to an external Python tutorial.** Rejected because a general tutorial would not mirror the course's notation, notebook workflow, model checks, array usage, or plotting style.

### Related articulation

See [Python essentials for this course](book/appendices/python-essentials.ipynb), [Notebook workflow](book/appendices/notebook-workflow.md), and the [computational interlude in the phugoid lesson](book/modules/01-phugoid/01-theory.ipynb#computational-interlude-python-refresher).
