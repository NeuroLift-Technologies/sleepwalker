# Claude Code — Governance Framing Restoration

**Date:** 2026-05-28
**Agent:** Claude Code (Opus 4.7)
**Repository:** NeuroLift-Technologies/sleepwalker
**Supersedes:** PR #4 (this PR) — restoration over Copilot PR #2 baseline (`copilot/update-governance-templates`)

## Summary

Restores org-level governance framing that the Copilot baseline (merged as PR
#2) over-trimmed. The Copilot PR ran a global find/replace from
`.github-private` to `sleepwalker` in every governance doc. That was correct
for *repo-local* artifacts (this repo's `.nltotoi/` namespace, this repo's
`nltotoi.json` `name` field, validator `check_content`) but it destroyed the
org-architecture references in:

- `NLT-DEV-OTOI.md` (the canonical org contract — must say "Organization-Wide")
- `AGENTS.md` (org-wide internal gateway, fallback access block, file map header)
- `file-structure.md` (describes the 3-tier org architecture)
- `SOPs/incident-response.md` (template path inside `.github-private`)
- `SOPs/new-agent-onboarding.md` (canonical contract source-of-truth URLs)
- `agents/nlt-governance-steward.md` (canonical contract location)
- `docs/agent-log/README.md` (template format reference)
- `docs/escalations/README.md` (template format reference)

## What this PR does

Starts from `main` (post-merge of Copilot PR #2 at `797fa80`) and reverts the
incorrect portions while keeping the *correct* parts of the Copilot baseline:

| Kept from Copilot PR #2 (correct repo-local scoping) | Why |
|---|---|
| `CLAUDE.md` URLs scoped to `sleepwalker` | OTOI / AGENTS.md ship in this repo |
| `.nltotoi/README.md` scoped to local repo | This namespace IS local |
| `.nltotoi/index/governance-files.md` scoped to local repo | This index IS local |
| `.nltotoi/proposals/validation-roadmap.md` scoped to local repo | This roadmap IS local |
| `.nltotoi/scripts/validate-governance.sh` check_content for local repo name | Validator must match the local manifest |
| `nltotoi.json` `repository.name` → `sleepwalker` | This manifest IS local |

| Added in this PR | Why |
|---|---|
| `README.md` — `ai_assistant_directive` YAML block | Points agents at OTOI before any work |
| `SOPs/repo-governance-setup.md` upgraded v1.0.0 → v1.1.0 from `.github-private` | Gains `.claude/` provisioning + governance-auto-propagate section |
| `nltotoi.json` `last_updated` → `2026-05-28` | Reflects this update |
| `docs/agent-log/2026-05-28-claude-governance-restoration.md` — this audit log | Trail |

## What this PR reverts (back to pre-Copilot state)

- `NLT-DEV-OTOI.md` — restored org-wide framing (Repository: `.github-private`)
- `AGENTS.md` — restored org-wide gateway, fallback access block, file map header
- `file-structure.md` — restored 3-tier architecture description (`.github-private` references intact)
- `SOPs/incident-response.md` — restored canonical template-path references
- `SOPs/new-agent-onboarding.md` — restored canonical contract source-of-truth URLs
- `agents/nlt-governance-steward.md` — restored canonical contract location
- `docs/agent-log/README.md` — restored canonical template reference
- `docs/escalations/README.md` — restored canonical template reference
- `nltotoi.json` `ethical_framework.public_governance` URL preserved (was never changed in PR #2)
- `nltotoi.json` `repository.purpose` preserved (was never changed in PR #2)
- `nltotoi.json` `visibility: private` preserved

## Validation

`bash .nltotoi/scripts/validate-governance.sh` must pass post-merge.

## Authority

Joshua W. Dorsey, Sr. — `info@neuroliftsolutions.com`
