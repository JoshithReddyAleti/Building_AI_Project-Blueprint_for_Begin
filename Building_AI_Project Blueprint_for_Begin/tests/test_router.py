"""
tests/test_router.py — Router Tests
=====================================
AI Engineering Roadmap 2026 · Episode 3

These tests use mocking — we don't want to make real LLM API calls
in unit tests (expensive, slow, non-deterministic).

Instead, we mock the LLM response and test that the router
makes the right decisions based on that response.

This is a key testing pattern in production AI systems.

Run with:
  pytest tests/test_router.py -v
"""

import pytest
from unittest.mock import patch, MagicMock
from app.state import AssistantState


class TestRouter:

    def _make_state(self, query="test"):
        return AssistantState(user_query=query)

    @patch("app.router.call_llm", return_value="calculator")
    @patch("app.tools.calculator.run")
    def test_routes_to_calculator(self, mock_calc, mock_llm):
        """When LLM says 'calculator', the calculator tool should be called."""
        mock_calc.return_value = {
            "result": 120.0, "expression": "25% of 480",
            "query": "What is 25% of 480?", "error": None
        }
        from app.router import route_query
        state = self._make_state("What is 25% of 480?")
        result = route_query("What is 25% of 480?", state)

        mock_calc.assert_called_once()
        assert state.tool_used == "calculator"
        assert "final_response" in result

    @patch("app.router.call_llm", return_value="direct")
    def test_routes_to_direct_llm(self, mock_llm):
        """When LLM says 'direct', no tool should be called."""
        # Second call_llm call is for generating the response
        mock_llm.side_effect = ["direct", "Vector embeddings are numerical representations..."]
        from app.router import route_query
        state = self._make_state("Explain vector embeddings")
        result = route_query("Explain vector embeddings", state)

        assert state.tool_used is None
        assert "final_response" in result

    @patch("app.router.call_llm", return_value="invalid_option_xyz")
    @patch("app.router._execute_direct")
    def test_falls_back_to_direct_on_unknown_decision(self, mock_direct, mock_llm):
        """Unknown routing decisions should fall back to direct, not crash."""
        mock_direct.return_value = {"final_response": "Fallback response."}
        from app.router import route_query
        state = self._make_state("Some query")
        result = route_query("Some query", state)

        mock_direct.assert_called_once()

    @patch("app.router.call_llm", side_effect=Exception("API timeout"))
    @patch("app.router._execute_direct")
    def test_falls_back_on_llm_failure(self, mock_direct, mock_llm):
        """If the routing LLM call fails, it should fall back to direct."""
        mock_direct.return_value = {"final_response": "Fallback response."}
        from app.router import route_query
        state = self._make_state("Some query")
        result = route_query("Some query", state)

        # Should not raise — should gracefully fall back
        mock_direct.assert_called_once()
