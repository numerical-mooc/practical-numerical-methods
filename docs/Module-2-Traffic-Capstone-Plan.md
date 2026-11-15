<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Module 2 traffic-flow capstone: modernization plan

**Status:** Implemented in the [Traffic Flow Capstone](../book/modules/02-spacetime/10-traffic-flow.ipynb) and its [review chapter](../book/modules/02-spacetime/traffic-capstone-review.md). Both appear in the Module 2 table of contents.

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

**Sensitivity criterion:** changes below **0.1 m/s** in both the evolving speed summaries and the averaged profile difference over two successive refinement comparisons, with the fixed-grid time-step check preserving the conclusion. Treat this as a numerical sensitivity criterion within the model, not a proven absolute-error bound. The private pilot supports extending the ladder through 1,601 points and applying the fixed-grid check at the first grid that passes the two-comparison rule for a scenario. Do not require Richardson extrapolation with a presumed order for the discontinuous patch or its minimum.

The private pilot checked the hand step, vehicle balance, controlled defect, and both refinement comparisons. The original ladder through 801 points leaves one scenario short of two successive passing comparisons. Extending it by one level gives both scenarios enough comparisons, and the fixed-grid time check passes at their candidate resolutions. Local front differences remain visible even after the whole-road profile measure passes. Keep numerical reference results in the private pilot.

## 6. Verdict and assessment

The notebook asks learners to use their existing evidence to write a short engineering verdict covering:

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

The notebook includes short self-check dropdowns. The companion review chapter offers an evidence checklist and sample questions for the individual conversation. The individual checkout samples existing evidence; it does not add a separate report or an unannounced technical task. Keep offering-specific checkpoint and revision logistics outside the notebook.

## Presentation and sequencing

The opening includes a road sketch, engineering brief, side-by-side scenario table, and plots of speed and flux. A paired figure connects density versus distance to speed versus density. Shared-axis baseline density snapshots motivate the refinement comparison. Learners overlay two profiles at a common time and identify a local feature whose behavior the summary statistics can conceal.

[PNM-0006](../DECISIONS.md#pnm-0006-introduce-discrete-conservation-before-the-full-conservation-law-module) distinguishes this restricted positive-characteristic-speed calculation from the full conservation-law treatment in Module 3. Lesson 9 supplies practice with nonlinear conservative updates and steep-front refinement. Lessons 6 and 7 supply the open-boundary conventions.

## What learners can bring to the capstone

| Lesson | Already practiced | Appropriate traffic transfer |
| --- | --- | --- |
| [6: Convection](../book/modules/02-spacetime/06-1d-convection.ipynb) | Old-state slices, backward differences, pointwise versus conservative nonlinear updates, open-boundary telescoping, and checks against known defects. | Reconstruct the flux update and its one-step balance for a new flux. Calculate one small update by hand and explain why a constant state cannot expose a wrong flux. |
| [7: CFL](../book/modules/02-spacetime/07-cfl-condition.ipynb) | Upstream dependence, downstream endpoint updates, convex weights, exact final-time step selection, and a bounded agent brief with independent acceptance cases. | Use the sign and maximum of the traffic characteristic speed to justify inflow, stencil, and step. Have learners explain the numerical requirements and specify the refinement experiment. |
| [8: Diffusion](../book/modules/02-spacetime/08-1d-diffusion.ipynb) | Physical smoothing, coupled space–time refinement, point-update cost, and choosing a grid against a stated target using an exact benchmark. | Predict the work increase and compare cost with sensitivity. Supply the comparison rule and distinguish a change between grids from error against an exact solution. |
| [9: Burgers](../book/modules/02-spacetime/09-1d-burgers.ipynb) | Quadratic flux factorization, preserved bounds, exact observation times, conservation versus profile agreement, nested-grid profile comparisons, and auditing an agent experiment. | Transfer the weighted-average reasoning with a short cue; contrast a road with a periodic grid. Supply the whole-road profile measure and a cue for interpreting local front shape. |

Learners should be able to reconstruct a one-step calculation, explain the boundary choices, and interpret a controlled comparison using these precedents. Give them the traffic-specific sampling and boundary conventions, a cue to factor the new quadratic flux, and instructions for the fixed-grid time-step comparison. Do not assume they can derive a general nonlinear stability result, infer an error bound from two grids, or analyze a discontinuity with the tools of Module 3.

## Completed authoring stages

| Stage | Outcome |
| --- | --- |
| Numerical pilot | Checked the hand step, controlled defect, open-road balance, nested-grid comparisons, and fixed-grid time-step sensitivity. |
| Model and paper exercise | Added the engineering question, scenario and sampling conventions, and notes on speeds, update, balance, and a three-point prediction. |
| Supplied computation and verification | Added the worked update, solver, controlled defect, 51-point estimates, baseline checks, and density snapshots. |
| Agent-assisted investigation | Added the refinement design, bounded brief, pre-run audit, independent profile comparison, and overlay prompt. A private simulated student brief produced runnable experiment cells and reproduced the pilot's candidate choices. |
| Verdict and review | Added the engineering verdict, completion rubric, and self-checks. The companion chapter closes Module 2 and prepares learners to discuss their own evidence. |

The assessment samples numerical reasoning, verification, audit, and interpretation. A well-supported unresolved claim is a valid outcome. Offering-specific interview logistics and numerical reference answers belong in instructor materials.
