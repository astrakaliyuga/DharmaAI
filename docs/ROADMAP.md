# DharmaAI Project Roadmap

## Current verified baseline
- Local Ollama inference works.
- Models: qwen2.5:1.5b, qwen2.5:7b, gemma2:9b.
- Brain engine and complexity-based router tests pass.
- ChromaDB long-term retrieval and memory-aware brain tests pass.
- JSONL structured memory and short-term memory modules exist.
- Seven agents are registered: Web, Voice, Image, Video, File,
  Shell, and Code.
- Latest recorded regression suite: 6 groups passed, 0 failures.
- Project root: /mnt/kaliyuga/DharmaAI.

## Development sequence

1. Continuity, source backup, and project audit.
2. Agent Orchestrator:
   - explicit task and step data structures
   - task planning and agent selection
   - execution state and timeouts
   - permission checks before sensitive operations
   - audit logging and result verification
3. Integrate MemoryManager into task planning and execution.
4. Add unit and integration tests for orchestration.
5. Improve safe file and shell tool boundaries.
6. Add resource-aware scheduling for this laptop.
7. Integrate voice, vision, and creative agents through tested interfaces.
8. Add evaluation, failure recovery, backups, and rollback.
9. Add a unified user interface and persistent session history.
10. Repeatedly evaluate capability, reliability, privacy, and security.

## Engineering rules
- Back up files before modifying them.
- Do not delete existing memories or models during routine development.
- Run focused tests after each change and the regression suite afterward.
- Never report a test as passed without its output.
- Require approval for destructive, privileged, external, or
  security-sensitive actions.
- Keep an honest distinction between demonstrated capability and aspiration.
- ASI is a long-term aspiration, not a guaranteed outcome.
