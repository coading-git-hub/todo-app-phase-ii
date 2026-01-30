# AI Todo Chatbot API Contracts

## Authentication API

### POST /api/auth/signup
Register a new user account.

**Request Body:**
```json
{
  "email": "string (valid email format)",
  "password": "string (min 8 characters)"
}
```

**Response (201 Created):**
```json
{
  "id": "UUID",
  "email": "string",
  "created_at": "ISO 8601 datetime"
}
```

**Validation:**
- Email must be valid format
- Password must be at least 8 characters
- Email must be unique

**Errors:**
- 400: Invalid email format or weak password
- 409: Email already exists
- 500: Server error

### POST /api/auth/signin
Authenticate user and return JWT token.

**Request Body:**
```json
{
  "email": "string (valid email format)",
  "password": "string"
}
```

**Response (200 OK):**
```json
{
  "access_token": "JWT string",
  "token_type": "bearer",
  "user": {
    "id": "UUID",
    "email": "string",
    "created_at": "ISO 8601 datetime"
  }
}
```

**Errors:**
- 401: Invalid credentials
- 500: Server error

## Task Management API

All endpoints require JWT authentication in Authorization header: `Bearer {token}`

### GET /api/tasks/
Retrieve all tasks for the authenticated user.

**Response (200 OK):**
```json
[
  {
    "id": "integer",
    "title": "string",
    "description": "string or null",
    "completed": "boolean",
    "user_id": "UUID",
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime"
  }
]
```

**Errors:**
- 401: Unauthorized (invalid/expired token)

### POST /api/tasks/
Create a new task for the authenticated user.

**Request Body:**
```json
{
  "title": "string (1-255 chars)",
  "description": "string (optional, 0-1000 chars)",
  "completed": "boolean (optional, default: false)"
}
```

**Response (201 Created):**
```json
{
  "id": "integer",
  "title": "string",
  "description": "string or null",
  "completed": "boolean",
  "user_id": "UUID",
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime"
}
```

**Validation:**
- Title is required and 1-255 characters
- Description is optional and 0-1000 characters if provided
- Completed is optional, defaults to false

**Errors:**
- 400: Validation error
- 401: Unauthorized
- 500: Server error

### PUT /api/tasks/{task_id}
Update an existing task for the authenticated user.

**Path Parameter:**
- `task_id`: integer (task identifier)

**Request Body:**
```json
{
  "title": "string (optional, 1-255 chars)",
  "description": "string (optional, 0-1000 chars)",
  "completed": "boolean (optional)"
}
```

**Response (200 OK):**
```json
{
  "id": "integer",
  "title": "string",
  "description": "string or null",
  "completed": "boolean",
  "user_id": "UUID",
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime"
}
```

**Errors:**
- 401: Unauthorized
- 404: Task not found
- 400: Validation error
- 500: Server error

### DELETE /api/tasks/{task_id}
Delete a task for the authenticated user.

**Path Parameter:**
- `task_id`: integer (task identifier)

**Response (204 No Content):**
Empty response body

**Errors:**
- 401: Unauthorized
- 404: Task not found
- 500: Server error

## AI Chat API

### POST /api/chat
Process natural language input and perform task management operations.

**Requires JWT authentication in Authorization header: `Bearer {token}`**

**Request Body:**
```json
{
  "message": "string (the natural language command)",
  "conversation_id": "integer (optional, for continuing conversation)"
}
```

**Response (200 OK):**
```json
{
  "conversation_id": "integer",
  "response": "string (AI-generated response)",
  "tool_calls": "array of objects (if any task operations were performed)"
}
```

**Errors:**
- 400: Missing message content
- 401: Unauthorized
- 404: Conversation not found (if conversation_id provided)
- 500: Server error or AI service error

## Common Headers
- `Authorization: Bearer {jwt_token}` (for protected endpoints)
- `Content-Type: application/json`
- `Accept: application/json`

## Common Error Responses

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Error description"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Server error occurred"
}
```

## Authentication Flow
1. User registers via POST /api/auth/signup
2. User authenticates via POST /api/auth/signin to get JWT token
3. User includes JWT token in Authorization header for protected endpoints
4. Token expires after 7 days (configurable)