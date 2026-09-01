<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Repository guidance

This repository contains the 2026 edition of **Practical Numerical Methods: Engineering computation in the agentic era**. Work incrementally and favor pedagogical clarity over software abstraction. Explain unfamiliar tools and consequential choices in plain language.

## Course architecture

- Notebooks are the canonical executable exposition: learners should see the model, derivation, algorithm, experiments, verification, and interpretation.
- Introduce numerical code transparently in a notebook before moving stable, reused logic into standalone `.py` files in `src/`. Avoid imports that hide the method being taught.
- Treat scientific-library and AI-agent results as claims requiring inspection and evidence. Learners remain responsible for specifications, verification, provenance, and engineering judgment.
- Follow `DECISIONS.md` and `docs/Notebook-First-Code-Architecture.md`. Record consequential new design choices in `DECISIONS.md` and elaborate them under `docs/` when useful.

## Authoring conventions

- Jupyter Book 2/MyST sources live in `book/`; lesson notebooks and their figures live together under `book/modules/<module>/`.
- Keep notebooks readable as chapters: interleave concise narrative with small code chunks, expose intermediate reasoning, and include reminders where learners with rusty Python may need them.
- During development, keep committed notebooks free of cell outputs and execution counts. Adding final outputs is a deliberate later step.
- Preserve notebook cell IDs and avoid unrelated notebook reserialization. Use triple single quotes (`'''`) for Python docstrings.
- Use `book/references.bib` and MyST citations instead of handwritten reference lists. Narrative citation (part of the sentence) are entered without brackets: `@author`, not `[@author]`. The latter is for parenthetical citations only. 
- Give referenced equations semantic labels such as `eq-radius-of-curvature` and use generated references such as `[Equation %s](#eq-radius-of-curvature)`; never type equation numbers manually.
- Build from `book/` with `npx --yes --package=mystmd@1.10.1 myst build --html`. The GitHub Pages workflow is `.github/workflows/book.yml`.

## Working agreement

- Make small, reviewable changes and preserve unrelated user work.
- Treat the archived repository at `../numerical-mooc` as source material only; do not modify it unless explicitly requested.
- When agreement leads to dropping some passage or code solution, no mention should remain in the notebook of the abandoned text or code. Explanations of removed content only belong in the chat, not in the book.
- Validate edited notebooks as JSON, review the diff, and run checks or a book build proportional to the change.
- Do not commit, push, or publish unless explicitly asked. Leave changes for local review when requested.
