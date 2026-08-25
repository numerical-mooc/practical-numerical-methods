(course-practice)=
# Working through a lesson

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

Numerical methods become useful when you can move from a model to a computation you have reason to trust. In contemporary engineering, some code may be written by you, some may come from a scientific library, and some may be proposed by an AI agent. Whatever its source, you remain responsible for understanding what was computed and whether the result is fit for purpose.

Each lesson follows a recurring practice. The stages will not always take equal time, but each has a purpose. Trust the method, and follow each one!

(course-practice-derive)=
## Derive — On paper

Begin away from the computer. You may carry out a pivotal part of a derivation, draw a diagram, check dimensions, calculate a limiting value, or predict the behavior of a solution.

This is not a test of your patience or nostalgia for handwriting. It gives you an expectation before code begins producing persuasive-looking results, and it externalizes thinking so your mind is ready to review the code. Keep this work nearby: you will use it as evidence later.

(course-practice-reconstruct)=
## Reconstruct — In your notebook

Treat the published lesson as a worked-out reference, not as a notebook you execute from top to bottom with "Run All." Create _your own notebook_ and reconstruct the calculation there. Type the equations, numerical updates, boundary conditions, loops, and checks that carry the main ideas. A little copy-and-paste is sensible for imports, plot labels, or other mechanical details.

Reconstruction turns recognition—“this code makes sense when I read it”—into working understanding. Record predictions before running important cells, change one thing at a time when experimenting, and explain surprises. See the [notebook workflow](./appendices/notebook-workflow.md) for practical guidance.

If Python is new rather than merely rusty, first work through [Python essentials for this course](./appendices/python-essentials.ipynb). Keep it open while reconstructing the first lesson; the goal is to recognize and make small changes to the recurring patterns, not to memorize the language before doing numerical work.

(course-practice-specify)=
## Specify — Before using an agent

Give an agent a bounded task rather than a vague request for help. State the intended outcome, relevant model and conventions, inputs and outputs, constraints, permitted access, and evidence that would count as success.

A specification makes delegation useful because it gives both you and the agent something concrete to work against. It need not be perfect on the first attempt; unresolved questions and assumptions should be made explicit and revised as you learn. The [agent-use guide](./appendices/agent-use.md) provides a template and examples.

(course-practice-audit)=
## Audit — Review and verify

Treat agent output and scientific-library output as claims. Inspect the equations, signs, indexing, units, boundaries, state, dependencies, and assumptions. Then choose checks that could distinguish a correct-_looking_ result from a correct one.

The strongest evidence usually combines complementary checks: perhaps an analytical prediction, a limiting case, a residual, or a refinement study. Ask what each check can detect, and what could still be wrong if it passes. The [verification patterns](./appendices/verification-patterns.md) introduce the recurring possibilities.

(course-practice-explain)=
## Explain — Your verdict

Close the lesson by stating what you accept, what evidence supports that decision, and what remains uncertain. Record material agent suggestions that you accepted, rejected, or corrected. “The code ran” and “the tests passed” are observations; your job is to explain what those observations allow you to claim.

By repeating this practice, you will become faster at turning mathematical understanding into reliable computational work, and better at recognizing when a polished result has not yet earned your trust.
