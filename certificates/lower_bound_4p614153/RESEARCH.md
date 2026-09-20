# Research notes: from R012 to 4.614153538384596

This note records the search path behind the current theorem without promoting
numerical trials into proofs.

## 1. R012 audit

Guzhou0806's R012 certificate at pinned commit
`931a0dfd64302e277057006e99388fe5c00b7f53` was reconstructed and replayed.
Its parent-domain reduction is sound: for a parent half-angle interval `[a,b]`,
the legal parent-center squares are nested, and the exact union is determined by
the smaller endpoint width. The selected concentric core is proved strictly
inside every parent in the whole interval, then coverage is checked over that
entire two-dimensional legal-center envelope.

The global counting step is also sound. Each hypothetical parent chooses one
closed core strictly inside its interior. Pairwise interior-disjoint parents
therefore have pairwise disjoint selected cores, so their masses can be summed
against the one common nonnegative measure.

R012 proves
$
s(17) > \frac{461300}{99999}=4.6130461304613046\ldots
$
(the source conservatively states a weak inequality; compactness makes the
endpoint exclusion strict).

## 2. Why parent awareness matters

The earlier all-core verifier required coverage at centers where an auxiliary
core fits even if its larger parent cannot fit. An exact retained ablation finds
one such recipe whose minimum mass is only 0.985238 on the all-core domain but
1.000288 on the complete legal-parent envelope. The former deficit is irrelevant
to the packing problem.

This is the conceptual value of R012: it removes a real verifier overconstraint,
not merely a few decimal digits of angular discretization.

## 3. Fixed-measure continuation

Keeping R012's 1,616-atom measure unchanged, adaptive parent-angle subdivision
and near-maximal safe rational cores were reported to reach
$
s(17) > \frac{922600}{199979}=4.613484415863665\ldots .
$

That intermediate catalogue is not retained in this package and is not part of
its replayed theorem. The same frozen measure cannot be pushed indefinitely by better core selection.
At parent side `A=99989/100000`, an exact legal parent has total closed-parent
mass only `998982/1000000`, below the common charge ratio required by the
measure. Since an inner core cannot contain more of a nonnegative measure than
its parent, this gives a support-independent obstruction for that fixed measure
under the same counting rule.

This is a limitation of the frozen measure, not an upper bound on `s(17)`.

## 4. Reweighting and support movement

The next stage fed exact low-mass parent placements back into a covering LP.
Numerical optimization was used only for discovery; every retained theorem was
rounded to rational data and replayed from scratch by the exact checker.

Reweighting the inherited support passed the fixed-measure obstruction. A second
stage added wall-adjusted copies of useful support points while retaining older
locations, allowing the optimizer to trade between wall-relative and interior
coverage.

The final accepted target is parent side
$
A=\frac{3999}{4000},
$
with outer side `L=4613/1000`, giving
$
\frac{L}{A}=\frac{18452}{3999}=4.61415353838459614903\ldots .
$

The final exact data contain 3,280 atoms in 417 D4 orbits and 4,391 parent-angle
intervals. Total mass is 16.999991644; minimum selected-core mass is
1.000000030; the exact counting surplus is 0.000008866.

## 5. Verification and failed higher trials

The complete exact C++ replay checks 27,918,671 center slabs. Segment-tree and
direct-prefix accumulation agree interval by interval, although they share the
same geometric partition and are not independent geometric proofs. The pinned
R012 catalogue is also replayed in full.

Higher numerical trials were explored but are not theorem claims. In particular,
failure of a particular dictionary or optimizer run is not treated as a ceiling
on the parent-aware method.

## 6. Next directions

The strongest immediate extensions are:

1. combine parent-aware transport with richer charging rules such as Levy's
   threshold atoms;
2. continue dual-guided support generation using exact parent counterexamples;
3. use compatibility information between possible square poses, rather than
   only one-square covering constraints;
4. connect the global lower-bound machinery with the repository's local analysis
   of Bidwell's construction.

No global optimality proof is claimed by the present certificate.
