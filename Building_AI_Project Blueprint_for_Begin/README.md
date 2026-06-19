# 🤖 Tool-Using AI Assistant with Validation & Structured Outputs

> ** :

**📬 Not subscribed yet? This repo is part of the AI Engineering Roadmap 2026 — a LinkedIn newsletter that walks you through becoming an AI engineer in 2026, one project at a time. Each episode comes with a real project, a carousel, and a concept deep-dive. → [Subscribe here](https://www.linkedin.com/newsletters/ai-engineering-roadmap-2026-7467249724752908288/)**

**Episode 3 of the [AI Engineering Roadmap 2026](https://www.linkedin.com/newsletters/ai-engineering-roadmap-2026-7467249724752908288/) Newsletter Series**
>
> *"This is where beginners stop learning… and start engineering."*

---

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?style=flat-square&logo=openai&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=flat-square)
![Pytest](https://img.shields.io/badge/Tested-pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-22C55E?style=flat-square)

**[📖 Read the Newsletter](https://www.linkedin.com/newsletters/ai-engineering-roadmap-2026-7467249724752908288/) · [🗺️ View Roadmap](docs/ROADMAP.md) · [💡 Examples](examples/) · [🧪 Tests](tests/)**

</div>

---

## 🎯 What Is This?

Most AI tutorials teach you to call a model and print the response.

**This project teaches you what comes after that.**

This is a modular, production-minded AI assistant that doesn't just *talk* — it *decides*, *acts*, *validates*, and *recovers*. It's built to show you the engineering layer that most tutorials skip entirely.

```
User Query → Routing Decision → Tool Selection → Tool Execution → Validation → Clean Response
```

This is the difference between building a **demo** and building a **system**.

---

## 🧠 The Core Concept (Why This Matters)

Here's the uncomfortable truth most tutorials won't tell you:

| What Beginners Build | What Engineers Build |
|---|---|
| Chatbot that calls a model | System that routes, executes, validates |
| Vague text responses | Structured JSON outputs |
| No error handling | Retry logic + graceful fallbacks |
| One big Python file | Modular, testable architecture |
| Works once in a demo | Reliable across edge cases |

This project bridges that gap. Every file, every design decision, every test in this repo is there to show you **how real AI systems think and behave**.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      User Query                          │
└─────────────────────┬───────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Routing Decision (router.py)                │
│   LLM decides: answer directly OR call a tool           │
└──────┬──────────────────────────────────┬───────────────┘
       │                                   │
       ▼                                   ▼
┌─────────────┐                 ┌──────────────────────┐
│  Direct LLM │                 │    Tool Selection     │
│  Response   │                 │  (tools/__init__.py)  │
│(llm_client) │                 └──────────┬───────────┘
└─────┬───────┘                            │
      │                         ┌──────────▼───────────┐
      │                         │   Tool Execution      │
      │                         │  calculator.py        │
      │                         │  weather_api.py       │
      │                         └──────────┬───────────┘
      │                                    │
      └──────────────┬─────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   Validation Layer     │
        │   (validator.py)       │
        │   + Pydantic Schemas   │
        └────────────┬───────────┘
                     │
             ┌───────▼───────┐
             │  Valid? ───────────────────┐
             │  Yes → respond             │
             │  No  → retry/fallback      │
             └───────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   State Update         │
        │   (state.py)           │
        └────────────┬───────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   Final Response       │
        │   Output to User       │
        └────────────────────────┘
```

---

## 📁 Repository Structure

```
tool-using-ai-assistant/
│
├── app/                          # Core application logic
│   ├── main.py                   # Entry point — runs the full pipeline
│   ├── router.py                 # LLM-based routing decision
│   ├── llm_client.py             # Wrapper for LLM API calls
│   ├── state.py                  # Tracks query, tool used, output, errors
│   ├── validator.py              # Validates inputs/outputs/retries
│   │
│   ├── prompts/                  # All LLM prompt templates
│   │   ├── routing_prompt.txt    # "Should I use a tool or answer directly?"
│   │   └── response_prompt.txt   # Final natural language response prompt
│   │
│   ├── tools/                    # Executable capabilities
│   │   ├── __init__.py           # Tool registry
│   │   ├── calculator.py         # Arithmetic tool
│   │   └── weather_api.py        # Live weather data tool
│   │
│   ├── schemas/                  # Pydantic data contracts
│   │   ├── tool_schema.py        # Schema for tool inputs/outputs
│   │   ├── response_schema.py    # Schema for final responses
│   │   └── state_schema.py       # Schema for system state
│   │
│   └── utils/                    # Shared utilities
│       ├── logger.py             # Structured logging
│       ├── config.py             # Environment + API key management
│       └── helpers.py            # Shared helper functions
│
├── tests/                        # Full test suite
│   ├── test_tools.py             # Unit tests for each tool
│   ├── test_validator.py         # Validation logic tests
│   ├── test_router.py            # Routing decision tests
│   └── test_end_to_end.py        # Full pipeline integration tests
│
├── examples/                     # Learning resources
│   ├── sample_inputs.md          # Example queries and what they trigger
│   └── expected_outputs.md       # What correct outputs look like
│
├── docs/                         # Deep-dive documentation
│   ├── ROADMAP.md                # Full AI Engineering Roadmap 2026
│   ├── ARCHITECTURE.md           # Detailed architecture explanation
│   ├── CONCEPTS.md               # Key AI engineering concepts explained
│   └── INTERVIEW_PREP.md         # How to talk about this project
│
├── .github/
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
│
├── .env.example                  # Environment variable template
├── requirements.txt              # All dependencies
├── run.py                        # Quick start runner
├── CONTRIBUTING.md               # How to contribute
├── CHANGELOG.md                  # Version history
└── LICENSE                       # MIT License
```

---

## ⚡ Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/Building_AI_Project_Blueprint_for_Begin
cd Building_AI_Project_Blueprint_for_Begin
```

### 2. Set up your environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add your API keys
```bash
cp .env.example .env
# Edit .env and add your OpenAI key + Weather API key
```

### 4. Run it
```bash
python run.py
```

---

## 💬 Example Interactions

```
You: What's 25% of 480?
System: [routes to calculator] → [validates] → 120.0

You: What's the weather in London?
System: [routes to weather API] → [validates] → {"temp": 14, "unit": "C", "condition": "Cloudy"}
        → "It's currently 14°C and cloudy in London."

You: Explain what a vector embedding is
System: [routes to direct LLM] → structured explanation returned
```

---

## 🧩 The 5-Layer Mental Model

This project is deliberately structured around 5 engineering layers. Learn these and you'll understand how production AI systems actually work.

| Layer | File | What It Does |
|---|---|---|
| **1. LLM** | `llm_client.py` | The decision-maker — reasoning engine |
| **2. Tools** | `tools/` | Capabilities — what the system can *do* |
| **3. State** | `state.py` | Context — what happened and what's next |
| **4. Orchestration** | `router.py`, `main.py` | Workflow — controls the flow of logic |
| **5. Validation** | `validator.py`, `schemas/` | Reliability — catches failures before users do |

Most beginner projects only have layers 1 and 2. That's why their systems break.

---

## 🗺️ Milestones

Follow this progression to build and understand the system step by step:

- [x] **Milestone 1** — Basic CLI assistant with direct LLM response
- [x] **Milestone 2** — Add calculator tool + routing logic
- [x] **Milestone 3** — Add weather API tool
- [x] **Milestone 4** — Add structured JSON output enforcement
- [x] **Milestone 5** — Add validation + retry logic
- [x] **Milestone 6** — Add tests + polished README

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_tools.py -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=term-missing
```

---

## 💼 Resume Bullet Points

Use one of these when adding this project to your resume:

> **Option 1 (concise):** Built a tool-using AI assistant in Python that dynamically routed user queries to APIs/functions, enforced structured outputs, and validated responses to improve reliability.

> **Option 2 (detailed):** Developed an end-to-end LLM application with tool calling, JSON-based output parsing, retry logic, and validation workflows to simulate production-grade AI behavior.

> **Option 3 (senior framing):** Engineered a modular AI assistant integrating LLM reasoning, external APIs, schema validation, and error handling, demonstrating practical AI system design beyond prompt-based demos.

---

## 🎤 Interview Story

When interviewers ask about this project, don't just describe *what it does*. Explain the *engineering decisions*:

> *"I wanted to move beyond a simple chatbot, so I built a modular AI assistant that could decide when to use tools, call external APIs, and validate outputs before returning responses. The main goal was to simulate a more production-grade architecture by separating reasoning, tool execution, and validation logic into distinct, testable layers."*

That answer sounds significantly stronger than: *"I built an AI chatbot using Python and OpenAI."*

See [`docs/INTERVIEW_PREP.md`](docs/INTERVIEW_PREP.md) for the full guide.

---

## 🛠️ Tech Stack

| Category | Tool | Why |
|---|---|---|
| Language | Python 3.10+ | Industry standard for AI/ML |
| LLM API | OpenAI / Anthropic | Production-grade LLM access |
| Validation | Pydantic v2 | Schema enforcement, type safety |
| HTTP | Requests | API calls (weather, etc.) |
| Env Mgmt | python-dotenv | Secure key management |
| Testing | pytest | Engineering maturity signal |
| Logging | Python logging | Observability |

---

## 📚 Part of the AI Engineering Roadmap 2026

This project is Episode 3 of a structured learning series designed to take you from AI beginner to AI engineer.

| Episode | Topic | Link |
|---|---|---|
| 1 | What is an LLM really? | Coming soon |
| 2 | Python for AI — what actually matters | Coming soon |
| **3** | **Tool calling, APIs & validation** | **← You are here** |
| 4 | Your first end-to-end AI project | Coming soon |
| 5 | RAG — connecting AI to your data | Coming soon |

[📬 Subscribe to the newsletter](https://www.linkedin.com/newsletters/ai-engineering-roadmap-2026-7467249724752908288/) to get each episode as it drops.

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Ideas for contributions:
- Add new tools (stock price, currency converter, unit converter)
- Add a Streamlit UI layer
- Add LangGraph orchestration
- Add observability/tracing

---

## 📄 License

MIT — use this freely, learn from it, build on it, share it.

---

<div align="center">

**If this helped you, give it a ⭐ — it helps other students find it.**

*Built with ❤️ for the AI Engineering Roadmap 2026 community*

[LinkedIn Newsletter](https://www.linkedin.com/newsletters/ai-engineering-roadmap-2026-7467249724752908288/) · [Episode 3 Carousel](#) · [Subscribe](#)

</div>
