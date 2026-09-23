<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Module 2 traffic-flow capstone: modernization plan

**Status:** Proposal for review; not an implemented assignment or an accepted decision change.

## Purpose and scope

Build `book/modules/02-spacetime/10-traffic-flow.ipynb` around this question:

> Can the traffic calculation support the reported minimum and average speeds in both scenarios, and what evidence distinguishes genuine traffic evolution from numerical smearing?

Keep the legacy one-lane traffic model, road length, two scenarios, and six requested speed summaries. Replace answer-box grading with a compact chain of prediction, specification, implementation audit, verification, and a defended verdict.

This follows PNM-0001–0003 and PNM-0007 in [DECISIONS.md](../DECISIONS.md), and the Module 2 proposal in [Assessment and capstone design](Assessment-and-Capstone-Design.md). The [rocket capstone](../book/modules/01-phugoid/05-rocket-capstone.ipynb) supplies the useful structure: engineering brief, independent expectations, provisional computation, verification, recorded agent work, and learner-owned interpretation. Its two-solver comparison and Richardson machinery need not be repeated here.

The progression in responsibility is specific: the learner derives the numerical requirements and completes a bounded solver specification; the agent drafts its implementation; the learner audits and accepts or rejects it. Lesson 7 already practices specification and audit for constant-speed transport. Here the learner transfers those practices to a nonlinear flux and an engineering claim.

## 1. Establish a precise problem before delegation

Preserve the legacy settings:

| Setting | Scenario A | Scenario B |
| --- | --- | --- |
| Road length | 11 km | 11 km |
| Maximum density | 250 cars/km | 250 cars/km |
| Free-flow speed | 80 km/h | 136 km/h |
| Background and inflow density | 10 cars/km | 20 cars/km |
| Dense-patch density | 50 cars/km | 50 cars/km |
| Baseline grid and step | 51 points; 0.001 h | 51 points; 0.001 h |
| Requested summaries | Minimum at 0; average at 3 min; minimum at 6 min | Minimum at 0; average and minimum at 3 min |

Define the patch as the physical interval **2.2 <= x < 4.4 km**, with an explicit endpoint convention. This reproduces the baseline slice `rho0[10:20]` and preserves its physical width under refinement. Use aligned grids with 50, 100, 200, ... intervals and verify patch membership; floating-point comparisons must not silently change the endpoint convention.

Resolve the source's undefined average explicitly: use the **arithmetic mean of vehicle speed over all grid points**, including the endpoints, for the legacy-style summaries. Describe it as a spatial sample average, not an average over cars or a predicted journey speed. Its endpoint weighting changes under refinement; it is a discrete approximation, not an exact road integral. This is a new explicit convention, not a recovered Open edX grading rule.

Keep internal units in kilometers and hours; convert reported speeds to m/s. Request exact output times, not the nearest stored step. State that the two scenarios change both free-flow speed and background density, so their difference cannot be attributed to the speed parameter alone.

## 2. On paper: derive what the code must implement

Use the existing model exposition, correcting the distinction between

\[
V(\rho)=V_{\max}(1-\rho/\rho_{\max}),\qquad
F(\rho)=\rho V(\rho),\qquad
a(\rho)=F'(\rho)=V_{\max}(1-2\rho/\rho_{\max}).
\]

Ask learners to derive:

- the units and limiting values of speed and flux;
- the characteristic speed and its sign over each scenario's density interval;
- the conservative update
  \[
  \rho_i^{n+1}=\rho_i^n-\frac{\Delta t}{\Delta x}
  [F(\rho_i^n)-F(\rho_{i-1}^n)];
  \]
- the positive-speed CFL restriction based on the maximum of `a` over the admissible density interval;
- the telescoping balance over the updated points; and
- the two initial minimum velocities and their unit conversions.

Both scenarios stay below half the maximum density in the intended stable calculation. This supports backward differencing and prescribed left inflow. Update through the rightmost point; do not fix both endpoints or introduce a periodic road.

Give a short worked bridge from Lesson 6's flux difference and Lesson 7's upstream dependence. Do not ask learners to discover an unfamiliar general conservation-law solver. For a rigorous short explanation of preserved bounds, factor the quadratic flux difference into a density difference times its secant slope, then show that the update is a convex combination under the stated bound. Do not transfer the constant-speed maximum-norm perturbation proof to a nonlinear equation without justification.

## 3. Specify, delegate, and audit one small solver

Supply a compact interface and requirement table. Have learners complete the numerical requirements and map them to acceptance evidence before contacting an agent. Keep the solver local to the working notebook, with visible flux and update expressions.

The contract should cover:

- endpoint-inclusive uniform grid, floating-point input copy, explicit model parameters and constant left inflow;
- conservative old-time-level flux differencing, including the downstream endpoint;
- a requested maximum time step, a CFL check, and a step count chosen to reach the requested final time;
- refusal of unsupported density ranges, invalid parameters, or an excessive step count, with an explanatory failure;
- no clipping of negative densities or overshoots to conceal a failed calculation;
- returned final density, actual spacing and step, completed steps, realized CFL bound, accumulated boundary flux, balance diagnostic, and point-update work;
- no input mutation, hidden global parameters, or unnecessary solution history.

For these scenarios the initial and inflow density bounds provide a fixed characteristic-speed bound. A general adaptive time integrator is unnecessary. Repeated calls can produce the few required snapshots.

Authorize the agent to add only the named unexecuted implementation and small check cells. Preserve the learner's equations, predictions, and existing cells. Reuse the rocket workflow of inspecting code before execution, requesting focused corrections, and recording material contributions. The agent must not choose the accepted resolution or write the verdict.

## 4. Establish complementary evidence

Use a small set of checks with distinct purposes:

| Evidence | What it can expose | What it cannot establish |
| --- | --- | --- |
| Hand-calculated nonuniform one-step case | Wrong flux, wrong slice, mixed time levels, or substitution of vehicle speed for wave speed | Accuracy of a long calculation |
| Constant state and initial speed checks | Broken boundary handling, initialization, or unit conversion | Correct motion of a density patch |
| Cumulative discrete balance | Lost or created vehicles due to update or boundary errors | Correct flux law or resolved profile |
| Density bounds and CFL report | Unsupported regime, overshoots, or unstable settings | Adequate spatial accuracy |
| Space-time refinement | Sensitivity of reported quantities and profile to discretization | Validation against real traffic |

Use the balance convention already taught in Lesson 6. For `N+1` nodes, node zero is prescribed and nodes 1 through N are updated:

\[
M^n=\Delta x\sum_{i=1}^{N}\rho_i^n,\qquad
R^n=M^n-M^0+\sum_{k=0}^{n-1}\Delta t_k
[F(\rho_N^k)-F(\rho_0^k)].
\]

Explain that this is a discrete total with the scheme's own quadrature. A trapezoidal integral does not satisfy this exact telescoping identity. Record the actual old-state boundary fluxes, and independently recompute the residual from the returned state and accumulated flux. Scale the floating-point tolerance to the quantities involved.

Require **one controlled defect**, preferably the plausible update `V(rho) * backward_difference(rho)`. Have learners identify which independent check detects it and why a constant-state test can miss it. A short defective step and bounded comparison suffice; a second production solver or a catalog of defects would duplicate earlier work.

## 5. Investigate resolution, not just six printed answers

Make the baseline runs provisional. Report the six legacy quantities in one table and show a few density profiles at the specified physical times.

Then refine with `nx = 51, 101, 201, 401, 801` and maximum steps `0.001 / 2**level` h. The same physical patch and output times must be used throughout. This holds each scenario's characteristic CFL bound fixed along its refinement family. Count work as `N * number_of_steps`, following Lesson 8's point-update comparison.

Use two complementary refinement measures:

1. Changes in the requested speed summaries, retaining unrounded values for comparisons.
2. A spatially averaged absolute difference between coarse and fine speed profiles at a shared physical time, with fine data sampled at the coincident coarse nodes and the quadrature stated explicitly.

The mean alone is weak evidence: the linear speed-density relation ties it closely to the discrete density total. While boundary fluxes are nearly equal, that total may barely change even when the profile is smeared or misplaced. A minimum can also settle while the edges remain poorly resolved. Profile comparison therefore has a distinct job.

For the candidate resolution, also halve the time step at fixed grid spacing. This separates a useful time-sensitivity question from the combined space-time refinement path; it does not require a full two-dimensional refinement matrix.

**Proposed acceptance target:** changes below **0.1 m/s** in both the evolving speed summaries and the averaged profile difference over two successive refinement comparisons, with the fixed-grid time-step check preserving the conclusion. Treat this as a numerical sensitivity criterion within the model, not a proven absolute-error bound. Establish the final grid ladder and target through an authoring pilot before putting them in the learner brief. Do not require Richardson extrapolation with a presumed order for the discontinuous patch or its minimum.

A preliminary local calculation during planning found appreciable minimum-speed sensitivity on the baseline grid: the A minimum at six minutes changed by about 1.0 m/s between 51 and 801 points, and the B minimum at three minutes by about 0.76 m/s. These are exploratory findings supporting the investigation, not verified reference answers. The complete checks above and the profile/time sensitivity study remain to be run before finalizing the assignment.

## 6. Verdict and assessment

The final notebook should state:

- whether the proposed solver meets its contract and what checks support that decision;
- which tested resolution supports each scenario's reported quantities;
- the remaining resolution sensitivity and computational work;
- what the profiles reveal that the means and minima conceal;
- any agent proposal corrected or rejected, and the evidence behind that action; and
- what remains uncertain about the numerical solution and about the idealized equilibrium traffic model.

Separate numerical smearing from physical dispersal of congestion. This model contains no explicit diffusion term; do not add viscosity merely to incorporate Lesson 8. Likewise, changes in this model's free-flow-speed parameter are not evidence for a real speed-limit policy.

Replace the legacy 30-point grading with the existing integrated module scale:

| Grade | Traffic-specific interpretation |
| --- | --- |
| 3: Complete | Required checkpoint and capstone evidence is complete; specification, audit, complementary checks, refinement, and verdict are defensible. |
| 4: Complete with distinction | The same core is complete, with independent judgment about a consequential uncertainty or limitation; for example, demonstrating why stable averages conceal profile error. Extra methods or more plots are not required. |
| 2: Developing | A substantial explainable attempt has an unresolved gap that weakens the claim; the learner identifies a concrete revision. |
| 1: Not assessable | Essential evidence is missing or consequential parts cannot be explained. |

Use short public self-check prompts for defense. The individual checkout samples existing evidence; it does not add a separate report or an unannounced technical task. Keep offering-specific checkpoint and revision logistics outside the notebook.

## Presentation and sequencing

Use a compact two-panel introductory plot: vehicle and characteristic speeds versus density, and flux versus density, with the assigned density range marked. Later use one figure of scenario snapshots and one refinement comparison, each answering a stated question. All can be generated with NumPy and Matplotlib; no custom illustration or animation is required.

PNM-0006 says the full traffic application remains in Module 3, while the assessment document assigns the traffic capstone to Module 2. When this plan is accepted, clarify the boundary in the decision record: Module 2 applies the already-taught conservative finite difference to a restricted positive-characteristic-speed regime; Module 3 develops control volumes, weak solutions, shock speeds, and general numerical fluxes. Do not silently introduce those topics here. Lesson 9 is still a legacy-style notebook, so the capstone should not depend on unimplemented modernization of that lesson.

## Authoring sequence and stop point

1. Verify the numerical design in a temporary author calculation: independent step checks, balance, defect detection, fixed physical initialization, profile refinement, and time sensitivity. Set a realistic target and a bounded grid ladder. Keep reference solutions outside public instructor documents.
2. Draft the learner-facing brief, short derivation bridge, specification scaffold, audit prompts, evidence requirements, and rubric in `10-traffic-flow.ipynb`. Preserve existing cell IDs where cells are revised. Add no complete delegated solution or fabricated outputs.
3. Review the complete workload against PNM-0007 and the preceding lessons. Update the assessment document and clarify PNM-0006 only for choices actually accepted. Validate notebook structure and rendering, and execute supplied setup/illustration cells separately while leaving committed outputs empty.

Stop when there is one coherent capstone with one bounded delegation, a small check set, one refinement investigation, and a defensible verdict. Additional solvers, general mixed-sign traffic regimes, congestion-arrival events, and optimization are outside this first modernization.
