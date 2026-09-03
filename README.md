# Practical Numerical Methods

**Engineering computation in the agentic era — 2026 edition**

**Practical Numerical Methods** is a problem-driven, executable introduction to numerical methods for engineering and applied science, redesigned for the realities of computational work in 2026.

The course develops numerical literacy through real models, transparent algorithms, computational experiments, and evidence of correctness. Jupyter notebooks are the canonical teaching narrative: each method first appears there in a readable, step-by-step implementation that learners can execute and examine. Once a method has been understood and needs to be reused, its stable implementation may graduate into a small, explicit Python module. Agent-enabled work is framed around specification, inspection, testing, verification, provenance, and engineering judgment.

## Planned repository structure

This is the intended structure as the new edition grows; the directories will be introduced gradually rather than scaffolded all at once.

```text
.
├── README.md
├── DECISIONS.md
├── AGENTS.md
├── CONTRIBUTING.md
├── CITATION.cff
├── LICENSE.md
├── LICENSES/
│   ├── CC-BY-4.0.txt
│   └── BSD-3-Clause.txt
├── pyproject.toml
├── <canonical lock file>
│
├── docs/
│   ├── Notebook-First-Code-Architecture.md
│   ├── Assessment-and-Capstone-Design.md
│   ├── History.md
│   ├── Teaching-Philosophy.md
│   ├── Authoring-Workflow.md
│   └── Migration-Map.md
│
├── book/
│   ├── myst.yml
│   ├── index.md
│   ├── quickstart.md
│   ├── references.bib
│   ├── modules/
│   │   ├── 01-phugoid/
│   │   │   ├── index.md
│   │   │   ├── 01-theory.ipynb
│   │   │   ├── 02-oscillation.ipynb
│   │   │   ├── 03-full-model.ipynb
│   │   │   ├── 04-accuracy-cost-judgment.ipynb
│   │   │   ├── rocket-assignment.ipynb
│   │   │   └── figures/
│   │   ├── 02-space-time/
│   │   └── ...
│   └── appendices/
│       ├── python-essentials.ipynb
│       ├── notebook-workflow.md
│       ├── verification-patterns.md
│       └── agent-use.md
│
├── src/
│   └── practical_numerical_methods/
│       ├── __init__.py
│       ├── ode.py
│       ├── transport.py
│       ├── diffusion.py
│       ├── elliptic.py
│       └── plotting.py
│
├── tests/
│   ├── test_ode.py
│   ├── test_transport.py
│   ├── test_diffusion.py
│   ├── test_elliptic.py
│   └── notebooks/
│
├── data/
│   ├── README.md
│   ├── checksums.txt
│   └── ...
│
└── .github/
    └── workflows/
        ├── tests.yml
        ├── notebooks.yml
        └── book.yml
```

The learner-facing book source—including the executable notebooks—will live in `book/`. The root [`DECISIONS.md`](DECISIONS.md) records accepted course-design decisions, and the `docs/` directory holds fuller articulations and the history of the new edition. The `src/` directory will contain only numerical code that has already been introduced transparently and is ready for reuse.

## Previous edition

> [!WARNING]
> The [original Practical Numerical Methods with Python course](https://github.com/numerical-mooc/numerical-mooc) is preserved as an archive. Its software instructions and other time-sensitive material are outdated and should not be used as guidance for this edition.

## Licensing

This repository uses separate licenses by material type:

- Course content—including narrative text, mathematical exposition, figures, and assignment prompts—is licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/) (`CC-BY-4.0`).
- Source code—including Python modules, tests, scripts, and code cells in notebooks—is licensed under the BSD 3-Clause License (`BSD-3-Clause`).

See [`LICENSE.md`](LICENSE.md) for the scope of each license and the complete texts in [`LICENSES/`](LICENSES/). Python files can carry `SPDX-License-Identifier: BSD-3-Clause`; Markdown and other content files can be marked `SPDX-License-Identifier: CC-BY-4.0`. Because notebooks combine prose and code, they should also carry a visible note explaining that their narrative content is CC BY 4.0 and their code cells are BSD 3-Clause. Third-party material will retain its own attribution and license.
