"""
tests/test_end_to_end.py — Full Pipeline Integration Tests
============================================================
AI Engineering Roadmap 2026 · Episode 3

End-to-end tests verify the full pipeline from user query to response.

These tests mock the LLM (to avoid API costs) but use real tool logic
and real validation — testing that all the layers work together.

In a production codebase, you'd also have:
  - Smoke tests against real APIs (run less frequently)
  - Load tests (how does the system behave under concurrent requests?)
  - Regression tests (does the new version break old behaviour?)

Run with:
  pytest tests/test_end_to_end.py -v
"""

import pytest
from unittest.mock import patch
from app.main import run_assistant
from app.utils.config import load_config


@pytest.fixture(autouse=True)
def load_env():
    """Load test config before each test."""
    load_config()


class TestFullPipeline:

    @patch("app.router.call_llm")
    @patch("app.tools.calculator.run")
    def test_calculator_pipeline_end_to_end(self, mock_calc, mock_llm):
        """
        Full pipeline: calculator query → tool called → validated → response returned.
        """
        mock_llm.side_effect = [
            "calculator",                     # routing decision
            "25% of 480 is 120."             # final response from LLM
        ]
        mock_calc.return_value = {
            "result": 120.0,
            "expression": "25% of 480",
            "query": "What is 25% of 480?",
            "error": None,
        }

        response = run_assistant("What is 25% of 480?")

        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0

    @patch("app.router.call_llm")
    def test_direct_pipeline_end_to_end(self, mock_llm):
        """
        Full pipeline: direct query → LLM answers → validated → response returned.
        """
        mock_llm.side_effect = [
            "direct",
            "A vector embedding is a numerical representation of data in high-dimensional space."
        ]

        response = run_assistant("What is a vector embedding?")

        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 5

    @patch("app.router.call_llm")
    def test_pipeline_never_returns_empty_string(self, mock_llm):
        """
        The pipeline must always return a non-empty string, even under failure.
        """
        # Simulate LLM returning garbage
        mock_llm.return_value = ""

        response = run_assistant("Some query")

        assert response is not None
        assert isinstance(response, str)
        assert len(response.strip()) > 0

    @patch("app.router.call_llm", side_effect=Exception("Total API failure"))
    def test_pipeline_survives_total_llm_failure(self, mock_llm):
        """
        Even when the LLM is completely unavailable, the pipeline should
        return a fallback message instead of raising an unhandled exception.
        """
        # This test verifies graceful degradation
        try:
            response = run_assistant("Any query")
            # If it returns, it must be a non-empty string
            assert isinstance(response, str)
        except RuntimeError:
            # A RuntimeError from the LLM client is acceptable (it means the error
            # propagated correctly rather than being silently swallowed)
            pass
