(agent-use)=
# Working with agents

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

If you have used AI only by asking a question in a chat window and reading the answer, you already know the conversational part of working with an agent. The new part is that an agent may also **take actions with tools** in pursuit of a goal.

(agent-definition)=
## What is a coding agent?

A **coding agent** is an AI system that combines a language model with instructions, access to selected context, and tools for working on software. Given a bounded goal, it can carry out a loop such as:

1. inspect the relevant files or computational state;
2. decide on a next step;
3. use a tool to search, edit, run, or test;
4. observe the result; and
5. revise its approach or report back.

For example, a coding agent may read a notebook, locate the function that advances a numerical solution, edit that function, run the notebook or a test, inspect the failure, and revise the change. A chat answer can _suggest_ the same edit, but you normally have to transfer the suggestion into the notebook and run it yourself.

The distinction is about capabilities and access, not the shape of the interface. You may control a coding agent through a chat window, and some chat assistants can use tools. Before using any AI system, ask: **What can it inspect? What actions can it take? What requires my approval?**

| In question-and-answer chat | In an agent task |
| --- | --- |
| You supply the relevant context in the conversation. | The agent may inspect permitted files, data, documentation, or computational state. |
| The main result is a response for you to interpret and apply. | The result may include changed files, executed commands, test results, or a review report. |
| You usually perform the proposed actions yourself. | The agent can perform permitted actions and adapt after seeing their results. |
| A poor answer can mislead your next decision. | A poor action can also alter artifacts, consume resources, or affect an external system. |

### Examples in this course

The following are all plausible uses of AI, but only the latter three require agent-like access to course artifacts or tools:

- **Question and answer:** “Explain why reducing the Euler time step should reduce the discretization error.” The system responds with an explanation; it does not inspect or change your work.
- **Read-only review:** “Read my derivation and notebook, then identify inconsistencies in signs, units, and initial conditions. Do not edit anything.” The agent inspects the permitted files and returns findings with locations.
- **Bounded implementation:** “Add the specified helper function to this notebook, leave the derivation unchanged, and run the three supplied checks.” The agent edits one artifact and reports the change and check results.
- **Numerical investigation:** “Reproduce this discrepancy, compare the result at four step sizes, and report evidence about whether the cause is discretization error. Do not change the accepted implementation.” The agent runs a bounded experiment and summarizes the evidence.

In every case, the agent works from incomplete context and can misunderstand the model, encode the same mistaken assumption in both code and tests, or change more than the task requires. Tool use makes the process more capable; it does not make the result authoritative. Treat agent output as a proposal, inspect its actions and artifacts, and decide for yourself whether the evidence is adequate.

(agent-first-task)=
## Start with a small, observable task

For a first agent experience, choose work that is easy to inspect and reverse. A read-only review is a good starting point: give the agent one notebook, a short checklist, and no permission to edit. Ask it to cite the exact cells or passages behind each finding. Compare the report with the notebook yourself before accepting any suggestion.

When you later permit edits, keep the scope narrow. Name the files the agent may change, ask to see the diff, and require a relevant check. Do not begin by handing an agent an entire project with the instruction to “improve it.”

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
