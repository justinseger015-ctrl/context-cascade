# Simulation Upgrade Plan v2.0

## Overview

Based on critical analysis from a mathematical physics perspective, we're upgrading all 6 scheme-invariance simulations to:
1. Stress test with harder cases
2. Add missing physics (esp. chiral anomaly)
3. Include convergence/scaling analysis
4. Preserve the evolution story (v1 -> v2)

---

## 1. QFT Renormalization Schemes

### Current State (v1)
- Schemes: MS-bar, On-shell, MOM
- 900 MOO evaluations
- Best invariance penalty: 0.0
- Uses proxy for higher-loop

### Upgrades for v2

**A. Harder Kinematics**
- Expand from single (s,t,u) point to grid of 20+ kinematic configurations
- Include threshold regions (s ~ 4m^2) where scheme differences are largest
- Test both timelike and spacelike momentum transfers

**B. Real 2-Loop Terms**
- Replace `higher_loop = |lambda|^2 * loop_factor` proxy with actual 2-loop beta function contribution
- Add scheme-dependent finite parts: delta_finite(MS-bar) != delta_finite(on-shell)
- Compute running coupling evolution across schemes

**C. Exotic Schemes**
- Add non-minimal subtraction schemes (with polynomial finite parts)
- Test pathological schemes that SHOULD fail invariance
- Verify MOO correctly flags them with high invariance penalty

### Success Criteria
- Invariance penalty remains ~0 for physical schemes across all kinematics
- Pathological schemes get flagged with penalty > 0.1
- 2-loop contributions don't break invariance

---

## 2. Kramers-Wannier Duality (2D Ising)

### Current State (v1)
- L = 16 lattice
- K_c found to 1e-11 precision
- Free energy difference at K_c: 0.0029

### Upgrades for v2

**A. Larger Lattice / Transfer Matrix**
- Increase to L = 32, 64, 128 (or use transfer matrix for L -> infinity)
- Drive free energy difference at K_c toward machine precision
- Show finite-size scaling: diff ~ L^(-alpha)

**B. Correlation Length Exponent**
- Compute correlation length xi on both sides of duality
- Verify xi(K) = xi(K*) within numerical error
- Extract nu exponent and compare to exact value (nu = 1)

**C. Duality with External Field**
- Add magnetic field h
- Show where invariance breaks (h != 0 generally breaks self-duality)
- Map out the phase diagram in (K, h) space

### Success Criteria
- Free energy diff at K_c < 1e-6 for large L
- Correlation exponent matches on both sides
- External field correctly breaks duality (documented)

---

## 3. Chiral Anomaly Detection

### Current State (v1) - KEEP AS FALSE-NEGATIVE EXAMPLE
- Naive lattice Dirac operator
- B = 0: No obstruction (correct)
- B != 0: Phase ~ 1e-14 (FALSE NEGATIVE - should see anomaly!)
- Demonstrates: framework is honest, scheme space needs expansion

### Upgrades for v2

**A. Wilson Fermions**
- Implement Wilson term: D_W = D_naive + (r/2a) * Laplacian
- This explicitly breaks chiral symmetry at finite a
- Jacobian should now show non-trivial structure

**B. Overlap/Domain-Wall Style**
- Implement sign function of Wilson operator: D_ov = 1 + gamma5 * sign(H_W)
- This has exact chiral symmetry at finite a
- Anomaly appears as topology of gauge field

**C. Fujikawa Mode Counting**
- Implement mode truncation: keep N lowest eigenmodes
- Compute Tr(gamma5) in truncated space
- Should approach (1/2pi) * integral(F) as N -> infinity

**D. Version Comparison**
- Keep v1 results as "initial_naive" in JSON
- Add v2 results as "wilson_fermions" and "fujikawa"
- Document the evolution: false-negative -> correct detection

### Success Criteria
- Wilson: Jacobian phase scales with B (expected: phase ~ B * area)
- Fujikawa: Trace approaches topological charge
- Clear documentation of v1 -> v2 evolution

---

## 4. PDE Numerical Schemes (Wave Equation)

### Current State (v1)
- 5 schemes tested
- 4/5 invariant, 1 (weighted spatial) flagged
- Energy drift: 0.10 - 0.21

### Upgrades for v2

**A. Convergence Analysis**
- Run each scheme at dx = 0.1, 0.05, 0.025, 0.0125
- Measure invariance_diff(dx) for scheme pairs
- Fit to diff ~ dx^p to extract convergence order

**B. Energy Conservation Scaling**
- Track energy_drift(dx) for each scheme
- Good schemes: drift -> 0 as dx -> 0
- Bad schemes: drift stays O(1) or grows

**C. Nonlinear Extension (Burgers' Equation)**
- u_t + u * u_x = nu * u_xx
- Test same scheme families
- See if invariance tests correlate with shock formation quality

**D. Numerical GR Preview**
- Add note about ADM vs BSSN vs generalized harmonic
- Sketch how this framework extends to constraint propagation

### Success Criteria
- Good schemes: diff ~ dx^2 (second order convergence)
- Bad schemes: diff ~ dx^0 or worse
- Burgers: invariance predicts shock quality

---

## 5. Quantum State Geometry

### Current State (v1)
- 30 random pure states, dim = 4
- FS vs Bures comparison
- 92.6% clustering agreement
- Best MOO: 99.9% agreement at epsilon = 0.01

### Upgrades for v2

**A. Entangled Bipartite States**
- Generate 50 random 2-qubit states (dim = 4 = 2 x 2)
- Vary entanglement from separable to maximally entangled
- Check if entanglement structure (Schmidt rank, entropy) is scheme-robust

**B. Mixed States**
- Extend from pure states to density matrices
- FS not defined for mixed states; use Bures + Hilbert-Schmidt
- Test if purity-based clustering is robust

**C. Complexity Metric (Nielsen-type)**
- Approximate geodesic distance under right-invariant metric
- Compare FS vs Bures vs Complexity
- See if key structures (clusters, diffusion embeddings) remain invariant

**D. Higher Dimensions**
- Test dim = 8 (3 qubits) to see if agreement degrades
- Finite-size scaling of spectral gap

### Success Criteria
- Entanglement structure preserved across metrics
- Mixed state extension maintains >90% agreement
- Complexity metric doesn't break established patterns

---

## 6. Wheeler-DeWitt Factor Ordering

### Current State (v1)
- Ordering parameter p in [-1, 3]
- p = 1 (Laplace-Beltrami) identified as optimal
- WKB semiclassical: scheme-robust

### Upgrades for v2

**A. Add Potentials**
- Cosmological constant: V(a) = Lambda * a^3
- Scalar field potential: V(a, phi) = m^2 * phi^2 * a^3
- Check if p = 1 remains optimal with potentials

**B. Different Clock Variables**
- Current: use scale factor a as time
- Alternative: use scalar field phi as clock
- Verify scheme-robust observables consistent across clock choice

**C. Quantum Corrections**
- Add O(hbar) corrections to WKB
- See if ordering-dependence appears at higher orders
- Map out where classical scheme-robustness breaks down

**D. Bouncing Cosmology**
- Test with bounce potential (a_min > 0)
- See if bounce properties are ordering-invariant

### Success Criteria
- p = 1 remains special with potentials
- Different clocks give consistent semiclassical predictions
- Quantum corrections properly tracked

---

## Implementation Order

1. **Chiral Anomaly** - Most impactful upgrade (false-negative -> detection)
2. **PDE Schemes** - Straightforward convergence analysis
3. **Kramers-Wannier** - Larger lattice + correlation exponent
4. **QFT Renormalization** - Harder kinematics + 2-loop
5. **Quantum Geometry** - Entangled states
6. **Wheeler-DeWitt** - Add potentials

---

## Data Structure for Evolution Tracking

Each simulation JSON will have:

```json
{
  "v1_initial": {
    "description": "Original implementation",
    "results": { ... },
    "limitations": "..."
  },
  "v2_upgraded": {
    "description": "After critical review upgrades",
    "changes": ["...", "..."],
    "results": { ... }
  },
  "evolution_story": {
    "what_changed": "...",
    "why_it_matters": "...",
    "lessons_learned": "..."
  }
}
```

This preserves the scientific narrative of improvement.
