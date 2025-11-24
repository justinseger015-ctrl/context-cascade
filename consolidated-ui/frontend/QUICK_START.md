# Quick Start - Ruv-Sparc UI Dashboard Frontend

## Install Dependencies
```bash
cd frontend
npm install
```

## Development
```bash
npm run dev
# Opens http://localhost:3000
# API proxy: /api -> http://localhost:8000
```

## Build for Production
```bash
npm run build
# Output: dist/
```

## Run Tests
```bash
# Unit tests
npm run test

# With coverage
npm run test:coverage

# E2E tests (requires dev server running)
npm run test:e2e
```

## Code Quality
```bash
# Type check
npm run typecheck

# Lint
npm run lint

# Format
npm run format
```

## Project Status

✅ All dependencies installed (zustand, @dnd-kit, reactflow, DayPilot, DOMPurify)
✅ TypeScript strict mode enabled
✅ Tailwind CSS v4 configured
✅ API proxy to FastAPI backend
✅ Jest + Playwright testing configured
✅ Build successful (146.4 KB total)
✅ Dev server working

## What's Included

- React 18.3.1
- TypeScript 5.6.2 (strict mode)
- Vite 5.4.10 (HMR, code splitting)
- Tailwind CSS 4.1.17
- Zustand 5.0.8 (state management)
- @dnd-kit (drag-and-drop, WCAG compliant)
- React Flow (workflow visualization)
- DayPilot Lite React (calendar)
- DOMPurify (XSS protection)
- Jest + React Testing Library
- Playwright (E2E)

## Next: Phase 3 Development

Ready to build:
1. Component library
2. Calendar views
3. Drag-and-drop interfaces
4. Workflow visualizations
5. State management
6. API integration
