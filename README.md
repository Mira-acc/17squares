# Packing 17 unit squares in a square

Let `s(17)` be the least side length of a square containing 17 pairwise
interior-disjoint unit squares, with arbitrary orientations. This repository
contains an exact computer-assisted proof that

\[
\boxed{s(17)>4.607028598640}.
\]

The base certificate excludes a packing at side `4.607`. Uniform dilation gives

```text
s(17) >= sqrt(17604407342714743536607440400 /
             829429719507765981945905041)
       = 4.6070285986402151094200443452...
```

The radical endpoint has a weak inequality; rational squaring verifies that the
displayed strict decimal is smaller. The cited Bidwell construction gives the
upper bound `s(17) <= 4.67553009360455...`.

## Read the proof

- [Paper (PDF)](paper/17squares-lower-bound.pdf)
- [LaTeX source](paper/main.tex) and [build notes](paper/README.md)
- [Weighted certificate package](certificates/lower_bound_4p607/README.md)
- [Exact weighted proof](certificates/lower_bound_4p607/PROOF.md)
- [Attribution and source hashes](certificates/lower_bound_4p607/ATTRIBUTION.md)

The measure assigns nonnegative rational weights to 1,200 atoms, with total
mass 16.98264408 < 17. An exact sweep checks every admissible translation of a
closed side-0.99985 core at 2,881 rational directions: the minimum mass is
1.00000116 across 6,679,269 centre slabs. A strict containment inequality covers
the intervening orientations and places the closed core inside the unit-square
interior. Seventeen disjoint interiors would require mass at least 17.

The initial 4.59 measure is credited to Joshua Levy's squares project under
CC BY 4.0. The stronger certificate retains an orbit from Mira's earlier
4.450837 point set. The weighted principle and sharp dilation lemma are
credited prior work; the new contribution is the stronger exact certificate.

## Verify

Requirements: Python 3 standard library, C++17 and Boost headers. The historical
archive checks also require `xz`, `sha256sum` and POSIX shell tools.

Replay the current theorem, both accumulation engines and all 26 controls:

```bash
python3 certificates/lower_bound_4p607/verify.py --direct
```

Fully reproduce both the weighted theorem and historical certificate:

```bash
bash ./verify_all.sh
```

See [VERIFY.md](VERIFY.md) for exact statements, hashes and expected output.
The [weighted replay workflow](.github/workflows/verify-weighted-cover.yml)
checks the new package in CI. Optimizer dependencies are unnecessary for proof
replay; optional discovery inputs are retained within the weighted package.

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
