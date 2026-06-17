# Governance File Index — NeuroLift Technologies `sleepwalker`

**Last updated:** 2026-06-17
**Maintained by:** `.nltotoi/` namespace tooling  
**Scope:** `NeuroLift-Technologies/sleepwalker`

---

## Core Governance Files

`Required` means the file is part of the governance inventory for this
repository. Automated enforcement is narrower: CI currently runs only
`.nltotoi/scripts/validate-governance.sh`, and the machine-readable required
path list lives in `nltotoi.json`.

| File | Type | Purpose | Required |
|---|---|---|---|
| `NLT-DEV-OTOI.md` | Contract | Org-level coding agent contract (ORG-DEV-OTOI-1.0.2) | ✅ |
| `AGENTS.md` | Gateway | Internal agent coordination gateway | ✅ |
| `nltotoi.json` | Manifest | Machine-readable discovery manifest | ✅ |
| `README.md` | Overview | Repository overview and purpose | ✅ |
| `file-structure.md` | ADR | Architecture decision record for this repo structure | ✅ |
| `CLAUDE.md` | Instructions | Agent session instructions and plan | ✅ |
| `docs/context/README_TO_AI.md` | Context | Source-verified codepath and workflow guide for agents | ✅ |

---

## .nltotoi Namespace

| File | Purpose | Required |
|---|---|---|
| `.nltotoi/README.md` | Namespace overview | ✅ |
| `.nltotoi/index/governance-files.md` | This file — governance registry | ✅ |
| `.nltotoi/contracts/README.md` | Contract namespace and versioning | ✅ |
| `.nltotoi/scripts/validate-governance.sh` | Automated compliance validation | ✅ |
| `.nltotoi/proposals/validation-roadmap.md` | Planned validation improvements | ✅ |

---

## Templates

| File | Purpose | Source |
|---|---|---|
| `templates/agent-registration.json` | Agent self-registration format | OTOI Section 3 |
| `templates/handoff-record.json` | Session handoff format | OTOI Section 5 |
| `templates/escalation.md` | Escalation record format | OTOI Section 4.3 |
| `templates/intent-log.md` | Intent logging before action | OTOI Section 7 |
| `templates/commit-message.md` | Commit message format reference | OTOI Section 4.2, SOP-NLT-001 Step 7 |

---

## GitHub Templates

| File | Purpose |
|---|---|
| `ISSUE_TEMPLATE/agent-escalation.md` | GitHub issue form for agent escalations |
| `ISSUE_TEMPLATE/governance-proposal.md` | GitHub issue form for OTOI amendment proposals |
| `PULL_REQUEST_TEMPLATE/agent-contribution.md` | Agent PR checklist with governance requirements |

---

## CI Workflows

| File | Purpose | Trigger | SOP |
|---|---|---|---|
| `.github/workflows/validate-governance.yml` | Governance validation (runs validate-governance.sh) | push, pull_request | SOP-NLT-002 |

---

## Agent Profiles

| File | Purpose | Required |
|---|---|---|
| `agents/nlt-governance-steward.md` | Governance steward agent — enforces ORG-DEV-OTOI-1.0.2 | ✅ |

---

## Agent Coordination Records

| File or directory | Purpose | Required |
|---|---|---|
| `docs/active-threads.md` | Tracks active and resolved work threads | ✅ |
| `docs/agent-log/README.md` | Explains registration and handoff directories | ✅ |
| `docs/escalations/README.md` | Explains escalation record storage | ✅ |
| `docs/troubleshooting/github-app-access.md` | Explains GitHub App access requirements for private governance files | ✅ |

---

## Roadmap / Not Yet Present

The following workflow and agent-profile families are referenced by SOPs or roadmap
discussion but are not present in this repository as of 2026-06-17:

- Reusable org-wide governance checks beyond `.github/workflows/validate-governance.yml`
- Agent commit-format and handoff-gate workflows
- Automated credential scanning workflows and local hook templates
- Additional Copilot or VS Code agent profiles beyond `agents/nlt-governance-steward.md`

Track implementation work in `.nltotoi/proposals/validation-roadmap.md` and update this
index only when files land in the repository.

---

## SOPs (Standard Operating Procedures)

| File | Purpose |
|---|---|
| `SOPs/new-agent-onboarding.md` | How to onboard a new coding agent |
| `SOPs/repo-governance-setup.md` | How to add governance stubs to a new NLT repo |
| `SOPs/incident-response.md` | What to do when an agent goes off-rails |

---

## File Count Summary

| Category | Count |
|---|---|
| Core governance | 7 |
| .nltotoi namespace | 5 |
| Templates | 5 |
| GitHub templates | 3 |
| CI workflows | 1 |
| SOPs | 3 |
| Agent profiles | 1 |
| Agent coordination records | 4 |
| **Total** | **29** |

---

*Generated from `.nltotoi/index/governance-files.md` | NeuroLift Technologies | ORG-DEV-OTOI-1.0.2*
