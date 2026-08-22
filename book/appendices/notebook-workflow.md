(notebook-workflow)=
# Notebook workflow

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

A notebook is both a computational scratchpad and a record of reasoning. Those roles pull in different directions at different moments, and that is useful.

(notebook-explore)=
## Explore nonlinearly

Nonlinear execution is a feature, not a bug, when you are thinking interactively with computing. You can rerun a cell with a new value, test an alternative idea, inspect an intermediate quantity, or return to an earlier step without rebuilding everything that followed.

But, _with great power comes great responsibility_. Pay attention to which definitions and data are currently in memory, especially after revising an earlier cell. When a surprising result appears, ask whether it comes from the model, the code, or the current notebook state.

(notebook-reconstruct)=
## Reconstruct a lesson

Create a separate notebook for your work and keep the published lesson open as a reference. Begin with your paper prediction, then rebuild the calculation in small pieces.

Type the code that expresses the model or numerical method: equations, updates, sign conventions, loops, boundary conditions, and checks. Copying a small amount of mechanical setup is fine when retyping it would add no understanding. Add short Markdown notes before important experiments so that your expectation is recorded before you see the result.

(notebook-linear-execution)=
## Recover a linear account

As exploration settles, organize the notebook into one understandable path from assumptions and inputs to evidence and interpretation. Preserve useful failed experiments when they teach something, but label them and make the successful computational argument clear.

Then restart the kernel and run the notebook from beginning to end. _Restart-and-run-all is your friend_: it reveals missing definitions, accidental dependencies on stale values, and results that cannot be reproduced from the notebook itself.

(notebook-close)=
## Close the lesson

Before leaving the notebook, make sure it records:

- the prediction or analytical result you began with;
- the implementation and experiments you actually used;
- the evidence supporting your conclusion;
- material agent contributions and your review of them; and
- your verdict, including important limitations or unresolved questions.

The goal is not to make exploration look artificially tidy. It is to leave a computational account that you—and someone else reviewing your work—can follow and reproduce.
