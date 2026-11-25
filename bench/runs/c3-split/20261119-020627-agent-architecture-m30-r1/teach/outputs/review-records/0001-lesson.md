# Review record: lesson 0001, context and memory (O3, 30 minutes)

## Plan and examples
- Plan: `drafts/plan-0001.md`. Examples: `drafts/examples-0001.md`.
- Departures: all four practice checks were replaced by the example designer's new cases (as the plan allowed). The plan's section 6 "Go further" community was left as "none verified", as the plan said. Chunk size is stated in tokens (about 200), per the designer's note. The tool-definition size changes between sections (300, 450, 400); the draft says section 5 uses a different tool set. Section 1's calendar-in-the-list example was changed to say it is the second call (clarity finding 1).
- Extra work by the writer: a "request" versus "call" definition was added in section 1.

## Clarity checker (one pass): 3 major, 9 minor
1. S1 calendar result in the first call - major - fixed: said it is the second call of the request.
2. S1 "tool definitions" undefined - major - fixed: defined before the table.
3. S1 role/system/samples - minor - fixed: one line explaining `system` and `user`; "samples" became "writes its response".
4. S1 request vs call - minor - fixed: defined both; cost steps now say "call".
5. S2 history before definition - minor - fixed: reordered and defined.
6. S2 "context editing" third term - minor - fixed: name dropped from the steps; clearing versus compaction separated.
7. S2 compaction without example - minor - fixed: added a before and after summary.
8. S4 "best match" unexplained - major - fixed: one sentence picturing scoring, with the method skipped.
9. S4 index/just in time/hybrid terms - minor - fixed: "searchable list", and step 7 rewritten in plain words.
10. S4 who writes the chunk line - minor - fixed.
11. S5 call count changes without reason - minor - fixed.
12. S5 task A solution used a fourth option - minor - fixed: restated with `check_calendar` and clearing.

## Lesson reviewer: 1 pass, verdict CLEAN (0 major, 5 minor)
- A1 (call-2 list omits the model's tool-request tokens) - fixed: noted in section 1.
- A2 (1,500 tokens called context rot) - fixed: reworded to say it becomes rot as windows grow.
- D1 (five terms in section 1) - not changed: request, call and tool definitions are needed before the first example; they are plain-language, not techniques.
- D2 (move step 7 of section 4 to Go further) - not changed: it covers just-in-time retrieval, named in the objective; I reworded it instead. Moving it would also shorten the lesson.
- D3 (confusing "not a saving" sentence) - fixed.
- No second pass, because the verdict was CLEAN.

## Length
My estimate was about 5,000 visible words (about 33 minutes), above the 100% target and under the bench's 1.5x ceiling (6,750). I could not run a word-count script (it needed a permission I did not have), so this is a by-hand estimate. Nothing was added to reach it.

## Final verdict
CLEAN. The final lesson was written once to `lessons/0001-context-and-memory.html`.
