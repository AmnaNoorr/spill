# Spill - Cryptocurrency Prediction Market Platform

A full-stack cryptocurrency portfolio management and prediction market platform with oracle consensus mechanisms, AI-powered evidence summarization, and advanced market analytics.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [API Reference](#api-reference)
- [Database Schema](#database-schema)
- [Key Features](#key-features)
- [Contributing](#contributing)

## 🎯 Overview

**Spill** is a decentralized prediction market platform built on blockchain principles. Users can:

- **Create Markets** - Submit cryptocurrency-related rumors/predictions with locked collateral
- **Trade Positions** - Buy and sell positions on market outcomes before resolution
- **Submit Oracle Reports** - Provide evidence-based truth verdicts on markets
- **Earn Reputation** - Build credibility through accurate oracle reporting
- **Manage Portfolios** - Track positions, earnings, and market exposure

The platform implements sophisticated consensus mechanisms, AI-powered evidence analysis, and duplicate detection to ensure market integrity.

## 🏗️ Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React + Vite)                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Components: Markets, Trades, Oracles, Portfolio, Auth    │   │
│  │ State Management: React Hooks, API Service               │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┬───────────────────────────────┘
          ↓ HTTP/REST API           ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Backend API (Flask + Python)                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Routes:    /auth, /markets, /oracles                     │   │
│  │ Services:  Market, Oracle, AI, Similarity, Reputation    │   │
│  │ Middleware: Rate Limiting, CORS                          │   │
│  │ Utilities: Supabase Client, OpenAI Integration           │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┬───────────────────────────────┘
          ↓ SQL Queries            ↓
┌─────────────────────────────────────────────────────────────────┐
│                Supabase PostgreSQL Database                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Tables: users, markets, positions, positions_settled    │   │
│  │         oracle_reports, market_resolutions, ...          │   │
│  │ Features: RLS, Versioning, Audit Trail                   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
          ↓ API Calls              ↓
┌─────────────────────────────────────────────────────────────────┐
│              External Services                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐  │
│  │ OpenAI API     │  │ Market Data    │  │ Other Services   │  │
│  │ (AI Summary)   │  │ APIs (Future)  │  │                  │  │
│  └────────────────┘  └────────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow Pipeline

```
┌──────────────────┐
│  User Submits    │
│  Market Rumor    │
└────────┬─────────┘
         ↓
┌──────────────────────────────────┐
│ Frontend Validation              │
│ - Input validation               │
│ - Format checking                │
└────────┬─────────────────────────┘
         ↓
┌──────────────────────────────────┐
│ Backend Receives Request         │
│ POST /markets/submit             │
└────────┬─────────────────────────┘
         ↓
┌──────────────────────────────────┐
│ Similarity Detection             │
│ - TF-IDF Analysis                │
│ - Cosine Similarity (>0.7)       │
│ - Reject Duplicates              │
└────────┬─────────────────────────┘
         ↓
┌──────────────────────────────────┐
│ Database Storage                 │
│ - Save market record             │
│ - Lock collateral from user      │
│ - Initialize positions table     │
└────────┬─────────────────────────┘
         ↓
┌──────────────────────────────────┐
│ Market Open for Trading          │
│ - Users can trade positions      │
│ - Buy/Sell mechanisms            │
│ - Portfolio tracking             │
└────────┬─────────────────────────┘
         ↓
┌──────────────────────────────────┐
│ Oracles Submit Evidence          │
│ POST /oracles/submit             │
│ - Verdict (true/false)           │
│ - Evidence URLs                  │
│ - Optional stake                 │
└────────┬─────────────────────────┘
         ↓
┌──────────────────────────────────┐
│ AI Evidence Summarization        │
│ - OpenAI GPT Analysis            │
│ - Auto-generate summary          │
│ - Store summary in DB            │
└────────┬─────────────────────────┘
         ↓
┌──────────────────────────────────┐
│ Consensus Check                  │
│ - Aggregate all oracle votes     │
│ - Calculate true_votes %         │
│ - Check 60% threshold            │
└────────┬─────────────────────────┘
         ↓
     ┌───────────────────────────────────────┐
     │                                       │
 ┌───┴────────────┐            ┌────────────┴──┐
 │                ↓            ↓               │
 │ NO CONSENSUS   │  CONSENSUS │  REACHED     │
 │                │            │              │
 │         (Still │  ┌─────────┴──┐          │
 │         Open)  │  │             ↓          │
 │                │  │  Market Resolution     │
 │                │  │  POST /oracles/resolve│
 │                │  │                        │
 │                │  │  ┌──────────────────┐  │
 │                │  └─→│ Settlement Calc   │  │
 │                │     │ - True payouts    │  │
 │                │     │ - False payouts   │  │
 │                │     │ - Fee collection  │  │
 │                │     └┬────────────────┬─┘  │
 │                │      │                │    │
 │                │      ↓                ↓    │
 │                │  Distribute Funds    Close │
 │                │  Close Positions     Market│
 │                │  Update Reputation   Status│
 │                │                           │
 └────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

### Frontend
- **Framework:** React 18.2.0
- **Build Tool:** Vite 5.1.5
- **UI Icons:** lucide-react 0.344.0
- **Styling:** CSS with CSS Variables
- **HTTP Client:** Fetch API / Axios

### Backend
- **Framework:** Flask 3.0.0
- **Language:** Python 3.x
- **CORS:** Flask-CORS 4.0.0
- **Database ORM:** Supabase 2.3.0
- **AI/ML:** OpenAI API 1.12.0
- **Scientific Computing:** NumPy 1.26.0
- **Production Server:** Gunicorn 21.2.0

### Database
- **Primary:** PostgreSQL (via Supabase)
- **Authentication:** Supabase Auth
- **Real-time:** Supabase Subscriptions (optional)

### External Services
- **AI Analysis:** OpenAI GPT (Evidence Summarization)
- **Backend Hosting:** Any Python-capable server (Heroku, AWS, GCP, etc.)
- **Frontend Hosting:** Any static host (Vercel, Netlify, AWS S3, etc.)

## 📁 Project Structure

```
spill/
├── frontend/                    # React + Vite Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx              # Top navigation
│   │   │   ├── Markets.jsx             # Market listing & display
│   │   │   ├── Oracle.jsx              # Oracle report submission
│   │   │   ├── PortfolioSidebar.jsx    # Portfolio dashboard
│   │   │   ├── SplashScreen.jsx        # Intro screen
│   │   │   ├── Submit.jsx              # Market creation form
│   │   │   └── TradeModal.jsx          # Position trading UI
│   │   ├── hooks/
│   │   │   └── useAuth.js              # Authentication hook
│   │   ├── services/
│   │   │   └── api.js                  # API communication layer
│   │   ├── styles/
│   │   │   ├── global.css              # Global styles
│   │   │   └── variables.css           # CSS variables & theme
│   │   ├── App.jsx                     # Root component
│   │   └── main.jsx                    # Entry point
│   ├── index.html                      # HTML template
│   ├── package.json                    # Dependencies
│   └── vite.config.js                  # Vite configuration
│
├── backend/                     # Flask Backend API
│   ├── routes/
│   │   ├── auth.py                     # Auth endpoints
│   │   ├── markets.py                  # Market management endpoints
│   │   └── oracles.py                  # Oracle submission endpoints
│   ├── services/
│   │   ├── ai_service.py               # OpenAI integration
│   │   ├── evidence_service.py         # Evidence management
│   │   ├── market_service.py           # Market business logic
│   │   ├── oracle_service.py           # Oracle consensus logic
│   │   ├── reputation_service.py       # Reputation tracking
│   │   └── similarity_service.py       # TF-IDF duplicate detection
│   ├── models/
│   │   ├── user.py                     # User data model
│   │   ├── market.py                   # Market data model
│   │   └── position.py                 # Position data model
│   ├── middleware/
│   │   └── rate_limit.py               # Rate limiting middleware
│   ├── utils/
│   │   └── supabase_client.py          # Supabase initialization
│   ├── database/
│   │   ├── schema.sql                  # Database schema
│   │   ├── setup_tables.py             # Table initialization
│   │   ├── verify_tables.py            # Schema verification
│   │   └── migration_*.sql             # Database migrations
│   ├── app.py                          # Flask app factory
│   ├── config.py                       # Configuration
│   ├── run.py                          # Entry point
│   └── requirements.txt                # Python dependencies
│
├── database/                    # Database configuration
│   ├── schema.sql                      # Full schema definition
│   ├── setup_tables.py                 # Automated setup
│   └── README.md                       # Database docs
│
├── docs/                        # Documentation
│   ├── BACKEND_SETUP.md                # Backend setup guide
│   ├── DEVELOPMENT.md                  # Development guide
│   ├── FRONTEND_BACKEND_INTEGRATION.md # Integration guide
│   └── ENV_SETUP.md                    # Environment setup
│
├── API_REFERENCE.md             # Complete API documentation
├── IMPLEMENTATION_SUMMARY.md    # Feature implementation details
├── NEW_FEATURES_SUMMARY.md      # Recent additions
├── README.md                    # This file
└── .env.example                 # Environment template

```

## ⚡ Getting Started

### Prerequisites
- Node.js v16+ (for frontend)
- Python 3.8+ (for backend)
- Supabase account
- OpenAI API key

### Backend Setup

1. **Clone and navigate:**
```bash
git clone <repo-url>
cd spill/backend
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your credentials:
# SUPABASE_URL=your_supabase_url
# SUPABASE_KEY=your_supabase_key
# OPENAI_API_KEY=your_openai_key
```

5. **Initialize database:**
```bash
cd database
python setup_tables.py  # Creates all tables
python verify_tables.py # Verifies schema
cd ..
```

6. **Start backend server:**
```bash
python run.py
```
Backend runs at `http://localhost:5000`

### Frontend Setup

1. **Navigate and install:**
```bash
cd spill/frontend
npm install
```

2. **Update API configuration:**
Edit `src/services/api.js` to point to your backend:
```javascript
const API_BASE_URL = 'http://localhost:5000';
```

3. **Start development server:**
```bash
npm run dev
```
Frontend runs at `http://localhost:5173`

### Production Build

**Frontend:**
```bash
npm run build  # Creates dist/ folder
# Deploy dist/ to static hosting
```

**Backend:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 🔄 Development Workflow

### Making Changes

1. **Backend:**
```bash
# Update service/route logic
# Test via Postman or curl
# Changes auto-reload on save
```

2. **Frontend:**
```bash
# Update components/styles
# Hot module replacement (HMR) auto-updates
npm run dev
```

### Testing Endpoints

```bash
# Health check
curl http://localhost:5000/health

# Submit market
curl -X POST http://localhost:5000/markets/submit \
  -H "Content-Type: application/json" \
  -d '{"title": "ETH will reach $5000", "submitter_id": "user123"}'

# Submit oracle report
curl -X POST http://localhost:5000/oracles/submit \
  -H "Content-Type: application/json" \
  -d '{"oracle_id": "user123", "market_id": "market123", "verdict": "true", "evidence": ["url1", "url2"]}'
```

## 📡 API Reference

### Market Management

**Create Market**
```
POST /markets/submit
{
  "title": "string",
  "description": "string",
  "submitter_id": "uuid",
  "collateral": number
}
Response: { market_id, status, message }
```

**Get Markets**
```
GET /markets/list
Response: [{ id, title, status, collateral, ... }]
```

**Trade Position**
```
POST /markets/<market_id>/bet
{
  "user_id": "uuid",
  "position": "true" | "false",
  "amount": number
}
Response: { position_id, status, message }
```

**Delete Market**
```
DELETE /markets/<market_id>/delete
{
  "user_id": "uuid"
}
Response: { message, refunded_amount, positions_closed }
```

### Oracle Management

**Submit Report**
```
POST /oracles/submit
{
  "oracle_id": "uuid",
  "market_id": "uuid",
  "verdict": "true" | "false",
  "evidence": ["url1", "url2"],
  "stake": number (optional)
}
Response: { report_id, ai_summary, consensus }
```

**Get Reports**
```
GET /oracles/reports/<market_id>
Response: [{ report, ai_summary, verdict, ... }]
```

**Resolve Market**
```
POST /oracles/resolve
{
  "market_id": "uuid",
  "outcome": "true" | "false" (optional)
}
Response: { settlement_data, payouts, ... }
```

For complete API reference, see [API_REFERENCE.md](API_REFERENCE.md)

## 🗄️ Database Schema

### Core Tables

**users**
- `id`: UUID (primary key)
- `pseudonym`: string
- `reputation_score`: number (default: 0)
- `total_earnings`: number (default: 0)
- `total_predictions`: number (default: 0)

**markets**
- `id`: UUID (primary key)
- `title`: string
- `description`: text
- `submitter_id`: UUID (foreign key → users)
- `status`: enum ('active', 'resolved', 'deleted')
- `collateral_locked`: number
- `created_at`: timestamp
- `resolved_at`: timestamp (nullable)

**positions**
- `id`: UUID (primary key)
- `market_id`: UUID (foreign key → markets)
- `user_id`: UUID (foreign key → users)
- `position`: enum ('true', 'false')
- `amount`: number
- `status`: enum ('active', 'settled', 'closed')

**oracle_reports**
- `id`: UUID (primary key)
- `market_id`: UUID (foreign key → markets)
- `oracle_id`: UUID (foreign key → users)
- `verdict`: enum ('true', 'false')
- `evidence`: text array
- `ai_summary`: text
- `stake`: number (nullable)
- `created_at`: timestamp

For full schema details, see [database/schema.sql](backend/database/schema.sql)

## ✨ Key Features

### 1. **Oracle Consensus Mechanism**
- Reports aggregated to determine market truth
- 60% consensus threshold
- Automatic settlement when consensus reached
- Prevents duplicate reports from same oracle

### 2. **AI Evidence Summarization**
- OpenAI GPT integration
- Automatic extraction of evidence summaries
- Human-readable report generation

### 3. **Duplicate Detection**
- TF-IDF (Term Frequency-Inverse Document Frequency) analysis
- Cosine similarity matching (>0.7 threshold)
- Prevents duplicate market submissions

### 4. **Rate Limiting**
- Market submissions: 5 requests/minute per user
- Trading: 20 requests/minute per user
- Prevents API abuse

### 5. **Reputation System**
- Tracks oracle accuracy
- Awards points for correct predictions
- Penalizes incorrect verdicts
- Influences user credibility

### 6. **Portfolio Management**
- Real-time position tracking
- Earnings calculation
- Risk assessment
- Trading history

### 7. **Market Lifecycle Management**
- Create, trade, resolve, delete flow
- Automatic fund distribution
- Audit trail for all transactions

## 🤝 Contributing

1. **Create feature branch:**
```bash
git checkout -b feature/your-feature
```

2. **Make changes following code style:**
   - Backend: PEP 8 Python
   - Frontend: ESLint + Prettier

3. **Test thoroughly:**
   - Test API endpoints
   - Test frontend components
   - Verify database consistency

4. **Commit with clear messages:**
```bash
git commit -m "feat: add new oracle verification system"
```

5. **Push and create PR:**
```bash
git push origin feature/your-feature
```

## 📚 Additional Documentation

- [Backend Setup](docs/BACKEND_SETUP.md) - Detailed backend configuration
- [Development Guide](docs/DEVELOPMENT.md) - Development best practices
- [Frontend-Backend Integration](docs/FRONTEND_BACKEND_INTEGRATION.md) - Integration guide
- [Environment Setup](backend/ENV_SETUP.md) - Environment variable guide
- [API Reference](API_REFERENCE.md) - Complete API documentation
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md) - Feature details

## 📄 License

Proprietary - All rights reserved

## 🆘 Support

For issues, questions, or suggestions, please open an issue on the repository.
