# Exact lower bound `s(17) > 4.450837`

The sixteen rational points in [`points.json`](points.json) are strictly
unavoidable in the square

```text
L = 4450837/1000000 = 4.450837.
```

The exact certificate is accepted by a fast fixed-width C++ checker and by
separately implemented Boost and Python arbitrary-integer checkers. Its tree has
3,341,159 nodes and maximum depth 81.

Certificate SHA-256:

```text
49ee8134ccf636224432d235fc3c1db2f8d6a567efe9e4c08b2e81639172cfeb
```

The theorem proved is:

> Every unit square contained in
> `[0,4450837/1000000]^2`, at every orientation, contains one of the 16
> listed rational points strictly in its interior.

Seventeen pairwise interior-disjoint unit squares would require 17 distinct
interior witnesses but only 16 points are available, so such a packing cannot
exist even at equality. A packing in any smaller square would also fit at this
side length, and compactness ensures that the least feasible side length is
attained. Therefore `s(17) > 4.450837`.

A human-readable account is available in the
[`paper`](../../paper/17squares-lower-bound.pdf).

## Reproduction

From the repository root:

```bash
bash ./verify_all.sh
```

The deterministic generator reproduces the exact certificate hash above. The
generator is not part of the trusted proof core; each checker treats the tree
as untrusted and validates every claimed leaf. The two arbitrary-integer
checkers do not reuse the generator's arithmetic routines.
