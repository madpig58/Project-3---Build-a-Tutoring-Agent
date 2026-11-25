---
name: grade
description: Grade the learner's submission to a quiz - a verdict and misconception for every item, and feedback that says what was wrong, why it went wrong, and how to fix it - then record what the grades show.
argument-hint: "Which submission should I grade?"
---

# Grade

You run the grading of the learner's answers to a quiz in this workspace and give them feedback they can act on.
You never read the answer key: `keys/` is closed to this conversation by the keys guard, and only the `grader` and `grade-reviewer` subagents may read it.
The `grader` subagent grades (step 1), the `grade-reviewer` subagent checks its draft (step 2), and you write the final files and finish with a short message to the learner.

## The request

$ARGUMENTS

If the request above is empty, the request is the learner's latest message.
If the learner gave their answers in the chat instead of a submission file, write them exactly as given to the next `submissions/sN.json`, as `FORMATS.md` shows, and grade that.

## Read first

The current directory is the workspace root; every path is relative to it.
Read `FORMATS.md` (the shape of a grades file), `MISSION.md`, `PREFERENCES.md`, `NOTES.md` and every file in `learning-records/`.
Then read the quiz and the submission, and find the lesson on the quiz's objective in `lessons/` if there is one.
Never open, search or list anything in `keys/`, by any tool: the key's path goes into the subagents' task messages, and they read it.
Never write anything under `.claude/`, and never edit `PREFERENCES.md`.

## 1. The grader writes the draft

1. Start the `grader` subagent with the Agent tool. Its task message names: the quiz (`quizzes/NNNN.json`), its key (`keys/NNNN.json`), the submission, the lesson's path in `lessons/` if there is one (or that there is none), the draft's path, `drafts/grade-NNNN-sN.json`, and pass 1.
   It sees nothing of this conversation, so the message must carry all of that.
2. **Wait for its report before you do anything else.**
3. Check that the draft exists and has one entry per quiz item, in the quiz's order, with non-empty feedback; if not, start the grader again with what is missing.

Never decide or change a verdict or a misconception id yourself: without the key you cannot know them.

## 2. Review with the grade-reviewer

1. Start the `grade-reviewer` subagent with the Agent tool. Its task message names: the draft's path, the quiz, its key, the submission, the lesson's path in `lessons/` if there is one (or that there is none), and the pass number.
2. **Wait for its report before you do anything else.** Do not revise, write a final file or finish while it is running.
3. Act on the report, at most **two review passes** in all:
   - verdict `CLEAN` (no major findings): fix the minor findings yourself in the draft, with Edit, when they are about wording, length or the summary's style (checks 6 to 9); stop, with no second pass;
   - verdict `REVISE` on pass 1: start the `grader` again (pass 2) with the draft's path, the same quiz, key, submission and lesson, and every finding of the report copied exactly; wait for its report; then start the `grade-reviewer` on pass 2, which checks above all the items that changed;
   - after review pass 2: send any major findings to the `grader` for one last revision and wait for it, fix the minor ones yourself as above, and stop, whatever the verdict.

A finding about a verdict, a misconception id or a fact always goes to the `grader`; you fix only wording.

## 3. Write the final files and the record

1. Write `grades/NNNN-sN.json` once, with the content of the final draft (Write the file; no job needs the shell).
2. Write `review-records/NNNN-sN-grade.md`: how many grader and review passes ran and why the loop stopped; for each review pass, the reviewer's findings as it listed them (item, check, major or minor, what was wrong) and who fixed each one (the grader or you), or why it was not fixed; the grader's reports; and the final verdict.
3. Write a learning record for what the grades show (an understanding, or a misconception to work on) in the format in `.claude/skills/teach/references/LEARNING-RECORD-FORMAT.md`, from the grades file.
4. Update `NOTES.md` with what the learner now knows and does not yet know.

## 4. Finish

Finish in the chat with the summary and the one next step, and the path of the grades file.
