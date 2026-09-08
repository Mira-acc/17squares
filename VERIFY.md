# Verification guide

Run all current and historical checks from the repository root:

```bash
bash ./verify_all.sh
```

This replays both engines for the current and preceding weighted certificates,
then fully regenerates
and checks the historical 122,626,747-node certificate. The historical Python
check is substantially slower than weighted replay alone. Final success is
`ALL_RETAINED_CHECKS_PASSED`.

## Current weighted theorem

The weighted package proves `s(17) > 4.613028635886`. Its exact radical endpoint
is a weak lower bound:

```text
s(17) >= sqrt(17650291964463886688094912400 / 829429719507765981945905041).
```

Replay just this package with:

```bash
python3 certificates/lower_bound_4p613/verify.py --source
```

The checker validates 1,620 rational atoms of total mass 16.99798498, then
checks every translation of a closed side-0.99985 core at 2,881 directions.
The minimum mass is 1.000002103 across 9,116,871 centre slabs. Strict core
containment covers all intermediate orientations and puts every captured atom
inside the parent unit square. Seventeen disjoint interiors would require
mass at least 17. Uniform dilation gives the radical bound; rational squaring
verifies the strict decimal below it.

The replay rebuilds the segment-tree and direct-prefix accumulation engines,
runs 13 positive/refusal controls per engine, checks the pinned Levy source
and new measure, compares full logs, and validates `result.json`. It also runs
eight exact diagnostic controls, checks the 356-orbit dictionary obstruction,
and reconstructs and tests deletion of the 19 final-stage orbits in both engines. Geometry
uses unbounded integers; weight numerators are capped to protect 64-bit sums.
The engines share the geometric partition and are not independent geometric
proofs. Discovery scripts and numerical optimization are untrusted.
See the [complete proof](certificates/lower_bound_4p613/PROOF.md).

Expected current-package success marker:

```text
EXACT_REPLAY_AND_DIAGNOSTIC_PASSED
```

The imported package manifest was checked before integration. The exact kernel
and input compiler match the preceding package byte-for-byte; the new data,
diagnostics and replay orchestration are reviewed in
[REVIEW.md](certificates/lower_bound_4p613/REVIEW.md).

## Preceding 4.607 weighted certificate

```bash
python3 certificates/lower_bound_4p607/verify.py --direct
```

This retained package proves `s(17) > 4.607028598640`; it uses the same geometric
kernel with its own earlier rational measure and result ledger.

## Historical 4.468292 verification

### The checked statement

The certificate proves:

> Every unit square contained in `[0, 4468292/1000000]^2`, at any orientation,
> contains at least one of the listed sixteen rational points strictly in its
> interior.

Point leaves prove this directly. Triangle leaves prove that the complete center
rectangle lies strictly inside a triangle whose three sides are strictly shorter
than one. The triangle-piercing lemma then puts at least one triangle vertex in
the square interior, regardless of orientation.

The pigeonhole principle rules out seventeen pairwise interior-disjoint unit
squares at the displayed side length. A packing in a smaller container would
also fit there, giving `s(17) ≥ 4468292/1000000`; compactness ensures that the
least feasible side length is attained, so equality is also impossible. Hence

```text
s(17) > 4468292/1000000 = 4.468292.
```

### Full deterministic reproduction

```bash
bash certificates/lower_bound_4p468292/verify_4p468292.sh
```

This regenerates the complete tree, checks its raw SHA-256, compares it
byte-for-byte with the decompressed archive, runs all three exact checkers, and
runs malformed-certificate rejection tests.

Expected final marker:

```text
ALL_EXACT_CHECKS_PASSED_4P468292
```

### Faster archived-certificate check

```bash
bash certificates/lower_bound_4p468292/verify_archived.sh
```

This checks the archived XZ hash, decompresses it into a temporary directory,
checks the raw hash, and runs the same checkers and rejection tests without
regenerating the tree.

Expected checker markers:

```text
CERTIFICATE_VALID_4P468292
BIGINT_CERTIFICATE_VALID_4P468292
PYTHON_INTEGER_CERTIFICATE_VALID_4P468292
REJECTION_TESTS_PASSED_4P468292
ARCHIVED_CERTIFICATE_VERIFIED_4P468292
```

### Certificate hashes

```text
2838f315302d67da131745925e9ec7dd2a602bb299d1335ce25e4e13a7b7b6d2  square17_lb_4p468292.cert
a349b81e630ccf7292ae0afe6ed954591f7e88fe6289847f67883204a7ed60ac  square17_lb_4p468292.cert.xz
```

### Trust boundary

The point search, certificate generator, and certificate bytes are not trusted.
Each checker treats the tree as untrusted input and recomputes every leaf claim.
The fast checker shares an arithmetic header with the generator. The Boost and
Python arbitrary-integer checkers separately implement the point, triangle, and
infeasibility tests and do not depend on bounded-integer overflow arguments.

The arbitrary-integer checkers use no floating-point arithmetic, numerical
optimizer, solver, or interval library. The remaining human argument—the square
parameterization, interval bounds, strict triangle-piercing lemma, tree-cover
induction, pigeonhole step, and compactness step—is given in the
[paper](paper/17squares-lower-bound.pdf) and the package's
[proof interface](certificates/lower_bound_4p468292/PROOF.md).
