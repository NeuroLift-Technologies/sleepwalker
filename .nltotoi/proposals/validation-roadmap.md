# Validation Roadmap — NLT Governance

**Status:** v1.0 — Basic file existence and marker validation implemented
**Scope:** `NeuroLift-Technologies/sleepwalker`  
**Owner:** Joshua W. Dorsey, Sr.

---

## Current State (v1.0)

The `validate-governance.sh` script provides:

- ✅ Required file existence checks
- ✅ Document ID marker validation (`ORG-DEV-OTOI-1.0.2`)
- ✅ Authority marker checks
- ✅ Ethical framework marker checks in `NLT-DEV-OTOI.md` (`Solidarity
  Framework`, `HAIEF`)
- ✅ Repository marker checks for `NeuroLift-Technologies/sleepwalker`
- ✅ `--strict` flag parsing for future warning-producing checks
- ✅ Exit code reporting for CI integration

The current script defines helper functions for empty-file and stale-file
warnings, but it does not invoke them yet. Running with `--strict` therefore has
no effect unless future checks increment the warning counter.

---

## Planned Improvements

### v1.1 — JSON Schema Validation

- [ ] Invoke existing empty-file and stale-file warning helpers
- [ ] Add `jsonschema` validation for `nltotoi.json`
- [ ] Validate `templates/agent-registration.json` against defined schema
- [ ] Validate `templates/handoff-record.json` against defined schema

### v1.2 — Cross-Reference Validation

- [ ] Verify all paths referenced in `nltotoi.json` exist on disk
- [ ] Verify all paths in `.nltotoi/index/governance-files.md` exist on disk
- [ ] Detect orphaned files not listed in the index

### v1.3 — Content Validation

- [ ] Check that OTOI sections (1–10) are all present
- [ ] Check that escalation template sections are complete
- [ ] Extend ethical framework marker checks beyond `NLT-DEV-OTOI.md` to
  downstream gateway, instruction, and template files where those markers are
  required

### v1.4 — Downstream Repo Validation

- [ ] Script to validate repo-level CLAUDE.md stubs point to correct OTOI URL
- [ ] Check that stub CLAUDE.md files contain required mandatory reading references

### v2.0 — Automated Reporting

- [ ] GitHub Actions job summary output with pass/fail per check
- [ ] Badge generation for governance compliance
- [ ] Slack/notification integration for validation failures

---

## Implementation Notes

All validation scripts must:
- Exit with code `0` on success, non-zero on failure
- Output human-readable status for each check
- Be idempotent (safe to run multiple times)
- Not modify any files

---

*Validation roadmap — NeuroLift Technologies | ORG-DEV-OTOI-1.0.2*
