# Quickstart Guide: AI-Powered Todo Chatbot

## Overview
This guide provides step-by-step instructions to get the AI-Powered Todo Chatbot up and running for development and testing.

## Prerequisites
- Python 3.11+ installed
- Node.js 18+ installed
- Git installed
- Neon PostgreSQL account with database created
- OpenAI API key
- MCP server installed and running

## Backend Setup

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd backend
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the backend root:
```env
DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
JWT_SECRET="your-super-secret-jwt-key-here-make-it-long-and-random"
OPENAI_API_KEY="sk-your-openai-api-key"
MCP_SERVER_URL="http://localhost:3001"  # or your MCP server URL
```

### 5. Run Database Migrations
```bash
alembic upgrade head
```

### 6. Start Backend Server
```bash
uvicorn src.main:app --reload --port 8000
```

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Configure Environment Variables
Create a `.env.local` file in the frontend root:
```env
NEXT_PUBLIC_API_URL="http://localhost:8000"
NEXT_PUBLIC_CHATKIT_API_KEY="your-chatkit-api-key-if-using"
NEXT_PUBLIC_APP_URL="http://localhost:3000"
```

### 4. Start Frontend Development Server
```bash
npm run dev
# or
yarn dev
```

## MCP Tools Setup

### 1. Install MCP Server
```bash
npm install -g @modelcontextprotocol/server
```

### 2. Configure MCP Tools
Create MCP tools for:
- add_task
- list_tasks
- complete_task
- delete_task
- update_task

### 3. Start MCP Server
```bash
mcp-server --config ./mcp-config.json
```

## Testing the Application

### 1. API Testing
- Backend API documentation available at: `http://localhost:8000/docs`
- Test the chat endpoint: `POST http://localhost:8000/api/{user_id}/chat`

### 2. Frontend Testing
- Open browser to: `http://localhost:3000`
- Sign up or sign in to access the chat interface
- Test natural language commands like:
  - "Add a task to buy groceries"
  - "Show me my tasks"
  - "Complete the first task"
  - "Delete the meeting task"

### 3. Integration Testing
- Verify conversation history persists
- Test multi-step operations
- Confirm MCP tools are called for all operations
- Validate user data isolation

## Development Commands

### Backend
```bash
# Run tests
pytest --cov=src --cov-report=html

# Format code
black src/
mypy src/

# Run with debug logging
LOG_LEVEL=DEBUG uvicorn src.main:app --reload --port 8000
```

### Frontend
```bash
# Run tests
npm run test

# Lint code
npm run lint

# Format code
npm run format
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify DATABASE_URL is correct
   - Check Neon PostgreSQL connection settings
   - Ensure SSL mode is properly configured

2. **Authentication Failures**
   - Confirm JWT_SECRET is consistent between frontend and backend
   - Check that Better Auth is properly configured

3. **MCP Tools Not Responding**
   - Verify MCP server is running
   - Check that tool endpoints are accessible
   - Confirm tool configurations are correct

4. **AI Agent Not Responding**
   - Verify OPENAI_API_KEY is valid
   - Check that AI model has sufficient tokens
   - Confirm MCP tools are properly registered

### Environment Variables
Ensure all required environment variables are set in both frontend and backend environments.

## Next Steps
- Explore the API documentation
- Customize the MCP tools for additional functionality
- Extend the data models for additional features
- Add more comprehensive tests