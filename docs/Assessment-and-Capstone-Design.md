<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Assessment and module-capstone design

## Purpose and status

This document records the instructor-facing assessment design for the 2026 course. It connects the repeated lesson practice to five problem-based module capstones and preserves the strongest engineering narratives from the legacy course without preserving its answer-box grading model.

This is an assessment architecture, not a set of finished assignments. Each module will later receive a learner-facing brief, open acceptance checks, and a concise rubric as its lessons are developed. Reference solutions, hidden checks, or instructor scoring notes should remain outside this public document when disclosure would weaken the assessment.

The GW syllabus is maintained outside the public Jupyter Book because it contains institution- and offering-specific policies. The book should continue to explain the learning practice; the syllabus should explain how that practice is assessed.

## Design principles

1. **Assess judgment, not code production.** Code written by a learner, proposed by an agent, or obtained from a scientific library is evidence only after the learner has inspected and verified it.
2. **Keep the memorable engineering problems.** Rocket flight, traffic flow, a shock tube, reaction-diffusion patterns, and lid-driven cavity flow remain effective integrations of each module.
3. **Check learning while it is happening.** Selected derivations and notebook work are reviewed during the lessons rather than inferred from a polished capstone at the end.
4. **Use one integrated capstone per module.** The capstone asks whether a consequential numerical claim is trustworthy and fit for a stated purpose.
5. **Allow revision.** A checkpoint marked `Revise` identifies unfinished learning rather than assigning a permanent penalty.
6. **Keep the evidence compact.** One learner-owned computational record, a lightweight provenance note, and a short individual review should normally be sufficient.
7. **Provide supported access.** The course will identify at least one AI route available to every enrolled student. Assignments will remain provider-neutral and accommodate usage caps or temporary service interruptions.

## Two layers of assessment

### Lesson checkpoints

Learners follow the **derive-reconstruct-specify-audit-explain** cycle throughout each module. The instructor checks selected evidence during class or brief one-on-one conversations:

- designated handwritten derivations, diagrams, dimensional checks, or predictions;
- reconstruction of central numerical steps in the learner's notebook;
- predictions recorded before important computations;
- selected task specifications or reviews of agent and library work; and
- verification evidence and interpretations developed during the lessons.

Lesson checkpoints are marked only `Complete` or `Revise`. They are not separate assignments, do not receive points, and need not inspect every practice-stage artifact from every lesson. Their purposes are to make participation in the learning process visible, correct misunderstandings early, and establish that the learner can explain the work later used in the capstone.

### Module capstone

At the end of each module, the learner applies the module's ideas to one integrated engineering problem. A capstone should contain:

1. **Claim and prediction:** the engineering quantity, behavior, or decision at issue, with relevant paper reasoning completed before computation.
2. **Specification:** the model, conventions, units, interface, constraints, agent access, and acceptance evidence for delegated work.
3. **Computational artifact:** a reproducible notebook and any consequential code or diff. The source of the code is less important than its inspectability.
4. **Audit:** inspection of equations, units, signs, indices, boundaries, state, dependencies, and failure behavior.
5. **Verification:** at least two complementary checks appropriate to the problem. At least one check should be capable of detecting a plausible wrong implementation.
6. **Provenance and verdict:** material agent or library contributions, accepted and rejected suggestions, the supported conclusion, limitations, and remaining uncertainty.

The instructor reviews the capstone in a short individual checkout, normally 5-10 minutes. The learner shows the relevant paper and notebook evidence and responds to a question about a derivation, modeling choice, code change, verification result, or limitation.

The capstone is not a separate report layered on top of the notebook. The notebook, compact provenance record, and oral explanation together form the submission.

## Relationship to the module grade

Lesson checkpoints and the capstone are assessed together as one module performance:

| Grade | Meaning |
| ---: | --- |
| **4** | **Complete with distinction.** Required checkpoints and capstone evidence are complete, and the learner demonstrates independent critical judgment by investigating a consequential failure mode, alternative, or uncertainty. |
| **3** | **Complete.** Required checkpoints and capstone evidence are complete; the numerical claim is supported by appropriate evidence; and the learner can explain and defend the work. |
| **2** | **Developing.** A substantial, explainable attempt is present, but one or more important gaps leave the evidence or defense only partly satisfactory. The learner can identify what needs revision. |
| **1** | **Not assessable.** Work is missing or fragmentary, or the learner cannot explain consequential parts of it. |

A grade of 4 recognizes stronger engineering judgment, not more code, decorative polish, or unnecessary scope. A module grade may be replaced after revision through the next module checkout; the final module uses a stated end-of-course deadline.

All five capstones must be submitted and individually reviewed. A module remaining at grade 1 after the final revision deadline is incomplete, and the learner has not met the minimum requirements to pass the course. This completion rule is clearer than an independent automatic-F trigger because it uses the same published module scale and preserves the ordinary accommodation or Incomplete process when applicable.

## Progression of agent responsibility

The capstones should not repeat the same generic prompt five times. Responsibility grows across the course:

| Module | Principal agent-aware practice |
| --- | --- |
| 1. Phugoid motion | Compare a transparent learner implementation with an agent-proposed alternative. |
| 2. Space and time | Delegate from a bounded numerical specification and audit the implementation. |
| 3. Riding the wave | Conduct adversarial review of a solver on discontinuous and failure-prone cases. |
| 4. Spreading out | Investigate reproducibility, sensitivity, and claims drawn from visually persuasive output. |
| 5. Relax and hold steady | Permit optimization only after a correctness suite passes, then check that numerical behavior is preserved. |

## Proposed module capstones

### Module 1: Rocket flight

**Legacy core.** The learner used Euler's method with a fixed time step of 0.1 s to simulate vertical rocket flight with gravity, drag, variable propellant mass, and a piecewise burn rate. Assessment asked for propellant mass, maximum speed, apogee, impact time, and impact velocity.

**Capstone question.** *Can the computed apogee and impact conditions be trusted to the stated accuracy?*

**Preserve.** Keep the force model, powered/coasting/falling regimes, event quantities, and physical interpretation. These make the task more valuable than a generic ODE exercise.

**Revise.** The learner should first construct a transparent baseline integrator, then specify an alternative implementation or event-detection improvement for an agent. Reporting the legacy event values may remain a regression check, but it is not the assessed outcome.

**Minimum evidence.** Include:

- a hand derivation of the state equations, sign convention, propellant history, and flight regimes;
- dimensional and limiting-case checks, including exact propellant mass before burnout;
- tests for nonnegative propellant, the sign of drag during ascent and descent, burnout handling, and ground crossing;
- time-step refinement for apogee and impact quantities;
- comparison with a second-order method or an independently configured library solver; and
- a justified time step and event-interpolation rule for the claimed accuracy.

A useful adversarial case changes `v * abs(v)` to `v**2`, mishandles the transition at burnout, or reports the first negative altitude as the impact state without interpolation.

### Module 2: Traffic flow

**Recovered legacy core.** The Open edX assignment modeled one-lane traffic using

\[
V(\rho) = V_{\max}\left(1-\frac{\rho}{\rho_{\max}}\right),
\qquad
F(\rho) = \rho V(\rho),
\]

and a forward-time/backward-space discretization of the density conservation law. It used an 11 km road, \(\rho_{\max}=250\) cars/km, 51 points, and \(\Delta t=0.001\) h. Part A used \(V_{\max}=80\) km/h, background and inflow density 10 cars/km, and a 10-point patch at 50 cars/km. Part B changed \(V_{\max}\) to 136 km/h and the background and inflow density to 20 cars/km. Learners entered six rounded minimum or average velocities at selected times.

**Conceptual correction.** The revised task must distinguish vehicle speed \(V(\rho)\) from the characteristic speed

\[
a(\rho)=\frac{dF}{d\rho}
=V_{\max}\left(1-2\frac{\rho}{\rho_{\max}}\right).
\]

The legacy explanation blurred these two quantities. The sign and magnitude of \(a\), not simply the vehicle speed, determine the direction of information propagation and the appropriate upwind stencil.

**Capstone question.** *Can an FTBS traffic solver be trusted in both operating scenarios, and what can it support us in claiming about the evolving congestion?*

**Preserve.** Keep the LWR flux, the two initial/boundary scenarios, the unit conversion, and the selected velocity summaries as baseline regression values. Restate the dense patch by its physical interval rather than by the grid-dependent slice `rho0[10:20]` so that refinement represents the same problem.

**Revise.** Give the learner responsibility for specifying a reusable conservative solver and its acceptance criteria. An agent may implement the bounded solver or propose a patch, but the learner must decide whether the discretization, boundary treatment, and outputs are valid. The two scenarios should support comparison rather than six isolated answer boxes.

**Minimum evidence.** Include:

- a hand derivation of \(F(\rho)\), \(a(\rho)\), the conservative FTBS update, and the applicable CFL condition;
- hand-checkable initial minimum velocities and unit conversions;
- a calculated CFL bound for both values of \(V_{\max}\), with an explanation of why the chosen spatial bias is appropriate for the stated density range;
- a discrete vehicle-balance check that includes boundary fluxes;
- refinement of the grid and time step for the legacy summary quantities or a congestion-arrival quantity, while holding the physical initial condition fixed;
- comparison of conservative flux differencing with a plausible but incorrect implementation that substitutes vehicle speed for characteristic speed or mishandles the inflow boundary; and
- a verdict separating numerical diffusion and discretization uncertainty from limitations of the traffic model itself.

The legacy summary quantities can become open regression checks once reference values are regenerated and verified. A later rubric should assess the specification, ability of the checks to detect defects, refinement evidence, and defended claim—not agreement to two decimal places alone.

### Module 3: Sod shock tube

**Legacy core.** The learner implemented the two-step Richtmyer method for the one-dimensional Euler equations and produced pressure, density, and velocity at \(t=0.01\) s for Sod's first shock-tube problem. Earlier versions specified 80 grid points and \(\Delta t=0.0002\) s and asked for additional derived quantities.

**Capstone question.** *Does the candidate conservative solver resolve the Riemann problem without violating the governing physics?*

**Preserve.** Keep the standard benchmark, conservative variables, equation of state, shock, contact discontinuity, rarefaction, and exact-solution comparison.

**Revise.** Provide or solicit an agent-produced solver or consequential diff rather than treating source-code production as the main challenge. The learner owns the contract, review, and evidence. A second Riemann case or controlled defect should prevent tuning to a single reference plot.

**Minimum evidence.** Include:

- paper conversion between primitive and conserved variables and derivation of the flux;
- density and pressure positivity checks for the assigned cases;
- conservation or boundary-flux balance for mass, momentum, and energy;
- quantitative comparison with the exact Sod solution, including wave locations and a stated error measure;
- grid refinement with an interpretation appropriate to discontinuous solutions; and
- review of at least one plausible defect in the pressure reconstruction, indexing, boundary flux, or conservation form.

### Module 4: Gray-Scott reaction-diffusion

**Legacy core.** The learner implemented a two-dimensional forward-time/central-space solver on a 192 by 192 grid, used zero-Neumann boundaries and supplied initial arrays, evolved to 8000 s, and compared the resulting Gray-Scott pattern with an example image.

**Capstone question.** *Which features of the computed pattern are reproducible, and which depend materially on discretization or perturbations?*

**Preserve.** Keep the coupled nonlinear model, two-dimensional diffusion, boundary treatment, deterministic initial data, parameter exploration, and visual appeal.

**Revise.** Matching one image is not sufficient evidence. Require deterministic local data and a separation between early-time numerical verification and long-time pattern interpretation. Pointwise agreement at long time should not be demanded when small perturbations can change detailed morphology.

**Minimum evidence.** Include:

- a paper derivation of the update and zero-normal-gradient boundary treatment;
- a constant-field check;
- a pure-diffusion case with component-mass balance under zero-flux boundaries;
- a spatially uniform reaction case compared with an independent ODE solution;
- inspection for array aliasing, unintended in-place state changes, and boundary-slice errors;
- time-step and grid sensitivity at an early verification time; and
- robust summary measures or qualitative classifications for long-time pattern sensitivity to parameters and initial perturbations.

### Module 5: Lid-driven Stokes cavity

**Legacy core.** The learner solved coupled vorticity-streamfunction equations on a 41 by 41 grid and stopped when the L1 differences between successive iterates for both fields fell below \(10^{-6}\). The expected result was primarily a matching streamfunction contour.

**Capstone question.** *Is the steady solution actually converged, and can the computation be accelerated without changing its numerical meaning?*

**Preserve.** Keep the Stokes reduction, coupled Poisson problems, difficult wall-vorticity treatment, iterative convergence, and lid-driven cavity visualization.

**Revise.** A small update between iterates and a familiar contour are not proofs of correctness. Establish a correctness suite before allowing an agent to refactor, vectorize, change the linear solver, or optimize the implementation.

**Minimum evidence.** Include:

- a paper derivation of the coupled equations and at least one wall-vorticity condition;
- residuals for both discrete field equations;
- no-slip and moving-lid boundary checks;
- a discrete incompressibility check for the reconstructed velocity;
- symmetry and grid-refinement checks for selected flow quantities;
- comparison with an independently assembled sparse or direct solve where practical; and
- timing and memory evidence showing that an optimization preserves the accepted numerical behavior.

The learner should explicitly distinguish algebraic iteration error, discretization error, and modeling error. A tighter stopping tolerance is useful only until algebraic error is small relative to the discretization error.

## Proposed syllabus articulation

The syllabus should describe the two assessment layers without reproducing the technical capstone plans:

> Assessment occurs throughout each module and at its conclusion. During the lessons, you will show selected handwritten derivations and predictions and maintain an individual computational notebook that records reconstruction of the methods, agent or library work, verification, and interpretation. These lesson checkpoints are marked **Complete** or **Revise**; they receive no separate points and are intended to give timely feedback.
>
> Each module concludes with a problem-based capstone in which you use the module's ideas to support and defend an engineering claim. Code may be written directly, proposed by an agent, or drawn from a scientific library, as directed by the assignment. You remain responsible for the specification, inspection, verification, provenance, and conclusion. The instructor will review your lesson checkpoints and capstone in a short individual checkout.

The syllabus may then state the module-grade and final-average tables, using the grade descriptions in this document. The completion rule should read:

> All five capstones must be submitted and individually reviewed. A module remaining at grade 1 after the final revision deadline is incomplete; no module may remain at grade 1 for a student to pass the course.

This articulation avoids implying that every lesson artifact is separately graded or that the capstone is merely a final notebook inspection.

## Risks and safeguards

### Instructor workload

Five individual reviews per learner are practical only because the class is small. Keep checkouts bounded, sample rather than exhaustively inspect lesson evidence, and use the same compact review form across modules.

### Excessive capstone scope

Agent access can encourage requirements to expand because implementation is faster. Each capstone should still ask for one primary claim, a bounded artifact, and a small set of high-value checks. “Do more” should mean stronger evidence and broader failure testing, not a larger software project.

### Public instructor-facing documentation

The repository is public. This document may explain assessment architecture and candidate evidence, but it must not contain hidden answers, unpublished student information, or secret test cases. Learner-facing rubrics should normally be public; only reference solutions and genuinely hidden checks need controlled storage.

### Generic agent rituals

Requiring the same specification template and provenance paragraph five times can become performative. The changing responsibility across modules should keep the agent work tied to the numerical risk of each problem.

### Overreliance on oral defense

The individual checkout strengthens accountability but should sample and confirm the documented evidence, not introduce unannounced content or become a separate high-stakes oral examination. Accommodations need an equivalent route.
