# Database Setup Guide

This directory contains the database schema and setup scripts for SipNSecret.

## Quick Setup

### Option 1: Using Supabase SQL Editor (Recommended)

1. **Open Supabase Dashboard**
   - Go to https://supabase.com/dashboard
   - Select your project

2. **Open SQL Editor**
   - Click "SQL Editor" in the left sidebar
   - Click "New Query"

3. **Execute Schema**
   - Open `schema.sql` in this directory
   - Copy the entire contents
   - Paste into the SQL Editor
   - Click "Run" (or press Ctrl+Enter)

4. **Verify Tables**
   - Go to "Table Editor" in the left sidebar
   - You should see these tables:
     - `users`
     - `markets`
     - `positions`
     - `trades`
     - `oracle_reports`

### Option 2: Using Supabase CLI

```bash
# Install Supabase CLI (if not installed)
npm install -g supabase

# Login to Supabase
supabase login

# Link your project
supabase link --project-ref your-project-ref

# Run the schema
supabase db push --file database/schema.sql
```

### Option 3: Using Python Script

```bash
cd backend
python database/setup_tables.py
```

This will display instructions and the SQL to copy.

## Schema Overview

### Tables Created

1. **users**
   - Stores user accounts with pseudonyms
   - Tracks balances (available, locked, earned, lost)
   - New users get 100 CC by default

2. **markets**
   - Stores prediction markets
   - Tracks bets (true/false), prices, status
   - Includes AI predictions and embeddings

3. **positions**
   - User positions in markets
   - Tracks shares, entry price, collateral
   - Status: 'open' or 'closed'

4. **trades**
   - Transaction history
   - Records all bets placed

5. **oracle_reports**
   - Oracle submissions for market resolution
   - Includes evidence and AI summaries

## Important Notes

### Vector Extension (for embeddings)

If you want to use the `embedding` column in the markets table, you need to enable the `pgvector` extension:

```sql
-- In Supabase SQL Editor
CREATE EXTENSION IF NOT EXISTS vector;
```

If you don't need embeddings, you can remove the `embedding` column from the schema or set it to `TEXT` type instead.

### Row Level Security (RLS)

The schema enables RLS with permissive policies for development. **For production, you should:**

1. Review and restrict RLS policies
2. Set up proper authentication
3. Create user-specific policies

### UUIDs

All tables use UUIDs as primary keys. The schema includes the `uuid-ossp` extension to generate UUIDs automatically.

## Verification

After running the schema, verify the setup:

```sql
-- Check if tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('users', 'markets', 'positions', 'trades', 'oracle_reports');

-- Check table structures
\d users
\d markets
\d positions
\d trades
\d oracle_reports
```

## Troubleshooting

### Error: "extension 'uuid-ossp' does not exist"
- The extension should be enabled automatically
- If not, run: `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";`

### Error: "extension 'vector' does not exist"
- Only needed if using embeddings
- Install pgvector extension in Supabase
- Or remove the embedding column from the schema

### Error: "relation already exists"
- Tables already exist, this is fine
- The `CREATE TABLE IF NOT EXISTS` should prevent errors
- You can drop tables and recreate if needed

### RLS Policy Errors
- If you get permission errors, check RLS policies
- For development, the schema creates permissive policies
- Adjust based on your security needs

## Next Steps

After setting up the database:

1. **Test the connection:**
   ```bash
   cd backend
   python -c "from utils.supabase_client import get_supabase_client; print('Connected:', get_supabase_client())"
   ```

2. **Test creating a user:**
   - Use the `/auth/initialize` endpoint
   - Check Supabase Table Editor to see the user

3. **Test creating a market:**
   - Use the `/markets/submit` endpoint
   - Verify the market appears in Supabase

## Support

If you encounter issues:
1. Check Supabase logs in the dashboard
2. Verify your `.env` file has correct credentials
3. Check the Flask backend logs for detailed errors

