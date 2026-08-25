---
title: Practical Numerical Methods
subtitle: Engineering computation in the agentic era — 2026 edition
---

A problem-driven, executable introduction to numerical methods for engineering and applied science.

Numerical methods turn mathematical models into computations that help us understand and design the physical world. But a computed answer is not automatically a trustworthy answer. We need to know what problem was solved, which assumptions entered the model, how numerical error affects the result, and what evidence supports our conclusions.

**Practical Numerical Methods** develops that judgment through real engineering models, transparent algorithms, computational experiments, and evidence of correctness. You will work in scientific Python, first building important methods where you can see every step, then connecting those ideas to reusable software and established scientific libraries.

## A new edition for a new computational practice

This course began in 2014 as an open, connected course taught across several universities and offered as a MOOC. Its distinctive strength was a problem-driven progression: begin with a physical model, derive a numerical method, implement it, study convergence and stability, and interpret the result. The aircraft, traffic-flow, diffusion, and elliptic-problem narratives of the [legacy course](https://github.com/numerical-mooc/numerical-mooc) remain the foundation of this edition.

The computational setting, however, has changed. Engineers now work not only by writing code directly, but also by using mature scientific libraries and directing AI agents that can implement, refactor, test, and optimize software. This 2026 edition is therefore more than a syntax update. It prepares you to **specify, delegate, inspect, test, verify, and communicate** computational work while remaining responsible for the engineering judgment behind it.

Code generation may be cheap; trustworthy numerical evidence is not. An agent can propose a solver, but it cannot relieve you of deciding whether the solver addresses the intended model, respects its physical constraints, converges as expected, or produces a result fit for purpose.

## What you will learn

By working through the course, you will learn to:

- translate an engineering problem into variables, equations, units, assumptions, initial and boundary conditions, and success criteria;
- implement foundational numerical methods clearly enough to understand their behavior and failure modes;
- choose and justify methods using accuracy, stability, conservation, conditioning, and computational cost;
- write bounded, testable specifications for work delegated to a coding agent;
- inspect code and results for errors in signs, indexing, units, boundaries, state, precision, and complexity;
- verify computations using exact or manufactured solutions, refinement studies, residuals, conservation laws, limiting cases, and independent implementations; and
- communicate methods, evidence, provenance, limitations, and uncertainty to an engineering audience.

## How the course works

Jupyter notebooks are the executable chapters of this book. Each notebook interleaves the model, mathematical reasoning, implementation, experiments, verification, and interpretation. Important algorithms appear transparently in the notebook before stable, reused code moves into a small course module. Scientific-library and agent-produced results are treated as claims to investigate, not authorities to accept.

Each module follows a recurring practice:

1. **Model** the physical or engineering system.
2. **Specify** what the computation must do and how success will be judged.
3. **Implement or delegate** a bounded piece of computational work.
4. **Inspect** the code, assumptions, dependencies, and intermediate results.
5. **Verify and validate** with mathematical and physical evidence.
6. **Communicate** the conclusion, uncertainty, provenance, and remaining risks.

You will sometimes write a method yourself, sometimes use a professional library, and sometimes supervise an agent. In every case, you remain responsible for the result.

## The course journey

The new edition is being rebuilt in public, one executable chapter at a time, following the durable problem-based arc of the original course:

1. **Phugoid motion:** ordinary differential equations, time integration, convergence, and stability through the oscillatory flight of a glider.
2. **Space and time:** finite-difference solutions of partial differential equations, beginning with one-dimensional convection and diffusion.
3. **Riding the wave:** conservation laws, traffic flow, shocks, numerical diffusion, dispersion, and high-resolution schemes.
4. **Spreading out:** explicit and implicit methods for diffusion, boundary conditions, two-dimensional problems, and reaction–diffusion patterns.
5. **Relax and hold steady:** elliptic problems, iterative linear solvers, convergence, and computational performance.

The first chapter begins with the physics of [phugoid motion](./modules/01-phugoid/01-theory.ipynb), derives an idealized model, and uses Lanchester's hand-constructed trajectories as a bridge to transparent scientific Python. If Python or scientific Python is new to you, begin with [Python essentials for this course](./appendices/python-essentials.ipynb); it introduces the small set of language, NumPy, and plotting patterns used in that chapter.

## Open by design

The original course was created as open education: material that people could use, share, modify, and remix. This edition continues that commitment while rebuilding the course with current, reproducible tools and accessible publication. The legacy repository remains available as a historical archive; its old software setup and platform instructions are outdated and should not be used as guidance for this edition.
