"""Conformance port of ``tests/toiLoader.test.ts``.

Mirrors every assertion from the TypeScript Jest suite. ``js-yaml`` on the TS side
maps to PyYAML here, so the same documents load to the same structures.
"""
from __future__ import annotations

import json

from sleepwalker_protocol import TOILoader


def test_returns_default_toi_when_no_path_given():
    toi = TOILoader().load()
    assert toi["swp"]["active"] is True
    assert toi["swp"]["intervention_threshold"] == "user_initiated_only"


def test_returns_default_toi_for_nonexistent_path(tmp_path):
    toi = TOILoader(str(tmp_path / "non-existent.yaml")).load()
    assert toi["swp"]["active"] is True


def test_loads_json_toi_document(tmp_path):
    file = tmp_path / "toi.json"
    file.write_text(json.dumps({"swp": {"active": False}}), encoding="utf-8")
    toi = TOILoader(str(file)).load()
    assert toi["swp"]["active"] is False


def test_loads_yaml_toi_document(tmp_path):
    file = tmp_path / "toi.yaml"
    file.write_text(
        "swp:\n  active: true\n  intervention_threshold: offer_support_without_pressure\n",
        encoding="utf-8",
    )
    toi = TOILoader(str(file)).load()
    assert toi["swp"]["intervention_threshold"] == "offer_support_without_pressure"
