# Packing 17 unit squares in a square

Let `s(17)` be the least side length of a square containing 17 pairwise
interior-disjoint unit squares, with arbitrary orientations. This repository
contains an exact computer-assisted proof that

\[
\boxed{s(17)>4.613028635886}.
\]

The base certificate excludes a packing at side `4.613`. Uniform dilation gives

```text
s(17) >= sqrt(17650291964463886688094912400 /
             829429719507765981945905041)
       = 4.6130286358861101094200443452...
```

The radical endpoint has a weak inequality; rational squaring verifies that the
displayed strict decimal is smaller. The cited Bidwell construction gives the
upper bound `s(17) <= 4.67553009360455...`.

## Read the proof

- [Paper (PDF)](paper/17squares-lower-bound.pdf)
- [LaTeX source](paper/main.tex) and [build notes](paper/README.md)
- [Weighted certificate package](certificates/lower_bound_4p613/README.md)
- [Exact weighted proof](certificates/lower_bound_4p613/PROOF.md)
- [Attribution and source hashes](certificates/lower_bound_4p613/ATTRIBUTION.md)

The measure assigns nonnegative rational weights to 1,620 atoms, with total
mass 16.99798498 < 17. An exact sweep checks every admissible translation of a
closed side-0.99985 core at 2,881 rational directions: the minimum mass is
1.000002103 across 9,116,871 centre slabs. A strict containment inequality covers
the intervening orientations and places the closed core inside the unit-square
interior. Seventeen disjoint interiors would require mass at least 17.

The initial 4.59 measure is credited to Joshua Levy's squares project under
CC BY 4.0. The new certificate improves the preceding weighted bound
`4.607028598640` through new spatial support and weights, with the same core
side, direction net and exact kernel. The weighted principle and sharp dilation
lemma are credited prior work.

The [review notes](certificates/lower_bound_4p613/REVIEW.md) record the replay and
scope checks. Exact diagnostics show that reweighting a specified old dictionary
cannot pass the core test at 4.61, and that deleting 19 final-stage orbits breaks
the new certificate. These are restricted statements, not global optimality
claims. See the [research report](certificates/lower_bound_4p613/RESEARCH.md).

## Verify

Requirements: Python 3.10 or newer with its standard library, C++17 and Boost headers. The historical
archive checks also require `xz`, `sha256sum` and POSIX shell tools.

Replay the current theorem, both accumulation engines, 26 geometric controls, eight diagnostic controls,
and the orbit-deletion checks:

```bash
python3 certificates/lower_bound_4p613/verify.py --source
```

Fully reproduce the current and preceding weighted theorems and historical
triangle-witness certificate:

```bash
bash ./verify_all.sh
```

See [VERIFY.md](VERIFY.md) for exact statements, hashes and expected output.
The [weighted replay workflow](.github/workflows/verify-weighted-cover.yml)
checks the new package in CI. Optimizer dependencies are unnecessary for proof
replay; optional discovery inputs are retained within the weighted package.

## Preceding weighted result

The [4.607 package](certificates/lower_bound_4p607/README.md) is retained unchanged
with its exact measure and replay logs. It remains separately reproducible with
`python3 certificates/lower_bound_4p607/verify.py --direct`.

## Historical result

The [4.468292 package](certificates/lower_bound_4p468292/README.md) remains
unchanged. Its sixteen-point proof, strict triangle-piercing lemma, coordinates
and checker interface are retained in the paper's appendix. The 122,626,747-byte
tree is stored as a deterministic 374,096-byte XZ archive. Check it without
regenerating the tree with:

```bash
bash certificates/lower_bound_4p468292/verify_archived.sh
```

## Status and trust

The weighted segment-tree and direct-prefix engines share one exact geometric
partition; their agreement is an accumulation audit, not two independent
geometric proofs. The three-checker independence statement belongs to the
historical triangle-witness package. Neither numerical discovery nor a sampled
LP result is trusted as a proof. External peer review remains pending.
