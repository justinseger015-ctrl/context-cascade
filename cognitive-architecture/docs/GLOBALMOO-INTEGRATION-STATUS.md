# GlobalMOO Integration Status

**Date**: 2025-12-28
**Status**: PARTIALLY INTEGRATED

## What Works

### API Connection
- **Base URI**: `https://app.globalmoo.com/api` (CORRECT - not api.globalmoo.ai)
- **Auth**: Bearer token via `GLOBALMOO_API_KEY`
- **Connection test**: Verified working

### Verified Endpoints

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/models` | GET | Working | Lists all models in account |
| `/models` | POST | Working | Creates new model |
| `/models/{id}` | GET | Working | Gets model with projects |
| `/models/{id}/projects` | POST | Working | Creates project (limited to 5 inputs on free tier) |

### Created Resources

**Model**: VERIX_VERILINGUA_Cognitive_v1
- ID: 2193
- Created: 2025-12-29T00:40:07

**Project**: cognitive_5dim_v1
- ID: 8318
- Input dimensions: 5
- Auto-generated input cases: 151

### 5-Dimensional Reduced Config Vector

Due to subscription limits (max 5 inputs), we use a reduced representation:

| Dim | Name | Range | Purpose |
|-----|------|-------|---------|
| 0 | evidential_frame | 0-1 | Core evidence frame toggle |
| 1 | aspectual_frame | 0-1 | Temporal reasoning toggle |
| 2 | verix_strictness | 0-2 | VERIX verification level |
| 3 | compression_level | 0-2 | Token efficiency level |
| 4 | require_ground | 0-1 | Edge robustness toggle |

## What Needs Work

### Endpoints Not Yet Working

| Endpoint | Issue | Notes |
|----------|-------|-------|
| Trial creation | 404 | Endpoint structure unclear |
| Objective setup | Unknown | May require trials first |
| Inverse optimization | Unknown | Requires trial + objectives |
| Load outputs | Unknown | Develop workflow unclear |

### Subscription Limitations

1. **Max 5 input dimensions** on current tier
2. **Trial/inverse optimization** may require higher tier
3. **Full 14-dim config** not possible without upgrade

## Mock Mode

The client includes a comprehensive mock mode for local development:

```python
from optimization.globalmoo_client import GlobalMOOClient

# Mock mode for testing
client = GlobalMOOClient(use_mock=True)

# Real API
client = GlobalMOOClient()  # Uses env vars
```

Mock mode provides:
- Full Pareto optimization locally
- Non-dominated sorting
- Impact factor estimation
- Inverse suggestion simulation

## Configuration

**.env file** (in cognitive-architecture/):
```
GLOBALMOO_API_KEY=gq8bbjzNZzJPsDaEzB4YWqzJKvSst2H7rL9R6JHfsUYm9Arc
GLOBALMOO_BASE_URI=https://app.globalmoo.com/api
```

## Next Steps

1. **Investigate trial creation** - Check web UI or contact GlobalMOO support
2. **Check subscription tier** - May need upgrade for full optimization
3. **Use mock mode** - Continue development with local Pareto optimization
4. **Map 5-dim to 14-dim** - Create codec for reduced representation

## Files Modified

- `optimization/globalmoo_client.py` - Updated with correct API patterns
- `.env` - Updated with correct base URI
- `storage/real_optimization/` - Contains optimization results

## API Documentation

- Official docs: https://globalmoo.gitbook.io/globalmoo-documentation
- Create model: POST `/models` with `{name, description}`
- Create project: POST `/models/{id}/projects` with `{name, inputCount, minimums, maximums, inputTypes}`
