"""
router.py — Routing Decision Layer
====================================
AI Engineering Roadmap 2026 · Episode 3

This is the brain of the orchestration layer.

The router decides whether the user's query should be:
  A) Answered directly by the LLM
  B) Sent to a specific tool (calculator, weather API, etc.)

This is a key engineering concept: separating ROUTING logic from
EXECUTION logic. The LLM is used to make smart decisions, not just
generate text.

Key concepts demonstrated:
  - LLM-as-router pattern
  - Prompt engineering for classification
  - Fallback to rule-based routing
  - Clean separation of concerns
"""

import json
from app.llm_client import call_llm
from app.state import AssistantState
from app.tools import TOOL_REGISTRY
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Available routing decisions — maps to keys in TOOL_REGISTRY or "direct"
ROUTING_OPTIONS = ["calculator", "weather", "direct"]


def route_query(user_query: str, state: AssistantState) -> dict:
    """
    Decide how to handle the user query and execute accordingly.

    The router uses the LLM to classify the intent, then:
      - If a tool is needed: call that tool and return its output
      - If direct: call the LLM for a full response

    Args:
        user_query: The user's input string
        state: The current AssistantState object (mutated in place)

    Returns:
        A dict with at minimum a 'final_response' key
    """
    logger.info("Routing query...")

    # Step 1: Ask the LLM to classify the intent
    routing_decision = _get_routing_decision(user_query)
    logger.info(f"Routing decision: {routing_decision}")

    state.routing_decision = routing_decision

    # Step 2: Execute based on routing decision
    if routing_decision in TOOL_REGISTRY:
        return _execute_tool(routing_decision, user_query, state)
    else:
        return _execute_direct(user_query, state)


def _get_routing_decision(user_query: str) -> str:
    """
    Use the LLM to classify the query into a routing category.

    Falls back to 'direct' if the LLM returns an unexpected value
    or if the API call fails entirely.

    Args:
        user_query: The user's raw query

    Returns:
        One of: 'calculator', 'weather', 'direct'
    """
    with open("app/prompts/routing_prompt.txt", "r") as f:
        prompt_template = f.read()

    prompt = prompt_template.format(
        options=", ".join(ROUTING_OPTIONS),
        query=user_query
    )

    try:
        raw = call_llm(prompt, max_tokens=20, temperature=0)
        decision = raw.strip().lower()

        if decision not in ROUTING_OPTIONS:
            logger.warning(
                f"LLM returned unexpected routing decision: {decision!r}. "
                f"Falling back to 'direct'."
            )
            return "direct"

        return decision

    except Exception as e:
        logger.error(f"Routing LLM call failed: {e}. Falling back to 'direct'.")
        return "direct"


def _execute_tool(tool_name: str, user_query: str, state: AssistantState) -> dict:
    """
    Execute the selected tool and package the result.

    Args:
        tool_name: Key in TOOL_REGISTRY
        user_query: Original query (passed to the tool)
        state: AssistantState (mutated to record tool usage)

    Returns:
        Dict with 'tool_output' and 'final_response'
    """
    tool_fn = TOOL_REGISTRY[tool_name]
    state.tool_used = tool_name

    logger.info(f"Executing tool: {tool_name}")

    try:
        tool_output = tool_fn(user_query)
        state.tool_output = tool_output

        # Use LLM to generate a human-friendly response from the tool output
        final_response = _generate_response_from_tool(user_query, tool_name, tool_output)
        state.final_response = final_response

        return {
            "tool_output": tool_output,
            "final_response": final_response
        }

    except Exception as e:
        logger.error(f"Tool execution failed: {e}")
        state.error = str(e)
        state.tool_output = None
        return {
            "tool_output": None,
            "final_response": f"I tried to use the {tool_name} tool but encountered an error: {e}"
        }


def _execute_direct(user_query: str, state: AssistantState) -> dict:
    """
    Answer the query directly using the LLM (no tools needed).

    Args:
        user_query: Original query
        state: AssistantState (mutated)

    Returns:
        Dict with 'final_response'
    """
    logger.info("Answering directly via LLM.")
    state.tool_used = None

    with open("app/prompts/response_prompt.txt", "r") as f:
        prompt_template = f.read()

    prompt = prompt_template.format(query=user_query)

    try:
        response = call_llm(prompt, max_tokens=500)
        state.final_response = response
        return {"final_response": response}
    except Exception as e:
        logger.error(f"Direct LLM call failed: {e}")
        state.error = str(e)
        return {"final_response": f"I encountered an error generating a response: {e}"}


def _generate_response_from_tool(query: str, tool_name: str, tool_output: dict) -> str:
    """
    Given a tool's structured output, ask the LLM to write a clear,
    friendly final response.

    This separates data retrieval (tool) from response generation (LLM).
    """
    with open("app/prompts/response_prompt.txt", "r") as f:
        prompt_template = f.read()

    context = (
        f"The user asked: {query}\n"
        f"You used the {tool_name} tool and got this data: {json.dumps(tool_output)}\n"
        f"Write a clear, concise, friendly response using this data."
    )

    try:
        return call_llm(context, max_tokens=300)
    except Exception as e:
        logger.error(f"Response generation from tool output failed: {e}")
        return str(tool_output)
