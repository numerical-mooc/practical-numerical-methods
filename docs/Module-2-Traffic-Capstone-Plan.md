<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Module 2 traffic-flow capstone: modernization plan

**Status:** Notebook draft in progress. The model, paper exercise, supplied solver, and baseline runs are in place. The agent investigation and verdict remain to be drafted.

## Purpose and scope

Build `book/modules/02-spacetime/10-traffic-flow.ipynb` around this question:

> Can the traffic calculation support the reported minimum and average speeds in both scenarios, and what evidence distinguishes genuine traffic evolution from numerical smearing?

Keep the legacy one-lane traffic model, road length, two scenarios, and six requested speed summaries. Replace answer-box grading with a compact chain of prediction, specification, implementation audit, verification, and a defended verdict.

This follows PNM-0001–0003 and PNM-0007 in [DECISIONS.md](../DECISIONS.md), and the Module 2 proposal in [Assessment and capstone design](Assessment-and-Capstone-Design.md). The [rocket capstone](../book/modules/01-phugoid/05-rocket-capstone.ipynb) supplies the useful structure: engineering brief, independent expectations, provisional computation, verification, recorded agent work, and learner-owned interpretation. Its two-solver comparison and Richardson machinery need not be repeated here.

Learners derive the update on paper, compare it with a worked solution, and run the same supplied solver. They then specify and audit a bounded refinement experiment drafted by an agent, transferring the practices from Lesson 7 to a nonlinear traffic calculation.

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
u(\rho)=u_{\max}(1-\rho/\rho_{\max}),\qquad
F(\rho)=\rho u(\rho),\qquad
a(\rho)=F'(\rho)=u_{\max}(1-2\rho/\rho_{\max}).
\]

Ask learners to derive:

- the units of density, vehicle speed, flux, and characteristic speed;
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

## 3. Run the supplied solver and delegate the refinement experiment

Learners organize their paper notes under four headings: speeds and units, discrete update, vehicle balance, and one-step prediction. They retain their first attempt and add corrections alongside it after comparing with the worked equation and the supplied NumPy step. The three-point example has unequal boundary fluxes and exercises the outlet update.

The notebook supplies the model plots, aligned grid initializer, conservative step, and driver. The driver copies the initial state, holds the leftmost value fixed, checks the positive-speed regime and CFL limit, and adjusts the step to reach the requested time. It returns the final state, actual step, step count, CFL number, accumulated net outflow, and point-update count. The 51-point runs retain the profiles and report the six baseline speeds.

Have learners specify the refinement experiment before contacting an agent. Include the physical patch, grid ladder, observation times, maximum steps, comparison measures, and retained results. Ask the agent to add only unexecuted experiment cells that call the supplied functions. At audit, check that the runs start from fresh initial data, align profiles at the same time and shared positions, and compute changes and cost from the retained arrays. Support chat-only agents by letting learners paste proposed cells after inspection. Learners choose what resolution the evidence supports and write the verdict.

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

Require **one controlled defect**, preferably the plausible update `u(rho) * backward_difference(rho)`. Have learners identify which independent check detects it and why a constant-state test can miss it. A short defective step and bounded comparison suffice; a second production solver or a catalog of defects would duplicate earlier work.

## 5. Investigate resolution, not just six printed answers

Make the baseline runs provisional. Report the six legacy quantities in one table and show a few density profiles at the specified physical times.

Then refine with `nx = 51, 101, 201, 401, 801, 1601` and maximum steps `0.001 / 2**level` h. The same physical patch and output times must be used throughout. This holds each scenario's characteristic CFL bound fixed along its refinement family. Count work as `N * number_of_steps`, following Lesson 8's point-update comparison.

Use two complementary refinement measures:

1. Changes in the requested speed summaries, retaining unrounded values for comparisons.
2. A spatially averaged absolute difference between coarse and fine speed profiles at a shared physical time, with fine data sampled at the coincident coarse nodes and the quadrature stated explicitly.

The mean alone is weak evidence: the linear speed-density relation ties it closely to the discrete density total. While boundary fluxes are nearly equal, that total may barely change even when the profile is smeared or misplaced. A minimum can also settle while the edges remain poorly resolved. Profile comparison therefore has a distinct job.

For the candidate resolution, also halve the time step at fixed grid spacing. This separates a useful time-sensitivity question from the combined space-time refinement path; it does not require a full two-dimensional refinement matrix.

**Proposed acceptance target:** changes below **0.1 m/s** in both the evolving speed summaries and the averaged profile difference over two successive refinement comparisons, with the fixed-grid time-step check preserving the conclusion. Treat this as a numerical sensitivity criterion within the model, not a proven absolute-error bound. The private pilot supports extending the ladder through 1,601 points and applying the fixed-grid check at the first grid that passes the two-comparison rule for a scenario. Do not require Richardson extrapolation with a presumed order for the discontinuous patch or its minimum.

The private pilot checked the hand step, vehicle balance, controlled defect, and both refinement comparisons. The original ladder through 801 points leaves one scenario short of two successive passing comparisons. Extending it by one level gives both scenarios enough comparisons, and the fixed-grid time check passes at their candidate resolutions. Local front differences remain visible even after the whole-road profile measure passes. Keep numerical reference results in the private pilot.

## 6. Verdict and assessment

The final notebook should state:

- what the verification checks establish about the supplied update and whether the agent experiment follows the brief;
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

The opening now includes the supplied speed and flux figure and NumPy/Matplotlib model plots with the assigned density bands. Add scenario snapshots and a refinement comparison with a close-up of a front to relate the scalar measures to the local profile.

PNM-0006 says the full traffic application remains in Module 3, while the assessment document assigns the traffic capstone to Module 2. When this plan is accepted, clarify the boundary in the decision record: Module 2 applies the already-taught conservative finite difference to a restricted positive-characteristic-speed regime; Module 3 develops control volumes, weak solutions, shock speeds, and general numerical fluxes. Do not silently introduce those topics here. The current Lesson 9 already works through conservative Burgers convection, a nonlinear bound from convex weights, and refinement of a steep front. Traffic transfers those ideas to a different flux and an open road. Lesson 6 and Lesson 7 supply the open-boundary conventions.

## What learners can bring to the capstone

| Lesson | Already practiced | Appropriate traffic transfer |
| --- | --- | --- |
| [6: Convection](../book/modules/02-spacetime/06-1d-convection.ipynb) | Old-state slices, backward differences, pointwise versus conservative nonlinear updates, open-boundary telescoping, and checks against known defects. | Reconstruct the flux update and its one-step balance for a new flux. Calculate one small update by hand and explain why a constant state cannot expose a wrong flux. |
| [7: CFL](../book/modules/02-spacetime/07-cfl-condition.ipynb) | Upstream dependence, downstream endpoint updates, convex weights, exact final-time step selection, and a bounded agent brief with independent acceptance cases. | Use the sign and maximum of the traffic characteristic speed to justify inflow, stencil, and step. Have learners explain the numerical requirements and specify the refinement experiment. |
| [8: Diffusion](../book/modules/02-spacetime/08-1d-diffusion.ipynb) | Physical smoothing, coupled space–time refinement, point-update cost, and choosing a grid against a stated target using an exact benchmark. | Predict the work increase and compare cost with sensitivity. Supply the comparison rule and distinguish a change between grids from error against an exact solution. |
| [9: Burgers](../book/modules/02-spacetime/09-1d-burgers.ipynb) | Quadratic flux factorization, preserved bounds, exact observation times, conservation versus profile agreement, nested-grid profile comparisons, and auditing an agent experiment. | Transfer the weighted-average reasoning with a short cue; contrast a road with a periodic grid. Supply the whole-road profile measure and a cue for interpreting local front shape. |

Learners should be able to reconstruct a one-step calculation, explain the boundary choices, and interpret a controlled comparison using these precedents. Give them the traffic-specific sampling and boundary conventions, a cue to factor the new quadratic flux, and instructions for the fixed-grid time-step comparison. Do not assume they can derive a general nonlinear stability result, infer an error bound from two grids, or analyze a discontinuity with the tools of Module 3.

## Reviewable authoring stages

Each stage has its own review artifact. Stage 1 can proceed while the teaching and assessment choices are being reviewed.

| Stage | Review artifact | Ready to move on when |
| --- | --- | --- |
| 1. Pilot the numerical design | Private author calculation and a short design note: independent nonuniform step, constant state, asymmetric boundary-flux check, correct and defective updates, patch alignment, exact times, refinement at all reporting times, and fixed-grid time-step checks. | The defect is detectable with an independent oracle, and the ladder, time check, metric, stopping rule, and work budget support a meaningful verdict even if a target is missed. |
| 2. Draft the brief and prediction | Drafted: model exposition, scenario table, sampling conventions, and a paper exercise with organized notes. | A learner can tell vehicle speed from wave speed, predict upstream dependence and initial minima, and connect the traffic update and balance to Lessons 6–9. |
| 3. Supply the solver and baseline | Drafted: model plots, worked update, runnable solver, hand check, and 51-point runs. Add the controlled-defect exercise next. | The update is inspectable and the hand check exercises the downstream node with unequal boundary fluxes. |
| 4. Draft the investigation | Next: bounded agent brief and audit, baseline profile plot, nested-grid comparison with work counts, fixed-grid time-step comparison, and verdict prompts. | A learner can trace a claim to a table row and a feature in the profile, distinguish the sampling average from a vehicle-weighted average, and report when no tested resolution supports a claim. |
| 5. Review the assessment and publishable source | Short rubric and public self-checks, plus an end-to-end author run and rendered review. Reconcile the assessment document and PNM-0006 only after the choices are accepted. | The individual checkout can sample existing evidence in the planned time; the notebook runs with the provided environment, preserves existing cell IDs where revised, and has no committed outputs or counts. Validate JSON, review the diff, and check the MyST render. |

## Decisions for instructor review

1. **Division of work.** The notebook supplies the step and driver. The agent drafts the refinement experiment from the learner’s brief. The checkout samples the learner’s reasoning, audit, and interpretation.
2. **How much mathematics must students produce?** Recommend requiring the characteristic speed and CFL calculation for each case, a hand update, and a short explanation of the inlet and balance. Give a cue or worked example for the secant factorization and ask learners to explain what the weights guarantee. Keep the full nonlinear perturbation proof outside the assignment. Decide whether the wave-direction prediction should also ask which edge compresses and which spreads; this is a useful qualitative transfer, with the traffic flux concavity made explicit.
3. **What counts as enough resolution?** The pilot supports the proposed 0.1 m/s criterion with the extended ladder. Confirm the work budget and give students a common-axis front plot so they can discuss local differences alongside the whole-road measure. A verdict that a claim remains unresolved is valid when supported by evidence.
4. **Which evidence should anchor the individual interview?** Recommend three compact notebook anchors: a hand prediction or step with its inputs; a named defect and the check that exposes it; and one resolution claim tied to a specific table row and profile feature. Sample two during the interview, asking the learner to point to the evidence and explain what would change under one familiar counterfactual. Treat predictions and provenance as records to discuss, not as proof that work was unaided. Decide whether all learners defend one common anchor or whether both are sampled from their own work. Keep the public self-checks and integrated 1–4 scale; keep actual interview selections outside the public notebook.
5. **Confirm the scope and reporting conventions.** Recommend keeping all six legacy quantities, with the arithmetic mean explicitly defined as an endpoint-inclusive spatial sample average and the initial minima as quick hand checks. Use unrounded values for sensitivity and make displayed precision consistent with the stated target. Keep Module 2 to positive characteristic speeds and conservative finite differences on the open road; reserve control-volume methods, weak solutions, shock speeds, and general numerical fluxes for Module 3.

Stop after one bounded agent contribution, one controlled defect, one refinement investigation, and a short defended verdict. A second solver, a general traffic regime, an additional report, and a new task during the interview are outside this draft.
