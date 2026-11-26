# Review record: lesson 0001, context and memory (O3)

Plan: `drafts/plan-0001.md`.
Examples: `drafts/examples-0001.md`.
Draft: `drafts/lesson-0001-context-and-memory.html`.
Final lesson: `lessons/0001-context-and-memory.html`.

## Departures from the plan and the examples file

- Section 4 practice uses a new student, Sam (the example designer's change), because the plan's item repeated step 1 of its worked example.
- Added a short definition of "model call", "input" and "reply" in the opening, since Riley has never called a model from code.
- Section 1 says the stop-early behaviour is for newer Claude models, as the cited docs describe, and the practice stem says so too.
- Code was re-wrapped to fit a narrow screen (`save_note`, `search_manual`, `call_model`); the behaviour is unchanged.
- Section 2 gained a two-step agent trace and a check (review pass 1). The plan had only student messages.
- Section 5 lost the pointer, hybrid and "simplest thing" material, and the 200,000-token guide moved to "Go further" (review pass 1). A "pick the search" practice was added.
- Section 6 lost the mix-up box the example designer added (to offset added length), and its table moved below the faded practice.
- Section times: Section 1 is 3 minutes and Section 2 is 5 (the plan had 4 and 4).
- Quiz 0001 overlap: the new agent trace necessarily shows a tool request, its result joining the history and a new model call, which bear on quiz 0001's ideas. The plan had limited this to one statement. Both quiz 0001 submissions were already in the workspace, it uses a different scenario and tools, and no quiz 0001 item is repeated as practice. Anyone grading or retaking quiz 0001 should know the lesson came after submissions s1 and s2.

## Clarity check (single pass): 4 major, 8 minor

| # | Section | Check | Level | Change |
|---|---|---|---|---|
| 1 | 3 | 3 | major | Said clearly that the source counts clearing as a light form of compaction with no summary, and how the lesson uses "clear" and "compact". |
| 2 | 3 | 5 | major | Explained why the older talk grew to 18,000 and why to compact before the limit. |
| 3 | 1 | 6 | major | Rewrote the rejected-option feedback. |
| 4 | 5 | 4 | major | Split "Could you skip retrieval?" into fit and cost checks. |
| 5 | 5 | 3 | minor | Rewrote the pointer paragraphs (later moved to "Go further"). |
| 6 | 6 | 6 | minor | Named the items to add in step 6; added the official record to the setup. |
| 7 | 3 | 5 | minor | Put the riddle and inventory in the setup; said a model writes the summary before the check. |
| 8 | 4 | 5 | minor | Stated the size of today's chat and what the comparison shows. |
| 9 | 1-3 | 2 | minor | Unbolded the extra terms; removed "turn" and "recent turns". |
| 10 | 1, 3 | 1 | minor | Stopped using "chunk" before Section 5. |
| 11 | 1 | 5 | minor | Showed the page calculation and units; reworded the estimate rule. |
| 12 | Summary | 3 | minor | Rewrote the line about new sessions. |

## Reviewer, pass 1: 2 major, 5 minor (verdict REVISE)

### A. Technical correctness and facts
- Check 1, minor: "simplest thing that works" was general advice, applied to whole-document input. Removed the quote.
- Check 3, minor: "one record per student" sat inside a citation that did not give it. Moved outside as the makerspace case.

### B. Pedagogy and structure
- Check 5, minor: the sorting table answered the faded practice. Moved it below.

### C. Alignment with the objective
- Check 8, major: what is kept between agent steps was only asserted. Added "each step is a new model call", a worked trace and a call-3 check. Used a game-debugging agent instead of the suggested calendar request, to stay clear of quiz 0001.

### D. Overall quality and unnecessary complexity
- Check 11, major: too many retrieval techniques. Cut or moved them as listed above and added practice on the two matching methods.
- Check 11, minor: "working memory" sentence cut.
- Check 13, minor: Figure 3 arrow labels placed beside their arrows.

## Reviewer, pass 2: 0 major, 0 minor (verdict CLEAN)

Narrow re-check of the changed parts. All four headings: none. Both pass-1 majors confirmed fixed. Checks 3, 9, 12 and 13 were not re-checked.

The loop stopped after pass 2 with a CLEAN verdict (also the two-pass limit).
After pass 2, one wording edit: the Section 2 mix-up quote now says "earlier messages" instead of the undefined "turns".

## Length

My estimate by section: opening and warm-up 420, Section 1 780, Section 2 950, Section 3 780, Section 4 680, Section 5 700, Section 6 760, summary, further and closing 400; about 5,450 words, or 36 minutes at 150 per minute.
This estimate runs high; the reviewer put the visible text at about 5,000 words (about 33 minutes) on pass 2.
Both are above the 4,500-word floor and inside the bench's range, so nothing was added for length.
Neither figure is a script count.

## Final verdict

CLEAN.
