# Agent architecture Resources

## Knowledge

- [Article: "Effective context engineering for AI agents" (Anthropic Engineering)](https://anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  Context rot, compaction, structured note-taking, just-in-time retrieval, sub-agents. Use for: anything about what an agent keeps in context and saves outside it.
- [Docs: Context windows (Claude Platform)](https://platform.claude.com/docs/en/build-with-claude/context-windows)
  What counts toward the window, how turns accumulate, compaction and context editing. Use for: token accounting and cost per call.
- [Article: "Contextual Retrieval" (Anthropic)](https://anthropic.com/news/contextual-retrieval)
  Chunks, embeddings, BM25, the 200,000-token "just paste it" threshold and retrieval failure rates. Use for: designing manual search.
- [Docs: Memory tool (Claude Platform)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
  A tool for saving and loading notes across sessions. Linked from the context-windows page; not yet read in full. Use for: per-student notes.

## Wisdom (Communities)

- Local: the learner's design team, course instructors and teaching assistants.
  Use for: design-review critique of what goes in context, notes or retrieval.

## Gaps

- No vetted community for agent builders yet; find a moderated forum for later lessons.
