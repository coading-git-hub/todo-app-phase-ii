# AI Todo Chatbot Data Model

## Entity Definitions

### User
Represents a registered user of the system.

**Fields:**
- `id`: UUID (Primary Key, Default: uuid.uuid4) - Unique identifier for the user
- `email`: String (Unique, Indexed, Max Length: 255) - User's email address
- `hashed_password`: String (Indexed) - Bcrypt hashed password
- `created_at`: DateTime (Default: datetime.utcnow) - Account creation timestamp
- `updated_at`: DateTime (Default: datetime.utcnow) - Last update timestamp

**Relationships:**
- `tasks`: One-to-Many relationship with Task (back_populates: user)
- `conversations`: One-to-Many relationship with Conversation (back_populates: user)
- `messages`: One-to-Many relationship with Message (back_populates: user)

### Task
Represents a todo item created by a user.

**Fields:**
- `id`: Integer (Primary Key, Auto-increment) - Unique identifier for the task
- `title`: String (Min Length: 1, Max Length: 255) - Task title
- `description`: Text (Optional, Max Length: 1000) - Task description
- `completed`: Boolean (Default: False) - Completion status
- `user_id`: UUID (Foreign Key: user.id, Indexed) - Owner of the task
- `created_at`: DateTime (Default: datetime.utcnow) - Creation timestamp
- `updated_at`: DateTime (Default: datetime.utcnow) - Last update timestamp

**Relationships:**
- `user`: Many-to-One relationship with User (back_populates: tasks)

### Conversation
Represents a conversation thread between a user and the AI assistant.

**Fields:**
- `id`: Integer (Primary Key, Auto-increment) - Unique identifier for the conversation
- `user_id`: UUID (Foreign Key: user.id, Indexed) - Owner of the conversation
- `created_at`: DateTime (Default: datetime.utcnow) - Creation timestamp
- `updated_at`: DateTime (Default: datetime.utcnow) - Last update timestamp

**Relationships:**
- `user`: Many-to-One relationship with User (back_populates: conversations)
- `messages`: One-to-Many relationship with Message (back_populates: conversation)

### Message
Represents a single message within a conversation.

**Fields:**
- `id`: Integer (Primary Key, Auto-increment) - Unique identifier for the message
- `role`: String (Regex: ^(user|assistant)$, Max Length: 20) - Sender role (user or assistant)
- `content`: Text (Min Length: 1, Max Length: 5000) - Message content
- `user_id`: UUID (Foreign Key: user.id, Indexed) - Author of the message
- `conversation_id`: Integer (Foreign Key: conversation.id, Indexed) - Conversation containing this message
- `created_at`: DateTime (Default: datetime.utcnow) - Creation timestamp

**Relationships:**
- `user`: Many-to-One relationship with User (back_populates: messages)
- `conversation`: Many-to-One relationship with Conversation (back_populates: messages)

## Validation Rules

### User Validation
- Email must be in valid email format
- Email must be unique across all users
- Password must be at least 8 characters (validated during registration)

### Task Validation
- Title must be 1-255 characters
- Description must be 0-1000 characters if provided
- User can only modify/delete their own tasks
- Completed status can be updated independently

### Message Validation
- Role must be either "user" or "assistant"
- Content must be 1-5000 characters
- Messages belong to conversations owned by the same user

## Indexing Strategy

### Primary Indexes
- User.id (UUID)
- Task.id (Integer)
- Conversation.id (Integer)
- Message.id (Integer)

### Foreign Key Indexes
- User.email (String, Unique)
- Task.user_id (UUID)
- Conversation.user_id (UUID)
- Message.user_id (UUID)
- Message.conversation_id (Integer)
- Message.role (String)

### Composite Indexes
- (Message.conversation_id, Message.created_at) for chronological ordering

## State Transitions

### Task States
- **Active**: Default state when created (completed: false)
- **Completed**: When completed status is set to true (completed: true)

### Message Roles
- **User**: Messages sent by the user (role: "user")
- **Assistant**: Messages sent by the AI assistant (role: "assistant")

## Data Integrity Constraints

### Referential Integrity
- Tasks must have valid user_id pointing to existing User
- Conversations must have valid user_id pointing to existing User
- Messages must have valid user_id and conversation_id pointing to existing records

### Business Logic Constraints
- Users can only access their own tasks, conversations, and messages
- Messages in a conversation must belong to the same user who owns the conversation
- Task deletion cascades to related records if needed (none in this case)