# Exact weighted-cover lower bounds for 17 unit squares

Prepared for Mira, 7 September 2026. This is a computer-assisted proof with an
explicit, auditable arithmetic kernel, not a Lean formalization or a claim of
external peer review. The final numerical record is supplied separately; this
proof applies to every certificate accepted by the kernel.

## 1. Problem and weighted contradiction

Let s(17) be the infimum of side lengths of axis-aligned containing squares that
admit seventeen unit squares with arbitrary orientations and pairwise disjoint
interiors. The small squares may touch each other and the container.

In Q_L = [0,L]^2 put a finite nonnegative measure

    mu = sum_j w_j delta_(x_j,y_j),  w_j >= 0.

If its total mass is below 17 and every contained unit square U satisfies
mu(int U) >= 1, seventeen such squares cannot have disjoint interiors: their
interior masses sum to at least 17 and at most mu(Q_L) < 17.

A sixteen-point unavoidable set is the special case of sixteen weights equal
to one. There is no restriction to sixteen support points in the weighted
version. A support with over a thousand points can still have mass below 17.

## 2. Certificate conditions

The input consists of rational L,B, rational atom coordinates and weights, and
an integer m > 0. This kernel uses the fixed rational endpoint

    T = 207107/500000,
    t_k = k T/m,  k = 0,...,m,
    theta_k = 2 arctan(t_k),
    h = T/m.

It checks the following sufficient conditions, without trusting the JSON's
claim or declared mass:

1. All atoms lie in Q_L; their weights are nonnegative; total mass is <17.
2. The measure is invariant under the eight symmetries D4 of Q_L.
3. T^2 + 2T >= 1, so the net extends at least as far as theta = pi/4.
4. B^2 (1+h)^2 < 1+h^2.
5. Every closed side-B square contained in Q_L at every theta_k has mass >=1.

The implementation additionally requires a positive-area centre domain at
every direction. It conservatively refuses inputs outside this supported
case. This extra requirement holds for all retained packing certificates.

D4 invariance is a restriction on the certificate, not on a hypothetical
packing. Individual squares in a packing can have entirely different angles.
A general feasible nonnegative measure could also be averaged over D4 without
changing its total mass or its universal coverage inequality.

## 3. Why finitely many directions cover ALL orientations

By the symmetries of the container and of a square, it suffices to treat a
single square whose orientation lies in [0,pi/4]. Between consecutive net
angles, its distance delta from the nearest net angle is at most half the net
gap. The half-gap identity gives

    tan((theta_(k+1)-theta_k)/2)
      = (t_(k+1)-t_k)/(1+t_k t_(k+1)) <= h.

Consequently 0 <= tan(delta) <= h < 1. For 0 <= z <= h < 1,

    (1+h)^2(1+z^2) - (1+z)^2(1+h^2)
      = 2(h-z)(1-hz) >= 0.

Thus

    cos(delta)+sin(delta) <= (1+h)/sqrt(1+h^2).

A concentric side-B square at the selected net angle has half-width
B(cos(delta)+sin(delta))/2 when projected on either axis of the unit square.
Condition 4 makes both projections strictly less than 1/2. The CLOSED core is
therefore strictly inside the OPEN interior of the unit square.

The core lies in Q_L, so Condition 5 gives it mass >=1. This proves
mu(int U) >=1. In particular, a support point on the boundary of a closed core
is safely in the interior of its parent unit square. Touching between different
unit squares cannot double-count it. This is the key boundary safeguard.

The angle net is not a numerical sampling argument. The entire gaps are paid
for by the exact strict support-containment inequality above.

## 4. Exact reduction of translations to an event arrangement

Here is the complete finite argument behind Condition 5.

Centre the container at the origin. At a fixed angle write c=cos(theta)>0 and
s=sin(theta)>=0. The centres of contained side-B squares form the axis-aligned
square [-H,H]^2, where H=(L-B(c+s))/2>0.

Rotate the centre coordinates by

    u = c x + s y,       v = -s x + c y.

In these coordinates a fixed atom contributes its weight exactly on a closed
rectangle [u_j-B/2,u_j+B/2] x [v_j-B/2,v_j+B/2]. The admissible centre domain D is

    |c u - s v| <= H,    |s u + c v| <= H.

All rectangle-edge u coordinates, together with the two extreme u coordinates
of D, partition the u axis into open slabs. The set of atom rectangles active
in u is constant within a slab. All rectangle-edge v coordinates partition the
v axis into open intervals; the covered mass is constant on each slab/interval
cell.

It remains to identify exactly which cells meet int(D). For a slab (a,b), its
intersection with int(D) is convex, open and connected. Its projection on the v
axis is an open interval (v_min,v_max). The values below give its exact infimum
and supremum, even when the extremum occurs at an endpoint of the slab.

For s>0 the lower and upper boundaries of D are

    lower(u) = max((c u-H)/s, (-H-s u)/c),
    upper(u) = min((c u+H)/s, (H-s u)/c).

The lower boundary is a V with minimum at u=H(c-s); the upper boundary has its
maximum at u=-H(c-s). Clamp these two u values to [a,b] and evaluate the
respective functions to obtain v_min and v_max. When s=0, the interval is
simply (-H,H).

A v cell is reachable exactly when its open interval intersects
(v_min,v_max). This requires only comparisons of rational numbers. In
particular, merely touching at an endpoint does not create a spurious open
cell. An exact range-minimum query then checks all reachable v cells in that
slab simultaneously.

### Boundaries of the arrangement and of D

The sweep checks the full-dimensional open cells. This suffices for CLOSED
cores and nonnegative atomic weights. Every boundary placement is a limit of
placements in int(D) that avoid all the finitely many event lines. Since the
arrangement is finite, take a subsequence from one fixed open cell. Every atom
captured throughout that cell is still captured at its limiting placement:
closed-square membership is a closed condition. The boundary placement can
therefore only gain mass relative to this limiting cell, not lose it.

This covers simultaneous events, coincident atom projections, container-wall
contacts, arrangement vertices and degenerate event coincidences. It does not
justify using closed unit-square interiors in the packing contradiction; that
separate issue is handled by the strict core inclusion in Section 3.

## 5. Integer coordinates used by the verifier

Choose G so that the following numbers are integers:

    X_j = G(x_j-L/2), Y_j = G(y_j-L/2),
    ell = G L/2,      b0 = G B/2.

For a reduced half-tangent p/q, define integer Pythagorean coordinates

    C=q^2-p^2,  S=2pq,  R=q^2+p^2,
    c=C/R,     s=S/R.

Set

    H0 = ell R - b0(C+S),
    E  = H0(C+S),
    V0 = H0(C-S),
    K  = R^2 H0,
    J  = b0 R^2.

The projected coordinates, in units 1/(R^2 G), are

    U_j = R(C X_j + S Y_j),
    V_j = R(-S X_j + C Y_j).

An atom's rectangle edges are U_j +/- J and V_j +/- J. The admissible domain is

    |C U-S V| <= K,  |S U+C V| <= K,

with U extent [-E,E]. The lower-boundary minimum has U coordinate V0 and the
upper-boundary maximum has U coordinate -V0. Formulae in Section 4 become

    lower(U) = max((C U-K)/S, (-K-S U)/C),
    upper(U) = min((C U+K)/S, (K-S U)/C).

Every geometry operation uses Boost.Multiprecision cpp_int, with no floating
point and no fixed-width geometry overflow. Rational order tests use
cross-multiplication with positive denominators.

Weights are integer numerators with one common denominator W. Their sum is
restricted to at most 10^12, which safely bounds the signed 64-bit accumulation
and segment-tree intermediate values. The kernel explicitly refuses overflow
risk, negative weights, malformed dimensions, extra trailing input, broken D4
symmetry and insufficient total-mass or angular slack.

A difference-array/prefix-sum engine also checks the exact same cells. It is an
independent implementation of weight accumulation, NOT an independent proof of
the geometric partition. Its complete output is compared byte-for-byte with
the segment-tree engine. Positive and deliberately invalid controls are run
against both engines.

## 6. Strict bound and strongest uniform-dilation corollary

Let a retained certificate at (L,B,m) satisfy the conditions above and put

    C0 = sqrt(1+h^2)/(B(1+h)) > 1,
    S_star = C0 L.

For every rational 0<r<C0, multiply L,B and every atom coordinate by r, leaving
weights and net directions fixed. Inverse scaling is a bijection of the core
placements, so coverage, total mass and symmetry are unchanged. The strict
angular condition still holds. Hence no seventeen-square packing exists at
side rL. Embedding smaller containers into larger ones rules out all smaller
sides too. Taking rational r increasing to C0 proves

    s(17) >= S_star = L sqrt(1+h^2)/(B(1+h)).

In particular, because C0>1, this implies s(17)>L without needing a compactness
argument. Any rational a<S_star yields the strict bound s(17)>a. Such a
comparison can be verified with integer arithmetic by testing a^2<S_star^2.

At the radical endpoint itself, the uniform strict support-containment
inequality becomes equality. We claim the weak inequality there, not strict
exclusion at the radical endpoint. We do NOT claim S_star is optimal among all
possible certificates or all consequences of these atom locations.

This sharper dilation lemma is already present in Joshua Levy's T-022 note
for eleven squares. Its use here is credited as an existing corollary; the new
contribution is the independently verified stronger 17-square certificate.

## 7. What numerical optimization does and does not prove

For D4 orbits O_j with one per-atom weight w_j, the discovery program minimizes

    sum_j |O_j| w_j

subject to

    sum_j (# of atoms in O_j captured by a placement) w_j >= 1,
    w_j >= 0.

It uses floating-point linear programming and counterexample-row generation.
That program is deliberately untrusted. Its candidate weights are rounded
upward to exact rationals, zero weights are removed, and the FULL exact
geometric check is rerun. No optimality assertion about the LP is needed for a
valid packing lower bound. Conversely, a sampled or numerical feasible output
is not promoted to a lower bound until exact replay accepts it.

An LP objective above 17 at a trial side is recorded only as a numerical
obstruction for that particular finite support/constraint family. It is not a
packing construction, a global limit on this method, or a disproof of a higher
lower bound.

## Source attribution

The initial 1184-point rational certificate is by Joshua Levy, the squares
project, https://github.com/jlevy/squares. Its exact source is
packing/cases/n17_fractional_certificate/certificate.json, Git blob SHA-1
f454e44dee1f2318af45e02efdfff5fcd7dbfbe1 and SHA-256
461cb731917bdaf7a58f54be651ca2c782bc519790d79d0fe4941c24fdd4c652.
It was reconstructed from the connector's exact text and its Git blob hash
matched byte-for-byte. The source data are attributed under CC BY 4.0.

The weighted-unavoidable-set principle predates the present calculation.
Levy's generator documents the same covering-LP / separation-oracle strategy.
Mira's earlier proof is the integral sixteen-point specialization. This package
supplies new certificate data and uses the independent arithmetic checker
implemented for the preceding 4.607 calculation, unchanged in this continuation.
It makes no ownership claim over the weighted-cover principle.

## 8. Parameters and exact finite premise for this continuation

For the final data in `best-certificate.json`, the integer sweep accepts

    L = 4613/1000, B = 19997/20000, m = 2880,
    number of atoms = 1620,
    total mass = 849899249/50000000 < 17,
    minimum net-core mass = 1000002103/1000000000 >= 1,
    center slabs checked = 9116871.

Sections 2–5 therefore establish the weighted contradiction in Section 1 at
this side. Section 6 gives

    s(17) >= sqrt(17650291964463886688094912400 /
                  829429719507765981945905041)
          > 4.613028635886.

The final strict comparison is rational after squaring positive quantities.
No numerical optimizer premise is used in this implication.
