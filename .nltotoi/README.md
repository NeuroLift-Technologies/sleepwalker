# .nltotoi — NLT Governance Namespace

This namespace contains internal governance artifacts for the `NeuroLift-Technologies/sleepwalker` repository.

## Purpose

The `.nltotoi/` namespace is the machine-readable and tooling-oriented layer of the NLT governance system. It provides:

- **File index** — registry of all governance files and their purpose
- **Contract namespace** — formal versioned governance contracts
- **Validation scripts** — automated governance compliance checking
- **Proposals** — roadmap and amendment tracking

## Structure

```
.nltotoi/
├── README.md                        ← This file
├── index/
│   └── governance-files.md         ← Registry of all governance files
├── contracts/
│   └── README.md                   ← Contract namespace overview
├── scripts/
│   └── validate-governance.sh      ← Runs governance compliance checks
└── proposals/
    └── validation-roadmap.md       ← Planned validation improvements
```

## Canonical Contract

The canonical governance contract is: **`NLT-DEV-OTOI.md`** (repository root)

Document ID: `ORG-DEV-OTOI-1.0.2`

## Discovery

Agents and tools can use `nltotoi.json` (repository root) as the machine-readable discovery manifest for all governance file locations.

## Validation

Run governance validation from the repository root:

```bash
bash .nltotoi/scripts/validate-governance.sh
```

Strict mode treats warnings as failures:

```bash
bash .nltotoi/scripts/validate-governance.sh --strict
```

The script currently verifies:

- Required governance, template, SOP, and GitHub workflow files exist
- Core content markers are present, including `ORG-DEV-OTOI-1.0.2`,
  `Joshua W. Dorsey`, `Solidarity Framework`, `HAIEF`, and
  `NeuroLift-Technologies/sleepwalker`
- Empty or stale file checks produce warnings unless `--strict` is used

GitHub Actions runs the same command through
`.github/workflows/validate-governance.yml` on `push` and `pull_request`.
Future validation improvements are tracked in
`.nltotoi/proposals/validation-roadmap.md`.

---

*Internal namespace — NeuroLift Technologies | ORG-DEV-OTOI-1.0.2*
