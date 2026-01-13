# Data Model Design
# Phase II Todo Full-Stack Web Application

**Date**: 2026-01-02
**Status**: Complete ✅
**Input**: Entity requirements from `spec.md` and research decisions from `research.md`

## Overview

This document defines the database schema, entity relationships, validation rules, and SQLModel implementations for the Phase II Todo application. The data model enforces user-task relationships with referential integrity and supports multi-user data isolation.

**Key Entities**:
1. **User** - Authentication and task ownership
2. **Task** - Todo items with user association

**Database**: Neon Serverless PostgreSQL
**ORM**: SQLModel 0.0.14+
**Migrations**: Alembic

---

## Entity Relationship Diagram

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │──┐
│ email (UNIQUE)  │  │
│ hashed_password │  │
│ created_at      │  │
└─────────────────┘  │
                     │ 1
                     │
                     │ *
                     │
              ┌──────▼──────┐
              │     Task     │
              ├──────────────┤
              │ id (PK)      │
              │ user_id (FK) │
              │ title        │
              │ description  │
              │ completed    │
              │ created_at   │
              │ updated_at   │
              └──────────────┘

Relationships:
- User → Task: One-to-Many
- Task → User: Many-to-One (Foreign Key: user_id)
```

---

## 1. User Entity

### Purpose
Represents a registered user with authentication credentials and serves as the owner of tasks.

### Fields

| Field           | Type         | Constraints                    | Description                          |
|-----------------|--------------|--------------------------------|--------------------------------------|
| `id`            | Integer (PK) | Auto-increment, NOT NULL       | Unique user identifier               |
| `email`         | String(255)  | UNIQUE, NOT NULL               | User's email address (login)         |
| `hashed_password` | String(255)| NOT NULL                       | Bcrypt hashed password (min 10 rounds) |
| `created_at`    | DateTime     | NOT NULL, default=now()        | Account creation timestamp           |

### Validations

- **Email**: Must match regex `^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$`
- **Password** (plaintext, before hashing): Min 8 characters
- **Unique Constraint**: `email` (prevents duplicate accounts)

### Indexes

- **Primary Key**: `id`
- **Unique Index**: `email` (enforced by unique constraint)

### SQLModel Implementation

```python
# backend/src/models/user.py
from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255, nullable=False)
    hashed_password: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship (not stored in DB, for ORM convenience)
    # tasks: List["Task"] = Relationship(back_populates="owner")


class UserCreate(SQLModel):
    """Schema for user registration (signup)"""
    email: str = Field(max_length=255)
    password: str = Field(min_length=8)


class UserRead(SQLModel):
    """Schema for user responses (no password)"""
    id: int
    email: str
    created_at: datetime


class UserSignIn(SQLModel):
    """Schema for user signin"""
    email: str
    password: str
```

### Relationships

- **One-to-Many with Task**: A user can have multiple tasks
- Cascade behavior: When user is deleted, all their tasks are deleted (ON DELETE CASCADE)

### Security Notes

- Password MUST be hashed using `bcrypt` with min 10 rounds before storage
- Never return `hashed_password` in API responses (use `UserRead` schema)
- Email uniqueness enforced at database level (unique constraint)

---

## 2. Task Entity

### Purpose
Represents a todo item owned by a specific user, with title, description, completion status, and timestamps.

### Fields

| Field          | Type         | Constraints                       | Description                          |
|----------------|--------------|-----------------------------------|--------------------------------------|
| `id`           | Integer (PK) | Auto-increment, NOT NULL          | Unique task identifier               |
| `user_id`      | Integer (FK) | NOT NULL, REFERENCES users(id)    | Owner of the task (foreign key)      |
| `title`        | String(200)  | NOT NULL                          | Task title (required)                |
| `description`  | Text         | NULL                              | Optional task description (max 2000 chars) |
| `completed`    | Boolean      | NOT NULL, default=False           | Completion status                    |
| `created_at`   | DateTime     | NOT NULL, default=now()           | Task creation timestamp              |
| `updated_at`   | DateTime     | NOT NULL, default=now(), on_update=now() | Last modification timestamp   |

### Validations

- **Title**: Required, max 200 characters, non-empty after trim
- **Description**: Optional, max 2000 characters
- **Completed**: Boolean (true/false only)
- **Foreign Key**: `user_id` MUST reference existing `users.id`

### Indexes

- **Primary Key**: `id`
- **Foreign Key Index**: `user_id` (for efficient filtering by user)
- **Composite Index**: `(user_id, created_at DESC)` (for paginated task lists)

### SQLModel Implementation

```python
# backend/src/models/task.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship (not stored in DB)
    # owner: Optional[User] = Relationship(back_populates="tasks")


class TaskCreate(SQLModel):
    """Schema for creating a new task"""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)


class TaskUpdate(SQLModel):
    """Schema for updating an existing task"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: Optional[bool] = None


class TaskRead(SQLModel):
    """Schema for task responses"""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
```

### Relationships

- **Many-to-One with User**: Each task belongs to exactly one user
- Foreign key constraint: `user_id` REFERENCES `users(id)` ON DELETE CASCADE

### Business Rules

1. **User Isolation**: Tasks MUST be filtered by `user_id` in all queries
   - `SELECT * FROM tasks WHERE user_id = :authenticated_user_id`
2. **Ownership Enforcement**: Users can ONLY modify/delete their own tasks
   - Validate `task.user_id == authenticated_user_id` before update/delete
3. **Automatic Timestamps**: `updated_at` automatically set on every update

### Query Patterns

```python
# Get all tasks for a user (ordered by creation date, newest first)
from sqlmodel import select

statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
tasks = await session.execute(statement)
```

---

## Database Schema SQL (for reference)

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);

-- Trigger for updated_at (PostgreSQL)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_tasks_updated_at
BEFORE UPDATE ON tasks
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
```

---

## Alembic Migration Files

### Initial Migration

```python
# backend/alembic/versions/001_initial_schema.py
"""Initial schema with users and tasks

Revision ID: 001
Create Date: 2026-01-02
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('idx_users_email', 'users', ['email'])

    # Tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('idx_tasks_user_created', 'tasks', ['user_id', 'created_at'])

    # Trigger for updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER update_tasks_updated_at
        BEFORE UPDATE ON tasks
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """)

def downgrade():
    op.drop_index('idx_tasks_user_created', table_name='tasks')
    op.drop_index('idx_tasks_user_id', table_name='tasks')
    op.drop_table('tasks')
    op.drop_index('idx_users_email', table_name='users')
    op.drop_table('users')
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;")
```

---

## Data Integrity Rules

### Referential Integrity

1. **Foreign Key Constraint**: `tasks.user_id` MUST reference valid `users.id`
   - Enforced at database level
   - ON DELETE CASCADE: When user deleted, all their tasks deleted
2. **Unique Constraint**: `users.email` prevents duplicate accounts
3. **NOT NULL Constraints**: All required fields enforced at DB level

### Application-Level Validation

1. **Email Format**: Validated by Pydantic before DB insert
2. **Password Strength**: Min 8 characters, validated in `UserCreate` schema
3. **Title Length**: Max 200 characters, validated in `TaskCreate` schema
4. **Description Length**: Max 2000 characters, validated in `TaskUpdate` schema

### Security Constraints

1. **User Isolation**: All task queries MUST filter by authenticated `user_id`
2. **Ownership Verification**: Update/delete operations MUST verify:
   ```python
   task = await session.get(Task, task_id)
   if task.user_id != authenticated_user_id:
       raise HTTPException(status_code=403, detail="Forbidden")
   ```
3. **No Cross-User Access**: Database queries MUST never return tasks from other users

---

## Testing Data Fixtures

### Pytest Fixtures (for backend tests)

```python
# backend/tests/conftest.py
import pytest
from sqlmodel import Session, create_engine
from src.models.user import User
from src.models.task import Task

@pytest.fixture
def test_user(session: Session) -> User:
    user = User(
        email="test@example.com",
        hashed_password="$2b$12$hashed_password_here"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture
def test_task(session: Session, test_user: User) -> Task:
    task = Task(
        user_id=test_user.id,
        title="Test Task",
        description="Test description",
        completed=False
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

---

## Performance Considerations

### Indexes

- **`idx_users_email`**: Fast user lookup during authentication
- **`idx_tasks_user_id`**: Fast filtering of tasks by user
- **`idx_tasks_user_created`**: Composite index for paginated task lists (user_id + created_at DESC)

### Query Optimization

```python
# Efficient: Uses index on user_id
statement = select(Task).where(Task.user_id == user_id)

# Inefficient: Scans all tasks (avoid!)
statement = select(Task).where(Task.title.contains("search_term"))
```

### Connection Pooling

- Neon PostgreSQL handles connection pooling via PgBouncer
- SQLAlchemy pool: `pool_size=5, max_overflow=10`
- `pool_pre_ping=True` to handle stale connections

---

## Migration Commands

```bash
# Generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Apply migrations (production)
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

---

## Summary

**Entities**: 2 (User, Task)
**Relationships**: 1 (User → Task, one-to-many)
**Foreign Keys**: 1 (tasks.user_id → users.id)
**Unique Constraints**: 1 (users.email)
**Indexes**: 3 (users.email, tasks.user_id, tasks.user_id+created_at)

**Constitutional Compliance**:
- ✅ Principle III: Database-Backed Persistence (Neon PostgreSQL + SQLModel)
- ✅ Foreign key constraints enforce referential integrity
- ✅ Versioned migrations via Alembic
- ✅ User data isolation enforced by design

---

**Data Model Status**: ✅ Complete
**Date Completed**: 2026-01-02
**Ready for**: API contract generation (contracts/)
