# Hyperparameter Calibration Documentation

**Last Updated**: 2025-12-28
**Module**: `optimization/two_stage_optimizer.py`

---

## Overview

The objective functions in `two_stage_optimizer.py` use calibrated coefficients
to model the relationship between configuration dimensions and optimization
objectives. This document explains the rationale behind each coefficient.

**IMPORTANT**: These are SYNTHETIC objective functions for optimization
exploration. They approximate expected behavior but are not a substitute for
real LLM task execution. See `RealTaskEvaluator` for production evaluation.

---

## Objective Function Coefficients

### Task Accuracy

| Constant | Value | Rationale |
|----------|-------|-----------|
| `BASE_ACCURACY` | 0.7 | Baseline accuracy with no cognitive frames |
| `FRAME_ACCURACY_COEFFICIENT` | 0.04 | Each active frame adds ~4% accuracy |
| `STRICTNESS_ACCURACY_COEFFICIENT` | 0.08 | Each VERIX strictness level adds ~8% |

**Model**: `accuracy = 0.7 + (frames * 0.04) + (strictness * 0.08)`

**Hypothesis**: More cognitive frames force more structured thinking, improving
accuracy. Stricter VERIX requirements (mandatory grounding, confidence) reduce
hallucination.

---

### Token Efficiency

| Constant | Value | Rationale |
|----------|-------|-----------|
| `BASE_EFFICIENCY` | 0.9 | High efficiency without cognitive overhead |
| `FRAME_EFFICIENCY_COST` | 0.06 | Each frame costs ~6% efficiency |
| `STRICTNESS_EFFICIENCY_COST` | 0.04 | Each strictness level costs ~4% |
| `COMPRESSION_EFFICIENCY_GAIN` | 0.05 | Compression gains ~5% per level |

**Model**: `efficiency = 0.9 - (frames * 0.06) - (strictness * 0.04) + (compression * 0.05)`

**Hypothesis**: Cognitive frames require additional tokens for compliance markers.
Higher compression levels reduce token usage through abbreviated notation.

---

### Edge Robustness

| Constant | Value | Rationale |
|----------|-------|-----------|
| `BASE_ROBUSTNESS` | 0.5 | 50% baseline edge case handling |
| `EVIDENTIAL_ROBUSTNESS_GAIN` | 0.2 | Evidential frame adds 20% |
| `GROUND_ROBUSTNESS_GAIN` | 0.2 | Requiring ground adds 20% |

**Model**: `robustness = 0.5 + (evidential * 0.2) + (require_ground * 0.2) + (strictness * 0.05)`

**Hypothesis**: Evidential marking forces explicit sourcing, which helps identify
when claims lack support. Grounding requirements prevent unsupported assertions
that fail on edge cases.

---

### Epistemic Consistency

| Constant | Value | Rationale |
|----------|-------|-----------|
| `BASE_CONSISTENCY` | 0.4 | 40% baseline consistency |
| `STRICTNESS_CONSISTENCY_GAIN` | 0.2 | Strictness adds 20% |
| `CONFIDENCE_CONSISTENCY_GAIN` | 0.15 | Confidence requirements add 15% |

**Model**: `consistency = 0.4 + (strictness * 0.2) + (require_ground * 0.15) + (evidential * 0.1)`

**Hypothesis**: Stricter VERIX requirements enforce consistent formatting and
claim structure. Confidence requirements prevent overconfident assertions that
conflict with later cautious statements.

---

## Calibration Methodology

These coefficients were estimated through:

1. **Qualitative Reasoning**: Based on expected behavior of cognitive frames
2. **Synthetic Testing**: Manual testing across configuration space
3. **Pareto Frontier Analysis**: Examining trade-off curves

**Limitations**:
- Not calibrated against real LLM execution
- Linear relationships assumed (reality may be non-linear)
- No interaction effects modeled (frame combinations)

---

## Future Work

1. **Real Evaluation Loop**: Wire RealTaskEvaluator through these functions
2. **A/B Testing**: Compare synthetic vs real objective correlations
3. **Bayesian Calibration**: Use real data to update coefficient priors
4. **Interaction Effects**: Model frame combinations (e.g., evidential + aspectual)

---

## References

- `optimization/two_stage_optimizer.py`: Implementation
- `core/verilingua.py`: Cognitive frame definitions
- `core/verix.py`: VERIX notation system
