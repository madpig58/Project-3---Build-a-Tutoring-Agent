# Riley knows what the model outputs for a tool call, but still thinks the model runs tools (M4) and that loops need no stop (M6)

In the spaced retake of quiz 0001 (s2), Riley correctly defined an agent, said the model outputs a tool request, and said the result goes back as the next input.
Still open: in q4 Riley said the model "runs" each tool, and in q3 chose to let a stuck agent run on (M6).
Riley also thinks the model picks tools by name alone (q6, partial).

**Evidence:** quiz 0001, submission s2, items q2, q3, q4, q5, q6.

**Implications:** Before building on this, revisit that the program runs the tools and that every loop needs a stopping condition. Teach tool descriptions (name, purpose, parameters) next, since it ties into the mission goal of writing tool descriptions.
