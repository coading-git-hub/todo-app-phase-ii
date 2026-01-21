# Todo Feature Tasks

## Phase 1: Setup
- [ ] T001 Initialize project structure per plan.md
- [ ] T002 Install required dependencies (Next.js, Tailwind, Better Auth, FastAPI, SQLModel)
- [ ] T003 Set up environment variables per .env.example
- [ ] T004 Configure Next.js App Router per plan.md

## Phase 2: Foundational
- [ ] T005 [P] Set up Better Auth configuration in src/auth/
- [ ] T006 [P] Create database models in src/models/ using SQLModel per plan.md
- [ ] T007 [P] Create protected route middleware per plan.md
- [ ] T008 [P] Set up API route handlers per plan.md

## Phase 3: [US1] User can create new todo items
- [ ] T009 [US1] Create Todo model with SQLModel (id, title, description, completed, userId, createdAt, updatedAt)
- [ ] T010 [P] [US1] Create POST /api/todos endpoint to handle new todo creation
- [ ] T011 [P] [US1] Create TodoForm component in src/components/TodoForm.tsx
- [ ] T012 [US1] Implement JWT validation middleware for todo creation
- [ ] T013 [US1] Connect TodoForm to POST /api/todos endpoint
- [ ] T014 [US1] Add form validation for todo creation
- [ ] T015 [US1] Add loading states for todo creation
- [ ] T016 [US1] Test user can create new todo items

## Phase 4: [US2] User can read/view their todo list
- [ ] T017 [P] [US2] Create GET /api/todos endpoint to retrieve user's todos
- [ ] T018 [P] [US2] Create TodoList component in src/components/TodoList.tsx
- [ ] T019 [P] [US2] Create TodoItem component in src/components/TodoItem.tsx
- [ ] T020 [US2] Implement user-based filtering in GET /api/todos
- [ ] T021 [US2] Connect TodoList to GET /api/todos endpoint
- [ ] T022 [US2] Display todos with loading and error states
- [ ] T023 [US2] Test user can read/view their todo list

## Phase 5: [US3] User can update/delete todo items
- [ ] T024 [P] [US3] Create PUT /api/todos/{id} endpoint for updates
- [ ] T025 [P] [US3] Create DELETE /api/todos/{id} endpoint for deletion
- [ ] T026 [US3] Add update functionality to TodoItem component
- [ ] T027 [US3] Add delete functionality to TodoItem component
- [ ] T028 [US3] Implement authorization checks for update/delete
- [ ] T029 [US3] Test user can update existing todo items
- [ ] T030 [US3] Test user can delete todo items

## Phase 6: Polish & Cross-Cutting Concerns
- [ ] T031 [P] Add responsive design to all components
- [ ] T032 [P] Implement error boundaries per plan.md
- [ ] T033 [P] Add loading spinners and better UX states
- [ ] T034 [P] Write unit tests for components
- [ ] T035 [P] Write integration tests for API
- [ ] T036 [P] Add proper error handling and messaging
- [ ] T037 [P] Optimize performance per plan.md requirements

## Dependencies
- US2 depends on US1 completion (need to create before viewing)
- US3 depends on US1 completion (need to create before updating/deleting)

## Parallel Execution Examples
- Authentication setup (T005) can run in parallel with database setup (T006)
- Component creation (T011, T017, T018, T019) can run in parallel
- API endpoints (T010, T017, T024, T025) can run in parallel

## Implementation Strategy
- MVP: Complete Phase 1, 2, and 3 (basic todo creation)
- Incremental delivery: Add read capability (Phase 4), then update/delete (Phase 5)