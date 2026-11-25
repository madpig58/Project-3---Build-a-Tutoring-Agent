# Examples: lesson 0001 (O3)

All token counts, request counts and sizes below are invented round numbers, chosen so the arithmetic is easy to follow. They are not real limits or prices for any model. The writer must say this once, early (Section 1), and again in a caption wherever a table of numbers appears. The Python snippets are illustrative sketches (`call_model` is a made-up name, not a real library call).

Answer positions for the multiple-choice checks: Section 1 c (3), Section 2 b (2), Section 3 d (4), Section 4 a (1). Within each check, all four options have the same word count (stated per section).

## Section 0: Opening and warm-up
Learning objective: none new. This section sets up the three questions of the lesson (keep now, save later, find in the manual) and recalls records 0001 and 0002.
Target words: about 225 for the opening example and the two warm-up questions with answers (of the 450 budget; the rest is the title, win sentence and mission link).

### Worked example
Setup: On Monday a student named Sam asks the makerspace assistant, "Can I use the laser cutter?" The assistant checks, and Sam finishes the laser cutter training that day. On Thursday Sam asks the same question again.
1. On Thursday the right answer depends on a fact from Monday: Sam's training is done. Where can that fact live?
2. It cannot live in the model. From record 0001, the model knows only its training plus the text it is given, so Monday's chat is not in it.
3. It also should not be everything said on Monday. Carrying the whole Monday chat, plus the whole 60-page laser cutter manual, in every request would be slow and costly on a small budget.
4. So the assistant needs three decisions: what to keep in front of the model right now, what to save for next time, and how to find the one right page in a long manual.
Takeaway: The model sees only the text it is given, so every fact it needs on Thursday has to be put into that text on purpose, and put there cheaply.

### Practice
Question 1 (recall, record 0002): List the four moves of the agent loop for "Is the laser cutter free on Friday?" and name the tool.
Answer: (1) The model asks for a calendar check (the tool is `check_calendar`). (2) The program runs it. (3) The result goes back to the model. (4) The model writes the answer, or asks for another tool.
Feedback:
- A good answer has the four moves in order and names `check_calendar`. If yours was thin, that is fine: Section 2 returns to the loop and fills it in.
- If you wrote that the model runs the tool, fix that now: the model only asks, and the program does the work.

Question 2 (recall, record 0001): Why can a chatbot state an outdated fact with confidence, and what does that tell you about where a model gets its facts?
Answer: Its knowledge stops when training stops, and it writes fluent text either way. So anything newer, or private to the makerspace, has to be in the text it is given.
Feedback:
- A good answer says "training stops" and "the text it is given". That second part is the floor for the whole lesson.
- If you said "it looks facts up", that is what this lesson builds: the program does the looking up and puts the result in the text.

### Misconception
Wrong idea: none is targeted here. Section 1 takes up "the model remembers by itself".
Why it is tempting: n/a.
Why it fails: n/a.

## Section 1: The context window: what the model sees on every call
Learning objective: Explain what the context window is (the tokens the model is given on each call), what limits it, and why it drives cost per request.
Target words: about 375 for the example, practice and feedback (of 750).

### Worked example
Setup: The assistant gets the question "Is the laser cutter free on Friday?" Think of one model call as a Python list the program builds. These sizes are invented round numbers:

| Part of the call | Tokens |
|---|---|
| Instructions ("You are the makerspace assistant...") | 400 |
| Tool definitions (`search_manual`, `check_calendar`) | 300 |
| The student's question | 20 |
| Calendar result (a dump of the week's bookings) | 1,500 |

```python
messages = [
    {"role": "system", "content": INSTRUCTIONS},      # about 400 tokens
    {"role": "user", "content": "Is the laser cutter free on Friday?"},  # about 20
]
tools = [search_manual_def, check_calendar_def]        # about 300 tokens
messages.append(calendar_result)                       # about 1,500 tokens
reply = call_model(messages, tools)                    # the model sees only these
```

1. A token is a small chunk of text, a word or part of a word. The model reads and writes tokens, and requests are limited and billed in tokens.
2. Add up the call: 400 + 300 + 20 + 1,500 = 2,220, so about 2,200 tokens. That list, as text, is the context window for this call: the tokens the model is given on one call.
3. The model's whole view is that list. If a fact is not in it, the model cannot use it, like a game that can draw only what fits in this frame's memory budget.
4. The window has a maximum size. If the list is over the maximum, the call fails or the program must cut something.
5. Cost follows size. Every request sends its whole list, and the budget counts tokens. At 200 requests a day, 2,200 tokens per call is 200 x 2,220 = 444,000 tokens a day (input only).
6. Compare a design that pastes the whole 60-page manual (invented: 40,000 tokens) into every call. Each call is 2,220 + 40,000 = 42,220 tokens, so 200 x 42,220 = 8,444,000 tokens a day. That is 42,220 / 2,220, about 19 times more. This is a design to compare, not a rule.
Takeaway: The context window is the list of tokens given on one call, and its size sets both what the model can use and what each request costs.

### Practice
Question: The team proposes adding a 3,000-token policy document to the instructions, so it is in every call. The assistant handles 500 requests a day, with one model call per request (all numbers invented). How many extra tokens a day does this add?
Options (all 10 words):
a) 3,000 extra tokens a day, since the text never changes.
b) 500 extra tokens a day, one for each request made.
c) 1,500,000 extra tokens a day, because every call resends it.
d) No extra tokens; the model keeps it after call one.
Answer: c. 3,000 x 500 = 1,500,000.
Feedback:
- Right answer: c. Each call is a fresh list, so the document is sent, and billed, every time. 3,000 tokens x 500 calls = 1,500,000.
- a: This assumes the document is sent once because it never changes. The program resends it on every call regardless. Next time, multiply the size by the number of calls.
- b: This counts requests, not tokens. The unit is tokens, and the document is 3,000 of them per call.
- d: This assumes the model remembers by itself. It does not; it sees only the list in front of it, so the program must resend the document, which is why it costs tokens each time.

### Misconception
Wrong idea: "The model remembers on its own. I told it my name once, so it knows it."
Why it is tempting: A chat feels like talking to one continuous mind, and the app shows the whole conversation on screen.
Why it fails: Each call starts from only the list it is given. Show it:
```python
call_model([{"role": "user", "content": "I'm Sam."}])
call_model([{"role": "user", "content": "What's my name?"}])  # no history sent
```
The second call has no name in it, so the model cannot know it. A chat app seems to remember because the program resends the earlier messages inside the list, and that is a choice the program makes (this is the floor from record 0001).

## Section 2: What stays between steps, and what to clear
Learning objective: Explain what the assistant keeps between the steps of one request, and how to keep that set small (clearing old tool results, compaction).
Target words: about 375 for the example, practice and feedback (of 750).

### Worked example
Setup: Request: "Book the 3D printer for 2 hours Friday afternoon." The assistant uses three tools: `check_calendar`, `search_manual` and `book_slot`. Invented sizes: instructions 400, tool definitions 450, the question 25, so the start is 875 tokens. The calendar result is 1,500, the manual page is 3,000 (a whole page, before Section 4 improves this) and the booking confirmation is 50. The model's own short messages are rounded away.

1. Call 1 sends 875 tokens. The model asks for `check_calendar`.
2. The program runs the tool, not the model. It adds the result to its history and makes a second, separate model call. The model keeps nothing between calls, so the program resends everything from call 1 plus the result:
```python
history.append(tool_result)                        # the program adds it
reply = call_model(instructions, tools, history)   # a brand-new call
```
Call 2 sends 875 + 1,500 = 2,375 tokens. The model asks `search_manual("3D printer booking rules")`.
3. Call 3 sends 2,375 + 3,000 = 5,375 tokens, and the model asks for `book_slot`.
4. Call 4 sends 5,375 + 50 = 5,425 tokens, and the model writes the answer. All four calls: 875 + 2,375 + 5,375 + 5,425 = 14,050 tokens. Yet the model needed only one fact from the calendar ("Fri 14:00-16:00 free") and one rule from the page ("max 2 hours").
5. Clear instead. After call 2 the model has used the calendar, so the program replaces it with a 30-token note: "calendar checked: Fri 14:00-16:00 free". After call 3 it replaces the page with "rule: max 2 h per booking" (30 tokens). This is clearing old tool results.
6. Recount: call 1 is 875; call 2 is 2,375; call 3 is 875 + 30 + 3,000 = 3,905; call 4 is 875 + 30 + 30 + 50 = 985. Total: 875 + 2,375 + 3,905 + 985 = 8,140 tokens, about 1.7 times fewer than 14,050.
7. For a long chat nearing the limit, use compaction: summarize and start a new window from the summary. Keep the booking and the student's choices; drop greetings and raw tool output.
Takeaway: Between steps, keep the smallest set of tokens that still lets the model do the next step, and clear or compact the rest.

### Practice
Question: A booking chat has run long and the window is nearly full. The program will compact it into a summary and continue. Which detail must the summary keep?
Options (all 9 words):
a) Every greeting and thank-you the student typed earlier on.
b) The confirmed booking: 3D printer, Friday 14:00-16:00, for Sam.
c) The full raw calendar listing from the first call.
d) Every search_manual page that was loaded and read earlier.
Answer: b.
Feedback:
- Right answer: b. The booking is the outcome, and it is tiny. Later steps, such as "move it an hour later", depend on it.
- a: This treats everything the student said as equally valuable. Greetings carry no facts the model needs, so keeping them spends tokens for nothing.
- c: This keeps raw output "in case". The one useful fact from the calendar is already in the booking, and the listing is large and goes stale quickly.
- d: Same belief as c. Once the rule has been used, a one-line note is enough, and the page can be fetched again if it is needed. Next time, ask: does the model need these tokens for the next step?

### Misconception
Wrong idea: "More context always helps, so keep everything."
Why it is tempting: Throwing information away feels risky, and a bigger window sounds like a better one.
Why it fails: Keeping everything cost 14,050 tokens against 8,140 above, for the same answer. It also makes the model's job harder: the one free slot sits among 1,500 tokens of other bookings. The effective-context source calls this context rot, where the model uses information less well as the window fills. The window has a finite attention budget, so a bigger context is not always better.

## Section 3: Between sessions: notes as memory
Learning objective: Explain what is saved between sessions, and how notes in a file outside the window work as memory.
Target words: about 300 for the example, practice and feedback (of 600).

### Worked example
Setup: Sam finishes laser cutter training on Monday. On Thursday Sam starts a new session and asks, "Can I use the laser cutter?" The assistant has a `save_note` tool and a folder of files, one per student, such as `students/sam.md`. Invented sizes: instructions 400, tools 300, question 20, and Monday's whole chat 6,000 tokens.

1. At the end of Monday's session the model asks `save_note`. The program, which the developers wrote, runs it:
```python
def save_note(student, line):
    with open(f"students/{student}.md", "a") as f:
        f.write(line + "\n")

save_note("sam", "laser cutter training: done, Mon")   # about 15 tokens
```
2. The session ends and its window is discarded. Nothing is left inside the model.
3. On Thursday the new window starts empty. The program reads the note into it first (or the model asks a `read_note` tool for it):
```python
notes = open("students/sam.md").read()
instructions = INSTRUCTIONS + "\nStudent notes:\n" + notes
```
4. The window now holds 400 + 300 + 15 + 20 = 735 tokens, and the model answers correctly: training is done.
5. Reloading Monday's whole chat instead would give 400 + 300 + 6,000 + 20 = 6,720 tokens, about 9 times more, with the same fact buried inside it.
6. Notice who does what. The model only asks. The developers write the tool and the storage. This is the agent loop again, with a file as the tool.
7. What to save: facts that matter next time and are costly to find again (training done, preferences, open bookings). What not to save: raw tool output, whole chats.
Takeaway: Between sessions only what is saved outside the window survives, and small notes read back into a new window are the cheapest way to carry it.

### Practice
Question: Thursday's session starts, and Sam finished laser cutter training on Monday. What puts that fact into Thursday's window?
Options (all 9 words):
a) The model recalls it from Monday's window by itself.
b) The model got retrained overnight on Monday's chat log.
c) The calendar tool returns it if the model asks.
d) The program reads students/sam.md into the new window first.
Answer: d.
Feedback:
- Right answer: d. The note was written to a file on Monday, and the program puts it into the new window. Having the model ask a `read_note` tool would work the same way.
- a: This assumes the model keeps its old window. A session's window is gone when the session ends.
- b: This assumes memory means the model learns. Nothing about the model changes; the note is a file.
- c: The calendar holds bookings, and nothing wrote training status there. Memory only holds what something saved on purpose, so decide what to save and where it goes.

### Misconception
Wrong idea: "Memory means the model has been retrained, or has learned something."
Why it is tempting: People say the assistant "learned" Sam's training, and the answer on Thursday changes, so it looks like learning.
Why it fails: Delete the file and ask again:
```python
os.remove("students/sam.md")   # same model, same Thursday question
```
The assistant now says it does not know Sam's training status. The model never changed. The knowledge was in the file the program reads back, and the change in behavior followed the file.

## Section 4: Retrieval: finding the right page in a long manual
Learning objective: Explain how retrieval finds the right page in a long manual (chunks, search, loading only the best chunks just in time), and why a chunk needs context of its own.
Target words: about 375 for the example, practice and feedback (of 750).

### Worked example
Setup: A student asks, "Why does the laser cutter show an air-assist error?" The laser cutter manual is 60 pages, about 40,000 tokens (invented, as in Section 1). Cut into chunks of about 200 tokens each, that gives 200 chunks (invented size).

1. Prepare once, ahead of time. Cut the manual into chunks, short pieces that can be searched and loaded on their own, and store them in an index:
```python
chunks = [
    {"id": 41, "text": "If air assist fails, check the hose and the pump switch."},
    {"id": 87, "text": "Check that it is connected before starting."},
    # ... about 200 chunks
]
```
2. The model asks for `search_manual("air assist error")`. The query is a small reference. It is not the whole document.
3. Retrieval finds the few chunks that best match the question. The program returns the top three, and only those go into the window: 3 x 200 = 600 tokens. Section 1's paste-it-all design sent 40,000, which is 40,000 / 600, about 67 times more.
4. The model answers from the chunks and names the page.
5. A failure. Chunk 87 may be the real fix, but "Check that it is connected before starting." never says which machine or which part. The word "it" and the topic are on other pages, so it may not match "air assist" at all, or it may match many unrelated questions. A chunk on its own loses context.
6. The fix: before indexing, add a short line to each chunk that says what it is about, written with the whole document in view:
```python
chunk["text"] = ("Laser cutter manual, Troubleshooting, Air assist. "
                 + chunk["text"])
```
Now chunk 87 contains the words a student would ask with. (The line adds about 15 tokens per chunk, invented.)
7. Load just in time: the assistant keeps small references (manual names, section titles) and loads chunks only when asked. Rules that are short and always needed, like safety rules, can be loaded up front instead. This mix is a hybrid.
Takeaway: Retrieval puts only the best few chunks into the window, and each chunk needs a line of context of its own so it can be found.

### Practice
Question: A chunk from the 3D printer manual says "Hold the button for 5 seconds to reset it." Which line should be added to it before indexing so that it can be found?
Options (all 8 words):
a) 3D printer manual, Troubleshooting, resetting the control panel.
b) Page 31 of 60, written by the staff.
c) Read this carefully before using any machine here.
d) Drop the index and load the whole manual.
Answer: a.
Feedback:
- Right answer: a. It names the machine, the section and the topic, which is exactly what the chunk lacks. A student asking about resetting the printer panel now matches it.
- b: A page number says where the chunk sits but not what it is about, so the question's words still do not match.
- c: Generic text could be added to every chunk and would help none of them. Chunk context must be specific to that chunk.
- d: This is the tempting one, because loading everything cannot miss the page. It brings back the cost from Section 1 and the context rot from Section 2. The real cause is a chunk that does not say what it is about.

### Misconception
Wrong idea: "To answer from a manual, put the manual in the prompt."
Why it is tempting: It is the simplest way to be sure the right page is present, and it is what you do when you paste a document into a chatbot.
Why it fails: Above, the whole manual cost about 67 times the tokens of three chunks, on every call, and the answer sits among thousands of unrelated tokens, which is the context rot of Section 2. Retrieval loads only what this question needs.

## Section 5: Main worked example and faded practice: design the assistant's memory
Learning objective: Decide what the assistant keeps in its window now, what it saves between sessions, and how it finds the right page, with a reason for each that fits a small budget (objectives 1 to 4 together).
Target words: about 700 for the example, faded practice and feedback (of 750). This section is mostly example and practice, so it runs above the half-budget guideline.

### Worked example
Setup: On Thursday Sam, who finished laser cutter training on Monday, asks: "Can I book the laser cutter for Friday afternoon?" Design one session. These invented sizes (reuse the numbers from Sections 1 to 3):

| Piece | Tokens |
|---|---|
| Instructions | 400 |
| Tool definitions (`check_calendar`, `search_manual`, `book_slot`, `save_note`) | 400 |
| Sam's question | 25 |
| Calendar result | 1,500 |
| Whole laser cutter manual | 40,000 |
| Top three manual chunks | 600 |
| Sam's training note | 15 |
| Safety rules | 250 |
| Booking confirmation | 50 |
| A one-line note replacing a used result | 30 |

1. List the pieces. They are the eight rows above, from instructions to booking confirmation (the last two rows are sizes for clearing and for the confirmation).
2. Sort each piece, with a reason:

| Piece | Keep in the window now | Save between sessions | Find in the manual |
|---|---|---|---|
| Instructions, tool definitions, question | Yes: needed for every step | | |
| Safety rules (250) | Yes, up front: small and always needed | | |
| Calendar result (1,500) | One step, then a 30-token line: large, goes stale | | |
| Training status (15) | Read in at session start | Yes, as a note: small, stable, costly to rediscover | |
| Laser cutter manual (40,000) | | | Yes: top chunks only (600) |
| Booking confirmation (50) | Yes: small, needed for the answer | | |

3. Add up the budget. Call 1: 400 + 400 + 250 + 15 + 25 = 1,090. Call 2 (calendar added): 1,090 + 1,500 = 2,590. Call 3 (calendar now one line, chunks added): 1,090 + 30 + 600 = 1,720. Call 4 (chunks cleared to one line, confirmation added): 1,090 + 30 + 30 + 50 = 1,200. Total: 1,090 + 2,590 + 1,720 + 1,200 = 6,600 tokens.
4. Compare with pasting everything: instructions, tools, question and manual are 400 + 400 + 25 + 40,000 = 40,825. Call 2 adds the calendar (42,325), and call 3 adds the confirmation (42,375). With one call fewer, the total is 40,825 + 42,325 + 42,375 = 125,525 tokens, and it still does not know Sam's training. That is 125,525 / 6,600, about 19 times more.
5. Write one sentence per decision for the design review:
   - Keep: "We keep only the instructions, tools, question and safety rules, and clear each tool result once it has been used, because every kept token is resent on every call."
   - Save: "We save one small note per student outside the window, because the window is gone when the session ends."
   - Find: "We search the manual and load three chunks, not 60 pages, because that is about 67 times fewer tokens and less noise."
Takeaway: Each piece goes where its size, how often it changes and how soon it is needed say it should go, and the choices together cut the cost per request by an order of magnitude.

### Practice
Task A (half filled). Case: "A student asks to book the 3D printer next week." Invented sizes: instructions 400, tools 400, question 25 (given); next week's 3D printer calendar 1,800; the student's past bookings, 12 entries, 400; the 3D printer manual 30,000.

| Piece | Keep now / Save / Find | Reason |
|---|---|---|
| Instructions, tools, question | Keep now | Needed for every step (given) |
| Calendar result (1,800) | your sort | your reason |
| Past bookings (400) | your sort | your reason |
| 3D printer manual (30,000) | your sort | your reason |

Answer:
| Piece | Sort | Reason |
|---|---|---|
| Calendar result | Keep for one step, then clear to a one-line note | Large and changes by the hour; once the free slot is noted the rest is noise |
| Past bookings | Save only a short note ("prefers 2 h, afternoons"); fetch the full list with a tool if needed | Preferences are small, stable and costly to rediscover; the full list lives in the calendar and changes |
| 3D printer manual | Find: load only the top chunks | 30,000 tokens on every call is too much; three chunks are about 600 |

Feedback:
- The most common misfilings: keeping the full calendar result for the whole session, and saving the whole chat or the full booking list. Both put large, changing text into every later window. Check yours against the question "does the model need these tokens for the next step, or next session?"
- If you put the manual under Keep, recompute: 30,000 tokens times every call.

Task B (prompt only). The sponsor asks you to cut token use per request. Name the first two things you would change in the assistant, and the reason for each.
Answer (on demand): First, clear used tool results (calendar and pages) to one line, because every kept token is resent on every later call. Second, retrieve a few chunks instead of loading whole pages or the whole manual, because it removes most of the tokens, and the noise. A good extra: save only small notes between sessions, so later sessions stay cheap.
Feedback:
- A good answer names both changes and a reason tied to resending or to size. If you suggested a smaller model or shorter instructions, those can help, but they do not touch the largest items in the table, which are the 40,000-token manual and the 1,500-token calendar dump.

### Misconception
Wrong idea: "The design is just 'save everything and load everything': nothing is lost, so it must be safest."
Why it is tempting: It feels like insurance against missing a fact.
Why it fails: The numbers above: 125,525 tokens against 6,600 for the same booking, with the answer buried in noise and, in the paste design, still missing Sam's training status. Safety here comes from putting the right small things in the window, not all things.

## Section 6: Summary and Go further
Learning objective: none new; consolidation.
Target words: about 100 for the summary prompt and its guidance (of 450).

### Worked example
Setup: not needed; this section recaps.
Steps: none.
Takeaway: The window is everything the model sees on a call; between steps keep the smallest set that works; between sessions only saved notes survive; for a long manual, retrieve a few chunks and give each context of its own.

### Practice
Question (self-explanation, answer not revealed): "In your own words, explain to a teammate why we do not paste the manual into every request."
Answer: Not revealed. A good answer touches two points: cost per call (the manual's tokens are resent and billed on every call, so 40,000 tokens times every request), and context rot (the right page is harder to use among thousands of unrelated tokens). A bonus is naming retrieval as the alternative.
Feedback:
- If you gave only cost, add what happens to the model's use of the page. If you gave only quality, add the per-request arithmetic.

### Misconception
Wrong idea: none new.
Why it is tempting: n/a.
Why it fails: n/a.

## Notes for the writer
- Invented numbers: say once that all token counts, request counts and chunk sizes are invented for easy arithmetic, and that real limits and prices are not taught. Reuse the table in Section 1 for Sections 2 and 5. Tool definitions change from 300 (two tools, Section 1) to 450 (three tools, Section 2) to 400 (four tools, Section 5, a different design). Either keep this and state "a different tool set" or unify them. The totals in each section depend on the numbers I gave.
- Words versus tokens: the plan says chunks of about 200 words; I used about 200 tokens so that three chunks make 600 tokens, as the plan says. Use "about 200 tokens" or "150 words".
- Section 2 loads a whole 3,000-token manual page. Section 4 later replaces this with chunks. Do not call it a mistake. It shows the problem that retrieval fixes.
- Check arithmetic if any number is changed: S1 2,220; 444,000; 8,444,000; ratio about 19. S2 14,050 vs 8,140 (1.7x). S3 735 vs 6,720 (about 9x). S4 600 tokens, 40,000/600 about 67x. S5 6,600 vs 125,525 (about 19x).
- Multiple-choice answer positions: S1 c, S2 b, S3 d, S4 a. The plan asked for 2 or 3 in S1 and S2, and 2 or 4 in S3 and S4. Four distinct positions were not possible within those limits, so S4 uses position 1.
- Section 5 Task A is half filled by design. In Task A, a row left to the learner is marked "your sort / your reason", and the answer is revealed on demand.
- Facts needing a citation, taken from the plan:
  - Context is the tokens included when the model samples; context rot and the finite attention budget; the smallest set of high-signal tokens; compaction; the Pokemon example if used; just-in-time retrieval with a hybrid (https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
  - Clearing old tool results as context editing, and the memory tool as a file store outside the window run by the developer (https://claude.com/blog/context-management).
  - Chunks lose context, and prepending chunk-specific context helps (https://anthropic.com/news/contextual-retrieval).
- Facts I used that the plan does not cite: (1) the context window has a maximum size, and requests are limited and billed in tokens; (2) the model keeps nothing between calls, so the program resends the history. The plan says to teach the second from the learning records, and to explain the first in plain words without exact limits. I did not cite either. If the writer wants a source for (1), it must be found; none is in the plan.
- The "air assist" and "reset it" chunks and the file name `students/sam.md` are invented. Real manuals are not quoted.
- Section 3 Practice option d says the program reads the note. The plan allows either the program or a `read_note` tool, so the feedback says both are fine.
- Quiz items must be fresh. Avoid the handbook-cost, long-chat-compaction, Sam-on-Thursday, reset-button and 3D-printer-booking cases used here.
