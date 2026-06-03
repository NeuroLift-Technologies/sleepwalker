# README_TO_AI - sleepwalker project context

Purpose: give coding agents a source-verified map of this repository before
they modify code or documentation.

## Required first reads

1. `NLT-DEV-OTOI.md` - org-level coding agent contract.
2. `AGENTS.md` - internal coordination gateway.
3. `CLAUDE.md` - repo-local session instructions.
4. `docs/active-threads.md` - current multi-agent work state and blockers.

Do not rewrite canonical governance framing or make architecture/deployment
decisions without Joshua W. Dorsey, Sr.'s approval.

## Repository map

| Path | What it contains | Notes |
|---|---|---|
| `sleepwalker_protocol/` | Python SWP package | Public exports are listed in `sleepwalker_protocol/__init__.py`. |
| `src/` | TypeScript SWP package | Public exports are listed in `src/index.ts`. |
| `tests/` | Python pytest suite | Pytest config is in `pyproject.toml`. |
| `examples/` | Python examples and sample TOI config | See `examples/README.md`. |
| `web/continuity/` | Static Continuity landing page | No build step; backend calls stay disabled while `CONTINUITY_API.base` is blank. |
| `web/continuity/worker/` | Cloudflare Worker API | Consent-gated submit/aggregate/withdraw endpoints; deploys require human approval. |
| `.nltotoi/` | Governance tooling namespace | Validator, file index, contracts namespace, and validation roadmap. |
| `templates/`, `SOPs/`, `agents/` | Governance templates, procedures, and agent profile | Treat OTOI amendments and canonical-source decisions as human-governed. |
| `docs/agent-log/`, `docs/escalations/` | Session records and escalation records | Use templates from `templates/`. |

## Implemented SWP interfaces

### Python package

Import from `sleepwalker_protocol`:

```python
from sleepwalker_protocol import SWP, SleepwalkerProtocol, ContinuityManager
```

Core classes:

- `SleepwalkerProtocol` / `SWP` in `sleepwalker_protocol/protocol.py`
  coordinates state detection, consent, TOI loading, and continuity.
- `StateDetector` and `EmotionalState` in `sleepwalker_protocol/state_detection.py`
  identify protective-state indicators.
- `ConsentManager` and `ConsentLevel` in `sleepwalker_protocol/consent.py`
  choose the appropriate consent/intervention level.
- `ContinuityManager` in `sleepwalker_protocol/continuity.py` stores session
  continuity as local JSON files under the configured storage path.
- `TOILoader` in `sleepwalker_protocol/toi_loader.py` loads YAML TOI files.

Continuity uses a stable `user_id`; do not key continuity on message text.
Storage filenames combine a sanitized slug with a SHA-256 hash of the full id
to keep path traversal and id-collision cases contained.

### TypeScript package

Public exports are in `src/index.ts`:

```ts
export { SleepwalkerProtocol, SWP } from './protocol';
export { EmotionalState, StateDetector } from './stateDetection';
export { ConsentLevel, ConsentManager } from './consent';
export { ContinuityManager } from './continuity';
export { TOILoader } from './toiLoader';
```

Use `npm run build` for the TypeScript compiler path declared in `package.json`.
Do not document additional generated outputs unless `dist/` or package artifacts
are present in the tree.

## Continuity web surface

`web/continuity/` is a static public page for `continuity.haief.org`:

- `index.html` is the single-scroll page.
- `continuity.js` renders the comparison graphic, filters the sentiment wall,
  previews `.toi` records, and controls form submission behavior.
- `withdraw.html` is the withdrawal-token page.

The page sends nothing while `CONTINUITY_API.base` is blank. Keep that preview
behavior honest unless the Worker is deployed and the frontend is explicitly
pointed at it.

`web/continuity/worker/` implements the optional Cloudflare Worker backend:

- `POST /api/submit` validates input, verifies Turnstile when configured, and
  stores only fields covered by consent switches.
- `GET /api/aggregate` returns real consented counts only after `AGGREGATE_MIN`
  rows exist.
- `POST /api/withdraw` hard-deletes the row matching a withdrawal token hash and
  returns the same success shape whether or not a row matched.

Production deployment is a human action. Do not run production deploy commands
or add secrets.

## Development and validation commands

Use commands that match the touched surface:

```bash
python3 -m pip install -e '.[dev]'
python3 -m pytest
npm install
npm run build
bash .nltotoi/scripts/validate-governance.sh
python3 -m json.tool nltotoi.json
```

Notes:

- This environment may provide `python3` even when `python` is absent.
- Documentation-only changes should still run governance validation and JSON
  checks for any session records or manifests touched.
- UI changes under `web/continuity/` need manual browser validation.

## Governance and coordination constraints

- `docs/active-threads.md` may block edits to contested governance files. Read
  it before changing OTOI, AGENTS, SOP, steward, or file-structure documents.
- `NLT-DEV-OTOI.md` cannot be amended by agents.
- Agent commits use `[AGENT_NAME] type(scope): description`.
- Keep documentation source-verified. If source files do not implement a
  workflow, endpoint, gate, or deployment, describe it as absent, planned, or
  human-controlled rather than active.
- External integrations, LLM provider choices, production deployment, and
  credential handling require Joshua's approval.
