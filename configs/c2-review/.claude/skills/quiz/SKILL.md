---
name: quiz
description: Write a quiz and its answer key on one objective for this learner - items that test understanding through practical cases at a planned mix of difficulty, with a key that explains step by step why each answer is right - or give an existing quiz in the chat.
argument-hint: "Which objective, and how many questions?"
---

# Quiz

You write quizzes and their answer keys for the learner in this workspace.
A quiz checks whether the learner can *use* an idea, not whether they remember a sentence.
Write the quiz in this conversation, have the `quiz-reviewer` subagent check the draft (step 4), and finish with a short message to the learner.

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

## 3. Write the draft quiz and key

Write the draft to `drafts/quiz-NNNN.json` and `drafts/key-NNNN.json`, in exactly the shapes `FORMATS.md` gives for a quiz and a key.
Never write a draft into `quizzes/` or `keys/`: those folders get the final files once, in step 5.

**Stems and options**

- One question per stem, complete on its own, in plain exact words.
  Name the criterion whenever a stem asks which is "best", "most" or "better": better for what?
- No double negatives, no "all/none of the above", no trick wording, and no item that gives away another.
- For `mcq`: usually four options, each one plausible to someone holding the misconception or error it encodes, all of similar length, grammar and detail; vary where the right one sits.
- For `numeric`: the unit in the stem and in `unit`, and the precision you expect.
- For `short`: ask for a word or a short phrase, never a sentence or a reason, so the key can list its correct wordings in `accepted`; when the reason matters, make it an `mcq`.
- For `numeric`: ask for exactly one number and name it plainly; when it is a comparison, say outright that you want the difference, not either total.

**The key's `rationale` explains, not just asserts.** For every item:

- Say why the answer is right as a short chain of reasoning, in two to four sentences: the idea that applies, how it applies to this case, and the conclusion.
- For a `numeric` item, show every step of the calculation with its units, ending in the answer.
- Say what the most tempting wrong answer shows, and why it is wrong.
- Fill `distractors` with the misconception id behind each wrong `mcq` option that has one, reusing the workspace's ids.

## 4. Check, then review with the quiz-reviewer

First check the draft yourself:

1. Answer every item from its stem alone, without looking at your key, and compare.
2. For each item, try to argue for a second answer the way a careful expert would, and the way a learner who reads the stem literally would; rewrite until only one answer survives.
3. Check the plan against the draft: every core idea covered, the levels mixed as planned, every item on the objective and carrying its id, and no item repeating one of the lesson's practice questions.

Then run the review loop, at most **two passes**:

1. Start the `quiz-reviewer` subagent with the Agent tool. Its task message names: the draft quiz and draft key paths, the objective's id and text, the lesson's path in `lessons/` if there is one (or that there is none), and the pass number.
   It sees nothing of this conversation, so the message must carry all of that.
2. **Wait for its report before you do anything else.** Do not revise, write a final file or finish while it is running.
3. If the verdict is `CLEAN`, the loop ends.
4. Otherwise, fix every finding in the drafts, or note why you did not (for example, a finding you are sure is wrong, with the reason).
   For each item you change, answer it again from its stem alone.
5. If this was pass 1 and you changed anything, start pass 2 on the revised drafts. After pass 2, the loop ends whatever the verdict; fix what pass 2 found without another review.

## 5. Write the final files and the record

1. Write the final quiz to `quizzes/NNNN.json` and the final key to `keys/NNNN.json`, once each, with the content of the revised drafts (Write the files; no job needs the shell).
2. Write `review-records/NNNN-quiz.md`: how many passes ran; for each pass, the reviewer's findings as it listed them (item id, check, what was wrong) and what you changed for each, or why you did not; and the final verdict.

## 6. Finish

Finish with a short message: the quiz's path, its objective, how many items and which ideas they cover, and that you will grade it when they send their answers.
Never put an answer, a hint or anything from the key in the message.

## Giving a quiz in the chat

Show the quiz's title and each item's stem and options from `quizzes/`, and never anything from `keys/`.
Do not give or check answers while the learner is taking it.
When they have answered every item, write their answers exactly as given to the next `submissions/sN.json`, as `FORMATS.md` shows, and tell them `/grade` will grade it.
