# Review record: lesson 0001, context and memory (O3)

**Passes:** 2. Pass 1 gave REVISE (3 major, 3 minor); pass 2, a narrow re-check of the changed parts, gave CLEAN, so the loop ended.

**Length:** My final estimate is about 4,500 to 5,000 visible words for a 30-minute request (the pass-2 reviewer put it at 4,200 to 5,600, above the 90% floor). The cut in section 5 was offset by moving the benchmark and just-in-time notes into "Go further" and adding a longer cost comparison to the retrieval worked example, so nothing went below budget. No further additions were needed.

## Pass 1

- **A. Facts, major.** The call-2 check implied the API would accept a history with a tool request and no result. Changed: the bug now drops both the request and the result, so the history is valid and the model starts over.
- **A. Facts, major.** "Hundreds of thousands of tokens" for 300 pages disagreed with the cited 200,000 tokens per 500 pages. Changed to about 120,000 tokens, and a gap of more than 100 times.
- **A. Facts, minor.** "Lightweight references" paraphrased the article's "lightweight identifiers". Changed in Go further to the article's wording.
- **B. Pedagogy, minor.** The footer said quiz 0002 was ready before it existed. Quiz 0002 and its key were written in the same pass, so the line is now true.
- **D. Complexity, major.** The retrieval section held too many named techniques. Changed: it keeps retrieval and chunk; search by meaning and by exact words is in plain words; BM25 is named once in practice feedback and once in Go further; the benchmark and just-in-time naming moved to Go further.
- **D. Complexity, minor.** "Attention budget" removed from the context-rot section.
- **D. Quality, minor (retrieval paragraph too dense).** Split into short paragraphs, with the TS-999 example as its own paragraph.

## Pass 2

No findings. All pass-1 major fixes confirmed. Final verdict: CLEAN.
