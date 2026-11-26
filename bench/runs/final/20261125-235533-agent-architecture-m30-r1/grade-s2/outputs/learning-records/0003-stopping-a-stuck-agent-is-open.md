# The core of the loop holds from memory; stopping a stuck agent does not yet

Four days after the agent-loop session, Riley correctly identified the loop as what makes an agent, said the model outputs a tool request, and explained that the result goes back in so the model can choose its next step.
Riley expected a stuck agent to fix its bug if left running (M6) and wrote that the model runs tools itself (M4), so both need work before designing the makerspace assistant's loop.

**Evidence:** quiz 0001, submission s2: q1, q2 and q5 correct; q3 wrong (M6); q4 partial (right count of 4, M4 in the reasoning); q6 partial (relied on the tool's name alone, leaving out its description and parameters).

**Implications:** Revisit stopping conditions first: record 0002 includes "or a limit is reached", but q3 shows this is not yet applied to a stuck agent.
M4 is mixed, since q2 was right and q4's reasoning was not, so check it again with a trace that labels each step "model" or "program".
Cover tool descriptions and parameters before Riley writes a tool definition.
