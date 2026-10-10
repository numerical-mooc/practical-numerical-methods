(rocket-capstone-review)=
# From trajectory to trust

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

A computed trajectory can look convincing long before it has earned our confidence. Moving from a plausible flight path to a defensible engineering result requires a chain of evidence: a correctly translated model, careful treatment of transitions and events, numerical refinement, independent checks, and a judgment that respects the remaining uncertainty. This closing section brings that evidence together.

The capstone is complete when you can explain why its conclusions deserve to be trusted—not merely when the code runs. A review conversation may draw from the questions below. The wording and follow-up questions may vary, and no one conversation will use every question.

These are not questions to answer from memory as a script. You should be prepared to point to your paper derivation, working notebook, numerical evidence, agent records, and final verdict. You should be able to connect each claim to the equations or computation that supports it and to state what the evidence does **not** establish.

## Have your evidence ready

Before the conversation, make sure you can quickly find and explain:

- your paper derivation, sign convention, state ordering, and pre-computation predictions;
- the RK2 right-hand side, time-aware step, flight driver, and event interpolation;
- the RK2 refinement results, observed-order evidence, and Richardson estimates;
- the specification, audit record, and any correction of agent-proposed code;
- the SciPy tolerance study and the comparison with the accepted RK2 result;
- the analytical coast-to-apogee check; and
- your final engineering verdict, including numerical uncertainty and model limitations.

If you were presenting to your team, you might start with a short summary. Prepare to state whether the requested flight quantities meet their numerical-accuracy targets, identify the RK2 step and SciPy configuration you accepted, and name the strongest evidence supporting that decision.

## Physical model and reported quantities

1. What is the state-vector ordering, and where must that ordering remain consistent in the right-hand side, stored histories, event functions, and reported results?
2. Why is the propellant outflow rate positive while the rate of change of remaining propellant is negative?
3. Why is aerodynamic drag proportional to $v|v|$ rather than $v^2$? Explain its direction during ascent and descent.
4. How would an incorrect drag sign affect different parts of the trajectory, and which of your checks could reveal the error?
5. Why is the reported maximum speed $\max |v|$ rather than $\max(v)$? Under what trajectory could these produce different answers?
6. Which quantities or bounds did you calculate before running the solver, and what kinds of mistakes could they expose?

## RK2, burnout, and flight events

1. Why is the rocket model a non-autonomous system? At what time and state does the midpoint RK2 method evaluate each of its two slopes?
2. What error would result from advancing the midpoint state but evaluating the second slope at the beginning-of-step time?
3. Why does the driver shorten a step so that powered flight ends exactly at the burnout time of $5\ \mathrm{s}$?
4. Why would stepping across burnout and then clamping the propellant mass to zero fail to repair the calculation?
5. Why must thrust be absent from every right-hand-side evaluation after burnout?
6. How is a known breakpoint such as burnout different from an event such as apogee or impact?
7. State the sign-change brackets used to identify apogee and impact. Why must the impact logic exclude the launch state $h(0)=0$?
8. What assumption does the linear event interpolation make? Why does obtaining exactly zero for the interpolated event component not establish that the event time is accurate?

## Verification and Richardson extrapolation

1. What did the provisional trajectory establish, and which accuracy claims remained unsupported after that first run?
2. Starting from a leading error proportional to $(\Delta t)^p$, explain how Richardson extrapolation estimates the fine-grid result's error.
3. For midpoint RK2 with step halving, why is the leading error estimate one third of the fine–coarse difference?
4. How is the observed order calculated from three successive step sizes, and why should it be checked before trusting a Richardson estimate?
5. What behavior would suggest that the refinement sequence has not yet reached the asymptotic range?
6. Which quantity controlled your selected RK2 step? Show how its estimated error compares with its acceptance target and how the next finer run supports your choice.
7. How did you compare accuracy and computational work rather than choosing the smallest available step automatically?

## Adaptive integration with SciPy

1. What role does SciPy's `solve_ivp()` play as a standard scientific-computing interface for ODE integration, and which engineering decisions remain your responsibility when using it?
2. What does it mean that SciPy's `RK45` method is an embedded Runge–Kutta pair?
3. Explain the local error scale $\mathrm{atol}_i+\mathrm{rtol}|y_i|$. Why are component-wise absolute tolerances useful for altitude, velocity, and propellant mass?
4. Why does satisfying a local error test not directly guarantee the required accuracy in apogee or impact quantities?
5. What is the difference between `max_step` and `t_eval`? Which one can constrain event-detection risk, and which one only requests stored output times?
6. Why does the SciPy implementation use separate powered and unpowered calls rather than asking one adaptive solve to cross burnout?
7. How do the SciPy event functions define apogee and impact, and what do their `direction` and `terminal` attributes control?
8. Which fields of the returned SciPy result did you inspect before accepting the trajectory and its work count?
9. What evidence from tolerance refinement supports your selected SciPy configuration? Why is Richardson extrapolation not applied to this tolerance sequence?
10. Why is `result.success` necessary but insufficient evidence that the reported quantities meet the engineering targets?

## Analytical and complementary checks

1. Why does the post-burn coast admit an analytical altitude-gain relation when the powered phase does not?
2. Starting from the supplied burnout state, explain the analytical coast-to-apogee check and how you compared it with each numerical result.
3. Which defects in the coast equation, drag direction, phase transition, or apogee calculation could this check reveal?
4. Why can the analytical coast check pass even when the powered-flight result is wrong?
5. What complementary information comes from comparing the accepted RK2 and SciPy calculations?
6. Why does close agreement between two numerical solvers not prove that the physical model is valid?
7. Which uncertainties in your verdict are numerical, and which arise from idealizations in the rocket model?

## Agent supervision and engineering judgment

1. What work did you delegate, what existing material could the agent inspect, and what actions were outside its authority?
2. Which numerical requirements in your task brief could materially change the result if omitted or misunderstood?
3. Show one consequential part of the proposed code that you audited. What evidence convinced you to accept it, or what correction did you request?
4. How did you distinguish a readable implementation from a trustworthy computation?
5. Defend your selected RK2 step, SciPy tolerances, and `max_step` as engineering choices. What additional cost would a tighter choice incur, and would it change the supported conclusion?
6. What result do you ultimately accept, to how many meaningful digits, and what is the strongest remaining limitation on that claim?

## Expect follow-up reasoning

A follow-up question may ask you to:

- point from one equation to the corresponding code and explain its sign or indexing;
- reproduce one Richardson estimate or normalized comparison from your recorded values;
- identify a plausible defect that a particular check would or would not catch;
- explain how the logic would change if a step crossed burnout or if drag did not reverse with velocity;
- distinguish a numerical-method limitation from a physical-model limitation; or
- revise a claim that is stronger than the available evidence supports.

The goal is not a flawless recitation. It is a coherent, evidence-based explanation of the computation you supervised and the engineering judgment you made.
