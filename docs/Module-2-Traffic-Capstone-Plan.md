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

PNM-0006 says the full traffic application remains in Module 3, while the assessment document assigns the traffic capstone to Module 2. When this plan is accepted, clarify the boundary in the decision record: Module 2 applies the already-taught conservative finite difference to a restricted positive-characteristic-speed regime; Module 3 develops control volumes, weak solutions, shock speeds, and general numerical fluxes. Do not silently introduce those topics here. The current Lesson 9 already works through conservative Burgers convection, a nonlinear bound from convex weights, and refinement of a steep front. Traffic transfers those ideas to a different flux and an open road. Lesson 6 and Lesson 7 supply the open-boundary conventions.

## What learners can bring to the capstone

| Lesson | Already practiced | Appropriate traffic transfer |
| --- | --- | --- |
| [6: Convection](../book/modules/02-spacetime/06-1d-convection.ipynb) | Old-state slices, backward differences, pointwise versus conservative nonlinear updates, open-boundary telescoping, and checks against known defects. | Reconstruct the flux update and its one-step balance for a new flux. Calculate one small update by hand and explain why a constant state cannot expose a wrong flux. |
| [7: CFL](../book/modules/02-spacetime/07-cfl-condition.ipynb) | Upstream dependence, downstream endpoint updates, convex weights, exact final-time step selection, and a bounded agent brief with independent acceptance cases. | Use the sign and maximum of the traffic characteristic speed to justify inflow, stencil, and step. Supply the interface and let learners fill in the numerical requirements. |
| [8: Diffusion](../book/modules/02-spacetime/08-1d-diffusion.ipynb) | Physical smoothing, coupled space–time refinement, point-update cost, and choosing a grid against a stated target using an exact benchmark. | Predict the work increase and compare cost with sensitivity. Supply the comparison rule and distinguish a change between grids from error against an exact solution. |
| [9: Burgers](../book/modules/02-spacetime/09-1d-burgers.ipynb) | Quadratic flux factorization, preserved bounds, exact observation times, conservation versus profile agreement, nested-grid profile comparisons, and auditing an agent experiment. | Transfer the weighted-average reasoning with a short cue; contrast a road with a periodic grid. Supply the whole-road profile measure and a cue for interpreting local front shape. |

Learners should be able to reconstruct a one-step calculation, explain the boundary choices, and interpret a controlled comparison using these precedents. Give them the traffic-specific sampling and boundary conventions, a cue to factor the new quadratic flux, and instructions for the fixed-grid time-step comparison. Do not assume they can derive a general nonlinear stability result, infer an error bound from two grids, or analyze a discontinuity with the tools of Module 3.

## Reviewable authoring stages

Each stage has its own review artifact. Stage 1 can proceed while the teaching and assessment choices are being reviewed.

| Stage | Review artifact | Ready to move on when |
| --- | --- | --- |
| 1. Pilot the numerical design | Private author calculation and a short design note: independent nonuniform step, constant state, asymmetric boundary-flux check, correct and defective updates, patch alignment, exact times, refinement at all reporting times, and fixed-grid time-step checks. | The defect is detectable with an independent oracle, and the ladder, time check, metric, stopping rule, and work budget support a meaningful verdict even if a target is missed. |
| 2. Draft the brief and prediction | First notebook chunk: model and scenario table, model plot, sampling conventions, and a short paper prompt. | A learner can tell vehicle speed from wave speed, predict upstream dependence and initial minima, and connect the traffic update and balance to Lessons 6–9. |
| 3. Draft the solver task and audit | Second chunk: compact interface, fill-in numerical requirements, bounded agent brief, and a small set of checks. Provide runnable setup and one deliberately defective step; decide whether to provide the complete driver. | The workflow works from a fresh notebook with a chat-only agent as well as an agent with notebook access. The reference step and balance oracle do not simply reuse the code under review. One check exercises the downstream node with unequal boundary fluxes. |
| 4. Draft the investigation | Third chunk: baseline summary table and profile plot, nested-grid comparison with point-update counts, one time-step comparison at fixed grid, and verdict prompts. Supply the repetitive plotting and comparison scaffolds. | A learner can trace a claim to a table row and a feature in the profile, distinguish the sampling average from a vehicle-weighted average, and report when no tested resolution supports a claim. |
| 5. Review the assessment and publishable source | Short rubric and public self-checks, plus an end-to-end author run and rendered review. Reconcile the assessment document and PNM-0006 only after the choices are accepted. | The individual checkout can sample existing evidence in the planned time; the notebook runs with the provided environment, preserves existing cell IDs where revised, and has no committed outputs or counts. Validate JSON, review the diff, and check the MyST render. |

## Decisions for instructor review

1. **Who supplies the driver?** Recommend keeping one bounded agent task to preserve the Module 2 progression: supply model setup, comparison scaffolds, and the controlled defect; let the agent draft the small time-marching function from a learner-completed numerical brief. If the priority is a more uniform unsupervised experience, supply a readable driver and give everyone the same bounded agent audit or correction task. Either route uses the code as inspectable evidence; authorship, style, and passing generated tests carry no credit on their own.
2. **How much mathematics must students produce?** Recommend requiring the characteristic speed and CFL calculation for each case, a hand update, and a short explanation of the inlet and balance. Give a cue or worked example for the secant factorization and ask learners to explain what the weights guarantee. Keep the full nonlinear perturbation proof outside the assignment. Decide whether the wave-direction prediction should also ask which edge compresses and which spreads; this is a useful qualitative transfer, with the traffic flux concavity made explicit.
3. **What counts as enough resolution?** Treat 0.1 m/s as a proposed sensitivity target, not a promise of two-decimal accuracy. A planning spot check with a trapezoidal whole-road profile comparison found that Scenario A's six-minute minimum changes by about 0.143 m/s from 201 to 401 points and 0.026 m/s from 401 to 801. The proposed ladder therefore gives only one consecutive passing comparison for that quantity. Decide after the full pilot whether to extend the ladder or make an unresolved claim an expected valid outcome. Define where the fixed-grid time check is applied and how to report a whole-road profile pass when local front differences remain visible. A whole-road average can hide localized differences; pair it with a common-axis front plot and avoid claiming the front is resolved from the scalar alone.
4. **Which evidence should anchor the individual interview?** Recommend three compact notebook anchors: a hand prediction or step with its inputs; a named defect and the check that exposes it; and one resolution claim tied to a specific table row and profile feature. Sample two during the interview, asking the learner to point to the evidence and explain what would change under one familiar counterfactual. Treat predictions and provenance as records to discuss, not as proof that work was unaided. Decide whether all learners defend one common anchor or whether both are sampled from their own work. Keep the public self-checks and integrated 1–4 scale; keep actual interview selections outside the public notebook.
5. **Confirm the scope and reporting conventions.** Recommend keeping all six legacy quantities, with the arithmetic mean explicitly defined as an endpoint-inclusive spatial sample average and the initial minima as quick hand checks. Use unrounded values for sensitivity and make displayed precision consistent with the stated target. Keep Module 2 to positive characteristic speeds and conservative finite differences on the open road; reserve control-volume methods, weak solutions, shock speeds, and general numerical fluxes for Module 3.

Stop after one bounded agent contribution, one controlled defect, one refinement investigation, and a short defended verdict. A second solver, a general traffic regime, an additional report, and a new task during the interview are outside this draft.
