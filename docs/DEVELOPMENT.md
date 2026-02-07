# Development Guide

## Frontend Setup

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Development Server

```bash
npm run dev
```

This starts a local development server with hot module replacement (HMR).

### Building

```bash
npm run build
```

Creates an optimized production build in the `dist/` folder.

### Preview

```bash
npm run preview
```

Serves the built files for preview before deployment.

## Project Components

### Components Structure
- **Header.jsx** - Top navigation component
- **Markets.jsx** - Market data display
- **Oracle.jsx** - Oracle integration component
- **PortfolioSidebar.jsx** - Portfolio sidebar navigation
- **SplashScreen.jsx** - Initial splash screen
- **Submit.jsx** - Form submission component

### Styling
- **global.css** - Global styles
- **variables.css** - CSS custom properties and variables

## Code Style Guidelines

- Use functional components with hooks
- Component names should use PascalCase
- Use meaningful variable names
- Keep components modular and reusable

## Adding New Features

1. Create new components in `src/components/`
2. Import and use in `App.jsx`
3. Style using global styles or component-specific CSS
4. Test in development server

## Troubleshooting

### Port Already in Use
If port 5173 is already in use, Vite will automatically use the next available port.

### Module Not Found
Ensure all imports use correct relative paths and extensions.

### Build Issues
Clear `node_modules` and `dist` folders, then reinstall:
```bash
rm -rf node_modules dist
npm install
npm run build
```
