# Agent architecture Resources

## Knowledge

- [Article: "Effective context engineering for AI agents" (Anthropic Engineering)](https://anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  Attention budget, just-in-time retrieval, compaction, note-taking, sub-agents. Use for: anything about what to keep in context and how to manage it.
- [Docs: "Context windows" (Claude docs)](https://platform.claude.com/docs/en/build-with-claude/context-windows)
  What counts toward the window, how turns accumulate, context rot, compaction. Use for: precise facts about the window and tokens.
- [Article: "Contextual Retrieval" (Anthropic)](https://anthropic.com/research/contextual-retrieval)
  Chunking, embeddings, BM25 and reranking for long documents. Use for: designing manual search.
- [Docs: "Memory tool" (Claude docs)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
  File-based memory across sessions. Use for: notes between sessions.
- [Paper: "Lost in the Middle: How Language Models Use Long Contexts" (Liu et al.)](https://Huggingface.co/papers/2307.03172)
  Evidence that models use the middle of long inputs less well. Use for: why not to stuff the window.

## Wisdom (Communities)

- None added yet. Surface a community for agent builders in a later lesson.

## Gaps

- A beginner-friendly source on first calling a model from Python.
