# Exact obstruction for the OLD support dictionary at side 4.61

This is not a packing infeasibility proof and is not a limit on all weighted
measures. It diagnoses a **particular prescribed 356-orbit D4 support dictionary**
under the side-0.99985 closed-core coverage test.

Run, using only Python's standard library:

```bash
python3 verify_obstruction.py verify restricted-dictionary-obstruction.json
```

Expected result:

```text
EXACT_RESTRICTED_DICTIONARY_OBSTRUCTION_VALID orbits 356 poses 106 dual_sum 17009583872717/1000000000000 exceeds_17_by 9583872717/1000000000000
```

Let O_j be the prescribed atom orbits, and let A_ij count how many atoms of O_j
belong to closed core C_i. The certificate gives 106 contained cores and rational
nonnegative dual weights z_i such that

    sum_i z_i A_ij <= |O_j|       for every prescribed orbit j,
    sum_i z_i = 17.009583872717 > 17.

Every nonnegative per-atom weighting w_j that covers these cores must satisfy

    total mass = sum_j |O_j| w_j
               >= sum_i z_i sum_j A_ij w_j
               >= sum_i z_i > 17.

The verifier reconstructs each core from its rational center and rational
half-tangent; proves it is contained in the outer square; recomputes every
closed-core incidence by integer inequalities; and checks every dual inequality
using exact Fractions. No stored floating incidence matrix or LP solver is
trusted. The checker refuses Python's `-O` mode, in which assertions would be
disabled. The separate discovery function uses NumPy and SciPy only to propose
dual multipliers and rounds/scales them before exact verification.

These 106 poses are from the 721-direction subset of the 2881-direction proof
net. Reweighting the old support cannot pass the full net either. A new support,
a different core side, or a stronger direct unit-square verifier is outside the
scope of this obstruction. It is especially NOT an upper bound on s(17).

## Exact deletion test for the final 4.613 certificate

`test_ablation.py` first checks that `../orbit-provenance.json` expands exactly
to the accepted measure. It removes the 19 orbits priced during the 4.613 stage
(indices >=444), leaving mass 16.682320324, and runs the original integer kernel.
The kernel must reject with direction-zero minimum **0.939043209**. Rescaling
the remaining weights to repair that minimum would exceed mass 17.

The standard `../verify.py` runs this experiment using both backends. It can
also be run against an already built checker:

```bash
python3 diagnostic/test_ablation.py .replay/exact_cover_tree \
  --log .replay/ablation-manual.log
```

Run that command from the package root. The retained
`ablation-without-final-priced-orbits.json` is intentionally NOT a valid
packing certificate. The experiment establishes the role of the selected
orbits in this particular core certificate, without claiming that they are
necessary in every reoptimization or every direct unit-square proof.
