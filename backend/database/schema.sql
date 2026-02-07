-- SipNSecret Database Schema for Supabase
-- Run this SQL in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pseudonym VARCHAR(255) UNIQUE NOT NULL,
    available_balance DECIMAL(15, 2) DEFAULT 100.0 NOT NULL,
    locked_balance DECIMAL(15, 2) DEFAULT 0.0 NOT NULL,
    total_earned DECIMAL(15, 2) DEFAULT 0.0 NOT NULL,
    total_lost DECIMAL(15, 2) DEFAULT 0.0 NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Markets table
CREATE TABLE IF NOT EXISTS markets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    text TEXT NOT NULL,
    category VARCHAR(100),
    submitter_id UUID REFERENCES users(id) ON DELETE SET NULL,
    stake DECIMAL(15, 2) DEFAULT 0.0 NOT NULL,
    price DECIMAL(5, 4) DEFAULT 0.5 NOT NULL CHECK (price >= 0.01 AND price <= 0.99),
    total_bet_true DECIMAL(15, 2) DEFAULT 0.0 NOT NULL,
    total_bet_false DECIMAL(15, 2) DEFAULT 0.0 NOT NULL,
    status VARCHAR(50) DEFAULT 'active' NOT NULL,
    ai_prediction VARCHAR(50),
    ai_confidence INTEGER,
    embedding TEXT, -- Store embeddings as JSON string (or use VECTOR(1536) if pgvector extension is enabled)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE
);

-- Positions table
CREATE TABLE IF NOT EXISTS positions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    market_id UUID REFERENCES markets(id) ON DELETE CASCADE NOT NULL,
    type VARCHAR(10) NOT NULL CHECK (type IN ('true', 'false')),
    shares DECIMAL(15, 4) DEFAULT 0.0 NOT NULL,
    entry_price DECIMAL(5, 4) NOT NULL CHECK (entry_price >= 0.01 AND entry_price <= 0.99),
    cost_basis DECIMAL(15, 2) DEFAULT 0.0 NOT NULL,
    collateral DECIMAL(15, 2) DEFAULT 0.0 NOT NULL,
    status VARCHAR(50) DEFAULT 'open' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Trades table (transaction history)
CREATE TABLE IF NOT EXISTS trades (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    market_id UUID REFERENCES markets(id) ON DELETE CASCADE NOT NULL,
    type VARCHAR(10) NOT NULL CHECK (type IN ('true', 'false')),
    cc_amount DECIMAL(15, 2) NOT NULL,
    shares DECIMAL(15, 4) NOT NULL,
    price DECIMAL(5, 4) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Oracle reports
CREATE TABLE IF NOT EXISTS oracle_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    oracle_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    market_id UUID REFERENCES markets(id) ON DELETE CASCADE NOT NULL,
    verdict VARCHAR(10) NOT NULL CHECK (verdict IN ('true', 'false')),
    evidence JSONB DEFAULT '[]'::jsonb,
    stake DECIMAL(15, 2) DEFAULT 0.0 NOT NULL,
    ai_summary TEXT,
    status VARCHAR(50) DEFAULT 'pending' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_users_pseudonym ON users(pseudonym);
CREATE INDEX IF NOT EXISTS idx_markets_status ON markets(status);
CREATE INDEX IF NOT EXISTS idx_markets_category ON markets(category);
CREATE INDEX IF NOT EXISTS idx_markets_submitter ON markets(submitter_id);
CREATE INDEX IF NOT EXISTS idx_markets_created_at ON markets(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_positions_user_id ON positions(user_id);
CREATE INDEX IF NOT EXISTS idx_positions_market_id ON positions(market_id);
CREATE INDEX IF NOT EXISTS idx_positions_status ON positions(status);
CREATE INDEX IF NOT EXISTS idx_trades_user_id ON trades(user_id);
CREATE INDEX IF NOT EXISTS idx_trades_market_id ON trades(market_id);
CREATE INDEX IF NOT EXISTS idx_trades_created_at ON trades(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_oracle_reports_market_id ON oracle_reports(market_id);
CREATE INDEX IF NOT EXISTS idx_oracle_reports_oracle_id ON oracle_reports(oracle_id);
CREATE INDEX IF NOT EXISTS idx_oracle_reports_status ON oracle_reports(status);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to auto-update updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_markets_updated_at BEFORE UPDATE ON markets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_positions_updated_at BEFORE UPDATE ON positions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_oracle_reports_updated_at BEFORE UPDATE ON oracle_reports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS) - Optional, adjust based on your needs
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE markets ENABLE ROW LEVEL SECURITY;
ALTER TABLE positions ENABLE ROW LEVEL SECURITY;
ALTER TABLE trades ENABLE ROW LEVEL SECURITY;
ALTER TABLE oracle_reports ENABLE ROW LEVEL SECURITY;

-- Create policies to allow all operations (adjust based on your security needs)
-- For development, we'll allow all operations. In production, you should restrict these.

CREATE POLICY "Allow all operations on users" ON users
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Allow all operations on markets" ON markets
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Allow all operations on positions" ON positions
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Allow all operations on trades" ON trades
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Allow all operations on oracle_reports" ON oracle_reports
    FOR ALL USING (true) WITH CHECK (true);

