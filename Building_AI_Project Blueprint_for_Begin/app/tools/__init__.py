"""
tools/__init__.py — Tool Registry
===================================
AI Engineering Roadmap 2026 · Episode 3

The tool registry is a dictionary that maps tool names to their
callable functions.

Why a registry?
  Instead of a chain of if/elif statements in the router, we use a
  dictionary. Adding a new tool means adding ONE line here.

  This is the Open/Closed Principle: open for extension (add tools),
  closed for modification (don't touch the router).

  It also makes testing trivial — you can swap any tool for a mock.

To add a new tool:
  1. Create a new file in tools/ (e.g., stock_price.py)
  2. Define a function: def run(query: str) -> dict
  3. Import it here and add it to TOOL_REGISTRY
"""

from app.tools.calculator import run as calculator_run
from app.tools.weather_api import run as weather_run

# Central registry — maps routing decision strings to callable functions
# Every tool function must accept (query: str) and return a dict
TOOL_REGISTRY: dict = {
    "calculator": calculator_run,
    "weather": weather_run,
}

__all__ = ["TOOL_REGISTRY"]
