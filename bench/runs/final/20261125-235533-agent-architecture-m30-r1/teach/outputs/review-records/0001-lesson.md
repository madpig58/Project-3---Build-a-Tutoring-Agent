# Review record: lesson 0001, context and memory in an agent (O3)

## Plan and examples
- Plan: `drafts/plan-0001.md`. Examples: `drafts/examples-0001.md`.
- Departures: the plan's practice for Sections 2, 3 and 4 was replaced by the designer's new cases (drill press, Jo, a sponsor's 2,000,000-token window). The Priya example uses six calls, not five, because the final answer is a call. The compaction term was cut to one plain sentence.

## Clarity checker (one pass)
- Retrieval, step 2 and the just-in-time paragraph (major): cut to one sentence on matching words or meaning, and a one-line load-when-needed note. Removed embeddings, CLAUDE.md, "lightweight identifiers".
- Reflect, safety (major): added in Section 5 why a model-written note is less safe than a program-checked booking database, and a line about the database in the Priya example.
- Priya sizes (major): the sizes are now in their own step and each call's addition is listed, ending in 10,820.
- Retrieval cost (minor): stated the three-call assumption and which calls re-send the chunks.
- "Top-20 failure" (minor): defined.
- Weights (minor): glossed in the option's feedback.
- Section 3 opening (minor): now opens with the game picture before the two terms.
- Section 5 rules (minor): split into four rules, each with a reason; "read on demand" explained; the safety question rewritten.
- High-signal (minor), pure function and "progressive accumulation" (minor): replaced with plain words.
- Compaction and sub-agents named (minor): names dropped.
- `role` in the sketch (minor): one gloss added.
- System prompt and tool definitions (minor, from the reviewer): kept as one short plain sentence before the example; each is also named where it enters the window in the worked example.

## Reviewer
- Passes: 1. Verdict CLEAN (0 major, 5 minor), so no second pass.
- A1 (1,840 slip): fixed to 1,900 with the sum shown.
- A2 (49% figure scope): reworded to say a model-written description added to both searches.
- A3 (caching): one aside added, with no teaching of caching.
- D1 (four definitions in Section 1): not changed; the two plain terms are one sentence and are named again in the example.
- D2 (statistic and summary remark): kept, because the statistic is now accurate and flagged as the source's result; not moved.

## Length
- Hand estimate about 5,300 visible words (about 35 minutes by 150 wpm, about 90% of that after the bench's usual overcount), inside the 2,700 to 6,750 range. The shell was blocked by the keys guard, so no script count. Nothing was added to reach the length.
- Final verdict: CLEAN.
