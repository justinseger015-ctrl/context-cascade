# GlobalMOO Integration Guide

**Updated**: 2025-12-28
**API Version**: v1
**Client File**: `optimization/globalmoo_client.py`

---

## Overview

GlobalMOO is a cloud-based multi-objective optimization service that enables:
- Pareto frontier exploration for multiple objectives
- Inverse optimization (target outcomes -> config vectors)
- Subscription-based dimensionality limits

**Integration Pattern**:
```
GlobalMOO (5D exploration) -> PyMOO NSGA-II (14D refinement)
```

---

## API Configuration

### Base URL

```
https://app.globalmoo.com/api
```

### Authentication

```bash
# Set environment variable
export GLOBALMOO_API_KEY="your_api_key_here"
```

Or in `.env` file:
```
GLOBALMOO_API_KEY=your_api_key_here
```

### Current Model/Project

| Setting | Value |
|---------|-------|
| Model ID | 2193 |
| Project ID | 8318 |
| Dimensions | 5 (subscription limited) |

---

## API Endpoints

### Models

```http
# Create model
POST /models
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "name": "cognitive-architecture-optimizer",
  "description": "Optimize VERILINGUA x VERIX configurations"
}

# List models
GET /models
Authorization: Bearer {api_key}

# Get model with projects
GET /models/{model_id}
Authorization: Bearer {api_key}
```

### Projects

```http
# Create project
POST /models/{model_id}/projects
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "name": "5dim-cognitive-config",
  "inputCount": 5,
  "minimums": [0, 0, 0, 0, 0],
  "maximums": [1, 1, 2, 2, 1],
  "inputTypes": ["continuous", "continuous", "discrete", "discrete", "continuous"]
}
```

### Trials/Evaluations

```http
# Submit evaluation (report outcome)
POST /models/{model_id}/projects/{project_id}/trials
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "inputs": [0.9, 0.8, 2, 1, 0.7],
  "outputs": {
    "task_accuracy": 0.92,
    "token_efficiency": 0.78,
    "edge_robustness": 0.85,
    "epistemic_consistency": 0.91
  }
}

# Get Pareto frontier
GET /models/{model_id}/projects/{project_id}/pareto
Authorization: Bearer {api_key}
```

### Inverse Optimization

```http
# Request config for target outcomes
POST /models/{model_id}/projects/{project_id}/inverse
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "target_outcomes": {
    "task_accuracy": 0.95,
    "token_efficiency": 0.80
  }
}
```

---

## 5-Dimensional Configuration Space

The GlobalMOO subscription limits to 5 dimensions. We use:

| Index | Dimension | Range | Type | Description |
|-------|-----------|-------|------|-------------|
| 0 | evidential_frame | 0-1 | continuous | Turkish evidential markers |
| 1 | aspectual_frame | 0-1 | continuous | Russian aspect markers |
| 2 | verix_strictness | 0-2 | discrete | RELAXED/MODERATE/STRICT |
| 3 | compression_level | 0-2 | discrete | L0/L1/L2 output format |
| 4 | require_ground | 0-1 | continuous | Require evidence citations |

### Mapping to 14D Full Config

```python
def expand_5d_to_14d(x_5d):
    """Expand 5D GlobalMOO vector to 14D full config."""
    return [
        x_5d[0],     # evidential
        x_5d[1],     # aspectual
        0.1,         # morphological (default low)
        0.1,         # compositional (default low)
        0.1,         # honorific (default low)
        0.1,         # classifier (default low)
        0.1,         # spatial (default low)
        x_5d[2],     # verix_strictness
        x_5d[3],     # compression_level
        x_5d[4],     # require_ground
        0.5,         # require_confidence (default)
        0.7,         # temperature (default)
        0.6,         # coherence_weight (default)
        0.7,         # evidence_weight (default)
    ]
```

---

## 4 Optimization Objectives

All objectives are maximized (negated for PyMOO minimization):

| Objective | Range | Description |
|-----------|-------|-------------|
| task_accuracy | 0-1 | Correctness of task completion |
| token_efficiency | 0-1 | Token usage optimization |
| edge_robustness | 0-1 | Handling of edge cases |
| epistemic_consistency | 0-1 | Consistency of epistemic markers |

### Objective Functions

```python
# Task accuracy: more frames + stricter = better
task_accuracy = 0.7 + (frame_count * 0.04) + (strictness * 0.08)

# Token efficiency: fewer frames + more compression = better
token_efficiency = 0.9 - (frame_count * 0.06) - (strictness * 0.04) + (compression * 0.05)

# Edge robustness: evidential + require_ground = more robust
edge_robustness = 0.5 + (evidential * 0.2) + (require_ground * 0.2) + (strictness * 0.05)

# Epistemic consistency: strictness + require_ground = more consistent
epistemic_consistency = 0.4 + (strictness * 0.2) + (require_ground * 0.15) + (evidential * 0.1)
```

---

## Two-Stage Optimization Pipeline

### Stage 1: GlobalMOO (5D Exploration)

```python
from optimization.globalmoo_client import GlobalMOOClient

client = GlobalMOOClient(
    api_key=os.environ["GLOBALMOO_API_KEY"],
    model_id=2193,
    project_id=8318,
)

# Load initial seed cases (151 from auto-generate)
cases = client.get_seed_cases()

# Report outcomes for each case
for case in cases:
    outcomes = evaluate_config_5dim(case.config_vector)
    client.report_outcome(case.config_vector, outcomes)

# Get Pareto frontier
pareto = client.get_pareto_frontier()  # ~100 solutions
```

### Stage 2: PyMOO NSGA-II (14D Refinement)

```python
from optimization.two_stage_optimizer import run_two_stage_optimization

# Expand 5D Pareto to 14D seeds
seeds_14d = [expand_5d_to_14d(p.config_vector) for p in pareto]

# Run PyMOO NSGA-II
results = run_two_stage_optimization(
    seeds=seeds_14d,
    population_size=200,
    generations=100,
)

# Distill to named modes
from optimization.distill_modes import distill_named_modes
modes = distill_named_modes(results.pareto_front)
```

---

## Subscription Limits

| Feature | Free | Paid |
|---------|------|------|
| Input dimensions | 5 | Unlimited |
| Models | 3 | Unlimited |
| Trials/month | 1000 | Unlimited |
| Inverse queries | Limited | Unlimited |

---

## Client Usage

### Initialize Client

```python
from optimization.globalmoo_client import GlobalMOOClient

client = GlobalMOOClient(
    api_key=os.environ.get("GLOBALMOO_API_KEY"),
    model_id=2193,
    project_id=8318,
    mock_mode=False,  # Set True for testing without API
)
```

### Check API Health

```python
status = client.health_check()
print(f"API Status: {status}")
```

### Report Evaluation

```python
from optimization.globalmoo_client import OptimizationOutcome

outcome = OptimizationOutcome(
    config_vector=[0.9, 0.8, 2, 1, 0.7],
    outcomes={
        "task_accuracy": 0.92,
        "token_efficiency": 0.78,
        "edge_robustness": 0.85,
        "epistemic_consistency": 0.91,
    },
)

client.report_outcome(outcome)
```

### Get Pareto Frontier

```python
pareto = client.get_pareto_frontier()
for point in pareto:
    print(f"Config: {point.config_vector}")
    print(f"Outcomes: {point.outcomes}")
```

---

## Troubleshooting

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid API key | Check GLOBALMOO_API_KEY |
| 403 Forbidden | Subscription limit | Check dimension count |
| 404 Not Found | Invalid model/project ID | Verify IDs in dashboard |
| 429 Too Many Requests | Rate limit | Add retry logic |

### Debug Mode

```python
client = GlobalMOOClient(
    api_key=os.environ.get("GLOBALMOO_API_KEY"),
    model_id=2193,
    project_id=8318,
    debug=True,  # Enables verbose logging
)
```

---

## Related Files

| File | Purpose |
|------|---------|
| `optimization/globalmoo_client.py` | API client implementation |
| `optimization/two_stage_optimizer.py` | Two-stage pipeline |
| `optimization/distill_modes.py` | Mode distillation |
| `storage/two_stage_optimization/` | Results storage |
| `docs/SYSTEM-INDEX.md` | Full system documentation |

---

*Generated: 2025-12-28*
*API: GlobalMOO v1*
