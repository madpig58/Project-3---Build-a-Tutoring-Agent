# Riley knows the loop's structure but still thinks the model runs the tools

On the spaced retake of quiz 0001 (s2), Riley got the agent definition, the model's tool request and the program feeding results back right (q1, q2, q5). Two gaps remain: Riley says the model "runs" each tool (M4, in q4 and in the name-only answer to q6), and expected a stuck agent to eventually succeed (M6, q3).

**Evidence:** quiz 0001, submission s2, items q3, q4, q6.

**Implications:** Before context and memory, make clear that the program executes tools and the model only reads descriptions and writes requests, and that a loop needs a stopping condition such as a step limit.
