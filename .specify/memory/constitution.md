<!--
============================================================================
SYNC IMPACT REPORT
============================================================================
Version Change: 1.0.0 → 2.0.0
Rationale: Major update to transition from Phase II Todo Full-Stack Web Application to Phase III AI-Powered Todo Chatbot with MCP + OpenAI Agents SDK

Modified Principles:
- Principle I: Updated to emphasize AI-native design and MCP tools
- Principle II: Updated authentication for AI agent context
- Principle III: Maintained database persistence with AI focus
- Principle IV: Updated API design for chatbot context
- Principle V: Updated UI principles for OpenAI ChatKit
- Principle VI: Updated agent responsibilities for AI/MCP tools

Added Sections:
- AI-native design principles
- MCP server integration
- OpenAI Agents SDK usage
- Conversation AI patterns
- Tool-driven reasoning

Removed Sections:
- Previous frontend/backend specific details (replaced with AI-focused requirements)

Templates Requiring Updates:
- ⚠ plan-template.md: Needs updates for AI agent development workflow
- ⚠ spec-template.md: Needs updates for conversation AI specifications
- ⚠ tasks-template.md: Needs updates for MCP tool development tasks
- ⚠ commands/sp.phr.*: May need updates for AI development context

Follow-up TODOs:
- Update agent-specific templates to reflect AI/MCP tool development

============================================================================
-->

# Phase III – AI-Powered Todo Chatbot Constitution (MCP + OpenAI Agents SDK)

## Core Principles

### I. Specification-Driven Development (NON-NEGOTIABLE)

All development MUST follow the Agentic Dev Stack workflow: **Specify → Plan → Tasks → Implement**.

- Specifications are the single source of truth
- All changes MUST be driven by specs
- No manual coding is allowed without corresponding spec approval
- Use Claude Code + Spec-Kit Plus for all development
- Changes to implementation require spec updates first
- AI-native design: All todo operations MUST be via AI agents & MCP tools only

**Rationale**: Ensures traceability, prevents scope creep, and maintains consistency between intention and implementation across the entire multi-agent development process with AI-focused architecture.

### II. AI-Native Authentication and Authorization

User authentication and authorization MUST be implemented with zero-trust security principles in an AI agent context.

- User signup and signin are mandatory
- Authentication MUST use Better Auth on the frontend
- JWT tokens MUST be issued after successful login
- All API requests MUST include a valid JWT token
- Backend MUST verify JWT using a shared secret
- Unauthorized requests MUST return HTTP 401
- Users MUST only access and modify their own data
- No cross-user data leakage is permitted
- AI agents MUST respect user boundaries and data isolation
- MCP tools MUST verify user permissions before executing actions

**Rationale**: Protects user data integrity in an AI agent environment, ensures data isolation in a multi-tenant architecture, and complies with modern security standards while enabling safe AI interactions.

### III. Database-Backed Persistence with AI State Management

All application data and conversation state MUST be stored in a persistent database with proper data modeling.

- All data MUST be stored in Neon Serverless PostgreSQL
- Database access MUST use SQLModel ORM
- Task data MUST persist across sessions
- Each task MUST have a clear owner (user_id foreign key)
- Conversation data MUST be stored for auditability
- All agent interactions MUST be logged in DB
- Schema migrations MUST be versioned and reversible
- Data relationships MUST enforce referential integrity
- No in-memory session state; all state in DB

**Rationale**: Ensures data durability, enables multi-user scenarios with conversation history, and provides a foundation for scalable AI agent architecture with full auditability.

### IV. AI-Driven API Design with Stateless Authentication

API endpoints MUST follow REST principles and maintain statelessness while supporting AI agent interactions.

- RESTful API endpoints MUST be implemented for all CRUD operations
- All endpoints MUST be protected by JWT authentication middleware
- API routes MUST filter data by authenticated user ID
- Stateless authentication (no server-side sessions)
- Chat endpoint: Single POST `/api/{user_id}/chat` for all AI interactions
- Idempotent operations where applicable (PUT, DELETE)
- Proper HTTP status codes for all responses (200, 201, 401, 404, 500)
- Consistent error response format across all endpoints
- MCP tools MUST provide structured inputs/outputs for AI agents

**Rationale**: Ensures scalability, predictability, and industry-standard API behavior that supports frontend-backend separation while enabling AI agent tool consumption.

### V. Conversation-Centric User Interface

The user interface MUST provide an excellent conversational experience through OpenAI ChatKit.

- OpenAI ChatKit MUST be used for the conversational interface
- Conversations MUST be persisted and restorable across sessions
- Natural language interactions for all todo operations
- Clear, friendly responses with action confirmation
- Error handling with natural language feedback
- Loading states and error feedback for all AI operations
- Environment variables MUST be used for configuration (no hardcoded URLs or secrets)

**Rationale**: Delivers a professional, delightful conversational user experience that meets modern AI application standards and ensures natural interaction patterns.

### VI. AI Agent-Based Development with MCP Tool Integration

Development MUST be orchestrated through specialized agents with clear responsibilities in an AI context.

- A Lead Orchestrator Agent MUST control the overall workflow
- Specialized sub-agents MUST be used for:
  - Specifications (spec-writer)
  - Frontend implementation (frontend-implementer)
  - Backend implementation (fastapi-backend-agent)
  - Authentication (better-auth-jwt-implementer)
  - MCP tool development (mcp-tool-developer)
  - AI agent orchestration (ai-agent-orchestrator)
- Each agent MUST operate only within its defined scope
- Inter-agent communication MUST go through the orchestrator
- Agents MUST follow the Specify → Plan → Tasks → Implement workflow
- MCP tools MUST be developed for all core functionality
- AI agents MUST use MCP tools for all actions (no hallucinations)

**Rationale**: Ensures separation of concerns in AI development, prevents scope creep, and maintains code quality through specialized expertise and clear accountability for AI/MCP tool integration.

## Technology Stack

### Fixed Technology Decisions

The following technology choices are **NON-NEGOTIABLE** and MUST be used:

- **Frontend**: OpenAI ChatKit (conversational interface)
- **Backend**: Python 3.11+ with FastAPI framework
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel (combines SQLAlchemy + Pydantic)
- **Authentication (Frontend)**: Better Auth with JWT
- **Authentication (Backend)**: JWT verification with shared secret
- **Language**: TypeScript (frontend), Python (backend)

**Rationale**: These choices provide a modern, scalable, AI-native stack with excellent developer experience and production-ready capabilities for conversation AI applications.

## AI Agent and MCP Development

### AI Agent Responsibilities

- **OpenAI Agents SDK**: Orchestrate all AI interactions and tool selection
- **Intent Detection**: Parse natural language for todo operations
- **Tool Selection**: Choose appropriate MCP tools for each action
- **Response Generation**: Formulate natural language responses
- **Conversation Memory**: Maintain context within database (no in-memory state)

### MCP Tool Development

- **MCP Tools**: MUST be developed for all core todo operations:
  - Create task tool
  - List tasks tool
  - Update task tool
  - Delete task tool
  - Search tasks tool
- **Tool Contracts**: MUST define explicit inputs, outputs, and error handling
- **Deterministic Behavior**: Same input + DB = consistent outcome
- **Error Handling**: Graceful handling of task not found, invalid input, permissions

### AI Agent Constraints

- AI agents MUST use MCP tools for all actions; no hallucinations
- AI agents MUST confirm successful actions in natural language
- AI agents MUST handle errors gracefully (task not found, invalid input, permissions)
- AI agents MUST allow multi-step tool calls if required (e.g., list → delete)
- Agents MUST NOT deviate from approved specs
- Agents MUST NOT operate outside their defined scope
- Agents MUST NOT make architectural decisions without orchestrator approval
- Agents MUST document all implementation decisions in code comments

## Quality Constraints

### Security Requirements (NON-NEGOTIABLE)

- ❌ No unauthenticated access to task APIs
- ❌ No cross-user data access (enforce user_id filtering)
- ❌ No hardcoded secrets or API keys (use environment variables)
- ❌ No AI agent bypass of MCP tool security checks
- ✅ All passwords MUST be hashed (handled by Better Auth)
- ✅ JWT secrets MUST be stored in `.env` files
- ✅ Database credentials MUST be environment variables
- ✅ HTTPS MUST be used in production
- ✅ MCP tools MUST verify user permissions before executing actions

### Code Quality Requirements

- ❌ No manual code changes (all changes spec-driven)
- ✅ TypeScript strict mode enabled (frontend)
- ✅ Type hints required (backend Python)
- ✅ Error handling for all async operations
- ✅ Proper HTTP status codes for all API responses
- ✅ Consistent code formatting (Prettier for frontend, Black for backend)
- ✅ Explicit tool contracts for all MCP tools (inputs, outputs, errors)
- ✅ Deterministic behavior in all AI interactions

### Functional Requirements

- ✅ Users can interact with todos via natural language
- ✅ AI agents can create tasks through MCP tools
- ✅ AI agents can list user's tasks through MCP tools
- ✅ AI agents can update tasks through MCP tools
- ✅ AI agents can delete tasks through MCP tools
- ✅ Users can sign up (POST /api/auth/signup)
- ✅ Users can sign in (POST /api/auth/signin)
- ✅ Tasks MUST be associated with authenticated user only
- ✅ All actions executed through MCP tools (no direct DB access)
- ✅ Conversations persist across server restarts
- ✅ Backend remains stateless (no in-memory sessions)

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can sign up, sign in, and interact with todos via natural language
- **SC-002**: All CRUD operations work correctly through AI agents and MCP tools
- **SC-003**: No user can access another user's tasks (verified by AI agent security)
- **SC-004**: AI agents respond naturally and confirm successful actions
- **SC-005**: All API endpoints return appropriate HTTP status codes
- **SC-006**: Application demonstrates clear separation between UI, AI logic, MCP tools, and persistence
- **SC-007**: All environment variables properly configured for secrets
- **SC-008**: Full todo management available via natural language
- **SC-009**: All actions executed through MCP tools without hallucination
- **SC-010**: Conversations persist across server restarts
- **SC-011**: Backend remains stateless with all state in DB

### Evidence of Agentic Development

- ✅ Specifications exist under `/specs/features/`
- ✅ Plans exist under `/specs/features/`
- ✅ Tasks exist under `/specs/features/`
- ✅ Implementation matches approved specs
- ✅ PHRs (Prompt History Records) document the development workflow
- ✅ ADRs (Architecture Decision Records) capture significant decisions
- ✅ MCP tools are properly defined and tested
- ✅ AI agent behavior matches spec requirements

## Governance

### Amendment Process

- Constitution amendments require documentation in a PHR
- Amendments MUST be approved before implementation
- Version MUST be incremented according to semantic versioning:
  - **MAJOR**: Breaking changes, principle removals, or fundamental redefinitions
  - **MINOR**: New principles, sections, or material expansions
  - **PATCH**: Clarifications, wording improvements, typo fixes

### Compliance Verification

- All PRs and reviews MUST verify compliance with this constitution
- Lead Orchestrator MUST enforce agent boundaries
- QA agent MUST verify security and authentication requirements
- AI agent testing MUST verify MCP tool usage and no hallucination
- Any deviation from specs MUST be justified and documented in an ADR

### Runtime Guidance

- This constitution supersedes all other practices
- Complexity MUST be justified (follow the "Complexity Tracking" section in plan-template.md)
- When in doubt, refer to the Agentic Dev Stack workflow: **Specify → Plan → Tasks → Implement**
- For runtime development guidance, refer to `CLAUDE.md` and agent-specific prompt files
- AI agents MUST use MCP tools for all actions; never rely on internal knowledge

**Version**: 2.0.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-01-22
