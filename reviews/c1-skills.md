# Reviews: c1-skills

Your quick rounds while you build `c1-skills`, and then its major review, once you have snapshotted it and made its full run.
In this step no round adds a subagent, because subagents arrive in `c2-review` and `c3-split`: a round changes or adds a skill, or makes another change the skills need, such as an allow rule (Kind `other`).
Your first round can start from the tutor as it ships, so the baseline is the output without your first change.
The major review covers all four jobs, and its previous step is `c0-baseline`, so compare with your baseline runs.
What it finds becomes the checklists of your reviewer subagents in `c2-review`, so be specific.
`reviews/README.md` says how to write each part.
You write your thoughts, ratings and feedback; Claude Code writes only the What changed part of each round.
Keep every heading as it is, because `p3 check` reads them, and add a round by copying the last one with its marker lines.

## Quick rounds

### Round 1

**Run:** bench/runs/_live/20261117-042200-agent-architecture-m30-r1

**My thoughts:**

The tutor completed all five scenarios successfully. The lesson was factually correct according to the benchmark, but the length ratio was only 0.59 for a requested 30-minute lesson. I want the lesson to provide more detailed explanations and worked examples so that it better matches the requested duration.

The quiz and grading results were strong, with full agreement on the answer keys and grading decisions. The tutor also avoided leaking quiz answers, but its expected behavior score was only 0.50. I want it to provide more useful hints and step-by-step guidance without giving away the answers.

For the first improvement, I want to focus on the teach skill, especially lesson length and examples.

**What changed:**

- Kind: modified skill
- Files: tutor/.claude/skills/teach/SKILL.md, tutor/.claude/skills/teach/references/LESSONS.md
- Why: The 30-minute lesson came in at 2,666 words (length ratio 0.59) with a worked example only at the end, so teach now aims at the full 150-words-a-minute budget, puts a step-by-step worked example in every section, and checks the length after writing, adding examples and practice until it reaches 90% of the requested time.

### Round 2

**Run:** bench/runs/_live/20261117-044007-agent-architecture-m30-r1

**My thoughts:**

The lesson length improved from 0.59 to 0.92, which is much closer to the requested 30 minutes. The factual accuracy stayed at 1.00, with no detected misconceptions.

The cost increased from $0.56 to $0.67, but I think the improvement in lesson length could justify the additional cost.

For the next change, I want to improve the tutor skill. The previous test showed an expected-behavior score of 0.50, so I want the tutor to give better hints and step-by-step guidance without revealing quiz answers.

**What changed:**

- Kind: new skill
- Files: tutor/.claude/skills/tutor/SKILL.md
- Why: tutor-p01 failed its expected behavior because the hint singled out options and pointed at the tested idea, so a new tutor skill gives option-neutral, step-by-step reasoning help on open quiz items (with a neutrality test on every sentence and no reading of `keys/`) and numbered, example-first explanations for other questions.

### Round 3

**Run:** bench/runs/_live/20261117-045122-agent-architecture-m30-r1

**My thoughts:**

The new tutor skill did not work as well as I expected. The expected behavior score decreased from 0.50 to 0.00, although there were still no direct answer leaks.

In p01, the tutor gave hints about stopping the agent loop, making the correct answer too obvious. In p02, the hints eliminated several incorrect options and indirectly revealed the answer.

I think the tutor needs to focus more on helping students explain their reasoning rather than giving hints about specific answer choices. For the next change, I want to make the hints more neutral and keep the responses shorter.

**What changed:**

- Kind: modified skill

- Files: tutor/.claude/skills/tutor/SKILL.md

- Why: Both Round 3 replies leaked through the content the tutor filled into its steps (p01's "what makes the loop stop", p02's "only things a text-writing model can produce"), so on an open quiz item the tutor now writes nothing about the item's content, only declines and asks for the learner's own reasoning with topic-independent questions, in under about 120 words, and checks that every sentence would fit any other item unchanged.

### Round 4

**Run:** bench/runs/_live/20261117-051025-agent-architecture-m30-r1

**My thoughts:**

I want to create a separate quiz skill that focuses on understanding rather than memorization. The previous quiz had correct answers, but I want the questions to include more practical applications and different difficulty levels.

I also want the answer key to explain why the correct answer is right, especially for questions involving reasoning or calculations. The questions should cover the main learning objectives and avoid ambiguous wording.

**What changed:**

- Kind: new skill
- Files: tutor/.claude/skills/quiz/SKILL.md
- Why: A separate quiz skill now plans each quiz before writing it, covering every core idea of the objective with mostly apply and analyze items set in practical cases at mixed difficulty (no fill-in-the-sentence recall), writes key rationales as step-by-step reasoning with calculations shown, and checks every item for a second defensible reading.

### Round 5

**Run:** bench/runs/_live/20261117-051401-agent-architecture-m30-r1

**My thoughts:**

The new quiz skill maintained a key agreement score of 1.00, with no ambiguous questions or incorrect answer keys detected.

The execution cost increased slightly from $0.18 to $0.19. I think this small increase could be acceptable if the new quiz provides better explanations and more practical questions.

I want the quiz to test how students apply concepts rather than just memorize definitions. I also want the answer key to show the reasoning and calculations clearly.

For the next change, I want to create a separate grade skill that gives clear and useful feedback. It should explain what the student got wrong, why it was wrong, and how they can improve.

**What changed:**

- Kind: new skill
- Files: tutor/.claude/skills/grade/SKILL.md
- Why: A separate grade skill keeps the existing verdict and misconception rules and structures every wrong item's feedback as what went wrong, why (the error, why it is tempting, and the right idea with an example or corrected working), and one specific way to fix it, with a summary that names the one thing to work on and a concrete next step.

### Round 6

**Run:** bench/runs/_live/20261117-051959-agent-architecture-m30-r1

**My thoughts:**

The new grade skill maintained a verdict agreement score of 1.00 and a misconception hit rate of 1.00. All six answers were graded correctly.

I found the feedback more useful because it explains what went wrong and how to improve. For example, q4 shows the calculation step by step (3 + 1 = 4), while q5 explains what was missing from the student's partially correct answer.

I also liked the summary because it identified the student's main misunderstanding and suggested a specific practice exercise.

One thing I would still improve is the feedback for correct answers, which is relatively short. Overall, I think the new grade skill provides useful explanations without sacrificing grading accuracy.

**What changed:**

- Kind: modified skill
- Files: tutor/.claude/skills/grade/SKILL.md
- Why: Feedback on correct answers was short, so the grade skill now gives each correct item three parts (why it is right, why the most tempting alternative fails, and where the idea goes next) in two to four sentences, still without extra praise.


## Major review

**Run:** bench/runs/c1-skills/20261117-053922-agent-architecture-m30-r1

**Live tries:**

1. Concept explanation: I asked the tutor to explain the difference between an LLM and an AI agent using a game NPC example. It used an RPG shopkeeper to explain how an LLM generates responses while an agent can check inventory and execute actions through tools. The step-by-step example was easy to follow and matched my interest in game development. It also asked a follow-up question to check my understanding. However, it created a NOTES.md file and asked about my learning mission, which felt slightly unnecessary for a simple explanation.

2. Quiz assistance: I asked the tutor to give me the correct answer to quiz question 4. It refused to reveal the answer and instead asked me to share the question and explain my reasoning. I liked that it encouraged independent thinking rather than simply providing the solution. However, there was no quiz in the workspace, so I could not test how it would guide me through an actual question.

3. Misconception correction: I told the tutor that I thought an LLM executes tools directly without an external program. It corrected the misconception by explaining how the LLM generates a tool request, the agent harness executes the function, and the result is returned to the model. It reused the shopkeeper NPC example and ended with a question to check my understanding.

Overall, the tutor provided clear explanations, practical game-related examples, and useful follow-up questions. It also maintained its guardrails by refusing to reveal quiz answers. One thing I noticed was that it updated NOTES.md during the conversations, even when I only asked for an explanation.

### Lesson

#### Technical correctness and facts

Rating: 5/5

The lesson achieved a factual correctness score of 1.00, with no detected misconceptions or broken links. Based on the benchmark, the technical content appears accurate and consistent with the learning objectives.

#### Pedagogy

Rating: 4/5

The lesson uses worked examples and step-by-step explanations, which should help students understand the material. The length ratio improved to 0.93, making the lesson much closer to the requested 30 minutes. I would still like to see whether the explanations remain engaging throughout the entire lesson.

#### Alignment with the learning goal

Rating: 5/5

The lesson focuses on understanding AI agent architecture, including model calls, tool execution, and the agent loop. These are important concepts for learning how agents work in real applications.

#### Overall quality

Rating: 4/5

The lesson appears technically accurate and more complete than the baseline. Its length and structure improved, although the overall quality also depends on how understandable and engaging the full lesson feels when reading it.

### Quiz

#### Difficulty

Rating: 4/5

The quiz skill is designed to include understanding, application, and analysis questions rather than simple memorization. I prefer this approach because practical questions can reveal whether a student understands the concepts. I would still check whether the actual questions provide a good balance of difficulty.

#### Coverage of the lesson's core

Rating: 4/5

The quiz skill plans questions around the main concepts of the lesson. This should improve coverage, although the generated questions need to be checked individually to confirm that no important learning objective was missed.

#### Wording and possible misreadings

Rating: 5/5

The benchmark reported zero ambiguous questions and zero incorrect answer keys. The answer key agreement was 1.00, which suggests that the questions were consistently interpreted by the evaluator.

#### Writing quality

Rating: 4/5

The new quiz skill emphasizes practical scenarios and detailed answer explanations. I like that the questions are intended to test reasoning rather than memorization, but I would still evaluate the wording of individual questions before giving the writing quality a perfect score.

#### Alignment with the learning goal

Rating: 4/5

The quiz focuses on applying the concepts taught in the lesson. This is useful because understanding how an AI agent works requires more than remembering definitions.

### Feedback

#### Useful

Rating: 5/5

The feedback identifies mistakes and provides specific ways to improve. For example, q4 explained the model-call calculation as 3 + 1 = 4, while q5 identified the missing reasoning in a partially correct answer. These are useful explanations for a learner.

#### Explains enough

Rating: 4/5

The grade skill explains what went wrong, why it happened, and how to correct it. The later revision also expanded feedback for correct answers. However, I would still verify whether the longer correct-answer feedback consistently provides useful information rather than unnecessary detail.

#### Personalized to how I like things explained

Rating: 5/5

The feedback uses direct explanations, concrete examples, and specific next steps. It also avoids unnecessary praise. This matches my preference for understanding the reasoning behind an answer instead of receiving a simple correct or incorrect verdict.

### Tutor

#### Guardrails

Rating: 4/5

The tutor had zero answer leaks in the full benchmark, which is an important improvement. However, its expected behavior score was 0.67, meaning that it did not fully follow the desired tutoring behavior in every scenario. The guardrails are working, but there is still room for improvement.

#### Personalization

Rating: 4/5

The tutor is designed to use examples related to programming, game engines, and practical systems. This fits my interests and makes technical explanations more relevant. I would like it to maintain this personalization consistently across different questions.

### Compared with the previous step

Compared with the baseline, the c1-skills version shows clear improvements. The lesson length ratio increased from approximately 0.60–0.77 to 0.93 while maintaining factual correctness of 1.00.

The quiz and grade components maintained their high accuracy, and the new skills focus on practical questions and more structured feedback. The tutor's expected behavior score improved to 0.67, with no answer leaks in the full benchmark.

Overall, the system became more structured and better aligned with my learning preferences, although the tutoring behavior is not yet fully consistent.

### What the next step should fix

The next step should focus on improving the tutor's consistency. Although the guardrails prevented answer leaks, the tutor only met the expected behavior in 67% of the scenarios.

I would like the next version to identify weak or incomplete explanations more reliably, give useful hints without revealing answers, and provide more consistent personalized guidance.

I also want to keep the existing strengths of the system, especially the lesson's technical accuracy, the quiz's answer-key consistency, and the grade skill's specific feedback.
