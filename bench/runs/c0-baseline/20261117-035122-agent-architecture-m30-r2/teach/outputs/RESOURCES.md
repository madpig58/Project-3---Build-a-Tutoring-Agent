# Agent architecture Resources

## Knowledge

- [Article: "Effective context engineering for AI agents" (Anthropic Engineering)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  Context as a finite resource, context rot, up-front vs just-in-time retrieval, compaction, note-taking, sub-agents. Use for: anything about what goes in the context and how to keep it small.
- [Docs: "Context windows" (Claude docs)](https://platform.claude.com/docs/en/build-with-claude/context-windows)
  How context accumulates across turns, what counts toward the window, compaction and context editing. Use for: how history is re-sent each call, and token accounting.
- [Article: "Building effective agents" (Anthropic Engineering)](https://www.anthropic.com/engineering/building-effective-agents)
  The augmented model (retrieval, tools, memory) and workflows vs agents. Use for: the workflow-vs-agent and multi-agent lessons. Notes that parts of its tooling landscape are dated (December 2024).

## Wisdom (Communities)

- [LlamaIndex community forum](https://community.llamaindex.ai/current-and-planned-memory-for-ai-agents-in-llamaindex-Pyq9VpcttfsN)
  Builders discussing memory and retrieval for agents. Use for: design questions about retrieval and memory once the learner has a prototype.

## Gaps

- A high-trust, moderated community specifically for agent design (not just a framework's users) has not been found.
