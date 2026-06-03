# Governance File Index — NeuroLift Technologies `sleepwalker`

**Last updated:** 2026-06-03
**Maintained by:** `.nltotoi/` namespace tooling  
**Scope:** `NeuroLift-Technologies/sleepwalker`

---

## Inventory Scope

This index is the human-readable registry for governance-adjacent files in this
repository. It is broader than the CI-required file list:

- `nltotoi.json` `required_files` is the machine-readable minimum contract.
- `.nltotoi/scripts/validate-governance.sh` is the executable CI check and
  currently mirrors the `required_files` minimum.
- This index also tracks coordination records, troubleshooting docs, agent
  profiles, and agent tooling so reviewers can understand the full operating
  surface.

`Required` in the tables below means the file is required for the documented
`sleepwalker` governance operating model. If a file must also be enforced by
CI, add it to both `nltotoi.json` and `validate-governance.sh`.

---

## Core Governance Files

| File | Type | Purpose | Required |
|---|---|---|---|
| `NLT-DEV-OTOI.md` | Contract | Org-level coding agent contract (ORG-DEV-OTOI-1.0.0) | ✅ |
| `AGENTS.md` | Gateway | Internal agent coordination gateway | ✅ |
| `nltotoi.json` | Manifest | Machine-readable discovery manifest | ✅ |
| `README.md` | Overview | Repository overview and purpose | ✅ |
| `file-structure.md` | ADR | Architecture decision record for this repo structure | ✅ |
| `CLAUDE.md` | Instructions | Agent session instructions and plan | ✅ |

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
| `agents/nlt-governance-steward.md` | Governance steward agent — enforces ORG-DEV-OTOI-1.0.0 | ✅ |

---

## Agent Tooling References

| File | Purpose | Required |
|---|---|---|
| `links.md` | Curated links for agent skills, Cloudflare MCP references, and platform docs | ✅ |
| `mcp-config.yaml` | Example MCP host configuration for GitHub and Cloudflare remote MCP servers | ✅ |

These files are operational references for agents, not active CI gates. Keep
secret values in environment variables only; do not commit `.env` files.

---

## Agent Coordination Records

| File or directory | Purpose | Required |
|---|---|---|
| `docs/active-threads.md` | Tracks active and resolved work threads | ✅ |
| `docs/agent-log/README.md` | Explains registration and handoff directories | ✅ |
| `docs/agent-log/intent/README.md` | Explains intent-log storage convention | ✅ |
| `docs/escalations/README.md` | Explains escalation record storage | ✅ |
| `docs/troubleshooting/github-app-access.md` | Explains GitHub App access requirements for private governance files | ✅ |

---

## Roadmap / Not Yet Present

The following workflow and agent-profile families are referenced by SOPs or roadmap
discussion but are not present in this repository as of 2026-06-03:

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
| Core governance | 6 |
| .nltotoi namespace | 5 |
| Templates | 5 |
| GitHub templates | 3 |
| CI workflows | 1 |
| SOPs | 3 |
| Agent profiles | 1 |
| Agent tooling references | 2 |
| Agent coordination records | 5 |
| **Total** | **31** |

---

*Generated from `.nltotoi/index/governance-files.md` | NeuroLift Technologies | ORG-DEV-OTOI-1.0.0*
