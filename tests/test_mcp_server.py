"""Tests for model-specific MCP tool routing."""

from __future__ import annotations

from unittest.mock import patch

from perplexity_web_mcp.mcp import server
from perplexity_web_mcp.models import Models


def test_current_model_tools_route_to_live_identifiers() -> None:
    cases = (
        (server.pplx_gpt56_terra, Models.GPT_56_TERRA),
        (server.pplx_gpt56_terra_thinking, Models.GPT_56_TERRA_THINKING),
        (server.pplx_gpt56_sol, Models.GPT_56_SOL),
        (server.pplx_gpt56_sol_thinking, Models.GPT_56_SOL_THINKING),
        (server.pplx_grok45, Models.GROK_45),
        (server.pplx_grok45_thinking, Models.GROK_45_THINKING),
    )

    with patch.object(server, "ask", return_value="ok") as mock_ask:
        for tool, model in cases:
            assert tool.fn("question", "none", "conversation") == "ok"
            mock_ask.assert_called_with("question", model, "none", "conversation")


def test_removed_gpt_tools_are_not_exposed() -> None:
    assert not hasattr(server, "pplx_gpt54")
    assert not hasattr(server, "pplx_gpt54_thinking")
    assert not hasattr(server, "pplx_gpt55")
    assert not hasattr(server, "pplx_gpt55_thinking")
