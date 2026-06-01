# Active Threads — sleepwalker

> This file tracks active work threads. Agents must read this at session start and update it during and at the end of each session.

**Last updated:** 2026-06-01

---

## Active Threads

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

*(None yet)*
