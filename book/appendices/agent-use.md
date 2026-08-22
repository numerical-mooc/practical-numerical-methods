<!-- SPDX-License-Identifier: CC-BY-4.0 -->

(agent-use)=
# Working with agents

An AI agent can implement code, inspect a diff, propose tests, search documentation, or investigate a discrepancy. Its speed is useful only when the task is clear enough to review and the result is checked independently. Treat agent output as a proposal; _you_ decide whether it is acceptable.

(agent-task-specification)=
## Define the task by specification

A task specification is a testable description of the work to be done. It is not a long prompt, and it does not prescribe every line of code. It defines the boundary between what you have decided and what you are delegating.

A useful specification states:

- **Outcome:** what should exist or be learned when the task is complete;
- **Context:** the governing model, notation, units, conventions, and relevant existing work;
- **Interface:** expected inputs, outputs, shapes, types, and error behavior;
- **Constraints:** required or prohibited methods, dependencies, files, and side effects;
- **Acceptance evidence:** examples, invariants, tolerances, tests, or comparisons that would support success; and
- **Access:** which files, data, tools, network resources, or compute the agent may use.

For example, “check my phugoid code” leaves the object and standard of review unclear. A specification might instead ask the agent to leave `trace_phugoid()` unchanged, propose NumPy-only tests for three stated limiting cases, and explain which plausible defect each test could expose. You can then judge the response against an explicit request.

You will not always know enough to write a complete specification immediately. State the unknowns and ask the agent to identify assumptions or ambiguities before it acts. Revise the specification as your understanding improves; do not silently let the agent choose consequential requirements for you.

(agent-task-types)=
## Three recurring task types

- **Implementation:** ask the agent to produce a bounded component from a stated interface and acceptance criteria.
- **Review:** ask the agent to compare existing work with a model, specification, or checklist and report concrete findings.
- **Validation:** ask the agent to propose or implement checks for a numerical claim without treating its own tests as proof.

Each type still requires human inspection and independent evidence. An agent may suggest additional acceptance criteria, but you decide which claims matter and whether the evidence is adequate.

(agent-review)=
## Review before accepting

Inspect the proposed equations, signs, indexing, units, boundary treatment, state, dependencies, and failure behavior. Look at changes rather than only the final output. Run relevant checks, investigate discrepancies, and consider whether a plausible wrong implementation could still pass.

Keep permissions proportional to the task. Prefer bounded local files and public or synthetic data; do not expose secrets or grant network, external-system, or costly-compute access without a clear need and explicit authorization.

(agent-record)=
## Leave a lightweight record

Record the agent or tool and date, the task delegated, access granted, material suggestions accepted, suggestions rejected or corrected, and the verification you performed. The purpose is not to preserve every conversational turn. It is to make the origin of consequential work and the basis for your judgment clear.
