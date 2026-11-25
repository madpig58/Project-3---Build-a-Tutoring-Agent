# Notes

## What Riley knows
- Python from classes: functions, lists and dicts, reading JSON, and calling a web API in one class project.
- Has used a chatbot for homework help and report drafts, and has noticed that it can state an outdated fact with confidence.
- A language model takes text in and writes text out, one token at a time, from patterns learned in training (learning record 0001).
- The agent loop at a high level: the model asks for an action, the action is carried out, the result comes back, and this repeats until it is done (learning record 0002).
- Quiz 0001, s2: knows that an agent is defined by the loop, that the model outputs a structured tool request, and that the tool result goes back as the model's next input (learning record 0003).

## What Riley does not know yet
- Still thinks the model runs the tools itself (M4, shown in q4 working), though q2 was answered correctly.
- Expects a stuck agent to succeed if left running (M6); has not yet linked this to stopping conditions such as a step limit.
- Picks a tool "by the name"; does not yet see that the model reads the whole tool description (name, purpose, parameters).
- Has never called a language model from code or written a tool definition.
- Has heard the words "token" and "context window" but cannot say what they limit or why they affect cost.
- Has not met memory, retrieval, workflows versus agents, or multi-agent systems.
- Has no machine-learning background beyond one statistics course.

## Working notes
- Quiz 0001 (the agent loop and tool calling) was taken twice: `submissions/s1.json` on the day of the agent-loop session, and `submissions/s2.json` four days later, from memory, as spaced practice.
  `s2` is now graded (`grades/0001-s2.json`: 3 correct, 2 partial, 1 wrong); `s1` has not been graded yet.
- Next in the mission is context and memory, because the makerspace assistant has to answer from long machine manuals and remember each student's training status between visits.
