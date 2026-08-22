<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Notebook-first code architecture

## Core principle

**Notebooks are the canonical executable exposition.** They are the place where a learner encounters a problem, follows the mathematical reasoning, sees an algorithm assembled step by step, runs it, and examines evidence that it works.

“Canonical” applies to the teaching narrative. A notebook should contain everything a learner needs to understand the method at that point in the course. Imported code must not create a conceptual gap or hide the part of the algorithm being taught. At the same time, canonical exposition does not require every reusable implementation to remain forever embedded in a notebook. Once code has been explained, exercised, and stabilized, it may graduate into a small course module.

Some deliberate duplication is therefore acceptable. A notebook may retain a compact reference implementation for study while later exercises use a tested module implementation for repeated computation.

## Three layers of computational material

| Layer | Primary purpose | What belongs here | What does not belong here |
| --- | --- | --- | --- |
| Executable notebook | Understanding and inquiry | Derivation, transparent implementation, experiments, visualization, verification, and interpretation | Important algorithmic steps hidden behind an unexplained import |
| Small course module | Reuse within the course | Stable numerical kernels and helpers that learners have already seen, exposed through small explicit APIs and supported by tests | A premature framework or a catch-all utilities package |
| Scientific library | Professional practice | Mature external tools such as NumPy and SciPy, introduced with attention to assumptions, interfaces, and validation | A substitute for understanding the numerical method |

The layers are a progression, not a hierarchy of quality. Notebook code can be intentionally direct and pedagogical. Course-module code should be more reusable and tested. Scientific-library code brings mature capabilities, performance, and robustness after learners have enough understanding to use it critically.

## Progression within a topic

### 1. Begin with the model and the numerical question

The notebook introduces the physical or engineering problem, develops the mathematical model, and states what the computation must accomplish. Learners should understand the inputs, outputs, assumptions, and expected behavior before encountering a packaged solver.

### 2. Build the algorithm visibly

The first implementation is written in the notebook in small, readable steps. Intermediate quantities remain visible, notation stays close to the mathematics, and plots or tables expose the behavior of the computation. Concision is less important than traceability.

### 3. Refactor without hiding

After the learner has worked through the steps, the notebook may collect them into a local function. This introduces decomposition and an explicit interface while keeping the complete implementation on the page. The learner can still read, execute, modify, and debug every part.

### 4. Verify before reuse

The notebook checks the implementation using evidence appropriate to the problem: limiting cases, conservation properties, convergence studies, dimensional reasoning, comparison with an analytical solution, or an independently obtained result. Verification is part of the algorithmic story, not an optional add-on.

### 5. Graduate stable code into a course module

When the implementation is understood and needed again, a tested version may move to `src/practical_numerical_methods/`. The transition should be explicit in the narrative: the notebook identifies what has moved, shows the small API, and demonstrates that the imported implementation reproduces the behavior already studied.

The notebook should remain intelligible on its own. Depending on the learning objective, it may retain the original reference implementation, present a shortened version alongside the import, or link directly to the module source.

### 6. Connect to a scientific library

Once learners understand the method, the course can introduce an established library implementation. The notebook should map the library’s vocabulary and parameters to the previously developed algorithm, compare results, and discuss what the library adds—such as adaptive control, broader method choices, performance, or safeguards.

The learning goal is not merely to call an API. It is to make an informed choice, inspect the result, and recognize failure or misuse.

### 7. Add agent-aware computational practice

An AI agent may help propose an implementation, refactor code, design tests, explain an unfamiliar API, or investigate a discrepancy. The learner remains responsible for the specification and the evidence. Agent-produced work should be inspected against the model, tested, and attributed when it materially shapes the result.

This preserves the course’s central purpose in an agentic setting: learners develop the judgment to direct computational work and determine whether its outputs deserve trust.

## Example progression: Euler’s method

A notebook might first derive the update

\[
u^{n+1} = u^n + \Delta t\,f(u^n,t^n),
\]

then implement the time loop directly and display selected intermediate states. It may next define a local `euler_step` function, investigate error under time-step refinement, and compare with a known solution. When later lessons need Euler’s method as a baseline, a tested `integrate_euler` function can be imported from the course package. Finally, learners can compare it with a solver from `scipy.integrate`, relating the professional interface and error controls to ideas they already understand.

At no point does the import retroactively replace the readable derivation and reference implementation that made the method understandable.

## Criteria for graduating code

Code is a candidate for a course module when most of the following are true:

- The algorithm has already been presented transparently in a notebook.
- The implementation will be reused across lessons, assignments, or verification work.
- Its inputs, outputs, and numerical assumptions can be expressed through a small API.
- Its behavior is stable enough to support tests.
- Moving it will reduce distracting repetition without creating a conceptual jump.
- The originating notebook will remain understandable after the move.

Code should stay in the notebook when it is part of the explanation, is still changing as ideas develop, supports a one-off experiment, or would become harder to understand if separated from the surrounding mathematics and narrative.

## Design of course modules

Course modules should favor:

- small functions with explicit inputs and return values;
- minimal hidden state and no reliance on notebook globals;
- names that reflect the numerical or physical idea;
- separation of numerical computation from plotting where practical;
- modest, purposeful dependencies;
- docstrings and type information when they improve clarity; and
- focused tests based on mathematical or physical expectations.

The goal is not to turn the course into a large software framework. The modules exist to support learning and principled reuse.

## Authoring implications

- A notebook is reviewed as a readable chapter as well as executable code.
- Removing duplication is not automatically an improvement; pedagogically useful repetition may remain.
- New imports of course code should point backward to where the algorithm was developed.
- Module tests complement, but do not replace, verification and interpretation in the notebooks.
- The `src/` directory grows only as code earns its way out of the notebooks.
- Scientific-library and agent-assisted results are treated as claims requiring evidence, not as authorities.

This architecture creates a gradual bridge from transparent learning code to reusable course software and, finally, to professional computational practice.
