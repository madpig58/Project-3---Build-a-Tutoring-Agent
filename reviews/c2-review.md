# Reviews: c2-review

Your quick rounds while you build the review loops on teach, quiz and grade, and then the major review of `c2-review`.
Add one reviewer subagent per round, so the run before it shows the output without it and the run after it shows the output with it.
The major review covers the lesson, the quiz and the feedback, and its previous step is `c1-skills`.
Say in it whether the problems your `c1-skills` review found are gone.
`reviews/README.md` says how to write each part.
You write your thoughts, ratings and feedback; Claude Code writes only the What changed part of each round.
Keep every heading as it is, because `p3 check` reads them, and add a round by copying the last one with its marker lines.

## Quick rounds

### Round 1

**Run:** bench/runs/_live/20261117-211255-agent-architecture-m30-r1

**My thoughts:**

The quiz performance was worse than in the previous full run. The answer-key agreement dropped from 1.00 to 0.80, and the evaluator detected two potentially ambiguous questions.

I want to add a separate quiz reviewer subagent that checks each question before the final quiz is saved. It should look for unclear wording, missing conditions, multiple defensible answers, and disagreements between the questions and answer key.

The reviewer should work with a fresh context so it can evaluate the questions independently. If it identifies a problem, the quiz skill should revise the affected question and check it again.

I would like to limit the review loop to two passes to avoid unnecessary token usage and execution time.

**What changed:**

- Kind: new subagent
- Files: tutor/.claude/agents/quiz-reviewer.md, tutor/.claude/skills/quiz/SKILL.md
- Why: Key agreement fell to 0.80 with q1 and q2 flagged as ambiguous, so a quiz-reviewer subagent with a fresh context now answers each draft item from its stem alone, then checks it against the key and a 12-point checklist (one defensible answer, missing conditions, one quantity asked, key agrees with stem, scorable short answers, coverage and difficulty), and the quiz skill drafts in drafts/, revises at most two passes, then writes quizzes/ and keys/ once plus review-records/NNNN-quiz.md.

### Round 2

**Run:** bench/runs/_live/20261117-213147-agent-architecture-m30-r1

**My thoughts:**
The quiz reviewer ran two passes and found several meaningful problems. In Pass 1, it identified answer leakage between questions, unclear short-answer grading, and weak distractors. In Pass 2, it also found answer-length clues, repeated wording, and a question that relied too much on recall.

I think the reviewer was useful because it identified problems that the quiz skill did not catch on its own. The final quiz achieved a key agreement score of 1.00 with zero ambiguous items.

However, the quiz cost increased from $0.23 to $0.56, and the final review verdict was still REVISE. All findings from Pass 2 were addressed, but the revised questions were not checked again.

For the next change, I want to add a grade reviewer that checks whether grading feedback is accurate, specific, and useful. I also want review loops to avoid unnecessary passes when no meaningful problems are found.

**What changed:**

- Kind: new subagent
- Files: tutor/.claude/agents/grade-reviewer.md, tutor/.claude/skills/grade/SKILL.md
- Why: A grade-reviewer subagent with a fresh context now regrades each item itself before reading the draft, then checks verdicts, misconception ids and the truth of the feedback (major), what-why-how completeness, and length, filler and fit to PREFERENCES.md (minor), and the grade skill drafts in drafts/ and runs a second pass only when pass 1 has a major finding, at most two passes, then writes grades/ once plus review-records/NNNN-sN-grade.md.

### Round 3

**Run:** bench/runs/_live/20261117-214101-agent-architecture-m30-r1

**My thoughts:**
The grade reviewer ran one pass and found no major problems, but it identified four minor issues. It removed unnecessary sentences, shortened q4's feedback, reduced repeated explanations of misconception M4, and simplified the summary to one main learning goal and one next step.

I think these changes made the feedback more focused without affecting grading accuracy. The verdict agreement and misconception hit rate both remained at 1.00.

The early stopping rule worked as intended because the reviewer returned CLEAN after the first pass. However, the grading cost increased from $0.16 to $0.28, so I am not sure whether the additional cost is worthwhile for every submission.

For the next change, I want to add a teach reviewer that checks technical correctness, lesson structure, learning-objective coverage, and unnecessary complexity. I would prefer a limited review loop that focuses on major problems to control the cost.

**What changed:**

- Kind: new subagent
- Files: tutor/.claude/agents/lesson-reviewer.md, tutor/.claude/skills/teach/SKILL.md
- Why: A lesson-reviewer subagent with a fresh context now reviews the draft lesson in four separate sections (facts checked against sources with WebSearch and WebFetch, pedagogy and structure, coverage of the objective, and unnecessary complexity such as the c1 full run's five new techniques in one section), marks only listed kinds of problem as major, and the teach skill drafts in drafts/, runs a second pass only on a major finding, at most two, then writes lessons/ once plus review-records/NNNN-lesson.md.

### Round 4

**Run:** bench/runs/_live/20261117-215059-agent-architecture-m30-r1

**My thoughts:**
The lesson reviewer ran two passes. The first pass returned REVISE because the lesson introduced too many technical terms in one section, including embeddings and different retrieval techniques. The reviewer also found inconsistent examples, unnecessary explanations, and a link that needed updating.

After the revisions, the second pass returned CLEAN. The reviewer found two additional minor issues, which were also corrected. I think the lesson became easier for a beginner to follow because it focused on the essential concepts instead of introducing too many new ideas at once.

The final lesson maintained a factual correctness score of 1.00, with no misconceptions or dead links. However, the length ratio decreased slightly from 0.93 to 0.90.

The main drawback was the cost. The lesson cost increased from $0.60 to $1.46, and the runtime increased from 3.1 to 6.9 minutes. I think the reviewer improved the lesson's clarity, but I would like to reduce its cost in future versions.

**What changed:**

- Kind: other
- Files: tutor/.claude/agents/lesson-reviewer.md, tutor/.claude/skills/teach/SKILL.md
- Why: The teach cost rose from $0.60 to $1.46 partly because pass 2 repeated the whole review and the fact-check (the same source pages were fetched up to three times), so the lesson-reviewer now caps pass 1 at three fetches and makes pass 2 a narrow re-check of only the changed parts and the pass-1 major findings, with no fetching and no new minor findings, and the teach skill's pass-2 task message lists those changes with their headings and quotes.

### Round 5

**Run:** bench/runs/_live/20261117-221148-agent-architecture-m30-r1

**My thoughts:**
The optimized lesson reviewer completed two passes and returned CLEAN. It identified two major issues and four minor issues. One important correction was removing a misleading statistic that had been attributed to the wrong retrieval method. It also simplified an overly technical section and improved the explanations for practice questions.

The second pass performed a narrow re-check and found no additional problems. This suggests that the revised review process can still catch meaningful issues.

However, the cost decreased only slightly from $1.46 to $1.39, while total token usage increased from 1.87M to 2.21M. The lesson length ratio also decreased from 0.90 to 0.82, below the intended minimum.

I think the reviewer improved technical accuracy and reduced unnecessary complexity, but the final lesson became too short. For the next change, I want the teach skill to check the final lesson length after all revisions and add relevant worked examples or practice if necessary, without reintroducing unnecessary technical details.

I would keep the narrow second review pass for now, but I do not consider the cost optimization fully successful based on one run.

**What changed:**

- Kind: modified skill
- Files: tutor/.claude/skills/teach/SKILL.md, tutor/.claude/skills/teach/references/LESSONS.md
- Why: The draft was already short before the review (3,775 visible words in drafts/, 3,770 in the final lesson), because the sentences-times-15 estimate runs high, so the teach skill now aims for an estimate of at least 100% of the requested minutes and checks the length once more after all revisions, before writing the final lesson, filling any gap only with worked examples or faded practice on ideas already taught, with no new terms or techniques.

### Round 6

**Run:** bench/runs/_live/20261117-223438-agent-architecture-m30-r1

**My thoughts:**
The final length check improved the lesson length ratio from 0.82 to 0.99, while factual correctness remained at 1.00 with no misconceptions or dead links.

The runtime decreased slightly from 6.7 to 6.5 minutes, and the list-price equivalent cost decreased from $1.39 to $1.36. The total token usage also decreased from 2.21M to 2.06M.

I think this was a useful improvement because it addressed the short lesson problem without increasing the measured cost. The lesson now comes much closer to the requested 30-minute length.

However, the result is based on one run, so I cannot be certain that the improvement will be consistent across other topics or lesson lengths.

I would keep the final length check and the narrower second review pass. At this point, I want to evaluate the complete review system rather than add more changes.

**What changed:**

- Kind: other
- Files: none (no change to the tutor in this round)
- Why: The final length check raised the length ratio from 0.82 to 0.99 at no extra measured cost, and these thoughts ask to keep the current implementation, including the narrow second review pass, and to evaluate the complete review system as it stands.


## Major review

**Run:** bench/runs/c2-review/20261117-230059-agent-architecture-m30-r1

**Live tries:**

I tested the tutor with two questions.

First, I asked it to explain the difference between an LLM and an AI agent using a game NPC example. It used a blacksmith NPC crafting an iron sword and explained the agent loop step by step. I liked that it used a game-related example and remembered my previous misconception about tool execution. It also asked a follow-up question to check my understanding.

Second, I asked for the answer to question 2 of quiz 0001 because I wanted to finish quickly. The tutor refused to give me the answer and offered to help me work through my reasoning instead. It also correctly noticed that quiz 0001 did not exist in the workspace.

Overall, I think the tutor followed my preferences and respected the quiz guardrails. However, since there was no actual quiz file, I could not fully test how it would handle hints for a real quiz question.

### Lesson

#### Technical correctness and facts

Rating: 5/5

The lesson achieved a factual correctness score of 1.00, with no misconceptions or dead links. During the quick rounds, the lesson reviewer also caught a misleading statistic about retrieval methods. I think the reviewer is useful because it can find technical errors that the original lesson writer might miss.

#### Pedagogy

Rating: 5/5

I liked how the reviewer focused on simplifying complicated explanations for beginners. It identified sections with too many technical terms and removed unnecessary details while keeping the main concepts. The worked examples and explanations also help students understand how the concepts work in practice.

#### Alignment with the learning goal

Rating: 5/5

The lesson stayed focused on the learning objective. Its length ratio was 0.92, which was close to the requested 30-minute duration. The final length check helped prevent lessons from becoming too short after revisions.

#### Overall quality

Rating: 4/5

The lesson was technically correct and well structured. I think the reviewer improved its clarity, especially by reducing unnecessary complexity. However, teaching became much more expensive, increasing from $0.60 to $1.32 per run. The additional review process was useful, but its cost was a disadvantage.

### Quiz

#### Difficulty

Rating: 4/5

The quiz tested understanding of agent architecture rather than only memorization. I think the difficulty was reasonable, but I did not see enough evidence that the reviewer significantly improved it compared with c1-skills.

#### Coverage of the lesson's core

Rating: 4/5

The quiz covered the main concepts of the learning objective. The reviewer also checked for overlapping questions and repeated ideas. However, the benchmark did not show a measurable improvement in coverage compared with the previous step.

#### Wording and possible misreadings

Rating: 5/5

The quiz achieved a key agreement score of 1.00 with zero ambiguous items. During the quick rounds, the reviewer identified unclear wording, answer choices that could be defended in multiple ways, and questions that revealed other answers. I think this was one of the reviewer's most useful contributions.

#### Writing quality

Rating: 5/5

The reviewer improved quiz writing by replacing weak distractors, removing answer clues, and making questions easier to interpret and grade. I think these changes made the questions clearer and more consistent.

#### Alignment with the learning goal

Rating: 4/5

The quiz stayed aligned with the objective and tested practical understanding. However, the results did not show a clear improvement over c1-skills, so I would keep the same rating.

### Feedback

#### Useful

Rating: 5/5

The grading system maintained a verdict agreement score of 1.00 and a misconception hit rate of 1.00. The grade reviewer removed unnecessary explanations and helped make the feedback more focused on the student's actual mistakes.

#### Explains enough

Rating: 5/5

I think the feedback provided enough explanation without repeating the same points too many times. During the quick rounds, the reviewer shortened overly long feedback and kept the important reasoning and next steps. This made the feedback easier to follow.

#### Personalized to how I like things explained

Rating: 5/5

The feedback followed my preference for direct and practical explanations. The reviewer also simplified the summary to one main learning goal and one clear next step, which I find more useful than receiving several suggestions at once.

### Compared with the previous step

The c2-review configuration completed all ten benchmark scenarios successfully. Compared with c1-skills, the objective quality scores remained almost identical. Both configurations achieved 1.00 factual correctness, quiz key agreement, grading agreement, and misconception detection. Tutor expected behavior also remained at 0.67.

The main improvement was the additional review process. The quiz reviewer found ambiguous questions and weak distractors, the grade reviewer reduced repetitive feedback, and the lesson reviewer identified technical errors and unnecessary complexity.

However, these improvements came with a significant cost. The total execution time increased from 7.2 to 14.2 minutes, and the list-price equivalent cost increased from $1.72 to $3.11. Quiz generation showed a particularly large increase, from $0.22 to $0.65.

I think the reviewers provide useful quality control, but the full benchmark does not show an improvement in the measured quality scores. Since both configurations hav

### What the next step should fix

The main problem I want to address next is the cost and complexity of the review process. The reviewers found useful issues, but they also increased the execution time and token usage significantly.

I would like to keep the independent reviewers while reducing unnecessary repeated work. I also want the next step to make the teaching workflow more efficient and reliable without losing the improvements in technical accuracy, quiz clarity, and feedback quality.

Another goal is to maintain the lesson length and make sure the tutor continues to guide students without revealing answers. The next version should preserve the quality improvements while avoiding unnecessary overhead.
