# Report

This file is written by `p3 report --write` (p3 0.2.0, 2026-11-26 01:37 UTC). Do not edit it by hand: it is written again whenever new runs are scored.

## Results on agent-architecture

Scored full runs (quick runs and --only runs left out); each cell is the mean over the runs, with the range in brackets.

### Quality

| config | runs | teach facts | teach misconc. | length ratio | dead links | key agreement | wrong keys | ambiguous items | verdict agreement | false wrong | misconc. hit | leaks | behavior met |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `c0-baseline` | 3 | 1.00 | 0 | 0.71 (0.60-0.77) | 0 | 1.00 | 0 | 0 | 1.00 | 0.00 | 1.00 | 0 | 0.44 (0.33-0.50) |
| `c1-skills` | 1 | 1.00 | 0 | 0.93 | 0 | 1.00 | 0 | 0 | 1.00 | 0.00 | 1.00 | 0 | 0.67 |
| `c2-review` | 1 | 1.00 | 0 | 0.92 | 0 | 1.00 | 0 | 0 | 1.00 | 0.00 | 1.00 | 0 | 0.67 |
| `c3-split` | 1 | 1.00 | 0 | 0.97 | 0 | 1.00 | 0 | 0 | 1.00 | 0.00 | 1.00 | 0 | 0.67 |
| `final` | 2 | 0.83 | 0 | 1.10 (1.03-1.18) | 0 | 1.00 | 0 | 0.5 (0-1) | 1.00 | 0.00 | 1.00 | 0 | 0.58 (0.50-0.67) |

Teach facts, key agreement, verdict agreement, false wrong, misconception hit and behavior met are shares (0 to 1); misconceptions, dead links, wrong keys, ambiguous items and leaks are counts per run.
A dash means no run could be scored on that check, and n= says how many of the runs could.
A job that failed counts against the config: no lesson scores 0 teach facts, no quiz and key 0 key agreement, a missing grades file disagrees on every item, and a tutor scenario with no reply is not met; leaks need a reply to check, so such a scenario is left out of them.
The length ratio is a rough reading-time estimate (visible words / 150) over the minutes requested; 0.6 to 1.5 counts as on length.

### Cost: teach

| config | runs | tokens | output tokens | minutes | subagents | list-price $ |
|---|---:|---:|---:|---:|---:|---:|
| `c0-baseline` | 3 | 755.5k (619.2k-969.8k) | 30.1k (25.8k-34.8k) | 3.2 (2.8-3.6) | 0 | 0.62 (0.54-0.70) |
| `c1-skills` | 1 | 726.7k | 28.2k | 3.1 | 0 | 0.60 |
| `c2-review` | 1 | 1.68M | 68.1k | 6.6 | 2 | 1.32 |
| `c3-split` | 1 | 3.37M | 112.2k | 12.2 | 4 | 2.31 |
| `final` | 2 | 3.57M (3.50M-3.65M) | 158.2k (112.3k-204.1k) | 24.1 (11.7-36.6) | 7 (6-8) | 3.02 (2.42-3.62) |

### Cost: quiz

| config | runs | tokens | output tokens | minutes | subagents | list-price $ |
|---|---:|---:|---:|---:|---:|---:|
| `c0-baseline` | 3 | 148.1k (144.6k-152.3k) | 4.8k (4.0k-6.1k) | 0.7 (0.6-0.9) | 0 | 0.17 (0.16-0.19) |
| `c1-skills` | 1 | 194.7k | 8.3k | 1.2 | 0 | 0.22 |
| `c2-review` | 1 | 830.2k | 28.4k | 3.2 | 2 | 0.65 |
| `c3-split` | 1 | 551.0k | 22.4k | 2.9 | 2 | 0.52 |
| `final` | 2 | 807.5k (803.2k-811.8k) | 44.6k (42.0k-47.3k) | 5.7 (5.4-6.0) | 3 | 0.81 (0.79-0.84) |

### Cost: grade

| config | runs | tokens | output tokens | minutes | subagents | list-price $ |
|---|---:|---:|---:|---:|---:|---:|
| `c0-baseline` | 3 | 283.1k (255.8k-297.3k) | 7.1k (6.8k-7.3k) | 1.1 | 0 | 0.32 (0.31-0.33) |
| `c1-skills` | 1 | 283.6k | 7.9k | 1.1 | 0 | 0.32 |
| `c2-review` | 1 | 621.7k | 17.9k | 2.3 | 2 | 0.57 |
| `c3-split` | 1 | 737.3k | 22.3k | 11.6 | 3 | 0.73 |
| `final` | 2 | 1.33M (1.25M-1.41M) | 62.1k (59.1k-65.2k) | 15.6 (7.6-23.7) | 6.5 (6-7) | 1.37 (1.30-1.44) |

### Cost: tutor

| config | runs | tokens | output tokens | minutes | subagents | list-price $ |
|---|---:|---:|---:|---:|---:|---:|
| `c0-baseline` | 3 | 627.0k (603.8k-653.0k) | 10.5k (9.9k-11.4k) | 2.7 (2.3-3.6) | 0 | 0.65 (0.64-0.66) |
| `c1-skills` | 1 | 523.2k | 7.9k | 1.8 | 0 | 0.57 |
| `c2-review` | 1 | 554.6k | 8.1k | 2.0 | 0 | 0.57 |
| `c3-split` | 1 | 540.5k | 8.2k | 1.9 | 0 | 0.58 |
| `final` | 2 | 1.03M (1.02M-1.04M) | 20.1k (20.0k-20.2k) | 3.5 (3.4-3.6) | 0 | 0.96 (0.95-0.98) |

### Cost: all jobs

| config | runs | tokens | output tokens | minutes | subagents | list-price $ |
|---|---:|---:|---:|---:|---:|---:|
| `c0-baseline` | 3 | 1.81M (1.66M-2.03M) | 52.4k (48.3k-55.8k) | 7.7 (6.8-8.9) | 0 | 1.77 (1.68-1.81) |
| `c1-skills` | 1 | 1.73M | 52.3k | 7.2 | 0 | 1.72 |
| `c2-review` | 1 | 3.68M | 122.5k | 14.2 | 6 | 3.11 |
| `c3-split` | 1 | 5.20M | 165.1k | 28.6 | 9 | 4.14 |
| `final` | 2 | 6.74M (6.73M-6.74M) | 285.1k (244.8k-325.4k) | 48.9 (44.7-53.1) | 16.5 (16-17) | 6.17 (5.65-6.68) |

Costs are per run, summed over the job's scenarios; list-price $ is the list-price equivalent, not what you pay on a subscription.

## Your ratings

Your ratings from 1 to 5 in the major reviews (reviews/<step>.md), which review full runs on the shared topic; a dash means no rating there yet, one that p3 check does not accept, or a job that step does not review (Tutor in c2-review; Quiz, Feedback and Tutor in c3-split).

| job | criterion | c1-skills | c2-review | c3-split | final |
|---|---|---:|---:|---:|---:|
| Lesson | Technical correctness and facts | 5 | 5 | 5 | - |
| Lesson | Pedagogy | 4 | 5 | 5 | - |
| Lesson | Alignment with the learning goal | 5 | 5 | 5 | - |
| Lesson | Overall quality | 4 | 4 | 4 | - |
| Quiz | Difficulty | 4 | 4 | - | - |
| Quiz | Coverage of the lesson's core | 4 | 4 | - | - |
| Quiz | Wording and possible misreadings | 5 | 5 | - | - |
| Quiz | Writing quality | 4 | 5 | - | - |
| Quiz | Alignment with the learning goal | 4 | 4 | - | - |
| Feedback | Useful | 5 | 5 | - | - |
| Feedback | Explains enough | 4 | 5 | - | - |
| Feedback | Personalized to how I like things explained | 5 | 5 | - | - |
| Tutor | Guardrails | 4 | - | - | - |
| Tutor | Personalization | 4 | - | - | - |

## The ablation

Each `final-minus-*` config's latest scored run on agent-architecture at 30 minutes (not a quick run) beside `final`'s scored full runs, for the jobs that run covered; each cell is the mean over the runs, with the range in brackets.

### `final-minus-clarity-checker`

#### Quality

| config | runs | teach facts | teach misconc. | length ratio | dead links |
|---|---:|---:|---:|---:|---:|
| `final` | 2 | 0.83 | 0 | 1.10 (1.03-1.18) | 0 |
| `final-minus-clarity-checker` | 1 | 1.00 | 0 | 1.00 | 0 |

`final-minus-clarity-checker` was run with --only and covers only these scenarios: teach; its costs add up only those, while the costs of `final` add up every scenario of each job.

#### Cost: teach

| config | runs | tokens | output tokens | minutes | subagents | list-price $ |
|---|---:|---:|---:|---:|---:|---:|
| `final` | 2 | 3.57M (3.50M-3.65M) | 158.2k (112.3k-204.1k) | 24.1 (11.7-36.6) | 7 (6-8) | 3.02 (2.42-3.62) |
| `final-minus-clarity-checker` | 1 | 2.33M | 102.0k | 10.6 | 4 | 1.97 |

Costs are per run, summed over the job's scenarios; list-price $ is the list-price equivalent, not what you pay on a subscription.

## Lesson length

Scored teach-only runs; each cell is the mean over the runs, with the range in brackets.

### Quality

| config | minutes | runs | teach facts | teach misconc. | length ratio | dead links |
|---|---:|---:|---:|---:|---:|---:|
| `c1-skills` | 10 | 3 | 0.89 (0.83-1.00) | 0 | 0.95 (0.94-0.96) | 0 |
| `c1-skills` | 30 | 3 | 1.00 | 0 | 0.94 (0.81-1.07) | 0 |
| `c1-skills` | 60 | 3 | 1.00 | 0 | 0.82 (0.80-0.85) | 0 |
| `final-minus-clarity-checker` | 30 | 1 | 1.00 | 0 | 1.00 | 0 |

Teach facts, key agreement, verdict agreement, false wrong, misconception hit and behavior met are shares (0 to 1); misconceptions, dead links, wrong keys, ambiguous items and leaks are counts per run.
A dash means no run could be scored on that check, and n= says how many of the runs could.
A job that failed counts against the config: no lesson scores 0 teach facts, no quiz and key 0 key agreement, a missing grades file disagrees on every item, and a tutor scenario with no reply is not met; leaks need a reply to check, so such a scenario is left out of them.
The length ratio is a rough reading-time estimate (visible words / 150) over the minutes requested; 0.6 to 1.5 counts as on length.

### Cost: teach

| config | minutes | runs | tokens | output tokens | minutes | subagents | list-price $ |
|---|---:|---:|---:|---:|---:|---:|---:|
| `c1-skills` | 10 | 3 | 735.7k (606.4k-939.1k) | 18.0k (16.7k-20.5k) | 2.0 (1.8-2.3) | 0 | 0.49 (0.43-0.59) |
| `c1-skills` | 30 | 3 | 1.05M (924.5k-1.11M) | 33.7k (29.9k-35.9k) | 3.7 (3.1-4.0) | 0 | 0.72 (0.61-0.81) |
| `c1-skills` | 60 | 3 | 1.36M (1.13M-1.81M) | 46.3k (43.4k-48.6k) | 5.2 (4.8-5.5) | 0 | 0.93 (0.86-1.05) |
| `final-minus-clarity-checker` | 30 | 1 | 2.33M | 102.0k | 10.6 | 4 | 1.97 |

### Cost: all jobs

| config | minutes | runs | tokens | output tokens | minutes | subagents | list-price $ |
|---|---:|---:|---:|---:|---:|---:|---:|
| `c1-skills` | 10 | 3 | 735.7k (606.4k-939.1k) | 18.0k (16.7k-20.5k) | 2.0 (1.8-2.3) | 0 | 0.49 (0.43-0.59) |
| `c1-skills` | 30 | 3 | 1.05M (924.5k-1.11M) | 33.7k (29.9k-35.9k) | 3.7 (3.1-4.0) | 0 | 0.72 (0.61-0.81) |
| `c1-skills` | 60 | 3 | 1.36M (1.13M-1.81M) | 46.3k (43.4k-48.6k) | 5.2 (4.8-5.5) | 0 | 0.93 (0.86-1.05) |
| `final-minus-clarity-checker` | 30 | 1 | 2.33M | 102.0k | 10.6 | 4 | 1.97 |

Costs are per run, summed over the job's scenarios; list-price $ is the list-price equivalent, not what you pay on a subscription.
