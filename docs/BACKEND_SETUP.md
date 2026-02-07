# Backend Setup Guide

## Overview

The backend folder is ready for API development. This guide will help you set up the backend infrastructure.

## Getting Started

### 1. Initialize Backend Project

Choose your preferred framework and initialize:

#### Node.js/Express Example
```bash
cd backend
npm init -y
npm install express cors dotenv
```

#### Python/Flask Example
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install flask flask-cors
```

### 2. Project Structure (Recommended)

```
backend/
├── src/
│   ├── routes/
│   ├── controllers/
│   ├── models/
│   ├── middleware/
│   └── app.js (or main.py)
├── .env
├── .env.example
├── package.json (or requirements.txt)
└── README.md
```

### 3. Environment Setup

Create a `.env` file with necessary configuration:
```
PORT=5000
DATABASE_URL=your_database_url
API_KEY=your_api_key
```

### 4. API Endpoints (Planned)

- Portfolio management endpoints
- Market data endpoints
- Oracle integration endpoints
- User authentication endpoints

### 5. Frontend Integration

The frontend runs on `http://localhost:5173/` by default. Configure CORS in your backend:

```javascript
// Express example
const cors = require('cors');
app.use(cors({
  origin: 'http://localhost:5173',
  credentials: true
}));
```

## Technology Stack (Recommended)

- **Runtime:** Node.js or Python
- **Framework:** Express.js or Flask
- **Database:** PostgreSQL or MongoDB
- **Authentication:** JWT or OAuth2
- **Validation:** Joi or Pydantic

## Next Steps

1. Choose your preferred technology stack
2. Initialize the project
3. Create API routes
4. Connect to frontend
5. Deploy to production

## Resources

- Express.js: https://expressjs.com/
- Flask: https://flask.palletsprojects.com/
- Node.js: https://nodejs.org/
- Python: https://www.python.org/
