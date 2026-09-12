<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Lesson 7: stability analysis new-edition plan

**Revision date**: Sep. 12, 2026
**Status**: Planned; implementation pending.

## Status and source

This author-approved and revised plan incorporates the critique by Claude (Opus 5 High) of an original modernization proposal by Codex (GPT-6 Astra Light) and the subsequent lesson outline. It follows [PNM-0007: Develop numerical judgment through focused investigations](../DECISIONS.md#pnm-0007-develop-numerical-judgment-through-focused-investigations). The lesson notebook has not yet been modernized.

The imported [lesson](../book/modules/02-spacetime/07-cfl-condition.ipynb) is the legacy `lessons/02_spacetime/02_02_CFLCondition.ipynb`, renamed to follow the new edition's sequential filenames. The opening copyright cell, closing CSS introduction and embedding cell, and code outputs/execution counts were removed. Its dependent `figures/CFLcondition.png` was copied unchanged. The notebook remains outside book navigation pending revision.

Sources inspected locally: all four legacy Module 2 notebooks and its README; the new edition's [Lesson 6](../book/modules/02-spacetime/06-1d-convection.ipynb) and [phugoid oscillation lesson](../book/modules/01-phugoid/02-oscillation.ipynb); [course decisions](../DECISIONS.md), especially PNM-0001, PNM-0002, PNM-0006, and PNM-0007; and the [traffic capstone plan](Assessment-and-Capstone-Design.md#module-2-traffic-flow). Mathematical predictions below follow from the displayed updates. Authoring should add suitable primary references to `book/references.bib` and use MyST citations.

## Central question and scope

**Why did refining the spatial grid improve the Lesson 6 calculation, make it an exact grid shift at one setting, and then destroy it?**

The lesson should answer that question rigorously and equip learners to audit a stability claim. Convex weights are the single analytical spine; direct substitution of an alternating perturbation establishes sharpness and supplies an independently calculable numerical prediction. CFL geometry gives a physical interpretation of the bound already established algebraically.

Reuse Lesson 6's `advance_linear_convection(u0, c, dx, dt, num_steps)`, its `gaussian_profile()` when a smooth profile is needed, and its existing refinement evidence. The opening requires no new solver. The legacy plotting functions are not the numerical implementation for the new lesson; one appears later only as an explicitly identified audit specimen.

**Note**: the `advance_linear_convection()` function from Lesson 6 is using a double loop, whereas afterwards in the Lesson 6 narrative, we explain how to perform the calculation using vectorized array operations. Keep the same interface and boundary behavior, replacing only the inner spatial loop.

Aim for approximately 4,800–5,200 markdown words, with 4,500–5,500 as a working planning range rather than a fixed requirement. Substance comes from the reasoning, falsifiable predictions, and defended conclusion. The agent activity is designed around that investigation, not appended as a generic parameter sweep.

## Conceptual corrections to carry into authoring

- The actual Lesson 6 experiment uses `nx_trials = [41, 81, 101, 121]`, `dt=0.02`, `L=2`, and `c=1`. Its Courant numbers are 0.4, 0.8, 1.0, and 1.2. Use these, not the legacy grid settings.
- For constant positive speed with the stated FTBS update and compatible boundary treatment, the stability interval includes equality: `0 <= C <= 1`. At `C=1`, the update shifts grid values exactly one point per step, explaining the existing `nx=101` result.
- Unchanged code is not evidence that a failure cannot be an implementation defect. Audit the update before attributing behavior to the method.
- Computing a time step from a parameter named “CFL” does not establish that its value, stencil direction, time direction, or boundary treatment is appropriate.
- Fixed step counts with changing time steps compare different physical times. This compromises a comparison; it is not itself an instability.
- Show extrema and growth without clipping the plot axis. Lesson 6 already avoids fixed vertical limits in its refinement figure, so reuse that evidence rather than proposing this as a new repair there.
- A sharper square pulse is not enough to establish convergence or accuracy. Lesson 6 already supplies a smooth-profile error and observed-order study; refer back to it.
- Characteristics describe propagation in the PDE. The numerical domain of dependence is determined by the repeated stencil. Keep these meanings distinct.
- Failure of convex weights means the non-amplification argument no longer applies; it is not a general proof of instability. Use a specific growing perturbation or counterexample for the stronger claim.
- The legacy lesson asserts:
  - > "Now, it doesn't matter how many points we use for the spatial grid: the solution will always be stable!"
   - That claim is false in at least five ways, and every one of them is checkable with the tools this lesson builds: `sigma > 1` is accepted silently; `c < 0` needs a flipped stencil, not a smaller step; `c = 0` divides by zero; fixed nt with computed dt compares different physical times; and a CFL-obeying FTCS scheme blows up anyway.

### Legacy implementation provenance

The legacy prose gives `dt=0.25` where the code uses `0.025`; both functions use `range(1, nt)` and thus advance 19 steps when labeled as 20; and the CFL function documents a nonexistent `dt` argument. Its plotting is coupled to evolution and clips the vertical range. These are authoring/provenance findings, not a corrections narrative for the learner. Reusing Lesson 6's solver avoids carrying them into the main computation. If the legacy function is reproduced as an audit specimen, label its provenance and make its actual step count explicit in the audit.

## Lesson outline

### 1. The threshold you already crossed — about 450 words

Return to the Lesson 6 experiment and its existing results.

| Grid points | 41 | 81 | 101 | 121 |
| --- | --- | --- | --- | --- |
| Courant number | 0.4 | 0.8 | 1.0 | 1.2 |

**On paper:** calculate these numbers and predict which run fails. Reuse the square-pulse calculation and report actual elapsed time, number of steps, `dx`, `dt`, and extrema. Identify the puzzling `nx=101` result as something to explain, rather than introduce another exact-shift experiment detached from preceding work.

### 2. What stability asks — about 650 words

Perturb one interior point by `1e-3`. Advance the original and perturbed states with the same inflow and track

\[
E^n=\max_i|u_{b,i}^n-u_{a,i}^n|.
\]

Compare `C=0.8, 1.0, 1.2` in one logarithmic plot. The stable case controls the disturbance, the unit-Courant case transports it without changing its maximum, and the supercritical case amplifies it. Select a grid and point placement that keep the disturbance away from the outflow over the observation interval. Use the existing solver for repeated single steps if needed; keep the diagnostic code small and visible.

Distinguish the short experiment, which illustrates amplification, from the definition: stability requires a mesh-independent amplification bound over a fixed physical interval under stated assumptions. A fixed-number-of-steps comparison at different C values is an amplification diagnostic, not a common-final-time accuracy comparison. Report its times explicitly.

Recall the phugoid amplitude growth learners already observed. For forward Euler on the undamped oscillator, the amplitude factor per step is `sqrt(1+(omega*dt)^2)`, but over fixed T the amplification is bounded by `exp(omega^2*dt*T/2)`, which tends to one under refinement. Thus that artifact does not establish failure of fixed-interval stability. Contrast it with the supercritical transport mode developed next. Keep this callback brief, without a new eigenvalue derivation.

Limit the consistency/convergence discussion to three sentences: name consistency and stability, state their implication for convergence in the appropriate linear well-posed setting, and distinguish convergence from meeting an accuracy requirement on a particular grid.

### 3. Why the bound is 0 <= C <= 1 — about 1,100 words

For positive constant speed, rewrite the update:

\[
u_i^{n+1}=(1-C)u_i^n+C u_{i-1}^n,
\qquad C=c\Delta t/\Delta x.
\]

**On paper:** hand-calculate an update and identify when its weights are nonnegative. Apply the same update to the difference e between two runs with identical prescribed inflow:

\[
\|e^{n+1}\|_\infty\leq\|e^n\|_\infty
\qquad(0\leq C\leq1).
\]

Explain range preservation and perturbation non-amplification as distinct consequences of the same convex weights. State the inflow and outflow treatment. At `C=1`, recover the grid shift in Lesson 6; at `C=0`, the update leaves the state unchanged. Do not imply that the method is generally exact away from this special alignment.

For the other direction, substitute an alternating perturbation directly:

\[
e_i^n=A_n(-1)^i,\qquad A_{n+1}=(1-2C)A_n.
\]

No complex exponentials or Fourier-series prerequisites are needed. Learners independently calculate `|1-2C|` and its nth power. For positive speed and `C>1`, the magnitude grows geometrically. Explain the refinement implication: with fixed supercritical C and fixed physical T, the number of steps grows as the grid is refined, so no uniform amplification bound exists. A sufficiently short T and an interior observation region allow this argument without inflow contamination.

For a finite-domain measurement after n steps, sample more than n grid cells from the left inflow, and use an alternating initial perturbation covering its whole backward stencil. Choose the grid and measurement region for the largest planned step count. Measure relative to initial amplitude; do not confuse the single-point perturbation's maximum with the alternating-mode formula.

An optional **Going further** dropdown may state

\[
|G(\theta)|^2=1-4C(1-C)\sin^2(\theta/2)
\]

for a Fourier mode on an infinite or periodic constant-coefficient grid, briefly defining theta as the phase increment per grid cell. No main argument or required exercise depends on this result.

### 4. The physical picture—and its limit — about 500 words

Use the imported CFL figure after the algebraic argument. Trace the physical backward characteristic and explain containment in the numerical domain of dependence. Connect this picture to the uncontaminated measurement region above.

Explain CFL containment as a necessary condition for convergence of the relevant explicit hyperbolic schemes, not a universal sufficient stability test. Show the forward-time/centered-space update's weights `(C/2, 1, -C/2)` and one compact run at `C=0.5` that demonstrates growth despite geometric containment. Specify initial data, boundaries, observation interval, and measured quantity; verify the counterexample during authoring. Do not use the alternating mode for this contrast: centered differencing annihilates that mode. Choose data that excite growth, and account for influence from both boundaries if using a finite-domain interior measurement.

Negative weights invalidate the convexity proof; the observed growing solution is separate evidence. Keep this a short counterexample, avoiding a second Fourier derivation or full second-solver lesson.

### 5. Living within the bound — about 650 words

For positive speed and `0 < C_target <= 1`, give the recipe for a common positive final time:

\[
\Delta t_{\rm limit}=C_{\rm target}\Delta x/c,\qquad
N=\lceil T/\Delta t_{\rm limit}\rceil,\qquad
\Delta t=T/N.
\]

Report the realized Courant number. Refer to Lesson 6's smooth-profile error and observed-order evidence instead of rebuilding the refinement study.

Explain briefly that negative speed needs forward spatial differencing and a right inflow boundary. Reducing a positive time step cannot repair backward differencing in that direction. For zero speed, no transport update is needed. If auditing the literal legacy formula `dt=sigma*dx/c`, note that negative c produces negative dt: distinguish that implementation behavior from advancing forward in time with a downwind stencil.

| Change at fixed T and C | Approximate consequence |
| --- | --- |
| Halve dx | Twice as many grid points |
| Halve the permissible dt | Twice as many steps |
| Combine both | Four times the work |

Assume work proportional to points times steps; this is an operation-count scaling, not a promised wall-clock ratio. Connect it to Module 1's accuracy-versus-cost judgment. State the leading numerical-diffusion coefficient `c*dx*(1-C)/2` for smooth solutions in one sentence to explain sharpening toward `C=1`; defer its derivation to diffusion.

### 6. Audit a stability claim — V1: REJECTED

The object under audit is the legacy assertion:

> Now, it doesn't matter how many points we use for the spatial grid: the solution will always be stable!

Present `linear_convection_cfl()` only as a clearly marked historical audit specimen. The learner's computation continues to use the inspected Lesson 6 solver. This is an investigation of the conditions supporting an assurance, not a request to repair or generalize a legacy function.

**Independent preparation.** Before contacting the agent, learners record their Courant-number calculations, one-step arithmetic, convex-weight argument, and alternating-mode predictions for `C=0.8, 1.0, 1.05, 1.2`. These are their acceptance references.

**Hypothesis generation.** Give the agent the specimen and quoted assertion, requesting reasoned conditions under which the assurance fails, with no code. Supply a bounded prompt rather than the full worked notebook. Ask learners to classify the answer:

| Finding | What it challenges |
| --- | --- |
| `sigma > 1` accepted without a check | The method's stability restriction |
| Negative c in the literal time-step formula | Forward-time interpretation; a positive-step FTBS variant also has the wrong spatial bias |
| Zero c | An undefined time-step calculation, not growth of a computed solution |
| Fixed nt with changing dt | Comparability of physical final times, not stability itself |
| FTCS growth despite CFL containment | Generalizing CFL sufficiency to other schemes, not the specific FTBS function |

**Bounded experimental code.** Ask the agent to add only unexecuted diagnostic cells for the prescribed alternating-perturbation experiment. Protect the numerical method and existing cells. Require fresh state for each C, identical inflow between paired runs, actual step/time reporting, a measurement region valid through the last step, normalized amplitudes, and measured per-step growth. The learner supplies the analytical prediction afterward rather than asking the agent to manufacture both prediction and evidence. Prescribe a short interval such as 20 steps and a large enough grid; handle vanishing amplitudes explicitly if the chosen cases are later changed.

**Audit and execute.** Inspect time-level use, step counts, perturbation construction, measurement region, and normalization before running. Compare measured amplification with `|1-2C|^n`. Reuse the unit-Courant shift and the short FTCS example. Check the zero- and negative-speed hypotheses by inspecting or safely evaluating the time-step calculation; do not require a full signed-speed solver. Bound additional agent suggestions rather than implementing every proposed test. A constant state alone cannot expose this instability, so learners must explain why the chosen perturbation matters.

**Your verdict.** Replace “always stable” with a qualified statement naming the PDE, positive speed, space-time discretization, Courant interval, and boundary assumptions. Distinguish stability, input validity, fair comparisons, and accuracy. Record which agent hypotheses were accepted, revised, or rejected and why, together with a concise provenance record. Use self-checks rather than expanding this into another long harness assignment.

### 7. What comes next — about 200 words

Preview the same question for diffusion: when are the update's weights nonnegative? The weights become `r, 1-2r, r`, while the permissible time step scales with `dx^2`. Reserve the derivation for that lesson. Burgers later combines transport and diffusion in one update, giving the convex-weight reasoning a further purpose.

## Material deliberately deferred

- No full von Neumann derivation in the core lesson; only the optional stated result above.
- No repeated convergence study: reuse Lesson 6's L1 error and observed-order evidence.
- No modified-equation derivation here; develop it with physical diffusion.
- No extended Lax theorem treatment, periodic-boundary tutorial, or general signed-speed solver.
- Legacy defects remain provenance or part of the explicitly labeled audit specimen, not a narrative of discarded code.

## How the rest of Module 2 should build on this

| Stage | Existing material | Proposed role in the stability arc |
| --- | --- | --- |
| Lesson 6 (Module 2 Lesson 1): convection | Finite differences, truncation error, nonlinear updates; new edition adds discrete conservation and diagnostic blind spots | Motivate failure and preserve the distinction between stability and conservation. Do not repeat its full audit activity. |
| Lesson 7 (Module 2 Lesson 2): stability | Grid-refinement failure, CFL diagram, time-step rescaling | Establish perturbation growth, convex weights, amplification, stencil direction, and controlled experiments. |
| Lesson 3: diffusion | Centered second derivative, stated restriction, square pulse, substantial animation tutorial | Reuse convex weights and the alternating perturbation; distinguish physical smoothing from numerical damping and examine refinement cost. |
| Lesson 4: viscous Burgers | Nonlinear convection plus diffusion, SymPy, analytical comparison, periodic boundaries, timing comparisons | Combine restrictions, verify boundary indexing and reference compatibility, and judge accuracy before performance. |
| Traffic capstone | Conservative density update and two operating scenarios in the current capstone plan | Apply characteristic-speed and boundary reasoning, balance checks, and refinement evidence to an engineering verdict. |

### Diffusion: reuse the reasoning, change the scaling

For `r=nu*dt/dx^2`, the explicit centered diffusion update has weights `r, 1-2r, r`. Derive `0 <= r <= 1/2` from the weights and use the alternating perturbation to obtain `G=1-4r`. The general mode factor `G=1-4r sin^2(theta/2)` can remain an extension. This reinforces the method of analysis while revealing a different time-step scaling: halving dx quarters the permissible dt. At fixed duration, one-dimensional work grows approximately eightfold on refinement, compared with fourfold for explicit convection, assuming work proportional to grid points times steps.

Use a decaying sine mode with compatible boundaries as independent evidence for physical decay and discretization error. Do not carry over the finite-wave-speed diagram as an explanation for a parabolic PDE. The legacy code calls r a “CFL limit”; distinguish the diffusion number explicitly. Keep animation subordinate to numerical reasoning, and avoid making a video encoder installation central to the lesson.

### Burgers: the restrictions interact

The legacy Burgers code chooses dt from diffusion alone. For the displayed pointwise backward-convection/centered-diffusion update with nonnegative u, let `C_i=u_i*dt/dx`. Its weights are `C_i+r, 1-C_i-2r, r`; a sufficient convex-weight bound is

\[
\max_i C_i+2r\leq1.
\]

Thus satisfying the separate bounds `C<=1` and `r<=1/2` does not necessarily make their combined explicit update safe. Derive a combined step bound, track the speed range, and explain the assumptions. This argument supplies a range-preservation condition for this nonlinear update, not a general nonlinear perturbation-stability theorem. If the flux or time integrator changes, derive its condition afresh. Signed speeds require an appropriate directional discretization.

Audit the periodic grid before refinement: the legacy uses an inclusive `[0,2*pi]` grid but updates both endpoints as independent neighbors. Choose either unique periodic points or an explicitly synchronized duplicate endpoint. Also verify that the stated two-Gaussian reference satisfies the intended periodic boundary problem over the run interval before using it as an exact benchmark. A formula satisfying the PDE is not enough to establish compatibility with a boundary condition.

SymPy should support inspected differentiation and residual checks; performance comparisons should follow equivalence checks and use current measured results. The lesson can revisit the conservative/pointwise distinction without importing Module 3's full weak-solution theory.

### Traffic and Module 3: maintain the boundary between modules

The traffic capstone plan already identifies the relevant speed as `F'(rho)`, not vehicle speed `V(rho)`. Lesson 7 should provide the conceptual tools to distinguish information speed, choose a spatial bias, and explain why a time-step number alone cannot certify a solver. Use the capstone to extend the constant-speed reasoning to state-dependent characteristic speeds, leaving the full traffic derivation to that application.

PNM-0006 reserves control volumes, weak solutions, shock speeds, and general numerical fluxes for Module 3. Preserve that scope. A stable nonlinear calculation can still propagate a discontinuity incorrectly if its discrete conservation is wrong. Neither stability nor conservation alone certifies the whole computation.

## Implementation and verification plan

1. Author from the current Lesson 6 and this focused outline, following PNM-0007. Reuse established definitions visibly, with enough setup for the published notebook to execute independently; do not hide the update in a new module.
2. Develop the perturbation diagnostic and elementary proof before the agent audit. Use triple-single-quoted docstrings, semantic equation labels, MyST citations, and the new edition's plotting conventions.
3. Execute a temporary notebook copy. Check the actual Lesson 6 Courant numbers, unit-Courant shift, maximum-norm non-amplification, alternating-mode predictions, uncontaminated observation region, exact step/time bookkeeping, and a reproducible FTCS counterexample. Treat numerical values supplied in the critique as checks to reproduce, not as already verified outputs of the new notebook.
4. Audit the agent briefs for bounded access and genuinely independent learner expectations. Ensure the verdict distinguishes evidence about this scheme from claims about stability in general.
5. Keep the source notebook output-free, validate JSON, review the diff, and inspect the rendered equations, figure, and activity flow before adding it to book navigation. Build with the repository's pinned MyST command.
6. Extend the reasoning as diffusion and Burgers are imported, preserving the downstream scope above. Record any further consequential sequencing changes in `DECISIONS.md`.
