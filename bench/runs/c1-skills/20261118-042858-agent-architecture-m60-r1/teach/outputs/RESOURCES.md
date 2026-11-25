# Agent architecture Resources

## Knowledge

- [Anthropic: Effective context engineering for AI agents](https://anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  Context rot, pre-retrieval vs just-in-time retrieval, compaction, note-taking, sub-agents. Use for: what to keep in context and how to manage long tasks.
- [Claude docs: Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)
  What counts toward the window, how history accumulates, compaction and context editing. Use for: token accounting and cost.
- [Claude docs: Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool.md)
  Client-side file memory, commands, security duties, multisession pattern. Use for: designing saved notes.
- [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents)
  Retrieval, tools and memory as the building blocks of an agent, and the advice to keep designs simple. Use for: choosing an architecture.

## Wisdom (Communities)

- [Letta community forum](https://forum.letta.com/)
  Forum for builders of agents with memory. Use for: asking for critique of a memory design.

## Gaps

- No high-trust source yet on evaluating retrieval quality for a small manual library.
