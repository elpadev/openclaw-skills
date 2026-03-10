---
name: codex-cli-complex-coding
description: Use ACP/Codex sessions for complex coding work instead of quick inline edits. Trigger when tasks involve multi-file refactors, architecture changes, migration plans, test-driven changes, debugging loops, or any repo task where iterative coding + validation is needed.
---

# Codex CLI Complex Coding

Use this skill when coding tasks are large enough that direct one-shot edits are risky.

## Workflow

1. Confirm scope and success criteria in one short plan.
2. Start an ACP Codex session for the task.
3. Keep all implementation work in that ACP session.
4. Run checks/tests in the target repo.
5. Summarize changes, risks, and next steps.

## ACP session defaults

For coding tasks, prefer:

- `runtime: "acp"`
- `agentId: "codex"` (or the configured Codex ACP agent)
- `thread: true`
- `mode: "session"`

Use `mode: "run"` only for very small one-off code tasks.

## Execution pattern

- Start with a concise implementation plan.
- Ask Codex to:
  - inspect relevant files,
  - implement in small commits/patches,
  - run project checks (lint/test/build),
  - report exact files changed.
- If checks fail, iterate in the same ACP thread until green (or blocked with explicit reason).

## Quality guardrails

- Prefer minimal, reversible diffs.
- Do not change unrelated files.
- Preserve existing style and conventions.
- Add or update tests when behavior changes.
- Include rollback notes for risky migrations.

## Output format

Return:

1. What changed (short)
2. Validation run (commands + result)
3. Open risks/blockers
4. Suggested follow-up
