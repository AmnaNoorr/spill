# Fix "Schema Cache" Error

## Problem
You're getting errors like:
```
Could not find the table 'public.users' in the schema cache
```

This means the tables exist in your database, but PostgREST (Supabase's API layer) hasn't refreshed its cache yet.

## Quick Fixes (Try in Order)

### Fix 1: Refresh Schema Cache (Recommended)

1. Go to Supabase Dashboard → SQL Editor
2. Run this command:

```sql
NOTIFY pgrst, 'reload schema';
```

3. Wait 5-10 seconds
4. Try your API calls again

### Fix 2: Restart Supabase Project

1. Go to Supabase Dashboard
2. Click on your project settings
3. Find "Restart" or "Pause/Resume" option
4. Restart the project
5. Wait 1-2 minutes for it to come back online

### Fix 3: Verify Tables Exist

Run this in SQL Editor to confirm tables exist:

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('users', 'markets', 'positions', 'trades', 'oracle_reports');
```

You should see all 5 tables listed.

### Fix 4: Check API Key

Make sure you're using the correct API key:
- Use the **anon** or **service_role** key (not the publishable key)
- Check in: Supabase Dashboard → Settings → API

### Fix 5: Verify RLS Policies

If tables exist but you still get errors, check RLS:

```sql
SELECT tablename, policyname 
FROM pg_policies 
WHERE schemaname = 'public';
```

Make sure policies exist for all tables.

## Test After Fix

Run this Python script to verify:

```bash
cd backend
python database/verify_tables.py
```

Or test via API:
```bash
curl http://localhost:5000/health
```

## Still Not Working?

1. **Check Supabase Logs:**
   - Dashboard → Logs → API Logs
   - Look for any errors

2. **Verify Connection:**
   - Check your `.env` file has correct `SUPABASE_URL` and `SUPABASE_KEY`
   - Test connection: `python -c "from utils.supabase_client import get_supabase_client; print(get_supabase_client())"`

3. **Check Table Schema:**
   - Make sure tables are in the `public` schema
   - Verify column names match your code

4. **Contact Support:**
   - If nothing works, the issue might be with Supabase project configuration

