# AI Todo Chatbot Quickstart Guide

## Prerequisites
- Python 3.10 or higher
- pip package manager
- PostgreSQL (recommended) or SQLite (for development)
- Google Gemini API key (for AI features)

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd todo-phase-III/backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Copy the example environment file:
```bash
cp .env.example .env
```

Update the `.env` file with your configuration:
```bash
# Database Configuration
DATABASE_URL=sqlite:///./todo_app.db  # For development
# DATABASE_URL=postgresql://user:password@host:port/database  # For production

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
JWT_EXPIRE_DAYS=7

# Google Gemini Configuration
GEMINI_API_KEY=your-gemini-api-key-here

# Application Configuration
DEBUG=True  # Set to False in production
```

### 5. Database Setup
Initialize the database:
```bash
# The application will create tables automatically on startup
# Or run manually if needed:
python -c "from src.db.session import create_db_and_tables; create_db_and_tables()"
```

### 6. Run the Application
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `https://kiran-ahmed-todo-phase-3.hf.space`

## API Usage Examples

### 1. User Registration
```bash
curl -X POST "https://kiran-ahmed-todo-phase-3.hf.space/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### 2. User Login
```bash
curl -X POST "https://kiran-ahmed-todo-phase-3.hf.space/api/auth/signin" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

Save the returned JWT token for subsequent API calls.

### 3. Create a Task
```bash
curl -X POST "https://kiran-ahmed-todo-phase-3.hf.space/api/tasks/" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, bread, eggs",
    "completed": false
  }'
```

### 4. Get All Tasks
```bash
curl -X GET "https://kiran-ahmed-todo-phase-3.hf.space/api/tasks/" \
  -H "Authorization: Bearer <your-jwt-token>"
```

### 5. Interact with AI Chat
```bash
curl -X POST "https://kiran-ahmed-todo-phase-3.hf.space/api/chat" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need to create a task to buy groceries",
    "conversation_id": null
  }'
```

## Testing

### Run Unit Tests
```bash
pytest tests/ -v
```

### Run Specific Test Files
```bash
pytest tests/test_auth.py -v
pytest tests/test_tasks.py -v
```

## Development Workflow

### 1. Running in Development Mode
```bash
# With auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# With detailed logging
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

### 2. Code Formatting
```bash
# Using black for code formatting
black src/ tests/
```

### 3. Static Type Checking
```bash
# Using mypy for type checking
mypy src/
```

## Common Issues and Solutions

### 1. Database Connection Issues
- Ensure PostgreSQL is running if using PostgreSQL
- Check `DATABASE_URL` in your `.env` file
- Verify database credentials are correct

### 2. JWT Authentication Issues
- Verify `JWT_SECRET` is set correctly in `.env`
- Ensure tokens are properly formatted in Authorization header
- Check token expiration time

### 3. Google Gemini API Issues
- Verify `GEMINI_API_KEY` is set correctly in `.env`
- Check API key permissions and quotas
- Handle rate limiting appropriately

### 4. CORS Issues
- Check `allow_origins` in `src/main.py`
- Ensure frontend URLs match the configured origins

## API Documentation
- Interactive API docs available at `https://kiran-ahmed-todo-phase-3.hf.space/docs`
- Alternative Redoc interface at `https://kiran-ahmed-todo-phase-3.hf.space/redoc`

## Environment Variables Reference
- `DATABASE_URL`: Database connection string
- `JWT_SECRET`: Secret key for JWT token signing
- `JWT_EXPIRE_DAYS`: Number of days until JWT expiration
- `GEMINI_API_KEY`: Google Gemini API key
- `DEBUG`: Enable/disable debug mode
- `APP_NAME`: Application name (defaults to "AI Todo Chatbot Backend")