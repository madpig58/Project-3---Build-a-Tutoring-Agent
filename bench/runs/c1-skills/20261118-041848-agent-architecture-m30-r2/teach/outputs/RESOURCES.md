# Agent architecture Resources

## Knowledge

- [Article: "Effective context engineering for AI agents" (Anthropic Engineering)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  Context as a finite resource, context rot, just-in-time retrieval, compaction, note-taking, sub-agents. Use for: what to keep in context and why smaller is often better. Primary source for lesson 0001-context-and-memory.
- [Docs: Context windows (Claude Platform)](https://platform.claude.com/docs/en/build-with-claude/context-windows)
  What counts toward the window, how turns accumulate, compaction and context editing. Use for: exact mechanics of the window and what happens when it fills.
- [Docs: Memory tool (Claude Platform)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
  A client-side file store the model reads and writes through tool calls, plus the multisession pattern and security notes. Use for: designing what the assistant saves between sessions.
- [Blog post: "LLM Powered Autonomous Agents" by Lilian Weng](https://lilianweng.github.io/posts/2023-06-23-agent)
  Overview of agent parts, including short-term and long-term memory with an external store and fast retrieval. Use for: the vocabulary of memory types. Seen only as search-result excerpts so far.

## Wisdom (Communities)

- Local: the learner's senior design team, their course instructor and the makerspace staff.
  Use for: testing the memory design against real student questions and the real manuals. No online community has been verified yet.

## Gaps

- A high-trust, moderated online community for building agents (to be found and verified by search in a later session).
- A source on cost per request for long contexts that fits the sponsor's small budget (check the pricing page of whichever model the team picks).
