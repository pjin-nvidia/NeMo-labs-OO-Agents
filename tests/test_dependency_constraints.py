# SPDX-FileCopyrightText: Copyright (c) 2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""LiteLLM policy: every release from 1.106.0.dev0 on is banned (dev, rc, final, later), in core and in nooa-acp."""

import tomllib
from pathlib import Path

import pytest
from packaging.requirements import Requirement

ROOT = Path(__file__).resolve().parents[1]


def _litellm(pyproject: Path) -> Requirement:
    project = tomllib.loads(pyproject.read_text())
    return next(r for r in map(Requirement, project["project"]["dependencies"]) if r.name == "litellm")


CASES = [
    ("1.97.0", True), ("1.105.7", True), ("1.105.9.post1", True),
    ("1.106.0.dev0", False), ("1.106.0.dev1", False), ("1.106.0rc1", False), ("1.106.0", False),
    ("1.106.8", False), ("1.107.0.dev1", False), ("1.108.1", False), ("1.108.2", False),
    ("1.109.0rc1", False), ("1.109.0", False), ("2.0.0", False),
]


@pytest.mark.parametrize("version,allowed", CASES + [("1.96.0", False)])
def test_core_litellm_bans_1_106_and_later(version, allowed):
    assert _litellm(ROOT / "pyproject.toml").specifier.contains(version, prereleases=True) is allowed


@pytest.mark.parametrize("version,allowed", CASES + [("1.95.0", False)])
def test_acp_litellm_bans_1_106_and_later(version, allowed):
    assert _litellm(ROOT / "packages/nooa-acp/pyproject.toml").specifier.contains(version, prereleases=True) is allowed
