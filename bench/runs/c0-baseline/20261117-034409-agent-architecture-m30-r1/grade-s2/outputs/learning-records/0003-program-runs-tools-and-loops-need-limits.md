# The program runs the tools, and a loop needs a stopping condition: both still open

On quiz 0001 (second attempt, s2) Riley correctly said the model outputs a tool request (q2) and that the tool result goes back as the model's next input so it can decide what to do (q5). Two ideas are still shaky: Riley's q4 reasoning says the model "runs" each tool itself (M4), even though the count of 4 calls was right, and Riley chose "it will eventually fix the bug" in q3 (M6), believing an agent needs no stopping condition.

**Evidence:** quiz 0001, submission s2, items q2, q3, q4, q5, q6. Compared with s1, q2 and q5 improved, and q6 moved from a mention of tool descriptions (plus an invented claim that the model remembers its choices) to the tool name alone.

**Implications:** Before building on context and memory, recheck M4 and M6 with a short retrieval question. Riley also treats a tool's name as enough for the model to choose it; tool descriptions need practice, as the mission asks.
