"""
main.py — Entry Point
=====================
AI Engineering Roadmap 2026 · Episode 3
Tool-Using AI Assistant with Validation & Structured Outputs

This file ties together the full pipeline:
  User Input → Router → Tool/LLM → Validator → State → Output

Run this file to interact with the assistant:
  python run.py  (or directly: python -m app.main)
"""

import sys
from app.router import route_query
from app.state import AssistantState
from app.validator import validate_response
from app.utils.logger import get_logger
from app.utils.config import load_config

logger = get_logger(__name__)


def run_assistant(user_query: str) -> str:
    """
    Run the full AI assistant pipeline for a given user query.

    Pipeline:
      1. Initialise state
      2. Route the query (LLM direct vs tool)
      3. Execute tool if needed
      4. Validate output
      5. Return clean final response

    Args:
        user_query: The raw string from the user

    Returns:
        A clean, validated response string
    """
    logger.info(f"Received query: {user_query!r}")

    # Step 1: Initialise state to track everything that happens
    state = AssistantState(user_query=user_query)

    # Step 2: Route the query — LLM decides what to do
    result = route_query(user_query, state)

    # Step 3: Validate the result before returning it
    validated = validate_response(result, state)

    # Step 4: Log the final state for observability
    logger.info(f"Tool used: {state.tool_used or 'none (direct LLM)'}")
    logger.info(f"Valid: {state.is_valid}")

    return validated.final_response


def main():
    """Interactive CLI loop."""
    load_config()

    print("\n" + "=" * 60)
    print("  🤖  Tool-Using AI Assistant")
    print("  AI Engineering Roadmap 2026 — Episode 3")
    print("=" * 60)
    print("  Try:")
    print("    'What is 25% of 480?'")
    print("    'What is the weather in London?'")
    print("    'Explain what a vector embedding is'")
    print("  Type 'quit' to exit.")
    print("=" * 60 + "\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            sys.exit(0)

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        try:
            response = run_assistant(user_input)
            print(f"\nAssistant: {response}\n")
        except Exception as e:
            logger.error(f"Pipeline error: {e}", exc_info=True)
            print(f"\n[Error] Something went wrong: {e}\n")


if __name__ == "__main__":
    main()
