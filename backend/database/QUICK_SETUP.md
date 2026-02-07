# Quick Database Setup

## Step-by-Step Instructions

### 1. Open Supabase Dashboard
- Go to: https://supabase.com/dashboard
- Select your project (or create one if you haven't)

### 2. Open SQL Editor
- Click **"SQL Editor"** in the left sidebar
- Click **"New Query"** button

### 3. Copy and Paste Schema
- Open the file: `backend/database/schema.sql`
- Copy **ALL** the contents (Ctrl+A, Ctrl+C)
- Paste into the SQL Editor (Ctrl+V)

### 4. Execute SQL
- Click the **"Run"** button (or press Ctrl+Enter)
- Wait for execution to complete
- You should see "Success. No rows returned"

### 5. Verify Tables
- Click **"Table Editor"** in the left sidebar
- You should see 5 tables:
  - ✅ users
  - ✅ markets
  - ✅ positions
  - ✅ trades
  - ✅ oracle_reports

## That's It!

Your database is now set up. You can:
- Test the backend API endpoints
- Create users via `/auth/initialize`
- Submit markets via `/markets/submit`

## Troubleshooting

**If you get an error about "uuid-ossp" extension:**
- The schema includes `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";`
- This should work automatically in Supabase
- If it doesn't, Supabase may have already enabled it

**If you get permission errors:**
- The schema includes Row Level Security (RLS) policies
- They're set to allow all operations for development
- This should work, but if not, check your Supabase project settings

**If tables already exist:**
- The schema uses `CREATE TABLE IF NOT EXISTS`
- It's safe to run multiple times
- Existing data won't be deleted

