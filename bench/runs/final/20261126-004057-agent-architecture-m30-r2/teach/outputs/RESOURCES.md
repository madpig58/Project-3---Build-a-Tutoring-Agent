# Agent architecture Resources

## Knowledge

- [Article: "Effective context engineering for AI agents" (Anthropic Engineering)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  What goes into an agent's context, context rot, compaction, note-taking and just-in-time retrieval. Use for: deciding what the assistant keeps, summarizes, writes down or fetches. Primary source for O3.
- [Docs: "Context windows" (Claude Platform)](https://platform.claude.com/docs/en/build-with-claude/context-windows)
  What counts toward the window, how a conversation grows turn by turn, what happens at the limit. Use for: tokens per request and cost.
- [Docs: "Memory overview" (LangChain)](https://docs.langchain.com/oss/python/concepts/memory)
  Thread-scoped versus long-term memory, memory types, profiles versus collections, when to write memories. Use for: what to save between sessions.
- [Article: "Contextual retrieval in AI systems" (Anthropic Engineering)](https://www.anthropic.com/engineering/contextual-retrieval)
  How retrieval works (chunks, embeddings, keyword search), when a knowledge base is small enough to skip it, and how it fails. Use for: searching long machine manuals.
- [Docs: Glossary (Claude Platform)](https://platform.claude.com/docs/en/about-claude/glossary)
  Short definitions of tokens, context window and RAG. Use for: terms.

## Wisdom (Communities)

- [Hugging Face Agents Course: Discord guide](https://huggingface.co/learn/agents-course/en/unit0/discord101)
  A free course community with a channel for questions. Use for: asking others to critique a context and memory design.
