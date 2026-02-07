"""Supabase client utility"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv
from config import Config

# Load environment variables
load_dotenv()

_supabase_client: Client = None

def get_supabase_client() -> Client:
    """Get or create Supabase client singleton"""
    global _supabase_client
    
    if _supabase_client is None:
        if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
            raise ValueError("Supabase URL and KEY must be set in environment variables")
        
        _supabase_client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
    
    return _supabase_client

def reset_supabase_client():
    """Reset Supabase client (useful for testing)"""
    global _supabase_client
    _supabase_client = None

def execute_query(table, action, data=None, filters=None):
    """
    Helper function to execute Supabase queries
    
    Args:
        table: Table name
        action: Action to perform ('select', 'insert', 'update', 'delete')
        data: Data for insert/update operations
        filters: Dictionary of filters for select/update/delete (e.g., {'id': 1})
    
    Returns:
        Query result
    """
    supabase = get_supabase_client()
    query = supabase.table(table)
    
    # Apply filters
    if filters:
        for key, value in filters.items():
            query = query.eq(key, value)
    
    # Execute action
    if action == 'select':
        result = query.select('*').execute()
        return result.data
    elif action == 'insert':
        if not data:
            raise ValueError("Data required for insert operation")
        result = query.insert(data).execute()
        return result.data
    elif action == 'update':
        if not data:
            raise ValueError("Data required for update operation")
        if not filters:
            raise ValueError("Filters required for update operation")
        result = query.update(data).execute()
        return result.data
    elif action == 'delete':
        if not filters:
            raise ValueError("Filters required for delete operation")
        result = query.delete().execute()
        return result.data
    else:
        raise ValueError(f"Unknown action: {action}")

