-- Migration: Add versioning and oracle reputation support
-- Run this SQL in your Supabase SQL Editor

-- Add parent_market_id to markets table for versioning (FR-2.4)
ALTER TABLE markets 
ADD COLUMN IF NOT EXISTS parent_market_id UUID REFERENCES markets(id) ON DELETE SET NULL,
ADD COLUMN IF NOT EXISTS version_number INTEGER DEFAULT 1;

-- Add oracle reputation fields to users table (FR-5.5)
ALTER TABLE users
ADD COLUMN IF NOT EXISTS oracle_reputation DECIMAL(5, 2) DEFAULT 50.0 CHECK (oracle_reputation >= 0 AND oracle_reputation <= 100),
ADD COLUMN IF NOT EXISTS oracle_reports_count INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS oracle_correct_count INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS oracle_incorrect_count INTEGER DEFAULT 0;

-- Add index for parent_market_id
CREATE INDEX IF NOT EXISTS idx_markets_parent_market ON markets(parent_market_id);

-- Add index for oracle reputation
CREATE INDEX IF NOT EXISTS idx_users_oracle_reputation ON users(oracle_reputation DESC);

-- Update oracle_reports table to track if report was correct
ALTER TABLE oracle_reports
ADD COLUMN IF NOT EXISTS was_correct BOOLEAN,
ADD COLUMN IF NOT EXISTS reputation_awarded DECIMAL(5, 2) DEFAULT 0.0;

