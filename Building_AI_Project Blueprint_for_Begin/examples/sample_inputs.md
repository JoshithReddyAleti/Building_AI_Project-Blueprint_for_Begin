# 📥 Sample Inputs

> Example queries and which route they trigger.
> Use these to test your system or demonstrate it in an interview.

---

## Calculator Queries

These should route to the **calculator tool**.

```
What is 25% of 480?
→ Tool: calculator | Result: 120.0

What is 1,500 divided by 4?
→ Tool: calculator | Result: 375.0

How much is 12 times 13?
→ Tool: calculator | Result: 156.0

What is 500 minus 180?
→ Tool: calculator | Result: 320.0

What is 100 plus 250?
→ Tool: calculator | Result: 350.0

Calculate 17.5% of 2,400
→ Tool: calculator | Result: 420.0

If I earn £3,200 per month, what is 8% saved?
→ Tool: calculator | Result: 256.0
```

---

## Weather Queries

These should route to the **weather API tool**.

```
What's the weather in London?
→ Tool: weather | Returns: temp, condition, humidity, wind

What is the current temperature in New York?
→ Tool: weather | Returns: current conditions

Is it raining in Paris right now?
→ Tool: weather | Returns: condition + precipitation data

How cold is it in Tokyo today?
→ Tool: weather | Returns: temperature + feels_like

What's the weather like in Sydney?
→ Tool: weather | Returns: full weather data
```

---

## Direct LLM Queries

These should route to the **LLM directly** (no tool needed).

```
What is a vector embedding?
→ Direct LLM response

Explain the difference between supervised and unsupervised learning
→ Direct LLM response

What is RAG in AI systems?
→ Direct LLM response

Why do LLMs hallucinate?
→ Direct LLM response

What is the difference between a model and a system?
→ Direct LLM response

Explain what Pydantic is and why it's useful
→ Direct LLM response

What is the ReAct pattern in AI agents?
→ Direct LLM response
```

---

## Edge Cases (Test Your Validation)

These are designed to stress-test the validation layer.

```
?
→ Expected: graceful fallback, not a crash

What is divided by?
→ Calculator: no numbers found, returns error dict gracefully

Weather in Xyzqwertyville123
→ Weather: geocoding fails, returns error dict gracefully

(empty string)
→ Expected: "query is empty" validation error, not a crash
```

---

## Combined / Ambiguous Queries

These test how your router handles complex intent.

```
What's 15% of the population of London?
→ Interesting: needs weather (population data) — will likely go direct LLM
   This is a good example of where multi-hop reasoning would help (Episode 7)

If it's below 10°C in Edinburgh, what should I wear?
→ Needs weather data + LLM reasoning
   Current system will likely route to weather, then use LLM for the suggestion

Convert 37 degrees Celsius to Fahrenheit
→ Could route to calculator (37 * 9/5 + 32) or direct LLM
   Good test of routing behaviour at the boundary
```

---

*See [expected_outputs.md](expected_outputs.md) for what correct outputs look like.*
