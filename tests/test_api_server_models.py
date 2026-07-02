"""Tests for API-compatible server model aliases."""

from __future__ import annotations

from perplexity_web_mcp.api.server import AVAILABLE_MODELS, get_model
from perplexity_web_mcp.models import Models


def test_claude_sonnet_aliases_route_to_sonnet_5() -> None:
    assert get_model("claude-sonnet-5-0") is Models.CLAUDE_50_SONNET
    assert get_model("claude-sonnet-5-0", thinking=True) is Models.CLAUDE_50_SONNET_THINKING


def test_legacy_claude_sonnet_alias_routes_to_current_sonnet() -> None:
    assert get_model("claude-sonnet-4-6") is Models.CLAUDE_50_SONNET
    assert get_model("claude-3-5-sonnet", thinking=True) is Models.CLAUDE_50_SONNET_THINKING


def test_glm_aliases_route_to_glm_5_2() -> None:
    assert get_model("glm-5.2") is Models.GLM_5_2
    assert get_model("glm52", thinking=True) is Models.GLM_5_2


def test_available_models_include_current_sonnet_and_glm() -> None:
    ids = {model["id"] for model in AVAILABLE_MODELS}
    assert "claude-sonnet-5-0" in ids
    assert "glm-5.2" in ids
