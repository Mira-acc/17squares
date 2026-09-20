# Result ledger

This file separates exact theorems from historical milestones, external source
reports, and numerical search outcomes.

## Current exact lower bound

\[
\boxed{s(17)>
\frac{46129999999859}{9997499999900}}
=4.614153538416645696808\ldots.
\]

Computational base package: [`certificates/lower_bound_4p614153/`](certificates/lower_bound_4p614153/)

Analytic sharpening: [`research/recentered_cores_and_intersection_triggers/`](research/recentered_cores_and_intersection_triggers/)

The certificate is instantiated at outer side `L = 4613/1000` with parent side
`A = 3999/4000`. It has 3,280 atoms in 417 positive D4 orbits, total mass
`4249997911/250000000 = 16.999991644`, and 4,391 continuous parent-angle
intervals. The exact sweep finds minimum selected-core mass
`100000003/100000000 = 1.000000030`. Therefore

```text
17 * minimum - mass = 4433/500000000 = 0.000008866 > 0.
```

The full replay checks 27,918,671 center slabs. Scaling converts exclusion of
seventeen side-`A` parents in the side-`L` outer square into exclusion of unit
squares at `L/A = 18452/3999`. Since feasibility is attained at the minimum,
the resulting lower bound is strict.

## Exact milestones retained locally

| Result | Status | Package |
|---|---|---|
| `s(17) > 46129999999859/9997499999900 = 4.614153538416645...` | Current analytic corollary of the parent-aware certificate | `paper/main.tex`; `research/recentered_cores_and_intersection_triggers/` |
| `s(17) > 18452/3999 = 4.614153538384596...` | Parent-aware computational base theorem | `certificates/lower_bound_4p614153/` |
| `s(17) > 4.613028635886` | Preceding weighted theorem and dilation | `certificates/lower_bound_4p613/` |
| `s(17) > 4.468292` | Historical exact triangle-witness certificate | `certificates/lower_bound_4p468292/` |
| `s(17) > 4.607028598640` | Strict decimal below the previous exact dilation endpoint | `certificates/lower_bound_4p607/` |
| `s(17) > 4.607` | Previous weighted base certificate | `certificates/lower_bound_4p607/` |

The current theorem numerically subsumes all earlier lower bounds. Earlier
packages remain important for provenance and independent proof architectures.

## Parent-aware progression

Guzhou0806's pinned R012 certificate proves

```text
s(17) >= 461300/99999 = 4.61304613046130461304...
```

using a rounded/reverified version of the preceding 4.613 measure and a complete
parent-angle catalogue. Our audit found its parent-domain reduction and counting
argument sound. Compactness also upgrades exclusion at the displayed side to a
strict inequality.

With the R012 measure unchanged, the research notes report the intermediate
adaptive parent-aware target

```text
922600/199979 = 4.61348441586366568489...
```

The intermediate certificate is not retained here; it is not a replayed result
of this package. An exact legal parent then blocks that frozen measure under the same common-charge
proof format at

```text
461300/99989 = 4.61350748582344057846...
```

because the entire parent captures only `0.998982` mass. Reweighting and then
mixing retained with wall-adjusted support produces the current `18452/3999`
certificate. This fixed-measure obstruction is not an upper bound on `s(17)` or
on other certificate families.

## Contemporary external milestones

For method and priority context, the public 2026 sequence includes Stanislav
Fort's exact `4.456575`, Sam Burns's weighted `4.4811`, Gustavo Massaccesi's
weighted `4.5058`, anabologyco-maker's `4.5705`, Joshua Levy's verified `4.59`,
and Guzhou0806's parent-aware R012. See [`CONTRIBUTORS.md`](CONTRIBUTORS.md) for
links, exact roles, and verification caveats.

## Upper-bound benchmark

| Packing | Side length `L` | Interpretation |
|---|---:|---|
| Bidwell | `4.6755300936045509516...` | Best known 17-square construction |
| Cantrell symmetric basin | `4.680125311320454` | Inferior symmetric local maximum retained here |
| Hämäläinen | `4.8228756555...` for 18 squares | Historical source construction used in deletion experiments |

No construction in this repository improves Bidwell.

## Numerical and optimality research

Exploratory packing states, tangent MILPs, local topology searches, and other
floating-point outputs are not lower-bound theorems. Separate research has
produced evidence and computer-assisted local results around Bidwell, but the
current global result remains the interval stated above. A proof that every
possible packing falls into the locally controlled family is still missing.

## Open target

A complete solution requires either:

1. a verified 17-square packing with side below Bidwell's value; or
2. a global lower-bound argument reaching Bidwell's side.


## Analytic recentering corollary

The current headline theorem reuses the already certified core shapes and
center domains. A core need not remain concentric with its physical parent; it
may be translated to any previously covered center as long as it stays strictly
inside the parent.

With parent decrement `epsilon = 10^-11` and container decrement
`delta = 1.41*10^-11`, the finite interval margins satisfy the recentering
criterion. Therefore the same budget excludes the slightly smaller parents in
the slightly smaller container, giving

```text
46129999999859/9997499999900
= 4.614153538416645696808...
```

This route is nearly exhausted for the frozen core/domain library: its
axis-aligned reuse cap is about `4.61415353842273443435`. That is a cap only
on this particular reuse strategy, not on the packing problem or on new
certificate families.

## Compatibility-aware charge framework

The paper also proves an intersection-trigger construction. Pairwise-intersecting
nonempty finite triggers define a budget-one charge, with fixed-direction
coverage represented by a union of rectangles. No checked numerical separation
from positive spatial mass or improved n=17 bound is claimed for this extension.
