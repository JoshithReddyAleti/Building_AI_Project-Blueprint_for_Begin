# 📤 Expected Outputs

> What correct system outputs look like at each layer.
> Use this to verify your system is working correctly.

---

## Calculator Tool Output

```python
# Input query: "What is 25% of 480?"

# Tool raw output (tool_output in state):
{
    "result": 120.0,
    "expression": "25% of 480",
    "query": "What is 25% of 480?",
    "error": None
}

# Final response (what the user sees):
"25% of 480 is 120."
```

---

## Weather Tool Output

```python
# Input query: "What's the weather in London?"

# Tool raw output:
{
    "location": "London, United Kingdom",
    "temperature": 14.0,
    "feels_like": 11.5,
    "condition": "Partly cloudy",
    "wind_speed": 18.0,
    "humidity": 72,
    "unit": "C",
    "error": None
}

# Final response:
"It's currently 14C (feels like 12C) in London with partly cloudy skies.
Wind speed is 18 km/h and humidity is at 72%."
```

---

## Direct LLM Output

```python
# Input query: "What is a vector embedding?"

# Tool raw output: None (no tool used)

# Final response:
"A vector embedding is a numerical representation of data as a list of numbers
in a high-dimensional space. Similar items have similar vectors.
They are the foundation of semantic search and RAG systems."
```

---

## Validation Failure then Repair then Success

```python
# Round 1: LLM returns empty dict — validation fails
# Validator detects: "Missing final_response key"
# Repair applied, round 2 passes

# Final state:
# is_valid=True, retry_count=1, error=None
```

---

## Total Validation Failure - Fallback

```python
# Final response (fallback):
"I wasn't able to process your request reliably. Please try rephrasing your question."

# Final state:
# is_valid=False, retry_count=2, error="Returned fallback response after validation failure"
```

---

## Log Output (What You See in the Terminal)

```
12:34:01 | INFO     | app.main       | Received query: 'What is 25% of 480?'
12:34:01 | INFO     | app.router     | Routing query...
12:34:02 | INFO     | app.router     | Routing decision: calculator
12:34:02 | INFO     | app.router     | Executing tool: calculator
12:34:02 | INFO     | app.tools.calculator | Calculator result: 25% of 480 = 120.0
12:34:03 | INFO     | app.validator  | Validation passed.
12:34:03 | INFO     | app.main       | Tool used: calculator
12:34:03 | INFO     | app.main       | Valid: True
```
