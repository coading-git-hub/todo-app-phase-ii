# Phase II Todo Full-Stack Web Application

A secure, multi-user todo application with authentication, task management, and responsive UI.

## Tech Stack

- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS, Framer Motion
- **Backend**: Python 3.11+, FastAPI, SQLModel, JWT authentication
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT tokens with 7-day expiry

## Features

- User registration and authentication
- Secure JWT-based authentication
- Personal task management (CRUD operations)
- Responsive UI with smooth animations
- Multi-user data isolation
- Cross-user access prevention

## Setup Instructions

### Prerequisites

- Node.js 18.x or higher
- Python 3.11 or higher
- Git
- Neon PostgreSQL account

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

4. Create `.env` file with your database and JWT configuration:
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

## API Documentation

The backend API documentation is available at `http://localhost:8000/docs` when the server is running.

## Environment Variables

### Backend (.env)

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret key for JWT signing (min 32 characters)
- `JWT_EXPIRY_DAYS`: JWT token expiry in days (default: 7)
- `CORS_ORIGINS`: Comma-separated list of allowed origins

### Frontend (.env.local)

- `NEXT_PUBLIC_API_URL`: Backend API base URL
- `NEXT_PUBLIC_APP_URL`: Frontend application URL

## Development

### Running Tests

**Backend Tests**:
```bash
cd backend
pytest --cov=src --cov-report=html
```

**Frontend Tests**:
```bash
cd frontend
npm run test
```

### Code Formatting

**Backend**:
```bash
cd backend
black src/
mypy src/
```

**Frontend**:
```bash
cd frontend
npm run lint
npm run format
```

## Security Features

- Passwords are hashed using bcrypt (min 10 rounds)
- JWT tokens with proper expiry and validation
- User data isolation (users can only access their own tasks)
- Input validation and sanitization
- CORS configured for secure cross-origin requests

## Project Structure

```
todo-app-phase-ii/
├── backend/
│   ├── src/
│   │   ├── models/          # SQLModel database models
│   │   ├── services/        # Business logic
│   │   ├── api/             # FastAPI route handlers
│   │   ├── middleware/      # JWT authentication middleware
│   │   ├── db/              # Database connection
│   │   ├── config.py        # Environment configuration
│   │   └── main.py          # FastAPI app entry point
│   ├── tests/               # Backend tests
│   ├── alembic/             # Database migrations
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables (not in git)
│
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js App Router pages
│   │   ├── components/      # React components
│   │   ├── lib/             # Utilities (API client, auth, types)
│   │   └── styles/          # Global styles
│   ├── package.json         # Node dependencies
│   └── .env.local           # Environment variables (not in git)
│
└── specs/
    └── todo-app-phase-ii/
        ├── spec.md          # Feature specification
        ├── plan.md          # Implementation plan
        ├── research.md      # Technology research
        ├── data-model.md    # Database schema
        ├── quickstart.md    # Setup guide
        └── contracts/       # API contracts (OpenAPI)
```

## End-to-End Flow

1. **Sign Up**: Create an account with email and password
2. **Sign In**: Authenticate and receive JWT token
3. **Create Task**: Add new tasks to your personal list
4. **View Tasks**: See all your tasks in a responsive grid
5. **Update Task**: Edit task details or mark as completed
6. **Delete Task**: Remove tasks you no longer need

## Deployment

- Frontend: Deploy to Vercel
- Backend: Deploy to Railway or Fly.io

## Troubleshooting

- If you encounter CORS errors, ensure `CORS_ORIGINS` in backend `.env` includes your frontend URL
- For database connection issues, verify your Neon PostgreSQL connection string
- If authentication fails, check that JWT_SECRET matches between frontend and backend