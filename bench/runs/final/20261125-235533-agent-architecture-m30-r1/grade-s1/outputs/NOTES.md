# Notes

## What Riley knows
- Python from classes: functions, lists and dicts, reading JSON, and calling a web API in one class project.
- Has used a chatbot for homework help and report drafts, and has noticed that it can state an outdated fact with confidence.
- A language model takes text in and writes text out, one token at a time, from patterns learned in training (learning record 0001).
- The agent loop at a high level: the model asks for an action, the action is carried out, the result comes back, and this repeats until it is done (learning record 0002).
- Recognises that the loop is what makes a system an agent, and that the program needs a step limit (quiz 0001, s1, q1 and q3).
- Knows a tool result goes back to the model, and that the model picks a tool from the names and descriptions it is sent (quiz 0001, s1, q5 and q6; both answers were partial).

## What Riley does not know yet
- Has never called a language model from code or written a tool definition.
- Has heard the words "token" and "context window" but cannot say what they limit or why they affect cost.
- Has not met memory, retrieval, workflows versus agents, or multi-agent systems.
- Has no machine-learning background beyond one statistics course.
- That the model only writes a tool request and the program runs the tool (M4: quiz 0001, s1, q2 and q4).
- That each tool result means another model call (s1, q4), and why the result is sent back (s1, q5).
- That the model does not remember earlier sessions on its own (M3: s1, q6).

## Working notes
- Quiz 0001 (the agent loop and tool calling) was taken twice: `submissions/s1.json` on the day of the agent-loop session, and `submissions/s2.json` four days later, from memory, as spaced practice.
  `s1` is graded (`grades/0001-s1.json`: 2 correct, 2 partial, 2 wrong; learning record 0003). `s2` has not been graded yet.
- Next step given to Riley: trace the q4 laser cutter request on paper, label each step "model" or "program", and count the model calls.
- Next in the mission is context and memory, because the makerspace assistant has to answer from long machine manuals and remember each student's training status between visits.
