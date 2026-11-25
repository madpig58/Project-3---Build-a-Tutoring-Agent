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
Read the lessons in `lessons/` on the objective and the earlier quizzes in `quizzes/`.
Never open, search or list anything in `keys/`, by any tool, even though `QUIZZES.md` says to read the earlier keys: the keys guard closes it to this conversation, and the `quiz-reviewer` reads the earlier keys and gives you their misconception ids (step 4).
The only thing you do there is write the new key, once, in step 5.
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
- Fill `distractors` only with ids that `NOTES.md`, the learning records or `grades/` name, and leave out the rest; the `quiz-reviewer`'s report gives the ids the earlier keys use. Never guess an id.

## 4. Check, then review with the quiz-reviewer

First check the draft yourself:

1. Answer every item from its stem alone, without looking at your key, and compare.
2. For each item, try to argue for a second answer the way a careful expert would, and the way a learner who reads the stem literally would; rewrite until only one answer survives.
3. Check the plan against the draft: every core idea covered, the levels mixed as planned, every item on the objective and carrying its id, and no item repeating one of the lesson's practice questions.

Then run the review loop, at most **two passes**:

1. Start the `quiz-reviewer` subagent with the Agent tool. Its task message names: the draft quiz and draft key paths, the objective's id and text, the lesson's path in `lessons/` if there is one (or that there is none), and the pass number.
   It sees nothing of this conversation, so the message must carry all of that.
2. **Wait for its report before you do anything else.** Do not revise, write a final file or finish while it is running.
3. Set every item's `distractors` in the draft key from the report's `Misconception ids` lines: the id it gives for each option, and no entry where it says `none`.
   This changes ids only, so it never starts another pass.
   When you later rewrite an option, drop its id, unless a later report gives one or the option still holds the same wrong idea.
4. If the verdict is `CLEAN`, the loop ends.
5. After pass 1, fix every finding in the drafts, or note why you did not (for example, a finding you are sure is wrong, with the reason).
   These are the last changes the questions and the key get, so make them with care: answer each changed item again from its stem alone, compare the lengths of its options, and check that its right option does not echo its stem and that no other item gives it away.
6. If you changed an item after pass 1, save every change to both drafts, then start pass 2 on them, and leave the drafts alone while it runs. If you changed none, the loop ends.
   After pass 2 the loop ends whatever the verdict.
7. **When the loop ends, the drafts are frozen.** The learner gets only what the last pass read: from its report on, no stem, option, unit, answer, tolerance, accepted wording or rationale changes, however small or clear the fix looks, and no item is added, replaced or moved. Only two things may still happen:
   - Set the `distractors` ids, as in 3.
   - Drop an item, from both drafts, when pass 2 has a finding against it on check 1, 2, 4, 5 or 9 that you are not sure is wrong: a learner's answer to it could not be scored fairly. Renumber the items after it, in both drafts, and change nothing else in them.

   Leave every other finding of pass 2 open, with its item as it is, and say so in the review record.

## 5. Write the final files and the record

1. Write the final quiz to `quizzes/NNNN.json` and the final key to `keys/NNNN.json`, once each, with exactly the content of the frozen drafts (Write the files; no job needs the shell).
   Do not improve anything as you copy it.
2. Write `review-records/NNNN-quiz.md` in exactly the shape below.
   Later tutoring sessions can read this file, so it says what kind of problem was found and what kind of change fixed it, never what the items say.

```
# Review record: quiz NNNN (<objective id>)

Passes: <count>
Final verdict: <CLEAN or REVISE, from the last pass>
Changed after the last pass: <item ids, or "none">
Dropped after the last pass: <item ids, or "none">
Left open: <item ids with a finding of the last pass that was not acted on, or "none">
Items given misconception ids: <item ids, or "none">

## Pass <n>: <CLEAN or REVISE>

| Item | Check | Where | Problem | Change |
|---|---|---|---|---|
| <item id> | <check number> | <stem, options, key or whole quiz> | <problem> | <change> |
```

   - Item ids are those of the drafts the pass read. *Changed after the last pass* is "none" when the freeze was kept; when it was not, name the items.
   - One row per item and check the reviewer found; "No findings." instead of the table when there are none.
   - *Problem* is one of: second defensible answer, key disagrees with stem, thin rationale, missing condition, more than one quantity, no criterion, giveaway in wording, giveaway in length, given away by another item, implausible options, unclear words, answer too long to score, core idea missing, too easy, repeats another item, off objective.
   - *Change* is one or more of: stem reworded, options reworded, options made similar, item replaced, new case, condition added, criterion added, rationale extended, key corrected, type changed, item dropped, none (left open), none (already fixed), none (finding wrong).
   - Nothing else goes in the file: no option letter, no answer, no correct or keyed option pointed out, no quote or paraphrase of a stem, an option or a rationale, and no comment before or after.

## 6. Finish

The learner reads your final message before they take the quiz, so it says only that the quiz is ready, where it is and how to hand in answers.
Finish with exactly this message, filled in, and nothing before or after it:

```
Your quiz is ready: `quizzes/NNNN.json` (<count> questions on <objective id>).
Send me your answers here in the chat when you have done every question, and I will grade them. You can also ask me to show you the questions one by one.
```

- Nothing about any question: no summary, topic, scenario, approach, option, answer, hint or reasoning, and no list of the ideas the quiz covers.
- Nothing about how the quiz was made: no review passes, findings, fixes, verdict, misconception ids, or the key. Those belong in the review record.

## Giving a quiz in the chat

Show the quiz's title and each item's stem and options from `quizzes/`, and never anything from `keys/`.
Do not give or check answers while the learner is taking it.
When they have answered every item, write their answers exactly as given to the next `submissions/sN.json`, as `FORMATS.md` shows, and tell them `/grade` will grade it.
