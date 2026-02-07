# Frontend-Backend Integration Guide

## Overview

The React frontend is now fully integrated with the Flask backend, which communicates with Supabase. All API calls flow through Flask, ensuring proper authentication, validation, and data management.

## Architecture

```
React Frontend → Flask Backend → Supabase Database
```

### Flow:
1. **Frontend** makes API calls to Flask backend
2. **Flask** validates requests, processes business logic
3. **Flask** communicates with Supabase for data operations
4. **Flask** returns JSON responses to frontend

## Setup

### 1. Backend Setup

Ensure the Flask backend is running:

```bash
cd backend
python run.py
```

The backend will run on `http://localhost:5000`

### 2. Frontend Setup

The frontend uses Vite's proxy configuration to forward API requests to the Flask backend during development.

**Environment Variables** (create `frontend/.env`):

```env
VITE_API_URL=http://localhost:5000
```

**Start the frontend:**

```bash
cd frontend
npm run dev
```

The frontend will run on `http://localhost:5173` (or another port if 5173 is taken)

## API Service

All API calls are centralized in `frontend/src/services/api.js`:

- **authAPI**: User authentication and management
- **marketsAPI**: Market operations (get, submit, bet)
- **oracleAPI**: Oracle reports and market resolution
- **systemAPI**: Health checks and statistics

## Key Features

### 1. Authentication

- Users initialize with a pseudonym
- New users receive 100 CC automatically
- User data stored in localStorage for persistence
- Auth hook (`useAuth`) manages user state

### 2. Markets

- Fetches real markets from backend
- Displays market data (price, volume, positions)
- Supports filtering by category
- Real-time price updates after trades

### 3. Trading

- Place bets (long/short) on markets
- Real-time share calculation
- Balance validation
- Position aggregation

### 4. Market Submission

- Submit new markets with AI analysis
- Stake validation (minimum 10 CC)
- Category selection
- AI-powered duplicate detection

## Components Updated

### Markets.jsx
- Fetches markets from `/markets` endpoint
- Displays real market data
- Opens TradeModal for placing bets
- Shows loading and error states

### TradeModal.jsx
- Calculates shares based on current price
- Validates user balance
- Places bets via `/markets/<id>/bet`
- Shows real-time calculations

### Submit.jsx
- Submits markets via `/markets/submit`
- Validates stake amount
- Shows AI analysis results
- Error handling and success messages

### Header.jsx
- Displays user balance from backend
- Shows user pseudonym
- Updates in real-time

### App.jsx
- Manages authentication state
- Shows auth modal for new users
- Integrates useAuth hook

## API Endpoints Used

### Auth
- `POST /auth/initialize` - Initialize or get user
- `GET /auth/user/<id>` - Get user details
- `GET /auth/users` - Get top users

### Markets
- `GET /markets` - Get all markets (with filters)
- `GET /markets/<id>` - Get market details
- `POST /markets/submit` - Submit new market
- `POST /markets/<id>/bet` - Place a bet

### Oracle
- `POST /oracles/resolve` - Resolve a market
- `POST /oracles/submit` - Submit oracle report
- `GET /oracles/reports/<market_id>` - Get reports

### System
- `GET /health` - Health check
- `GET /stats` - System statistics

## CORS Configuration

The Flask backend is configured with CORS to allow requests from the frontend:

```python
CORS(app, resources={r"/*": {"origins": "*"}})
```

## Development Workflow

1. **Start Backend:**
   ```bash
   cd backend
   python run.py
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access Application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000

## Error Handling

All API calls include:
- Try-catch error handling
- User-friendly error messages
- Loading states
- Retry mechanisms where appropriate

## Data Flow Example: Placing a Bet

1. User clicks "Yes" or "No" on a market card
2. TradeModal opens with market details
3. User enters amount and selects position
4. Frontend calculates shares and potential return
5. On submit, `marketsAPI.placeBet()` is called
6. Flask validates the trade (balance, market status)
7. Flask updates Supabase (user balance, market totals, position)
8. Flask returns updated market and position data
9. Frontend updates UI and closes modal

## Testing

To test the integration:

1. Start both servers
2. Open frontend in browser
3. Enter a pseudonym when prompted
4. Browse markets (should load from backend)
5. Submit a new market
6. Place a bet on a market
7. Check that balances update correctly

## Troubleshooting

### CORS Errors
- Ensure Flask backend is running
- Check CORS configuration in `app.py`
- Verify API URL in frontend `.env`

### API Connection Errors
- Check backend is running on port 5000
- Verify `VITE_API_URL` in frontend `.env`
- Check browser console for detailed errors

### Authentication Issues
- Clear localStorage if user data is corrupted
- Check backend logs for authentication errors
- Verify Supabase connection in backend

## Next Steps

- Add real-time updates using WebSockets
- Implement position management UI
- Add market resolution UI
- Create portfolio view with positions
- Add leaderboard display

