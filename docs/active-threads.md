# Active Threads — sleepwalker

> This file tracks active work threads. Agents must read this at session start and update it during and at the end of each session.

**Last updated:** 2026-11-22

---

## Active Threads

### Thread: 2026-11-22-codex-sleepwalker-archive
**Status:** pending review
**Owner:** Codex
**Branch:** `codex/retire-sleepwalker-archive`
**Task:** Retire the Sleepwalker archive and reconcile the work tracker.
**Scope:** The two tracked archive files and repository coordination records.
**Related PR:** Pending.
**Started:** 2026-11-22
**Last updated:** 2026-11-22
**Next action:** Review the archive retirement PR.

---

## Resolved Threads

### TS port security parity
- **Agent:** Claude Code, session `2026-06-23-harden-ts-continuity`
- **Status:** [PR #25](https://github.com/NeuroLift-Technologies/sleepwalker/pull/25) merged on 2026-06-25. The published [npm 1.0.2 package](https://www.npmjs.com/package/@neurolift-technologies/sleepwalker-protocol/v/1.0.2) contains the patched continuity and protocol modules.
- **Summary:** Aligned TypeScript continuity file naming and user identity handling with the Python implementation, and aligned package license metadata.

### Governance fork #4 vs #5
- **Agent:** Claude Code
- **Status:** [PR #5](https://github.com/NeuroLift-Technologies/sleepwalker/pull/5) merged on 2026-06-03. [PR #4](https://github.com/NeuroLift-Technologies/sleepwalker/pull/4) closed without merging.
- **Summary:** The two branches took different approaches to restoring repository governance files.

### Cleanup: archive legacy artifacts
- **Agent:** SWE, session `2026-07-31-cleanup-sleepwalker-legacy-archive`
- **Branch:** `cleanup/sleepwalker-legacy-archive`
- **Status:** [PR #29](https://github.com/NeuroLift-Technologies/sleepwalker/pull/29) merged on 2026-07-31.
- **Summary:** Documented deprecated flat-layout build artifacts. The [archived migration note](https://github.com/NeuroLift-Technologies/sleepwalker/blob/137c1eac1578455007614021531346c44d920ab9/legacy/DEPRECATED.md) remains available in Git history.

### Thread: 2026-06-17-docs-follow-up-pr14
**Status:** resolved
**Owner:** Cursor Automation GPT-5.5
**Started:** 2026-06-17
**Last updated:** 2026-06-17
**Summary:** Documentation automation aligned developer and operations docs with PR #14 by adding the missing agent context page, documenting TypeScript package build/test/publish checks, correcting Python/TypeScript usage examples, and clarifying the current governance validator scope.
**Blockers:** None.
**Next action:** Review the documentation PR and decide whether dependency audit warnings or Python/npm license metadata drift need a separate maintainer-directed follow-up.

### Thread: 2026-06-01-continuity-user-id-fix
**Status:** resolved
**Owner:** Claude Code
**Started:** 2026-06-01
**Last updated:** 2026-07-31
**Summary:** `assess_interaction` keyed continuity on the message text instead of a
  stable user id, so continuity always returned "no history". Threaded a real
  `user_id` through `SWP.__init__` and `assess_interaction`; added two behavioral
  tests (second assessment for the same user now sees the first's context).
  Merged via PR. No further follow-up needed.
**Blockers:** None.
**Next action:** None.

### Thread: 2026-05-22-docs-governance-inventory
**Status:** resolved
**Owner:** Cursor Automation GPT-5.5
**Started:** 2026-05-22
**Last updated:** 2026-05-22
**Summary:** Documentation automation is aligning governance inventory and operational docs with the source-verified `sleepwalker` repository contents after PR #2 made governance artifacts repository-specific.
**Blockers:** None.
**Next action:** Review the documentation PR and decide whether roadmap items should become implemented governance automation.
