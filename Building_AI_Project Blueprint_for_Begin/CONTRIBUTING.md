# 🤝 Contributing

Contributions are welcome! This repo is part of an educational series, so the bar for quality is high — but so is the welcome.

## Ways to Contribute

### Add a New Tool
1. Create `app/tools/your_tool.py` with a `run(query: str) -> dict` function
2. Register it in `app/tools/__init__.py`
3. Add it to the routing prompt in `app/prompts/routing_prompt.txt`
4. Add unit tests in `tests/test_tools.py`
5. Add examples in `examples/sample_inputs.md`

**Ideas for new tools:**
- Currency converter (free API: exchangerate.host)
- Unit converter (length, weight, temperature)
- Stock price lookup (free tier: Alpha Vantage)
- Wikipedia summary
- Basic date/time queries

### Improve Existing Code
- Better regex for the calculator
- More robust location extraction in the weather tool
- Improved retry/repair logic in the validator

### Add Documentation
- More examples in `examples/`
- Concept explanations in `docs/CONCEPTS.md`
- Translations of the README

## Standards

- Every new tool must have unit tests
- All functions must have docstrings
- Keep the same code style (comments explaining the *why*, not the *what*)
- Run `pytest tests/ -v` before submitting a PR

## Getting Started

```bash
git clone https://github.com/YOUR_USERNAME/tool-using-ai-assistant
cd tool-using-ai-assistant
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your API key to .env
pytest tests/ -v  # make sure everything passes
```

## Questions?

Open an issue — no question is too basic. This is a learning repo.
