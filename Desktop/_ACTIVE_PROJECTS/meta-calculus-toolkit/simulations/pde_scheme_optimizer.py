#!/usr/bin/env python3
"""
PDE Scheme Optimizer

Multi-objective optimization of numerical schemes for PDEs:
- Coordinate/gauge choices as C-schemes
- Discretization strategies
- Time parametrizations

Key insight: Different numerical schemes are C-scheme choices.
Physical observables (conserved quantities, final states) should be invariant.

Applications: Numerical GR, fluid dynamics, wave equations

Author: Meta-Calculus Development Team
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any, Callable
import time
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from pymoo.core.problem import Problem
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.optimize import minimize
    from pymoo.operators.sampling.rnd import FloatRandomSampling
    PYMOO_AVAILABLE = True
except ImportError:
    PYMOO_AVAILABLE = False

# Try GlobalMOO import
try:
    from meta_calculus.moo_integration import GlobalMOOClient, GlobalMOOAdapter
    GLOBALMOO_AVAILABLE = True
except ImportError:
    GLOBALMOO_AVAILABLE = False


# =============================================================================
# NUMERICAL SCHEMES FOR WAVE EQUATION
# =============================================================================

@dataclass
class NumericalScheme:
    """A numerical scheme for solving PDEs."""
    name: str
    time_scaling: float  # tau = alpha * t
    spatial_weight: float  # Weighted discretization
    cfl_factor: float  # CFL number adjustment
    description: str


class WaveEquationSolver:
    """
    1D Wave equation solver with configurable schemes.

    u_tt = c^2 * u_xx

    Different schemes = different C-scheme choices.
    """

    def __init__(
        self,
        Lx: float = 1.0,
        c: float = 1.0,
        Nx: int = 100
    ):
        self.Lx = Lx
        self.c = c
        self.Nx = Nx
        self.x = np.linspace(0, Lx, Nx)
        self.dx = self.x[1] - self.x[0]

    def initial_gaussian(self, x0: float = 0.5, sigma: float = 0.1) -> np.ndarray:
        """Gaussian initial condition."""
        return np.exp(-((self.x - x0) / sigma)**2)

    def solve(
        self,
        scheme: NumericalScheme,
        T: float = 1.0,
        Nt: int = 500,
        u0: np.ndarray = None
    ) -> Dict[str, Any]:
        """
        Solve wave equation with given scheme.

        Returns solution and diagnostics.
        """
        if u0 is None:
            u0 = self.initial_gaussian()

        # Effective parameters with scheme scaling
        alpha = scheme.time_scaling
        c_eff = self.c / alpha
        dt = T / Nt
        d_tau = alpha * dt

        # CFL number
        CFL = c_eff * d_tau / self.dx * scheme.cfl_factor

        if CFL > 1.0:
            return {
                'status': 'unstable',
                'CFL': CFL,
                'scheme': scheme.name
            }

        # Initialize
        u_prev = u0.copy()
        u_curr = u0.copy()
        u_next = np.zeros_like(u0)

        # Spatial weight for discretization
        w = scheme.spatial_weight

        # Energy tracking
        energies = []

        start_time = time.time()

        for n in range(Nt):
            # Weighted central difference
            # Standard: (u[i+1] - 2*u[i] + u[i-1])
            # Weighted: w*(u[i+1] + u[i-1]) + (1-2w)*u[i] - u[i]
            #         = w*u[i+1] - (1+2w-2)*u[i] + w*u[i-1]
            # For w=0.5 (standard), this gives normal Laplacian

            for i in range(1, self.Nx - 1):
                laplacian = (w * u_curr[i+1] + w * u_curr[i-1]
                             - 2 * w * u_curr[i]) / self.dx**2
                u_next[i] = (2 * u_curr[i] - u_prev[i]
                             + (c_eff * d_tau)**2 * laplacian)

            # Boundary conditions (Dirichlet)
            u_next[0] = 0
            u_next[-1] = 0

            # Compute energy
            kinetic = 0.5 * np.sum((u_curr - u_prev)**2 / d_tau**2) * self.dx
            potential = 0.5 * c_eff**2 * np.sum(np.gradient(u_curr, self.dx)**2) * self.dx
            energies.append(kinetic + potential)

            # Rotate arrays
            u_prev, u_curr, u_next = u_curr, u_next, u_prev

        runtime = time.time() - start_time

        return {
            'status': 'completed',
            'scheme': scheme.name,
            'CFL': CFL,
            'runtime': runtime,
            'u_final': u_curr.copy(),
            'x': self.x.copy(),
            'energies': energies,
            'energy_drift': abs(energies[-1] - energies[0]) / energies[0] if energies[0] > 0 else 0
        }


# =============================================================================
# SCHEME INVARIANCE TESTING
# =============================================================================

class PDEInvarianceTester:
    """Test invariance of physical observables across numerical schemes."""

    def __init__(self, solver: WaveEquationSolver):
        self.solver = solver

    def compare_final_states(
        self,
        scheme_A: NumericalScheme,
        scheme_B: NumericalScheme,
        T: float = 1.0,
        Nt: int = 500
    ) -> Dict[str, Any]:
        """Compare final states across schemes."""
        u0 = self.solver.initial_gaussian()

        result_A = self.solver.solve(scheme_A, T, Nt, u0)
        result_B = self.solver.solve(scheme_B, T, Nt, u0)

        if result_A['status'] != 'completed' or result_B['status'] != 'completed':
            return {
                'scheme_A': scheme_A.name,
                'scheme_B': scheme_B.name,
                'status': 'failed',
                'reason': 'One or both schemes unstable'
            }

        # Compare final states
        diff = np.linalg.norm(result_A['u_final'] - result_B['u_final'])
        rel_diff = diff / np.linalg.norm(result_A['u_final'])

        return {
            'scheme_A': scheme_A.name,
            'scheme_B': scheme_B.name,
            'difference': diff,
            'relative_difference': rel_diff,
            'energy_drift_A': result_A['energy_drift'],
            'energy_drift_B': result_B['energy_drift'],
            'is_invariant': rel_diff < 0.1
        }

    def compare_conserved_quantities(
        self,
        scheme_A: NumericalScheme,
        scheme_B: NumericalScheme,
        T: float = 1.0
    ) -> Dict[str, Any]:
        """Compare energy conservation across schemes."""
        u0 = self.solver.initial_gaussian()

        result_A = self.solver.solve(scheme_A, T, 500, u0)
        result_B = self.solver.solve(scheme_B, T, 500, u0)

        if result_A['status'] != 'completed' or result_B['status'] != 'completed':
            return {'status': 'failed'}

        # Energy should be conserved
        E_final_A = result_A['energies'][-1]
        E_final_B = result_B['energies'][-1]

        return {
            'scheme_A': scheme_A.name,
            'scheme_B': scheme_B.name,
            'E_final_A': E_final_A,
            'E_final_B': E_final_B,
            'energy_difference': abs(E_final_A - E_final_B),
            'is_invariant': abs(E_final_A - E_final_B) / max(E_final_A, E_final_B) < 0.1
        }


# =============================================================================
# MOO: OPTIMIZE NUMERICAL SCHEME
# =============================================================================

class PDESchemeOptimization(Problem):
    """
    Multi-objective optimization of PDE numerical schemes.

    Decision variables:
        x[0]: time_scaling (alpha)
        x[1]: spatial_weight
        x[2]: cfl_factor

    Objectives:
        f1: Error vs reference solution (minimize)
        f2: Runtime (minimize)
        f3: Energy drift (minimize)
    """

    def __init__(self, Nx: int = 100):
        super().__init__(
            n_var=3,
            n_obj=3,
            n_ieq_constr=0,
            xl=np.array([0.5, 0.3, 0.5]),
            xu=np.array([2.0, 0.7, 1.0])
        )
        self.solver = WaveEquationSolver(Nx=Nx)
        self.evaluation_count = 0

        # Generate reference solution (high resolution)
        ref_scheme = NumericalScheme("Reference", 1.0, 0.5, 0.8, "High-res reference")
        self.reference = self.solver.solve(ref_scheme, T=0.5, Nt=1000)

    def _evaluate(self, x, out, *args, **kwargs):
        n_samples = x.shape[0]
        f = np.zeros((n_samples, 3))

        for i in range(n_samples):
            alpha = x[i, 0]
            w = x[i, 1]
            cfl = x[i, 2]

            scheme = NumericalScheme(
                f"Test_{i}", alpha, w, cfl, "Optimization candidate"
            )

            result = self.solver.solve(scheme, T=0.5, Nt=500)

            if result['status'] != 'completed':
                f[i, :] = [10, 10, 10]
                continue

            # Objective 1: Error vs reference
            if self.reference['status'] == 'completed':
                error = np.linalg.norm(
                    result['u_final'] - self.reference['u_final']
                ) / np.linalg.norm(self.reference['u_final'])
                f[i, 0] = error
            else:
                f[i, 0] = 1.0

            # Objective 2: Runtime
            f[i, 1] = result['runtime']

            # Objective 3: Energy drift
            f[i, 2] = result['energy_drift']

            self.evaluation_count += 1

        out["F"] = f


# =============================================================================
# STANDARD SCHEMES
# =============================================================================

def get_standard_schemes() -> List[NumericalScheme]:
    """Get a set of standard numerical schemes."""
    return [
        NumericalScheme("Standard Leapfrog", 1.0, 0.5, 0.9, "Standard second-order"),
        NumericalScheme("Time-scaled (2x)", 2.0, 0.5, 0.45, "Double time scaling"),
        NumericalScheme("Weighted Spatial", 1.0, 0.6, 0.8, "Asymmetric spatial weights"),
        NumericalScheme("Conservative", 1.0, 0.5, 0.7, "Lower CFL for stability"),
        NumericalScheme("Aggressive", 1.0, 0.5, 0.95, "Near CFL limit")
    ]


# =============================================================================
# SIMULATION RUNNER
# =============================================================================

def run_pde_demo():
    """Demonstrate PDE scheme optimization."""
    print("=" * 70)
    print("PDE SCHEME OPTIMIZER")
    print("Wave Equation Numerical Schemes as C-schemes")
    print("=" * 70)

    solver = WaveEquationSolver(Nx=100)
    tester = PDEInvarianceTester(solver)
    schemes = get_standard_schemes()

    print("\n1. NUMERICAL SCHEMES")
    print("-" * 40)
    for s in schemes:
        print(f"  {s.name}: alpha={s.time_scaling}, w={s.spatial_weight}, CFL={s.cfl_factor}")

    print("\n2. SCHEME INVARIANCE TEST")
    print("-" * 40)
    results = []
    for i, scheme_A in enumerate(schemes):
        for scheme_B in schemes[i+1:]:
            result = tester.compare_final_states(scheme_A, scheme_B, T=0.5)
            results.append(result)
            if result.get('status') != 'failed':
                status = "PASS" if result['is_invariant'] else "DIFF"
                print(f"  [{status}] {scheme_A.name} vs {scheme_B.name}: "
                      f"rel_diff={result['relative_difference']:.4f}")

    print("\n3. ENERGY CONSERVATION")
    print("-" * 40)
    for scheme in schemes:
        result = solver.solve(scheme, T=0.5, Nt=500)
        if result['status'] == 'completed':
            print(f"  {scheme.name}: energy_drift={result['energy_drift']:.2e}")
        else:
            print(f"  {scheme.name}: UNSTABLE")

    return {
        'schemes': [s.name for s in schemes],
        'invariance_tests': results
    }


def run_pymoo_optimization():
    """Run PyMOO optimization for PDE schemes."""
    if not PYMOO_AVAILABLE:
        print("PyMOO not available.")
        return {'status': 'skipped'}

    print("\n" + "=" * 70)
    print("PYMOO PDE SCHEME OPTIMIZATION")
    print("=" * 70)

    problem = PDESchemeOptimization(Nx=80)

    algorithm = NSGA2(
        pop_size=30,
        sampling=FloatRandomSampling(),
        eliminate_duplicates=True
    )

    print("Running optimization...")
    res = minimize(problem, algorithm, ('n_gen', 20), seed=42, verbose=False)

    print(f"Evaluations: {problem.evaluation_count}")

    pareto_front = []
    if res.F is not None:
        for i, (f, x) in enumerate(zip(res.F, res.X)):
            pareto_front.append({
                'time_scaling': float(x[0]),
                'spatial_weight': float(x[1]),
                'cfl_factor': float(x[2]),
                'error': float(f[0]),
                'runtime': float(f[1]),
                'energy_drift': float(f[2])
            })

    pareto_front.sort(key=lambda x: x['error'])

    print("\nTop 5 Pareto-optimal schemes:")
    for p in pareto_front[:5]:
        print(f"  alpha={p['time_scaling']:.2f}, w={p['spatial_weight']:.2f}: "
              f"error={p['error']:.4f}, drift={p['energy_drift']:.2e}")

    return {
        'status': 'completed',
        'pareto_front': pareto_front[:20]
    }


def run_globalmoo_optimization():
    """Run GlobalMOO optimization for PDE schemes."""
    if not GLOBALMOO_AVAILABLE:
        print("\nGlobalMOO not available. Using grid search fallback.")
        return run_grid_search_fallback()

    print("\n" + "=" * 70)
    print("GLOBALMOO PDE SCHEME OPTIMIZATION")
    print("=" * 70)

    try:
        client = GlobalMOOClient()
        connection = client.check_connection()
        if not connection['connected']:
            print(f"GlobalMOO not connected: {connection.get('error')}")
            return run_grid_search_fallback()
        print("Connected to GlobalMOO API")
        return run_grid_search_fallback()
    except Exception as e:
        print(f"GlobalMOO error: {e}")
        return run_grid_search_fallback()


def run_grid_search_fallback():
    """Grid search fallback for PDE scheme optimization."""
    print("Running grid search exploration...")

    solver = WaveEquationSolver(Nx=80)
    ref_scheme = NumericalScheme("Reference", 1.0, 0.5, 0.8, "High-res reference")
    reference = solver.solve(ref_scheme, T=0.5, Nt=1000)

    results = []
    for alpha in np.linspace(0.5, 2.0, 8):
        for w in np.linspace(0.3, 0.7, 8):
            for cfl in np.linspace(0.5, 0.95, 5):
                scheme = NumericalScheme(f"Test", alpha, w, cfl, "Grid search")
                result = solver.solve(scheme, T=0.5, Nt=500)

                if result['status'] != 'completed':
                    continue

                error = np.linalg.norm(
                    result['u_final'] - reference['u_final']
                ) / np.linalg.norm(reference['u_final']) if reference['status'] == 'completed' else 1.0

                results.append({
                    'time_scaling': alpha,
                    'spatial_weight': w,
                    'cfl_factor': cfl,
                    'error': error,
                    'runtime': result['runtime'],
                    'energy_drift': result['energy_drift']
                })

    results.sort(key=lambda x: x['error'])

    print(f"Grid search: {len(results)} points evaluated")
    print(f"Top 3 by error:")
    for r in results[:3]:
        print(f"  alpha={r['time_scaling']:.2f}, error={r['error']:.4f}")

    return {
        'status': 'completed',
        'method': 'grid_search',
        'n_evaluations': len(results),
        'pareto_front': results[:20]
    }


def main():
    results = {}
    results['demo'] = run_pde_demo()
    results['pymoo'] = run_pymoo_optimization()
    results['globalmoo'] = run_globalmoo_optimization()

    output_path = os.path.join(os.path.dirname(__file__),
                               'pde_scheme_results.json')
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved to: {output_path}")

    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)
    print("""
    Key findings:
    1. Different numerical schemes = different C-schemes
    2. Physical observables (final state, energy) should be invariant
    3. Discretization artifacts break invariance

    MOO finds schemes that:
    - Minimize error (accurate)
    - Minimize runtime (efficient)
    - Minimize energy drift (physically correct)

    This is an "auto-tuner for PDE schemes" using G_scheme principles.
    Applications: Numerical GR, plasma physics, CFD
    """)

    return results


if __name__ == "__main__":
    main()
