# Examples: lesson 0001 (O3)

All token counts in this file are invented to show a pattern. Label them "illustrative" in the lesson. Real counts need a tokenizer.

## Section 0: Opening and warm-up
Learning objective: Recall the loop (record 0002) and what the model knows (record 0001), and see the two storage problems the lesson solves.
Target words: 270 (60% of the 450-word budget)

### Worked example
Setup: A small game. It has a player position, a list of enemies, and a save file.

1. While the game runs, the player's position and the enemies sit in RAM. They change every frame.
2. The player quits. The process ends and RAM is wiped, so the position and the enemies are gone.
3. The save file is different. The game wrote `{"level": 4, "keys": 2}` to disk on purpose, so it is still there tomorrow.
4. The makerspace assistant has the same two problems. Some text is only needed while one request runs. Some facts, such as a student's training status, must survive until the next visit.

Takeaway: Working storage and saved storage are different things, and this lesson decides what goes in each, and how the right manual page is found.

### Practice
Question 1 (recall, answer on demand): A student asks, "Can I book the 3D printer on Thursday afternoon?" Name, in order, the four things that happen in one trip around the loop, and say what ends the loop.

Question 2 (recall, answer on demand): Besides what it learned in training, what does the model know when it writes its next token?

Answer:
1. The model asks for an action (a calendar check for the printer on Thursday). The program runs it. The result goes back to the model. The model either asks for another action or writes the final answer. A final answer, or a step limit, ends the loop.
2. Only the text it is given. Today we look at exactly what that text is.

Feedback:
- Right answer (Q1): The model only asks. The program does the work and sends the result back. That is why the loop needs a program around the model.
- Wrong answer, "the loop ends when the model has called the tool": Calling the tool is the middle of the loop. The model still has to read the result and decide whether it is done.
- Wrong answer (Q2), "it also knows its earlier chats with this student": Nothing in training or in the model carries a chat forward. An earlier chat is only known if its text is given again. Section 3 shows this.

### Misconception
Wrong idea: "The assistant already knows Sam from last week. I told it."
Why it is tempting: Talking to a chatbot feels like talking to a person, who remembers.
Why it fails: The model maps the text it is given to new text. If last week's text is not in this week's input, the model has no trace of it. Like a game that was not saved, it starts blank.

## Section 1: Tokens and what fills the context window
Learning objective: List what fills the context window at a step (system prompt, tool definitions, history, tool results, reply) and say it is counted in tokens.
Target words: 360 (60% of 600)

### Worked example
Setup: A student asks the makerspace assistant, "What nozzle temperature for PETG on the Prusa?" The assistant has a system prompt (its role and rules, about 400 tokens) and three tool definitions: `check_calendar`, `book_machine`, `search_manuals` (about 600 tokens together). All counts are illustrative.

First, what a token is. Text is cut into chunks, and the model reads and writes chunks. "Nozzle temperature" might become `Noz` + `zle` + ` temperature` (illustrative split, real splits differ by model). Rule of thumb, approximate: one manual page is roughly 500 to 800 tokens.

1. The system prompt goes in first: about 400 tokens. The student never sees it, but the model reads it.
2. The tool definitions go in: about 600 tokens. The model can only ask for `search_manuals` because it reads this description.
3. The student's message goes in: about 15 tokens. Window so far: 400 + 600 + 15 = 1,015 tokens.
4. The model replies with a request for `search_manuals`: about 40 tokens. The reply is in the window too, because it is sent back in on the next step.
5. The program runs the search and adds the manual excerpt as a tool result: about 1,500 tokens.
6. Total in the window at the next step: 1,015 + 40 + 1,500 = 2,555 tokens. The student typed 15 of them, under 1%.

A sketch of the idea in Python (not a specific library's exact API):

```python
messages = [
    {"role": "user", "content": "What nozzle temperature for PETG on the Prusa?"},
    {"role": "assistant", "content": "request: search_manuals('PETG nozzle temperature')"},
    {"role": "user", "content": "tool_result: <manual excerpt, about 1,500 tokens>"},
]
reply = call_model(system=SYSTEM_PROMPT, tools=TOOLS, messages=messages)
```

`system` and `tools` travel with every call. `messages` is the history, including the tool result. The window counts all three, plus the reply.

Takeaway: The window holds everything the model reads and writes, not only what the student typed.

### Practice
Question: A student asks, "Is the vinyl cutter free on Friday?" The model replies with a calendar request, and the program adds the calendar result. Which statement about the window at the next step is true?
Options:
a) It holds the student's question alone, because that is all the student typed.
b) It holds the question and the tool result, but not the model's request.
c) It holds the question and the reply, but not the tool definitions.
d) It holds the system prompt, tool definitions, question, request, and the calendar result.
Answer: d
Feedback:
- Right answer: Everything sent so far is in: the rules, the tool descriptions, the question, the model's own request, and the result. The next call reads all of it.
- a: This assumes the chat view is the whole input. The student sees only their own messages, but the model also reads the system prompt, the definitions and the results.
- b: This drops the model's own request. The request is part of the history, and the model needs it to see what the result answers.
- c: This drops the tool definitions. They are sent on every call, and without them the model could not name a tool. (It also drops the tool result.)

### Misconception
Wrong idea: "The context is what the student typed."
Why it is tempting: The student only sees their own messages and the final answer.
Why it fails: In the example, the student typed 15 tokens and the window held 2,555. The rest is the rules, the tool descriptions, the model's request and the manual excerpt. All of it is counted, and all of it is billed.

## Section 2: Every step re-sends the history: the cost link
Learning objective: Explain that each step is a separate call that is re-sent the whole history, and estimate the input tokens billed.
Target words: 360 (60% of 600)

### Worked example
Setup: The model is like a pure function of its input. Input tokens are the tokens you send in on a call. Output tokens are the tokens the model writes. Both are billed, and cost grows with tokens. Request: "Can a first-year student use the Prusa on Friday, and what temperature for PETG?" Numbers are illustrative.

```python
def call_model(messages): ...   # no state kept inside. Pass everything in, every call.
```

1. Call 1. System prompt and tool definitions are 1,000 tokens, and the question is 30. Input: 1,030. Output: a `search_manuals` request, 40 tokens.
2. The program appends that request and the tool result (1,500 tokens). Call 2 input: 1,030 + 40 + 1,500 = 2,570. Output: a `check_calendar` request, 40 tokens.
3. The program appends that request and the calendar result (200 tokens). Call 3 input: 2,570 + 40 + 200 = 2,810. Output: the final answer, 150 tokens.
4. Add up the input billed: 1,030 + 2,570 + 2,810 = 6,410 tokens. The final window was 2,810, so the bill is more than twice the final window. Output billed: 40 + 40 + 150 = 230.
5. The 1,500-token excerpt is paid for in call 2 and again in call 3. Two levers: keep tool results small, and set a step limit. If the window fills, the request errors or stops.

Takeaway: Cost grows with the number of steps and with the size of what is carried, because every call re-sends the whole history.

### Practice
Question (faded): Request: "Which drill press bit for acrylic, and is the drill press free on Monday?" Call 1: system prompt and tool definitions are 900 tokens, the question is 20. Input: 920. Output: a `search_manuals` request, 30 tokens. Call 2: the program adds that request and an 800-token manual result. Input: 920 + 30 + 800 = 1,750. Output: a `check_calendar` request, 30 tokens. The calendar result is 120 tokens. (a) What is call 3's input? (b) What is the total input billed over the three calls?
Answer: (a) 1,750 + 30 + 120 = 1,900 tokens. (b) 920 + 1,750 + 1,900 = 4,570 tokens.
Feedback:
- Right answer: Each call carries the whole history so far, plus the newest request and result. The total is the sum of three full windows, not one.
- Wrong answer 150 (or 30 + 120): This assumes each call sends only what is new. The model keeps nothing between calls, so the 920 and the 800 must be sent again.
- Wrong answer 1,840 for the total (920 + 800 + 120): This counts each piece once, as if it were stored. Each piece is billed again on every later call.

### Misconception
Wrong idea: "The model remembers the earlier steps, so the program only needs to send the new result."
Why it is tempting: A chat feels continuous, so it seems the model holds the thread.
Why it fails: Suppose the program sent only `"Mon 2-4 pm free"`. The model would see a bare fragment, with no question and no idea which machine. It could not answer. The program must re-send the full list each call.

## Section 3: Between steps versus between sessions
Learning objective: Separate what is kept between steps (the message list in the running program) from what is kept between sessions (nothing, unless the program saves it).
Target words: 300 (60% of 500)

### Worked example
Setup: Sam is a student. The assistant is a Python program that calls a model. A session is one conversation. To persist something is to save it outside the running program, so it survives.

1. Monday, visit 1. Sam asks about the laser cutter and says safety training is done. The `messages` list grows across the steps. This is "kept between steps".
2. Sam closes the chat. The Python process ends, and the list is freed from RAM.
3. The code starts each session with a fresh list:

```python
def run_session():
    messages = []          # new, empty list every session
    ...
```

4. Wednesday, visit 2. Sam asks, "Can I book it now?" The list is empty, so the model has nothing about Monday and asks about training again.
5. Cause: nothing was saved. The model never held Sam's training, because it only reads what it is given. Fix, in one line: load the saved record into the new list. Sections 4 and 5 give the tools.

| Kept between steps | Kept between sessions |
|---|---|
| The message list in the program, re-sent each call | Nothing, unless the program writes it to a file or database and reads it back |

Takeaway: The message list is working storage for one run, and memory must be written out and read back on purpose.

### Practice
Question: The assistant is the team's own Python program calling a model. On Tuesday, Jo says, "I only print in PLA." On Wednesday, a new session starts. Where could the assistant learn Jo's preference?
Options:
a) From a note file the program saved Tuesday and loaded Wednesday.
b) From the model's weights, which update live while chatting with students.
c) From the old message list, which waits inside the model overnight.
d) From the context window, which the provider saves between sessions automatically.
Answer: a
Feedback:
- Right answer: Only a file (or database) written by the program and read at the start of the new session carries the fact across.
- b: This assumes the model learns from chats. Weights are fixed after training, so chatting changes nothing in them.
- c: This feels natural, because "the conversation is still there". But the list lives in the program's RAM, which ends with the process, and the model holds nothing between calls.
- d: This assumes the window is a saved object. It is just the text sent on one call, and nobody saves it unless your program does.

### Misconception
Wrong idea: (1) "The model remembers earlier chats by itself." (2) "The program's message list is the memory."
Why it is tempting: Within one session the list does carry things forward, so it looks like memory.
Why it fails: Quit the game without saving and the progress is gone. The list is RAM. The model has no memory of its own, and a list that vanishes with the process is not memory across sessions.

## Section 4: Retrieval, finding the right manual page
Learning objective: Explain how retrieval puts only the relevant chunks into context, and why that beats loading the whole manual.
Target words: 390 (60% of 650)

### Worked example
Setup: Retrieval is searching a store of documents and putting only the best matches into the context. A chunk is a small piece of a document, a few paragraphs, stored and searched on its own. Question: "Why does printer A say 'thermal runaway'?" The manual for printer A has 400 pages. At roughly 600 tokens a page (approximate), that is about 250,000 tokens.

Like level streaming: the engine loads the tiles near the player, not the whole open world.

1. Prepare once, ahead of time. Split each manual into chunks and store each with a label, such as `printer-A.pdf, p.37`.
2. At question time, the model calls `search_manuals("thermal runaway")`. Keyword search matches exact words, such as the error name. Meaning-based search ("embeddings") finds chunks that say similar things in other words. Good systems combine both.
3. The search returns the top three chunks, about 600 tokens, with page labels.
4. Only those chunks enter the context as the tool result. The model answers and cites "printer A manual, p.37".
5. Cost, illustrative: the chunks sit in history for two later calls, so 600 x 2 = 1,200 input tokens. The whole manual, loaded from call 1, would be 250,000 x 3 = 750,000.
6. One failure: a chunk reading "restart it" with no machine or section is useless alone. So each chunk is stored with its source and heading. In the source's own tests, adding a short description of where a chunk comes from cut top-20 retrieval failures from 5.7% to 2.9% (49% fewer). That is their result, not a promise for the makerspace.

Takeaway: Retrieval loads only the few chunks that matter, which keeps the window small, the bill low, and the right text easy to find.

### Practice
Question: A sponsor says: "The window now holds 2,000,000 tokens and all manuals total 900,000, so skip retrieval." What is the best reply?
Options:
a) Agree, because text that fits in the window is always read well.
b) Agree, because you pay only for the few tokens the answer uses.
c) Disagree, because each step re-pays for it all, and middle text suffers.
d) Disagree, because models refuse any input above one third of the window.
Answer: c
Feedback:
- Right answer: Every call re-sends the whole history, so the 900,000 tokens would be billed at each step. Tests also show accuracy is highest at the start or end of the input and drops in the middle.
- a: This confuses the limit with quality. It fits, and the model does read it, but it reads the middle less reliably.
- b: This assumes you pay only for what the answer uses. Input tokens are billed for everything sent, used or not.
- d: There is no such rule. The window limit is a maximum, and the real problem is cost and accuracy, not refusal.

### Misconception
Wrong idea: "A bigger window means no need for retrieval."
Why it is tempting: If everything fits, loading it all seems simpler and safer.
Why it fails: A bigger window raises the limit. It does not lower the cost. In the example, loading the manual would be 750,000 input tokens against 1,200, for an answer on one page.

## Section 5: Notes and memory files
Learning objective: Use a memory file to carry a student's training status across sessions: what to write, when to read it, and who does the file work.
Target words: 330 (60% of 550)

### Worked example
Setup: A memory file is a file the assistant writes notes into and reads in a later session. The memory tool is a tool the model calls to ask for file operations (view, create), which the program runs. Like a save file with `{"level": 4, "keys": 2}`, the assistant keeps one small file per student, such as `students/sam.md`. (In one published example, a model playing a Pokemon game kept tallies and maps in notes across thousands of steps.)

1. Visit 1 starts. The model, as its system prompt tells it, views `/memories` for a file on Sam. None exists.
2. Sam completes laser-cutter safety training. The model calls the memory tool: `create students/sam.md` with "Safety training: laser cutter, passed 2026-11-24. Prefers evening slots."
3. The program runs the file operation and returns "ok". The model only asked, as with any tool.
4. The session ends and the process exits. The file stays on disk.
5. Visit 2. The program starts with an empty `messages`. The model's first move is to view `/memories`, and it reads Sam's file: a few dozen tokens, not Monday's transcript.
6. Sam asks, "Can I book it now?" The model knows the training is on record and goes straight to the calendar.
7. Rules of thumb. Write facts and decisions. Do not write whole transcripts or raw tool output. Keep notes short, since each read costs tokens. Read on demand.
8. A question for later: if the training record gates a safety rule, should it live in this note, or in the booking database the program checks?

Takeaway: A memory file carries the few facts that matter across sessions, and the program does all the reading and writing.

### Practice
Question: Leo finishes vinyl cutter training today. Which of these belongs in Leo's memory file?
Options:
a) The full text of the manual pages Leo read today.
b) That Leo passed vinyl cutter training and prefers morning slots.
c) Every calendar result the assistant fetched while helping Leo today.
d) The model's full step-by-step reasoning behind each answer it gave.
Answer: b
Feedback:
- Right answer: A short fact and a preference are what the next session needs. They are cheap to read and stay true.
- a: This assumes more notes are safer. Manual pages can be retrieved again when needed, and they cost tokens at every read.
- c: Calendar results go stale as soon as someone books. A stale note can mislead the next session. Fetch fresh.
- d: Reasoning is bulky and helps no later session. The conclusion is what matters.

### Misconception
Wrong idea: "Memory means the model stores things inside itself."
Why it is tempting: Saying the assistant "remembers" sounds like something inside it changed.
Why it fails: The memory is an ordinary file. The model asks to create or view it, and the program does the reading and writing. Delete the file and the memory is gone, and the model is unchanged.

## Section 6: Main worked example and faded practice, design the assistant's memory
Learning objective: Decide what stays in context, what is retrieved, and what is saved, and defend each choice by cost and accuracy (objectives 1-5).
Target words: 600 (worked example about 330, faded practice about 270)

### Worked example
Setup: Request: "I'm Priya, I need to cut acrylic on the laser cutter next week. What settings, and book me a slot." Candidate items: system prompt, tool definitions, the question, the laser-cutter manual (250 pages, about 150,000 tokens, rough), Priya's training status, the calendar for all machines, and past chats with all students. Token counts are illustrative.

1. Sort every item into "always in context", "retrieved when needed" or "saved between sessions", with a reason.
2. System prompt and tool definitions: always in. They define the assistant and are small (about 1,000 tokens).
3. The manual: retrieved. Only the top chunks enter (about 700 tokens), not 150,000.
4. Priya's training status: saved, in her memory file or the booking database, and read at the start of her visit.
5. The calendar: fetched with `check_calendar` for one machine and one week. It changes, so it is never stored.
6. Past chats of all students: not loaded, and not saved in full. They are bulky, and most are irrelevant.
7. Trace the run. Call 1 reads Priya's file. Call 2 searches the manual for acrylic settings. Call 3 checks the calendar. Call 4 books the slot. Call 5 writes a note: "Priya: cut acrylic, booked Tue 2 pm." Call 6 writes the final answer.
8. Illustrative sizes. Base 1,040 (1,000 + 40-token question). Each request is about 40 tokens. Results: file 60, chunks 700, calendar 250, booking 50. The note request is 60 and its "ok" is 10. Inputs: call 1 is 1,040. Call 2 is 1,040 + 40 + 60 = 1,140. Call 3 is 1,140 + 40 + 700 = 1,880. Call 4 is 1,880 + 40 + 250 = 2,170. Call 5 is 2,170 + 40 + 50 = 2,260. Call 6 is 2,260 + 60 + 10 = 2,330. Total input: 10,820 tokens. Loading the whole manual would add about 150,000 x 6 = 900,000.

| Item | Where it lives | Why |
|---|---|---|
| System prompt, tool definitions | Always in context | Small, and they define the assistant |
| Laser-cutter manual | Retrieved | 700 tokens instead of 150,000, and easier to read |
| Priya's training status | Saved, read at start | Survives between visits |
| Calendar | Fetched for one machine and week | Changes, so never stored |
| Past chats of all students | Not loaded | Bulky and mostly irrelevant |

9. Check: remove a step and see what breaks. Without the file read, the assistant asks about training again. Without retrieval, cost multiplies. Without the note, the next visit starts blank.

Takeaway: Keep small, always-needed text in context, fetch big or changing things on demand, and save the few facts that must survive.

### Practice
Question (faded): Request: "I'm Marcus, I want to use the vinyl cutter and I'm not sure how to load the roll. Can you book me for Friday?" Marcus has a memory file: "Vinyl cutter training: passed 2026-11-10." The vinyl cutter manual is 120 pages. Fill in the blanks.

(a) Table, where each item lives and why:

| Item | Where it lives | Why |
|---|---|---|
| System prompt | Always in context | Small, defines the assistant |
| Tool definitions | Always in context | Small, and the model needs them to name a tool |
| Vinyl cutter manual | ? | ? |
| Marcus's training status | ? | ? |
| Friday calendar | ? | ? |

(b) Put these calls in order: write the note, search the manual, read Marcus's file, check the calendar, final answer, book.
(c) What goes in Marcus's note?

Answer:
(a)
- Manual: retrieved, only the roll-loading chunks, because the whole manual would be paid for at every step and hurts accuracy.
- Training status: saved in his file (and checked by the program for safety), read at the start of the visit.
- Friday calendar: fetched with `check_calendar` for the vinyl cutter and Friday only, because it changes.

(b) Read Marcus's file, search the manual, check the calendar, book, write the note, final answer.
(c) Facts only, such as "Marcus: first vinyl session, asked how to load the roll, booked Friday 1 pm." Not the manual text, and not the calendar results.

Feedback:
- Right answer: Each choice keeps the window small (retrieve and fetch what is big or changing) and keeps what must last (the file and the note).
- Wrong answer, "put the whole vinyl manual in the system prompt to be safe": This assumes more text is safer. It is paid for at every step, and the answer can get lost in the middle.
- Wrong answer, "save the calendar results in the note": They go stale, and the next session could be misled.
- Wrong answer, writing the note before booking: The note would record a booking that has not happened yet.

Reflection (answer on demand): Which of your choices saves the most tokens, and which one protects the student's safety? Model answer: Retrieving only the roll-loading chunks saves the most tokens. Checking the training record in the database the program reads, rather than trusting a convenience note, protects safety.

### Misconception
Wrong idea: "To be safe, put the whole manual in the system prompt."
Why it is tempting: It feels like nothing can be missed.
Why it fails: The manual is re-sent and billed at every call, and relevant text in the middle is read less reliably. Retrieval gives the same page for a fraction of the tokens.

## Section 7: Summary and Go further
Learning objective: Say the main idea in your own words.
Target words: 100 (the summary and Go further are written by the writer, from the plan)

### Worked example
Setup: Prompt (in the lesson): "In two or three sentences, explain to a teammate why the assistant forgot Sam's training, and what you would add so that it does not."
Model answer (reveal on demand):
1. The assistant's message list lives only in the running program, so it ended with the session. The model keeps nothing between calls.
2. Add a memory file for each student: write "training passed" when it happens, and read the file at the start of each visit.
3. For safety, check the booking database too.

Takeaway: Things last between sessions only if the program saves them and reads them back.

### Practice
Question: Use the same prompt for the vinyl cutter: why would a fresh session ask Marcus about training again, and what is the one-line fix?
Answer: The new session starts with an empty list and nothing was saved, so the model has nothing about Marcus. The fix is to save a note on training and load it at the start of the session.
Feedback:
- Right answer: It names the cause (nothing saved, empty list) and the fix (save, then load).
- Wrong answer, "use a bigger window": A bigger window holds more of the current session. It does not carry anything into a new one.
- Wrong answer, "tell the model to remember": The model has no place to keep it. Only text given or a file the program reads counts.

### Misconception
Wrong idea: "A bigger context window will fix the forgetting."
Why it is tempting: "Window" sounds like memory, so more of it seems like more memory.
Why it fails: The window is only the text for one call. A new session starts it empty, however large it is.

## Notes for the writer
- All token counts, page counts and per-page figures are invented or rough. Label them "illustrative" or "approximate", as the plan says. The 49% figure (5.7% to 2.9%) and lost-in-the-middle come from the plan's cited sources only.
- Section 6: the plan says call 5 writes the note and does not count a final-answer call. Under the loop rule from record 0002 (each call either requests a tool or answers), the final answer is a sixth call. The file uses six calls, with an input total of 10,820. If you prefer five, drop call 6 and the total changes.
- Section 6 faded practice: Marcus's file ("Vinyl cutter training: passed 2026-11-10") and the 120-page manual are my inventions. The plan does not cite them. The Section 6 manual size (150,000 tokens) follows from the plan's 500 to 800 tokens per page.
- Section 2 practice and Section 6 faded practice use new cases, not the plan's 4,000-token variant, because the rules ban re-skinning the worked example. Sections 1, 3, 4 and 5 practice also use new cases (vinyl cutter, Jo, a sponsor's 2,000,000-token window, Leo).
- MCQ answer positions: Section 1 d, Section 3 a, Section 4 c, Section 5 b. Option word counts are equal within each question (Section 1: 13 words each; Section 3: 11; Section 4: 12; Section 5: 10). Character length is close but not exact.
- Section 0 has no stand-alone MCQ. Its practice is the plan's two recall questions. Section 7 has no worked example in the plan, so the "explain in your own words" prompt serves as its practice.
- The code sketches are ideas, not a specific library's API. The `tool_result` shown as a "user" message follows the plan, and the writer should say it is a sketch.
- Sections 2 and 6 mention the window error or stop in passing only. Prompt caching and compaction are not used.
- Avoided quiz 0001 items: no "laser cutter free tomorrow" question, no "count the model calls" question, and no `check_training_record` tool.
