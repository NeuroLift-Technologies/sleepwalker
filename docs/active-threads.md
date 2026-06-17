# Active Threads — sleepwalker

> This file tracks active work threads. Agents must read this at session start and update it during and at the end of each session.

**Last updated:** 2026-06-17

---

## Active Threads

### Governance fork #4 vs #5 (Task A — diagnosis only)
- **Agent:** Claude Code — read-only diagnosis for Joshua.
- **Status:** AWAITING JOSHUA'S DECISION. Do not merge or modify the contested files.
- **Finding:** PR #5 (`claude/governance-docs-restore-yB5sI`) is **divergent** from PR #4
  (`governance/otoi-compliance`), not a superset — the two move in opposite directions
  on the same governance docs. Diagnosis delivered in the session report; no merge
  recommended.

---

## Resolved Threads

### Thread: 2026-06-17-docs-automation-pr15
**Status:** resolved
**Owner:** Cursor Automation GPT-5.5
**Started:** 2026-06-17
**Last updated:** 2026-06-17
**Summary:** Documentation automation reviewed merged PR #15, found remaining source-verified developer and governance-inventory doc gaps, and updated non-contested docs for Python continuity persistence, TypeScript exports and continuity constraints, contributor tooling caveats, examples guidance, and validator/manifest alignment.
**Blockers:** None.
**Next action:** Review the documentation PR. The active governance fork thread remains unresolved, so contested governance files were not modified.

### Thread: 2026-06-01-continuity-user-id-fix
**Status:** resolved
**Owner:** Claude Code
**Started:** 2026-06-01
**Last updated:** 2026-06-17
**Summary:** `assess_interaction` now keys continuity on a stable user id instead of message text. The fix is present on `main`, with `user_id` support in `SWP.__init__` and `assess_interaction`, hash-backed continuity filenames, and behavioral coverage for repeated assessments.
**Blockers:** None.
**Next action:** Use the documented stable `user_id` and `maintain_continuity()` pattern in future Python examples and integrations.

### Thread: 2026-06-17-docs-follow-up-pr14
**Status:** resolved
**Owner:** Cursor Automation GPT-5.5
**Started:** 2026-06-17
**Last updated:** 2026-06-17
**Summary:** Documentation automation aligned developer and operations docs with PR #14 by adding the missing agent context page, documenting TypeScript package build/test/publish checks, correcting Python/TypeScript usage examples, and clarifying the current governance validator scope.
**Blockers:** None.
**Next action:** Review the documentation PR and decide whether dependency audit warnings or Python/npm license metadata drift need a separate maintainer-directed follow-up.

### Thread: 2026-05-22-docs-governance-inventory
**Status:** resolved
**Owner:** Cursor Automation GPT-5.5
**Started:** 2026-05-22
**Last updated:** 2026-05-22
**Summary:** Documentation automation is aligning governance inventory and operational docs with the source-verified `sleepwalker` repository contents after PR #2 made governance artifacts repository-specific.
**Blockers:** None.
**Next action:** Review the documentation PR and decide whether roadmap items should become implemented governance automation.
