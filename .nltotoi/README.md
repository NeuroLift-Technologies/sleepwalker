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

Document ID: `ORG-DEV-OTOI-1.0.0`

## Discovery

Agents and tools can use `nltotoi.json` (repository root) as the machine-readable discovery manifest for all governance file locations.

## Validation

Run governance validation from the repository root:

```bash
bash .nltotoi/scripts/validate-governance.sh
```

The script accepts a strict-mode flag for warning-producing checks:

```bash
bash .nltotoi/scripts/validate-governance.sh --strict
```

The script currently verifies:

- Required governance, template, SOP, and GitHub workflow files exist
- Core content markers are present, including `ORG-DEV-OTOI-1.0.0`,
  `Joshua W. Dorsey`, `Solidarity Framework`, `HAIEF`, and
  `NeuroLift-Technologies/sleepwalker`

`--strict` is available for warning-producing checks. As of
`ORG-DEV-OTOI-1.0.0`, the default validation path does not invoke empty-file or
file-age checks; wiring those checks into the script is tracked in
`.nltotoi/proposals/validation-roadmap.md`.

GitHub Actions runs the same command through
`.github/workflows/validate-governance.yml` on `push` and `pull_request`.
Future validation improvements are tracked in
`.nltotoi/proposals/validation-roadmap.md`.

---

*Internal namespace — NeuroLift Technologies | ORG-DEV-OTOI-1.0.0*
