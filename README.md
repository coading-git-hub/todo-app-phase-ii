# AI-Powered Todo Chatbot (MCP + OpenAI Agents SDK)

An innovative todo application that allows users to manage their tasks through natural language interactions with an AI assistant. The system leverages OpenAI Agents SDK and Model Context Protocol (MCP) tools to process natural language requests and perform todo operations.

## Features

- **Natural Language Processing**: Interact with your todo list using everyday language
- **AI-Powered**: Powered by OpenAI's advanced language models
- **Secure Authentication**: JWT-based authentication with user data isolation
- **Persistent Storage**: All tasks and conversations stored in PostgreSQL
- **Real-time Interaction**: Instant responses to your natural language commands

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLModel ORM
- **AI Integration**: OpenAI Agents SDK
- **MCP Tools**: Model Context Protocol for AI tool integration
- **Authentication**: JWT tokens with Better Auth

### Frontend
- **Framework**: Next.js 16+
- **UI Components**: React with TypeScript
- **Chat Interface**: Custom chat interface with OpenAI ChatKit integration

## Architecture

The application follows a stateless design where all conversation history and task data are persisted in Neon Serverless PostgreSQL. The backend exposes a single `/api/{user_id}/chat` endpoint that processes natural language input and routes appropriate actions through MCP tools for data operations.

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file with your configuration:
   ```bash
   cp .env.example .env
   # Edit .env with your actual configuration
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the backend server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Create `.env.local` file:
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local with your actual configuration
   ```

4. Start the frontend development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. Open your browser to `http://localhost:3000`

## Environment Variables

### Backend (.env)
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret key for JWT signing (min 32 characters)
- `OPENAI_API_KEY`: OpenAI API key for AI agent functionality
- `JWT_EXPIRE_DAYS`: JWT token expiry in days (default: 7)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL`: Backend API base URL
- `NEXT_PUBLIC_APP_URL`: Frontend application URL

## API Endpoints

- `POST /api/{user_id}/chat`: Process natural language chat message
- `POST /api/auth/signup`: User registration
- `POST /api/auth/signin`: User login
- `GET /health`: Health check endpoint

## MCP Tools

The system implements several MCP tools for AI agent interactions:
- `add_task`: Create new tasks
- `list_tasks`: Retrieve user's tasks
- `complete_task`: Mark tasks as completed
- `delete_task`: Remove tasks
- `update_task`: Modify existing tasks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.