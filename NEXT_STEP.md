# DharmaAI — Next Session Handoff

Project root:
`/mnt/kaliyuga/DharmaAI`

Python environment:
`~/ai-lab/venv`

Latest known regression result:
`logs/test_runner.status` recorded PASS.
`logs/test_runner.log` reported 6 test groups, 0 failures,
and 4 agent tests passed.

Current architecture:
- Brain: `brain/engine.py`, `brain/router.py`,
  `brain/ollama_client.py`
- Memory: `memory/manager.py`, `memory/context.py`,
  `memory/long_term.py`, `memory/short_term.py`, `memory/store.py`
- Agents: `agents/manager.py` and individual agent modules
- Config: `config/settings.py`

NEXT TASK:
Audit existing agent interfaces, logger, settings, and test patterns.
Then implement a modular Agent Orchestrator without replacing the
existing BrainEngine, MemoryManager, or AgentManager APIs.

Required orchestrator features:
1. Represent tasks and steps explicitly.
2. Plan and execute one step at a time.
3. Select registered agents using existing interfaces.
4. Record each step's status and output.
5. Enforce timeouts and controlled permissions.
6. Log decisions and errors.
7. Verify results and test failure paths.
8. Back up modified source files before edits.

Do not claim the orchestrator is complete until tests pass.
After implementation, update this file with actual results and the
next unfinished task.

For a new chat, paste this handoff and the latest test log/status.

## Latest milestone: Agent Orchestrator V1

- Added `core/orchestrator.py`.
- Added `tests/test_orchestrator.py`.
- Supports agent selection, a one-step task plan, approval gating,
  structured execution results, and JSONL audit logging.
- This is a first-generation single-step orchestrator, not yet
  a multi-step autonomous planner.
- The approved execution path still delegates to existing agents;
  do not treat approval as a sandbox. Harden ShellAgent and FileAgent
  before enabling untrusted or autonomous execution.
- Focused and regression tests passed in the latest recorded run.

NEXT:
1. Review and harden ShellAgent against shell injection.
2. Restrict FileAgent paths to the workspace.
3. Add permission policy and explicit confirmation boundaries.
4. Implement multi-step plans with per-step verification.

## Planner V1 / Multi-step Orchestrator

- Added `core/planner.py` for explicit ordered task plans.
- Extended `core/orchestrator.py` with `run_plan()`.
- Each step records agent, status, output/error, and timestamps.
- Execution stops at the first failure or approval gate.
- Audit records are written to the configured JSONL audit path.
- Planner tests cover ordering, invalid plans, approvals, failures,
  and audit logging.
- This version executes user-specified steps; it does not yet
  autonomously infer and validate a plan from an arbitrary goal.
- Passing tests do not constitute a full security sandbox.

NEXT:
1. Update `run_tests.sh` to include all new test modules.
2. Add stronger output verification and step dependency handling.
3. Add resource limits and execution timeouts for all agents.
4. Integrate MemoryManager for task context and verified outcomes.
5. Design an optional model-assisted planner with strict validation.
