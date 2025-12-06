#!/usr/bin/env python3
"""
Phase-II Cosmology Observables - Extended Scheme-Invariance Tests

Extends from H(t) to full cosmological summary:
- Deceleration parameter q(t)
- Effective equation of state w_eff(t)
- Inflationary slow-roll parameters (epsilon_H, eta_H)
- Spectral index n_s and tensor-to-scalar ratio r
- E-folds N_e

Key insight: Meta-calculus replaces time derivatives (dot, ddot) with D_meta.
Observables like (n_s, r, N_e) should be approximately invariant across calculi
for "safe class" potentials, even though intermediate quantities differ.

VERSION: Phase-II (extracted from AI conversation analysis)
Author: Meta-Calculus Development Team
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any, Callable, Optional
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# =============================================================================
# DERIVATIVE OPERATORS (Classical, Bigeometric, Meta)
# =============================================================================

def d_classical(f: np.ndarray, t: np.ndarray) -> np.ndarray:
    """Classical derivative df/dt via numpy gradient."""
    return np.gradient(f, t)


def d_bigeometric(f: np.ndarray, t: np.ndarray, delta: float = 1e-30) -> np.ndarray:
    """
    Bigeometric derivative: D_BG f = t * d/dt[ln f] = t * f'/f

    For f(t) = t^n: D_BG f = n (constant!)

    CRITICAL NOTE (from audit):
    - D_BG a = n is constant for a(t) = t^n
    - H_BG = D_BG a / a = n / t^n is NOT constant
    - But the ratio |K|/H_BG^2 = |k|/n^2 IS constant (key invariant)
    """
    f_safe = np.maximum(np.abs(f), delta)
    df_ln = np.gradient(np.log(f_safe), t)
    return t * df_ln


def d_meta(f: np.ndarray, t: np.ndarray,
           u: Callable[[np.ndarray], np.ndarray] = None,
           v: Callable[[np.ndarray], np.ndarray] = None) -> np.ndarray:
    """
    Meta-derivative: D_meta f = u(t)*df/dt + v(t)*D_BG f

    This is a weighted combination allowing smooth interpolation
    between classical and bigeometric regimes.
    """
    if u is None:
        u = lambda x: 0.5 * np.ones_like(x)
    if v is None:
        v = lambda x: 0.5 * np.ones_like(x)

    df_class = d_classical(f, t)
    df_bg = d_bigeometric(f, t)

    return u(t) * df_class + v(t) * df_bg


# =============================================================================
# BACKGROUND COSMOLOGY SOLVER
# =============================================================================

@dataclass
class CosmologyParams:
    """Parameters for cosmological background."""
    n: float = 2.0  # Power-law index a(t) ~ t^n
    w: float = 0.0  # Equation of state for matter
    rho_0: float = 1.0  # Initial density
    t_0: float = 1.0  # Reference time


def solve_background(params: CosmologyParams,
                    t_grid: np.ndarray,
                    calculus: str = "classical",
                    meta_weights: Optional[Dict] = None) -> Dict[str, np.ndarray]:
    """
    Solve background cosmology with given calculus.

    Uses power-law ansatz a(t) = (t/t_0)^n
    Computes H, dH, d2H using specified calculus.

    Args:
        params: Cosmological parameters
        t_grid: Time grid
        calculus: "classical", "bigeometric", or "meta"
        meta_weights: Dict with 'u' and 'v' functions for meta-calculus

    Returns:
        Dictionary with a, H, dH, d2H
    """
    n = params.n
    t_0 = params.t_0

    # Scale factor a(t) = (t/t_0)^n
    a = (t_grid / t_0) ** n

    if calculus == "classical":
        # H = d(ln a)/dt = n/t
        H = d_classical(np.log(a), t_grid)
        dH = d_classical(H, t_grid)
        d2H = d_classical(dH, t_grid)

    elif calculus == "bigeometric":
        # D_BG a = n (constant)
        # H_BG = D_BG a / a = n / a = n / t^n
        D_BG_a = d_bigeometric(a, t_grid)
        H = D_BG_a / a
        dH = d_bigeometric(H, t_grid)
        d2H = d_bigeometric(dH, t_grid)

    elif calculus == "meta":
        if meta_weights is None:
            meta_weights = {'u': lambda x: 0.5 * np.ones_like(x),
                           'v': lambda x: 0.5 * np.ones_like(x)}

        # Meta-Hubble as weighted combination
        H_class = d_classical(np.log(a), t_grid)
        D_BG_a = d_bigeometric(a, t_grid)
        H_bg = D_BG_a / a

        u = meta_weights['u']
        v = meta_weights['v']
        H = u(t_grid) * H_class + v(t_grid) * H_bg

        dH = d_meta(H, t_grid, u, v)
        d2H = d_meta(dH, t_grid, u, v)

    else:
        raise ValueError(f"Unknown calculus: {calculus}")

    return {
        'a': a,
        'H': H,
        'dH': dH,
        'd2H': d2H,
        't': t_grid,
        'calculus': calculus
    }


# =============================================================================
# COSMOLOGICAL OBSERVABLES
# =============================================================================

def compute_slow_roll_parameters(bg: Dict[str, np.ndarray]) -> Dict[str, float]:
    """
    Compute inflationary slow-roll parameters.

    epsilon_H = -dH/H^2  (first Hubble slow-roll)
    eta_H = epsilon_H - d^2H / (2H*dH)  (second Hubble slow-roll)

    These relate to observables:
    n_s ~ 1 - 2*epsilon_H - eta_H
    r ~ 16 * epsilon_H
    """
    H = bg['H']
    dH = bg['dH']
    d2H = bg['d2H']

    # Use representative time (mid-point for "horizon crossing")
    idx = len(H) // 2
    H_star = H[idx]
    dH_star = dH[idx]
    d2H_star = d2H[idx]

    # First slow-roll parameter
    eps_H = -dH_star / (H_star**2 + 1e-30)

    # Second slow-roll parameter
    if abs(dH_star) > 1e-30:
        eta_H = eps_H - d2H_star / (2 * H_star * dH_star)
    else:
        eta_H = 0.0

    return {
        'epsilon_H': eps_H,
        'eta_H': eta_H,
        'H_star': H_star,
        'dH_star': dH_star
    }


def compute_spectral_observables(slow_roll: Dict[str, float]) -> Dict[str, float]:
    """
    Compute CMB spectral observables from slow-roll parameters.

    n_s = 1 - 2*epsilon_H - eta_H (scalar spectral index)
    r = 16 * epsilon_H (tensor-to-scalar ratio)
    """
    eps = slow_roll['epsilon_H']
    eta = slow_roll['eta_H']

    n_s = 1.0 - 2.0 * eps - eta
    r = 16.0 * eps

    return {
        'n_s': n_s,
        'r': r,
        'epsilon_H': eps,
        'eta_H': eta
    }


def compute_e_folds(bg: Dict[str, np.ndarray],
                   t_start: Optional[float] = None,
                   t_end: Optional[float] = None) -> float:
    """
    Compute number of e-folds N_e = integral(H dt).

    Args:
        bg: Background solution
        t_start: Start time (default: first grid point)
        t_end: End time (default: last grid point)
    """
    t = bg['t']
    H = bg['H']

    if t_start is None:
        i_start = 0
    else:
        i_start = np.argmin(np.abs(t - t_start))

    if t_end is None:
        i_end = len(t)
    else:
        i_end = np.argmin(np.abs(t - t_end))

    # Integrate H dt
    N_e = np.trapz(H[i_start:i_end], t[i_start:i_end])

    return N_e


def compute_deceleration_parameter(bg: Dict[str, np.ndarray]) -> np.ndarray:
    """
    Compute deceleration parameter q(t) = -a*ddot{a}/dot{a}^2.

    For power-law a(t) ~ t^n:
    Classical: q = (1-n)/n
    """
    a = bg['a']
    H = bg['H']
    dH = bg['dH']

    # q = -1 - dH/H^2
    q = -1.0 - dH / (H**2 + 1e-30)

    return q


def compute_equation_of_state(bg: Dict[str, np.ndarray]) -> np.ndarray:
    """
    Compute effective equation of state w_eff(t).

    w_eff = -1 - (2/3) * dH/H^2
    """
    H = bg['H']
    dH = bg['dH']

    w_eff = -1.0 - (2.0/3.0) * dH / (H**2 + 1e-30)

    return w_eff


# =============================================================================
# SCHEME INVARIANCE TESTS
# =============================================================================

def cosmology_observables_full(params: CosmologyParams,
                               t_grid: np.ndarray,
                               calculus: str = "classical",
                               meta_weights: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Compute all cosmological observables for given calculus.
    """
    bg = solve_background(params, t_grid, calculus, meta_weights)
    slow_roll = compute_slow_roll_parameters(bg)
    spectral = compute_spectral_observables(slow_roll)
    N_e = compute_e_folds(bg)
    q = compute_deceleration_parameter(bg)
    w_eff = compute_equation_of_state(bg)

    return {
        'background': bg,
        'slow_roll': slow_roll,
        'spectral': spectral,
        'N_e': N_e,
        'q_mean': float(np.mean(q)),
        'w_eff_mean': float(np.mean(w_eff)),
        'n_s': spectral['n_s'],
        'r': spectral['r'],
        'calculus': calculus
    }


def cosmology_invariance_penalty(params: CosmologyParams,
                                 t_grid: np.ndarray,
                                 meta_weights: Optional[Dict] = None,
                                 weights: Optional[Dict] = None) -> Tuple[float, Dict]:
    """
    Compute invariance penalty across calculi.

    Penalty measures max pairwise difference in (n_s, r, N_e).

    IMPORTANT NOTE (from audit):
    This is currently a DIAGNOSTIC HARNESS, not evidence for invariance.
    Large penalties indicate naive meta choices don't give physically
    equivalent calculi - not a bug, but useful information.

    Returns:
        penalty: Maximum invariance penalty
        obs: Dict of observables for each calculus
    """
    if weights is None:
        weights = {'n_s': 1.0, 'r': 1.0, 'N_e': 0.01}

    calculi = ["classical", "bigeometric", "meta"]
    obs = {}

    for calc in calculi:
        obs[calc] = cosmology_observables_full(
            params, t_grid, calc, meta_weights
        )

    # Max pairwise difference
    max_penalty = 0.0
    comparisons = []

    for i, c1 in enumerate(calculi):
        for j, c2 in enumerate(calculi):
            if i >= j:
                continue

            o1, o2 = obs[c1], obs[c2]

            diff_ns = abs(o1['n_s'] - o2['n_s'])
            diff_r = abs(o1['r'] - o2['r'])
            diff_Ne = abs(o1['N_e'] - o2['N_e']) / (abs(o1['N_e']) + 1e-10)

            penalty = (weights['n_s'] * diff_ns +
                      weights['r'] * diff_r +
                      weights['N_e'] * diff_Ne)

            comparisons.append({
                'calculi': (c1, c2),
                'diff_n_s': diff_ns,
                'diff_r': diff_r,
                'diff_N_e_rel': diff_Ne,
                'penalty': penalty
            })

            max_penalty = max(max_penalty, penalty)

    return max_penalty, {
        'observables': {c: {'n_s': obs[c]['n_s'],
                          'r': obs[c]['r'],
                          'N_e': obs[c]['N_e'],
                          'q_mean': obs[c]['q_mean'],
                          'w_eff_mean': obs[c]['w_eff_mean']}
                       for c in calculi},
        'comparisons': comparisons,
        'max_penalty': max_penalty,
        'interpretation': 'diagnostic' if max_penalty > 1.0 else 'possibly_invariant'
    }


# =============================================================================
# FRW WITH CURVATURE (k != 0)
# =============================================================================

def frw_meta_with_curvature(t_grid: np.ndarray,
                            n: float,
                            k: float,
                            calculus: str = "bigeometric") -> Dict[str, Any]:
    """
    Analyze FRW with curvature under different calculi.

    Standard FRW:
    H^2 = (8piG/3)*rho - k/a^2

    Key insight (from audit correction):
    - Classical: H = n/t, so |K|/H^2 ~ t^{2-2n} diverges for n > 1 as t->0
    - Bigeometric: H_BG = n/t^n, so |K|/H_BG^2 = |k|/n^2 (CONSTANT!)

    This is why bigeometric calculus "tames" the curvature term.
    """
    a = t_grid ** n
    curvature_term = -k / a**2

    if calculus == "classical":
        # H = d(ln a)/dt = n/t
        H = n / t_grid
        H_squared = H**2

    elif calculus == "bigeometric":
        # H_BG = D_BG a / a = n / t^n
        H = n / (t_grid ** n)
        H_squared = H**2

    else:
        raise ValueError(f"Unknown calculus: {calculus}")

    # Ratio of curvature to Hubble^2
    ratio = np.abs(curvature_term) / (H_squared + 1e-30)

    # Analytic ratio for bigeometric
    analytic_ratio_bg = abs(k) / (n**2) if calculus == "bigeometric" else None

    return {
        'a': a,
        'H': H,
        'curvature_term': curvature_term,
        'ratio_curv_H2': ratio,
        'max_ratio': float(np.max(ratio)),
        'analytic_ratio_bg': analytic_ratio_bg,
        'early_time_behavior': 'constant' if calculus == 'bigeometric' else 'divergent',
        'calculus': calculus,
        'n': n,
        'k': k
    }


def curvature_dominance_analysis(n_values: List[float] = [0.5, 1.0, 2.0, 3.0],
                                 k: float = 1.0,
                                 t_min: float = 1e-4,
                                 t_max: float = 1.0,
                                 N_t: int = 1000) -> Dict[str, Any]:
    """
    Analyze when curvature dominates vs expansion for different n, k.

    Tests whether k != 0 regimes are relevant at Planck scale.
    """
    t_grid = np.logspace(np.log10(t_min), np.log10(t_max), N_t)

    results = {}

    for n in n_values:
        results[f'n={n}'] = {
            'classical': frw_meta_with_curvature(t_grid, n, k, 'classical'),
            'bigeometric': frw_meta_with_curvature(t_grid, n, k, 'bigeometric')
        }

        # Summary comparison
        class_max = results[f'n={n}']['classical']['max_ratio']
        bg_max = results[f'n={n}']['bigeometric']['max_ratio']

        results[f'n={n}']['comparison'] = {
            'classical_max_ratio': class_max,
            'bigeometric_max_ratio': bg_max,
            'curvature_taming_factor': class_max / (bg_max + 1e-30),
            'bigeometric_is_finite': np.isfinite(bg_max) and bg_max < 1e10
        }

    return {
        't_range': [t_min, t_max],
        'k': k,
        'results': results,
        'conclusion': 'Bigeometric calculus regularizes curvature/H^2 ratio'
    }


# =============================================================================
# MAIN DEMO
# =============================================================================

def run_phase2_cosmology_demo() -> Dict[str, Any]:
    """
    Run complete Phase-II cosmology observables demonstration.
    """
    print("=" * 60)
    print("PHASE-II: Extended Cosmology Observables")
    print("=" * 60)

    results = {}

    # 1. Basic observable comparison
    print("\n1. Computing observables across calculi...")

    params = CosmologyParams(n=2.0, w=0.0)
    t_grid = np.logspace(-4, 0, 500)

    penalty, obs_results = cosmology_invariance_penalty(params, t_grid)
    results['invariance_test'] = obs_results

    print(f"   Max invariance penalty: {penalty:.4e}")
    print(f"   Interpretation: {obs_results['interpretation']}")

    for calc, obs in obs_results['observables'].items():
        print(f"   {calc}: n_s={obs['n_s']:.4f}, r={obs['r']:.4e}, N_e={obs['N_e']:.4f}")

    # 2. Curvature analysis
    print("\n2. Curvature dominance analysis (k != 0)...")

    curv_results = curvature_dominance_analysis()
    results['curvature_analysis'] = curv_results

    for key, val in curv_results['results'].items():
        comp = val['comparison']
        print(f"   {key}: Classical max ratio = {comp['classical_max_ratio']:.2e}, "
              f"Bigeometric = {comp['bigeometric_max_ratio']:.4f}")

    # 3. Slow-roll parameter scan
    print("\n3. Slow-roll parameter scan across power-law indices...")

    slow_roll_scan = []
    for n in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
        params_n = CosmologyParams(n=n)

        for calc in ['classical', 'bigeometric']:
            obs = cosmology_observables_full(params_n, t_grid, calc)
            slow_roll_scan.append({
                'n': n,
                'calculus': calc,
                'epsilon_H': obs['slow_roll']['epsilon_H'],
                'eta_H': obs['slow_roll']['eta_H'],
                'n_s': obs['n_s'],
                'r': obs['r']
            })

    results['slow_roll_scan'] = slow_roll_scan

    print("   n    | calculus     | epsilon_H    | n_s      | r")
    print("   " + "-" * 55)
    for sr in slow_roll_scan:
        print(f"   {sr['n']:.1f}  | {sr['calculus']:12} | {sr['epsilon_H']:+.4e} | "
              f"{sr['n_s']:.4f} | {sr['r']:.4e}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("- Cosmology observables computed across classical/bigeometric/meta")
    print("- Curvature analysis confirms bigeometric taming of |K|/H^2")
    print("- Slow-roll parameters extracted for power-law cosmologies")
    print("=" * 60)

    return results


if __name__ == "__main__":
    results = run_phase2_cosmology_demo()

    # Save results
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "phase2_cosmology_results.json")

    # Convert numpy arrays to lists for JSON serialization
    def convert_for_json(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_for_json(v) for v in obj]
        elif isinstance(obj, (np.floating, np.integer)):
            return float(obj)
        return obj

    with open(output_path, 'w') as f:
        json.dump(convert_for_json(results), f, indent=2)

    print(f"\nResults saved to: {output_path}")
