# UI Consolidation Audit

**Date**: 2025-11-17
**Status**: Discovery Complete
**Goal**: Consolidate 3 UIs into one ultra UI/UX experience

---

## Executive Summary

Discovered **3 UI implementations** across the device:

1. **Terminal Manager** (frontend/) - Production calendar/terminal UI
2. **Rose Tree** (skilltree/) - AI-powered skill tree (RUNNING on boot)
3. **Archived Dashboard** (archive/) - Full-stack production dashboard (MOST COMPREHENSIVE)

**Recommendation**: Use **Archived Dashboard** as the base and migrate best components from Terminal Manager and Rose Tree.

---

## UI #1: Terminal Manager Frontend

**Location**: `C:/Users/17175/frontend/`
**Status**: Active development
**Boot Status**: Not running on boot

### Tech Stack
- **Framework**: React 18.3.1 + Vite 6.0.1
- **Language**: TypeScript 5.7.2
- **UI Library**: Radix UI (13 components)
- **Styling**: TailwindCSS 4.1.17
- **State**: Zustand 5.0.8
- **Testing**: Playwright 1.56.1 (E2E)

### Component Inventory (10 directories)
```
components/
hooks/
pages/
services/
store/
styles/
types/
validators/
```

### Key Features
- **Calendar**: react-big-calendar 1.19.4 (event scheduling)
- **Terminal**: xterm 5.3.0 with fit/search addons
- **Toast Notifications**: react-hot-toast 2.6.0
- **Search**: Fuse.js 7.1.0 (fuzzy search)
- **Syntax Highlighting**: react-syntax-highlighter 16.1.0
- **Date Handling**: date-fns 4.1.0

### E2E Test Coverage
- Dashboard tests
- Performance tests
- Accessibility tests
- Integration tests

### Strengths
- Modern Radix UI components (accessible)
- Comprehensive E2E testing
- Terminal emulation ready
- Calendar integration
- TypeScript strict mode

### Weaknesses
- No WebSocket integration
- No agent monitoring
- No workflow visualization
- Missing project management

---

## UI #2: Rose Tree (Skilltree)

**Location**: `C:/Users/17175/skilltree/`
**Status**: RUNNING (localhost:3001)
**Boot Status**: **AUTO-STARTS ON BOOT**

### Tech Stack
- **Framework**: Next.js 14.2.5
- **Language**: React 18
- **Styling**: SASS 1.77.8
- **AI**: Anthropic AI SDK 0.24.3
- **Rendering**: Katex 0.16.11 (LaTeX), Marked 4.3.0 (Markdown)

### Component Inventory (5 components)
```
components/
  Button/
  FloatingTextInput/
  SegmentedControl/
  Selector/
  timestamp/
```

### Directory Structure
```
src/
  app/
  components/
  pages/
  styles/
  utils/
```

### Key Features
- **AI Integration**: Anthropic Claude SDK
- **LaTeX Rendering**: Mathematical notation support
- **Markdown Parsing**: marked + marked-extended-latex
- **SVG Processing**: svg-parser 2.0.4
- **UUID Generation**: uuid 10.0.0
- **YAML Parsing**: yaml 2.8.1

### Strengths
- **Production-ready Next.js setup**
- **AI-native architecture** (Claude integration)
- **Advanced content rendering** (LaTeX, Markdown)
- **Minimal, focused component library**
- **Server-side rendering** (Next.js)

### Weaknesses
- Limited component library (5 components)
- No calendar/scheduling
- No terminal integration
- No drag-and-drop
- No WebSocket/real-time features

---

## UI #3: Archived Dashboard (WINNER)

**Location**: `C:/Users/17175/archive/ruv-sparc-ui-dashboard-20251115/`
**Status**: Archived (production-ready)
**Boot Status**: Not running

### Tech Stack
- **Framework**: React 18.3.1 + Vite 5.4.10
- **Language**: TypeScript 5.6.2
- **Routing**: React Router DOM 7.9.5
- **State**: Jotai 2.15.1 + Zustand 5.0.8 (dual state management)
- **Forms**: React Hook Form 7.66.0 + Zod 4.1.12 (validation)
- **Real-time**: Socket.io-client 4.8.1
- **Workflow**: ReactFlow 11.11.4 (node-based graphs)
- **Styling**: TailwindCSS 4.1.17
- **Code Editor**: CodeMirror (@uiw/react-codemirror 4.25.3)
- **Drag-and-Drop**: @dnd-kit/* 6.3.1
- **Calendar**: @daypilot/daypilot-lite-react 4.8.1
- **Search**: Fuse.js 7.1.0
- **Security**: DOMPurify 3.2.4
- **Testing**: Jest 30.2.0 + Playwright 1.56.1 + Axe-core 4.11.0

### Component Inventory (30+ components)

#### Agent Monitoring
- **AgentActivityFeed.tsx** - Real-time agent activity stream
- **AgentMonitor.tsx** - Agent status and metrics
- **AgentWorkflowGraph.tsx** - Visual workflow editor (ReactFlow)
- **AgentWorkflowGraph.optimized.tsx** - Performance-optimized version

#### Project Management
- **ProjectDashboard.tsx** - Main project view
- **CreateProjectForm.tsx** - Project creation
- **ExistingProjectsList.tsx** - Project picker
- **ProjectSelectorModal.tsx** - Project switcher

#### Task Management
- **TaskList.tsx** - Task list view
- **TaskItem.tsx** - Individual task
- **TaskForm.tsx** - Task creation/editing
- **DraggableTaskList.tsx** - Drag-and-drop task reordering
- **TaskFilters.tsx** - Filter controls
- **TaskFormDemo.tsx** - Interactive demo
- **TaskReminders.tsx** - Reminder system

#### Calendar & Scheduling
- **Calendar.tsx** - Main calendar component
- **CalendarEnhancements.tsx** - Advanced calendar features
- **CalendarFilters.tsx** - Calendar filter UI
- **RecurringTaskTemplate.tsx** - Recurring task builder
- **CronBuilder.tsx** - Cron expression editor
- **CalendarViews/** - Multiple calendar views

#### Search & Navigation
- **GlobalSearch.tsx** - App-wide search
- **SearchAutocomplete.tsx** - Autocomplete search
- **ExportButton.tsx** - Data export
- **ImportModal.tsx** - Data import

#### System Components
- **WebSocketIndicator.tsx** - Connection status
- **MCPStatusIndicator.tsx** - MCP server status
- **degraded-mode-ui-banner.tsx** - Degraded mode warning
- **NotificationSettings.tsx** - Notification preferences
- **DirectoryPicker.tsx** - File system picker
- **Button.tsx** - Base button component

#### Feature-Specific Modules
```
agents/                 - Agent-specific components
BestOfN/                - Best-of-N algorithm UI
FeedbackLoops/          - Feedback loop visualization
logging/                - Log viewer components
mcp/                    - MCP integration UI
memory/                 - Memory system UI
scheduling/             - Advanced scheduling
sessions/               - Session management
terminals/              - Terminal emulator UI
ui/                     - Shared UI components
design-system/          - Design system tokens
```

### Key Features

#### Real-time Monitoring
- WebSocket integration (Socket.io)
- Live agent activity feed
- Real-time workflow updates
- Connection status indicators

#### Workflow Visualization
- ReactFlow-based workflow editor
- Drag-and-drop node connections
- Optimized rendering for large graphs
- Interactive workflow execution

#### Advanced Scheduling
- Multiple calendar views (day/week/month/year)
- Cron expression builder
- Recurring task templates
- Task reminders with notifications

#### Form Validation
- React Hook Form + Zod schema validation
- Type-safe form inputs
- Error handling
- Auto-save capabilities

#### Accessibility
- Axe-core integration
- WCAG compliance testing
- Keyboard navigation
- Screen reader support

#### Code Editing
- CodeMirror integration
- JSON syntax highlighting
- Auto-formatting
- Error detection

#### Security
- DOMPurify for XSS protection
- Content sanitization
- Secure WebSocket connections

### Testing Infrastructure

#### Unit Tests (Jest)
- Component testing
- Service testing
- Store testing
- Coverage reporting

#### E2E Tests (Playwright)
- Workflow testing
- Multi-browser support (Chromium/Firefox/WebKit)
- Docker-based testing
- UI mode for debugging
- Test report generation

#### Accessibility Tests
- Axe-core automated audits
- WCAG 2.1 compliance
- Manual a11y testing

### Production Features
- Docker deployment
- K6 load testing scripts
- Lighthouse performance reports
- Staging deployment logs
- Production validation

### Strengths
- **MOST COMPREHENSIVE UI** by far
- **Production-ready** (Docker, testing, validation)
- **Real-time capabilities** (WebSocket)
- **Advanced workflow visualization** (ReactFlow)
- **Complete project/task management**
- **Professional calendar system**
- **Accessibility built-in** (Axe)
- **Dual state management** (Jotai + Zustand)
- **Type-safe forms** (Zod validation)
- **Code editing** (CodeMirror)
- **Drag-and-drop** (@dnd-kit)
- **Security** (DOMPurify)
- **Multi-browser E2E testing**

### Weaknesses
- No terminal emulation (need to import from Terminal Manager)
- No AI SDK integration (need to import from Rose Tree)
- Archived (not actively running)

---

## Consolidation Strategy

### Phase 1: Base Selection

**Winner**: Archived Dashboard (ruv-sparc-ui-dashboard-20251115)

**Rationale**:
- Most comprehensive feature set (30+ components)
- Production-ready architecture
- Real-time WebSocket integration
- Complete testing infrastructure
- Professional project/task management
- Advanced workflow visualization
- Accessibility built-in

### Phase 2: Component Migration

#### From Terminal Manager → Archived Dashboard
- **Terminal emulation** (xterm integration)
- **Radix UI components** (more modern than current)
- **Playwright E2E tests** (additional coverage)
- **Date-fns** (replace other date libraries)

#### From Rose Tree → Archived Dashboard
- **Anthropic AI SDK** (Claude integration)
- **LaTeX rendering** (Katex)
- **Markdown parsing** (marked-extended-latex)
- **SASS theming** (if needed)
- **Next.js SSR** (optional future enhancement)

### Phase 3: Feature Consolidation

#### Keep from Archived Dashboard
- All 30+ existing components
- WebSocket real-time system
- ReactFlow workflow editor
- Jotai + Zustand state management
- React Hook Form + Zod validation
- CodeMirror editor
- Drag-and-drop (@dnd-kit)
- Calendar system (@daypilot)
- Testing infrastructure (Jest + Playwright + Axe)

#### Add from Terminal Manager
- xterm terminal emulator
- Radix UI component upgrades
- Enhanced accessibility features

#### Add from Rose Tree
- Anthropic Claude AI integration
- LaTeX/Markdown rendering
- AI-powered features

### Phase 4: Visual/UX Enhancements

#### Modern Design System
- **Radix UI primitives** (from Terminal Manager)
- **TailwindCSS 4.1.17** (already in all 3)
- **Lucide React icons** (already in 2/3)
- **Consistent spacing/typography**
- **Dark mode** (if not present)

#### UX Improvements
- **Unified navigation** (single source of truth)
- **Keyboard shortcuts** (app-wide)
- **Command palette** (search + actions)
- **Responsive design** (mobile-first)
- **Performance optimization** (code splitting)

---

## Technology Stack (Consolidated UI)

### Core
- React 18.3.1
- TypeScript 5.7.2
- Vite 6.0.1 (or Next.js 14 for SSR)

### UI Framework
- Radix UI (from Terminal Manager)
- TailwindCSS 4.1.17
- Lucide React icons

### State Management
- Jotai 2.15.1 (atomic state)
- Zustand 5.0.8 (global state)

### Forms & Validation
- React Hook Form 7.66.0
- Zod 4.1.12

### Real-time
- Socket.io-client 4.8.1

### Specialized Features
- ReactFlow 11.11.4 (workflows)
- xterm 5.3.0 (terminal)
- CodeMirror (code editing)
- @dnd-kit/* (drag-and-drop)
- @daypilot/* (calendar)
- Anthropic AI SDK (AI features)
- Katex (LaTeX)
- Marked (Markdown)

### Testing
- Jest 30.2.0
- Playwright 1.56.1
- Axe-core 4.11.0
- Testing Library

### Security
- DOMPurify 3.2.4
- Zod schema validation

---

## File Structure (Proposed)

```
consolidated-ui/
  src/
    app/                      # App initialization
    components/
      agents/                 # Agent monitoring (from Archived)
      calendar/               # Calendar system (from Archived)
      code-editor/            # CodeMirror integration (from Archived)
      design-system/          # Radix UI + design tokens (NEW)
      feedback/               # Feedback loops (from Archived)
      forms/                  # Form components (from Archived)
      layout/                 # App shell, navigation (NEW)
      mcp/                    # MCP integration (from Archived)
      memory/                 # Memory system (from Archived)
      projects/               # Project management (from Archived)
      scheduling/             # Advanced scheduling (from Archived)
      search/                 # Global search (from Archived)
      sessions/               # Session management (from Archived)
      tasks/                  # Task management (from Archived)
      terminals/              # Terminal emulator (from Terminal Manager)
      ui/                     # Shared UI primitives (Radix)
      workflows/              # ReactFlow workflows (from Archived)
    features/
      ai-assistant/           # Anthropic integration (from Rose Tree)
      content-rendering/      # LaTeX + Markdown (from Rose Tree)
    hooks/                    # Custom React hooks
    lib/                      # Utilities
    pages/                    # Route pages
    services/                 # API clients
    store/                    # Jotai + Zustand stores
    styles/                   # Global styles
    types/                    # TypeScript types
    validators/               # Zod schemas
  tests/
    e2e/                      # Playwright tests
    unit/                     # Jest tests
    accessibility/            # Axe tests
  public/                     # Static assets
  package.json
  vite.config.ts
  tsconfig.json
  tailwind.config.js
  playwright.config.ts
  jest.config.js
```

---

## Implementation Plan

### Week 1: Foundation (8-12 hours)
1. Copy archived dashboard to new `consolidated-ui/` directory
2. Upgrade dependencies to latest versions
3. Set up development environment
4. Verify all tests pass
5. Document current state

### Week 2: Terminal Integration (4-6 hours)
1. Extract terminal components from Terminal Manager
2. Integrate xterm into archived dashboard
3. Add terminal page/routes
4. Test terminal functionality
5. Update documentation

### Week 3: AI Integration (6-8 hours)
1. Extract AI features from Rose Tree
2. Install Anthropic SDK
3. Create AI assistant component
4. Integrate LaTeX/Markdown rendering
5. Add AI-powered features to existing components
6. Test AI interactions

### Week 4: UI/UX Polish (8-12 hours)
1. Upgrade to Radix UI components
2. Implement unified design system
3. Add dark mode support
4. Optimize performance (code splitting)
5. Add keyboard shortcuts
6. Implement command palette
7. Mobile responsive design

### Week 5: Testing & Validation (6-8 hours)
1. Write additional E2E tests
2. Accessibility audit (Axe)
3. Performance testing (Lighthouse)
4. Cross-browser testing
5. Security audit
6. Bug fixes

### Week 6: Deployment (2-4 hours)
1. Docker configuration
2. Production build
3. Deploy to localhost
4. Auto-start on boot configuration
5. Documentation finalization

**Total Estimated Time**: 34-50 hours (5-7 weeks part-time)

---

## Success Metrics

### Functionality
- [ ] All features from 3 UIs working in one place
- [ ] Real-time WebSocket connections stable
- [ ] Terminal emulation functional
- [ ] AI assistant integrated
- [ ] Calendar/scheduling operational
- [ ] Workflow visualization working

### Performance
- [ ] Lighthouse score >90 (all categories)
- [ ] First Contentful Paint <1.5s
- [ ] Time to Interactive <3s
- [ ] Bundle size <500KB (gzipped)

### Quality
- [ ] Test coverage >80%
- [ ] All E2E tests passing
- [ ] Zero Axe accessibility violations (WCAG 2.1 AA)
- [ ] Zero security vulnerabilities
- [ ] TypeScript strict mode (no errors)

### UX
- [ ] Responsive design (mobile/tablet/desktop)
- [ ] Dark mode functional
- [ ] Keyboard navigation complete
- [ ] Command palette working
- [ ] <100ms UI response time

---

## Next Steps

1. **Get User Approval**: Present this audit to user for feedback
2. **Create Prototype**: Build Week 1 foundation
3. **Incremental Migration**: Follow 6-week plan
4. **Continuous Testing**: Test after each integration
5. **Documentation**: Keep docs updated throughout

---

**Status**: Discovery Complete - Awaiting User Approval
**Recommendation**: Proceed with archived dashboard as base + Terminal + AI integrations
