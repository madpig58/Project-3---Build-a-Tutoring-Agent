# Agent architecture Resources

## Knowledge

- [Article: "Effective context engineering for AI agents" (Anthropic Engineering)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  Defines context, context rot, just-in-time retrieval, compaction, structured note-taking and sub-agents. Use for: anything about what an agent keeps in its context and how to keep it small.
- [Docs: "Memory" concepts (LangChain)](https://docs.langchain.com/oss/python/concepts/memory)
  Short-term (thread) versus long-term (cross-session) memory, semantic/episodic/procedural types, writing memory in the hot path or in the background. Use for: deciding what the assistant saves between sessions and when it writes it.
- [Article: "Introducing Contextual Retrieval" (Anthropic)](https://www.anthropic.com/news/contextual-retrieval)
  Chunking, embeddings, BM25, why chunks lose context, and when to skip retrieval and put a small knowledge base in the prompt. Use for: finding the right page in a long manual.
- [Article: "Building effective agents" (Anthropic)](https://www.anthropic.com/research/building-effective-agents)
  The augmented model (retrieval, tools, memory) as the basic building block, and advice to keep systems simple. Use for: workflows versus agents, and choosing the simplest design (note: written December 2024, and its header says some tooling has since changed).

## Wisdom (Communities)

No community has been added yet. Riley has not said whether they want one; ask before proposing any.
