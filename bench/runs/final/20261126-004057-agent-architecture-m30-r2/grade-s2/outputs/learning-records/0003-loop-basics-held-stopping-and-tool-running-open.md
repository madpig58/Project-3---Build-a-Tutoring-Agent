# The loop holds up from memory; stopping it and who runs tools need work

On a spaced second attempt, Riley identified what makes a system an agent, counted the model calls in a three-tool run, and explained that a tool's result goes back to the model for its next step, so the basic loop from record 0002 can be built on.
Two misconceptions are open: M6 (shown as expecting a stuck agent to succeed if left running) and M4 (shown as the model running tools itself), and Riley's account of how the model chooses a tool rests on the name alone.

**Evidence:** quiz 0001, submission s2: q1, q2 and q5 correct; q3 wrong (M6); q4 partial (M4, with the correct count of 4); q6 partial.

**Implications:** Revisit stopping conditions such as a step limit first.
M4 is mixed: Riley correctly chose that the model outputs a tool request (q2) but wrote in q4 that the model runs the tool itself, so check it again with an answer in Riley's own words.
Tool descriptions (purpose and parameters) also need teaching before Riley writes one for the makerspace assistant.
