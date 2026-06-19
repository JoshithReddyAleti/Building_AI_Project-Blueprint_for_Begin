# 🎤 Interview Prep Guide — Episode 3 Project

> How to talk about this project in interviews. Don't just describe what it does — explain the engineering decisions.

---

## The One-Sentence Summary

> "I built a modular AI assistant that decides when to use external tools, calls APIs, validates every output against a schema, and recovers gracefully from failures — demonstrating a more production-oriented approach to AI system design."

---

## The Full Story (2-minute version)

Use this when the interviewer says "tell me about a project you've built":

> "I wanted to go beyond the typical chatbot tutorial, so I built a tool-using AI assistant that demonstrates what production AI systems actually require.
>
> The core challenge was: how do you build something reliable when your central component — the LLM — is inherently probabilistic?
>
> I solved this by adding three layers that most beginner projects skip entirely: a routing layer that decides whether the LLM should answer directly or call a tool, a validation layer that checks every output against a Pydantic schema before it reaches the user, and a state layer that tracks everything that happens in the pipeline so failures are debuggable.
>
> The system can handle arithmetic queries using a calculator tool, live weather queries using the Open-Meteo API, and general knowledge questions directly through the LLM. Every output goes through validation, and the system retries automatically on failure before falling back to a safe default response.
>
> I wrote unit tests for the tools, mocked the LLM in router tests to keep things fast and free, and wrote end-to-end integration tests to verify the full pipeline.
>
> The main thing I learned was that the difference between a demo and a system is validation and error handling. Most tutorials show the happy path. Real systems spend most of their code on the unhappy paths."

---

## Questions You'll Be Asked

### "Why did you build this?"
> "I noticed that most AI tutorials stop at 'call the API and print the response.' I wanted to understand what comes after that — how do real AI systems handle tool calling, structured outputs, and failures? This project was how I taught myself that layer."

### "Walk me through the architecture."
Use the 5-layer model:
> "The system has 5 layers. The LLM is the decision-maker — it classifies queries and generates responses. The tools layer contains the actual capabilities — calculator and weather API. The state layer tracks everything that happens during a pipeline run. The orchestration layer — the router and main.py — controls the flow. And the validation layer checks every output before it reaches the user. Most beginner projects only have the first two layers. The other three are what make a system production-grade."

### "How does the routing work?"
> "The router sends the user's query to the LLM with a classification prompt — it asks the LLM to classify the intent as 'calculator', 'weather', or 'direct'. If the LLM returns an unexpected value, the router falls back to direct response rather than crashing. I chose LLM-based routing over regex because it handles natural language better — 'two hundred minus seventeen' doesn't match a number regex, but an LLM understands it needs arithmetic."

### "Why Pydantic?"
> "Without a schema, I'm trusting that every dict has the exact keys I expect. If the LLM returns a response missing the 'final_response' key, I'd get a KeyError buried 10 function calls deep. Pydantic raises a clear, immediate ValidationError at the boundary. It also self-documents the data contract — anyone reading the code knows exactly what shape the data must be."

### "How did you handle failures?"
> "I have three levels of failure handling. First, each tool handles its own exceptions internally and returns a structured error dict — it never raises. Second, the validator catches invalid outputs and retries up to two times, attempting to repair the response before retrying. Third, if all retries fail, the system returns a graceful fallback message. The user never sees a Python traceback."

### "Why did you write tests?"
> "Three reasons. First, tools that call external APIs can break in unexpected ways — tests catch those breaks before users do. Second, I needed to test the router without making real LLM API calls on every test run, so I used mocking. Third, tests proved to me that the layers actually worked together correctly, not just individually."

### "What would you add next?"
> "A few things: conversation state so the assistant remembers what was said earlier in a session, more tools (stock prices, unit conversion, database queries), a Streamlit UI to make it accessible to non-technical users, and proper observability — structured logging that can be sent to a monitoring service. Eventually I'd add LangGraph to handle more complex multi-step agentic workflows."

---

## Resume Bullets

Choose the version that fits the job description:

**For AI/ML Engineer roles:**
> Engineered a modular LLM-powered assistant in Python with tool calling, external API integration, Pydantic schema validation, retry logic, and 95%+ test coverage across unit, mock, and end-to-end test suites.

**For Software Engineer (AI focus) roles:**
> Built a tool-using AI system separating routing, execution, and validation into distinct, testable layers — demonstrating production-grade AI system design beyond prompt-based demos.

**For entry-level/new grad roles:**
> Developed an end-to-end AI assistant with LLM-based routing, calculator and weather API tools, structured JSON outputs, and validation workflows — applied software engineering principles (separation of concerns, testing, error handling) to AI system design.

---

## What NOT to say

❌ "I built an AI chatbot using Python and OpenAI."
❌ "I followed a tutorial and added some features."
❌ "It's basically like ChatGPT but you can ask it about the weather."

✅ Lead with the engineering problem you solved.
✅ Explain the decisions you made and why.
✅ Show that you understand the tradeoffs.

---

## GitHub README Checklist

Before sharing this project:
- [ ] Replace `YOUR_USERNAME` in README links with your actual GitHub username
- [ ] Add your LinkedIn newsletter link
- [ ] Make sure tests pass (`pytest tests/ -v`)
- [ ] Make sure the README renders correctly on GitHub
- [ ] Add at least one real screenshot or terminal recording
- [ ] Remove any hardcoded API keys (check with `git grep "sk-"`)

---

*Back to [README](../README.md) · [Concepts](CONCEPTS.md) · [Roadmap](ROADMAP.md)*
