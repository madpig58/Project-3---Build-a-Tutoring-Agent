# Examples: lesson 0001 (O3)

All token counts, window sizes and costs below are illustrative round numbers, not real figures for any model. Correct-answer positions across the multiple-choice items: S1 b, S2 d, S3 c, S4 a, S5 b.

## Section 0: Opening and warm-up
Learning objective: recall the agent loop (record 0002) and why a model can be out of date (record 0001), as the floor for this lesson.
Target words: 200 (no worked example in this section; warm-up only)

### Practice (warm-up, answers on demand)
Question 1: For "Is the laser cutter free on Friday?", list the four beats of the agent loop in order.

Question 2: Why can a chatbot state an outdated fact with confidence?

Answer 1:
1. The model asks for an action: `check_calendar(laser, Friday)`.
2. The program carries out that action.
3. The result goes back to the model.
4. The model either asks for another action or writes the final answer. Here it writes "Yes, free from 12:00."

Answer 2: The model knows only its training plus the text it is given. Its training stops at some date, and it writes plausible text whether or not that text is true. Today's lesson is about the second half: what text it is given.

Feedback:
- Right answer 1: all four beats are there, and beat 3 is the one that makes it a loop. Without the result going back, the model could never use what the tool found.
- Wrong answer to watch (skipping "the result goes back"): "ask, run, answer" sounds complete, but the final answer depends on the result. Something has to put the result in front of the model.
- Wrong answer to watch for 2 ("it looks the fact up and the source was wrong"): a plain chatbot does not look anything up. It writes from patterns it learned, so the fix is to give it text, which is what context and memory do.

### Misconception
Wrong idea: "The chatbot checks the internet, so an old fact means a bad website."
Why it is tempting: chatbots feel like search engines.
Why it fails: with no tool, nothing is checked. Its knowledge ends where its training ended. A tool can fix this only because the tool result becomes text it is given.

## Section 1: Tokens and the context window
Learning objective: say what a token and the context window are, and what the window limits.
Target words: 300

### Worked example
Setup: the bandsaw manual is 120 pages, with about 300 words per page. Assume (illustrative) the model's window is 32,000 tokens. A token is a chunk of text, often a word or part of one. English averages about 3/4 of a word per token (a rough rule, not exact).

First, a tiny split by hand. "Can I book the laser cutter on Friday?" has 8 words. One plausible split is: `Can` `I` `book` `the` `laser` `cutter` `on` `Friday` `?`. That is 9 tokens. A real tokenizer may split "Friday" or "laser" differently.

1. Count the words on one page: 300.
2. Convert to tokens. Divide by 3/4, which is the same as multiplying by 4/3: 300 x 4/3 = 400 tokens per page.
3. Multiply by pages: 400 x 120 = 48,000 tokens for the whole manual.
4. Compare with the window: 48,000 > 32,000, so the manual does not fit in one call. It is 16,000 tokens over.
5. The window counts everything, not only the manual. Say the system prompt and tool descriptions take 1,000 tokens and the answer needs 500. That leaves 32,000 - 1,000 - 500 = 30,500 tokens, which holds 30,500 / 400 = 76 pages at most.

Rough estimate in Python (a guess, not a real tokenizer):

```python
def est_tokens(text):
    return len(text.split()) * 4 // 3   # words x 4/3
```

Takeaway: the context window is the limit on how many tokens one call can take in and produce, counting everything given plus the answer.

### Practice
Question: A manual is 30,000 words and the window is 32,000 tokens. Does it fit, with room for a question and an answer?

Options:
a) Yes, because 30,000 is clearly smaller than 32,000.
b) No, because 30,000 words is about 40,000 tokens.
c) Yes, because the model ignores any extra text.
d) No, because the window only holds one page.

Answer: b. 30,000 x 4/3 = 40,000 tokens, which is 8,000 over the window before any question or answer is added.

Feedback:
- Right answer (b): words convert to more tokens (x 4/3), so 30,000 words is about 40,000 tokens.
- a: you treated words as tokens. That is the first slip. The second is that even 30,000 tokens would leave only 2,000 for the prompt, tools and answer.
- c: you may think overflow is quietly cut off. The limit is on what a call can take in, so you must choose what goes in. Nothing guarantees the important part survives.
- d: you may think the window is a tiny fixed size. It holds tens of thousands of tokens, many pages, but not 120.

### Misconception
Wrong idea: "The context window is the model's memory of the student."
Why it is tempting: the word "context" sounds like a running memory of the conversation.
Why it fails: the window is only the input and output of one call. Call A says "I'm Riley, trained on the laser cutter." A separate call B asks "What's my training status?" and has no way to know, because call A's text was not sent in call B.

## Section 2: Between steps: the transcript is re-sent
Learning objective: explain what is kept between the steps of one loop.
Target words: 320

### Worked example
Setup: Riley's request from before, "Is the laser cutter free on Friday?", as pseudocode. The transcript is the list of all messages so far in this request. The model is stateless: it keeps nothing from one call to the next.

```python
messages = [{"role": "user", "text": question}]
while True:
    reply = call_model(messages)          # one separate model call
    messages.append(reply)
    if reply["type"] == "final":
        break
    result = run_tool(reply["tool"], reply["args"])   # the PROGRAM runs it
    messages.append({"role": "tool", "text": result})
```

Token counts below are illustrative, and the system prompt is left out.

1. Call 1 receives `[question]`, about 12 tokens.
2. The model's output is only a request: `check_calendar(laser, Friday)`, about 20 tokens. It cannot run anything.
3. The program runs the tool, gets "free 12:00-17:00" (about 30 tokens), and appends both the request and the result to `messages`.
4. Call 2 receives `[question, request, result]`: 12 + 20 + 30 = 62 tokens. The whole list goes again, longer.
5. Suppose the program forgot to append. Call 2 would receive `[question]` again, the model would make the same request, and the loop would never end.

Takeaway: each step is a separate model call, the program runs the tools, and the only thing that carries over is the transcript the program re-sends.

### Practice
Question: In call 3 of a loop, where does the model get the result of call 1's tool?

Options:
a) It remembers the result from call 1.
b) The tool pushes it into the model.
c) The window keeps it between calls automatically.
d) The program re-sent it in the transcript.

Answer: d.

Feedback:
- Right answer (d): the program stored the result in `messages` and sent the whole list with call 3. If it had not, call 3 would not know the result existed.
- a: you imagine one continuing mind, like a phone call. Each call starts fresh, so nothing is remembered.
- b: you imagine the tool talking to the model. A tool only returns text to the program, and the program decides what the model sees.
- c: you treat the window as storage. It is only the size limit on one call. Nothing is kept in it after the call.

### Misconception
Wrong idea: "The model remembers the earlier steps by itself."
Why it is tempting: the loop feels like a conversation with one continuing mind.
Why it fails: delete the append line from the code above and the agent forgets every result. One consequence: because the program re-sends everything, the transcript grows every step. Section 3 shows why that costs money.

## Section 3: Why size costs money and quality
Learning objective: explain why context size drives cost and quality, and name two ways to shrink it.
Target words: 330

### Worked example
Setup: a 10-step request. Each step fetches one manual page of 2,000 tokens. For simplicity, count call n as sending n pages (ignore the question and system prompt). Cost is roughly proportional to input tokens, so we count tokens sent. Context rot means answers get less reliable at recalling details as the context fills. Compaction means summarizing a long transcript and starting fresh with the summary.

1. Each step adds 2,000 tokens to the transcript.
2. The transcript is re-sent in full, so call n sends about 2,000 x n tokens: 2,000, 4,000, ... up to 20,000.
3. Sum for 10 steps: 2,000 x (1 + 2 + ... + 10) = 2,000 x 55 = 110,000 input tokens. Not 20,000.
4. Double the steps to 20: 2,000 x 210 = 420,000. That is about 3.8 times more, so doubling steps roughly quadruples input.
5. Now clear each page's text after the model has used it, keeping a 30-token note such as "read bandsaw p.14: blade change steps". Call n sends 2,000 (the new page) plus 30 for each earlier note. The sum is 2,000 x 10 + 30 x (0 + 1 + ... + 9) = 20,000 + 30 x 45 = 21,350 tokens.
6. Compare: 110,000 / 21,350 is about 5. Input falls to about one fifth. The model also has less old text competing with the page it needs now.

Takeaway: because the transcript is re-sent, cost grows faster than the step count, and clearing old tool results (or compaction) shrinks both cost and clutter.

### Practice
New case: a booking agent runs 8 steps. Each step the calendar tool returns a 1,500-token listing. The tool description is 300 tokens, re-sent every call. The final answer is 200 tokens. The window is large enough for everything.

Question: Budget is tight. Which change cuts the most input tokens?

Options:
a) Make the final answers 100 tokens shorter.
b) Trim the tool description by 100 tokens.
c) Replace used listings with one-line 20-token notes.
d) Switch to a window twice as large.

Answer: c. Without clearing, input from listings is 1,500 x (1 + ... + 8) = 1,500 x 36 = 54,000. With clearing it is 1,500 x 8 + 20 x (0 + ... + 7) = 12,000 + 20 x 28 = 12,560. That saves 41,440 tokens.

Feedback:
- Right answer (c): the re-sent old results are the biggest part of input. Clearing them cuts 41,440 tokens.
- a: you think visible output is the main cost. Here it saves 100 output tokens once, and the answer is never re-sent.
- b: you think a smaller tool description helps. It does, but only by 100 x 8 = 800 tokens, about 2% of what clearing saves.
- d: you think a bigger window saves money. It only raises the limit. The same tokens are still sent and paid for.

### Misconception
Wrong idea: "A bigger window means the model uses everything in it perfectly."
Why it is tempting: if it fits, it seems like it should be used.
Why it fails: context is a finite resource with diminishing returns. As the window fills, recall of details gets less reliable (context rot). Picture a blade-change instruction on page 2, buried under nine other pages. It fits, but the model is more likely to miss it than if only that page were in context.

## Section 4: Retrieval: fetching the right manual pages
Learning objective: explain how retrieval finds the right pages instead of loading whole manuals, and when loading everything is fine.
Target words: 330

### Worked example
Setup: the question is "How do I change the bandsaw blade?" Retrieval means finding the few relevant pieces of a large text and adding only those to the prompt. A chunk is one piece of the manual, such as a page. Like a game keeping an index of asset names and loading only what the level needs, we keep an index and load pages. Chunks are pre-split with IDs.

```python
chunks = {
 "bandsaw/p14": "Bandsaw manual, blade change: unplug the machine, open the wheel cover, release the tension and slip the old blade off.",
 "bandsaw/p15": "Bandsaw manual, blade tension: after fitting, set the tension knob to the mark for the blade width.",
 "laser/p07":   "Laser cutter manual, lens care: wipe the lens, and change the filter each month.",
}
STOP = {"how", "do", "i", "the", "a", "to", "it", "and"}
def words(t): return {w.strip(",.:?").lower() for w in t.split()} - STOP
def top_chunks(question, k=2):
    q = words(question)
    scored = [(len(q & words(t)), cid) for cid, t in chunks.items()]
    return sorted(scored, reverse=True)[:k]
```

1. Split the manuals into chunks with IDs such as `bandsaw/p14` (done above).
2. Score each chunk by words shared with the question. The question's words, after dropping stop words, are {change, bandsaw, blade}. p14 shares all 3, p15 shares 2 (bandsaw, blade), and laser/p07 shares 1 (change).
3. `top_chunks(...)` returns `[(3, 'bandsaw/p14'), (2, 'bandsaw/p15')]`. Put those two in the prompt: about 400 tokens each is 800 tokens, instead of 48,000. That is 60 times fewer.
4. A failure: a chunk that reads only "Remove it before step 3" does not say which machine. So we added a short header to each chunk ("Bandsaw manual, blade change:").
5. Just-in-time variant: keep only the IDs in context and give the agent a `read_page(id)` tool, so text loads only when needed. Many systems mix both.

Takeaway: retrieval puts only the chosen chunks into one call's input, and each chunk must carry enough context to make sense alone.

### Practice
New case: the makerspace has a 40-page safety sheet of about 20,000 tokens, needed in almost every request, plus 30 long manuals (say about 48,000 tokens each, 30 x 48,000 = 1,440,000 in total).

Question: What do you do?

Options:
a) Load a one-page rules summary; retrieve everything else.
b) Retrieve everything, since retrieval is the modern approach.
c) Load every manual and sheet into every request.
d) Load nothing; the model already knows the rules.

Answer: a.

Feedback:
- Right answer (a): a short document needed every time is cheap to load whole. At about 500 tokens over 10 steps it costs 5,000 tokens. The sheet's detail and the manuals are retrieved when needed. Loading all 20,000 tokens of the sheet would cost 20,000 x 10 = 200,000 tokens per 10-step request.
- b: you think retrieval is always better because it sounds advanced. A short, always-needed rules page is simpler and safer to load whole, since a bad search could miss it. (If the whole knowledge base were about 200,000 tokens or less, you could even skip retrieval.)
- c: 1,440,000 tokens for manuals alone is far over any window, and it would be paid again at every step.
- d: the model learned nothing about this makerspace's rules in training. Only text you give it can contain them.

### Misconception
Wrong idea: "Retrieval makes the model know the manual."
Why it is tempting: after retrieval it answers correctly, so it feels like it knows.
Why it fails: retrieval only places chosen text in this call's input. Ask about a blade change with a search that returns `laser/p07` (the filter page) and the right page never arrives, so the model has nothing correct to work from.

## Section 5: Notes as memory between sessions
Learning objective: explain how notes saved in files give memory between sessions, and who runs the save and load.
Target words: 330

### Worked example
Setup: a game does not keep your progress in RAM after you quit. It writes a save file and loads it at next launch. The same idea works for student training status. A session is one visit, ending when the program stops sending the transcript. A memory store is files the program keeps outside the context window and loads later. Student 4417 completes laser cutter training on 24 Nov 2026.

1. During the loop the model requests: `create /memories/students/4417.md` with "laser cutter: trained 2026-11-24; bandsaw: not trained". It only requests.
2. The program (not the model) checks that the path is under `/memories`, applies a size cap and writes the file.
3. The visit ends and the transcript is thrown away.
4. At the next visit a new session starts with an empty transcript. The model knows nothing about 4417.
5. The program views the file and puts its text in the context. The model now answers "You're cleared for the laser cutter, not the bandsaw."
6. Only three of the memory operations appear here:

```python
def run_memory(cmd):                       # the PROGRAM runs this
    path = check_path(cmd["path"])         # must be inside /memories
    if cmd["op"] == "view":        return read(path)
    if cmd["op"] == "create":      write(path, cmd["text"][:MAX_BYTES])
    if cmd["op"] == "str_replace": replace(path, cmd["old"], cmd["new"])
```

Design tension: notes can be wrong or stale, so a real training record may belong in the makerspace's own database, which the model reads through a tool. Storing student data also raises privacy questions, which come later.

Takeaway: memory between sessions is files the program saves and loads, and the model's own part is only asking for them.

### Practice
Question: A student says "I finished bandsaw training yesterday." Should the assistant write that to the memory file?

Options:
a) Yes, memory exists to store whatever students say.
b) Not before checking it against the official record.
c) Yes, so the model can learn this student.
d) No, because the model cannot write any files.

Answer: b.

Feedback:
- Right answer (b): notes are text the model writes, so they can hold unverified claims. A wrong "trained" note could clear someone for a dangerous machine. Check the official record first, then save.
- a: you think memory means store everything. A note is only as good as its source, and a student's claim is not a verified fact.
- c: you think memory trains the model. It does not. The model is unchanged and only the file persists.
- d: you think the model has no write access, which is half right. The model asks for a write and the program does it, so writing is possible. The problem is checking, not ability.

### Misconception
Wrong idea: "Memory means the model learns or changes."
Why it is tempting: "remembers you" sounds like the model itself has changed.
Why it fails: delete `/memories/students/4417.md` and the assistant forgets student 4417 at once, though nothing else changed. Everything it knew was in the file, and the model is exactly as it was.

## Section 6: Main worked example and faded decision exercise
Learning objective: apply objectives 1 to 5 together.
Target words: 600 (worked example about 300, faded practice and solution about 300)

### Worked example
Setup: a returning student (ID 5108) asks "Can I use the bandsaw tomorrow afternoon, and how do I swap the blade?" Illustrative numbers: system prompt plus tool descriptions 800 tokens; the student's note 60 tokens; the question 25 tokens; each retrieved chunk about 400 tokens. The note says "laser cutter: trained; bandsaw: not trained". The window is the 32,000 from section 1.

| What | Timescale | Where it lives |
|---|---|---|
| System prompt, tools, note, question | one call | the context window |
| Request and result so far | between steps | the transcript, re-sent by the program |
| Student's training status | between sessions | a file in the memory store |
| Manual pages | fetched when needed | the chunk index |

1. Session start: the program loads student 5108's note (memory between sessions).
2. Call 1 receives system prompt, tools, note and question: 800 + 60 + 25 = 885 tokens (the context window).
3. The model sees "bandsaw: not trained", so it will not book the bandsaw and will say why. For the blade question it requests `search_manual("bandsaw blade change")`, about 30 tokens.
4. The program runs the search and appends the top 2 chunks, 2 x 400 = 800 tokens. Call 2 receives 885 + 30 + 800 = 1,715 tokens. The model requests a note update (`str_replace`: "asked about bandsaw blade, not yet trained", about 40 tokens), and the program writes it.
5. Clearing old tool results is not needed for a loop this short. In a 10-step loop it would be, as in section 3.
6. Call 3 receives 1,715 + 40 + 20 (the "ok" result) = 1,775 tokens. The model gives the final answer: "Not booked: you aren't trained on the bandsaw. Here are the blade steps; please take training first."

Total input: 885 + 1,715 + 1,775 = 4,375 tokens, about 4,400. If the 48,000-token manual were preloaded, every call would carry it: at least 3 x 48,000 = 144,000 tokens, and it would not fit in the 32,000 window at all.

Takeaway: each piece goes where it is cheapest and safest: the note in memory between sessions, the manual retrieved by chunk, and the transcript carrying results between steps.

### Faded practice
New case: returning student 5230 asks "Book me the 3D printer Friday and tell me the filament temperature." The note says "3D printer: trained 2026-10-02; laser cutter: not trained". Use the same illustrative sizes: 800 tokens for system prompt and tools, 400 per chunk, a calendar result of about 100 tokens, a note of 50 tokens, a question of 20 tokens.

1. (Given) Session start: the program loads the student's note and puts it in context.
2. Call 1 receives: ____. How many tokens is that? (Hint: what is in the transcript now?)
3. The model requests `check_calendar(3d_printer, Friday)`. Who runs it, and what is appended to the transcript? ____
4. For the filament temperature, what do you retrieve, and how many tokens does it add? ____
5. At the end, what do you save to the note, and what do you clear or leave out? ____

Answer:
2. System prompt and tools, the note, and the question: 800 + 50 + 20 = 870 tokens.
3. The program runs it. It appends the request and the calendar result (about 100 tokens) to the transcript, so the next call receives about 870 + 30 + 100 = 1,000 tokens.
4. Retrieve only the 3D printer chunks that mention filament, the top 2, with a header naming the machine: 2 x 400 = 800 tokens. Do not load the whole manual.
5. Save the booking (for example "booked Friday 14:00"), because the calendar tool returned it, so it is verified. Do not save the filament temperature, since the manual can supply it again. Clear the calendar result if the loop runs long.

Feedback checklist:
- You put the manual in as retrieved chunks. If you loaded the whole manual (about 48,000 tokens), it would not fit in the window and would be re-sent every step.
- You said the program runs each tool. If you wrote "the model runs it", reread section 2: the model only requests.
- You saved only the verified fact. If you saved something the student only said, reread section 5: the model's notes can carry unchecked claims.
- You counted tokens as a sum over calls. If you gave one number, remember each call re-sends the transcript.

## Section 7: Summary and Go further
Learning objective: consolidate in the learner's own words.
Target words: 120 (no worked example; one prompt with a model answer on demand)

### Practice
Question: In your own words, in three sentences, explain to a teammate why the assistant cannot "just remember" a student.

Model answer (example): Each model call sees only the text sent with it, and the model keeps nothing afterward. Within one request the program re-sends the transcript, and between visits the program saves notes in a file and loads them into the next call. So "memory" is something we build, and we choose what to save and what to leave out.

Feedback checklist: Did you say the model keeps nothing? Did you say the program does the saving and loading? Did you avoid saying the model "learns" the student? If one is missing, add it and try again.

### Misconception
Wrong idea: "A good enough model would just remember."
Why it is tempting: people remember each other, so it seems like a built-in feature.
Why it fails: a model maps text in to text out (record 0001). With no text about the student in the input, no model, however good, can know them.

## Notes for the writer
- The 3/4-word-per-token rule and every window size, token count and cost proportion are uncited and illustrative; the lesson should say so wherever they appear. No prices are used.
- The plan says student 4417 visits "Monday" and trains on 2026-11-24, but 24 Nov 2026 is a Tuesday. I used the date without the weekday. Keep it that way.
- Section 3 simplifies: call n is counted as sending n pages, although the nth page arrives after call n. State this simplification in the setup (it is in the setup text).
- Section 6 assumes the team's policy is to explain the blade steps to an untrained student while declining to book. The plan says only that it "stops booking and says so". If you think that is unsafe, change the final answer to "take training first" and skip the steps. The numbers hold either way.
- The manual chunk texts, the filament manual chunk, and the 20,000-token safety sheet are invented for illustration. No real temperatures are given; keep it that way.
- Section 4's practice has the learner's nuanced answer (one-page rules load, retrieve the rest). The "one-page rules summary of about 500 tokens" is my own illustrative number, not in the plan.
- The privacy and "training record may belong in a database" lines are each kept to one sentence, as the plan asks.
- Section 0 and section 7 have no worked example by plan. The quiz should not reuse the 30,000-word question, the 8-step booking agent, the safety sheet, the "finished bandsaw training yesterday" case or the 3D printer case.
