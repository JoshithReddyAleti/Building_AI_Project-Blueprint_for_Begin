# Changelog

All notable changes to this project will be documented here.

## [1.0.0] — 2026

### Added
- Full tool-calling pipeline with router, tools, validator, and state
- Calculator tool with support for percentages, addition, subtraction, multiplication, division
- Weather API tool using Open-Meteo (free, no API key required)
- Validation layer with retry logic and graceful fallbacks
- Pydantic schemas for all data contracts
- Structured logging across all modules
- Full test suite: unit, mock, and integration tests
- Comprehensive documentation: README, ROADMAP, CONCEPTS, INTERVIEW_PREP
- `.env.example` with clear setup instructions
- Episode 3 of the AI Engineering Roadmap 2026 newsletter series

### Architecture decisions
- Adapter pattern for LLM client (easy provider switching)
- Tool registry pattern (easy tool addition)
- State dataclass for full pipeline observability
- Separation of routing, execution, and validation into distinct modules
