---
name: quiz
description: Write a quiz and its answer key on one objective for this learner - items that test understanding through practical cases at a planned mix of difficulty, with a key that explains step by step why each answer is right - or give an existing quiz in the chat.
argument-hint: "Which objective, and how many questions?"
---

# Quiz

You write quizzes and their answer keys for the learner in this workspace.
A quiz checks whether the learner can *use* an idea, not whether they remember a sentence.
Do the job in this conversation, in one pass, and finish with a short message to the learner.

## The request

$ARGUMENTS

If the request above is empty, the request is the learner's latest message.
If the learner wants to take an existing quiz in the chat, go to **Giving a quiz in the chat**.

## Read first

The current directory is the workspace root; every path is relative to it.
Read `FORMATS.md` (the exact shape of a quiz and a key: follow it to the letter, and add no keys it does not list), `MISSION.md`, `PREFERENCES.md`, `NOTES.md` and every file in `learning-records/`.
Then read `.claude/skills/teach/references/QUIZZES.md`, the general guide; where it and this skill differ, this skill wins.
Read the lessons in `lessons/` on the objective and the earlier quizzes in `quizzes/`; read earlier keys and grades only for the misconception ids they use.
Never write anything under `.claude/`, and never edit `PREFERENCES.md`.

## 1. Pin down the quiz

- The objective, its id, and the number of items asked for (four or five if none is given).
- The next number in `quizzes/`; the key takes the same number in `keys/`.
- The objective's core: the three to six ideas a learner must get right to have met it, from its lessons or, when there are none, from a high-trust source you search for and read.
  Write the core down as a short list before writing any item.

## 2. Plan the items before writing them

Make a plan, one line per item: which core idea it tests, its level, its type, and the practical case it uses.

- **Coverage:** every core idea gets at least one item before any idea gets a second, and no item tests trivia or the lesson's wording.
- **Levels:** use three levels, and mix them through the quiz rather than stacking the hard ones at the end:
  - *understand*: explain or recognize what the idea means in a plain case (about one item in five, never more than one in three);
  - *apply*: use the idea in a new, concrete situation to predict, compute or choose (most items);
  - *analyze*: compare two designs or diagnose a failure, where the learner must weigh more than one idea (one or two items).
  No item is pure recall of a definition or a sentence to finish.
- **Practical cases:** set most items in a short, realistic situation, drawn from the mission and from the examples `PREFERENCES.md` names (for this kind of learner, code, games, and real systems), and give the learner every fact, number and condition the answer depends on.
  Vary the cases; do not reuse the lesson's own examples or practice questions.
- **Types:** `mcq` when the typical errors are predictable, `numeric` when the idea involves a quantity, `short` when the learner should produce the idea in a few words; mix them when the objective allows.

## 3. Write the quiz and the key

Write `quizzes/NNNN.json` and `keys/NNNN.json` exactly as `FORMATS.md` shows.

**Stems and options**

- One question per stem, complete on its own, in plain exact words.
  Name the criterion whenever a stem asks which is "best", "most" or "better": better for what?
- No double negatives, no "all/none of the above", no trick wording, and no item that gives away another.
- For `mcq`: usually four options, each one plausible to someone holding the misconception or error it encodes, all of similar length, grammar and detail; vary where the right one sits.
- For `numeric`: the unit in the stem and in `unit`, and the precision you expect.
- For `short`: ask for a word, a phrase or one sentence, so the key can list its correct wordings in `accepted`.

**The key's `rationale` explains, not just asserts.** For every item:

- Say why the answer is right as a short chain of reasoning, in two to four sentences: the idea that applies, how it applies to this case, and the conclusion.
- For a `numeric` item, show every step of the calculation with its units, ending in the answer.
- Say what the most tempting wrong answer shows, and why it is wrong.
- Fill `distractors` with the misconception id behind each wrong `mcq` option that has one, reusing the workspace's ids.

## 4. Check for ambiguity before you finish

1. Answer every item yourself from its stem alone, without looking at your key, and compare.
2. For each item, try to argue for a second answer the way a careful expert would, and the way a learner who reads the stem literally would.
   If either argument works, rewrite the stem or the options until only one answer survives, and check again.
3. Check the plan against the result: every core idea covered, the levels mixed as planned, every item on the objective and carrying its id.
4. Check that the quiz file holds no answers and that no item repeats one of the lesson's practice questions.

## 5. Finish

Finish with a short message: the quiz's path, its objective, how many items and which ideas they cover, and that you will grade it when they send their answers.
Never put an answer, a hint or anything from the key in the message.

## Giving a quiz in the chat

Show the quiz's title and each item's stem and options from `quizzes/`, and never anything from `keys/`.
Do not give or check answers while the learner is taking it.
When they have answered every item, write their answers exactly as given to the next `submissions/sN.json`, as `FORMATS.md` shows, and tell them `/grade` will grade it.
