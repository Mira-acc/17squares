# Archived 4.61 milestone report

This report is preserved from the intermediate package. Paths mentioned below
are relative to that original package; its certificate and result are retained
in this history directory with a `4p61-` prefix. The current headline is in
`../result.json`.

# Further improvement by pricing previously unused spatial information

## Outcome

The completed exact certificate proves **s(17)>4.610028617263**. Its base side is
4.61 and its weak radical endpoint is given in `result.json`. This improves the
preceding strict decimal 4.607028598640 by **0.003000018623**. The main gain is
0.003 in the certified container side, not a change in displayed precision.

| Quantity | Previous certificate | This certificate |
|---|---:|---:|
| Base containing side | 4.607 | 4.61 |
| Core side | 0.99985 | 0.99985 |
| Rational directions | 2881 | 2881 |
| Atoms | 1200 | 1672 |
| Positive orbit variables | 158 | 214 |
| Total mass | 16.98264408 | 16.995831388 |
| Least exact net-core mass | 1.00000116 | 1.000002015 |
| Exact center slabs | 6679269 | 9368005 |

The C++ exact kernel is byte-identical to the preceding package. Both
accumulation backends accepted the new data; their complete per-direction logs
agree. This is not an independently authored second geometric proof.

## 1. What information was being left unused?

The previous search primarily asked which weights to put on a chosen set of
point locations. It repeatedly added under-covered core placements to a covering
LP, but a location outside the allowed support could never receive weight.

The LP contains more information: dual multipliers identify the combination of
core placements that is currently expensive to cover. They can guide the
placement of NEW atoms rather than merely the reweighting of old atoms.

For an orbit O_j and retained core C_i, put A_ij=|O_j intersect C_i|. The primal
and dual are

    minimize sum_j |O_j| w_j    with A w >= 1, w >= 0;
    maximize sum_i z_i         with A^T z <= (|O_j|)_j, z >= 0.

For a proposed new orbit O(p), define its normalized price

    rho(p) = [sum_i z_i |O(p) intersect C_i|] / |O(p)|.

A score above one means the old dual would violate the new orbit constraint.
It therefore identifies a promising column, not a guaranteed amount of progress
in the full continuum problem. A previously omitted core may still constrain it.
Column generation and LP duality are standard; the new work here is their
specific implementation and the checked certificate they produced.

## 2. Spatial pricing and row separation

The new numerical tool symmetrizes the dual-weighted cores under D4, scans
horizontal lines, and uses a weighted interval sweep to find valuable locations
on each line. It refines lines near large scores, rounds candidate coordinates
to eight decimal places, adds orbits, and resolves the covering LP.

It then sweeps translations at the direction net again. Newly under-covered
cores become new rows. All discovered finite rows remain in a retained pool;
a working-set solver must restore omitted violated rows before accepting an LP
iterate. Points are not added without checking the new coverage deficiencies
that can appear when the optimum shifts.

The scan over possible new points is heuristic. It does NOT prove there are no
better locations left. Both row and column discovery use floating point and are
outside the trusted proof kernel.

## 3. An exact reason reweighting alone cannot reach this result

The augmented old dictionary has 356 distinct D4 orbits after deduplication at
L=4.61. We extracted 106 actual core placements and rational dual weights for it.
The exact diagnostic independently checks core containment, closed membership,
and all dual inequalities. Their sum is

    17009583872717 / 1000000000000 = 17.009583872717.

Thus no nonnegative D4 weighting of those prescribed locations can cover even
those 106 side-0.99985 cores with mass at most 17. This also blocks the complete
2881-direction core test for that dictionary.

This is a useful obstruction with a carefully limited scope. It does not rule
out better points, other core sizes, a direct full-orientation argument, or any
larger lower bound. Nor is it a statement that a packing exists at 4.61.
See `diagnostic/README.md` for the complete short dual proof.

## 4. The successful support really uses new sites

Of the 214 positive orbit variables in the final certificate:

| Family | Orbits | Atoms | Exact mass |
|---|---:|---:|---:|
| Sites available in the old augmented dictionary | 180 | 1400 | 15.400351732 |
| Newly dual-priced sites | 34 | 272 | 1.595479656 |
| Total | 214 | 1672 | 16.995831388 |

Orbit indices below 356 refer to the old dictionary in this run; indices at
least 356 are newly priced additions. `orbit-provenance.json` gives their exact
coordinates and weights.

Examples of new canonical representatives and their total eight-point orbit
masses are:

| Representative (x,y) | Orbit mass |
|---|---:|
| (0.99984877, 1.77046127) | 0.364977304 |
| (0.98110384, 1.99943613) | 0.336986784 |
| (0.99981519, 1.76316473) | 0.231456800 |
| (0.50482008, 0.99978501) | 0.137780440 |

The near-unit-distance structure suggested by the earlier wall/strip search
persists, but the useful transverse coordinates are not restricted to a coarse
grid. This is an observed feature of the new certificate, not a proof that all
optimal measures must have this form.

## 5. Positive-only repair made the final step work

Reoptimizing every weight can fix one deficient placement by reducing weights
that were covering another. Near a flat LP optimum, this creates slow exchanges
between different weak placements.

Instead, at a nearly feasible iterate we held its existing weights w fixed and
solved for additions delta >= 0:

    minimize sum_j |O_j| delta_j,
    A_bad delta >= 1.000002 - A_bad w.

For every core, known or unknown, its mass cannot decrease under this update.
The separation sweep is still necessary because there can be previously unseen
deficits; positivity merely prevents the repair itself from creating new ones.

The retained numerical run started with mass 16.983804422676073 and full-net
minimum 0.9955395601215482. One repair added mass 0.01202611387371233. The next
full sweep found minimum 1.00000199998335 at mass 16.995830536549782. A tiny
normalization and upward rounding of weights to denominator 10^9 gave the
immutable exact certificate. Its integer replay, not these decimals, proves
mass 16.995831388 and minimum 1.000002015.

## 6. What was not done

The weighted three-dimensional continuous-orientation pose-space verifier
suggested in the preceding report remains unimplemented. The present gain was
obtained without changing the exact angular argument. The same B=0.99985 and
m=2880 are used in both the old and new record, so this is not a finer-net gain.

The work does not prove optimality of the measure or of the best known packing.
Spatial pricing is incomplete over the continuum of possible sites. A finite LP
above mass 17 for one dictionary cannot be called a method-wide ceiling.
External independent geometric/code review remains pending.

## Sources and attribution

The original support comes from Joshua Levy's T-019 fractional certificate,
combined in the previous 4.607 work with anchored copies, strip locations, and
Mira's old witness points. Burns and Massaccesi precede this work's use of
weighted certificates. Levy's T-022 supplies the dilation corollary. The current
source check read `jlevy/squares/packing/frontier/n-017.md`, blob
`c9fe497e264a9613866cf8e24b0cea2bb1a64f81`, still recording 4.59. This is a dated
source observation, not a guarantee about unpublished or future work.
See `ATTRIBUTION.md` for source paths, hashes, and licensing.
