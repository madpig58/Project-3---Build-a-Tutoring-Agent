# Reviews: c3-split

Your quick rounds while you split up the teach job, and then the major review of `c3-split`.
Add one subagent of the teach pipeline per round, so the run before it shows the lesson without it and the run after it shows the lesson with it.
The major review covers the lesson only, and its previous step is `c2-review`.
`reviews/README.md` says how to write each part.
You write your thoughts, ratings and feedback; Claude Code writes only the What changed part of each round.
Keep every heading as it is, because `p3 check` reads them, and add a round by copying the last one with its marker lines.

## Quick rounds

### Round 1

**Run:** bench/runs/_live/20261118-060051-agent-architecture-m30-r1

**My thoughts:**

The lesson achieved 1.00 factual correctness with no misconceptions or dead links. The length ratio was 0.94, which is close to the requested 30 minutes.

However, the teach job used 2.30M tokens and took 6.9 minutes. It already uses a lesson reviewer, but planning, drafting, and revision are still handled together by the main agent.

I want to separate lesson planning from writing. A dedicated planner could create the lesson structure, learning objectives, and time allocation before the main agent writes the content. I want to see whether this improves consistency and reduces unnecessary revisions.

**What changed:**

- Kind: new subagent
- Files: tutor/.claude/agents/lesson-planner.md, tutor/.claude/skills/teach/SKILL.md
- Why: Planning, drafting and revision were all done by the main agent, so a lesson-planner subagent now writes drafts/plan-NNNN.md before any drafting (the win, three to six learning objectives, the sections in order with minutes and word budgets adding up to 150 words a minute, each section's terms, worked example, practice and citations, and an out-of-scope list), and the teach skill starts it after choosing sources, waits for it, and writes the draft section by section from the plan.

### Round 2

**Run:** bench/runs/_live/20261118-223720-agent-architecture-m30-r1

**My thoughts:**

After adding the lesson-planner, the lesson still achieved 1.00 factual correctness with no misconceptions or dead links. The length ratio improved from 0.94 to 0.98, which is closer to the requested 30 minutes.

Token usage decreased from 2.30M to 2.01M, while the number of subagents increased from one to two. However, runtime increased from 6.9 to 7.7 minutes, and the list-price cost stayed almost the same ($1.53 versus $1.54).

I think separating lesson planning from drafting helped organize the lesson and may have improved length accuracy. However, this is only one run, so I cannot conclude that the planner consistently improves performance.

For the next round, I want to separate the creation of worked examples and practice activities into another subagent. This would let the main agent focus on writing the explanation while a dedicated subagent prepares examples that follow the lesson plan.

**What changed:**

- Kind: new subagent
- Files: tutor/.claude/agents/lesson-example-designer.md, tutor/.claude/skills/teach/SKILL.md
- Why: These thoughts ask to move the worked examples and practice out of the main agent, so a lesson-example-designer subagent now reads the lesson-planner's plan and writes drafts/examples-NNNN.md with, for each section, a step-by-step worked example, a practice activity with its answer, feedback for each tempting wrong answer, and the misconception it heads off, and the teach skill starts it after the planner, waits for it, and writes the explanations around its examples in the draft.

### Round 3

**Run:** bench/runs/_live/20261118-230521-agent-architecture-m30-r1

**My thoughts:**

After adding the lesson-example-designer, the lesson still achieved 1.00 factual correctness, with no misconceptions or dead links. However, the length ratio decreased from 0.98 to 0.94 compared with the planner-only run.

Token usage increased from 2.01M to 2.40M, runtime increased from 7.7 to 9.4 minutes, and the list-price equivalent increased from $1.54 to $1.82.

I expected the example designer to improve the lesson by separating worked examples and practice activities from the main agent's writing. However, the benchmark did not show an improvement in the measured quality scores. The additional subagent also increased output tokens significantly, possibly because the examples were written by both the designer and the main agent.

I think the example designer may still improve the quality of practice activities, but I would need to inspect the actual lessons to confirm that. Based only on this run, its additional cost is difficult to justify.

**What changed:**

- Kind: new subagent
- Files: tutor/.claude/agents/lesson-clarity-checker.md, tutor/.claude/skills/teach/SKILL.md
- Why: As asked for this round, a lesson-clarity-checker subagent (read-only, no web tools) now reads the draft as a beginner and reports only clarity problems (undefined terms, jargon beyond the plan's term limits, unclear explanations, gaps in the learning progression, hard-to-follow examples, and practice a beginner cannot yet attempt), marked major or minor with quoted fixes, and the teach skill runs it once after drafting, fixes its findings without cutting examples or practice, rechecks the length, and only then starts the lesson-reviewer.

### Round 4

**Run:** bench/runs/_live/20261118-233137-agent-architecture-m30-r1

**My thoughts:**

After adding the lesson-clarity-checker, the lesson maintained 1.00 factual correctness with no misconceptions or dead links. The length ratio changed from 0.94 to 1.05, so the lesson was slightly longer than requested but still close to the target.

However, the additional subagent significantly increased resource usage. Token usage rose from 2.40M to 3.84M, runtime increased from 9.4 to 11.2 minutes, and the list-price equivalent increased from $1.82 to $2.36.

I expected the clarity checker to make explanations easier for beginners, but the objective benchmark did not measure that improvement directly. The lesson was already factually correct before adding it, and length accuracy improved only slightly in absolute terms.

I think the clarity checker may be useful for readability, but I am concerned about its cost. I would want to inspect the review findings and the actual lesson before deciding whether it deserves a permanent place in the final configuration.

**What changed:**

- Kind: other
- Files: none (no change to the tutor in this round)
- Why: This round records the run with the lesson-clarity-checker (length ratio 0.94 to 1.05, tokens 2.40M to 3.84M, $1.82 to $2.36) and closes the quick rounds of c3-split with the pipeline as it stands; whether the checker stays is left to the major review.

## Major review

**Run:** bench/runs/c3-split/TODO

**Live tries:**

TODO

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

### Compared with the previous step

TODO

### What the next step should fix

TODO
