# Verification guide

## The checked statement

The certificate proves:

> Every unit square contained in `[0, 4450837/1000000]^2`, at any orientation,
> contains at least one of the listed sixteen rational points strictly in its
> interior.

The pigeonhole principle therefore rules out seventeen pairwise
interior-disjoint unit squares at that side length. A packing in a smaller
container would also fit there, giving `s(17) ≥ 4450837/1000000`; compactness
ensures that the least feasible side length is attained, so equality is also
impossible. Hence

```text
s(17) > 4450837/1000000 = 4.450837.
```

## One-command reproduction

```bash
bash ./verify_all.sh
```

The script:

1. compiles the deterministic generator and both C++ checkers;
2. regenerates the complete subdivision tree in a temporary directory;
3. checks the generated and archived SHA-256 hashes;
4. compares the two trees byte-for-byte;
5. runs the fast C++, arbitrary-precision C++, and arbitrary-precision Python
   checkers on the regenerated tree.

The expected success markers are:

```text
CERTIFICATE_VALID
BIGINT_CERTIFICATE_VALID
PYTHON_INTEGER_CERTIFICATE_VALID
ALL_EXACT_CHECKS_PASSED
```

## Trust boundary

The point search, certificate generator, and certificate bytes are not trusted.
Each checker treats the tree as untrusted input and recomputes every leaf claim.
The fast checker shares an arithmetic header with the generator. The Boost and
Python arbitrary-integer checkers separately implement the leaf tests and do not
depend on a bounded-integer overflow argument.

All theorem-critical comparisons in the arbitrary-integer checkers are exact.
They use no floating-point arithmetic, numerical optimizer, solver, or interval
library.

The remaining human argument—the square parameterization, interval bounds,
tree-cover induction, pigeonhole step, and compactness step—is given in the
[paper](paper/17squares-lower-bound.pdf).
