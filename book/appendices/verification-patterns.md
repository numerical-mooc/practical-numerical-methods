<!-- SPDX-License-Identifier: CC-BY-4.0 -->

(verification-patterns)=
# Verification patterns

Verification asks whether the computation solves the equations as intended. No single check establishes correctness in every respect; combine patterns that expose different plausible failures. We will revisit these ideas in detail when each lesson needs them.

(verification-before-computing)=
## Before computing

- **Dimensions and units:** confirm that equations, parameters, and returned quantities are dimensionally consistent.
- **Analytical predictions:** calculate a value, sign, trend, or qualitative behavior before running the computation.

(verification-known-behavior)=
## Compare with known behavior

- **Exact solutions:** compare with a case whose mathematical solution is known.
- **Limiting and special cases:** reduce the problem to a simpler regime where the expected behavior is clear.
- **Conservation laws and invariants:** check quantities that should remain constant or balance according to the model.
- **Residuals:** substitute a computed result back into the governing discrete or continuous equations and measure the discrepancy.

(verification-numerical-behavior)=
## Examine numerical behavior

- **Grid and time-step refinement:** reduce a discretization scale and examine whether the solution approaches a stable result at the expected rate.
- **Manufactured solutions:** choose a convenient solution, derive the forcing or data that make it exact, and test whether the method recovers it.
- **Independent implementations:** compare results produced by separately written algorithms or tools that are unlikely to share the same defect.
- **Benchmark comparisons:** reproduce a documented case with trusted reference data or accepted quantitative features.
- **Sensitivity and uncertainty checks:** vary uncertain inputs, tolerances, or modeling choices and observe which conclusions remain robust.

(verification-defect-injection)=
## Test the checks

**Deliberate defect injection** introduces a controlled error to confirm that the proposed checks can detect it.

(verification-evidence-record)=
## Record the evidence

For an important check, state the claim, expected result, observed result, tolerance or comparison used, interpretation, and remaining limitation. A passing check supports a bounded claim; it does not certify everything the computation might be used to assert.
