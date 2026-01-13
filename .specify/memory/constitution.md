<!--
============================================================================
SYNC IMPACT REPORT
============================================================================
Version Change: UNVERSIONED → 1.0.0
Rationale: Initial ratification of Phase II Todo Full-Stack Web Application constitution

Modified Principles:
- All principles newly defined (was template)

Added Sections:
- Core Principles (6 principles defined)
- Technology Stack
- Agent-Based Development
- Quality & Success Criteria
- Governance

Removed Sections:
- Generic template placeholders removed

Templates Requiring Updates:
- ✅ plan-template.md: Constitution Check section already in place; compatible with new principles
- ✅ spec-template.md: User story format aligns with multi-user requirements
- ✅ tasks-template.md: Task organization compatible with agent-driven development workflow

Follow-up TODOs:
- None: All sections complete and ready for use

============================================================================
-->

# Phase II Todo Full-Stack Web Application Constitution

## Core Principles

### I. Specification-Driven Development (NON-NEGOTIABLE)

All development MUST follow the Agentic Dev Stack workflow: **Specify → Plan → Tasks → Implement**.

- Specifications are the single source of truth
- All changes MUST be driven by specs
- No manual coding is allowed without corresponding spec approval
- Use Claude Code + Spec-Kit Plus for all development
- Changes to implementation require spec updates first

**Rationale**: Ensures traceability, prevents scope creep, and maintains consistency between intention and implementation across the entire multi-agent development process.

### II. Multi-User Secure Authentication

User authentication and authorization MUST be implemented with zero-trust security principles.

- User signup and signin are mandatory
- Authentication MUST use Better Auth on the frontend
- JWT tokens MUST be issued after successful login
- All API requests MUST include a valid JWT token
- Backend MUST verify JWT using a shared secret
- Unauthorized requests MUST return HTTP 401
- Users MUST only access and modify their own data
- No cross-user data leakage is permitted

**Rationale**: Protects user data integrity, ensures data isolation in a multi-tenant architecture, and complies with modern security standards.

### III. Database-Backed Persistence

All application data MUST be stored in a persistent database with proper data modeling.

- All data MUST be stored in Neon Serverless PostgreSQL
- Database access MUST use SQLModel ORM
- Task data MUST persist across sessions
- Each task MUST have a clear owner (user_id foreign key)
- Schema migrations MUST be versioned and reversible
- Data relationships MUST enforce referential integrity

**Rationale**: Ensures data durability, enables multi-user scenarios, and provides a foundation for scalable data architecture.

### IV. RESTful API Design with Stateless Authentication

API endpoints MUST follow REST principles and maintain statelessness.

- RESTful API endpoints MUST be implemented for all CRUD operations
- All endpoints MUST be protected by JWT authentication middleware
- API routes MUST filter data by authenticated user ID
- Stateless authentication (no server-side sessions)
- Idempotent operations where applicable (PUT, DELETE)
- Proper HTTP status codes for all responses (200, 201, 401, 404, 500)
- Consistent error response format across all endpoints

**Rationale**: Ensures scalability, predictability, and industry-standard API behavior that supports frontend-backend separation.

### V. Responsive, Animated, User-Friendly Frontend

The user interface MUST provide an excellent user experience across all devices.

- Fully responsive design using Tailwind CSS
- Smooth animations and transitions (Framer Motion or CSS animations)
- Accessible UI components (ARIA labels, keyboard navigation)
- Loading states and error feedback for all async operations
- Centralized API client for all backend communication
- Environment variables MUST be used for configuration (no hardcoded URLs or secrets)
- Modern App Router patterns in Next.js

**Rationale**: Delivers a professional, delightful user experience that meets modern web application standards and ensures accessibility.

### VI. Agent-Based Development Workflow

Development MUST be orchestrated through specialized agents with clear responsibilities.

- A Lead Orchestrator Agent MUST control the overall workflow
- Specialized sub-agents MUST be used for:
  - Specifications (spec-writer)
  - Frontend implementation (frontend-implementer)
  - Backend implementation (fastapi-backend-agent)
  - Authentication (better-auth-jwt-implementer)
  - Quality assurance (phase-ii-qa-reviewer)
- Each agent MUST operate only within its defined scope 
- Inter-agent communication MUST go through the orchestrator
- Agents MUST follow the Specify → Plan → Tasks → Implement workflow

**Rationale**: Ensures separation of concerns, prevents scope creep, and maintains code quality through specialized expertise and clear accountability.

## Technology Stack

### Fixed Technology Decisions

The following technology choices are **NON-NEGOTIABLE** and MUST be used:

- **Frontend**: Next.js 16+ (App Router, TypeScript, Tailwind CSS, Framer Motion or CSS animations)
- **Backend**: Python 3.11+ with FastAPI framework
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel (combines SQLAlchemy + Pydantic)
- **Authentication (Frontend)**: Better Auth with JWT
- **Authentication (Backend)**: JWT verification with shared secret
- **Styling**: Tailwind CSS
- **Language**: TypeScript (frontend), Python (backend)

**Rationale**: These choices provide a modern, scalable, type-safe stack with excellent developer experience and production-ready capabilities.

## Agent-Based Development

### Lead Orchestrator Responsibilities

- Review all specifications before delegating to sub-agents
- Coordinate frontend, backend, and authentication implementation
- Ensure cross-component consistency
- Validate sub-agent outputs against specifications
- Approve completion of implementation phases

### Sub-Agent Responsibilities

- **spec-writer**: Create and refine specifications under `/specs/features/`
- **fastapi-backend-agent**: Implement FastAPI endpoints, SQLModel models, JWT middleware
- **better-auth-jwt-implementer**: Configure Better Auth, JWT token flow, authentication UI
- **frontend-implementer**: Build Next.js pages, components, API client, UI/UX
- **phase-ii-qa-reviewer**: Verify authentication, authorization, security, and spec compliance

### Agent Constraints

- Agents MUST NOT deviate from approved specs
- Agents MUST NOT operate outside their defined scope
- Agents MUST NOT make architectural decisions without orchestrator approval
- Agents MUST document all implementation decisions in code comments

## Quality Constraints

### Security Requirements (NON-NEGOTIABLE)

- ❌ No unauthenticated access to task APIs
- ❌ No cross-user data access (enforce user_id filtering)
- ❌ No hardcoded secrets or API keys (use environment variables)
- ✅ All passwords MUST be hashed (handled by Better Auth)
- ✅ JWT secrets MUST be stored in `.env` files
- ✅ Database credentials MUST be environment variables
- ✅ HTTPS MUST be used in production

### Code Quality Requirements

- ❌ No manual code changes (all changes spec-driven)
- ✅ TypeScript strict mode enabled (frontend)
- ✅ Type hints required (backend Python)
- ✅ Error handling for all async operations
- ✅ Proper HTTP status codes for all API responses
- ✅ Consistent code formatting (Prettier for frontend, Black for backend)

### Functional Requirements

- ✅ Users can create tasks (POST /api/tasks)
- ✅ Users can view their tasks (GET /api/tasks)
- ✅ Users can update tasks (PUT /api/tasks/:id)
- ✅ Users can delete tasks (DELETE /api/tasks/:id)
- ✅ Users can sign up (POST /api/auth/signup)
- ✅ Users can sign in (POST /api/auth/signin)
- ✅ Tasks MUST be associated with authenticated user only

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can sign up, sign in, and access their tasks without errors
- **SC-002**: All CRUD operations work correctly and persist to database
- **SC-003**: No user can access another user's tasks (verified by QA agent)
- **SC-004**: UI is fully responsive on mobile, tablet, and desktop
- **SC-005**: All API endpoints return appropriate HTTP status codes
- **SC-006**: Application demonstrates clear separation between frontend and backend
- **SC-007**: All environment variables properly configured for secrets

### Evidence of Agentic Development

- ✅ Specifications exist under `/specs/features/`
- ✅ Plans exist under `/specs/features/`
- ✅ Tasks exist under `/specs/features/`
- ✅ Implementation matches approved specs
- ✅ PHRs (Prompt History Records) document the development workflow
- ✅ ADRs (Architecture Decision Records) capture significant decisions

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
- Any deviation from specs MUST be justified and documented in an ADR

### Runtime Guidance

- This constitution supersedes all other practices
- Complexity MUST be justified (follow the "Complexity Tracking" section in plan-template.md)
- When in doubt, refer to the Agentic Dev Stack workflow: **Specify → Plan → Tasks → Implement**
- For runtime development guidance, refer to `CLAUDE.md` and agent-specific prompt files

**Version**: 1.0.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-01-02
