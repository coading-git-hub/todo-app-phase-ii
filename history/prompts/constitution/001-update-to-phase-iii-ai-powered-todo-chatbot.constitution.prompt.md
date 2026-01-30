---
id: "001"
title: "Update to Phase III AI-Powered Todo Chatbot"
stage: "constitution"
date: "2026-01-22"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "master"
user: "Claude Code"
command: "/sp.constitution"
labels: ["constitution", "phase-iii", "ai", "mcp", "openai-agents"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
  - "README.md"
tests: []
---

# Prompt History Record: Update to Phase III AI-Powered Todo Chatbot

## Original Prompt

```
# /sp.constitution (phase-III update)

**Project:** Phase III – AI-Powered Todo Chatbot (MCP + OpenAI Agents SDK)
This update extands the exiting todo full-Stack web Application constitution
 to include conversation AI , agent-base execution, and MCP tooling.

---

##Additional Core Principles
- **AI-native design:** All todo operations via AI agents & MCP tools only.
- **Stateless backend:** No in-memory session; all state in DB.
- **Tool-driven reasoning:** Agents must use MCP tools for all actions.
- **Deterministic behavior:** Same input + DB = consistent outcome.
- **Human-centered interaction:** Clear, friendly responses with action confirmation.

---

## Additional Key Standards
- **No manual coding:** Implementation via Claude Code only.
- **Spec-first workflow:** Spec → Plan → Tasks → Implementation.
- **Single source of truth:** Database stores all tasks & conversations.
- **Explicit tool contracts:** Inputs, outputs, and errors defined for each MCP tool.
- **Agent autonomy:** Detect intent, select tools, perform multi-step reasoning.
- **Auditability:** Log all messages, responses, and tool calls.

---

## Additional Constraints
- **Backend:** Python FastAPI
- **AI Framework:** OpenAI Agents SDK
- **MCP Server:** Official MCP SDK
- **Frontend:** OpenAI ChatKit
- **Database:** Neon Serverless PostgreSQL + SQLModel
- **Authentication:** Better Auth (user-scoped)
- **Server State:** Fully stateless
- **Chat Endpoint:** Single POST `/api/{user_id}/chat`

---

## Additional Behavioral Rules
- Call MCP tools for all task actions; no hallucinations.
- Confirm successful actions in natural language.
- Handle errors gracefully (task not found, invalid input, permissions).
- Allow multi-step tool calls if required (e.g., list → delete).

---

## Additional Non-Goals
- No traditional CRUD UI
- No client-side state persistence
- No real-time streaming or voice input
- No agent memory outside DB

---

## Additional Quality Standards
- Clear separation: UI, agent logic, MCP tools, persistence
- Consistent naming in specs, tools, DB models
- Idempotent MCP tool behavior
- Readable, structured prompts
- Production-grade error handling

---

## Additional Success Criteria
- Full todo management via natural language
- All actions executed through MCP tools
- Conversations persist across server restarts
- Backend remains stateless
- Agent behavior matches spec
- Passes architectural & functional review without manual coding
```

## Response Summary

Updated the project constitution from Phase II (Todo Full-Stack Web Application) to Phase III (AI-Powered Todo Chatbot with MCP + OpenAI Agents SDK). The key changes include:

- **Version Bump**: From 1.0.0 to 2.0.0 (major update)
- **AI-Native Design**: Emphasized AI agents and MCP tools for all todo operations
- **New Technology Stack**: Added OpenAI Agents SDK, MCP Server, OpenAI ChatKit
- **AI-Specific Principles**: Updated all six core principles to reflect AI agent context
- **MCP Tool Integration**: Defined requirements for MCP tools for all core functionality
- **Stateless Architecture**: Reinforced no in-memory session requirement
- **Natural Language Interface**: Shifted from traditional UI to conversational interface
- **Enhanced Security**: Added AI-specific security requirements for MCP tool verification

## Outcome

The constitution has been successfully updated to guide the development of the AI-powered todo chatbot with MCP tools and OpenAI Agents SDK. The README.md file was also updated to reflect the new project focus.

## Evaluation

The constitution update successfully captures all the requirements specified in the user input, including AI-native design principles, MCP tool integration, and the new technology stack. The version has been properly incremented to 2.0.0 to reflect the major architectural shift from a traditional web application to an AI-powered chatbot.