# Data Model: AI-Powered Todo Chatbot

## Overview
This document defines the database schema and entity relationships for the AI-Powered Todo Chatbot.

## Entities

### 1. User
- **Purpose**: Represents application users
- **Fields**:
  - `id` (UUID/Integer): Primary key
  - `email` (String): Unique user identifier
  - `password_hash` (String): Hashed password (managed by Better Auth)
  - `created_at` (DateTime): Account creation timestamp
  - `updated_at` (DateTime): Last update timestamp
- **Relationships**:
  - One-to-Many with Task (user.tasks)
  - One-to-Many with Conversation (user.conversations)
  - One-to-Many with Message (user.messages)

### 2. Task
- **Purpose**: Represents individual todo items
- **Fields**:
  - `id` (Integer): Primary key
  - `user_id` (UUID/Integer): Foreign key to User
  - `title` (String, required): Task title
  - `description` (Text, optional): Detailed task description
  - `completed` (Boolean, default=False): Completion status
  - `created_at` (DateTime): Creation timestamp
  - `updated_at` (DateTime): Last update timestamp
- **Validation rules**:
  - Title must not be empty
  - User_id must reference existing user
- **State transitions**:
  - `incomplete` → `completed` (via complete_task MCP tool)
  - `completed` → `incomplete` (via update_task MCP tool)
- **Relationships**:
  - Many-to-One with User (task.user)

### 3. Conversation
- **Purpose**: Represents a conversation session between user and AI agent
- **Fields**:
  - `id` (Integer): Primary key
  - `user_id` (UUID/Integer): Foreign key to User
  - `created_at` (DateTime): Session creation timestamp
  - `updated_at` (DateTime): Last activity timestamp
- **Validation rules**:
  - User_id must reference existing user
- **Relationships**:
  - Many-to-One with User (conversation.user)
  - One-to-Many with Message (conversation.messages)

### 4. Message
- **Purpose**: Represents individual messages in a conversation
- **Fields**:
  - `id` (Integer): Primary key
  - `user_id` (UUID/Integer): Foreign key to User
  - `conversation_id` (Integer): Foreign key to Conversation
  - `role` (String, required): Message role ('user' or 'assistant')
  - `content` (Text, required): Message content
  - `created_at` (DateTime): Message creation timestamp
- **Validation rules**:
  - Role must be either 'user' or 'assistant'
  - User_id must match conversation's user_id
  - Conversation_id must reference existing conversation
- **Relationships**:
  - Many-to-One with User (message.user)
  - Many-to-One with Conversation (message.conversation)

## Relationships and Constraints

### Foreign Key Relationships
```
User (1) ←→ (Many) Task
User (1) ←→ (Many) Conversation
User (1) ←→ (Many) Message
Conversation (1) ←→ (Many) Message
```

### Database Constraints
- **User uniqueness**: Email must be unique
- **Referential integrity**: All foreign keys must reference existing records
- **Data isolation**: Users can only access their own records (enforced by application logic and MCP tools)
- **Required fields**: All required fields must have values
- **Timestamps**: created_at and updated_at automatically managed by the database

## Indexes for Performance

### Required Indexes
- `idx_user_email`: On User.email for authentication lookups
- `idx_task_user_id`: On Task.user_id for user-specific queries
- `idx_conversation_user_id`: On Conversation.user_id for user-specific queries
- `idx_message_conversation_id`: On Message.conversation_id for conversation retrieval
- `idx_message_created_at`: On Message.created_at for chronological ordering

### Optional Indexes (for future scaling)
- `idx_task_completed`: On Task.completed for filtering completed tasks
- `idx_message_role`: On Message.role for filtering by message type

## Security Considerations

### Data Access Controls
- All queries must filter by user_id to prevent cross-user data access
- MCP tools must validate user permissions before any data operation
- No direct database access allowed - all operations through MCP tools

### Privacy
- Message content stored encrypted at rest (if required by compliance)
- User data anonymization procedures for analytics
- Audit logs for data access patterns

## Migration Considerations

### Initial Schema
- Create User table first (authentication dependency)
- Create Conversation and Task tables next
- Create Message table last (references other entities)

### Future Extensions
- Support for task categories/tags
- Support for recurring tasks
- Support for task due dates and reminders
- Support for file attachments to tasks or messages