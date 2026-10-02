<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Module 3 modernization plan: Riding the wave

**Status:** Proposal for review, dated 2026-10-01. This document combines the audits of the four imported lessons and proposes a coordinated modernization. It does not record adoption of the proposed scope, implement notebook changes, or supersede course decisions.

## 1. Purpose and governing question

Build the module around one question:

> What evidence makes a numerical solution of a conservation law trustworthy when waves change direction, steepen, and form discontinuities?

The module should develop four connected judgments: whether an update respects information propagation, whether it resolves a discontinuity adequately, whether the flux model satisfies its specification, and whether reconstruction improves accuracy without compromising admissibility. Conservation is essential throughout, but never sufficient evidence by itself.

Preserve the traffic-flow narrative and the transition to the Sod shock-tube capstone. Keep the four existing lesson numbers and filenames during modernization; titles may change to express their investigations. The inherited name `13-a-better-model.ipynb` need not dictate a claim that its model is better.

This plan follows [PNM-0001–0003, PNM-0005–0007](../DECISIONS.md), [Notebook-first code architecture](Notebook-First-Code-Architecture.md), and [Assessment and module-capstone design](Assessment-and-Capstone-Design.md). In particular:

- Keep derivations, algorithms, and consequential intermediate states visible in executable notebooks.
- Follow derive–reconstruct–specify–audit–explain, with one bounded agent activity serving each lesson's investigation.
- Select complementary evidence for a stated purpose; avoid repeating a complete solver survey or diagnostic framework in every lesson.
- Use public self-checks and selected Complete/Revise checkpoints; assess the capstone and lesson evidence together under the existing module scale.
- Treat symbolic results, agent code, and library results as claims requiring inspection.

## 2. Starting point, provenance, and boundaries

### Preserved baselines

| New-edition notebook | Legacy source in `../numerical-mooc/lessons/03_wave/` | Retained cells / code cells |
| --- | --- | ---: |
| [11-conservation-law.ipynb](../book/modules/03-wave/11-conservation-law.ipynb) | `03_01_conservationLaw.ipynb` | 54 / 17 |
| [12-convection-schemes.ipynb](../book/modules/03-wave/12-convection-schemes.ipynb) | `03_02_convectionSchemes.ipynb` | 64 / 24 |
| [13-a-better-model.ipynb](../book/modules/03-wave/13-a-better-model.ipynb) | `03_03_aBetterModel.ipynb` | 70 / 35 |
| [14-muscl.ipynb](../book/modules/03-wave/14-muscl.ipynb) | `03_04_MUSCL.ipynb` | 59 / 14 |

The imports removed copyright-header cells, CSS injection and explanatory cells, outputs, and execution counts. Retained source and metadata were preserved. Referenced figures are present, together with the unchanged legacy `traffic.py` needed by Lesson 14. These are source-faithful baselines, not publication-ready lessons.

The evidence base is the supplied Lesson 11 audit and the Lesson 12–14 audits in the import conversation. Numerical findings below summarize those audit runs; they were not regenerated while writing this plan. The runs checked numerical kernels independently, not complete rendered notebook execution. Notebook schema validation was unavailable during import, and the Lesson 13 symbolic workflow was not executed because SymPy was unavailable. These gaps become explicit authoring checks rather than implied successes.

### Prerequisites and unresolved sequencing

Lesson 6 already introduces conservative differences and telescoping balance. Lesson 7 establishes directional dependence and constant-speed stability; Lesson 8 practices choosing evidence and comparing accuracy with work. Reuse those ideas without repeating their full development. Do not transfer a constant-speed perturbation proof unchanged to a nonlinear equation.

Lessons 9 and 10 remain legacy or draft material. The [Module 2 traffic-capstone plan](Module-2-Traffic-Capstone-Plan.md) is a proposal, not an implemented prerequisite. Lesson 11 must therefore supply the short traffic-model bridge it needs, and Lesson 13 must include just enough symbolic-Python guidance to remain understandable if Lesson 9 has not yet been modernized.

PNM-0006 reserves the full conservation-law treatment for Module 3. Its wording about the traffic application needs clarification if the Module 2 capstone proposal is accepted: Module 2 would use a restricted positive-characteristic-speed case; Module 3 develops control volumes, discontinuities, shock propagation, and general interface fluxes. Record that clarification only when adopted.

The legacy `03_05_Sods_Shock_Tube.ipynb` is a separate coding exercise, not one of the four audited lessons. It was read for this plan's capstone bridge but has not received the same import and numerical audit. Its detailed modernization remains a separate work item.

## 3. Coordinated learning progression

| Lesson | Investigation | Main addition | Evidence learners own | Question carried forward |
| --- | --- | --- | --- | --- |
| 11 | Why can a conservative traffic update fail while cars move forward? | Integral balance and density-dependent information speed | A hand update, balance identity, wave-direction prediction, and two distinct failure diagnoses | How can a method handle both wave directions? |
| 12 | Can a growing traffic jam be resolved sharply without impossible densities? | Shock-speed benchmark and a controlled comparison of conservative schemes | Exact-front prediction, matched-time error, bounds, and refinement | Can we reduce smearing without oscillations? |
| 13 | Does a symbolic solution satisfy the model we intended to build? | Model specification and branch admissibility | Independent algebra, substitution residuals, physical constraints, and a conditional model verdict | What must be reconsidered when the flux changes? |
| 14 | Can limited reconstruction improve resolution while retaining conservation and admissibility? | Cell averages, shared interface fluxes, minmod, and SSP RK2 | Reconstruction checks, stage-aware balance, smooth convergence, and shock diagnostics | What additional obligations arise for a system of conservation laws? |

Keep this order. Lesson 13 provides a deliberate model-audit interlude; Lesson 14 must explicitly return to the quadratic LWR flux to isolate the numerical-method question. It must not silently inherit the cubic model or call that model validated.

Allocate theory where it first enables a judgment. Lesson 11 distinguishes shocks from rarefactions qualitatively and explains the smoothness limitation of the chain rule. Lesson 12 derives the jump-speed relation and gives a short characteristic-compression explanation of the selected traffic shock. Lesson 14 introduces Riemann problems, entropy-admissible wave selection at the level needed to interpret them, and exact versus approximate numerical fluxes. A general weak-solution theory or a catalogue of entropy conditions is outside the core module.

## 4. Lesson 11: physical balance and the limits of one-sided transport

### Preserve and correct

Preserve the progression from control-volume conservation to the traffic model, failed FTBS calculation, wave direction, and time-step restriction. Correct the surface-normal convention and replace “gradient” with “divergence” in the Gauss-theorem discussion. Make the one-dimensional balance central:

\[
\frac{d}{dt}\int_{x_L}^{x_R}\rho\,dx
=F(\rho(x_L,t))-F(\rho(x_R,t)).
\]

Separate vehicle speed, flux, and characteristic speed:

\[
V(\rho)=V_{\max}(1-\rho/\rho_{\max}),\qquad
F(\rho)=\rho V(\rho),\qquad
a(\rho)=F'(\rho)=V_{\max}(1-2\rho/\rho_{\max}).
\]

Cars can move forward while disturbances propagate backward. For the concave quadratic flux, the downward stoplight jump produces a rarefaction; the rising ramp steepens. A shock is a discontinuity, not simply a large gradient. Integral balance remains meaningful when pointwise differentiation is unavailable.

### Proposed investigation

1. On paper, derive the balance with units and signs, calculate `F'`, and mark the wave-speed directions over the physical density interval.
2. Reconstruct the conservative FTBS update. Connect its telescoping sum to Lesson 6 rather than presenting discrete conservation as new.
3. Contrast a supported low-density calculation, a mixed-sign case with modest Courant magnitude, and a low-density case with an excessive time step. Use stated physical times and stop failed runs before overflow obscures the first defect.
4. Check one nonuniform hand update, boundary-flux balance, finiteness, density bounds, and selected profiles. Never clip density to conceal failure.
5. Explain supported behavior through the quadratic flux's secant slopes and nonnegative weights. Distinguish this bounds argument from a complete nonlinear stability or convergence theorem.

The inherited high-density case violated density bounds after two steps; the excessive-CFL case did so after one. The reduced-density example remained bounded through 40 steps. These are candidate public failure demonstrations, not accuracy benchmarks.

**Agent activity:** learners specify unexecuted diagnostic cells around their own update. The agent may not change the numerical method, clip values, or write the verdict. Learners explain which failure each check detects and why a small balance residual cannot rescue a failed run.

**Exit criterion:** learners can distinguish a wrong stencil direction from an excessive time step and explain why conservation plus a plausible plot is insufficient. General interface fluxes and shock-speed calculations remain for subsequent lessons.

## 5. Lesson 12: shock resolution, bounds, and controlled comparisons

### Independent benchmark

Retain the red-light problem with left density 5, right density 10, `u_max=1`, `rho_max=10`, and initial front at `x=3`. Derive the jump-speed relation from a balance around the moving discontinuity:

\[
s=\frac{F(\rho_R)-F(\rho_L)}{\rho_R-\rho_L}
=-\frac12,\qquad x_s(t)=3-\frac12t.
\]

The characteristic speeds are 0 and −1; neither is the shock speed. State the time interval before boundaries invalidate the reference. Specify the point-sampling convention at the jump for these finite-difference comparisons; later finite-volume comparisons need cell averages instead.

### Proposed investigation

Make Lax–Friedrichs and Lax–Wendroff the core comparison. Derive each visibly and implement each once as a small notebook-local function. Retain MacCormack as a bounded extension whose distinct purpose is avoiding an explicit flux Jacobian, rather than a third complete investigation.

Compare methods and CFL settings at the same physical time. The legacy 40-step runs reach `T=2` at nominal CFL 1 and `T=1` at nominal CFL 0.5, so they do not isolate time-step effects. Reducing the LF time step at fixed spacing also changes its numerical dissipation; explain why this is not an ordinary refinement of a fixed spatial operator.

Use an exact-front overlay for position and shape, integrated absolute error for overall discrepancy, extrema for admissibility, and each method's numerical boundary flux for discrete balance. Refine a short aligned grid sequence at fixed nominal CFL. Record actual characteristic CFL throughout and distinguish nominal settings from achieved values.

Prior audit maxima over the original histories were:

| Method | Nominal CFL 1 | Nominal CFL 0.5 |
| --- | ---: | ---: |
| Lax–Friedrichs | 10.000 | 10.000 |
| Lax–Wendroff | 10.840 | 11.158 |
| MacCormack | 11.260 | 11.547 |

The histories have different final times, so this table documents bounds violations, not a controlled accuracy ranking. All methods satisfied their discrete interior flux balances to roundoff. At nominal CFL 1, overshoots raised the actual maximum CFL to about 1.168 and 1.252 for LW and MacCormack. A finer grid reduced integrated error without eliminating overshoots in the tested cases.

Qualify second-order accuracy as a smooth-solution property; do not expect a second-order shock convergence rate. Correct the Taylor expansion's stated expansion point, blanket claims against first-order methods, and MacCormack's predictor-boundary handling before reuse.

**Agent activity:** draft a matched-time comparison harness, including a deliberate mismatched-time case that the harness must detect. The learner supplies verified update functions and owns execution and interpretation.

**Exit criterion:** a verdict supported separately by conservation, error, and admissibility evidence. The unresolved sharpness-versus-oscillation problem motivates Lesson 14.

## 6. Lesson 13: symbolic candidates and model admissibility

### Turn the central defect into an explicit investigation

Retain the proposed cubic flux as a candidate model:

\[
F(\rho)=u_{\max}\rho(1-A\rho-B\rho^2).
\]

Start with a model contract: endpoint values, coefficient units, positive interior density for the optimum, nonnegative and nonincreasing vehicle speed, an upper speed bound, and a true maximum of flux. Distinguish hypothetical parameter choices from measured observations. A more flexible formula is not automatically a more accurate model.

Introduce dimensionless density `r=rho/rho_max`, speed ratio `k=u_star/u_max`, and coefficients `alpha=A*rho_max`, `beta=B*rho_max**2`. The jam condition becomes `alpha+beta=1`. On paper, combine the stationarity and prescribed-speed conditions to obtain

\[
A\rho^\star=2-3k.
\]

For the inherited `k=0.7`, the right-hand side is −0.1. A positive `A` necessarily gives a negative intended optimum. Independent algebra produced:

| Branch | A | B | Implied optimum density |
| --- | ---: | ---: | ---: |
| Legacy selection | 0.014611 | 0.008539 | −6.844289 |
| Other branch | −0.017111 | 0.011711 | 5.844289 |

The selected curve's physical maximum instead occurs near density 5.703574 with speed `0.638889*u_max`. The other branch matches the desired positive-density optimum but initially increases vehicle speed, reaching `1.00625*u_max`. Neither satisfies the complete intended contract at 0.7.

### Proposed investigation

Use SymPy to produce candidates, then substitute every branch into the original equations and check physical constraints over the full density interval. Check whether stationary points are the intended maxima. Treat `A=0` separately because the elimination divides by `A`; do not infer existence or uniqueness merely by counting equations and unknowns.

Preserve 0.7 as a deliberately examined failure. Follow it with one compatible parameter choice selected and verified in an authoring pilot. Do not silently change parameters to make the legacy claim appear correct. Reduce repeated pretty-printing cells and retain only the symbolic operations that advance the reasoning. Convert accepted coefficients explicitly to floating point for numerical work.

Compare the accepted candidate with the quadratic model using one already-taught method in a regime supported by both fluxes, matched data and final times, and resolution checks. Recalculate `F'`, stencil suitability, and CFL. The legacy low-density FTBS run was bounded, but changing `rho_light` to 10 produced density about 10.164 after one step. “Only change the flux function” is therefore an incomplete numerical contract.

Explain which quantities are held fixed in model comparisons: a fixed `u_star/u_max` does not remove proportional scaling of capacity with `u_max`. Different traffic evolution demonstrates model sensitivity, not empirical improvement. Validation against real traffic requires data beyond this lesson.

**Agent activity:** learners write a model-admissibility specification; the agent drafts a branch audit. Require checks capable of rejecting both negative optimum density and the speed-bound violation. The learner verifies the algebra independently and accepts or rejects each candidate.

**Exit criterion:** a defensible distinction among an algebraic solution, an admissible model, a verified numerical solution of that model, and an empirically validated model.

## 7. Lesson 14: limited reconstruction with a justified time step

### Establish the finite-volume contract

Make the move from point values to cell averages explicit. Define cell faces, centers, physical cells, and ghost cells. The inherited code places 100 centers across the road but evolves only 98 interior entries, holding the end cells fixed; the modernization must remove this geometric ambiguity.

Derive conservation from one numerical flux shared by adjacent cells. Show why the inherited first-order flux reproduces LF on a uniform grid. Distinguish exact Godunov flux, local Rusanov flux, and the legacy coefficient `dx/dt`. The inequality bounding wave speeds does not make these definitions interchangeable.

**Recommended design for the modernized core:** use a wave-speed-based Rusanov flux for both constant and limited-linear reconstruction, with the same SSP RK2 integrator when isolating the effect of reconstruction. Retain the original LF/Euler equivalence as a short bridge. Keeping the numerical flux independent of the chosen step makes the spatial and temporal roles clearer. This recommendation needs a numerical pilot and acceptance; it is not an implemented change.

For the quadratic scalar traffic flux, define the speed bound explicitly over the interface-state interval. Derive or cite a sufficient restriction for the exact reconstruction, flux, and time integrator used. Do not carry the first-order CFL setting over by analogy or claim a universal `C<=0.5` guarantee from experiments alone.

### Reconstruction and time integration

On paper, reconstruct a constant profile, a linear ramp, an extremum, and a jump. Show that a centered linear reconstruction preserves its cell average and that minmod chooses the smaller same-sign slope or zero. Use an unlimited reconstruction only as a short failure contrast. Correct the Godunov-theorem discussion: its linearity restriction matters; nonlinear limiting is not a contradiction of the theorem.

Explain SSP RK2 as forward-Euler steps and averaging, with a restriction inherited from the chosen spatial update. Check intermediate stages as well as final states. The prior audit supplied a concrete regression case for the inherited scheme:

```
rho0 = [0., 0., 0., 5., 7., 7.]
rho_max = 10; u_max = 1
dx = dt = 0.04
fixed endpoint values = (0., 7.)
```

One original MUSCL step gives a minimum density of `-0.101984375`. This is a public illustration of an overbroad guarantee, not a hidden assessment test. The successful red-light animation cannot establish general bounds preservation. Also fix integer-dtype truncation in `minmod()`.

### Evidence with distinct purposes

Use one smooth benchmark with an independently known solution and exact cell-average initialization to test convergence order. A periodic constant-speed translation is a suitable bounded verification case if its boundary treatment is introduced explicitly. Do not use the shock to prove second-order accuracy; limiters may also reduce local order near smooth extrema.

Use the red-light case for front location, integrated cell-average error, density bounds, total variation, and stage-weighted boundary-flux balance. State what changing total variation means under the chosen boundary conditions rather than imposing an unqualified rule on every open-boundary problem.

The original `T=1.2`, nominal-CFL-1 audit found:

| Cells | LF/Euler integrated absolute error | Legacy MUSCL/RK2 integrated absolute error |
| --- | ---: | ---: |
| 100 | 0.253914 | 0.316284 |
| 200 | 0.094544 | 0.134379 |
| 400 | 0.047272 | 0.067196 |

These errors use the exact cell averages of the shock at `x=2.4`. Both calculations remained bounded on that problem and conserved to roundoff, but the legacy MUSCL calculation had larger errors. Reconstruction and time integration both change in this comparison, so it does not isolate a limiter's effect or establish a general method ranking.

**Agent activity:** review a bounded diagnostic implementation or consequential change. Require reconstruction checks, stage-aware balance, a known indexing defect, and the inherited negative-density counterexample. The learner supplies independent expectations and decides what is verified.

**Exit criterion:** evidence for the chosen method's accuracy and admissibility within a stated contract, with the remaining limits of the scalar analysis explicit.

## 8. Module-wide verification and code conventions

Use consistent notation: `V` for vehicle speed, `a=F'` for scalar characteristic speed, `s` for shock speed, `F` for physical flux, and a visibly distinct numerical interface flux. Avoid using the same symbol for Courant number and reconstruction slope. Retain familiar names in small functions where this aids continuity, with explicit parameter meanings.

| Evidence | Primary purpose | Limitation to state |
| --- | --- | --- |
| Independent nonuniform one-step calculation | Signs, indexing, old-state use, flux formula | Does not establish long-time accuracy |
| Constant-state preservation | Consistency and boundary implementation | Many defective schemes also pass |
| Discrete boundary-flux balance | Shared-flux cancellation and bookkeeping | Does not validate the flux model or resolve the profile |
| Bounds, finiteness, actual CFL, and stage checks | Expose unsupported or inadmissible evolution | Passing is not proof of sufficient accuracy |
| Exact solution and matched-time comparison | Quantitative error for that benchmark | Must match point values or cell averages and boundary assumptions |
| Controlled refinement | Resolution sensitivity and appropriate observed order | No assumed second-order rate across shocks |
| Constraint and branch checks | Mathematical-model admissibility | Not validation against observations |
| A known defect that a check detects | Sensitivity of the verification process | Not exhaustive correctness |

Use the update's own quadrature and boundary fluxes. In Lesson 11, sum over the nodes actually evolved. In Lesson 14, sum physical cell averages times cell width, excluding ghosts. For RK2, accumulate the half-weighted fluxes from both stages. Do not substitute a trapezoidal integral or final-state flux into an unrelated exact discrete identity.

Implement methods once per notebook with their bodies visible; avoid a general-purpose solver framework. A small explicit flux callable is justified when an experiment truly varies the flux. Do not move all algorithms into `src/` simply to shorten the notebooks. Reassess the imported `traffic.py`: either keep its two short definitions visible locally or graduate them deliberately to a tested standalone file under `src/` with the established download/import explanation. The present adjacent legacy file is a baseline dependency, not an accepted architecture decision.

Use matched physical initial conditions and output times, float copies, explicit boundary conventions, and minimal state storage. Show selected static profiles by default. Keep animations only where motion adds information; include the final state and physical-time labels, avoid hidden plotting globals, and do not allow axis limits to hide failure.

For cost comparisons, report updated cells or nodes, steps, and flux/reconstruction stages separately. A two-stage method does more work per step, and a method with a Jacobian has different work from one without it. Do not present a raw stage count as an exact runtime ratio.

## 9. Bridge to the Sod shock-tube capstone

Retain the capstone question already proposed in the assessment design:

> Does the candidate conservative solver resolve the Riemann problem without violating the governing physics?

The legacy exercise specifies a tube from −10 to 10 m, a diaphragm at zero, initial states `(rho,u,p)=(1,0,100000)` and `(0.125,0,10000)` in SI units, `gamma=1.4`, and output at `T=0.01 s`. It introduces the Richtmyer method. Preserve these source conditions as the starting point for a separate capstone audit; do not confuse pressures given in kN/m² with values in Pa or silently replace them with nondimensional textbook data.

The four lessons do not yet teach the full Euler system. Supply an explicit capstone bridge covering:

- primitive and conserved states, `U=(rho, rho*u, E)`;
- pressure `p=(gamma-1)*(E-(rho*u)**2/(2*rho))` and the energy convention;
- the three-component flux and characteristic speeds `u-c`, `u`, `u+c`;
- shock, contact, and rarefaction roles, and boundary conditions valid for the selected time interval;
- positivity of density and pressure, including intermediate states;
- an independently sourced exact Riemann reference, verified before learners use it, with the sampling convention matched to the candidate solver.

Recommend a bounded adversarial review of a supplied or agent-produced Richtmyer candidate, preserving the legacy method and introducing its two-step update transparently. Do not require learners to derive an exact Euler solver or implement a second full MUSCL solver for this first modernization. A MUSCL comparison can be an optional extension after the scalar-to-system issues are taught; scalar bounds arguments do not automatically protect Euler pressure.

Require a model/interface specification, hand checks of variable conversion and flux, density/pressure checks, boundary-flux balances for all three conserved components, quantitative exact-solution comparison, and a short refinement study. Include one controlled defect or additional bounded case to prevent acceptance based on one familiar plot. The learner records material agent contributions and gives the final verdict.

Pilot the reference calculation, wave-position extraction, error measures, grid ladder, and achievable tolerances before fixing the learner brief. Keep reference answers and controlled instructor material out of this public plan. Do not import or number the capstone as part of implementing the four lessons without that separate task being agreed.

## 10. Authoring sequence and acceptance gates

### Stage A — agree the coordinated scope

Review the proposed lesson questions and boundaries, MacCormack's extension status, the model-audit role of Lesson 13, the Lesson 14 flux/time-step design, and the capstone bridge. Record consequential adopted choices in `DECISIONS.md`; keep pending choices visibly pending. Reconcile the Module 2 traffic boundary only if that capstone proposal is adopted.

### Stage B — pilot the numerical evidence

Reproduce the audit findings before using them as teaching examples. Establish exact-reference conventions, supported boundary/time intervals, finite-difference and finite-volume totals, and scale-aware floating-point tolerances. Verify the compatible cubic model and the new Lesson 14 stability contract. Select small experiment sets whose outcomes support the intended claims. Resolve failures before polishing prose; do not manufacture the expected outcome by clipping or selective plotting.

### Stage C — modernize Lessons 11 and 12

Write the physical balance, failure diagnoses, shock benchmark, and controlled comparisons. Add learner reconstruction, bounded agent briefs, and verdict prompts. Review both lessons together so that conservation, CFL, and failure checks accumulate rather than restart. Keep outputs and execution counts empty in the working notebooks.

### Stage D — modernize Lessons 13 and 14

Build the branch audit around independently derived constraints. Then return explicitly to the quadratic model and develop finite-volume reconstruction with justified boundaries and time integration. Keep the smooth convergence and shock experiments complementary. Review the four-lesson arc for workload, repeated explanations, and missing prerequisites.

### Stage E — develop the capstone separately

Import and audit the legacy assignment, establish a reliable reference, draft the learner contract and Euler bridge, and pilot the adversarial-review workload. Align its evidence and rubric with PNM-0003. Grades reward a defensible audit and judgment, not extra methods or decorative output.

### Stage F — validate and integrate the book

For each notebook:

- Preserve existing cell IDs and unrelated metadata; use triple-single-quoted docstrings for revised Python functions.
- Validate JSON and notebook schema in an environment with the required dependencies.
- Execute from a fresh kernel, including deliberate-failure demonstrations handled so the published notebook completes reliably; then clear outputs and counts.
- Review code and narrative together, checking formulas, units, figures, physical times, links, and prerequisite claims.
- Move bibliographic entries into `book/references.bib`, use MyST citations, and replace handwritten equation numbers with semantic labels and generated references.
- Update obsolete kernel metadata and resolve dependency distribution deliberately. Preserve source attribution through repository-appropriate provenance and licensing rather than recreating removed per-notebook banners.
- Verify that local assets and intended figure content survive rendering; replace inaccurate figures when the revised explanation requires it.
- Add ready lessons to `book/myst.yml` deliberately, then build from `book/` with `npx --yes --package=mystmd@1.10.1 myst build --html` and inspect rendered mathematics, tables, figures, and cross-references.

Full notebook execution, schema validation, and rendering are publication gates; the import checks alone do not satisfy them. No commit, push, or publication follows automatically from this plan.

## 11. Completion criteria and scope limits

The four-lesson modernization is complete when learners can trace each main claim from an independent expectation through a visible computation to appropriate evidence, with no unresolved mathematical or implementation defect undermining that claim. Each lesson must include one meaningful bounded agent activity and a learner-owned verdict, execute reliably, and meet the book's structural and rendering checks.

The complete module additionally needs the independently reviewed Sod capstone and its explicit Euler bridge. Completion of the four lessons alone should not be reported as completion of that assessment work.

Keep unstructured grids, multiple alternative Riemann solvers, WENO and other limiter catalogues, extensive symbolic-parameter classification, empirical traffic calibration, general entropy theory, and production solver architecture outside the core. They are possible later investigations, not prerequisites for a rigorous answer to this module's question.

## Supporting references for authoring

The current notebooks and their cited legacy sources remain the primary source record. During implementation, verify bibliographic details and add needed entries to the book bibliography. Two sources consulted during the Lesson 14 audit clarify consequential distinctions:

- [Clawpack Riemann book: approximate solvers](https://www.clawpack.org/riemann_book/html/Approximate_solvers.html), for exact Godunov versus LF and local Rusanov constructions.
- [Strong stability preserving methods](https://www.sspsite.org/), for the conditional relationship between forward-Euler properties and SSP time integration.

These references support the method discussion; they do not certify the particular legacy implementation or replace the proposed numerical and analytical checks.
