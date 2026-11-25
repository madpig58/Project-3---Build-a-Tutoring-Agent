# Components

One entry for every skill and every subagent you built, from `c1-skills` to `final`, including the ones you dropped, even one you took out again before any snapshot.
The heading is the skill's folder name or the subagent's `name` from its frontmatter, and `reviews/README.md` says what each field holds.
Replace the empty entry at the bottom with your first component, and copy it for each one after that.
Claude Code may fill in Kind, Step added, and With and without; Purpose, Review and Kept in final are yours.

<!--
An example of a finished entry:

### quiz-reviewer

- Kind: subagent
- Step added: c2-review
- Purpose: My c1 review found two quiz items that could be read two ways (q2 and q4) and one whose correct option repeated the stem; a reviewer with a fresh context reads the draft the way a learner will, which the quiz skill writing its own items cannot do, so it is a subagent and not a step in the skill.
- With and without: reviews/c2-review.md, Round 1 (without) and Round 2 (with)
- Review: Without it, q2 asked which design "is better" with no criterion; with it, every stem names its criterion and the reviewer's record shows two items flagged and fixed in one pass, for about 0.6M more tokens per quiz, which I think a quiz is worth, because a misread item teaches the wrong thing.
- Kept in final: yes
-->

### teach

- Kind: skill
- Step added: c1-skills
- Purpose: I wanted the tutor to provide complete lessons with clear explanations and worked examples. The baseline lessons were too short, so this skill focuses on better lesson structure, practical examples, and matching the requested lesson length.
- With and without: reviews/c1-skills.md, Round 1 (without) and Round 2 (with)
- Review: The lesson length ratio improved from 0.71 in the baseline to 0.93 in c1-skills, while factual correctness remained at 1.00. I think this was a useful improvement because the lesson became more complete without increasing the teaching cost. However, one c1-skills run is not enough to establish consistent improvement.
- Kept in final: yes

### tutor

- Kind: skill
- Step added: c1-skills
- Purpose: I wanted the tutor to guide students without revealing quiz answers or giving hints that make the correct answer too obvious. The baseline sometimes gave overly specific hints, so this skill focuses on encouraging independent reasoning while respecting the student's learning level.
- With and without: reviews/c1-skills.md, Round 2 (without) and Round 3 (with)
- Review: The expected behavior score improved from 0.44 to 0.67, with zero direct answer leaks. During my live tests, the tutor used game NPC examples, refused to reveal quiz answers, and corrected misconceptions step by step. However, the benchmark score shows that its behavior was still inconsistent.
- Kept in final: yes

### quiz

- Kind: skill
- Step added: c1-skills
- Purpose: I wanted quizzes to test understanding and practical application rather than memorization. The skill plans questions at different difficulty levels and provides explanations that show the reasoning behind each correct answer.
- With and without: reviews/c1-skills.md, Round 4 (without) and Round 5 (with)
- Review: The quiz maintained an answer-key agreement score of 1.00, with no detected ambiguous items or incorrect keys. The new skill emphasizes application and analysis questions, but its cost increased from $0.17 to $0.22 per quiz scenario. I think the additional structure is useful, although the objective checks alone cannot prove that the questions became better.
- Kept in final: yes

### grade

- Kind: skill
- Step added: c1-skills
- Purpose: I wanted feedback to explain not only whether an answer was correct, but also why it was correct or incorrect and how the learner could improve. This skill separates grading from teaching and gives more structured explanations.
- With and without: reviews/c1-skills.md, Round 5 (without) and Round 6 (with)
- Review: Grading agreement and misconception detection remained at 1.00, while the cost stayed around $0.16 per scenario. The feedback explained mistakes clearly, including the calculation in q4 and the missing reasoning in q5. I found this useful because it gives students a specific way to improve instead of only showing the correct answer.
- Kept in final: yes

### quiz-reviewer

- Kind: subagent
- Step added: c2-review
- Purpose:  I added this reviewer because the quiz skill sometimes created ambiguous questions, weak distractors, and questions that revealed answers to other items. I wanted a separate subagent to check each question and its answer key before the quiz was finalized.
- With and without: reviews/c2-review.md, Round 1 (without) and Round 2 (with)
- Review: During the quick rounds, the reviewer found unclear wording, overlapping questions, weak distractors, and incorrect misconception tags. After adding it, the quiz key agreement improved from 0.80 to 1.00, with zero ambiguous items. However, the cost increased from $0.23 to $0.56. In the full benchmark, quiz generation cost $0.65 compared with $0.22 in c1-skills, while both achieved perfect key agreement. I think the reviewer was useful for catching mistakes, but the additional cost was significant.
- Kept in final: yes

### grade-reviewer

- Kind: subagent
- Step added: c2-review
- Purpose: I added this reviewer to improve grading feedback without changing correct verdicts. The original grading was accurate, but some explanations were too long or repetitive. I wanted the reviewer to check accuracy, remove unnecessary details, and make feedback easier to follow.
- With and without: reviews/c2-review.md, Round 2 (without) and Round 3 (with)
- Review: The reviewer found four minor issues and no major issues during the quick round. It shortened feedback, removed repeated explanations, and simplified the summary to one main learning goal and one next step. It stopped after one pass because there were no major findings. Grading agreement remained at 1.00, but the cost increased from $0.16 to $0.28 for the tested scenario. I think the feedback became clearer and more focused, although the reviewer increased the cost.
- Kept in final: yes

### lesson-reviewer

- Kind: subagent
- Step added: c2-review
- Purpose: I added this reviewer to check technical correctness, lesson structure, learning-goal coverage, and unnecessary complexity. I wanted lessons to remain accurate and beginner-friendly without introducing too many advanced concepts at once.
- With and without: reviews/c2-review.md, Round 3 (without) and Round 4 (with)
- Review: The reviewer identified a misleading retrieval statistic, unnecessary technical terms, and inconsistencies in examples. It corrected these problems while maintaining factual correctness at 1.00. However, the first reviewed lesson cost $1.46 compared with $0.60 before the reviewer. I later reduced repeated reviewing and added a final length check, which improved the length ratio from 0.82 to 0.99 in the quick runs. In the full benchmark, the lesson achieved a length ratio of 0.92 and cost $1.32. I think the reviewer improved clarity and technical reliability, but its cost was still high.
- Kept in final: yes

### lesson-planner

- Kind: subagent
- Step added: c3-split
- Purpose: I wanted to separate lesson planning from lesson writing so the tutor could organize learning goals, decide which concepts to introduce first, and build a logical progression before generating a lesson. This subagent focuses on lesson structure rather than writing the final explanation.
- With and without: reviews/c3-split.md, Round 1 (without) and Round 2 (with)
- Review: The split gave lesson planning a dedicated role and made the workflow easier to organize. However, adding more subagents increased the complexity and cost of lesson generation. The available results do not establish that the planner alone caused a measurable improvement, so I consider it useful mainly for separating responsibilities.
- Kept in final: yes

### lesson-example-designer

- Kind: subagent
- Step added: c3-split
- Purpose: I wanted the tutor to create concrete and relevant examples instead of relying only on abstract explanations. This subagent designs examples that connect technical concepts to situations learners can understand, including programming and game development.
- With and without: reviews/c3-split.md, Round 2 (without) and Round 3 (with)
- Review: Separating example design made it possible to focus specifically on examples and their relationship to learning goals. However, the additional subagent increased the amount of work required to generate lessons. I cannot attribute the overall lesson quality to this component alone, but I think relevant examples are important for making difficult concepts easier to understand.
- Kept in final: yes

### lesson-clarity-checker

- Kind: subagent
- Step added: c3-split
- Purpose: I wanted a final review of lesson clarity after the planner and example designer had completed their work. This subagent checks whether explanations are understandable, logically connected, and appropriate for the learner's level.
- With and without: reviews/c3-split.md, Round 3 (without) and Round 4 (with)
- Review: The checker added a separate opportunity to identify confusing explanations and unnecessary complexity. However, the additional review stage also contributed to the cost of the larger lesson-generation architecture. I think the clarity check is useful, although the available evidence does not isolate its individual effect from the other lesson subagents.
- Kept in final: yes

### grader

- Kind: subagent
- Step added: final
- Purpose: I wanted to separate the actual grading process from the main tutor so that answer keys could be handled in a more restricted workflow. The grader subagent evaluates submissions and produces grading results, while the main tutor focuses on communicating with the learner.
- With and without: reviews/final.md, Round 1 (without) and Round 2 (with)
- Review: The dedicated grader worked with the existing grade-reviewer workflow. In a targeted test with deliberately incorrect grading details, the review process identified and corrected the errors. The separation also allowed the main tutor to avoid directly reading answer keys during grading. However, this is not a complete security guarantee, and the workflow still requires careful handling of grading information.
- Kept in final: yes

### practice

- Kind: skill
- Step added: final
- Purpose: I wanted learners to strengthen their understanding through exercises instead of only reading lessons or taking quizzes. The practice skill gives one exercise at a time, checks both the answer and the reasoning, and provides progressive hints when the learner struggles.
- With and without: reviews/final.md, Round 12 (without) and Round 13 (with)
- Review: In my manual A* pathfinding test, the practice skill accepted the correct calculations but did not treat the answer as proof of understanding because the learner had not explained the reasoning. When I deliberately gave an incorrect generalization about h(n), the skill identified the misconception and asked a targeted follow-up question instead of revealing the solution. It also updated NOTES.md to record the learning gap. This demonstrated useful adaptive feedback, although I did not test the complete mastery process across multiple exercises.
- Kept in final: yes

### explanation-checker

- Kind: subagent
- Step added: with-explanation-checker
- Purpose: I wanted a separate subagent to review general explanations before they were sent to learners while quizzes were open. It checked whether explanations answered the question, stayed within the word limit, mapped analogies correctly, and avoided unnecessary hints toward quiz answers.
- With and without: reviews/final.md, Round 15 (without) and Rounds 16 and 17 (with); removed in Round 17
- Review: The checker ran at the intended time and shortened one draft from 312 words to 254 words. However, it significantly increased token usage and runtime. In the final focused test, p06 used approximately 68% more tokens and 56% more runtime than the version without the checker. The checker also introduced wording close to an open quiz answer, even though preventing such hints was one of its main purposes. Both versions passed p06 in their respective single runs, so I did not find enough evidence that the checker justified its additional cost.
- Kept in final: no. I preserved the component in configs/with-explanation-checker/ for the experimental comparison, but removed it from the final tutor because its additional cost and potential quiz-hint risks were not justified by the observed benefits.

### study-plan

- Kind: skill
- Step added: final
- Purpose: I wanted the tutor to support learning across multiple sessions instead of only answering individual questions. The study-plan skill uses the learner's goals, available time, notes, and learning records to recommend a prioritized sequence of study sessions.
- With and without: reviews/final.md, Round 18 (without) and Round 19 (with)
- Review: In manual tests, the skill created five sessions totaling 180 minutes, revised an existing plan to four sessions totaling 90 minutes, and correctly requested missing goals or time information. It saved and replaced plans only after explicit approval. It also declined to reveal open quiz topics and was correctly invoked through /tutor. However, one routing test proposed 170 minutes based on MISSION.md instead of preserving the saved 90-minute limit. The focused regression benchmark passed both tutor probes with zero detected answer leaks, although those probes did not directly test study-plan.
- Kept in final: yes
