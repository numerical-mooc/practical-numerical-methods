<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Module 4 ("Spreading out"): look-ahead after the Lesson 8 modernization

**Revision date**: Sep. 19, 2026
**Status**: Planning note. No Module 4 authoring has started.
**Compiled with**: Claude Opus 5

## Status and source

This note records what the modernized [Lesson 8](../book/modules/02-spacetime/08-1d-diffusion.ipynb) consumes from the legacy diffusion module, what remains for that module to do, and the technical findings that should shape it. It follows [PNM-0007](../DECISIONS.md#pnm-0007-develop-numerical-judgment-through-focused-investigations), whose first consequence is to inspect the actual preceding lessons before planning new material.

Sources inspected: the seven legacy notebooks `04_00`–`04_06` in `lessons/04_spreadout` of the [`legacy-archive-2026`](https://github.com/numerical-mooc/numerical-mooc/tree/legacy-archive-2026) archive (about 12,200 markdown words and 1,100 lines of code); the modernized Lesson 8; [PNM-0001](../DECISIONS.md), PNM-0002, PNM-0003 and PNM-0007; and the [Lesson 7 modernization plan](Module-2-Stability-Modernization.md).

Every numerical result below was measured in a scratch session, not estimated. The parameters are given in the reproduction notes at the end. Treat them as checks to reproduce during authoring, not as verified outputs of any new notebook.

## Where Lesson 8 leaves the legacy module

| Legacy notebook | Status after Lesson 8 |
| --- | --- |
| `04_00_Python_Function_Quirks` | Python names and mutability. Belongs in the python-essentials appendix, not a lesson. |
| `04_01_Heat_Equation_1D_Explicit` | **Largely consumed.** Its stability content is a stencil-weights figure and the assertion that the solution "will develop growing errors" for `sigma > 1/2`. Lesson 8 derives the bound from convex weights, proves a maximum-norm perturbation bound, and supplies the growth mechanism. Surviving material: parabolic classification, the physical heat framing with material properties, **Neumann boundary conditions**, and the observation that diffusion propagates boundary information instantly while an explicit stencil moves it one point per step. |
| `04_02_Heat_Equation_1D_Implicit` | Intact, and better motivated: Lesson 8 quantifies the cost of the explicit restriction. |
| `04_03_Heat_Equation_2D_Explicit` | Stability follows from the same convex-weight argument. Reuse the reasoning; do not re-derive it. |
| `04_04_Heat_Equation_2D_Implicit` | Intact. Its linear system is where direct solves stop being cheap. |
| `04_05_Crank-Nicolson` | Its convergence studies partly duplicate Lesson 8. Its analytic rod solution forces a fudge: the initial gradient is so sharp that the study starts at `t = 1` to avoid resolving it. |
| `04_06_Reaction_Diffusion` | Intact as a capstone, and the hardest thing in the course to verify. |

**The module thesis has to change.** It can no longer be "introduce diffusion and solve the heat equation several ways." Lesson 8 performs the introduction more rigorously than the legacy module did. What remains is sharper and more practical: *escape the explicit time-step limit, and verify what you cannot check by hand.*

## Findings that should shape the module

### 1. The Lesson 8 benchmark cannot be reused for comparing methods

FTCS on the decaying-sine benchmark benefits from error cancellation: the leading temporal and spatial error terms carry opposite signs and cancel at a particular diffusion number. Maximum error at `nx = 81`, `T = 1`:

| `r` | Sine benchmark | Manufactured solution |
| ---: | ---: | ---: |
| 0.0913 | 2.05e-05 | **4.62e-09** |
| 1/6 | **1.56e-09** | 1.07e-05 |
| 0.2 | 9.08e-06 | 1.54e-05 |
| 0.3 | 3.63e-05 | 2.95e-05 |
| 0.5 | 9.08e-05 | 5.78e-05 |

Each problem has a sweet spot, and they sit at different values of `r`. Lesson 8 uses `r = 0.2`, near the sine benchmark's, so the errors it reports are flattered by cancellation. A Module 4 comparison run on the same benchmark would reach a conclusion that does not generalize.

**Author decision (2026-09-19): the `r = 1/6` cancellation is addressed in Module 4, not in Lesson 8.** Lesson 8 stays focused on its own question. Module 4 is where method comparison makes the phenomenon consequential, and where naming it prevents a false conclusion.

### 2. "Explicit beats implicit" is a trap waiting on that benchmark

The spatial error floor — the error remaining as the time step goes to zero — measured with Crank-Nicolson at 20,000 steps:

| `nx` | Spatial floor | FTCS at `r = 0.2` |
| ---: | ---: | ---: |
| 41 | 1.82e-04 | 3.63e-05 |
| 81 | 4.54e-05 | 9.08e-06 |
| 161 | 1.13e-05 | 2.27e-06 |

FTCS at `r = 0.2` is consistently *better than the spatial floor of its own grid*, which is only possible through cancellation. At a target of 1e-5, FTCS reaches the target on `nx = 161` even though that grid cannot resolve 1e-5 in space alone. A naive comparison would report that the explicit method wins.

### 3. Unconditional stability is not efficiency

Cost to reach maximum error at or below 1e-5 at `T = 1`:

| Method | Grid | Steps | Interior point-solves |
| --- | ---: | ---: | ---: |
| FTCS | `nx = 161` | 8,192 | 1,302,528 |
| BTCS | `nx = 321` | 32,768 | 10,452,992 |
| Crank-Nicolson | `nx = 161` | **32** | **5,088** |

Backward Euler removes the step-size *limit*, not the accuracy requirement. It remains first order in time, so it needs small steps anyway and loses outright — to the explicit method as well as to Crank-Nicolson. Crank-Nicolson wins by a factor of about 256 in point-solves; charging a tridiagonal solve three times an explicit update still leaves it roughly 85 times ahead.

This is a better module-level result than "implicit schemes are unconditionally stable," and it is exactly the accuracy-versus-cost question Lesson 8 teaches learners to ask. Authoring should reproduce these numbers with a defensible work model before relying on them.

### 4. Neumann boundary conditions are the untouched gap

Lesson 8 uses Dirichlet conditions throughout. Implementing a zero-flux condition with a one-sided first-order difference is the classic defect: the solution looks entirely plausible while global accuracy silently drops from second order to first. Only a convergence study on a problem with nonzero flux exposes it. This is the strongest available candidate for Module 4's first lesson, and it reuses the verification instrument rather than adding new theory.

### 5. Manufactured solutions replace the legacy's analytic fudge

The legacy Crank-Nicolson lesson starts at `t = 1` because its analytic rod solution has an initial gradient too sharp to resolve. A manufactured solution removes that compromise entirely, and it is the only practical reference for Neumann data, for two dimensions with mixed boundary conditions, and for Gray-Scott. If Lesson 8 introduces a manufactured-solution harness, Module 4 uses it repeatedly. That is depth accumulating across lessons rather than new technique per lesson, which PNM-0007 favors.

## Consequences for module design

- **Do not modernize `04_01` as a standalone lesson.** Fold its survivors — parabolic framing, physical properties, Neumann conditions — into the module opener, and spend the first lesson on boundary conditions rather than rediscovering FTCS.
- **Use manufactured solutions as a working tool, not as new content to teach again.**
- **Plan the work-model seam deliberately.** Lesson 8 counts interior point updates. That measure stops being comparable as soon as a linear solve enters. The module needs an honest extension — cost per step for a banded solve against an explicit update — designed rather than improvised.
- **Scientific libraries arrive here.** *Author decision (2026-09-19): Module 4 uses scientific libraries heavily.* This is the point PNM-0001's third layer describes: learners understand the method well enough to choose, configure and validate a library implementation. Nobody should hand-code the Thomas algorithm now. The authentic practice is calling a banded solver and verifying it, which also fits the course's agentic framing.
- **Two dimensions make the cost argument decisive** (roughly sixteen times the work per refinement, and a system that is no longer tridiagonal), and form the natural on-ramp to Module 5's iterative solvers.

## Open questions

1. **Where does the manufactured-solution harness belong** — capping Lesson 8, or opening Module 4? Lesson 8 is where the absence of an exact solution first becomes a real limitation, which argues for introducing it there. But the tool now serves two modules, so the placement is a sequencing decision, not a lesson-local one.
2. **What evidence standard applies to the Gray-Scott capstone?** It has no exact solution, no analytic reference, and no obvious invariant. Deciding what a learner must produce there determines how much verification machinery the earlier lessons must build.
3. **What is the module's work model**, stated precisely enough to compare an explicit update with a banded solve?

## Reproduction notes

All measurements used `L = 2`, `nu = 0.3`, `T = 1`, the maximum norm over the final grid, and the Lesson 8 time-selection rule (round the step count up, then adjust the step to reach `T` exactly).

- Sine benchmark: `u(x,0) = 1 + sin(pi x / L)`, exact solution `1 + exp(-nu (pi/L)^2 t) sin(pi x / L)`.
- Manufactured solution: `u_m(x,t) = 1 + exp(-t) cos(pi x / L)`, with source `f = (nu (pi/L)^2 - 1) exp(-t) cos(pi x / L)` and time-dependent Dirichlet values taken from `u_m`. Boundary values are imposed at the new time level; the source is evaluated at the old time level.
- BTCS and Crank-Nicolson were run as a theta-scheme with `scipy.linalg.solve_banded` on the interior unknowns.
- The cost table searched step counts over powers of two only, so its step counts are indicative rather than minimal.
