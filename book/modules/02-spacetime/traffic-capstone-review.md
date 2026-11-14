(traffic-capstone-review)=
# From traffic profiles to trustworthy speeds

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

The traffic capstone asks which speed estimates you can report with confidence and which changes in the dense patch depend on the grid and time step. A calculation can preserve the discrete vehicle balance while still smoothing an edge of the patch. Your verdict draws on several kinds of evidence because each addresses a different question.

Use this chapter to prepare for a one-to-one conversation about your [Traffic Flow Capstone](./10-traffic-flow.ipynb). The questions are examples. Practice pointing to your own equations, notes, tables, and plots as you explain your reasoning. A conversation may follow up on one answer or ask you to reconsider a claim in light of your evidence.

## Have your evidence ready

Find the following in your existing work:

- your paper derivation, CFL estimates, and three-point prediction;
- the supplied update and the results of the controlled-defect and baseline checks;
- your agent brief and one consequential part of the experiment you audited;
- your refinement tables, the comparison you reproduced independently, and your profile overlay;
- your verdict about the reported speeds, including any claim the tested runs leave unresolved.

Practice giving a short account of one scenario. State what you would report, point to the comparison that most influenced your decision, and explain what uncertainty remains.

## Model and reported speeds

1. Pick a point on a road snapshot. How do you use its density to read vehicle speed and flux from the model curves? What does the horizontal axis represent in each plot?
2. Explain the roles of vehicle speed $u$, flux $F$, and characteristic speed $a=F'(\rho)$. Which quantity determines the direction of propagation of a small density change?
3. How did you predict the initial minimum vehicle speed? How does a change in peak density affect that minimum later?
4. What goes into your reported spatial average? What additional information would you need to make a claim about the speeds experienced by drivers?

## The conservative update and its checks

1. Point to the two flux slices in the supplied step. Which nodes and time level do they represent? Why is the left endpoint held fixed while the right endpoint is updated?
2. Which density gives the largest characteristic speed in your scenario? Use your notes to explain how that speed enters the CFL check.
3. Use your three-point calculation to explain how the old inlet and outlet fluxes determine the change in the discrete vehicle total. Why does the sum start at node 1?
4. Why did the deliberately wrong update preserve constant density? Show which evidence exposed the defect once the density varied.
5. What does a small cumulative balance residual establish? What could still be wrong with the shape or location of the computed patch?

## Refinement and the agent's experiment

1. Show how you held the physical patch and observation time fixed as you doubled the number of grid intervals. Why do these choices matter?
2. Show how you aligned the two profiles in the comparison you reproduced. Which points enter the profile average, how are the endpoints weighted, and which points enter each run's speed summaries?
3. Point to a consequential requirement in your brief. How did you check that the proposed code respected it? If you requested a correction, what evidence prompted it?
4. Which pairs passed the sensitivity rule in your scenario? Explain how you used the two consecutive comparisons to choose a candidate, or why the tested grids left you without one.
5. What did halving the time step at fixed spacing tell you? How does that comparison differ from halving the spacing and step together? Use your step counts to explain the cost.

## Defend your engineering verdict

1. Which reported quantities does your evidence support? Point to a table entry that matters to your decision and explain what the 0.1 m/s threshold measures.
2. Point to the feature you tracked in your overlay. Which aspects persist under refinement, and where do the grids still disagree? How could that disagreement coexist with a small whole-road profile average?
3. What evidence would lead you to revise your verdict? What observations from a real road would help assess the traffic model itself?

A follow-up may ask you to explain a line of the update from your paper derivation, trace one table entry back to the saved arrays, or narrow a claim after looking again at the local profile. Use the evidence you already have and explain how it led you to your judgment.
