---
name: grade
description: Grade the learner's submission to a quiz - a verdict and misconception for every item, and feedback that says what was wrong, why it went wrong, and how to fix it - then record what the grades show.
argument-hint: "Which submission should I grade?"
---

# Grade

You grade the learner's answers to a quiz in this workspace and give them feedback they can act on.
Do the job in this conversation, in one pass, and finish with a short message to the learner.

## The request

$ARGUMENTS

If the request above is empty, the request is the learner's latest message.
If the learner gave their answers in the chat instead of a submission file, write them exactly as given to the next `submissions/sN.json`, as `FORMATS.md` shows, and grade that.

## Read first

The current directory is the workspace root; every path is relative to it.
Read `FORMATS.md` (the exact shape of a grades file: follow it to the letter), `MISSION.md`, `PREFERENCES.md`, `NOTES.md` and every file in `learning-records/`.
Then read `.claude/skills/teach/references/GRADING.md`, the general guide: its rules for verdicts and misconceptions hold here unchanged.
Then read the quiz, its key, the submission, and the lesson on the quiz's objective if there is one.
Never write anything under `.claude/`, and never edit `PREFERENCES.md`.

## 1. Decide each verdict

For every item, in order, including unanswered ones:

1. Work out what the response means, not how it is worded.
2. Compare that meaning with the key's `answer` and `rationale`, by the rules in `GRADING.md`: `correct`, `partial` or `wrong`.
3. Name the misconception id the response shows, from the key's `distractors` or the ids the workspace already uses, or `null`; never invent an id.
4. If you are sure the key itself is wrong, grade against what is actually correct and say so in the summary.

## 2. Write the feedback

Write each item's feedback to the learner, the way `PREFERENCES.md` asks for feedback: direct and constructive, with the reasoning, and no empty praise.
Two to four short sentences, in plain words, following the pattern for its verdict.

- **Wrong:** three parts, in this order.
  1. *What went wrong:* name the learner's answer and what it claims, in their terms ("You picked ..., which says ...").
  2. *Why it went wrong:* the reasoning error or wrong belief behind it, why it is tempting, and the right idea, with a short concrete example or the step of working that shows it.
  3. *How to fix it:* one specific thing to do next time, such as a question to ask yourself, a check to run, or the lesson section to reread.
- **Partial:** what was right, exactly which part was off and why, and how to fix that part.
- **Correct:** three parts, in two to four sentences, with no praise beyond a plain "Right".
  1. *Why it is right:* the reasoning that gets to the answer in one sentence, so the learner knows they were right for the right reason and not by luck; if they gave a reason, say whether it is the key reason, and for an unusual route, why it works.
  2. *Why the tempting alternative fails:* for an `mcq`, the distractor most likely to have pulled them, and the one fact that rules it out; for a `numeric` or `short` item, the most common slip.
  3. *Where it goes next:* the one insight that makes it stick, or how the idea links to the next one, a harder case, or the mission.

For a calculation, show the corrected working with its units.
Never just restate the key's answer: the learner should be able to see how to reach it.
Do not blame; describe the error, not the learner.

## 3. Write the summary

The `summary`, in three or four sentences: what the learner has down; the one most important thing to work on, named plainly; and one concrete next step, such as a lesson section to revisit, a practice to try, or a quiz to retake.
If several items share a misconception, say so here, once.

## 4. Write the files

1. Write `grades/NNNN-sN.json` exactly as `FORMATS.md` shows, with one entry per quiz item in the quiz's order, and non-empty feedback for every item.
2. Write a learning record for what the grades show (an understanding, or a misconception to work on) in the format in `.claude/skills/teach/references/LEARNING-RECORD-FORMAT.md`.
3. Update `NOTES.md` with what the learner now knows and does not yet know.

## 5. Finish

Finish in the chat with the summary and the one next step, and the path of the grades file.
