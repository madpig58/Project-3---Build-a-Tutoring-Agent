# Examples: lesson 0001 (O3)

## Section 0: Opening and warm-up
Learning objective: recall from learning record 0001 (no new objective)
Target words: 170 (the two warm-up questions, answers and feedback, inside the plan's 230)

### Practice
Question 1: The makerspace closing time changed after the model was trained. How could the assistant still answer correctly without retraining the model?

Answer: Put the new time in the text the model is given.

Feedback:
- Why it works: the model knows only what it learned in training, plus the text it is given. Today is about managing that text.
- "The model will pick up the change on its own": it feels natural because people hear news. The model has no way to know the new time unless it is in that text.

Question 2: When a model writes a reply, what does it produce one at a time, and what is each choice based on?

Answer: One token at a time. Each choice predicts what is likely to come next, based on patterns learned in training.

Feedback:
- If you said "one whole sentence" or "a stored answer": the reply is not pulled out ready-made. It is built piece by piece. Next you will see how big those pieces are and why you count them.

## Section 1: The context window: what has to fit
Learning objective: You can count what goes into one model call in tokens and say whether it fits the context window.
Target words: 430 (worked example 260, practice and feedback 110, misconception 60)

### Worked example
Setup: Will this makerspace request fit? These are made-up, illustrative numbers: the context window is 20,000 tokens, and you keep 500 of them free for the reply. The standing instructions are 2,100 characters, the tool list is 1,400, the student's question is 140, and the manual has 60 pages of 1,400 characters each.

To turn characters into tokens, use the rough figure of 3.5 English characters per token:

```python
def estimate_tokens(text):
    # rough estimate only; the real count varies by model
    return len(text) / 3.5
```

The `return` line counts the characters with `len` and divides by 3.5.

1. **Standing instructions:** 2,100 / 3.5 = 600 tokens. They are sent with the request, so they take space.
2. **Tool list:** 1,400 / 3.5 = 400 tokens. It takes space even if no tool gets used.
3. **Question:** 140 / 3.5 = 40 tokens. So far the input is 600 + 400 + 40 = 1,040 tokens.
4. **Try the whole manual:** one page is 1,400 / 3.5 = 400 tokens, so 60 pages are 60 x 400 = 24,000. The input becomes 1,040 + 24,000 = 25,040 tokens, which is over 20,000 before any reply, so the request is rejected with a "prompt is too long" error.
5. **Try only the one relevant page:** the input is 1,040 + 400 = 1,440 tokens. Add 500 for the reply and you need 1,940 of 20,000, so it fits with lots of room.

Takeaway: Before you send a request, add up every part of the input, leave room for the reply, and compare the total with the window.

### Practice
Question: Made-up, illustrative numbers: the window is 8,000 tokens. Your input is 7,600 tokens, and a full answer needs about 900. On a newer model, what happens?

Options: a) The request is rejected before starting b) The reply starts, then stops early c) The whole reply fits without trouble

Answer: b) The reply starts, then stops early.

Feedback:
- Right answer: the input fits, but it leaves only 8,000 - 7,600 = 400 tokens. The reply counts too, so a 900-token answer runs out of room. Behaviour at the limit differs between models.
- "The request is rejected before starting": this would fit an input that is too big on its own. Here the input, 7,600, is under 8,000.
- "The whole reply fits without trouble": this treats the window as a limit on input only. Input plus reply is 7,600 + 900 = 8,500, which is 500 too many.

### Misconception
Wrong idea: "The window only limits what the student types."
Why it is tempting: A chat box shows you your message and little else.
Why it fails: In the one-page request above, the question is just 40 of 1,440 input tokens. The other 1,400 are standing instructions, tool list and manual page, and the reply needs room as well.

## Section 2: Between steps: the whole history goes again
Learning objective: You can explain what is carried from one step to the next and calculate how that grows input tokens and cost.
Target words: 440 (worked example with code 280, practice and feedback 100, misconception 60)

### Worked example
Setup: A student asks four questions in one visit. These are made-up, illustrative numbers: standing instructions plus tool list are 1,000 tokens, each question is 40, each reply is 160, and with question 2 the student pastes an 800-token manual section. Suppose you pay 1 made-up credit per 1,000 input tokens.

Here is a sketch of the code. `call_model` is a stand-in, not a real library, and we assume the tool list travels with `INSTRUCTIONS`.

```python
history = []                      # short-term memory for this visit

def ask(question):
    history.append({"role": "user", "content": question})
    reply = call_model(instructions=INSTRUCTIONS, messages=history)  # stand-in, not a real library
    history.append({"role": "assistant", "content": reply})
    return reply
```

1. **`history = []`** creates a list that lives in your program. Each entry records who said something (`role`) and what was said (`content`).
2. **`messages=history`** passes the whole list on every call, not just the newest question.
3. **The second `append`** saves the reply, so the next call includes it.
4. **Call 1 input:** 1,000 + 40 = 1,040 tokens. There is no earlier history yet.
5. **Call 2:** everything from call 1 (1,040), plus reply 1 (160), question 2 (40) and the pasted section (800) = 2,040.
6. **Call 3:** 2,040 + 160 (reply 2) + 40 = 2,240. The pasted section is still inside the 2,040.
7. **Call 4:** 2,240 + 160 (reply 3) + 40 = 2,440.
8. **Add up what you pay for:** 1,040 + 2,040 + 2,240 + 2,440 = 7,760 input tokens, or 7.76 credits, although the last input is only 2,440. The pasted section alone was sent three times, for 2,400 tokens.

Takeaway: Anything that stays in the history is sent, and paid for, again on every later call.

### Practice
Question: Same made-up, illustrative chat, with nothing removed. Reply 4 is 160 tokens. The student sends a fifth question of 40 tokens. How many input tokens does call 5 carry?

Options: a) 40 tokens b) 200 tokens c) 2,640 tokens

Answer: c) 2,640 tokens.

Feedback:
- Right answer: call 5 carries everything in call 4, plus reply 4 and the new question: 2,440 + 160 + 40 = 2,640.
- "40 tokens": the chat screen makes it feel as if only the new message is sent. The instructions, tool list and history go too.
- "200 tokens": this counts reply 4 and the new question but leaves out everything earlier, which is still in the list.

### Misconception
Wrong idea: "The model remembers the earlier turns, so my program only sends the new message."
Why it is tempting: Chat apps feel continuous, like talking to one person.
Why it fails: In this setup, continuity comes from sending the history again. Send "What settings cut 3 mm acrylic?", its reply and "and for 6 mm?", and the follow-up makes sense. Send only "and for 6 mm?", and nothing says 6 mm of what, or for which job.

## Section 3: A crowded context: clear and summarize
Learning objective: You can say why a crowded context hurts, and decide what to clear or summarize.
Target words: 450 (worked example 280, practice and feedback 105, misconception 65)

### Worked example
Setup: An AI game master is running a long text adventure. These are made-up, illustrative numbers: the window is 32,000 tokens. The context holds standing instructions (1,000), early talk where decisions were made, such as the north door being locked (2,000), four old map listings returned by a tool (5,000 each), and recent turns (3,000). In this game, any map can be fetched again.

1. **Count it:** 1,000 + 2,000 + 20,000 + 3,000 = 26,000 tokens. It fits, but 20,000 of that is old map listings, which crowd the locked-door decision.
2. **Ask of each block:** will a later step need this exact text? The listings have been used and can be fetched again, so they are good candidates to clear.
3. **Clear the listings,** leaving a one-line placeholder for each, such as "Cellar map cleared; fetch again if needed". All four take 100 tokens, so the context drops to 26,000 - 20,000 + 100 = 6,100.
4. **Much later, count again:** instructions 1,000 + placeholders 100 + older talk, early decisions included, 18,000 + recent turns 3,000 = 22,100. The old listings are already gone, so clearing is not enough now.
5. **Compact:** a 500-token summary replaces the older talk and placeholders, giving 1,000 + 500 + 3,000 = 4,500. Keeping instructions and recent turns word for word is this example's design choice.
6. **Check the summary** against a list: the locked north door (decision), the unsolved riddle (open problem) and the player's inventory (important detail). Suppose the draft has the door and riddle but no inventory: change the summary instructions to require it, then check again.
7. **Count the summary's cost:** if your program asks a model to write it, that call uses tokens too.

Back in the makerspace chat from Section 2, removing the pasted section after question 2 is answered would make calls 3 and 4 carry 1,440 and 1,640 tokens. The total falls from 7,760 to 6,160, with one risk: a follow-up question may need that section again.

Takeaway: Clear what is used up and easy to get back first, then summarize what is left, and check that nothing important got lost.

### Practice
Question: The makerspace chat is getting crowded. Its context holds a calendar listing from a week ago that has already been used, a rule in the standing instructions that only trained students may book, and a booking the student asked for that is not finished yet. Which item is safest to clear first?

Options: a) A week-old calendar listing, already used b) The training rule in standing instructions c) The student's request that's still open

Answer: a) A week-old calendar listing, already used.

Feedback:
- Right answer: it has done its job, it is probably out of date, and a fresh one can be fetched.
- "The training rule in standing instructions": it may look like fixed text that was read long ago, but every later booking answer depends on it.
- "The student's request that's still open": old text can look disposable. This work is unfinished, so the assistant still needs it.

### Misconception
Wrong idea: "A bigger window fixes this, so put everything in."
Why it is tempting: A bigger window makes the "too long" error go away.
Why it fails: Give the game master a made-up window ten times larger and the old listings fit easily, but they still crowd the locked-door line, so the model is more likely to miss it. At 1 made-up credit per 1,000 input tokens, those 20,000 tokens also cost 20 credits on every call that carries them.

## Section 4: Between sessions: notes the assistant saves
Learning objective: You can choose what to save as a note between sessions and show how it gets back into the context.
Target words: 440 (worked example with code 290, practice and feedback 95, misconception 55)

### Worked example
Setup: Jordan, a student, visits the assistant today and will be back next week. Jordan passed laser cutter training, confirmed on 3 November 2026. During the visit they also looked at Friday's free slots. The token counts below are made-up, illustrative numbers.

1. **Choose what to save:** keep what is needed next visit and changes slowly. Training passed and its date: yes. Friday's free slots: no, fetch them fresh. The whole chat: no, it is too big for what it tells you.
2. **Write two small functions:**

   ```python
   import json
   from pathlib import Path

   def load_note(student_id):
       path = Path(f"notes/{student_id}.json")
       if path.exists():
           return json.loads(path.read_text())
       return {}                      # first visit: nothing saved yet

   def save_note(student_id, note):
       Path("notes").mkdir(exist_ok=True)
       Path(f"notes/{student_id}.json").write_text(json.dumps(note))
   ```

   `load_note` reads the student's file back into a dict. `save_note` makes the folder if needed and writes the dict as JSON, replacing the old file.
3. **Visit 1 ends:** `save_note("s1042", {"laser_training": "passed", "confirmed": "2026-11-03"})` puts the fact on disk, outside the context.
4. **Visit 2 starts:** load the note, add it to the instructions and begin an empty history.

   ```python
   note = load_note("s1042")
   instructions = INSTRUCTIONS + "\nSaved note: " + json.dumps(note)
   history = []
   ```

5. **Send it:** in Section 2's `ask`, change `instructions=INSTRUCTIONS` to `instructions=instructions`. The note counts only once it is in what gets sent.
6. **Compare sizes:** allow about 50 tokens for the note, with room to spare. Last visit's chat was 4 x 40 + 800 + 4 x 160 = 1,600 tokens.
7. **Keep it current:** when a fact changes, save an updated note with a new date, so stale facts can be spotted. Our advice: if the makerspace has an official training record, treat that as the truth for permission to book.

Takeaway: Between sessions, your system saves the few facts worth keeping and loads them back into the context.

### Practice
Question: Another student, Sam, finishes a visit about the vinyl cutter. During it, Sam said that step-by-step written answers always work best for them. Which item belongs in Sam's saved note?

Options: a) Today's open slots on vinyl cutter b) Every message from today's long chat c) Sam's preference for step-by-step written answers

Answer: c) Sam's preference for step-by-step written answers.

Feedback:
- Right answer: it is small, unlikely to change soon and useful on the next visit.
- "Today's open slots on vinyl cutter": they matter today, but they change. Look them up when asked.
- "Every message from today's long chat": saving everything feels safe, but loading it spends tokens on every call and crowds the context.

### Misconception
Wrong idea: "The model will remember Jordan next time because it talked with them."
Why it is tempting: Some chat products appear to remember people.
Why it fails: Start visit 2 with `instructions = INSTRUCTIONS` and `history = []`. Nothing sent mentions Jordan's training, so the model has nothing to go on. The remembering is storage plus loading that you design.

## Section 5: Retrieval: fetching the right page
Learning objective: You can explain how retrieval brings the right part of a long manual into the context, and when you could skip it.
Target words: 430 (worked example with code 265, practice and feedback 100, misconception 65)

### Worked example
Setup: A student asks, "What does error E-42 mean on the laser cutter?" These are made-up, illustrative numbers: the manual has 60 pages and 24,000 tokens. Standing instructions, tool list and question add up to 1,040 tokens, as in Section 1.

1. **Split the manual** into chunks of 300 tokens: 24,000 / 300 = 80 chunks. Do this ahead of time, so single pieces can be fetched later.
2. **Label each chunk** with its machine, section and page, so it still makes sense alone. For example, a chunk's text might start "Laser cutter, Troubleshooting, page 41".
3. **Search by exact words** for "error E-42", because a code should match letter for letter. This toy code is far simpler than real search:

   ```python
   def search_manual(chunks, query, top=3):
       words = query.lower().split()
       def score(chunk):              # how many query words appear
           return sum(word in chunk["text"].lower() for word in words)
       return sorted(chunks, key=score, reverse=True)[:top]
   ```

   `words` becomes `["error", "e-42"]`. `score` counts how many of them appear in one chunk, and the last line returns the three highest scorers.
4. **Add those 3 chunks to the context:** 3 x 300 = 900 tokens, so the input is 1,040 + 900 = 1,940. With the whole manual it would be 1,040 + 24,000 = 25,040.
5. **Check the result:** does a chunk contain E-42 and name this machine? The code returns three chunks even when none is a good match.
6. **If the check fails,** search again with other words. For a description such as "the beam keeps cutting out", try search by meaning, since the manual may word it differently.

Takeaway: Retrieval keeps the long manual outside the context and brings in only the pieces that this question needs.

### Practice
Question: A search returns a chunk that says only: "Set the speed to 20 first." (The setting is made up.) What is the chunk missing?

Options: a) More words copied from the question b) Which machine and material it means c) A bigger context window for reading

Answer: b) Which machine and material it means.

Feedback:
- Right answer: cut from its page, the chunk lost its surroundings, so you cannot tell where the instruction applies. Label chunks when you split the manual.
- "More words copied from the question": a closer match might help a search find a chunk, but it does not say what this instruction applies to.
- "A bigger context window for reading": more room feels helpful, but it does not restore information the chunk never carried.

### Misconception
Wrong idea: "Search by meaning is the smart one, so it always finds the right page."
Why it is tempting: It can match a passage even when the wording differs.
Why it fails: Search by meaning for "error E-42" might return a general page on reading error codes and miss the one line that mentions E-42. For an exact code or part number, search by exact words suits the job.

## Section 6: Worked example and faded practice
Learning objective: all five (LO1 to LO5)
Target words: 630 (worked example 340, faded practice with solution 250, misconception 40)

### Worked example
Setup: Jordan returns and asks, "What settings do I use for 3 mm acrylic, and can I have the laser on Friday?" These are made-up, illustrative numbers: the window is 20,000 tokens with 500 kept for the reply. Standing instructions are 600 tokens, the tool list 400, Jordan's note 50, the question 40, Friday's calendar listing 200, and the full manual 24,000, split into 300-token chunks.

Sort each piece into one or more of these: **every call**, **load at session start**, **fetch when needed**, **clear or summarize**, **save for next time**.

1. **Standing instructions (600) and tool list (400): every call.** The assistant needs its rules and its list of tools each time.
2. **Jordan's note (50): load at session start.** It is small and needed, and once loaded it goes along with each call.
3. **Question (40): into the history.** The starting input is 600 + 400 + 50 + 40 = 1,090 tokens.
4. **Manual: fetch when needed.** Retrieve 3 chunks on the acrylic settings, 900 tokens, instead of all 24,000.
5. **Friday's calendar (200): fetch fresh.** Slots change, so keep them out of the note, and clear the listing once it is no longer needed.
6. **Check the size:** 1,090 + 900 + 200 = 2,190 input tokens, or 2,690 with the reply space, so it fits. With the whole manual instead of chunks, the input would be 1,090 + 24,000 + 200 = 25,290, which does not.
7. **If the visit runs long: clear, then summarize.** Clear used results first. If it is still crowded, compact, keeping the chosen settings and any unfinished booking.
8. **End of visit: save only lasting changes.** A Friday booking lives in the booking calendar, so the note need not copy it. If nothing lasting changed, the note stays as it is.

Takeaway: For each piece of information, ask when it is needed and how fast it changes, then give it the cheapest place that still gets it to the model in time.

### Practice
Question (your turn): A returning student asks, "Why did my 3D print warp, and is the printer free Monday?" They also mention that they passed resin printer training today. These are made-up, illustrative numbers, with the same 20,000-token window and 500 for the reply.

Step 1, done for you: **standing instructions and tool list (1,000 tokens): every call.**

Now you finish:

2. Where does the saved note (50) go?
3. The troubleshooting guide is 30,000 tokens. How do you handle its warping section (two chunks, 600 in total)?
4. What about Monday's calendar listing (200)?
5. What about this visit's messages (300, including the question and the training remark)?
6. Estimate the largest input, when all of these are in the context at once.
7. What do you save at the end, and what do you check first?

Answer (show the solution):

2. **Load it at session start.** It is small and may matter to the answer.
3. **Fetch the two chunks** when needed. The rest of the guide stays outside.
4. **Fetch it fresh,** then clear it after use, because slots change.
5. **Keep them in the history,** and summarize only if the context gets crowded.
6. **Largest input:** 1,000 + 50 + 300 + 600 + 200 = 2,150 tokens. With 500 for the reply, that is 2,650, well inside 20,000.
7. **Check the official training record,** then save the confirmed training with its date.

Feedback:
- Right answer: each piece arrives when it is needed, and only the lasting fact is carried to the next visit.
- Saving Monday's calendar: it feels useful because the student asked about it, but it can be out of date by the next visit.
- Loading the whole guide: it feels thorough, but the input becomes 1,000 + 50 + 300 + 30,000 + 200 = 31,550 tokens, over the window.
- Saving the training remark unchecked: the student's message is a claim, and the official record is what should decide permission to book.
- Got 2,190 or another total? Add only this case's five numbers. The question is already inside the 300.

Next step if you missed one: for that item, ask "When is it needed, and how fast does it change?" and sort it again.

### Misconception
Wrong idea: "If something matters, it belongs in the saved note."
Why it is tempting: Saving feels like the safe choice.
Why it fails: Monday's calendar matters a lot today, yet a saved copy can be wrong tomorrow. Fetch it instead.

## Section 7: Summary and Go further
Learning objective: all five (own-words prompt)
Target words: 90 (model answer and self-check, inside the plan's 220 for the summary)

### Practice
Question: Explain to a teammate why the assistant can "remember" Jordan's training next week without the model remembering anything. Say where the fact is stored and how the model gets to see it.

Answer (one good version): "Our program saves Jordan's training status and date in a note, a file outside the context. Next visit, the program loads that file and adds it to the instructions it sends. The model sees the fact because it is in the context. Saving the note does not change the model's training."

Feedback:
- Check yours for three things: where the fact is stored, who loads it, and how it reaches the model. If you wrote "the model remembers", replace it with what your program does.

## Notes for the writer
- Word budgets: I followed the plan's split (worked example about 260, practice about 100, mix-up about 60), so each of Sections 1 to 5 has about 430 to 450 words from this file. That is more than half of 600, and leaves about 150 to 180 for the opening example and general idea. The plan asks for at least 4,500 estimated words, so write those parts in full. Opening examples and general ideas are not in this file.
- Section 4 practice differs from the plan: the plan's item (Jordan, "Passed laser cutter training, 3 November") repeats step 1 of the worked example, which gives the answer away. It is now a new case (Sam), with the same objective, three six-word options, the same two wrong-answer beliefs, and the right answer still third.
- Section 4 note size: the plan's "about 50 tokens" is a made-up allowance. The two-field note shown is about 55 characters, roughly 16 tokens by `estimate_tokens`. Keep the wording "allow about 50 tokens for the note, with room to spare".
- The total 1,940 appears twice with different meanings: Section 1 is 1,440 input plus 500 reply space; Section 5 is input only. Keep those labels.
- Section 1: the explanation must say, before the practice, that on newer models a reply that reaches the window limit stops early, and that an input too long on its own gives an error (context-windows page).
- Section 6 reuses Section 1's made-up 20,000-token window and 500-token reply space so "fits" can be judged; the plan names no window there. The faded practice's slip "saving the training remark unchecked" follows the plan's "confirm against official record".
- Made-up details added to make the examples concrete (none needs a citation, all are example assumptions): maps can be fetched again; the "only trained students may book" rule; "Troubleshooting, page 41"; Sam's preference; the draft summary that omits the inventory. No meaning is given for E-42 and no laser settings are stated.
- The pricing assumption (1 made-up credit per 1,000 input tokens) must be stated as an assumption, with no citation.
- Figure numbers: Fig 1 uses the one-page request (600, 400, 40, 400, reply 500, out of 20,000; the used part is small, so use large labels or a zoomed bar). Fig 2 uses 1,040, 2,040, 2,240, 2,440, with 800 shaded in calls 2 to 4. Fig 3 shows the note and manual chunks outside the context window with arrows in; the calendar listing may be shown the same way.
- The code in Sections 2, 4 and 5 is a sketch. `call_model` is a stand-in and `INSTRUCTIONS` is assumed to be defined; say so in the text.
