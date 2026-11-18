# Evaluation report

This is the report on what each step of your architecture bought and what it cost.
I read it for one thing above all: whether each claim matches its evidence, including the steps that did not pay.
A step you measured carefully and then dropped is as good a result as a step that won.

Three kinds of material go here.
The tables are pasted from commands: `uv run p3 report --configs a,b` for the objective checks, the cost and your ratings, and `uv run p3 compare --reveal <session-id>` for each blind comparison.
Paste them as they are, and name the session id or the run ids next to each one, so I can find them in `bench/compare/` and `bench/runs/`.
The evidence from your reviews stays in `reviews/`, and here you point at it: name the round, such as `c2-review` Round 3, or the criterion, such as the `c1-skills` review's Wording and possible misreadings, so I can follow the trail.
The prose is yours.

Each section ends with a marker line.
Replace that line with your own writing; `uv run p3 check --final` fails while one is left.

Words used below.
**Your ratings** is the table `p3 report` prints from your major reviews, one row per criterion and one column per step, from 1 to 5.
A **round** is a quick round in one of your step files in `reviews/`, and its **What changed** is the change Claude Code made from your thoughts in it.
A **pass** is one revise-and-review iteration inside one of your tutor's review loops, so a loop capped at two passes reviews a draft at most twice.
A **tally** is the wins for each config and the ties in one blind comparison, and the **p-value** is the reveal's two-sided sign test on the picks that were not ties: with 10 such picks, 8 for one config is suggestive and 9 is strong.
**Could tell** is the share of pairs where you said you could tell which config made which.
The objective checks use the names `p3 report` prints, such as `teach_facts_correct`, `quiz_key_agreement`, `grade_false_wrong` and `tutor_leaks`, the README's section "The scenarios and the objective checks" lists them, and `guide/06-the-bench.html` ("The headline numbers") says what each one measures.
**Cost** is tokens, output tokens, minutes and subagents per scenario, and the list-price equivalent, which is not what you pay on a subscription.

---

## 1. The baseline, `c0-baseline`

Paste the `p3 report` table for `c0-baseline` (three full runs on the shared topic).

### Quality

| config | runs | teach facts | teach misconc. | length ratio | dead links | key agreement | wrong keys | ambiguous items | verdict agreement | false wrong | misconc. hit | leaks | behavior met |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `c0-baseline` | 3 | 1.00 | 0 | 0.71 (0.60-0.77) | 0 | 1.00 | 0 | 0 | 1.00 | 0.00 | 1.00 | 0 | 0.44 (0.33-0.50) |

Teach facts, key agreement, verdict agreement, false wrong, misconception hit and behavior met are shares (0 to 1); misconceptions, dead links, wrong keys, ambiguous items and leaks are counts per run.
A dash means no run could be scored on that check, and n= says how many of the runs could.
A job that failed counts against the config: no lesson scores 0 teach facts, no quiz and key 0 key agreement, a missing grades file disagrees on every item, and a tutor scenario with no reply is not met; leaks need a reply to check, so such a scenario is left out of them.
The length ratio is a rough reading-time estimate (visible words / 150) over the minutes requested; 0.6 to 1.5 counts as on length.

### Cost: teach

| config | runs | tokens | output tokens | minutes | subagents | list-price $ |
|---|---:|---:|---:|---:|---:|---:|
| `c0-baseline` | 3 | 755.5k (619.2k-969.8k) | 30.1k (25.8k-34.8k) | 3.2 (2.8-3.6) | 0 | 0.62 (0.54-0.70) |

### Cost: quiz

| config | runs | tokens | output tokens | minutes | subagents | list-price $ |
|---|---:|---:|---:|---:|---:|---:|
| `c0-baseline` | 3 | 148.1k (144.6k-152.3k) | 4.8k (4.0k-6.1k) | 0.7 (0.6-0.9) | 0 | 0.17 (0.16-0.19) |

### Cost: grade

| config | runs | tokens | output tokens | minutes | subagents | list-price $ |
|---|---:|---:|---:|---:|---:|---:|
| `c0-baseline` | 3 | 283.1k (255.8k-297.3k) | 7.1k (6.8k-7.3k) | 1.1 | 0 | 0.32 (0.31-0.33) |

### Cost: tutor

| config | runs | tokens | output tokens | minutes | subagents | list-price $ |
|---|---:|---:|---:|---:|---:|---:|
| `c0-baseline` | 3 | 627.0k (603.8k-653.0k) | 10.5k (9.9k-11.4k) | 2.7 (2.3-3.6) | 0 | 0.65 (0.64-0.66) |

### Cost: all jobs

| config | runs | tokens | output tokens | minutes | subagents | list-price $ |
|---|---:|---:|---:|---:|---:|---:|
| `c0-baseline` | 3 | 1.81M (1.66M-2.03M) | 52.4k (48.3k-55.8k) | 7.7 (6.8-8.9) | 0 | 1.77 (1.68-1.81) |

Costs are per run, summed over the job's scenarios; list-price $ is the list-price equivalent, not what you pay on a subscription.

**Baseline run IDs:**
- 20261117-034409-agent-architecture-m30-r1
- 20261117-035122-agent-architecture-m30-r2
- 20261117-040046-agent-architecture-m30-r3


What did the baseline do well, and where did it fall short, for each of the four jobs?
Read its outputs as you will read your own steps', because your `c1-skills` review compares against it.
Which of the gaps in `KNOWN-GAPS.md` did you see in your own runs, and did you find one that is not listed?
Which number moved the most from one run to the next, and what does that spread mean for a step measured on a single run?

The baseline performed well in technical accuracy. The teach job achieved a factual correctness score of 1.00 with no detected misconceptions or broken links. However, the average lesson length ratio was 0.71, which suggests that the lessons were substantially shorter than the requested 30 minutes.

The quiz job also performed well, with an answer-key agreement score of 1.00, no incorrect keys, and no detected ambiguous questions. However, these checks do not measure whether the questions require practical application or deeper reasoning.

The grade job achieved a verdict agreement of 1.00, a false-wrong rate of 0.00, and a misconception hit rate of 1.00. This shows that the baseline was already accurate at grading, although the quality and usefulness of its written feedback still need to be judged separately.

The tutor was the weakest part of the baseline. Its expected behavior score averaged only 0.44, even though it had zero direct answer leaks. KNOWN-GAPS.md describes failures involving overly revealing hints, explanations above the learner's level, and responses that exceeded the requested length. My benchmark scores are consistent with these problems, but individual traces need to be inspected to determine exactly which failures occurred in my runs.

The lesson length ratio varied from 0.60 to 0.77, while the tutor's expected behavior score varied from 0.33 to 0.50. Both ranges have a width of 0.17. This variation suggests that a single run may not represent the system's typical behavior.

Overall, the baseline provided a strong foundation in factual correctness, quiz generation, and grading accuracy, but needed improvements in lesson completeness and consistent tutoring behavior.

I compared my baseline outputs with KNOWN-GAPS.md and found several of the same problems.

In run 20261117-034409-agent-architecture-m30-r1, tutor-p01 refused to reveal the answer to quiz question 3, but its hints still narrowed down the correct choice. For example, it asked which option would stop the agent from continuing to spend money. This indirectly pointed toward the stopping condition rather than remaining neutral.

In tutor-p05, the tutor recognized that a full PPO derivation was outside the learner's goals but still included the PPO objective formula. This was unnecessarily complicated for a beginner. The formula also contained garbled characters in the output I inspected, although this may have been a terminal encoding issue.

In tutor-p06, the tutor used a clear restaurant analogy to explain tool calling, but its response appeared to exceed the requested length. The analogy was helpful, but the tutor did not fully respect the response-length constraint.

The lesson length issue also appeared in my baseline runs, with an average length ratio of 0.71.

I did not identify a clearly separate failure beyond the documented gaps in the outputs I inspected. These examples help explain why the baseline had zero direct answer leaks but an average expected tutoring behavior score of only 0.44.

---

## 2. Step 1: `c1-skills` against `c0-baseline`56

### What changed

Name the rounds that built this step, such as `c1-skills` Rounds 1 to 4, and the inventory entries of the skills they added; the trail from thoughts to change to outcome is already in `reviews/` and `reviews/components.md`, so do not retell it here.
Then what you put in `PREFERENCES.md`, and anything about how the four skills work together that no single inventory entry says.

The c1-skills version was developed through Rounds 1–6 in reviews/c1-skills.md. The four skills are documented in reviews/components.md under teach, tutor, quiz, and grade.

Rounds 1–3 improved lesson explanations and tutoring behavior. Round 4 introduced a separate quiz skill focused on application questions, mixed difficulty, and detailed answer explanations. Round 5 introduced a grade skill that provides structured feedback, while Round 6 improved feedback for correct answers.

My PREFERENCES.md emphasizes step-by-step explanations, practical examples related to programming and game development, and clear feedback without unnecessary praise.

Together, the four skills create a connected learning process. Teach explains the material, quiz checks understanding, grade identifies mistakes and misconceptions, and tutor helps the learner work through questions without revealing answers. Their separation also makes it easier to improve each part independently.

### Your review, the objective checks and the cost

Paste `uv run p3 report --configs c0-baseline,c1-skills`: the objective checks, the cost per job, and your ratings.

(p3-tutor) C:\Users\ohwj5\OneDrive\Desktop\CSCI598E\p3\Project-3---Build-a-Tutoring-Agent>uv run p3 report --configs c0-baseline,c1-skills
## Results on agent-architecture

Scored full runs (quick runs and --only runs left out); each cell is the mean over the runs, with the range in brackets.

### Quality

| config | runs | teach facts | teach misconc. | length ratio | dead links | key agreement | wrong keys | ambiguous items | verdict agreement | false wrong | misconc. hit | leaks | behavior met |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `c0-baseline` | 3 | 1.00 | 0 | 0.71 (0.60-0.77) | 0 | 1.00 | 0 | 0 | 1.00 | 0.00 | 1.00 | 0 | 0.44 (0.33-0.50) |
| `c1-skills` | 1 | 1.00 | 0 | 0.93 | 0 | 1.00 | 0 | 0 | 1.00 | 0.00 | 1.00 | 0 | 0.67 |

Teach facts, key agreement, verdict agreement, false wrong, misconception hit and behavior met are shares (0 to 1); misconceptions, dead links, wrong keys, ambiguous items and leaks are counts per run.
A dash means no run could be scored on that check, and n= says how many of the runs could.
A job that failed counts against the config: no lesson scores 0 teach facts, no quiz and key 0 key agreement, a missing grades file disagrees on every item, and a tutor scenario with no reply is not met; leaks need a reply to check, so such a scenario is left out of them.
The length ratio is a rough reading-time estimate (visible words / 150) over the minutes requested; 0.6 to 1.5 counts as on length.

### Cost: teach

| config | runs | tokens | output tokens | minutes | subagents | list-price $ |
|---|---:|---:|---:|---:|---:|---:|
| `c0-baseline` | 3 | 755.5k (619.2k-969.8k) | 30.1k (25.8k-34.8k) | 3.2 (2.8-3.6) | 0 | 0.62 (0.54-0.70) |
| `c1-skills` | 1 | 726.7k | 28.2k | 3.1 | 0 | 0.60 |

### Cost: quiz

| config | runs | tokens | output tokens | minutes | subagents | list-price $ |
|---|---:|---:|---:|---:|---:|---:|
| `c0-baseline` | 3 | 148.1k (144.6k-152.3k) | 4.8k (4.0k-6.1k) | 0.7 (0.6-0.9) | 0 | 0.17 (0.16-0.19) |
| `c1-skills` | 1 | 194.7k | 8.3k | 1.2 | 0 | 0.22 |

### Cost: grade

| config | runs | tokens | output tokens | minutes | subagents | list-price $ |
|---|---:|---:|---:|---:|---:|---:|
| `c0-baseline` | 3 | 283.1k (255.8k-297.3k) | 7.1k (6.8k-7.3k) | 1.1 | 0 | 0.32 (0.31-0.33) |
| `c1-skills` | 1 | 283.6k | 7.9k | 1.1 | 0 | 0.32 |

### Cost: tutor

| config | runs | tokens | output tokens | minutes | subagents | list-price $ |
|---|---:|---:|---:|---:|---:|---:|
| `c0-baseline` | 3 | 627.0k (603.8k-653.0k) | 10.5k (9.9k-11.4k) | 2.7 (2.3-3.6) | 0 | 0.65 (0.64-0.66) |
| `c1-skills` | 1 | 523.2k | 7.9k | 1.8 | 0 | 0.57 |

### Cost: all jobs

| config | runs | tokens | output tokens | minutes | subagents | list-price $ |
|---|---:|---:|---:|---:|---:|---:|
| `c0-baseline` | 3 | 1.81M (1.66M-2.03M) | 52.4k (48.3k-55.8k) | 7.7 (6.8-8.9) | 0 | 1.77 (1.68-1.81) |
| `c1-skills` | 1 | 1.73M | 52.3k | 7.2 | 0 | 1.72 |

Costs are per run, summed over the job's scenarios; list-price $ is the list-price equivalent, not what you pay on a subscription.

## Your ratings

Your ratings from 1 to 5 in the major reviews (reviews/<step>.md), which review full runs on the shared topic; a dash means no rating there yet, one that p3 check does not accept, or a job that step does not review (Tutor in c2-review; Quiz, Feedback and Tutor in c3-split).

| job | criterion | c1-skills | c2-review | c3-split | final |
|---|---|---:|---:|---:|---:|
| Lesson | Technical correctness and facts | 5 | - | - | - |
| Lesson | Pedagogy | 4 | - | - | - |
| Lesson | Alignment with the learning goal | 5 | - | - | - |
| Lesson | Overall quality | 4 | - | - | - |
| Quiz | Difficulty | 4 | - | - | - |
| Quiz | Coverage of the lesson's core | 4 | - | - | - |
| Quiz | Wording and possible misreadings | 5 | - | - | - |
| Quiz | Writing quality | 4 | - | - | - |
| Quiz | Alignment with the learning goal | 4 | - | - | - |
| Feedback | Useful | 5 | - | - | - |
| Feedback | Explains enough | 4 | - | - | - |
| Feedback | Personalized to how I like things explained | 5 | - | - | - |
| Tutor | Guardrails | 4 | - | - | - |
| Tutor | Personalization | 4 | - | - | - |

**Run IDs:**

c0-baseline:
- 20261117-034409-agent-architecture-m30-r1
- 20261117-035122-agent-architecture-m30-r2
- 20261117-040046-agent-architecture-m30-r3

c1-skills:
- 20261117-053922-agent-architecture-m30-r1

### What the step bought and what it cost

For each job: what did your major review find against `c0-baseline`, and did the objective checks agree?
Where they disagree, which do you believe, and why?
`c1-skills` is also the first config with your `PREFERENCES.md`, while `c0-baseline` keeps the neutral one: which of the differences could come from your preferences rather than the skills?
What did the step cost per scenario, and was the gain worth it?
Say what one run of `c1-skills` against three of `c0-baseline` lets you claim, and what it does not.

The c1-skills version improved lesson completeness and tutoring behavior while maintaining the baseline's strong technical accuracy.

For teaching, the length ratio increased from 0.71 to 0.93 while factual correctness remained at 1.00. This agrees with my major review, where I rated pedagogy 4/5 and overall lesson quality 4/5. The lesson was more complete and used practical examples, although there was still room to improve its presentation.

For quizzes, answer-key agreement remained at 1.00, with no wrong keys or ambiguous items detected. My review rated difficulty and coverage 4/5 because practical applications and question variety matter beyond answer-key accuracy. The quiz cost increased from $0.17 to $0.22 per scenario, so the benefit needs to be judged mainly from the quality of the questions rather than the objective accuracy checks.

For grading, verdict agreement and misconception detection remained at 1.00, while the cost stayed at approximately $0.16 per scenario. My review rated the usefulness of feedback 5/5 because it explained mistakes and provided specific ways to improve. However, these qualitative improvements are not measured by verdict agreement alone.

For tutoring, expected behavior improved from 0.44 to 0.67, and direct answer leaks remained at zero. My live tests showed that the tutor could explain concepts through game NPC examples, avoid revealing quiz answers, and guide the learner through misconceptions. However, the remaining failed scenarios show that tutoring behavior was still inconsistent.

Some of these differences may be caused by my PREFERENCES.md rather than the skills themselves. The preferences emphasize game development examples, step-by-step explanations, and direct feedback. Since the baseline used neutral preferences, this comparison cannot isolate the contribution of the new skills.

The full benchmark cost decreased slightly from an average of 1.81 million tokens and 7.7 minutes to 1.73 million tokens and 7.2 minutes. The list-price equivalent decreased from $1.77 to $1.72. The quiz became more expensive, but the tutor became cheaper, while grading cost remained almost unchanged.

I think the improvements were worthwhile, particularly for lesson length and tutoring behavior. However, c1-skills was measured with only one full run, compared with three baseline runs. The results show promising improvements on this topic, but they do not prove that the gains are consistent across repeated runs or generalize to other topics.

---

## 3. Step 2: `c2-review` against `c1-skills`

### What changed

Name the rounds that built this step and the inventory entries of the reviewers they added, as in step 1.
Then the loops' design, for each of teach, quiz and grade: who reviews, what is on each reviewer's checklist and which items came from your `c1-skills` major review, how each reviewer gets a fresh context, how many passes a loop may run and what ends it early, and what each loop records.
Then one design choice you could have made the other way, such as one reviewer against several, a cap of one pass against three, or a reviewer that edits against one that only reports, and why you chose as you did.

TODO: the rounds and entries, and the design of your review loops.

### The loops as they ran

For teach, quiz and grade: how many review passes ran in your bench run, what the reviewers flagged, and whether the revisions moved anything you can point at, a fact corrected, an ambiguous item rewritten, feedback that changed.
The loop records in the run's outputs are the evidence; name the files.

TODO: what the review loops did in the run.

### Your review, the objective checks and the cost

Paste `uv run p3 report --configs c1-skills,c2-review`.

TODO: paste the report tables.

### What the step bought and what it cost

Did the problems your `c1-skills` review found go away, and which ratings moved?
Which loop earned its cost and which did not?
If a loop ran several passes and the final output was no better than the first draft, say so, because that is the finding.

TODO: your judgment of step 2.

---

## 4. Step 3: `c3-split` against `c2-review`

### What changed

Name the rounds that built this step and the inventory entries of the pipeline's subagents.
Then the split: the roles you split the teach job into, what each one receives and returns, what runs in order and what in parallel, and who puts the lesson together at the end.
Why this split and not a smaller one, and what did you try that you took out again?

TODO: the rounds and entries, and the design of your teach split.

### Your review, the objective checks and the cost

Paste `uv run p3 report --configs c2-review,c3-split`.

TODO: paste the report tables.

### What the step bought and what it cost

What did the split change in the lesson: its structure, its figures, its references, its fit to you, and how did your four Lesson ratings move against `c2-review`'s?
What did it cost in tokens, minutes and subagents against `c2-review`, and how much of that was overhead rather than writing?
Each step has one run, so say how confident you are, and what would change your mind.

TODO: your judgment of step 3.

---

## 5. `final` against `c0-baseline`, with repeats

### What went into `final`

A diagram of `final`: the main conversation, each skill, each subagent and the guard hook, with arrows for who starts whom and which files each one reads and writes.
ASCII art in a code block or a Mermaid block are both fine; for example:

```
/quiz (skill, main conversation)  writes drafts/0002.json
  -> quiz-reviewer (subagent, fresh context)  reads drafts/
  <- revise, at most 2 passes
  => quizzes/NNNN.json, keys/NNNN.json, review-records/NNNN-quiz.md
```

Draw yours, all four jobs, and delete the example.

TODO: your diagram.

What did you keep from each step, what did you drop, and why?
Point at the inventory entries in `reviews/components.md` rather than repeating them.
If `final` had to get cheaper tomorrow, which component would you cut first and which last, and what do you expect the tutor to lose?

TODO: what `final` is made of, and what you would cut first.

### Your review, the objective checks and the cost

Paste `uv run p3 report --configs c0-baseline,final`, with three scored runs of each.

TODO: paste the report tables.

### What the repeats let you claim

For each headline number: is the difference between the two configs larger than the spread between runs of the same config?
Where the ranges overlap, say "not distinguishable with three runs", and do not rank the two by their means.
Then the overall cost: how many times more tokens and minutes per scenario does `final` take, and for which jobs is it worth it, by your review and by the numbers?

TODO: your reading of `final` against the baseline.

---

## 6. The ablation

Which component did `final-minus-<x>` remove, and what did you expect to happen before you ran it?
Paste `uv run p3 report --configs final,final-minus-<x>`.
What changed, in quality and in cost, and does one run against three let you say the component matters?
If you looked at its outputs, what did you see that the numbers do not show?

TODO: your ablation, its prediction, its table and your reading.

---

## 7. The guard

What does your guard block, and what does it allow, and how does it tell the grader from the main conversation?
Why is it a PreToolUse hook in `tutor/.claude/settings.json`, and not a permission deny rule, a hook in a subagent's frontmatter, a subagent's `tools` list, or an instruction in a skill?
What changed elsewhere in the tutor because of it, such as grading handed to a subagent the guard allows?
Paste the result of running its tests, and list the cases they cover: the main conversation reading `keys/` with each of Read, Grep, Glob, Bash and PowerShell, the grader reading them, and the reads that must still work.
Then the bench evidence that the hook runs in the bench and not only in its tests: the run id and scenario of a trace where it allowed the grader's read of `keys/` or blocked the main conversation's, since a hook that fails to start lets every call through.
Then `tutor_leaks` for `final` against `c0-baseline`, and any denial of the guard you found in a trace.
Last, the gap you know of: one way the main conversation could still reach a key, or a case your tests do not cover, and why you accepted it or how you closed it.

TODO: the guard, its tests and the evidence.

---

## 8. The blind comparison

### `c0-baseline` against `final`

Paste the reveals of the four sessions (teach, quiz, grade, tutor), three run pairs each, with their session ids.

TODO: paste the four reveals with their session ids.

### Your open reviews against your blind picks

This is the check on your own bias, as lecture 24 checks a model judge's.
For each job, what did your open reviews say about `final` against `c0-baseline`: your `final` major review, written before the blind comparison, your `c1-skills` review's comparison with the baseline, and your ratings across the ladder?
Then, for each job, did the blind tally and your reasons agree with them?
Where they disagree, what do you think happened: knowing the labels shaped what you saw in the open, the outputs you judged blind differed from the ones you reviewed, or the difference was too small to see?
Did your picks follow your open reviews more often in the pairs where you could tell than in the pairs where you could not?
Which do you believe now, and what does that say about the ratings in your reviews?

TODO: your open reviews against your blind picks.

### A second blind comparison

For 498E this is optional: if you made one, say which configs and job, why you chose it, paste its reveal, and say whether it agreed with your open reviews.
For 598E, and for the length-study stretch, the length study's three comparisons are your second; say so here and write them up in section 13.
If you made no second comparison, say so in one line.

TODO: your second blind comparison, or why there is none.

---

## 9. The test topics

### The two topics

Name each topic and its id, why you chose it, and the commit in which you committed its items, before its first run.
If you fixed a real mistake in a topic after its runs, as `bench/own/README.md` describes, list the run ids you deleted, what you changed and why.

TODO: your two topics and their commits.

### Results

For each topic, paste `uv run p3 report --topic <id> --configs c0-baseline,final`, and sum up your open review of the topic in `reviews/final.md` in two or three sentences.

TODO: paste the tables for both topics, with your summaries.

### Did the architecture still pay off?

Compare each topic with the shared topic: did `final` win where it won before, and did it fail somewhere new?
Was there anything about the topic, its kind of knowledge or its learner, that explains the difference?
On the life-skill topic, did both configs stay inside general knowledge when your probe asked for personal advice?

TODO: your reading of the test topics.

### Your learning sessions against the bench

Your three learning sessions are in `reviews/final.md`.
Did the bench predict what you saw in them?
Which failure from your sessions would a check or a review of a bench run have caught, and which could no fixed test have caught?
Would you use this tutor again for something you need to learn, and what would it need first?

TODO: the bench against your sessions.

---

## 10. The judge check

Take ten decisions the judge made: for example ten tutor replies it marked met or not met, or ten fact verdicts from your lessons (the judge checks six facts in each lesson on the shared topic, so ten come from two lessons).
Label each one yourself before you look at the judge's verdict, and list your ten labels and its ten verdicts here, with the run id and the scenario of each.
How many of ten did you agree on?
Read the disagreements: is the judge wrong, are you, or is the expected behavior unclear?
What does that agreement mean for the judge numbers you reported above?

TODO: your ten labels, the agreement, and what it means.

---

## 11. A change that did not pay off

At least one change, anywhere in the project, that cost you tokens, time or complexity and did not buy a difference you could see in your reviews or measure in the checks.
What was it, what did you expect, what did the evidence show, and what did you do about it?
Name the round or the inventory entry where it shows.

TODO: the change that did not pay off.

---

## 12. The trade-offs

Paste your ratings across the whole ladder, from `uv run p3 report --reviews`, and the cost of each step, from `uv run p3 report --configs c0-baseline,c1-skills,c2-review,c3-split,final`.

TODO: paste the ratings and cost tables for the whole ladder.

Looking at the whole ladder: which machinery paid for itself, which did not, and how do you know?
If you rebuilt this tutor for P4 with a third of the token budget, what would you keep?
Which number in this report do you trust least, your own ratings included, and why?

TODO: your trade-offs.

---

## 13. The stretch

For 598E this is the rider, and its write-up goes here, with `PREREG.md` beside it.
Cover five things:

1. the option's name;
2. what you did, and the files that hold it;
3. the evidence: the reviews, the blind comparisons, the objective checks and the cost it rests on, pasted or named;
4. what that evidence lets you claim, and what it does not;
5. one thing you would do next, and what result would tell you it worked.

TODO: your stretch.
