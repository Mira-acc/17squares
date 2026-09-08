# What changed, what was tested, and how to extend the result

## Audit of the competing result

Joshua Levy's T-019 certificate, registered 4 September 2026, states s(17)>=4.59.
It has 1184 atoms, total weight 423327/25000 = 16.93308, core side 9977/10000,
and 181 rational directions. Its published minimum is 200009/200000.
The newly written integer checker reproduces that minimum exactly. The full
upstream data have also been checked against the original Git blob hash.

This is not merely a small improvement to the archived Mira result. The
Mira-Cult/17squares README still records 4.450837; Levy's n=17 frontier also
records and reports replaying Mira's later 4.468292 result. The latter should
not be confused with the older certificate actually retained in this repo.

Levy's survey also lists the 4.5705 anabologyco-maker candidate, Massaccesi's
4.5058, Burns' 4.4811, and Fort's 4.456575. The source trail checked here did not
reveal an existing bound above Levy's 4.59. This is a dated literature/source
check, not a guarantee about unpublished work or future priority. The much
older published survey tables can lag the current certificate repositories.

## Their mechanism

The decisive generalization is to replace sixteen indivisible witnesses by a
nonnegative measure of total mass below 17. Every possible unit square must
consume at least one unit of that mass. Disjoint square interiors cannot consume
the same atom twice. More support points are therefore allowed without
sacrificing the counting contradiction.

The weights are found by a covering linear program. A translation/orientation
with insufficient mass gives another LP row. The proposed solution is rounded
to rational data and checked exactly. A shrunken core plus a rational direction
net pays rigorously for angles between the net directions. Their current n=17
record uses this finite-net route, rather than requiring a direct enumeration
of all orientation events.

## Progress made in this calculation

First, the already-published sharper dilation lemma gives the easy corollary
4.5900309898665... from Levy's existing n=17 certificate. This is not claimed
as a new mechanism or as the main advance.

Next, finer angular nets permit larger cores. Uniform scaling and a small
weight adjustment gave an exact 4.596 certificate. Reoptimizing the weights on
the scaled source support gave exact 4.600 and 4.601 certificates. These are
new finite certificates, not consequences of a sampled numerical minimum.

The larger improvement comes from changing the point dictionary itself. A
single uniform dilation moves every near-wall point away from its original wall
clearance. This can remove an important atom from a nearly axis-aligned square.
In the augmented dictionary we retain both choices:

- a uniformly scaled copy of every Levy D4 orbit;
- a copy with its distances to the closest horizontal and vertical walls held
  fixed, while the containing square expands;
- additional strips near coordinates 0.9996 and 1.9992, with several transverse
  positions; and optional D4-symmetrized sites from Mira's earlier certificate.

Weights are reoptimized jointly, not assigned by simply adding the old
measures. The strongest final certificate, its exact parameters, and the
allocation of weight between these families are recorded in best-certificate.json
and result.json. Every final assertion is gated by full integer replay.

The exact 4.605 certificate, for example, allocates mass as follows:

| Family | Positive orbit variables | Mass |
|---|---:|---:|
| Uniformly scaled Levy sites | 72 | 9.53423764 |
| Wall-anchored Levy sites | 67 | 5.73765688 |
| Added near-unit-grid strips | 11 | 1.70768372 |
| Mira's sixteen old sites, symmetrized | 0 | 0 |
| Total | 150 | 16.97957824 |

A separate exact 4.603 certificate does use one of the Mira-derived orbit
variables, contributing mass 0.01087376. Thus the literal point-set union can
participate in a valid stronger certificate, but it was not needed in the
stronger 4.605 result. We do not attribute its numerical improvement to old
points that received zero weight.


## Final 4.607 record and ablation

The final, independently replayed certificate reaches **4.607**, using 1200
atoms, 2881 directions and total mass 16.98264408. Its minimum net-core mass
is exactly 1.00000116. Uniform dilation gives the stronger radical endpoint
and strict decimal in result.json.

| Family | Positive orbit variables | Mass |
|---|---:|---:|
| Uniformly scaled Levy sites | 77 | 9.26740384 |
| Wall-anchored Levy sites | 68 | 6.15802400 |
| Added near-unit-grid strips | 12 | 1.52282656 |
| Mira's old point #10, D4-symmetrized | 1 | 0.03438968 |
| Total | 158 | 16.98264408 |

The retained Mira point is (1.494140, 2.660211) in the old 4.450837 container.
Its transformed D4 orbit has eight atoms of weight 0.00429871 each. In an exact
ablation with those eight weights removed, the direction-0 closed-core
minimum is 0.99140418, below 1. The remaining total mass is 16.9482544;
uniformly rescaling it to repair that minimum would exceed mass 17. Thus the
legacy orbit is not just a zero-weight decorative inclusion in the final
certificate. This proves its role in THIS certificate, not that every possible
4.607 certificate must use it, or that the ablated measure cannot be proved
useful by a different core/verification argument.

The 4.608 run did not yield a certificate. With the tested dictionary and core,
its finite-row numerical optimization returned mass about 17.0075885. No
packing or method-wide obstruction is inferred from that failed trial.

## Negative and inconclusive experiments

At L=4.600 with the coarser 721-direction net and core side 0.9994, reweighting
only the uniformly scaled source support produced a numerical feasible measure
of mass approximately 17.0084: not below 17, so not a certificate. A finer net
removed that obstacle. It would have been wrong to stop at the sampled value
or count a weight total above 17 as a proof.

A straightforward union with the old Mira points did not certify 4.605 in the
trial run. The boundary-anchored and strip additions were materially more
useful. Larger-side runs and their finite-LP objectives are exploratory only;
an objective above 17 for a chosen point dictionary does not rule out a better
dictionary, a stronger geometric verifier, or a packing-specific argument.

## The useful merger with the earlier proof infrastructure

Mira's archived proof checks boxes in the full three-dimensional pose space and
closes a box when an unavoidable-point statement has been certified. The
natural weighted extension is to certify a LOWER BOUND on captured mass in
each box. In the simplest version, sum the weights of atoms guaranteed to lie
strictly inside every square in that box, and close when the sum is at least 1.

Disjunctive certificates must be handled carefully: if a geometric lemma only
says that at least one point of a set S is captured, its direct weighted payoff
is min_{j in S} w_j, NOT sum_{j in S} w_j. More elaborate leaves can certify the
minimum total weight across their admissible capture patterns. Any merger must
retain strict interior information; points on boundaries may be shared by
touching squares.

A weighted, full-orientation pose-space checker could reduce or remove the
uniform angular-core loss. That extension was not implemented here. The new
proof kind is added alongside the existing certificate archive, with a new
integer event-sweep kernel. The old verifiers and old proof files are not
silently changed or relabeled as proving the new result.

## Improving the search without weakening the proof

The discovery code remains deliberately untrusted. Two practical changes make
continued searches less wasteful:

1. Retain all discovered LP rows in a pool, but solve a small working set.
   Every candidate LP solution is checked against the FULL saved row pool;
   omitted violated rows are restored. Merely forgetting inactive rows can
   lead to cycling, which was observed in an earlier exploratory version.
2. In the floating-point sweep, defer constructing O(N)-length capture profiles
   until after finding representative low-mass slabs. Retain the global minimum
   and representatives across u buckets. This reduces discovery overhead;
   it does not change the separate exact verifier or replace full replay.

A small deterministic objective perturbation reduces jumping between different
vertices of a flat LP optimum. Available total-mass slack can also be used to
rescale a nearly feasible numerical measure before rationalization. Neither
operation is trusted as a proof: the resulting exact atoms must pass the full
integer sweep again.

## Keeping a durable frontier

The maintainable object is an immutable certificate, a proved lower-bound
formula, its exact replay logs, and a dated provenance record. The supplied CI
workflow rebuilds the arithmetic checker and rejects proof regressions or
metadata mismatches. Optimizers, competitor announcements, and decimal claims
are discovery inputs, not trusted updates to the theorem.

No process can promise permanent priority over unknown future work. The
operational goal is to make a newly discovered improvement cheap to verify,
attribute, integrate and then improve further. This package was produced and
checked in the present session; no monitoring or future computation is claimed
to be running after delivery.

## References

- Joshua Levy, n=17 frontier: https://github.com/jlevy/squares/blob/main/packing/frontier/n-017.md
- Levy's T-019 data: https://github.com/jlevy/squares/tree/main/packing/cases/n17_fractional_certificate
- Covering-LP generator: https://github.com/jlevy/squares/blob/main/packing/src/sqpack/fractional/generate.py
- T-022 dilation lemma: https://github.com/jlevy/squares/blob/main/packing/cases/n11_fractional_certificate/t-022-dilation-limit-proof.md
- Mira's archived repository: https://github.com/Mira-Cult/17squares
- Sam Burns' weighted certificate: https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/
- Gustavo Massaccesi's LP improvement: https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html
