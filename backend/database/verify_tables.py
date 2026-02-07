"""
Script to verify tables exist and are accessible in Supabase
"""

import os
from dotenv import load_dotenv
from supabase import create_client
from config import Config

load_dotenv()

def verify_tables():
    """Verify that all required tables exist and are accessible"""
    
    print("="*60)
    print("Verifying Supabase Tables")
    print("="*60)
    
    try:
        supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        
        # List of required tables
        required_tables = ['users', 'markets', 'positions', 'trades', 'oracle_reports']
        
        print("\nChecking tables...")
        print("-"*60)
        
        for table in required_tables:
            try:
                # Try to query the table (even if empty)
                response = supabase.table(table).select('*').limit(1).execute()
                print(f"✅ {table:20} - Found and accessible")
            except Exception as e:
                error_msg = str(e)
                if 'PGRST205' in error_msg or 'schema cache' in error_msg.lower():
                    print(f"⚠️  {table:20} - Exists but not in schema cache")
                    print(f"   Solution: Wait 10-30 seconds or restart Supabase project")
                elif 'permission' in error_msg.lower() or 'policy' in error_msg.lower():
                    print(f"❌ {table:20} - Permission denied (check RLS policies)")
                else:
                    print(f"❌ {table:20} - Error: {error_msg[:50]}")
        
        print("-"*60)
        print("\nIf you see schema cache errors:")
        print("1. Wait 10-30 seconds for PostgREST to refresh")
        print("2. Or restart your Supabase project")
        print("3. Or run: SELECT pg_notify('pgrst', 'reload schema');")
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"\n❌ Connection Error: {str(e)}")
        print("\nPlease check:")
        print("1. SUPABASE_URL in .env file")
        print("2. SUPABASE_KEY in .env file")
        print("3. Internet connection")

if __name__ == '__main__':
    verify_tables()

