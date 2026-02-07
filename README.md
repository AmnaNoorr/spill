# SipNSecret

A comprehensive cryptocurrency portfolio management application built with React and Vite.

## Project Structure

```
SipNSecret/
├── frontend/          # React frontend application
│   ├── src/          # Source code
│   │   ├── components/
│   │   ├── styles/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── dist/         # Build output
│   └── node_modules/
├── backend/          # Backend API (future implementation)
├── docs/             # Documentation
└── README.md
```

## Getting Started

### Frontend Development

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173/`

### Build for Production

```bash
cd frontend
npm run build
```

This creates an optimized build in the `dist/` folder.

### Preview Production Build

```bash
cd frontend
npm run preview
```

## Technologies Used

- **Frontend:** React 18, Vite, lucide-react
- **Styling:** CSS with CSS Variables
- **Build Tool:** Vite
- **Icons:** lucide-react

## Features

- Portfolio management dashboard
- Market data tracking
- Oracle integration
- Responsive sidebar navigation
- Modern UI with custom styling

## Project Folders

- **frontend/** - React application with Vite build system
- **backend/** - Backend API (ready for development)
- **docs/** - Project documentation

## License

Proprietary
