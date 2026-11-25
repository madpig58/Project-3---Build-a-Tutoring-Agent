# Reviews: final

Your review of `final`: optional quick rounds, its major review, your three learning sessions, and your review of the two test topics.
Quick rounds are optional here; use one for each component that `final` adds, such as a grader subagent, so its inventory entry has its with and without.
`p3 check` ignores an optional round you leave untouched.
The major review covers all four jobs on one of the three runs of `final`, and its previous step is `c3-split`; for the quiz and the feedback, which `c3-split` did not review, compare with `c2-review`, and for the tutor with `c1-skills`.
Its live tries are your three learning sessions, all on one of your two test topics, written up under Learning sessions below, so its Live tries line points at them.
Hold the sessions on `tutor/` as you snapshotted `final`, and note what they make you want to change instead of changing it.
`reviews/README.md` says how to write each part.
You write your thoughts, ratings and feedback; Claude Code writes only the What changed part of each round.
Keep every heading as it is, because `p3 check` reads them, and add a round by copying the last one with its marker lines.

## Quick rounds

### Round 1 (optional)

**Run:** bench/runs/_live/20261124-021045-agent-architecture-m30-r1

**My thoughts:**

The guard successfully blocked the main conversation from reading the answer key. However, the grading still achieved 1.00 verdict agreement because the grade-reviewer accessed the key and shared information through its reports.

I think the guard works for direct file access, but the answer key is not completely isolated from the main conversation. For the next round, I want to add a dedicated grader subagent and reduce unnecessary answer-key information in the reviewer's reports.

**What changed:**

- Kind: new subagent
- Files: tutor/.claude/agents/grader.md, tutor/.claude/skills/grade/SKILL.md
- Why: The guard kept the main conversation from the key but it still drafted the grades without it and learned the key's verdicts and misconception ids from the grade-reviewer's reports, so a grader subagent, which the guard already allows, now reads the key, decides every verdict, misconception id, feedback and summary, writes drafts/grade-NNNN-sN.json and reports only counts with nothing from the key, and the grade skill starts it, never reads keys/, sends the reviewer's verdict and fact findings back to the grader for revision instead of fixing them itself, and only writes the final grades, the records and the message to the learner.

### Round 2 (optional)

**Run:** bench/runs/_live/20261124-024911-agent-architecture-m30-r1

**My thoughts:**

Adding the grader subagent kept the verdict agreement at 1.00 while preventing the main conversation from directly accessing the answer key. Token usage increased from 409.3k to 484.8k, but the estimated cost decreased from $0.42 to $0.39.

I think separating grading into its own subagent was a good improvement because it made the system more organized without reducing accuracy. However, some answer-key information could still reach the main conversation through the subagent reports. I want the next round to reduce unnecessary information in those reports while keeping the grading results accurate.

**What changed:**

- Kind: other
- Files: tutor/.claude/agents/grade-reviewer.md
- Why: Some answer-key information still reached the main conversation through the reviewer's report, such as a sentence about what the key's rationale covers, so the reviewer now quotes only the draft and the submission, points at the key by item id alone, and gives fixes such as "re-grade q3 against the key" for the grader to carry out, never the key's answers, option letters or rationale.

### Round 3 (optional)

**Run:** bench/runs/_live/20261124-040845-agent-architecture-m30-r1

**My thoughts:**

The reviewer no longer included unnecessary answer-key information in its reports, while verdict agreement remained at 1.00. Token usage increased slightly from 484.8k to 505.6k, but the estimated cost stayed at $0.39.

I think this was a useful improvement because the main conversation received less sensitive information without losing grading accuracy. However, the reviewer returned CLEAN, so I still do not know whether the revised reporting format works correctly when it finds a major grading error.

For the next round, I want to test the REVISE process and make sure the grader can correct mistakes without exposing the answer key.

**What changed:**

- Kind: other
- Files: tutor/.claude/agents/grader.md
- Why: The REVISE test showed the grader adding commentary to its report, such as which distractor an item's misconception fits, so its report is now exactly five lines holding only counts, the draft's path, item ids, finding numbers or "none", and a finding it does not apply is listed by number with no reason, all grading reasoning staying in the draft.

### Round 4 (optional)

**Run:** bench/runs/_live/20261124-042049-agent-architecture-m30-r1

**My thoughts:**

The grader successfully corrected both planted errors, and the final grades matched all six expected results. Its second-pass report also followed the required five-line format without extra commentary.

However, the grade-reviewer added an unnecessary paragraph outside its required report format during pass 2. I think the grading process is working correctly, but the reporting format still needs improvement.

For the next round, I want the grade-reviewer to follow a strict report format without adding extra explanations or repeating the final verdicts.

**What changed:**

- Kind: other
- Files: tutor/.claude/agents/grade-reviewer.md
- Why: On pass 2 of the REVISE fixture the grade-reviewer added a paragraph outside its report format, listing every verdict and misconception id it agreed with, so its report must now hold nothing before the PASS line or after the Verdict line, the numbered findings are its only free text, and agreement is left to "Checks with no finding".

### Round 5 (optional)

**Run:** bench/runs/_live/20261124-043342-agent-architecture-m30-r1

**My thoughts:**

The REVISE test successfully corrected both planted grading errors, and all six final grades matched the expected results. The reviewer also followed its report structure without adding an extra paragraph, although the reports were still wrapped in Markdown code fences.

I think the grading workflow is reliable enough to move forward. However, the teach skill still contains outdated instructions telling the main conversation to read answer keys, which conflicts with the new guard.

For the next improvement, I want to update the teach skill so grading requests follow the dedicated grader workflow instead.

**What changed:**

- Kind: modified skill
- Files: tutor/.claude/skills/teach/SKILL.md
- Why: The teach skill's grade section still told the main conversation to read the key and grade, which the guard now blocks, so it now never opens keys/ or decides a verdict, and hands a grade request to the grade skill's workflow by reading .claude/skills/grade/S  KILL.md and following it, so the grader and grade-reviewer do the grading.


### Round 6 (optional)

**Run:** Scratchpad `/teach` grading integration test on `a-star-pathfinding`, quiz 0001, submission s1 (`scratchpad/teach-grade-test`). Not an official benchmark run.

**My thoughts:**

The /teach grading test successfully delegated grading to the grader and grade-reviewer subagents. The main conversation did not attempt to read the answer key, and all six final grades matched the expected results.

I think this improvement makes the tutoring system more consistent because both /teach and /grade now use the same grading workflow.

However, the test also revealed that the quiz skill still contains instructions to read previous answer keys, which conflicts with the new guard. I want to fix this while preserving the quiz's ability to reuse existing misconception IDs.

**What changed:**

- Kind: other
- Files: tutor/.claude/hooks/keys_guard.py, tests/test_guard.py
- Why: The quiz skill reads earlier keys for their misconception ids, which the guard blocks, and in a fresh workspace those ids live only in keys/, so the guard now also lets the quiz-reviewer subagent read keys/, the first of two steps toward having the reviewer check the draft key's ids against the earlier keys while the main conversation stays blocked; the reviewer's check and the quiz skill's change are left for the next round.

### Round 7 (optional)

**Run:** bench/runs/_live/20261124-045902-agent-architecture-m30-r1

**My thoughts:**

The quiz baseline timed out after 15 minutes, although it completed its output files and received a key agreement score of 0.83. The main conversation attempted to read the previous answer key, but the guard blocked it. The quiz-reviewer did not use its newly granted permission, and no existing misconception IDs were reused.

I think the guard is working as intended, but the quiz workflow is not yet compatible with it. I want the quiz-reviewer to check existing misconception IDs against earlier keys and report conflicts without exposing answer-key contents to the main conversation.

I also want the quiz skill to stop reading keys directly. The next change should preserve quiz quality while reducing unnecessary processing time.

**What changed:**

- Kind: modified skill
- Files: tutor/.claude/skills/quiz/SKILL.md, tutor/.claude/agents/quiz-reviewer.md
- Why: The quiz skill's read of the earlier keys was blocked and no misconception id was reused, so the skill now never opens keys/ except to write the new key once, and the quiz-reviewer reads the earlier keys and returns only an id or none for each wrong mcq option of the draft, which the skill copies into the key without another review pass.

### Round 8 (optional)

**Run:** bench/runs/_live/20261124-052024-agent-architecture-m30-r1

**My thoughts:**

The quiz benchmark completed successfully in 2.5 minutes, compared with the previous run that timed out after 15 minutes. Key agreement improved from 0.83 to 1.00, and token usage decreased from 714.1k to 612.2k.

The quiz-reviewer successfully accessed earlier answer keys and reused misconception IDs without requiring the main conversation to read keys/ directly.

However, some misconception IDs were assigned to distractors that did not seem to represent the same misunderstanding. I also noticed that the draft answer key remained readable outside the protected keys/ directory.

I think protecting answer-key information is more important for the next improvement because the current draft location weakens the guard's security boundary. After that, I want to improve misconception ID matching accuracy.

**What changed:**

- Kind: other
- Files: tutor/.claude/hooks/keys_guard.py, tests/test_guard.py
- Why: The draft key in drafts/ held the same answers as the final key and stayed readable, so the guard now blocks Read, Grep and shell reads of draft keys for every agent but the allowed ones, as it does for keys/, while the quiz skill can still write and edit its draft and the quiz-reviewer can still read it; probing it also showed three older gaps into keys/, which it now closes: Windows path forms such as keys./0001.json, brace lists in shell commands, and several or partly excluding globs in one Grep.

### Round 9 (optional)

**Run:** bench/runs/_live/20261124-053212-agent-architecture-m30-r1

**My thoughts:**

The updated guard successfully blocked direct reads of draft answer keys while keeping the quiz benchmark's key agreement at 1.00. All 25 guard tests passed, although one additional security probe still found a way around the protection.

However, the benchmark revealed that review records can contain correct answer choices, making them another source of answer-key exposure. I also noticed that the second review pass started before the quiz revisions were saved, so some final quiz items were not reviewed.

I think preventing answer exposure through review records is the higher priority because it affects future tutoring sessions. I want to address that issue next while preserving useful review feedback.

**What changed:**

- Kind: modified skill
- Files: tutor/.claude/skills/quiz/SKILL.md
- Why: The quiz review record copied the reviewer's findings and the fixes, which named correct options in a file later tutoring sessions can read, so the skill now writes the record in a fixed shape that gives each finding's item, check, place, kind of problem and kind of change from set lists, with no option letters, answers, quotes or rationales.

### Round 10 (optional)

**Run:** bench/runs/_live/20261124-053950-agent-architecture-m30-r1

**My thoughts:**

The new review-record format successfully prevented answer-key information from appearing in the quiz review record while preserving the review findings.

However, the quiz benchmark's key agreement dropped from 1.00 to 0.83, and two items were flagged as potentially ambiguous. The final message also gave hints about the correct answers before the learner could take the quiz.

I think preventing answer hints in the final message is the most important next improvement because it directly affects the learner's experience and the fairness of the quiz.

I also want to address the issue of quiz items being modified after the final review, but I would prefer to handle that separately so I can evaluate each change.

**What changed:**

- Kind: modified skill
- Files: tutor/.claude/skills/quiz/SKILL.md
- Why: The quiz skill's closing message summarized the questions and the review fixes and so hinted at the correct approaches before the learner took the quiz, so it now ends with a fixed message that says only that the quiz is ready, where it is and how to hand in answers.

### Round 11 (optional)

**Run:** bench/runs/_live/20261124-054742-agent-architecture-m30-r1

**My thoughts:**

The quiz skill's final message no longer revealed any answers or hints, and the benchmark maintained a key agreement of 1.00 with no likely ambiguous items.

However, token usage increased from 675.8k to 792.3k. The reviewer also returned REVISE on both passes, and q2 was modified after the final review without being checked again.

I think the next improvement should focus on preventing unreviewed changes to the final quiz. Even if the reviewer checks the original draft carefully, modifying questions afterward can introduce new mistakes or ambiguities.

I want the final quiz to reflect the reviewer's feedback without allowing significant unverified changes after the last review.

**What changed:**

- Kind: modified skill
- Files: tutor/.claude/skills/quiz/SKILL.md
- Why: The quiz skill told the tutor to fix pass 2's findings without another review, so q2 reached the learner unchecked; the drafts are now frozen at the last pass (only misconception ids may be set and an unscorable item dropped), and findings left open are listed in the review record.

### Round 12 (optional)

**Run:** bench/runs/_live/20261124-110214-agent-architecture-m30-r1

**My thoughts:**

The latest quiz run achieved a key agreement of 1.00, with no likely ambiguous items or incorrect answer keys. The final quiz was also identical to the version reviewed in pass 2, so the new freeze rule worked as intended.

However, q4 still contained a wording giveaway that made the correct answer easier to identify. I decided to accept this limitation rather than introduce an unreviewed change after the final review.

For my next improvement, I want to add a new practice skill that helps learners work on specific weaknesses identified in their learning records. The existing skills can teach concepts, answer questions, generate quizzes and grade submissions, but they do not provide a dedicated adaptive practice workflow.

I want the practice skill to offer targeted exercises and feedback based on the learner's current understanding, without revealing quiz answers.

**What changed:**

- Kind: new skill
- Files: tutor/.claude/skills/practice/SKILL.md, tutor/.claude/skills/tutor/SKILL.md
- Why: The tutor had no dedicated adaptive practice workflow, so the new practice skill gives one targeted exercise at a time from the weak spots in NOTES.md and the learning records, judges the reasoning as well as the answer and keeps away from open quiz items, and the tutor skill now starts it when the learner asks or agrees.

### Round 13 (optional)

**Run:** bench/runs/_live/20261125-044705-agent-architecture-m30-r1

**My thoughts:**

The practice skill was added successfully, but the focused tutor benchmark revealed a regression. Probe p01 met the expected behavior without leaking a quiz answer, while p06 failed because the tutor refused to explain a general concept related to an open quiz.

I think the tutor is being too restrictive. Protecting open quiz answers is important, but learners should still be able to receive general explanations using independent examples.

For the next improvement, I want the tutor to distinguish between requests that would reveal a specific quiz answer and requests for general conceptual understanding. It should explain general concepts without referring to the open quiz's scenario, options, or correct answers.

Practice should still require the learner's request or consent.

**What changed:**

- Kind: modified skill
- Files: tutor/.claude/skills/tutor/SKILL.md
- Why: The tutor refused a general explanation because an open quiz covered the same idea, so it now sorts a message by what it asks rather than its topic, keeps any request about a specific open item protected, and explains general ideas at once with an independent example that stays away from the item's question, case, options and answer.

### Round 14 (optional)

**Run:** bench/runs/_live/20261125-045339-agent-architecture-m30-r1

**My thoughts:**

The tutor now provides general explanations even when an open quiz covers the same topic, which fixes the refusal observed in the previous p06 run.

However, the latest benchmark met only one of three expected behaviors. In p06, the explanation was too long and did not clearly connect the analogy to the actual concept. More importantly, the tutor introduced an unnecessary detail about stopping a process, which could hint at an answer to an open quiz item.

I think the tutor should explain what the learner actually asked without adding unrelated details that could reveal quiz answers. I want to preserve useful general explanations while limiting unnecessary information.

For the next improvement, I want the tutor to stay focused on the learner's question, use concise explanations, and explicitly connect analogies to the concepts they represent without referring to any open quiz item.

**What changed:**

- Kind: modified skill
- Files: tutor/.claude/skills/tutor/SKILL.md
- Why: A general explanation ran long, left its analogy unmapped and added a detail the learner had not asked about that could hint at an open quiz item, so the tutor skill now keeps to the question asked, holds replies to about 200 words, maps an analogy back itself and cuts any part that points toward an open item and is not needed for the answer.

### Round 15 (optional)

**Run:** bench/runs/_live/20261125-053052-agent-architecture-m30-r1

**My thoughts:**

The latest tutor benchmark passed two of the three probes, but the explanations still had some weaknesses. In p06, the tutor provided a useful general explanation, but the response exceeded the 250-word limit and included details that were close to open quiz items.

I think the tutor has difficulty checking its own explanations consistently. The previous attempts to improve the instructions helped, but they did not fully solve the length and answer-hint problems.

For the next improvement, I want to add an explanation-checker subagent that reviews the tutor's draft before it is sent to the learner.

The checker should verify that the explanation answers the learner's question, stays within the word limit, clearly connects analogies to the real concepts, and avoids unnecessary hints about open quiz items.

I also want to measure whether the improvement is worth the additional token usage and cost.

**What changed:**

- Kind: new subagent
- Files: tutor/.claude/agents/explanation-checker.md, tutor/.claude/skills/tutor/SKILL.md
- Why: The tutor did not keep to its own length and answer-hint rules when it checked its own explanation, so the new explanation-checker subagent checks the draft once, with a fresh context, whenever a quiz is open, and the tutor fixes what it finds before replying.

### Round 16 (optional)

**Run:** bench/runs/_live/20261125-054338-agent-architecture-m30-r1

**My thoughts:**

The explanation-checker was invoked correctly, but its benefits were limited. The p06 explanation was shorter and avoided the unnecessary stopping hint, yet the judge marked it as not meeting expected behavior because the explanation omitted an important concept about tool descriptions.

The checker also caused a significant increase in token usage. Across p02 and p06, tokens increased by approximately 70% compared with the previous run.

I think the checker needs to prioritize the completeness of the explanation while still avoiding unnecessary quiz hints. Its feedback should not cause the tutor to remove essential information or replace a meaningful understanding question with a generic closing question.

I want to make one focused improvement and evaluate whether the additional cost is justified. If the checker still does not provide a clear benefit, I would prefer to remove it from the final configuration.

**What changed:**

- Kind: other
- Files: tutor/.claude/agents/explanation-checker.md, tutor/.claude/skills/tutor/SKILL.md
- Why: The checker missed an essential concept the draft left out and had the tutor swap a real closing question for a generic one, so it now lists what the idea needs before it reads the quiz, reports a missing part as major, cuts only what is not on that list and always gives another applying question, and the tutor's fix step lets a missing part be added.

### Round 17 (optional)

**Run:** bench/runs/_live/20261125-055002-agent-architecture-m30-r1

**My thoughts:**

The revised explanation-checker passed both focused probes, including p06. The explanation also recovered an important concept that was missing in the previous run, so the modification improved the result.

However, I am still concerned about its effectiveness and cost. In p06, the checker caused the tutor to add wording about a service name and its arguments that closely resembled an open quiz item's answer. This is especially concerning because protecting open quiz answers was one of the checker's main purposes.

The checker also increased token usage and runtime compared with the tutor without it. The tutor had already passed p06 without the checker in Round 14, so these results do not demonstrate a clear benefit from the additional subagent.

I want to remove explanation-checker from the final tutor while preserving the experimental snapshot for comparison. I would rather keep the final tutor simpler and more efficient than retain a component whose additional cost and potential quiz-hint risks are not clearly justified.

**What changed:**

- Kind: other
- Files: tutor/.claude/agents/explanation-checker.md (removed), tutor/.claude/skills/tutor/SKILL.md
- Why: The checker's benefit did not clearly justify its added tokens and runtime, and one of its fixes added wording close to an open quiz item's answer, so the subagent and the section of the tutor skill that started it are removed, and the tutor's own explanation rules stay as Round 14 left them.

### Round 18 (optional)

**Run:** bench/runs/_live/20261125-053052-agent-architecture-m30-r1

**My thoughts:**

The current tutor can explain concepts, provide practice exercises, create quizzes, and grade submissions, but it does not have a dedicated way to organize learning across multiple sessions.

The learning notes contain unresolved misconceptions and unanswered check questions, but there is no clear process for deciding what the learner should review first or when to revisit earlier topics.

For the next improvement, I want to add a study-plan skill that uses the learner's goals, available time, NOTES.md, and existing learning records to recommend a short sequence of study sessions.

Each session should have a specific goal, a reason based on the learner's records, an estimated duration, a suggested skill, and a way to check understanding.

The skill should not generate lessons or exercises itself, assume that a learner has mastered something, or reveal information from open quizzes. It should ask for missing essential information and save the plan only after the learner agrees.

I think this would make the tutor more useful for long-term learning while keeping the responsibilities of the existing skills separate.

**What changed:**

- Kind: new skill
- Files: tutor/.claude/skills/study-plan/SKILL.md, tutor/.claude/skills/tutor/SKILL.md
- Why: The tutor had no way to organize learning across sessions, so the new study-plan skill proposes three to five sessions from the learner's goal, time, notes and records, asks for what is missing and saves the plan only after the learner agrees, and the tutor skill now starts it when the learner asks or agrees.

### Round 19 (optional)

**Run:** bench/runs/_live/20261125-072753-agent-architecture-m30-r1

**My thoughts:**

The focused regression benchmark passed both tutor probes with no detected answer leaks. The new study-plan skill was not invoked during unrelated tutor requests.

I also tested study-plan manually in a separate environment. It successfully created personalized study plans using existing learner notes, organized three to five sessions within the available time, and required explicit approval before saving or replacing a plan.

The skill correctly handled missing information, revised an existing plan from 180 to 90 minutes, and declined to reveal the topics of an open quiz. In the routing test, /tutor provided a normal explanation and then invoked study-plan when I explicitly requested a study plan.

One issue remains: when I requested a new study plan, the skill proposed a longer plan based on MISSION.md rather than preserving the 90-minute limit in the existing saved plan. It requested approval before replacing the plan, so the original file was not automatically overwritten.

Overall, I think study-plan adds useful long-term learning support without duplicating the existing teaching or practice skills. I want to keep it in the final tutor.

**What changed:**

- Kind: modified skill
- Files: tutor/.claude/skills/study-plan/SKILL.md
- Why: A new study plan went over the saved plan's 90 minutes because the skill had no rule for when the saved plan and MISSION.md disagree about time, so the saved plan's time now comes first unless the learner explicitly asks for a different amount.


## Major review

**Run:** bench/runs/final/TODO

**Live tries:**

TODO: one line that points at your three learning sessions under Learning sessions below, and names anything else you tried with `final`.

### Lesson

#### Technical correctness and facts

Rating: TODO

TODO

#### Pedagogy

Rating: TODO

TODO

#### Alignment with the learning goal

Rating: TODO

TODO

#### Overall quality

Rating: TODO

TODO

### Quiz

#### Difficulty

Rating: TODO

TODO

#### Coverage of the lesson's core

Rating: TODO

TODO

#### Wording and possible misreadings

Rating: TODO

TODO

#### Writing quality

Rating: TODO

TODO

#### Alignment with the learning goal

Rating: TODO

TODO

### Feedback

#### Useful

Rating: TODO

TODO

#### Explains enough

Rating: TODO

TODO

#### Personalized to how I like things explained

Rating: TODO

TODO

### Tutor

#### Guardrails

Rating: TODO

TODO

#### Personalization

Rating: TODO

TODO

### Compared with the previous step

TODO

### What I would do next

TODO

## Learning sessions

### Session 1

**Date:** TODO

**Topic:** TODO

TODO

### Session 2

**Date:** TODO

**Topic:** TODO

TODO

### Session 3

**Date:** TODO

**Topic:** TODO

TODO

## Test topics

### TODO: your first test topic's id

TODO

### TODO: your second test topic's id

TODO
