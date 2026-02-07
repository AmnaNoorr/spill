-- Refresh PostgREST schema cache
-- Run this in Supabase SQL Editor if tables exist but aren't accessible

-- Method 1: Notify PostgREST to reload schema
NOTIFY pgrst, 'reload schema';

-- Method 2: Check if tables exist in public schema
SELECT 
    table_name,
    table_schema
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('users', 'markets', 'positions', 'trades', 'oracle_reports')
ORDER BY table_name;

-- Method 3: Verify table structures
SELECT 
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public' 
AND table_name = 'users'
ORDER BY ordinal_position;

-- Method 4: Check RLS policies
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual
FROM pg_policies
WHERE schemaname = 'public'
AND tablename IN ('users', 'markets', 'positions', 'trades', 'oracle_reports');

