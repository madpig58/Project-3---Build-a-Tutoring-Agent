# The agent loop is understood, but the model still seems to run the tools itself

On the spaced-practice attempt of quiz 0001, Riley recognised the loop as what defines an agent (q1), knew the model only outputs a tool request (q2), and knew the result goes back as the next input (q5). Three things are still open: Riley's q4 working says the model runs each tool itself (M4), Riley expected a stuck agent to succeed if left running (M6, q3), and Riley chose tools "by the name" alone (q6, incomplete rather than a misconception).

**Evidence:** quiz 0001, submission s2, items q1-q6. Riley's count in q4 was right (4), but the reasoning was "the model can only run one tool itself each time it's called".

**Implications:** Teaching should show a request/run/result trace with the model's output and the program's actions in separate columns. Stopping conditions and tool descriptions need a short revisit before context and memory. Submission s1 has not been graded and may show how this changed over four days.
