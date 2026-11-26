# Agent architecture Resources

## Knowledge

- [Article: "Effective context engineering for AI agents" (Anthropic Engineering)](https://anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  Defines context, context rot, just-in-time retrieval, compaction, structured note-taking and sub-agents. Use for: what to keep in context, what to save outside it.
- [Docs: Context windows (Claude Platform)](https://platform.claude.com/docs/en/build-with-claude/context-windows)
  Context window as working memory, how turns accumulate, what counts toward the limit, overflow behaviour. Use for: how big the context gets and why cost grows.
- [Docs: Memory tool (Claude Platform)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
  File-based memory that the application runs and that persists across conversations. Use for: designing what the assistant saves between sessions.
- [Article: "Introducing Contextual Retrieval" (Anthropic)](https://www.anthropic.com/engineering/contextual-retrieval)
  How chunking, embeddings and keyword search find the right passage in a long document set. Use for: finding the right page in a long manual.
- [Paper: "Lost in the Middle: How Language Models Use Long Contexts" (Liu et al., TACL 2024)](https://aclanthology.org/2024.tacl-1.9.pdf)
  Accuracy is highest when relevant text is at the start or end of the input. Use for: why stuffing a whole manual into context is risky.

## Wisdom (Communities)

No community has been vetted yet; add one once the learner has a prototype to share.

## Gaps

- A vetted community for agent builders (to be added after the learner has a prototype).
