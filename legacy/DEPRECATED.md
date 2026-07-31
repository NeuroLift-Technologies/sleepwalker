# Legacy Artifacts — Deprecated

This directory contains archived artifacts from the pre-PR #25 flat-layout Python package structure. These are **deprecated and no longer used** — they are preserved for historical reference only.

## What Was Archived

| Artifact | Original Location | Reason |
|----------|-------------------|--------|
| `sleepwalker_protocol-root/sleepwalker_protocol/__pycache__/` | `sleepwalker_protocol/` (root) | Old flat-layout package directory — contained only `__pycache__` bytecode remnants |
| `sleepwalker_protocol.egg-info/` | `sleepwalker_protocol.egg-info/` (root) | Stale setuptools metadata from flat-layout builds |
| `.pytest_cache/` | Root | Pytest cache from legacy test runs |
| `.coverage` | Root | Coverage data from legacy test runs |
| `tests/__pycache__/` | `tests/__pycache__/` | Bytecode cache from legacy test modules |
| `.swp_storage/` | Root | Legacy continuity storage directory (superseded by configured storage paths) |

## Migration: Flat Layout → Src Layout

**Before (flat layout, deprecated):**
```
sleepwalker_protocol/
  __init__.py
  protocol.py
  ...
sleepwalker_protocol.egg-info/
```

**After (src layout, current — PR #25):**
```
src/sleepwalker_protocol/
  __init__.py
  protocol.py
  continuity.py
  state_detection.py
  consent.py
  toi_loader.py
```

The `src/sleepwalker_protocol/` directory is the **canonical PyPI package source** for `sleepwalker-protocol==1.0.1` and later. The flat layout was replaced to comply with modern Python packaging standards (PEP 517/518, `pyproject.toml` build backend).

## Current Package Sources

- **Python (PyPI):** `src/sleepwalker_protocol/` → `sleepwalker-protocol` on PyPI
- **TypeScript (npm):** `src/*.ts` → `@neurolift-technologies/sleepwalker-protocol` on npm

## Do Not Use

Do not import from, build from, or reference any artifact in this `legacy/` directory. They are preserved solely for git history continuity and audit purposes.

---

*Archived: 2026-07-31 | PR #25: Python port + src-layout migration | PR #26: Crisis/check-in fix | v1.0.2 release*