#!/usr/bin/env python3
"""
Phase-II Amplitude Representation Invariance

Tests scheme-invariance across amplitude representations:
- Feynman diagrams
- BCFW recursion
- Amplituhedron / positive geometry

Key insight from AI conversation:
Pick tree-level 4-pt color-ordered gluon amplitude (MHV) in N=4 SYM
as a testbed. Different representations should give identical results.

Parke-Taylor: A_4(1^-,2^-,3^+,4^+) = i * <12>^4 / (<12><23><34><41>)

CURRENT STATUS: Structural placeholder with correct invariance testing pattern.
All three "representations" currently call the same function - this proves the
penalty logic works, not anything about real Feynman vs BCFW vs amplituhedron.

VERSION: Phase-II (extracted from AI conversation analysis)
Author: Meta-Calculus Development Team
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any, Callable, Optional, Union
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# PyMOO integration
try:
    from pymoo.core.problem import Problem
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.optimize import minimize
    from pymoo.operators.sampling.rnd import FloatRandomSampling
    PYMOO_AVAILABLE = True
except ImportError:
    PYMOO_AVAILABLE = False


# =============================================================================
# SPINOR HELICITY BASICS
# =============================================================================

@dataclass
class SpinorMomentum:
    """
    Spinor-helicity representation of null momentum.

    For null p^mu, we write p = lambda * tilde_lambda
    where lambda is a 2-component spinor.
    """
    lambda_spinor: np.ndarray  # Complex 2-vector
    tilde_lambda: np.ndarray  # Complex 2-vector

    @classmethod
    def from_4momentum(cls, p: np.ndarray) -> 'SpinorMomentum':
        """
        Construct spinors from 4-momentum p^mu = (E, px, py, pz).

        For null momentum p^2 = 0, we have:
        p = |p] <p| in spinor notation.
        """
        E, px, py, pz = p
        pt = np.sqrt(px**2 + py**2)

        if pt > 1e-10:
            lam = np.sqrt(E + pz) * np.array([1.0, (px + 1j*py)/(E + pz + 1e-30)])
            lam_tilde = np.sqrt(E + pz) * np.array([1.0, (px - 1j*py)/(E + pz + 1e-30)])
        else:
            # Special case for pz aligned
            lam = np.array([np.sqrt(E + pz), 0.0], dtype=complex)
            lam_tilde = np.array([np.sqrt(E - pz), 0.0], dtype=complex)

        return cls(lambda_spinor=lam, tilde_lambda=lam_tilde)


def angle_bracket(lam1: np.ndarray, lam2: np.ndarray) -> complex:
    """
    Angle bracket <12> = lambda1_alpha * epsilon^{alpha beta} * lambda2_beta
                       = lambda1[0]*lambda2[1] - lambda1[1]*lambda2[0]
    """
    return lam1[0] * lam2[1] - lam1[1] * lam2[0]


def square_bracket(tilde1: np.ndarray, tilde2: np.ndarray) -> complex:
    """
    Square bracket [12] = tilde_lambda1 * epsilon * tilde_lambda2
    """
    return tilde1[0] * tilde2[1] - tilde1[1] * tilde2[0]


def mandelstam_s(lam_i: np.ndarray, tilde_i: np.ndarray,
                 lam_j: np.ndarray, tilde_j: np.ndarray) -> complex:
    """
    Mandelstam variable s_ij = <ij>[ji]
    """
    return angle_bracket(lam_i, lam_j) * square_bracket(tilde_j, tilde_i)


# =============================================================================
# AMPLITUDE REPRESENTATIONS
# =============================================================================

def parke_taylor_4pt(spinors: List[SpinorMomentum]) -> complex:
    """
    Parke-Taylor formula for 4-point MHV amplitude.

    A_4(1^-,2^-,3^+,4^+) = i * <12>^4 / (<12><23><34><41>)

    Args:
        spinors: List of 4 SpinorMomentum objects

    Returns:
        Complex amplitude value
    """
    if len(spinors) != 4:
        raise ValueError("Need exactly 4 external particles")

    lam = [s.lambda_spinor for s in spinors]

    a12 = angle_bracket(lam[0], lam[1])
    a23 = angle_bracket(lam[1], lam[2])
    a34 = angle_bracket(lam[2], lam[3])
    a41 = angle_bracket(lam[3], lam[0])

    numerator = a12 ** 4
    denominator = a12 * a23 * a34 * a41

    if abs(denominator) < 1e-30:
        return complex(0, 0)

    return 1j * numerator / denominator


def amplitude_feynman(spinors: List[SpinorMomentum]) -> complex:
    """
    Feynman diagram representation of 4-point amplitude.

    In real implementation: explicitly sum s, t channel diagrams.
    Currently: placeholder calling Parke-Taylor (known to be equivalent).
    """
    # TODO: Implement explicit Feynman diagram sum
    # For now, returns same as Parke-Taylor (structurally correct)
    return parke_taylor_4pt(spinors)


def amplitude_bcfw(spinors: List[SpinorMomentum]) -> complex:
    """
    BCFW recursion representation of 4-point amplitude.

    Shift legs 1 and 2, reconstruct from 3-pt amplitudes.
    Currently: placeholder calling Parke-Taylor.
    """
    # TODO: Implement BCFW shift and recursion
    # For now, returns same as Parke-Taylor
    return parke_taylor_4pt(spinors)


def amplitude_amplituhedron(spinors: List[SpinorMomentum]) -> complex:
    """
    Amplituhedron / positive geometry representation.

    At 4-pt MHV, the canonical form reduces to Parke-Taylor factor.
    Currently: placeholder calling Parke-Taylor.
    """
    # TODO: Implement canonical form evaluation
    # For now, returns same as Parke-Taylor
    return parke_taylor_4pt(spinors)


# =============================================================================
# INVARIANCE TESTING
# =============================================================================

def generate_random_kinematics(n_external: int = 4,
                               seed: Optional[int] = None) -> List[SpinorMomentum]:
    """
    Generate random on-shell momenta satisfying momentum conservation.

    For n=4, we generate 3 random momenta and fix the 4th by conservation.
    """
    if seed is not None:
        np.random.seed(seed)

    # Generate random energies and angles for first 3 particles
    spinors = []

    # Random momenta (not yet satisfying conservation)
    total_p = np.zeros(4)

    for i in range(n_external - 1):
        E = np.random.uniform(1.0, 10.0)
        theta = np.random.uniform(0, np.pi)
        phi = np.random.uniform(0, 2 * np.pi)

        px = E * np.sin(theta) * np.cos(phi)
        py = E * np.sin(theta) * np.sin(phi)
        pz = E * np.cos(theta)

        p = np.array([E, px, py, pz])
        total_p += p

        spinors.append(SpinorMomentum.from_4momentum(p))

    # Last momentum fixed by conservation: p_4 = -sum(p_1 to p_3)
    p4 = -total_p
    p4[0] = np.sqrt(p4[1]**2 + p4[2]**2 + p4[3]**2)  # Make massless
    spinors.append(SpinorMomentum.from_4momentum(p4))

    return spinors


def amplitude_invariance_penalty(spinors: List[SpinorMomentum]) -> Tuple[float, Dict]:
    """
    Compute invariance penalty across amplitude representations.

    Returns maximum relative difference between any pair of representations.
    """
    A_feynman = amplitude_feynman(spinors)
    A_bcfw = amplitude_bcfw(spinors)
    A_amplituhedron = amplitude_amplituhedron(spinors)

    vals = [A_feynman, A_bcfw, A_amplituhedron]
    names = ["Feynman", "BCFW", "Amplituhedron"]

    # Compute pairwise differences
    penalty = 0.0
    comparisons = []

    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            diff = abs(vals[i] - vals[j])
            norm = max(abs(vals[i]), abs(vals[j]), 1e-16)
            rel_diff = diff / norm

            comparisons.append({
                'pair': (names[i], names[j]),
                'absolute_diff': float(diff),
                'relative_diff': float(rel_diff)
            })

            penalty = max(penalty, rel_diff)

    return penalty, {
        'amplitudes': {names[i]: {'real': float(vals[i].real),
                                 'imag': float(vals[i].imag),
                                 'abs': float(abs(vals[i]))}
                      for i in range(len(vals))},
        'comparisons': comparisons,
        'max_penalty': float(penalty),
        'is_invariant': penalty < 1e-10,
        'note': 'Currently placeholder - all representations identical by construction'
    }


def scan_kinematic_space(n_samples: int = 100,
                        seed: int = 42) -> Dict[str, Any]:
    """
    Scan across random kinematic configurations.

    Tests amplitude invariance across momentum space.
    """
    np.random.seed(seed)

    penalties = []
    all_results = []

    for i in range(n_samples):
        spinors = generate_random_kinematics(4, seed=seed + i)
        penalty, result = amplitude_invariance_penalty(spinors)
        penalties.append(penalty)
        all_results.append(result)

    return {
        'n_samples': n_samples,
        'max_penalty': float(np.max(penalties)),
        'mean_penalty': float(np.mean(penalties)),
        'std_penalty': float(np.std(penalties)),
        'all_invariant': all(p < 1e-10 for p in penalties),
        'penalty_distribution': {
            'min': float(np.min(penalties)),
            'p25': float(np.percentile(penalties, 25)),
            'p50': float(np.percentile(penalties, 50)),
            'p75': float(np.percentile(penalties, 75)),
            'max': float(np.max(penalties))
        }
    }


# =============================================================================
# TOY SCALAR AMPLITUDE (SIMPLER FOR TESTING)
# =============================================================================

def parke_taylor_scalar_toy(s: float, t: float, g: float = 1.0) -> float:
    """
    Toy scalar amplitude: A(s,t) = g^2 * (1/s + 1/t)

    This simple form allows testing the invariance infrastructure
    before full spinor-helicity implementation.
    """
    if abs(s) < 1e-30 or abs(t) < 1e-30:
        return 0.0
    return g**2 * (1.0/s + 1.0/t)


def scalar_feynman(s: float, t: float, g: float = 1.0) -> float:
    """Feynman representation of scalar toy amplitude."""
    # s-channel + t-channel
    return parke_taylor_scalar_toy(s, t, g)


def scalar_bcfw(s: float, t: float, g: float = 1.0) -> float:
    """BCFW-like representation."""
    return parke_taylor_scalar_toy(s, t, g)


def scalar_positive_geometry(s: float, t: float, g: float = 1.0) -> float:
    """Positive geometry representation."""
    return parke_taylor_scalar_toy(s, t, g)


def scalar_amplitude_invariance(s_range: Tuple[float, float] = (1.0, 2.0),
                                t_range: Tuple[float, float] = (1.5, 2.5),
                                n_samples: int = 50) -> Dict[str, Any]:
    """
    Test invariance of scalar toy amplitudes across representations.
    """
    s_vals = np.linspace(*s_range, n_samples)
    t_vals = np.linspace(*t_range, n_samples)

    penalties = []

    for s in s_vals:
        for t in t_vals:
            A_F = scalar_feynman(s, t)
            A_B = scalar_bcfw(s, t)
            A_P = scalar_positive_geometry(s, t)

            vals = [A_F, A_B, A_P]
            mu = np.mean(vals)

            if abs(mu) > 1e-16:
                penalty = np.mean([abs(v - mu)/abs(mu) for v in vals])
            else:
                penalty = 0.0

            penalties.append(penalty)

    return {
        's_range': s_range,
        't_range': t_range,
        'n_samples': n_samples,
        'max_penalty': float(np.max(penalties)),
        'mean_penalty': float(np.mean(penalties)),
        'invariance_verified': np.max(penalties) < 1e-10,
        'note': 'Toy scalar amplitude - all representations identical'
    }


# =============================================================================
# POSITIVE GEOMETRY STRUCTURES
# =============================================================================

@dataclass
class PositiveGeometry:
    """
    Base class for positive geometries (amplituhedron, associahedron, etc.)

    A positive geometry is a polytope/variety with a unique canonical form
    having logarithmic singularities on boundaries.
    """
    dim: int
    name: str

    def canonical_form_at(self, point: np.ndarray) -> complex:
        """Evaluate canonical form at a point."""
        raise NotImplementedError

    def is_inside(self, point: np.ndarray) -> bool:
        """Check if point is inside the positive region."""
        raise NotImplementedError


class Simplex(PositiveGeometry):
    """
    n-simplex as a simple positive geometry.

    Canonical form: Omega = dx_1 ^ ... ^ dx_n / (x_1 * ... * x_n)
    with x_i >= 0 and sum(x_i) <= 1.
    """

    def __init__(self, dim: int = 2):
        super().__init__(dim=dim, name=f"{dim}-simplex")

    def canonical_form_at(self, point: np.ndarray) -> complex:
        """Canonical form has 1/product(coords) behavior."""
        if len(point) != self.dim + 1:
            raise ValueError(f"Point must have {self.dim + 1} coordinates")

        product = np.prod(point)
        if abs(product) < 1e-30:
            return complex(np.inf, 0)

        return complex(1.0 / product, 0)

    def is_inside(self, point: np.ndarray) -> bool:
        """Check if in positive simplex."""
        return all(p >= 0 for p in point) and sum(point) <= 1 + 1e-10


class Associahedron(PositiveGeometry):
    """
    Associahedron (Stasheff polytope) for phi^3 amplitudes.

    Dimension n-3 for n-particle scattering.
    """

    def __init__(self, n_particles: int = 4):
        self.n = n_particles
        super().__init__(dim=n_particles - 3, name=f"Associahedron K_{n_particles-1}")

    def canonical_form_at(self, planar_vars: np.ndarray) -> complex:
        """
        Canonical form in planar kinematic variables.

        For n=4: just 1/s or 1/t type poles.
        """
        if len(planar_vars) != self.dim:
            raise ValueError(f"Need {self.dim} planar variables")

        # Simplified: product of 1/X_i
        product = np.prod(planar_vars)
        if abs(product) < 1e-30:
            return complex(np.inf, 0)

        return complex(1.0 / product, 0)


# =============================================================================
# MAIN DEMO
# =============================================================================

def run_phase2_amplitude_demo() -> Dict[str, Any]:
    """
    Run complete Phase-II amplitude invariance demonstration.
    """
    print("=" * 60)
    print("PHASE-II: Amplitude Representation Invariance")
    print("=" * 60)

    results = {}

    # 1. Scalar toy amplitudes
    print("\n1. Testing scalar toy amplitude invariance...")

    scalar_result = scalar_amplitude_invariance()
    results['scalar_toy'] = scalar_result

    print(f"   Max penalty: {scalar_result['max_penalty']:.2e}")
    print(f"   Invariance verified: {scalar_result['invariance_verified']}")

    # 2. Spinor-helicity amplitudes
    print("\n2. Testing spinor-helicity 4-pt amplitudes...")

    kinematic_scan = scan_kinematic_space(n_samples=50)
    results['spinor_helicity'] = kinematic_scan

    print(f"   Samples tested: {kinematic_scan['n_samples']}")
    print(f"   Max penalty: {kinematic_scan['max_penalty']:.2e}")
    print(f"   All invariant: {kinematic_scan['all_invariant']}")

    # 3. Positive geometry examples
    print("\n3. Testing positive geometry canonical forms...")

    simplex = Simplex(dim=2)
    test_point = np.array([0.3, 0.3, 0.4])

    results['positive_geometry'] = {
        'simplex_dim': simplex.dim,
        'test_point': test_point.tolist(),
        'inside_simplex': simplex.is_inside(test_point),
        'canonical_form': float(simplex.canonical_form_at(test_point).real)
    }

    print(f"   2-simplex test point: {test_point}")
    print(f"   Inside: {simplex.is_inside(test_point)}")
    print(f"   Canonical form: {results['positive_geometry']['canonical_form']:.4f}")

    # 4. Single detailed example
    print("\n4. Detailed amplitude comparison at one kinematic point...")

    spinors = generate_random_kinematics(4, seed=12345)
    penalty, detail = amplitude_invariance_penalty(spinors)
    results['detailed_example'] = detail

    print(f"   Feynman: |A| = {detail['amplitudes']['Feynman']['abs']:.4e}")
    print(f"   BCFW: |A| = {detail['amplitudes']['BCFW']['abs']:.4e}")
    print(f"   Amplituhedron: |A| = {detail['amplitudes']['Amplituhedron']['abs']:.4e}")
    print(f"   Max penalty: {detail['max_penalty']:.2e}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("- Scalar toy amplitude: representations equivalent (tautology)")
    print("- Spinor-helicity: Parke-Taylor formula tested across kinematics")
    print("- Positive geometry: canonical form infrastructure in place")
    print("- NOTE: Currently placeholder - real Feynman/BCFW needed")
    print("=" * 60)

    return results


if __name__ == "__main__":
    results = run_phase2_amplitude_demo()

    # Save results
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "phase2_amplitude_results.json")

    # Convert numpy types for JSON
    def convert_for_json(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_for_json(v) for v in obj]
        elif isinstance(obj, (np.floating, np.integer, np.bool_)):
            if isinstance(obj, np.bool_):
                return bool(obj)
            return float(obj)
        elif isinstance(obj, bool):
            return obj
        return obj

    with open(output_path, 'w') as f:
        json.dump(convert_for_json(results), f, indent=2)

    print(f"\nResults saved to: {output_path}")
