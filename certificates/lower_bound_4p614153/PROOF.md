# Parent-aware weighted certificates: proof and exact replay

This supplement proves the strict lower bound recorded in the exact JSON payload stored in `certificate.json`
and `result.json`. The outer square always has side L = 4613/1000. The
certificate gives a rational parent side A, a finite nonnegative atomic measure,
and an interval catalogue. Its conclusion is **s(17) > L/A**. It does not assert
that Bidwell is optimal or that the measure method can approach that optimum.

## 1. Certificate contract

An orbit row `(x,y,w)` has position `(x/100000,y/100000)`, weight
`w/weight_denominator`, and all distinct D4 images in `[0,L]^2` with that weight.
The loader rejects overlapping orbit rows, negative weights, noninteger rows,
incorrect mass, or a different outer square. Let M be the expanded total mass.

Each catalogue row `(a,b,t,B)` consists of rational half-angle endpoints, a
rational core half-angle, and a rational positive core side. Consecutive closed
intervals meet exactly, starting at zero and ending at T with
`T*T + 2*T > 1`, so they cover half-angles through `tan(pi/8)`.

The theorem follows if every row selects a strictly interior concentric core
for every parent in that row's angle interval; every such core, at every legal
parent center, has mass at least gamma; and `17*gamma > M`.

Neither the historical output logs nor a numerical optimizer are premises.
`verify.py` reconstructs every geometric job, compiles the exact kernel, and
requires every catalogue obligation to be replayed before reporting success.

## 2. Rational angles and strict core containment

For a half-angle parameter u in `[0,1)`, set

    c(u) = (1-u*u)/(1+u*u),   s(u) = 2*u/(1+u*u).

These are exact rational unit-vector coordinates for angle `2 atan(u)`.
For a row `(a,b,t,B)`, define

    g(t,u) = c(t)c(u) + s(t)s(u) + |s(t)c(u) - c(t)s(u)|.

The verifier checks a positive dot product and `dot >= abs(cross)` at each
endpoint. Thus the endpoint relative angles are at most pi/4. The maximum
absolute angular difference from the fixed core direction occurs at an endpoint,
and `cos(delta)+sin(abs(delta))` increases with `abs(delta)` on this range.
Therefore the exact rational inequality

    B * max(g(t,a),g(t,b)) < A

proves strict containment for the entire interval. This is not interpolation
between sampled successful poses. All core boundary points lie inside the
parent's interior, including at angle-interval seams and parent-wall contacts.

## 3. Exact parent-center envelope

An A-square at half-angle u has coordinate half-extent `A*f(u)/2`, where

    f(u) = c(u)+s(u) = (1+2u-u*u)/(1+u*u).

Its legal centers form `[A*f(u)/2, L-A*f(u)/2]^2`. Since

    f'(u) = 2*(1-2u-u*u)/(1+u*u)^2,

f has one interior maximum and no interior minimum on `[0,1)`. The center
squares are nested, so their union over the closed interval `[a,b]` is exactly

    D = [r,L-r]^2,   r = A*min(f(a),f(b))/2.

Every point of D is a legal center for the endpoint having the smaller f.
There are no omitted parent centers. The verifier additionally checks
`B*(c(t)+s(t))/2 <= r < L/2`, giving contained cores and a positive-area domain.

The old all-core domain `[B*(c(t)+s(t))/2, L-B*(c(t)+s(t))/2]^2` can be strictly
larger. A deficient core centered in that difference is not a counterexample to
this parent-aware condition. The retained ablation is an explicit example.

## 4. Exact sweep over all translations

Translate the domain center to the origin and put `d=L/2-r`. At core direction
`(c,s)`, rotate center coordinates to

    u=c*x+s*y,   v=-s*x+c*y.

A spatial atom p is captured by a **closed** B-core precisely when `(u,v)` lies
in its closed axis-aligned capture rectangle

    [u_p-B/2,u_p+B/2] x [v_p-B/2,v_p+B/2].

The center domain is the rotated square

    |c*u-s*v| <= d,   |s*u+c*v| <= d.

The vertical capture-rectangle events split it into open u-slabs. Inside each
slab the active capture rectangles are fixed; horizontal rectangle events then
split v into cells of constant mass.

For `s>0`, the domain's lower and upper boundaries are

    lower(u) = max((c*u-d)/s, (-d-s*u)/c),
    upper(u) = min((c*u+d)/s, ( d-s*u)/c).

The convex lower boundary has its minimum at `u=d*(c-s)`; the concave upper
boundary has its maximum at `u=-d*(c-s)`. On a closed slab `[a,b]`, their extrema
are therefore found by clamping those vertices to `[a,b]`. The axis case `s=0`
is handled separately.

This implementation does not need to insert internal polygon vertices as
additional events: the clamped-extremum computation accounts for a vertex inside
a slab. In contrast, the retained R012 Python implementation inserts the polygon
vertices and evaluates each piece's endpoints. Both compute the projection of the
**whole slab**, not a midpoint cross-section.

The intersection of a slab and the domain is convex; its v-projection is an
interval. Every horizontal open cell having positive-length intersection with
that projection is reachable with positive area and must be tested. Exact
binary searches determine this complete query range. A segment tree computes its
minimum integer mass. The alternate build uses a direct prefix accumulator on
the same geometric partition.

For each angle row, the kernel also reconstructs a rational interior point of a
minimizing cell, converts it back to a legal center, and recounts every atom using
exact inequalities. A missing cell, invalid center, or disagreeing recount is a
rejection, not a successful partial proof.

## 5. Boundary coverage

The domain is a closed convex polygon with positive area. Every boundary or
event point is a limit of non-event interior domain points. The arrangement is
finite, so a subsequence lies in one cell. Each atom captured throughout that
cell remains captured at the limit because capture rectangles are closed.
Nonnegative weights imply that the boundary charge cannot be less than that
cell's charge. Thus checking all reachable open cells establishes the same lower
bound everywhere in the closed domain. Degenerate domains are rejected.

## 6. Global counting and a strict bound

Fold each physical parent's orientation separately using square periodicity and
a container reflection. This places it in the catalogue's covered angle range.
D4 invariance preserves mass under the fold and its inverse; it does NOT impose
symmetry on a hypothetical packing.

Choose one certified core for each parent. The choices may differ in direction
and size, but consume the same measure. Because the chosen closed cores are
strictly inside pairwise disjoint parent interiors, the cores are disjoint. If
seventeen A-parents existed in `[0,L]^2`, then

    17*gamma <= sum_i mu(core_i) <= M < 17*gamma,

an impossibility. Scaling a proposed unit-square packing at side `L/A` by A gives
exactly such a forbidden parent packing. No packing exists at the endpoint itself.

The minimum defining s(17) is attained: a five-by-five grid supplies a finite
upper bound; center, angle, and side variables then range over compact sets;
containment and interior-nonoverlap define a closed feasible set. If the infimum
were `L/A`, it would produce the just-excluded packing. Hence **s(17) > L/A**.
This same compactness observation strengthens the conservatively stated weak
inequality of R012; it is not a correction to a false R012 claim.

## 7. Arithmetic trust boundary

The C++ geometric arithmetic uses Boost unbounded integers, with denominators
cleared using common multiples. No floating-point geometric comparison is used.
Weights are accumulated as signed 64-bit integers. Input validation bounds the
sum of nonnegative weights by 10^12, well below the accumulator and sentinel
limits. Rectangle insertion/removal may use signed updates but represents a
nonnegative atomic measure.

The Python wrapper uses exact Fraction arithmetic for every angle, parent inset,
strict margin, and endpoint comparison. It rejects incomplete interval unions,
invalid source identities, and a counting budget that does not close. A printed
expected minimum in a JSON file is checked against newly computed minima.

The two C++ accumulators are not independently designed geometric proofs. The
source-distinct Python implementation supplies further cross-checks of the same
rectangle-arrangement approach. Neither language diversity nor passing test cases
replaces mathematical review. This is a computer-assisted proof, not a theorem
formalized in a proof assistant; independent external review remains outstanding.

## 8. Extension to threshold atoms (theorem only; not used in the new bound)

Levy's threshold atom `(S,k,w)` charges w when a core contains at least k distinct
points of S. Its budget is `w*floor(|S|/k)`: disjoint cores have disjoint traces on
S, so at most that many cores can reach the threshold. The elementary two-of-three
case has budget w, not 3w or 3w/2.

The parent-angle catalogue above transfers this charging rule without change.
For any D4-invariant collection of point and threshold atoms, substitute total
charge for mu(core), and substitute the sum of their budgets for M. Complete
parent-envelope coverage at gamma and total budget below `17*gamma` imply the
same strict lower bound. The proof is exactly the disjoint-core argument above.

This is a useful combination of Guzhou's transport and Levy's charging rule, not
a claim to have invented threshold atoms. A new n=17 threshold certificate has
NOT been computed here. The current numerical certificate uses point atoms only.
