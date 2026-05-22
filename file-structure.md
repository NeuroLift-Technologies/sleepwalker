# Architecture Decision: Public vs. Private Governance

| Layer | Repo | Audience | Purpose |
|---|---|---|---|
| **Public governance identity** | `NeuroLift-Technologies/.github` | All agents, public | Solidarity Framework principles, HAIEF attribution, org profile |
| **Private operational governance** | `NeuroLift-Technologies/sleepwalker` | Internal coding agents only | TOI-OTOI contracts, internal procedures, escalation templates, agent registration |
| **Repo-level stubs** | Each NLT repo | That repo's agents | Thin pointers to both repos above |

The key distinction: the **principles** are public, while the **operational machinery**
— escalation routing, agent registration, handoff formats, and credential-response
procedures — is private.

---

## Current `sleepwalker` Structure

This structure reflects files present in this repository as of 2026-05-22.

```text
sleepwalker/
├── AGENTS.md                         # Internal agent coordination gateway
├── CLAUDE.md                         # Repo-level agent session instructions
├── NLT-DEV-OTOI.md                   # Canonical org-level coding agent contract
├── nltotoi.json                      # Machine-readable governance manifest
├── README.md                         # SWP overview and protocol examples
├── CONTRIBUTING.md                   # Contribution and development guidance
├── file-structure.md                 # This source-verified structure note
├── links.md                          # Related project links
├── package.json                      # TypeScript package metadata and scripts
├── pyproject.toml                    # Python package metadata and tooling
├── requirements*.txt                 # Python dependency lists
│
├── sleepwalker_protocol/             # Python SWP implementation
├── src/                              # TypeScript SWP implementation
├── tests/                            # Python pytest suite
├── examples/                         # Python examples and sample TOI config
│
├── agents/
│   └── nlt-governance-steward.md     # Governance steward profile
│
├── .github/
│   └── workflows/
│       └── validate-governance.yml   # Runs governance validation on push and PR
│
├── .nltotoi/
│   ├── README.md                     # Governance namespace overview
│   ├── index/
│   │   └── governance-files.md       # Source-verified governance file index
│   ├── contracts/
│   │   └── README.md                 # Contract namespace pointer
│   ├── scripts/
│   │   └── validate-governance.sh    # Governance validation script
│   └── proposals/
│       └── validation-roadmap.md     # Planned validation improvements
│
├── templates/
│   ├── agent-registration.json       # OTOI Section 3 registration format
│   ├── handoff-record.json           # OTOI Section 5 handoff format
│   ├── escalation.md                 # OTOI Section 4.3 escalation format
│   ├── intent-log.md                 # OTOI Section 7 intent log format
│   └── commit-message.md             # Agent commit format reference
│
├── ISSUE_TEMPLATE/
│   ├── agent-escalation.md           # Escalation issue template
│   └── governance-proposal.md        # OTOI amendment proposal template
│
├── PULL_REQUEST_TEMPLATE/
│   └── agent-contribution.md         # Agent PR checklist
│
├── docs/
│   ├── active-threads.md             # Multi-agent thread tracker
│   ├── agent-log/
│   │   ├── README.md
│   │   ├── registrations/            # Session registration records
│   │   └── handoffs/                 # Session handoff records
│   ├── escalations/
│   │   └── README.md                 # Escalation record storage notes
│   └── troubleshooting/
│       └── github-app-access.md      # GitHub App access troubleshooting
│
└── SOPs/
    ├── new-agent-onboarding.md       # SOP-NLT-001
    ├── repo-governance-setup.md      # SOP-NLT-002
    └── incident-response.md          # SOP-NLT-003
```

---

## Implemented Validation Workflow

`sleepwalker` currently has one GitHub Actions workflow:

```text
.github/workflows/validate-governance.yml
```

It runs:

```bash
bash .nltotoi/scripts/validate-governance.sh
```

on `push` and `pull_request`. The script checks required governance files and content
markers. It also supports `--strict` for treating warnings as failures.

---

## Roadmap Items Not Yet Present

The repository does **not** currently include these previously discussed artifacts:

- Additional `.github/workflows/*` gates for commit format, handoff records, credential
  scanning, org-wide compliance, or agent-profile validation
- `.github/actions/*` composite actions
- `.github/agents/*` VS Code / Copilot Chat agent profiles
- `agents/README.md`, `agents/registry.json`, or additional agent profiles beyond
  `agents/nlt-governance-steward.md`
- Local secret-scanning hook templates under `agents-templates/hooks/`

When any of these are added, update `.nltotoi/index/governance-files.md`,
`nltotoi.json` if they become required, and the relevant SOP.

---

## Historical Migration Note

PR #2 updated governance artifacts that still referenced
`NeuroLift-Technologies/.github-private` so they now point to
`NeuroLift-Technologies/sleepwalker`. The current repository-specific canonical
references are:

```json
{
  "repository": {
    "name": "NeuroLift-Technologies/sleepwalker",
    "purpose": "Internal coding agent governance — TOI-OTOI operational contracts",
    "mode": "production"
  }
}
```

---

## Stub Template for NLT Repos

Each NLT repo should carry a root `CLAUDE.md` that points agents to the canonical
contract and local coordination files:

```markdown
# CLAUDE.md — [REPO NAME]

You are working in a NeuroLift Technologies repository.

**Mandatory reading (in order):**
1. Org-level governance (private, primary):
   https://github.com/NeuroLift-Technologies/sleepwalker/blob/main/NLT-DEV-OTOI.md
   Public mirror (if the link above returns 404):
   https://github.com/NeuroLift-Technologies/.github/blob/main/governance/NLT-DEV-OTOI.md
2. Internal gateway (private, primary):
   https://github.com/NeuroLift-Technologies/sleepwalker/blob/main/AGENTS.md
   Public mirror (if the link above returns 404):
   https://github.com/NeuroLift-Technologies/.github/blob/main/governance/AGENTS.md
3. Project context: `docs/context/README_TO_AI.md` (this repo, if present)
4. Active threads: `docs/active-threads.md` (this repo)

**Non-negotiable:** Joshua W. Dorsey, Sr. is final authority on all architectural,
deployment, UX, and strategic decisions. Escalate. Do not guess.

**Governed by:** Solidarity Framework | HAIEF | https://elevaitionfoundation.org
**OTOI Version:** ORG-DEV-OTOI-1.0.0
```
