# Sleepwalker Context for Coding Agents

This page gives source-verified orientation for agents working in this
repository. Keep it concise and update it when public APIs, package workflows,
or governance contracts change.

## Canonical Governance

- Read `NLT-DEV-OTOI.md` first. The active document ID is
  `ORG-DEV-OTOI-1.0.2`.
- `AGENTS.md` is the internal gateway for agent coordination and points back to
  the same OTOI contract.
- `.nltotoi/scripts/validate-governance.sh` is the only tracked governance CI
  validator. It checks required files and marker strings, and it is run by
  `.github/workflows/validate-governance.yml` on `push` and `pull_request`.
- As of `origin/main` commit `54cfe82`, `.github/workflows/validate-governance.yml`
  is still the only tracked GitHub Actions workflow. PR #19 was titled as an
  npm trusted-publishing workflow change, but its merged diff is empty and
  `.github/workflows/publish-npm.yml` is not present. Do not assume npm publish
  automation exists until that workflow file lands in source.
- Session records belong in `docs/agent-log/registrations/` and
  `docs/agent-log/handoffs/`; active work state belongs in
  `docs/active-threads.md`.

## Implemented Runtime Surfaces

### Python package: `sleepwalker_protocol/`

Primary public entry point:

```python
from sleepwalker_protocol import SWP

swp = SWP(
    user_toi_path="examples/sample_toi.yaml",
    storage_path=".swp_storage",
    user_id="stable-user-id",
)
assessment = swp.assess_interaction("I feel numb today")
response = swp.generate_response(
    "I feel numb today",
    detected_state=assessment["emotional_state"],
)
swp.maintain_continuity(
    "stable-user-id",
    {"emotional_state": "numbing", "protective_state_active": True},
)
```

Important contracts:

- `SWP` is an alias of `SleepwalkerProtocol`.
- `assess_interaction(..., user_id=...)` uses a stable user identifier for
  continuity lookup. Do not use message text as the continuity key.
- `TOILoader` accepts YAML and JSON TOI files and falls back to a conservative
  default when no file is provided or parsing fails.
- `ContinuityManager` stores local JSON state under the configured storage path
  using traversal-safe, hash-backed filenames.

### TypeScript package: `src/`

Primary public entry point:

```ts
import { SWP, ConsentLevel } from "@neurolift-technologies/sleepwalker-protocol";

const swp = new SWP({
  userToiPath: "examples/sample_toi.yaml",
  storagePath: ".swp_storage",
  loggingEnabled: false,
});

const assessment = swp.assessInteraction("I feel numb today");
const response = swp.generateResponse(
  "I feel numb today",
  assessment.emotionalState,
);
```

Important contracts:

- `src/index.ts` exports `SleepwalkerProtocol`, `SWP`, `StateDetector`,
  `ConsentManager`, `ConsentLevel`, `ContinuityManager`, and `TOILoader`.
- The root npm package is `@neurolift-technologies/sleepwalker-protocol`.
- `tsconfig.json` emits CommonJS JavaScript and declarations to `dist/`.
- `package.json` publishes only `dist/**/*`, `README.md`, and `LICENSE`.
- `prepublishOnly` runs `npm run build`, so publish dry-runs should compile
  before producing a tarball.
- `publishConfig.access` is `public`; no npm token or trusted-publishing
  workflow is currently tracked in the repository.
- `package-lock.json` is committed; use `npm ci` for reproducible Node setup.

## Verification Commands

Run the checks that match your change:

```bash
# Governance docs and templates
bash .nltotoi/scripts/validate-governance.sh

# Python package
python3 -m pip install -e ".[dev]"
python3 -m pytest tests/

# TypeScript package
npm ci
npm run build
npm test
npm pack --dry-run
```

Only the governance validation workflow is tracked in `.github/workflows/` at
the time of writing, so Python and TypeScript package checks are manual unless a
new workflow is added. If an npm publish workflow is introduced, verify that the
workflow file exists in source, uses `npm ci`, runs from the repository root,
and publishes the root package only after `npm run build` succeeds.

## Known Constraints and Pitfalls

- `dist/` is ignored by `.gitignore` and should be generated locally, not
  committed.
- The Python and TypeScript implementations use different naming conventions
  (`assess_interaction` vs. `assessInteraction`, `user_toi_path` vs.
  `userToiPath`). Match the ecosystem you are editing.
- The root `LICENSE` and npm `package.json` currently use `Apache-2.0`; Python
  package metadata still declares MIT. Do not make licensing changes without
  explicit maintainer direction.
- `file-structure.md` includes historical architecture notes for the private
  governance repository. Verify against actual files before treating it as an
  inventory of this checkout.
