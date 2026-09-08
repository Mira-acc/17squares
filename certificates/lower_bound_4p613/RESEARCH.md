# Pricing unused spatial information: from 4.607 to 4.613

## Exact outcome

The final result is

    s(17) > 4.613028635886.

The certificate directly excludes side 4.613; the existing dilation corollary
supplies the remaining digits. The weak radical endpoint is

    4.61302863588611076617205655840261924140098182197751... .

The previous delivered strict bound was 4.607028598640, so the strict displayed
improvement is **0.006000037246**. The actual base-side improvement is **0.006**.

| Quantity | Previous package | First new milestone | Final certificate |
|---|---:|---:|---:|
| Base containing side | 4.607 | 4.61 | 4.613 |
| Core side | 0.99985 | 0.99985 | 0.99985 |
| Rational directions | 2881 | 2881 | 2881 |
| Atoms | 1200 | 1672 | 1620 |
| Positive orbit variables | 158 | 214 | 206 |
| Total mass | 16.98264408 | 16.995831388 | 16.99798498 |
| Least exact core mass | 1.00000116 | 1.000002015 | 1.000002103 |
| Exact center slabs | 6679269 | 9368005 | 9116871 |

All new claims rest on complete integer replay. Both accumulation backends
accepted each new certificate and agree on every printed direction value. The
geometric kernel is byte-identical to the preceding package, with SHA-256
`1bb626a560e3c67620b2aa7851bc467db72b3530f6cae394c1d9d9f034910f4b`.
Their shared geometric partition is explicitly part of the trust boundary.

## 1. The unused information was not another decimal of angular accuracy

The earlier optimizer mainly varied weights at prescribed locations, adding bad
core placements to a covering LP. It could not put weight at a better location
outside that dictionary.

The same LP also supplies dual multipliers: a weighted collection of placements
that is difficult to cover with the available sites. Those multipliers tell us
where to put NEW atoms that serve several difficult placements efficiently.

For a D4 orbit O_j and core C_i, let A_ij=|O_j intersect C_i|. The primal and dual
are

    minimize sum_j |O_j| w_j    with A w >= 1, w >= 0;
    maximize sum_i z_i         with A^T z <= (|O_j|)_j, z >= 0.

For a proposed new orbit O(p), the normalized price is

    rho(p) = [sum_i z_i |O(p) intersect C_i|] / |O(p)|.

A price above one would violate the old dual's constraint for this new orbit.
It identifies a promising column, not a guaranteed gain in the full continuum
problem. Previously omitted cores may still constrain it.

LP duality and column generation are standard optimization ideas. The new
contribution is their implementation for this geometry, the exact diagnostic,
and the stronger rational certificates—not invention of those general ideas.

## 2. Spatial column generation is interleaved with geometric row generation

The numerical pricing tool averages the dual-weighted cores under D4, scans
horizontal lines, and uses weighted interval sweeps to find high-value locations.
It refines lines near large scores and adds rational-rounded point orbits.

After reoptimization, a full translation sweep searches for under-covered cores.
Those become new rows. The full finite row pool is retained; an LP working set
must restore omitted violated rows before its numerical solution is accepted.
The improved continuation also avoids adding columns with identical profiles
on the current dual support and uses a small deterministic objective perturbation.

This is not a globally exhaustive search over all possible sites. Both pricing
and separation discovery use floating arithmetic and remain untrusted. The
final atoms are checked afresh by the unchanged exact geometric kernel.

## 3. An exact obstruction shows why new sites were necessary at 4.61

At L=4.61, deduplication leaves 356 orbits in the old augmented dictionary. We
extracted 106 contained rational cores and exact rational dual weights z_i with

    sum_i z_i A_ij <= |O_j|     for every old orbit j,
    sum_i z_i = 17.009583872717 > 17.

Consequently any nonnegative D4 weighting of those old sites that covers even
those 106 cores has total mass at least 17.009583872717. Reweighting alone cannot
pass the previous core test at 4.61.

The diagnostic checker independently recomputes core containment and every
closed membership using integers, then checks every dual inequality using exact
Fractions. The finite floating LP and its stored incidence matrix are not trusted.
The 106 directions belong to the 721-direction subset of the 2881-direction net.

This obstruction is deliberately narrow. It does not rule out different sites,
a different core side, a direct full-orientation verifier, or any larger lower
bound. It is not a packing construction or an upper bound on s(17).
See `diagnostic/README.md` for the short dual proof and replay command.

## 4. The first successful repair gave an exact 4.61 certificate

At a nearly feasible iterate, unconstrained reoptimization could fix one weak
placement by removing weights needed elsewhere. We instead held its weights w
fixed and solved for additions delta >= 0:

    minimize sum_j |O_j| delta_j,
    A_bad delta >= 1.000002 - A_bad w.

Every core's mass can only increase during this repair, including cores not yet
seen by the search. A global separation sweep is still required to find any
remaining pre-existing deficits.

The saved 4.61 iterate had mass 16.983804422676073 and full-net minimum
0.9955395601215482. One positive repair added mass 0.01202611387371233. The next
full sweep found minimum 1.00000199998335; tiny normalization and upward rational
rounding yielded the independently replayed mass 16.995831388 and minimum
1.000002015.

That certificate gives 34 newly priced orbits mass 1.595479656. Its complete
report is retained as `history/4p61-RESEARCH.md`, with data and exact replay logs.
Those counts belong to the 4.61 milestone, not the final certificate.

## 5. Geometry from a higher unsuccessful target improved the final result

We then searched at 4.615, retaining both scaled and wall-anchored descendants
of the positive support, and continued spatial pricing. No 4.615 certificate
was obtained. Some finite LP objectives fell below 17, but under-covered cores
remained; such an objective is not a lower-bound proof.

The trial was nevertheless useful: some of its support geometry was reused at
4.613. After further row-and-column generation at that side, the search was
moved to the full 2881-direction net. All the saved finite rows remained in the
working problem. The full-net continuation completed at iteration 11.

The final numerical iterate had mass 16.99334752164479 and full-net minimum
0.9997292238416635. Uniform normalization to target minimum 1.000002 raised the
mass to 16.99798415718938, still below 17. Upward rounding to denominator 10^9
produced exact mass 16.99798498. The exact replay found minimum 1.000002103.

The final 4.613 step therefore used further support optimization and uniform
normalization. It did NOT require another successful positive-only repair LP.
Two earlier positive-only repairs at 4.613 exceeded the budget and are retained
as unsuccessful numerical trials, not evidence against this later certificate.

## 6. The final additional orbits have a directly tested role

The final search dictionary had 604 candidate orbits. Of these, 206 receive
positive rational weight in the accepted certificate:

| Family within the 4.613 search | Positive orbits | Atoms | Exact mass |
|---|---:|---:|---:|
| Inherited, transformed higher-target seed (indices <444) | 187 | 1468 | 16.682320324 |
| Orbits newly priced during the 4.613 stage (indices >=444) | 19 | 152 | 0.315664656 |
| Total | 206 | 1620 | 16.997984980 |

The inherited family already contains newly priced sites from earlier stages;
it must not be relabeled as the original fixed Levy/Mira dictionary.

Deleting the 19 final-stage priced orbits, without reoptimizing the other
weights, leaves mass 16.682320324. Exact replay then rejects the measure at
direction zero, where the minimum core mass is **0.939043209**. A uniform increase
of the remaining weights sufficient to repair that core minimum would require
mass 16.682320324/0.939043209, which is greater than 17.

Thus the new sites are not decorative in the final proof. This is a statement
about THIS certificate and the specified core test. It does not rule out a
different reoptimization without those sites, nor a direct unit-square proof for
the deleted measure.

The largest final-stage priced orbit masses include 0.072485608 at representative
(1.74817256,1.95722173), 0.065192872 at (1.68270006,1.88524177), and 0.05378176 at
(0.99968966,0.99976956). These examples show that pricing selected both near-unit
strip sites and interior sites. Their exact rational data, not the examples,
are authoritative in `orbit-provenance.json`.

## 7. Other tests and remaining scope

A finite-LP interior-point choice inside a mass-budget slice was also tried at
4.613. It satisfied the stored rows but had full-net minimum about 0.9684. It was
not used in either exact result. Extra grid sites and a persistent-LP experiment
were also explored without producing a separate certificate; no theorem is
inferred from interrupted or unsuccessful optimizations.

The full weighted three-dimensional continuous-orientation pose-space verifier
suggested earlier is still unimplemented. These gains use the SAME B=0.99985,
SAME direction net and SAME exact kernel as the 4.607 certificate. They come from
better use of spatial and LP-dual information, not a finer angular allowance.

No global optimality or permanent priority is claimed. The source check read
`jlevy/squares/packing/frontier/n-017.md`, blob
`c9fe497e264a9613866cf8e24b0cea2bb1a64f81`, still recording 4.59. That is a dated
source observation, not a guarantee about unpublished or future work. External
independent geometric and code review of these certificates remains pending.

See `ATTRIBUTION.md` for Burns, Massaccesi, Levy, the previous Mira certificate,
source paths, hashes, licensing and the inherited dilation lemma.
