---
id: "003"
title: "AI Service Integration"
status: "Accepted"
date: "2026-01-26"
---

# ADR-003: AI Service Integration

## Context
The AI Todo Chatbot requires natural language processing capabilities to interpret user commands and convert them into task management operations. We need to select an AI service that can reliably understand user intents and integrate smoothly with our backend system.

## Decision
We will integrate Google Gemini for natural language processing. The AI service will interpret user commands through the chat endpoint and translate them into appropriate task management operations (create, update, delete tasks). We acknowledge that the current implementation uses a deprecated package and plan to migrate from `google.generativeai` to `google.genai`.

## Alternatives Considered
- **OpenAI GPT**: More expensive, potential vendor lock-in concerns
- **Anthropic Claude**: Good alternative but smaller ecosystem
- **Self-hosted models**: Higher maintenance overhead, less reliable
- **Azure OpenAI**: Vendor lock-in to Microsoft ecosystem
- **Multiple provider fallback**: Increased complexity without clear benefit

## Consequences
### Positive
- Strong natural language understanding capabilities
- Good API reliability and documentation
- Reasonable pricing model
- Good integration with Python ecosystem
- Ability to handle diverse user commands for task management

### Negative
- Dependency on external service introduces potential downtime
- API costs that scale with usage
- Need to handle API rate limits
- Potential data privacy considerations
- Deprecated package requires migration to `google.genai`

## References
- plan.md: AI Layer section
- spec.md: US3.1-US3.4 (AI Chat Interface requirements)
- research.md: AI service provider evaluation