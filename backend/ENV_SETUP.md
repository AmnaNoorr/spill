# Environment Variables Setup

## Location
Create a file named `.env` in the `backend/` directory.

## Required Variables

Copy this template and fill in your values:

```env
# Supabase Configuration
SUPABASE_URL=https://foeqlhupxqonniomkyce.supabase.co
SUPABASE_KEY=your_anon_key_here

# OpenAI Configuration
OPENAI_API_KEY=sk-7890abcdef7890abcdef7890abcdef7890abcd

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

## How to Get Your Anon Key

1. Go to: https://supabase.com/dashboard
2. Select your project
3. Click **Settings** (gear icon) → **API**
4. Under **Project API keys**, find **anon public**
5. Click the eye icon to reveal it
6. Copy the key (it's a long string starting with `eyJ...`)

## Important Notes

- **SUPABASE_KEY** should be the **anon public** key (not service_role)
- The anon key is safe to use in frontend/backend code
- Never commit `.env` to git (it's in `.gitignore`)
- Use `service_role` key only for admin operations (server-side only)

## File Structure

```
backend/
├── .env          ← Create this file here
├── .env.example  ← Template (safe to commit)
├── config.py     ← Reads from .env
└── ...
```

## After Setup

Restart your Flask server for changes to take effect:

```bash
# Stop the server (Ctrl+C)
# Then restart:
cd backend
python run.py
```

