"""
tests/test_tools.py — Tool Unit Tests
=======================================
AI Engineering Roadmap 2026 · Episode 3

These tests verify that each tool:
  - Returns the correct data structure
  - Handles valid inputs correctly
  - Handles invalid/edge-case inputs gracefully (doesn't crash)

Why test the tools specifically?
  Tools are the part of your system that talks to the outside world.
  They're the most likely to fail — bad input, API downtime, weird edge cases.
  Tests here are your safety net.

Run with:
  pytest tests/test_tools.py -v
"""

import pytest
from app.tools.calculator import run as calc_run
from app.tools.weather_api import run as weather_run


# ============================================================
# CALCULATOR TESTS
# ============================================================

class TestCalculatorTool:

    def test_percentage_calculation(self):
        """Basic percentage: 25% of 480 = 120"""
        result = calc_run("What is 25% of 480?")
        assert result["error"] is None
        assert result["result"] == pytest.approx(120.0)

    def test_percentage_with_comma_in_number(self):
        """Handles numbers with commas: 10% of 1,000 = 100"""
        result = calc_run("What is 10% of 1,000?")
        assert result["error"] is None
        assert result["result"] == pytest.approx(100.0)

    def test_addition(self):
        result = calc_run("What is 100 plus 250?")
        assert result["error"] is None
        assert result["result"] == pytest.approx(350.0)

    def test_subtraction(self):
        result = calc_run("What is 500 minus 180?")
        assert result["error"] is None
        assert result["result"] == pytest.approx(320.0)

    def test_multiplication(self):
        result = calc_run("What is 12 times 13?")
        assert result["error"] is None
        assert result["result"] == pytest.approx(156.0)

    def test_division(self):
        result = calc_run("What is 144 divided by 12?")
        assert result["error"] is None
        assert result["result"] == pytest.approx(12.0)

    def test_division_by_zero_returns_error(self):
        """Division by zero should return an error, not crash."""
        result = calc_run("What is 100 divided by 0?")
        assert result["error"] is not None
        assert result["result"] is None

    def test_no_numbers_returns_error(self):
        """Query with no numbers should return a graceful error."""
        result = calc_run("What is the meaning of life?")
        assert result["error"] is not None
        assert result["result"] is None

    def test_output_always_has_required_keys(self):
        """Regardless of success/failure, the output dict must have these keys."""
        result = calc_run("What is 50% of 200?")
        for key in ("result", "expression", "query", "error"):
            assert key in result, f"Missing key: {key}"

    def test_query_preserved_in_output(self):
        """The original query should always be echoed back."""
        query = "What is 10 plus 5?"
        result = calc_run(query)
        assert result["query"] == query

    def test_decimal_result(self):
        """Handles decimal results cleanly."""
        result = calc_run("What is 1 divided by 3?")
        assert result["error"] is None
        assert result["result"] == pytest.approx(0.333, rel=1e-2)


# ============================================================
# WEATHER TESTS (these hit the real API — mark with @pytest.mark.integration)
# ============================================================

class TestWeatherTool:

    def test_output_always_has_required_keys(self):
        """
        Even on failure, the weather tool must return a dict with all expected keys.
        This test uses a real API call. Mark as integration if you want to skip in CI.
        """
        result = weather_run("What is the weather in London?")
        for key in ("location", "temperature", "condition", "unit", "error"):
            assert key in result, f"Missing key: {key}"

    @pytest.mark.integration
    def test_successful_weather_lookup(self):
        """Test a real weather lookup for a well-known city."""
        result = weather_run("What's the weather in Paris?")
        # We can't assert exact values (weather changes!) but we can assert structure
        assert result["error"] is None
        assert result["location"] is not None
        assert isinstance(result["temperature"], (int, float))
        assert result["unit"] == "C"
        assert result["condition"] is not None

    def test_nonsense_location_returns_error(self):
        """A made-up location should return a graceful error, not crash."""
        result = weather_run("What's the weather in Xyzqwertyville?")
        # Either returns error field set, or None values — should never raise
        assert isinstance(result, dict)

    def test_empty_query_handled(self):
        """Completely empty query should not crash the tool."""
        result = weather_run("")
        assert isinstance(result, dict)
        # Should have an error
        assert result.get("error") is not None or result.get("location") is None
