# Quickstart Guide
# Phase II Todo Full-Stack Web Application

**Date**: 2026-01-02
**Status**: Complete ✅
**Audience**: Developers setting up local development environment

## Overview

This guide walks you through setting up and running the Phase II Todo application locally. The application consists of a FastAPI backend, Next.js frontend, and Neon PostgreSQL database.

**Tech Stack**:
- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS, Better Auth
- **Backend**: Python 3.11+, FastAPI, SQLModel, JWT authentication
- **Database**: Neon Serverless PostgreSQL
- **Deployment**: Vercel (frontend), Railway/Fly.io (backend)

**Estimated Setup Time**: 15-20 minutes

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js**: 18.x or higher ([Download](https://nodejs.org/))
- **Python**: 3.11 or higher ([Download](https://www.python.org/downloads/))
- **Git**: Latest version ([Download](https://git-scm.com/downloads))
- **Neon PostgreSQL Account**: Free tier ([Sign up](https://neon.tech/))

**Verification**:
```bash
node --version   # Should show v18.x.x or higher
python --version # Should show Python 3.11.x or higher
git --version    # Should show git version 2.x.x
```

---

## Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/your-username/todo-app-phase-ii.git
cd todo-app-phase-ii

# Checkout the feature branch
git checkout todo-app-phase-ii
```

---

## Step 2: Database Setup (Neon PostgreSQL)

### 2.1 Create Neon Database

1. Go to [Neon Console](https://console.neon.tech/)
2. Create a new project: "Todo App Phase II"
3. Copy the connection string (format: `postgresql://user:password@host/dbname`)

### 2.2 Note Your Connection String

```
Example:
postgresql://user:AbCd1234@ep-cool-name-123456.us-east-2.aws.neon.tech/tododb
```

Keep this handy for Step 3.

---

## Step 3: Backend Setup

### 3.1 Navigate to Backend Directory

```bash
cd backend
```

### 3.2 Create Python Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**Verification**: Your terminal prompt should show `(venv)` prefix.

### 3.3 Install Backend Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected packages**:
- fastapi
- uvicorn[standard]
- sqlmodel
- psycopg2-binary
- python-jose[cryptography]
- passlib[bcrypt]
- python-dotenv

### 3.4 Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# backend/.env
DATABASE_URL=postgresql://user:password@host/dbname
JWT_SECRET=your-super-secret-jwt-key-min-32-characters-long
JWT_EXPIRY_DAYS=7
CORS_ORIGINS=http://localhost:3000
```

**Important**:
- Replace `DATABASE_URL` with your Neon connection string from Step 2.2
- Generate a secure `JWT_SECRET` (min 32 characters, random):
  ```bash
  # Generate secure secret (macOS/Linux)
  openssl rand -hex 32

  # Or use Python
  python -c "import secrets; print(secrets.token_hex(32))"
  ```

**Security Note**: Never commit `.env` to git. It's already in `.gitignore`.

### 3.5 Run Database Migrations

```bash
# Initialize Alembic (if not already done)
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

**Expected output**:
```
INFO [alembic.runtime.migration] Running upgrade -> 001_initial_schema
```

**Verification**: Check Neon console - you should see `users` and `tasks` tables.

### 3.6 Start Backend Server

```bash
uvicorn src.main:app --reload --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Test backend**:
Open https://kiran-ahmed-todo-phase-3.hf.space/docs to see interactive API documentation.

---

## Step 4: Frontend Setup

**Open a new terminal** (keep backend running).

### 4.1 Navigate to Frontend Directory

```bash
cd frontend
```

### 4.2 Install Frontend Dependencies

```bash
npm install
# or
yarn install
```

**Expected packages**:
- next
- react
- react-dom
- typescript
- tailwindcss
- better-auth

### 4.3 Configure Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=https://kiran-ahmed-todo-phase-3.hf.space
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**Note**: `.env.local` is already in `.gitignore`.

### 4.4 Start Frontend Development Server

```bash
npm run dev
# or
yarn dev
```

**Expected output**:
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
info  - automatically enabled Fast Refresh for 1 custom loader
```

**Open application**: http://localhost:3000

---

## Step 5: Verify Installation

### 5.1 Backend Health Check

```bash
curl https://kiran-ahmed-todo-phase-3.hf.space/docs
```

**Expected**: Should return HTML for Swagger UI.

### 5.2 Frontend Health Check

Open http://localhost:3000 in your browser.

**Expected**: You should see the landing/signin page.

### 5.3 End-to-End Test

1. **Sign Up**:
   - Navigate to http://localhost:3000/signup
   - Enter email: `test@example.com`, password: `password123`
   - Click "Sign Up"
   - **Expected**: Redirect to signin or dashboard

2. **Sign In**:
   - Navigate to http://localhost:3000/signin
   - Enter credentials from step 1
   - Click "Sign In"
   - **Expected**: Redirect to tasks dashboard

3. **Create Task**:
   - Click "Add Task" button
   - Enter title: "Test Task"
   - Enter description (optional): "This is a test"
   - Submit
   - **Expected**: Task appears in list

4. **Update Task**:
   - Click "Edit" on the task
   - Change title or mark as completed
   - Submit
   - **Expected**: Task updates immediately

5. **Delete Task**:
   - Click "Delete" or trash icon
   - Confirm deletion
   - **Expected**: Task removed from list

---

## Common Issues & Troubleshooting

### Issue: Backend won't start - "ModuleNotFoundError"

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Database connection error - "could not connect to server"

**Solution**:
- Verify Neon connection string in `backend/.env`
- Check Neon console for database status
- Ensure connection string includes password and correct host

### Issue: Frontend won't start - "Cannot find module"

**Solution**:
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Issue: CORS error in browser console

**Solution**:
- Verify `CORS_ORIGINS` in `backend/.env` includes `http://localhost:3000`
- Restart backend server after changing `.env`

### Issue: JWT token invalid/expired

**Solution**:
- Clear browser cookies for `localhost:3000`
- Sign in again to get a new token
- Verify `JWT_SECRET` matches between backend and frontend (if applicable)

### Issue: Tasks not loading after signin

**Solution**:
- Check browser console for errors
- Verify backend is running (https://kiran-ahmed-todo-phase-3.hf.space/docs)
- Check Network tab for API request status
- Ensure JWT token is included in Authorization header

---

## Development Workflow

### Running Tests

**Backend Tests**:
```bash
cd backend
pytest --cov=src --cov-report=html
```

**Frontend Tests** (if implemented):
```bash
cd frontend
npm run test        # Unit tests
npm run test:e2e    # E2E tests with Playwright
```

### Code Formatting

**Backend**:
```bash
cd backend
black src/           # Format code
mypy src/            # Type checking
```

**Frontend**:
```bash
cd frontend
npm run lint         # ESLint
npm run format       # Prettier
```

### Database Migrations

**Create new migration**:
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

**Rollback migration**:
```bash
alembic downgrade -1
```

---

## Environment Variables Reference

### Backend (`backend/.env`)

| Variable          | Required | Default | Description |
|-------------------|----------|---------|-------------|
| `DATABASE_URL`    | ✅ Yes   | -       | Neon PostgreSQL connection string |
| `JWT_SECRET`      | ✅ Yes   | -       | Secret key for JWT signing (min 32 chars) |
| `JWT_EXPIRY_DAYS` | No       | 7       | JWT token expiry in days |
| `CORS_ORIGINS`    | ✅ Yes   | -       | Comma-separated list of allowed origins |

### Frontend (`frontend/.env.local`)

| Variable               | Required | Default | Description |
|------------------------|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL`  | ✅ Yes   | -       | Backend API base URL |
| `NEXT_PUBLIC_APP_URL`  | ✅ Yes   | -       | Frontend application URL |

---

## Project Structure Overview

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
        ├── quickstart.md    # This file
        └── contracts/       # API contracts (OpenAPI)
```

---

## Next Steps

After completing the quickstart:

1. **Explore API Documentation**: https://kiran-ahmed-todo-phase-3.hf.space/docs
2. **Review Specifications**: See `specs/todo-app-phase-ii/spec.md`
3. **Run Tests**: Execute backend and frontend test suites
4. **Implement Features**: Follow the task breakdown in `tasks.md` (generated via `/sp.tasks`)
5. **Deploy**: See deployment instructions in `specs/todo-app-phase-ii/plan.md`

---

## Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Next.js Documentation**: https://nextjs.org/docs
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com/
- **Better Auth Documentation**: https://better-auth.com/
- **Neon Documentation**: https://neon.tech/docs
- **Tailwind CSS**: https://tailwindcss.com/docs

---

## Getting Help

If you encounter issues not covered in troubleshooting:

1. Check backend logs (terminal running `uvicorn`)
2. Check frontend console (browser DevTools)
3. Review API documentation: https://kiran-ahmed-todo-phase-3.hf.space/docs
4. Check Neon database status in console
5. Consult project specifications in `specs/todo-app-phase-ii/`

---

**Quickstart Guide Status**: ✅ Complete
**Last Updated**: 2026-01-02
**Ready for Development**: Yes
