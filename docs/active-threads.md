# Active Threads — sleepwalker

> This file tracks active work threads. Agents must read this at session start and update it during and at the end of each session.

**Last updated:** 2026-06-23

---

## Active Threads

### TS port security parity (hash user_id filenames + key continuity on user_id)
- **Agent:** Claude Code — session `2026-06-23-harden-ts-continuity`
- **Branch:** `claude/harden-ts-continuity` (own branch + draft PR)
- **Status:** Implemented, tests passing (jest 29 passed; tsc clean; pytest 46 passed). Draft PR open for Joshua's review.
- **Summary:** Brought the published `@neurolift-technologies/sleepwalker-protocol`
  TS port to parity with the already-fixed Python code: `src/continuity.ts` wrote a
  raw `${userId}.json` filename (a `../` escape — a **live path-traversal exposure in
  the published package**), now SHA-256-hashes the user_id for the on-disk filename
  (mirrors `ContinuityManager._user_file`); `src/protocol.ts` `assessInteraction` now
  keys continuity on a stable `user_id` instead of ignoring continuity entirely.
  Also aligned Python license metadata (`pyproject.toml`, `__init__.py`) MIT -> Apache-2.0
  to match LICENSE + package.json.
- **Follow-up (Joshua):** npm version bump + republish of the patched package needs
  Joshua's 2FA OTP + sign-off — **not** done in this session.

### Continuity user_id fix (Task B)
- **Agent:** Claude Code — session `2026-06-01-continuity-fix-and-pr-diagnosis`
- **Branch:** `claude/friendly-bardeen-5kuHW` (own branch + PR)
- **Status:** Implemented, tests passing (43 passed). PR open for Joshua's review.
- **Summary:** `assess_interaction` keyed continuity on the message text instead of a
  stable user id, so continuity always returned "no history". Threaded a real
  `user_id` through `SWP.__init__` and `assess_interaction`; added two behavioral
  tests (second assessment for the same user now sees the first's context).

### Governance fork #4 vs #5 (Task A — diagnosis only)
- **Agent:** Claude Code — read-only diagnosis for Joshua.
- **Status:** AWAITING JOSHUA'S DECISION. Do not merge or modify the contested files.
- **Finding:** PR #5 (`claude/governance-docs-restore-yB5sI`) is **divergent** from PR #4
  (`governance/otoi-compliance`), not a superset — the two move in opposite directions
  on the same governance docs. Diagnosis delivered in the session report; no merge
  recommended.

---

## Resolved Threads

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
