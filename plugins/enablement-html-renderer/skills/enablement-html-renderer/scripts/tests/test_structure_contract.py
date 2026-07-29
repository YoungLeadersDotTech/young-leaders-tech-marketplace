#!/usr/bin/env python3
"""
test_structure_contract.py - self-consistency check for renderer-structure-contract.json.

KTLO B-01 (ai-os-personal-ktlo--2026-07-28), task T-B01-01: the "expected structure" contract
is only useful if it actually describes the template it claims to describe. This test proves
that every feature entry in the contract genuinely detects against the CURRENT
renderer-template.html - a contract that can't validate clean against its own source of truth
would make the drift checker (T-B01-02, a separate task) broken from day one.

This is a self-consistency test, not the drift checker itself. The checker that scans
*other* rendered artifacts (the two orphaned gallery prototypes, B-05) is built in T-B01-02
and reuses this same manifest - it is a distinct, dependency-free tool (mirrors
rasterize_diagrams.py's pure-Python approach so it runs in Cowork and Claude Code identically).

No third-party dependencies beyond pytest itself (stdlib json + re only), matching the
plugin's existing dependency-free convention (see rasterize_diagrams.py).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parents[2]  # .../skills/enablement-html-renderer
TEMPLATES_DIR = SKILL_DIR / "templates"
CONTRACT_PATH = TEMPLATES_DIR / "renderer-structure-contract.json"
TEMPLATE_PATH = TEMPLATES_DIR / "renderer-template.html"

REQUIRED_TOP_KEYS = {"_schema", "source_of_truth", "defined_at", "features"}
REQUIRED_FEATURE_KEYS = {"id", "label", "introduced_in", "detection"}
SCHEMA_PREFIX = "enablement-html-renderer/structure-contract v1."


@pytest.fixture(scope="module")
def contract() -> dict:
    assert CONTRACT_PATH.exists(), f"contract manifest missing at {CONTRACT_PATH}"
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def template_text() -> str:
    assert TEMPLATE_PATH.exists(), f"template missing at {TEMPLATE_PATH}"
    return TEMPLATE_PATH.read_text(encoding="utf-8")


def test_contract_has_required_top_level_keys(contract):
    missing = REQUIRED_TOP_KEYS - contract.keys()
    assert not missing, f"contract missing top-level keys: {missing}"


def test_contract_schema_is_v1(contract):
    assert contract["_schema"].startswith(SCHEMA_PREFIX), (
        f"expected _schema to start with {SCHEMA_PREFIX!r}, got {contract['_schema']!r}"
    )


def test_source_of_truth_points_at_the_real_template(contract):
    # Path recorded in the contract must resolve to the actual template file relative to
    # the plugin's repo root - a stale/typo'd pointer would silently defeat every check below.
    # SKILL_DIR = .../plugins/enablement-html-renderer/skills/enablement-html-renderer
    # parents[0]=skills, [1]=enablement-html-renderer (plugin root), [2]=plugins, [3]=repo root
    repo_root = SKILL_DIR.parents[3]
    resolved = (repo_root / contract["source_of_truth"]).resolve()
    assert resolved == TEMPLATE_PATH.resolve(), (
        f"source_of_truth {contract['source_of_truth']!r} resolves to {resolved}, "
        f"expected {TEMPLATE_PATH.resolve()}"
    )


def test_contract_has_at_least_one_feature(contract):
    assert isinstance(contract["features"], list) and contract["features"], (
        "contract.features must be a non-empty list"
    )


def test_every_feature_has_required_fields(contract):
    for feature in contract["features"]:
        missing = REQUIRED_FEATURE_KEYS - feature.keys()
        assert not missing, f"feature {feature.get('id', '<no id>')} missing keys: {missing}"


def test_feature_ids_are_unique(contract):
    ids = [f["id"] for f in contract["features"]]
    assert len(ids) == len(set(ids)), f"duplicate feature ids found: {ids}"


def _check_detection(detection: dict, text: str, feature_id: str) -> None:
    """Evaluate one feature's detection block against the template text.

    Supported detection types (kept intentionally small for v1 - T-B01-02 extends the
    checker, not this manifest schema):
      - regex_all: every pattern in `patterns` must re.search successfully.
      - composite: any pattern in `must_match_any` must match, AND (if present) every
        pattern in `must_match_all` must match, AND (if present) no pattern in
        `must_not_match` may match.
    """
    dtype = detection.get("type")
    if dtype == "regex_all":
        for pattern in detection["patterns"]:
            assert re.search(pattern, text), (
                f"[{feature_id}] expected pattern to match template: {pattern!r}"
            )
    elif dtype == "composite":
        must_any = detection.get("must_match_any", [])
        if must_any:
            assert any(re.search(p, text) for p in must_any), (
                f"[{feature_id}] expected at least one of must_match_any to match: {must_any!r}"
            )
        for pattern in detection.get("must_match_all", []):
            assert re.search(pattern, text), (
                f"[{feature_id}] expected must_match_all pattern to match: {pattern!r}"
            )
        for pattern in detection.get("must_not_match", []):
            assert not re.search(pattern, text), (
                f"[{feature_id}] expected must_not_match pattern to be ABSENT, but found: {pattern!r}"
            )
    else:
        pytest.fail(f"[{feature_id}] unknown detection type: {dtype!r}")


def test_every_feature_detects_clean_against_current_template(contract, template_text):
    """The whole point of the contract: it must describe reality right now.

    If this fails, either the manifest drifted from the template it claims to describe, or a
    detection pattern was written by hand without verifying it against the real file - both are
    authoring bugs in the manifest itself, not findings about the template.
    """
    for feature in contract["features"]:
        _check_detection(feature["detection"], template_text, feature["id"])


def test_expected_feature_set_is_present(contract):
    # Locks in the 5 signals KTLO B-01 named explicitly, so a future edit can't silently
    # drop one of the checklist items the backlog item was raised to cover.
    expected_ids = {
        "format-selector-v1",
        "images-v1",
        "dark-mode-toggle-v1",
        "auto-linking-v1",
        "accent-palette-v1",
    }
    actual_ids = {f["id"] for f in contract["features"]}
    missing = expected_ids - actual_ids
    assert not missing, f"contract is missing expected B-01 checklist features: {missing}"
