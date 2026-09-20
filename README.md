# Packing 17 unit squares in a square

This repository archives exact lower-bound certificates, numerical constructions,
and research code for the 17-squares-in-a-square problem.

Let `s(17)` be the least side length of a square containing 17 pairwise
interior-disjoint unit squares, with arbitrary rotations.

## Current interval

The strongest retained exact computer-assisted lower bound is

\[
\boxed{s(17)>\frac{46129999999859}{9997499999900}}
=\boxed{4.614153538416645696808\ldots}.
\]

The best known construction is John Bidwell's 1998 packing,

\[
\boxed{s(17)\le 4.6755300936045509516\ldots}.
\]

Thus the current retained interval is

\[
4.614153538416645696808\ldots<s(17)
\le4.6755300936045509516\ldots.
\]

No global proof of Bidwell optimality is claimed.

## Current theorem and parent-aware base certificate

The computational base certificate is
[`certificates/lower_bound_4p614153`](certificates/lower_bound_4p614153).
It works in an outer square of side `L = 4.613` and excludes seventeen parent
squares of side `A = 3999/4000`. Scaling gives the unit-square target

```text
L/A = 18452/3999 = 4.61415353838459614903...
```

The base exact certificate has:

- **3,280** weighted atoms in **417** positive `D4` orbits;
- total mass **16.999991644**;
- **4,391** continuous parent-angle intervals;
- minimum selected-core mass **1.000000030**;
- counting surplus `17*minimum - mass = 0.000008866`;
- **27,918,671** exact center slabs in the full replay.

The base certificate's key improvement is **parent-aware coverage**. For an entire parent-angle
interval, the verifier computes the complete center domain attainable by legal
parent squares, selects a concentric core strictly inside every parent in that
interval, and checks every translation of that core over that legal domain. This
builds directly on Guzhou0806's R012 certificate and removes constraints arising
from auxiliary cores that could fit near a wall even though their parent square
could not.

```bash
python3 certificates/lower_bound_4p614153/verify.py \
  --output /tmp/n17-parent-aware --upstream --direct
python3 certificates/lower_bound_4p614153/test_verify.py
```

The replay needs Python 3.10+, a C++17 compiler with OpenMP, and Boost headers.
The numerical optimizer is not part of the trusted proof path.

## Paper and research lineage

The paper follows the proof from disjoint-core counting and parent geometry to
the exhaustive finite verification, the base certificate, and the recentering
improvement. A separate section proves the finite intersection-trigger
separation. Reproduction details, supplementary results, and the dated history
of improvements are in appendices.

- [Rendered PDF](paper/17squares-lower-bound.pdf)
- [LaTeX source](paper/main.tex)
- [Paper build notes](paper/README.md)
- [Contributors and source links](CONTRIBUTORS.md)

The contributors page distinguishes direct dependencies from parallel and
historical results. It includes links for Mira, Stanislav Fort, Joshua Levy,
Guzhou0806, Sam Burns, Gustavo Massaccesi's audited certificate, anabologyco-maker,
Trevor Green/Friedman, Stromquist, Nagamochi, David MacIver, Bidwell, and other
relevant sources.

## Progression retained in this repository

| Bound | Role |
|---:|---|
| `4.468292` | historical exact sixteen-point certificate with triangle witnesses |
| `4.607028598640...` | weighted certificate plus exact dilation endpoint |
| `4.613028635886...` | preceding weighted certificate plus dilation |
| `4.614153538384596...` | parent-aware computational base theorem |
| `4.614153538416645...` | current analytic recentering corollary |

Additional intermediate and external milestones are documented in
[`RESULTS.md`](RESULTS.md) and [`CONTRIBUTORS.md`](CONTRIBUTORS.md).

## Repository map

- [`certificates/lower_bound_4p614153`](certificates/lower_bound_4p614153) — current parent-aware exact certificate and replay.
- [`certificates/lower_bound_4p607`](certificates/lower_bound_4p607) — previous weighted theorem and source lineage from Levy's 4.59 certificate.
- [`certificates/lower_bound_4p613`](certificates/lower_bound_4p613) — preceding weighted theorem and diagnostics.
- [`certificates/lower_bound_4p468292`](certificates/lower_bound_4p468292) — historical exact triangle-witness certificate.
- [`paper`](paper) — current technical paper, source, and rendered PDF.
- [`PROVENANCE.md`](PROVENANCE.md) — trust classes and claim discipline.
- [`VERIFY.md`](VERIFY.md) — exact reproduction guide.

All retained checks run with:

```bash
bash ./verify_all.sh
```

## Status and trust

The current theorem is an exact computer-assisted proof with reproducible
rational data and integer/rational verification. The two C++ accumulation
backends in the current package share a geometric partition and are not
represented as independent geometric proofs. The pinned R012 Python kernel is
also replayable for the upstream parent-angle certificate.

The repository does **not** claim peer review, a completed proof-assistant
formalization of the parent-aware theorem, or global optimality of Bidwell's
packing. Numerical search outputs remain research evidence rather than theorems.


## Stronger mathematical framework

The paper now proves two extensions beyond the base weighted certificate.

First, certified cores may be **recentered inside their physical parent** rather
than remaining concentric. An exact Minkowski/erosion criterion reuses the old
coverage domains and yields the current rational headline bound without another
global coverage sweep.

Second, **intersection-trigger atoms** compile finite pose incompatibilities
into budgeted spatial charges. The paper proves their budget and describes their
coverage geometry. They are not used in the headline numerical bound.

The [verified 29-pose trigger example](certificates/intersection_trigger_29/)
exhibits a budget-one charge whose coverage on those cores would require
positive spatial mass at least `81407286808/59431493389 = 1.3697668048682659...`.
Its independent exact load check does not change the packing bound.
