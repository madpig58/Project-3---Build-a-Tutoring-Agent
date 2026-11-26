# The loop is in place, but who runs the tools is not yet clear

On quiz 0001, Riley identified the loop as what makes an agent and chose a step limit for a stuck one, but had the model running tools itself (M4), which also led to counting one model call instead of four.
This should be fixed before building on the loop, since it affects how the assistant is designed and what each request costs.

**Evidence:** quiz 0001, submission s1: q1 and q3 correct; q2 and q4 wrong (M4); q5 partial (said the result goes back to the model, gave no reason); q6 partial (right on tool names and descriptions, but said the model remembers earlier sessions' choices on its own, M3).

**Implications:** Have Riley trace a new request, labelling each step "model" or "program" and counting model calls.
Address M3 when teaching context and memory.
Submission s1 was taken on the day of the agent-loop session; the later attempt, s2, is not yet graded and may show a different picture.
