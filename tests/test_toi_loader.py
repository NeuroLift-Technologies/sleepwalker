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


def test_returns_empty_dict_for_valid_empty_yaml_document(tmp_path):
    """Regression guard for PR #25 review item #6.

    A valid but empty mapping (``{}``) is truthy in JS, so the TS
    ``yaml.load(content) || getDefaultToi()`` returns it as-is. The Python port
    must do the same and NOT fall back to the default just because ``{}`` is
    falsy in Python. Fallback happens only for a nullish (``None``) parse.
    """
    file = tmp_path / "empty.yaml"
    file.write_text("{}\n", encoding="utf-8")
    toi = TOILoader(str(file)).load()
    assert toi == {}


def test_returns_empty_list_for_valid_empty_yaml_sequence(tmp_path):
    """An empty sequence (``[]``) is likewise truthy in JS and must survive."""
    file = tmp_path / "empty-seq.yaml"
    file.write_text("[]\n", encoding="utf-8")
    toi = TOILoader(str(file)).load()
    assert toi == []


def test_returns_default_toi_for_whitespace_only_yaml(tmp_path):
    """A whitespace-only document parses to ``None`` -> default TOI (matches TS)."""
    file = tmp_path / "blank.yaml"
    file.write_text("\n   \n", encoding="utf-8")
    toi = TOILoader(str(file)).load()
    assert toi["swp"]["active"] is True
