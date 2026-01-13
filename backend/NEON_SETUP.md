# Neon Database Setup Guide

## Step 1: Get Your Neon Connection String

1. Go to your Neon Console: https://console.neon.tech
2. Select your project: **todo-app**
3. Go to **Connection Details** or click on your branch
4. Copy the connection string (it will look like this):
   ```
   postgresql://username:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

## Step 2: Create .env File

1. In the `backend` folder, create a file named `.env`
2. Add your Neon connection string in this format:
   ```env
   DATABASE_URL=postgresql+asyncpg://username:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
   
   **Important**: 
   - Change `postgresql://` to `postgresql+asyncpg://` (for async support)
   - Keep the `?sslmode=require` at the end for Neon SSL connection

3. Example:
   ```env
   DATABASE_URL=postgresql+asyncpg://kiran:password123@ep-wispy-dream-83834904.us-east-2.aws.neon.tech/neondb?sslmode=require
   JWT_SECRET=your-super-secret-jwt-secret-key-change-in-production
   JWT_EXPIRY_DAYS=7
   ```

## Step 3: Run Database Migrations

After creating the `.env` file with your Neon connection string, run:

```bash
cd backend
alembic upgrade head
```

This will create the `user` and `task` tables in your Neon database.

## Step 4: Restart Your Backend

Restart your backend server to connect to Neon:

```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Step 5: Verify Tables Are Created

1. Go back to Neon Console
2. Click on **Tables** in the left sidebar
3. You should see:
   - `user` table
   - `task` table

## Troubleshooting

If migrations fail:
- Make sure your connection string is correct
- Ensure the database exists in Neon
- Check that SSL mode is set to `require`

