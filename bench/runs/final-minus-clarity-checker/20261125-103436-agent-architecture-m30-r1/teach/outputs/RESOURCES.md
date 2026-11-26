# Agent architecture Resources

## Knowledge

- [Article: "Effective context engineering for AI agents" (Anthropic Engineering, Sep 2025)](https://anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  Primary source for O3. Defines context, context rot and the attention budget, just-in-time retrieval vs preloading, compaction, structured note-taking and sub-agents. Use for: what to keep in context and why smaller is better.
- [Article: "Managing context on the Claude Developer Platform" (Anthropic)](https://www.anthropic.com/news/context-management)
  Context editing (clears stale tool results from the live context) vs the memory tool (storage outside the window that survives sessions). Use for: the difference between within-session and between-session memory.
- [Docs: Memory tool (Claude Platform Docs)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
  Files under /memories, commands view/create/str_replace/insert/delete/rename, run by your own application. Use for: how notes-as-memory works in code.
- [Article: "Contextual Retrieval" (Anthropic Research)](https://anthropic.com/research/contextual-retrieval)
  RAG, chunking, why a chunk needs context, and the advice to skip retrieval for small knowledge bases (under about 200,000 tokens). Use for: finding the right page in a long manual.

## Wisdom (Communities)

- [LangChain forum](https://forum.langchain.com/t/building-reliable-ai-agent-workflows-with-langgraph-and-rag/4945)
  Practitioners discuss agent workflows, retrieval and memory choices. Use for: asking how others handle retrieval and memory for a document-answering assistant.

## Gaps

- A beginner-level, framework-neutral source on token counting and per-request cost; needed for the cost side of the mission.
