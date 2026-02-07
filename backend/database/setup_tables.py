"""
Script to set up database tables in Supabase
This script reads the schema.sql file and executes it via Supabase API
"""

import os
import sys
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv
from config import Config

# Load environment variables
load_dotenv()

def setup_database():
    """Set up database tables by executing SQL schema"""
    
    # Read schema SQL file
    schema_file = Path(__file__).parent / 'schema.sql'
    
    if not schema_file.exists():
        print(f"Error: Schema file not found at {schema_file}")
        return False
    
    with open(schema_file, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    # Split SQL into individual statements
    # Remove comments and split by semicolons
    statements = []
    current_statement = ""
    
    for line in schema_sql.split('\n'):
        # Skip comment lines
        if line.strip().startswith('--'):
            continue
        
        current_statement += line + '\n'
        
        # If line ends with semicolon, it's a complete statement
        if line.strip().endswith(';'):
            stmt = current_statement.strip()
            if stmt:
                statements.append(stmt)
            current_statement = ""
    
    # Add any remaining statement
    if current_statement.strip():
        statements.append(current_statement.strip())
    
    print(f"Found {len(statements)} SQL statements to execute")
    
    # Note: Supabase Python client doesn't directly support executing raw SQL
    # You need to use the Supabase SQL Editor or REST API
    # This script provides instructions instead
    
    print("\n" + "="*60)
    print("DATABASE SETUP INSTRUCTIONS")
    print("="*60)
    print("\nThe Supabase Python client doesn't support executing raw SQL directly.")
    print("Please follow these steps to set up your database:\n")
    print("1. Go to your Supabase Dashboard: https://supabase.com/dashboard")
    print("2. Select your project")
    print("3. Go to 'SQL Editor' in the left sidebar")
    print("4. Click 'New Query'")
    print("5. Copy and paste the contents of 'backend/database/schema.sql'")
    print("6. Click 'Run' to execute the SQL")
    print("\nAlternatively, you can use the Supabase CLI or REST API.")
    print("\n" + "="*60)
    
    # Print the SQL for easy copying
    print("\nSQL Schema to execute:\n")
    print("-"*60)
    print(schema_sql)
    print("-"*60)
    
    return True

if __name__ == '__main__':
    try:
        setup_database()
        print("\n✓ Setup instructions displayed successfully")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)

