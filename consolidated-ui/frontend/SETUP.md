# Frontend Setup - Ruv-Sparc UI Dashboard

## Project Overview
React 18+ frontend with TypeScript strict mode, Vite, and Tailwind CSS.

## Technology Stack

### Core
- **React**: 18.3.1
- **TypeScript**: 5.6.2 (strict mode enabled)
- **Vite**: 5.4.10 (development server + build tool)
- **Tailwind CSS**: 4.1.17 (utility-first CSS)

### State Management
- **Zustand**: 5.0.8 ✅ (verified - simple, performant state management)
- **Jotai**: 2.15.1 (alternative atomic state management)

### UI Libraries
- **@dnd-kit/core**: 6.3.1 (drag-and-drop with WCAG 2.1 AA compliance)
- **@dnd-kit/sortable**: 10.0.0
- **@dnd-kit/utilities**: 3.2.2
- **DayPilot Lite React**: 4.8.1 (calendar component - React 19 compatible)
- **React Flow**: 11.11.4 (workflow visualization - 60 FPS with 100+ nodes)

### Security
- **DOMPurify**: 3.2.4 (XSS protection - CRITICAL)

### Testing
- **Jest**: 30.2.0
- **@testing-library/react**: 16.3.0
- **@testing-library/jest-dom**: 6.9.1
- **@testing-library/user-event**: 14.6.1
- **@playwright/test**: 1.56.1 (E2E testing)
- **ts-jest**: 29.4.5

### Code Quality
- **ESLint**: 9.13.0
- **Prettier**: 3.6.2
- **TypeScript ESLint**: 8.11.0

## TypeScript Configuration

Strict mode enabled with additional safety checks:
- `strict: true`
- `noUncheckedIndexedAccess: true`
- `noImplicitReturns: true`
- `noFallthroughCasesInSwitch: true`
- `noUnusedLocals: true`
- `noUnusedParameters: true`

## Project Structure

```
frontend/
├── src/
│   ├── components/     # React components (Button.tsx, etc.)
│   ├── hooks/          # Custom React hooks
│   ├── store/          # Zustand stores (useProjectStore.ts)
│   ├── types/          # TypeScript type definitions
│   ├── utils/          # Utility functions
│   ├── App.tsx         # Main application component
│   └── main.tsx        # Entry point
├── tests/              # Jest unit tests
│   └── setup.ts        # Test environment setup
├── e2e/                # Playwright E2E tests
├── public/             # Static assets
├── dist/               # Build output
└── node_modules/       # Dependencies
```

## Available Scripts

```bash
# Development
npm run dev              # Start Vite dev server (http://localhost:3000)

# Building
npm run build            # TypeScript compile + Vite production build
npm run preview          # Preview production build

# Code Quality
npm run typecheck        # TypeScript type checking
npm run lint             # ESLint check
npm run lint:fix         # ESLint auto-fix
npm run format           # Prettier format
npm run format:check     # Prettier check

# Testing
npm run test             # Run Jest unit tests
npm run test:watch       # Jest watch mode
npm run test:coverage    # Jest with coverage report
npm run test:e2e         # Playwright E2E tests
```

## Vite Configuration

### Development Server
- Port: 3000
- HMR: Enabled
- API Proxy: `/api` → `http://localhost:8000` (FastAPI backend)

### Build Optimization
- Code splitting with manual chunks:
  - `react-vendor`: React core libraries
  - `state-vendor`: Zustand, Jotai
  - `ui-vendor`: dnd-kit, React Flow
- Sourcemaps: Enabled
- Target: ES2020
- Gzip size warnings: 1000 KB threshold

## Build Output

Latest build metrics:
```
dist/index.html                     0.55 kB │ gzip:  0.33 kB
dist/assets/index.css               0.95 kB │ gzip:  0.55 kB
dist/assets/ui-vendor.js            0.08 kB │ gzip:  0.10 kB
dist/assets/state-vendor.js         0.09 kB │ gzip:  0.10 kB
dist/assets/index.js                3.90 kB │ gzip:  1.59 kB
dist/assets/react-vendor.js       140.78 kB │ gzip: 45.25 kB
```

## Loop 1 Research Validation

All dependencies verified against Loop 1 research:

✅ **Zustand**: Correct package (NOT zustand.js) - 12.84M downloads/week
✅ **@dnd-kit**: UNANIMOUS 5/5 consensus - WCAG 2.1 AA compliant
✅ **DayPilot**: React 19 compatible - Apache 2.0 license
✅ **React Flow**: 95% confidence - 60 FPS performance
✅ **DOMPurify**: Security critical - XSS protection

## Success Criteria

- [x] `npm install` completes with zero errors
- [x] `npm run dev` starts Vite dev server
- [x] `npm run build` compiles TypeScript with strict mode
- [x] `npm run lint` passes with zero errors
- [x] `npm run typecheck` passes with zero errors
- [x] Zustand package verified as correct (NOT zustand.js)
- [x] All Loop 1 recommended packages installed

## Next Steps

This setup enables Phase 3 (Frontend Core) development:
1. Component library development
2. State management implementation
3. API integration with FastAPI backend
4. Calendar, drag-and-drop, workflow features
5. Comprehensive testing suite
6. Production deployment

## Notes

- **Tailwind CSS v4**: Uses `@tailwindcss/postcss` plugin (new architecture)
- **API Proxy**: Configured for `/api` routes to FastAPI backend
- **Coverage Threshold**: 80% minimum (branches, functions, lines, statements)
- **Security**: DOMPurify integration mandatory for user-generated content
