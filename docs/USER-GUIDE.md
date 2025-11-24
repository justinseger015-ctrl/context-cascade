# Agent Reality Map - User Guide

## Overview

The Agent Reality Map provides real-time visibility into agent activities, performance metrics, and quality enforcement across your AI agent ecosystem.

## Getting Started

### Accessing the Dashboard

1. **Start Backend**: `cd backend && uvicorn app.main:app --reload`
2. **Access**: Open http://localhost:3000 in your browser
3. **Default View**: Agent Registry with 207 registered agents

### Dashboard Components

#### 1. Agent Registry
- **Location**: Main dashboard
- **Shows**: All 207 agents organized in 10 categories
- **Features**:
  - Real-time agent status
  - Performance metrics
  - RBAC permissions
  - Budget tracking

#### 2. Activity Feed
- **Location**: `/activity` route
- **Shows**: Real-time agent operations
- **Features**:
  - Live WebSocket updates
  - Operation timeline
  - Success/failure indicators
  - Performance stats

#### 3. Resource Monitors
- **Location**: `/resources` route
- **Shows**: System resource usage
- **Metrics**:
  - API calls per agent
  - Token usage
  - Cost tracking
  - Budget status

#### 4. Quality Metrics
- **Location**: `/quality` route
- **Shows**: Code quality scores
- **Features**:
  - Connascence scores (0-100)
  - Quality grades (A-F)
  - Violation tracking
  - Trend analysis

### Common Tasks

#### View Agent Details

1. Navigate to Agent Registry
2. Click on agent name
3. View detailed metrics:
   - Capabilities
   - RBAC permissions
   - Budget limits
   - Performance history

#### Monitor Real-Time Activity

1. Open Activity Feed
2. WebSocket auto-connects
3. View live operations:
   - Green: Success
   - Red: Failure
   - Yellow: Warning

#### Check Resource Usage

1. Open Resource Monitors
2. Select agent or timeframe
3. View metrics:
   - Tokens used today
   - Cost (USD)
   - Remaining budget
   - Projected usage

#### Review Quality Scores

1. Open Quality Metrics
2. View aggregated scores
3. Drill down to specific files
4. See violation details

## Troubleshooting

### Dashboard Not Loading

**Symptom**: Blank page or errors
**Solution**:
1. Check backend running: `curl http://localhost:8000/health`
2. Check frontend: `cd frontend && npm run dev`
3. Check browser console for errors

### No Real-Time Updates

**Symptom**: Activity feed static
**Solution**:
1. Check WebSocket connection (browser DevTools > Network > WS)
2. Verify backend WebSocket endpoint: `ws://localhost:8000/ws`
3. Refresh page to reconnect

### Agent Not Showing

**Symptom**: Agent missing from registry
**Solution**:
1. Check agent registered: `curl http://localhost:8000/api/v1/agents/`
2. Verify agent in database
3. Check filters applied in UI

## Best Practices

1. **Monitor Budget Daily**: Check Resource Monitors to avoid overages
2. **Review Quality Weekly**: Track quality trends to maintain standards
3. **Audit Activity Monthly**: Review Activity Feed for security/compliance
4. **Update Agents**: Keep agent definitions current with capabilities

## Support

- **Documentation**: `/docs` folder
- **API Reference**: `http://localhost:8000/docs` (FastAPI auto-docs)
- **Issues**: Check backend logs in `/tmp/backend.log`
