# Pre-registration: the length study

This file is for 598E students, for whom the length study is the required rider, and for 498E students who chose it as their stretch.
Everyone else can ignore it or delete it.

A pre-registration is a claim you write down, with the analysis that will judge it, before you can see the answer.
Its value is that the claim can be wrong in a way anyone can check, and that you cannot bend it afterwards to fit the numbers.
A clear "no difference as large as the one I cared about" scores as well as a confirmation, so you have no reason to hedge.

**Git history is how I will know the order.**
Fill in sections 1 to 4 and commit this file before the first of the eighteen length-study runs.
`uv run p3 check --final` reads `git log` and confirms that the commit came first.
After that commit, do not edit sections 1 to 4.
If something must change, add a dated entry in section 6 and leave the original as it was.
Section 5 you write at the end, after the runs and the comparisons.

Each section that needs your words ends with a marker line.
Replace that line with your answer; `uv run p3 check --final` fails while one is left.

The design is fixed: two configs, three lengths, three teach-only runs in each cell, on the shared topic.

| | 10 minutes | 30 minutes | 60 minutes |
|---|---|---|---|
| `c1-skills` | 3 runs | 3 runs | 3 runs |
| `final` | 3 runs | 3 runs | 3 runs |

```
uv run p3 bench --config c1-skills --only teach --minutes 10 --repeats 3
uv run p3 bench --config c1-skills --only teach --minutes 30 --repeats 3
uv run p3 bench --config c1-skills --only teach --minutes 60 --repeats 3
uv run p3 bench --config final --only teach --minutes 10 --repeats 3
uv run p3 bench --config final --only teach --minutes 30 --repeats 3
uv run p3 bench --config final --only teach --minutes 60 --repeats 3
```

After the runs, one blind comparison per length, each pairing only the study's teach-only runs at that length, three pairs each:

```
uv run p3 compare c1-skills final --job teach --teach-only --minutes 10
uv run p3 compare c1-skills final --job teach --teach-only --minutes 30
uv run p3 compare c1-skills final --job teach --teach-only --minutes 60
```

`--teach-only` matters at 30 minutes, where the ladder's full runs of `c1-skills` and `final` hold a 30-minute lesson too; it keeps them out, so every length is paired the same way.
These three sessions are your second blind comparison of the project, beside `c0-baseline` against `final`, and you make no other on top.
The numbers for every cell come from one command:

```
uv run p3 report --configs c1-skills,final --teach-only
```

---

## 1. Hypothesis

One or two sentences: as the requested length grows from 10 to 60 minutes, which config loses more quality, in which measure, and why you expect it.
For example: "The single-agent `c1-skills` loses more than `final` as lessons get longer, because one context writing a 60-minute lesson drifts from the plan, so its `teach_facts_correct` falls further from 10 to 60 minutes, and `final` wins more of the blind pairs at 60 minutes than at 10."
It should be something you could be wrong about.

I predict that c1-skills will lose more lesson-length accuracy than final as the requested lesson length increases from 10 to 60 minutes. Longer lessons require more planning and content, so I expect c1-skills to underestimate the amount of material needed, while final will maintain a length ratio closer to 1.00 because of its additional planning, review, and final length checks.

---

## 2. The smallest difference that matters

Choose one primary measure now, so you cannot pick the better one afterwards, and say how large a difference in it would matter to a learner, and why that size.
Call it Δ (delta).

Know what three runs per cell can show before you choose.
There are three blind teach pairs at each length, and even 3 of 3 for one config has a two-sided sign-test p-value of 0.25, so no single length can settle a preference on its own.
Across all three lengths there are nine pairs: 8 of 9 gives a p-value of about 0.04, and 7 of 9 about 0.18.
An objective measure, such as `teach_facts_correct` or the judge's level fit, gives three numbers per cell, and you can see a difference only when it is larger than the spread between the three runs.
So choose a Δ that is large enough to matter and large enough for three runs to see.

My primary measure is lesson-length error, calculated as the absolute difference between teach_length_ratio and 1.00.

I choose Δ = 0.15, meaning a difference of 15 percentage points in length error. For a 60-minute lesson, this represents approximately 9 minutes of estimated reading time, which I think would noticeably affect a learner's study plan. A smaller difference might be difficult to distinguish from normal variation with only three runs per cell.

I will calculate the mean length error for each configuration and length, then compare how much that error changes from 10 to 60 minutes.
---

## 3. The measures

Name each measure you will report, and how you will compute it.
At least these:

- **Your primary measure** from section 2, per cell, as the mean and the range of the three runs.
- **The blind comparison** of `c1-skills` against `final` at each length, one session per length, never across lengths, and `final`'s share of the non-tie picks at each.
- **Length accuracy:** `teach_length_ratio` per cell, the lesson's estimated reading time against the minutes requested.
  It is a rough estimate at 150 words a minute, and a "60-minute" lesson that is really 35 confounds every other measure, so say now what you will do with a cell whose lessons miss their length.
- **Cost against length:** tokens per minute of lesson for each config, and whether `final`'s overhead grows in step with length or faster.
  Say whether you divide by the minutes requested or by the estimated minutes.

I will report the following measures for each configuration and requested lesson length.

**Primary measure — Length error:** I will calculate abs(teach_length_ratio - 1.00) for each run and report the mean and range across the three runs in each cell. Lower values mean that the lesson is closer to the requested duration.

**Blind comparison:** I will run one blind comparison session for each length, using only the three teach-only runs from c1-skills and final at that length. I will report final's share of non-tie preferences as final wins divided by all non-tie picks. I will also record ties and how often I could identify which configuration produced each lesson.

**Length accuracy:** I will report teach_length_ratio as the mean and range across the three runs. I will treat a lesson as substantially short or long if its ratio falls outside 0.90 to 1.10. I will still include these runs in the primary analysis, but I will flag them and avoid attributing differences in other quality measures entirely to the architecture when lesson lengths differ substantially.

**Cost against length:** I will divide each run's total token usage by the requested lesson minutes (10, 30, or 60), then report the mean and range for each cell. I will also compare the token usage of final against c1-skills at each length to see whether the additional overhead grows proportionally with lesson length or faster.

---

## 4. The analysis, and what each result will mean

The comparison is the change from 10 to 60 minutes in your primary measure, for each config, read against the spread of the three runs.
Write the rule now.
This is the default rule, and you can tighten it, but do not loosen it after you see your numbers.

| The result | I will say |
|---|---|
| the two configs' changes differ by Δ or more in the direction I predicted, and the three runs' ranges at 60 minutes do not overlap | supported |
| they differ by Δ or more in the other direction, and the ranges at 60 minutes do not overlap | contradicted: the opposite holds on these runs |
| they differ by less than Δ | no difference as large as Δ on these runs, with the ranges reported |
| anything else | inconclusive with three runs per cell, and I say so |

Then name the threats to validity you will report (lecture 22): blinding failures (your could-tell share at each length), judge bias toward longer outputs (lecture 24), the rough length estimate, and three runs per cell.
Say which one worries you most for your hypothesis.

I will use the decision rule provided in the assignment without changing it after seeing the results.

For each configuration, I will calculate the change in mean length error from 10 to 60 minutes. My hypothesis predicts that c1-skills will have a larger increase in error than final.

If the difference between these changes is at least Δ = 0.15 in the predicted direction, and the three-run ranges at 60 minutes do not overlap, I will consider the hypothesis supported.

If the difference is at least 0.15 in the opposite direction and the 60-minute ranges do not overlap, I will consider the hypothesis contradicted.

If the difference is smaller than 0.15, I will report that there was no difference as large as my chosen threshold in these runs. All other outcomes will be inconclusive with three runs per cell.

My main threats to validity are the small sample size, the rough lesson-length estimate, possible bias toward longer outputs in the judge, and failures in blinding.

I am most concerned about the rough length estimate because length accuracy is my primary measure. The benchmark estimates reading time from visible words at 150 words per minute, but actual learning time also depends on the difficulty of the material, examples, and practice exercises. A lesson with the correct word count might still take much longer or shorter to complete.

---

## 5. Outcome (write this after the fact)

What did each measure show, cell by cell?
Which row of the table in section 4 is it?
Did the lessons meet their lengths, and what did the cost per minute of lesson do?
What would you do next, and what would you want a reader to take from this?

TODO: your outcome.

---

## 6. Amendments

Dated entries only, one per change, each saying what changed and why.
Leave this section as it is if nothing changed.
